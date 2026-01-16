import React, { useState } from 'react';

interface PdfUploaderProps {
  onExtractedText: (text: string) => void;
}

const API_REST = import.meta.env.VITE_API_REST || 'http://localhost:8000';

const PdfUploader: React.FC<PdfUploaderProps> = ({ onExtractedText }) => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch(`${API_REST}/api/v1/pdf/extract`, {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) throw new Error('Error al extraer texto del PDF');
      const data = await res.json();
      onExtractedText(data.text || '');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ margin: '1em 0' }}>
      <input type="file" accept="application/pdf" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={!file || loading}>
        {loading ? 'Procesando...' : 'Extraer texto PDF'}
      </button>
      {error && <div style={{ color: 'red' }}>{error}</div>}
    </div>
  );
};

export default PdfUploader;
