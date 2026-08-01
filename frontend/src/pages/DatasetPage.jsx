import { useState, useEffect, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { uploadImages, getPersons, deletePerson, trainModel } from '../api/client'
import { Database, Upload, Cpu, Loader2, Plus } from 'lucide-react'
import toast from 'react-hot-toast'

export default function DatasetPage() {
  const [persons, setPersons] = useState([])
  const [name, setName] = useState('')
  const [files, setFiles] = useState([])
  const [uploading, setUploading] = useState(false)
  const [training, setTraining] = useState(false)
  const [loading, setLoading] = useState(true)

  // ---------------- LOAD PERSONS ----------------
  const loadPersons = async () => {
    try {
      const res = await getPersons()
      setPersons(res.data.persons || [])
    } catch {
      toast.error('Could not load persons')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadPersons()
  }, [])

  // ---------------- FILE DROP ----------------
  const onDrop = useCallback((accepted) => setFiles(accepted), [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.jpg', '.jpeg', '.png'] },
    multiple: true,
  })

  // ---------------- UPLOAD ----------------
  const handleUpload = async () => {
    if (!name.trim()) return toast.error('Enter a person name')
    if (!files.length) return toast.error('Select at least one image')

    setUploading(true)

    try {
      const fd = new FormData()
      fd.append('name', name.trim())
      files.forEach((f) => fd.append('images', f))

      const res = await uploadImages(fd)

      toast.success(`Saved ${res.data.images_saved} image(s) for ${res.data.person}`)

      setName('')
      setFiles([])
      loadPersons()

    } catch (e) {
      toast.error(e.response?.data?.error || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  // ---------------- DELETE ----------------
  const handleDelete = async (pname) => {
    if (!confirm(`Delete all images for "${pname}"?`)) return

    try {
      await deletePerson(pname)
      toast.success(`Deleted ${pname}`)
      loadPersons()
    } catch {
      toast.error('Delete failed')
    }
  }

  // ---------------- TRAIN (FINAL FIX) ----------------
  const handleTrain = async () => {
    setTraining(true)

    try {
      const res = await trainModel()
      const data = res.data || {}

      const persons = data.persons ?? 0
      const samples = data.samples ?? 0

      toast.success(`Trained ${persons} person(s) — ${samples} samples`)

    } catch (e) {
      toast.error(e.response?.data?.message || 'Training failed')
    } finally {
      setTraining(false)
    }
  }

  // ---------------- UI ----------------
  return (
    <div className="space-y-6 max-w-5xl mx-auto">

      <div className="flex items-start justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Database className="w-6 h-6 text-brand-400" /> Dataset Manager
          </h1>
          <p className="text-gray-400 mt-1">
            Add persons and images, then train the model
          </p>
        </div>

        <button
          onClick={handleTrain}
          disabled={training}
          className="btn-primary flex items-center gap-2"
        >
          {training ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <Cpu className="w-4 h-4" />
          )}
          {training ? 'Training…' : 'Train Model'}
        </button>
      </div>

      <div className="grid md:grid-cols-2 gap-6">

        {/* Upload */}
        <div className="card space-y-4">
          <h2 className="font-semibold text-white flex items-center gap-2">
            <Plus className="w-4 h-4 text-brand-400" /> Add New Person
          </h2>

          <input
            className="input"
            placeholder="Person name (e.g. Nisha)"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer
            ${isDragActive ? 'border-brand-500 bg-brand-500/5' : 'border-gray-700'}`}
          >
            <input {...getInputProps()} />

            <Upload className="w-8 h-8 text-gray-600 mx-auto mb-2" />

            {files.length ? (
              <p className="text-brand-400">{files.length} file(s) selected</p>
            ) : (
              <p className="text-gray-500 text-sm">
                Drop images or <span className="text-brand-400">browse</span>
              </p>
            )}
          </div>

          <button onClick={handleUpload} className="btn-primary w-full">
            {uploading ? 'Uploading…' : 'Upload Images'}
          </button>
        </div>

        {/* Persons */}
        <div className="card space-y-4">
          <h2 className="text-white font-semibold">
            Known Persons ({persons.length})
          </h2>

          {persons.map((p) => (
            <div key={p.name} className="flex justify-between items-center">
              <div>
                <span>{p.name}</span>
                <p className="text-xs text-gray-500">
                  {p.image_count || 0} image(s)
                </p>
              </div>

              <button
                onClick={() => handleDelete(p.name)}
                className="text-red-400 text-sm"
              >
                Delete
              </button>
            </div>
          ))}
        </div>

      </div>
    </div>
  )
}