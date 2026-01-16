<?php

declare(strict_types=1);

function json_response(int $statusCode, array $payload): void
{
    http_response_code($statusCode);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($payload, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
}

function get_env_or_empty(string $key): string
{
    $value = getenv($key);
    return $value === false ? '' : (string) $value;
}

function get_request_path(): string
{
    $uri = $_SERVER['REQUEST_URI'] ?? '/';
    $path = parse_url($uri, PHP_URL_PATH);
    return is_string($path) ? $path : '/';
}

function get_request_method(): string
{
    return strtoupper($_SERVER['REQUEST_METHOD'] ?? 'GET');
}

function get_header_value(string $name): string
{
    // Most PHP+Apache setups expose headers via getallheaders().
    $headers = function_exists('getallheaders') ? getallheaders() : [];
    if (is_array($headers)) {
        foreach ($headers as $k => $v) {
            if (strcasecmp((string) $k, $name) === 0) {
                return is_array($v) ? (string) ($v[0] ?? '') : (string) $v;
            }
        }
    }

    // Fallback for some SAPIs.
    $key = 'HTTP_' . strtoupper(str_replace('-', '_', $name));
    $value = $_SERVER[$key] ?? '';
    return is_string($value) ? $value : '';
}

function read_raw_body(): string
{
    $raw = file_get_contents('php://input');
    return $raw === false ? '' : $raw;
}

function compute_hmac_sha256_hex(string $body, string $secret): string
{
    return hash_hmac('sha256', $body, $secret);
}

function constant_time_equals(string $a, string $b): bool
{
    return hash_equals($a, $b);
}

function require_json_body(string $rawBody): array
{
    if ($rawBody === '') {
        json_response(400, ['error' => 'empty_body', 'message' => 'Request body is empty']);
        exit;
    }

    $decoded = json_decode($rawBody, true);
    if (!is_array($decoded)) {
        json_response(400, ['error' => 'invalid_json', 'message' => 'Body must be valid JSON']);
        exit;
    }

    return $decoded;
}

function require_shared_secret(): string
{
    $secret = get_env_or_empty('PARTNER_SHARED_SECRET');
    if ($secret === '') {
        json_response(500, ['error' => 'missing_config', 'message' => 'PARTNER_SHARED_SECRET is not configured']);
        exit;
    }
    return $secret;
}

function verify_hmac_or_401(string $rawBody, string $secret): void
{
    $signature = trim(get_header_value('X-Signature'));
    if ($signature === '') {
        json_response(401, ['error' => 'missing_signature', 'message' => 'X-Signature header is required']);
        exit;
    }

    $expected = compute_hmac_sha256_hex($rawBody, $secret);

    // Normalize to lowercase hex.
    $signatureNorm = strtolower($signature);
    $expectedNorm = strtolower($expected);

    // Basic sanity: hex length should be 64 for sha256.
    if (!preg_match('/^[0-9a-f]{64}$/', $signatureNorm)) {
        json_response(401, ['error' => 'invalid_signature_format', 'message' => 'X-Signature must be 64 hex chars']);
        exit;
    }

    if (!constant_time_equals($expectedNorm, $signatureNorm)) {
        json_response(401, ['error' => 'invalid_signature', 'message' => 'Signature verification failed']);
        exit;
    }
}

function handle_health(): void
{
    json_response(200, ['status' => 'ok', 'service' => 'partner-php']);
}

function handle_partner_webhook(): void
{
    if (get_request_method() !== 'POST') {
        json_response(405, ['error' => 'method_not_allowed', 'message' => 'Use POST']);
        return;
    }

    $secret = require_shared_secret();
    $rawBody = read_raw_body();

    verify_hmac_or_401($rawBody, $secret);

    $payload = require_json_body($rawBody);

    $event = $payload['event'] ?? null;
    $data = $payload['data'] ?? null;
    $timestamp = $payload['timestamp'] ?? null;
    $source = $payload['source'] ?? null;

    if (!is_string($event) || $event === '') {
        json_response(400, ['error' => 'invalid_payload', 'message' => 'Field "event" is required']);
        return;
    }
    if (!is_array($data)) {
        json_response(400, ['error' => 'invalid_payload', 'message' => 'Field "data" must be an object']);
        return;
    }
    if (!is_string($timestamp) || $timestamp === '') {
        json_response(400, ['error' => 'invalid_payload', 'message' => 'Field "timestamp" is required']);
        return;
    }
    if (!is_string($source) || $source === '') {
        json_response(400, ['error' => 'invalid_payload', 'message' => 'Field "source" is required']);
        return;
    }

    json_response(200, ['status' => 'ack', 'received_event' => $event]);
}

function http_post_json(string $url, string $jsonBody, array $headers, int $timeoutSeconds = 10): array
{
    $headerLines = [];
    foreach ($headers as $k => $v) {
        $headerLines[] = $k . ': ' . $v;
    }

    $context = stream_context_create([
        'http' => [
            'method' => 'POST',
            'header' => implode("\r\n", $headerLines),
            'content' => $jsonBody,
            'timeout' => $timeoutSeconds,
            'ignore_errors' => true, // capture response body even for 4xx/5xx
        ],
    ]);

    $responseBody = @file_get_contents($url, false, $context);
    $responseBodyStr = $responseBody === false ? '' : $responseBody;

    $responseHeaders = $http_response_header ?? [];
    $statusCode = 0;
    if (is_array($responseHeaders) && isset($responseHeaders[0]) && is_string($responseHeaders[0])) {
        if (preg_match('#^HTTP/\\d+\\.\\d+\\s+(\\d+)#', $responseHeaders[0], $m)) {
            $statusCode = (int) $m[1];
        }
    }

    return [
        'status_code' => $statusCode,
        'response_body' => $responseBodyStr,
        'response_headers' => $responseHeaders,
    ];
}

function handle_partner_trigger(): void
{
    if (get_request_method() !== 'POST') {
        json_response(405, ['error' => 'method_not_allowed', 'message' => 'Use POST']);
        return;
    }

    $secret = require_shared_secret();

    // Opcional: si el receptor requiere identificar al partner (ej: payment-service exige X-Partner-Id)
    $partnerId = trim(get_env_or_empty('PARTNER_ID'));

    // Preferimos TARGET_URL (según guía Semana 3); mantenemos compatibilidad con OUR_PARTNER_HANDLER_URL.
    $targetUrl = get_env_or_empty('TARGET_URL');
    if ($targetUrl === '') {
        $targetUrl = get_env_or_empty('OUR_PARTNER_HANDLER_URL');
    }
    if ($targetUrl === '') {
        json_response(500, ['error' => 'missing_config', 'message' => 'TARGET_URL (or OUR_PARTNER_HANDLER_URL) is not configured']);
        return;
    }

    $eventPayload = [
        'event' => 'tour.purchased',
        'data' => [
            'order_id' => 'order_' . bin2hex(random_bytes(6)),
            'amount' => 123.45,
            'currency' => 'USD',
        ],
        'timestamp' => gmdate('c'),
        'source' => 'partner-php',
    ];

    $jsonBody = json_encode($eventPayload, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    if (!is_string($jsonBody)) {
        json_response(500, ['error' => 'encode_failed', 'message' => 'Failed to encode JSON payload']);
        return;
    }

    $signature = compute_hmac_sha256_hex($jsonBody, $secret);

    $headers = [
        'Content-Type' => 'application/json',
        'X-Signature' => $signature,
    ];
    if ($partnerId !== '') {
        $headers['X-Partner-Id'] = $partnerId;
    }

    $result = http_post_json(
        $targetUrl,
        $jsonBody,
        $headers,
        10
    );

    json_response(200, [
        'status' => 'sent',
        'target_url' => $targetUrl,
        'signed_with' => 'HMAC-SHA256',
        'partner_id_header_sent' => $partnerId !== '' ? $partnerId : null,
        'event' => $eventPayload['event'],
        'downstream' => [
            'status_code' => $result['status_code'],
            'response_body' => $result['response_body'],
            'response_headers' => $result['response_headers'],
        ],
    ]);
}

$path = get_request_path();

if ($path === '/health') {
    handle_health();
    exit;
}

if ($path === '/partner/webhook') {
    handle_partner_webhook();
    exit;
}

if ($path === '/partner/trigger') {
    handle_partner_trigger();
    exit;
}

json_response(404, ['error' => 'not_found', 'message' => 'Route not found', 'path' => $path]);
