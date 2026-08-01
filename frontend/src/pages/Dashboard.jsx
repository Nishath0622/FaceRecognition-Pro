import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getModelInfo, getDatasetStats, trainModel } from '../api/client'
import { ScanFace, Database, Cpu, Users, ChevronRight, Zap, AlertTriangle } from 'lucide-react'
import toast from 'react-hot-toast'

export default function Dashboard() {
  const [modelInfo, setModelInfo] = useState(null)
  const [stats, setStats]         = useState(null)
  const [training, setTraining]   = useState(false)

  const load = async () => {
    try {
      const [mi, ds] = await Promise.all([getModelInfo(), getDatasetStats()])
      setModelInfo(mi.data)
      setStats(ds.data)
    } catch { /* backend not running yet */ }
  }

  useEffect(() => { load() }, [])

  const handleTrain = async () => {
    setTraining(true)
    try {
      const res = await trainModel()
      toast.success(`Trained ${res.data.persons_trained} person(s) — ${res.data.total_samples} samples`)
      load()
    } catch (e) {
      toast.error(e.response?.data?.message || 'Training failed')
    } finally {
      setTraining(false)
    }
  }

  const statCards = [
    {
      label: 'Model Status',
      value: modelInfo?.trained ? 'Trained ✓' : 'Not Trained',
      icon: Cpu,
      color: modelInfo?.trained ? 'text-green-400' : 'text-yellow-400',
      bg: modelInfo?.trained ? 'bg-green-500/10' : 'bg-yellow-500/10',
    },
    {
      label: 'Persons in DB',
      value: modelInfo?.person_count ?? '—',
      icon: Users,
      color: 'text-blue-400',
      bg: 'bg-blue-500/10',
    },
    {
      label: 'Dataset Images',
      value: stats?.total_images ?? '—',
      icon: Database,
      color: 'text-purple-400',
      bg: 'bg-purple-500/10',
    },
    {
      label: 'Algorithm',
      value: 'DeepFace',
      icon: Zap,
      color: 'text-brand-400',
      bg: 'bg-brand-500/10',
    },
  ]

  return (
    <div className="space-y-8">
      {/* Hero */}
      <div className="card bg-gradient-to-br from-gray-900 via-gray-900 to-brand-900/20 border-brand-800/40">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-white mb-1">
              Face Recognition <span className="text-brand-400">Pro</span>
            </h1>
            <p className="text-gray-400">
              DeepFace-powered face recognition · Real-time · Scalable
            </p>
          </div>
          <button
            onClick={handleTrain}
            disabled={training}
            className="btn-primary flex items-center gap-2 self-start sm:self-auto"
          >
            <Cpu className="w-4 h-4" />
            {training ? 'Training…' : 'Train Model'}
          </button>
        </div>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((c) => (
          <div key={c.label} className="card flex items-center gap-4">
            <div className={`w-11 h-11 rounded-xl flex items-center justify-center ${c.bg}`}>
              <c.icon className={`w-5 h-5 ${c.color}`} />
            </div>
            <div>
              <p className="text-xs text-gray-500 font-medium uppercase tracking-wide">{c.label}</p>
              <p className={`text-xl font-bold ${c.color}`}>{c.value}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Quick actions */}
      <div className="grid sm:grid-cols-3 gap-4">
        {[
          { to: '/recognize', icon: ScanFace,  title: 'Recognize Face',   desc: 'Upload a photo to identify a person', color: 'brand' },
          { to: '/live',      icon: Zap,        title: 'Live Camera',      desc: 'Real-time recognition from webcam',   color: 'blue' },
          { to: '/dataset',   icon: Database,   title: 'Manage Dataset',   desc: 'Add or remove persons from the DB',  color: 'purple' },
        ].map(({ to, icon: Icon, title, desc, color }) => (
          <Link key={to} to={to} className="card hover:border-gray-600 transition-colors group flex flex-col gap-3">
            <div className={`w-10 h-10 rounded-xl bg-${color}-500/10 flex items-center justify-center`}>
              <Icon className={`w-5 h-5 text-${color}-400`} />
            </div>
            <div>
              <h3 className="font-semibold text-white group-hover:text-brand-400 transition-colors">{title}</h3>
              <p className="text-sm text-gray-500">{desc}</p>
            </div>
            <ChevronRight className="w-4 h-4 text-gray-600 group-hover:text-brand-400 transition-colors mt-auto" />
          </Link>
        ))}
      </div>

      {/* Persons list */}
      {modelInfo?.persons?.length > 0 && (
        <div className="card">
          <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Users className="w-5 h-5 text-brand-400" /> Known Persons
          </h2>
          <div className="flex flex-wrap gap-2">
            {modelInfo.persons.map((p) => (
              <span key={p} className="badge-green">{p}</span>
            ))}
          </div>
        </div>
      )}

      {/* Warning if not trained */}
      {modelInfo && !modelInfo.trained && (
        <div className="card border-yellow-700/40 bg-yellow-900/10 flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-yellow-400 mt-0.5 shrink-0" />
          <div>
            <p className="font-semibold text-yellow-300">Model not trained</p>
            <p className="text-sm text-yellow-500 mt-0.5">
              Go to <Link to="/dataset" className="underline">Dataset</Link> to add images, then click <strong>Train Model</strong> above.
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
