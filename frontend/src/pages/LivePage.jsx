import { useState, useEffect } from 'react'
import { setStreamMode, STREAM_URL } from '../api/client'
import { Video, Eye, ScanFace, VideoOff } from 'lucide-react'
import toast from 'react-hot-toast'

const MODES = [
  { id: 'none',      label: 'Off',       icon: VideoOff,  color: 'gray' },
  { id: 'detect',    label: 'Detect',    icon: Eye,       color: 'blue' },
  { id: 'recognize', label: 'Recognize', icon: ScanFace,  color: 'brand' },
]

export default function LivePage() {
  const [mode, setMode]         = useState('detect')
  const [streamOn, setStreamOn] = useState(false)
  const [streamKey, setStreamKey] = useState(0)

  const applyStreamMode = async (m) => {
    try {
      await setStreamMode(m)
      setMode(m)
      setStreamOn(m !== 'none')
      return true
    } catch {
      toast.error('Could not set mode — is the backend running?')
      return false
    }
  }

  const toggleStream = async () => {
    if (streamOn) {
      await applyStreamMode('none')
      return
    }

    const nextMode = mode === 'none' ? 'detect' : mode
    const started = await applyStreamMode(nextMode)
    if (started) {
      setStreamKey((prev) => prev + 1)
    }
  }

  const handleModeChange = async (m) => {
    setMode(m)
    if (streamOn) {
      await applyStreamMode(m)
    }
  }

  const stopStream = async () => {
    await applyStreamMode('none')
  }

  useEffect(() => () => { stopStream() }, [])

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Video className="w-6 h-6 text-brand-400" /> Live Camera Feed
        </h1>
        <p className="text-gray-400 mt-1">Real-time face detection and recognition from your webcam</p>
      </div>

      {/* Stream controls */}
      <div className="flex flex-wrap items-center gap-3">
        <button
          onClick={toggleStream}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all
            ${streamOn ? 'bg-red-600 text-white shadow-lg' : 'bg-green-600 text-white hover:bg-green-500'}`}
        >
          {streamOn ? 'Turn OFF' : 'Turn ON'}
        </button>

        <div className="flex flex-wrap gap-2">
          {MODES.filter((item) => item.id !== 'none').map(({ id, label }) => (
            <button
              key={id}
              onClick={() => handleModeChange(id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all
                ${mode === id
                  ? 'bg-brand-500 text-white shadow-lg'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
            >
              {label}
            </button>
          ))}
        </div>

        <div className="rounded-xl px-3 py-2 bg-gray-800 text-xs text-gray-400">
          Status: {streamOn ? `LIVE · ${mode.toUpperCase()}` : 'OFF'}
        </div>
      </div>

      {/* Stream */}
      <div className="card p-2 bg-black rounded-2xl border-gray-800">
        {streamOn ? (
          <div className="relative">
            <img
              key={streamKey}
              src={`${STREAM_URL}?t=${streamKey}`}
              alt="live stream"
              className="w-full rounded-xl"
              style={{ maxHeight: '520px', objectFit: 'contain' }}
            />
            <div className="absolute top-3 left-3 flex items-center gap-1.5 bg-black/60 rounded-lg px-2.5 py-1">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
              <span className="text-xs text-white font-medium">LIVE · {mode.toUpperCase()}</span>
            </div>
          </div>
        ) : (
          <div className="aspect-video flex flex-col items-center justify-center gap-4 text-gray-600 rounded-xl bg-gray-900">
            <VideoOff className="w-14 h-14" />
            <p className="text-sm">Select <strong>Detect</strong> or <strong>Recognize</strong> to start the stream</p>
          </div>
        )}
      </div>

      {/* Info */}
      <div className="grid sm:grid-cols-3 gap-4 text-sm">
        {[
          { title: 'Off mode',       desc: 'Camera stream is paused' },
          { title: 'Detect mode',    desc: 'Draws boxes around all detected faces' },
          { title: 'Recognize mode', desc: 'Identifies known persons from the trained model' },
        ].map(({ title, desc }) => (
          <div key={title} className="card py-4">
            <p className="font-semibold text-white">{title}</p>
            <p className="text-gray-500 mt-0.5">{desc}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
