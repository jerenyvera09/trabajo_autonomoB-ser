import React, { useState } from 'react'

interface Props {
  onImageBase64: (b64: string | null) => void
}

const ImageUploader: React.FC<Props> = ({ onImageBase64 }) => {
  const [name, setName] = useState<string>('')
  const [error, setError] = useState<string | null>(null)

  const handleFile = (file: File | null) => {
    setError(null)
    if (!file) {
      setName('')
      onImageBase64(null)
      return
    }

    if (!file.type.startsWith('image/')) {
      setError('Solo se permiten archivos de imagen (png/jpg/webp, etc).')
      setName('')
      onImageBase64(null)
      return
    }

    // Para demo: evitar imágenes gigantes
    if (file.size > 2 * 1024 * 1024) {
      setError('Imagen demasiado grande (máx 2MB para demo).')
      setName('')
      onImageBase64(null)
      return
    }

    setName(file.name)

    const reader = new FileReader()
    reader.onload = () => {
      const result = String(reader.result || '')
      onImageBase64(result)
    }
    reader.onerror = () => {
      setError('No se pudo leer la imagen.')
      setName('')
      onImageBase64(null)
    }
    reader.readAsDataURL(file)
  }

  return (
    <div style={{ border: '1px solid #ddd', padding: 12, borderRadius: 8, maxWidth: 500, margin: '1em auto' }}>
      <b>Imagen (multimodal)</b>
      <div style={{ marginTop: 8 }}>
        <input type="file" accept="image/*" onChange={e => handleFile(e.target.files?.[0] || null)} />
      </div>
      {name && <div style={{ marginTop: 6, fontSize: 12 }}>Seleccionada: {name}</div>}
      {error && <div style={{ marginTop: 6, fontSize: 12, color: 'crimson' }}>{error}</div>}
      <div style={{ marginTop: 6, fontSize: 12, color: '#555' }}>
        La imagen se envía como base64 al AI Orchestrator para análisis local.
      </div>
    </div>
  )
}

export default ImageUploader
