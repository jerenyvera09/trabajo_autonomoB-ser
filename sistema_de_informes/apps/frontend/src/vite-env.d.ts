/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_REST: string
  readonly VITE_API_GRAPHQL: string
  readonly VITE_WS_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
