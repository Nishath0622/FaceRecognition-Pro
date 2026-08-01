import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { recognizeFaces, detectFaces } from '../api/client'
import { Upload, ScanFace, CheckCircle, XCircle, Loader2, ImageIcon } from 'lucide-react'
import toast from 'react-hot-toast'

export default function RecognizePage() {
  const [file, setFile]       = useState(null)
  const [preview, setPreview] = useState(null)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [mode, setMode]       = useState('recognize') // recognize | detect

  const onDrop = useCallback((accepted) => {
    if (!accepted.length) return
    const f = accepted[0]
    setFile(f)
    setPreview(URL.createObjectURL(f))
    setResults(null)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.jpg', '.jpeg', '.png'] },
    multiple: false,
  })

  const handleSubmit = async () => {
    if (!file) return toast.error('Please select an image')
    setLoading(true)
    try {
      const fd = new FormData()
      fd.append('image', file)
      const fn = mode === 'recognize' ? recognizeFaces : detectFaces
      const res = await fn(fd)
      setResults(res.data)
    } catch (e) {
      toast.error(e.response?.data?.error || 'Request failed')
    } finally {
      setLoading(false)
    }
  }

  const reset = () => { setFile(null); setPreview(null); setResults(null) }

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <ScanFace className="w-6 h-6 text-brand-400" /> Face Recognition
        </h1>
        <p className="text-gray-400 mt-1">Upload an image to detect or recognise faces</p>
      </div>

      {/* Mode toggle */}
      <div className="flex gap-2">
        {['recognize', 'detect'].map((m) => (
          <button
            key={m}
            onClick={() => { setMode(m); setResults(null) }}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-all capitalize
              ${mode === m ? 'bg-brand-500 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
          >
            {m}
          </button>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Upload area */}
        <div className="space-y-4">
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all
              ${isDragActive ? 'border-brand-500 bg-brand-500/5' : 'border-gray-700 hover:border-gray-500 bg-gray-900'}`}
          >
            <input {...getInputProps()} />
            {preview ? (
              <img src={preview} alt="preview" className="max-h-64 mx-auto rounded-xl object-contain" />
            ) : (
              <div className="space-y-3">
                <Upload className="w-10 h-10 text-gray-600 mx-auto" />
                <p className="text-gray-400">Drop image here or <span className="text-brand-400">browse</span></p>
                <p className="text-xs text-gray-600">JPG, JPEG, PNG</p>
              </div>
            )}
          </div>

          <div className="flex gap-3">
            <button onClick={handleSubmit} disabled={!file || loading} className="btn-primary flex-1 flex items-center justify-center gap-2">
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <ScanFace className="w-4 h-4" />}
              {loading ? 'Processing…' : mode === 'recognize' ? 'Recognize' : 'Detect'}
            </button>
            {file && <button onClick={reset} className="btn-secondary">Reset</button>}
          </div>
        </div>

        {/* Results */}
        <div className="card min-h-[200px]">
          <h2 className="font-semibold text-white mb-4 flex items-center gap-2">
            <ImageIcon className="w-4 h-4 text-brand-400" /> Results
          </h2>

          {!results && !loading && (
            <p className="text-gray-500 text-sm">Results will appear here after processing</p>
          )}

          {loading && (
            <div className="flex items-center gap-3 text-brand-400">
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Analysing image…</span>
            </div>
          )}

          {results && !loading && (
            <div className="space-y-3">
              <p className="text-sm text-gray-400">
                Found <span className="text-white font-semibold">{results.face_count}</span> face(s)
              </p>

              {/* Recognition results */}
              {results.results?.map((r, i) => (
                <div key={i} className={`rounded-xl p-4 border ${r.matched ? 'bg-green-900/20 border-green-700/40' : 'bg-gray-800 border-gray-700'}`}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {r.matched
                        ? <CheckCircle className="w-5 h-5 text-green-400" />
                        : <XCircle className="w-5 h-5 text-red-400" />}
                      <span className="font-semibold text-white text-lg">{r.name}</span>
                    </div>
                    {r.matched && (
                      <span className="badge-green">{r.confidence}% confident</span>
                    )}
                  </div>
                  {!r.matched && (
                    <p className="text-sm text-gray-400 mt-1 ml-7">
                      Not recognised. Add this person to the dataset and retrain.
                    </p>
                  )}
                </div>
              ))}

              {/* Detection-only results */}
              {results.faces?.map((f, i) => (
                <div key={i} className="rounded-xl p-3 bg-gray-800 border border-gray-700 text-sm text-gray-300">
                  Face {i + 1} — position ({f.x}, {f.y}) size {f.w}×{f.h}px
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
