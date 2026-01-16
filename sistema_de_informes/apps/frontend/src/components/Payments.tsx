import React, { useEffect, useState } from 'react';

interface Payment {
  id: string;
  amount: number;
  status: string;
  currency?: string;
}

const API_PAYMENT = import.meta.env.VITE_API_PAYMENT || 'http://localhost:8002';

const Payments: React.FC = () => {
  const [payments, setPayments] = useState<Payment[]>([]);
  const [amount, setAmount] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchPayments = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_PAYMENT}/payments`);
      if (!res.ok) throw new Error('Error al obtener pagos');
      const data = await res.json();
      setPayments(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!amount) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_PAYMENT}/payments/checkout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount: parseFloat(amount), currency: 'USD', metadata: { source: 'frontend-week4' } }),
      });
      if (!res.ok) throw new Error('Error al crear pago');
      setAmount('');
      await fetchPayments();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPayments();
  }, []);

  return (
    <div style={{ border: '1px solid #ccc', padding: 16, borderRadius: 8, maxWidth: 500, margin: '1em auto' }}>
      <h3>Pagos</h3>
      <div>
        <input
          type="number"
          value={amount}
          onChange={e => setAmount(e.target.value)}
          placeholder="Monto"
          style={{ width: 120, marginRight: 8 }}
        />
        <button onClick={handleCreate} disabled={loading || !amount}>
          Crear Pago
        </button>
      </div>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <ul>
        {payments.map(p => (
          <li key={p.id}>
            <b>ID:</b> {p.id} | <b>Monto:</b> {p.amount} {p.currency || 'USD'} | <b>Estado:</b> {p.status}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Payments;
