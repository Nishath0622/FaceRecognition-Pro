import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

// ── Face ──────────────────────────────────────────────────────
export const detectFaces   = (formData) => api.post('/face/detect', formData)
export const recognizeFaces = (formData) => api.post('/face/recognize', formData)
export const trainModel    = ()          => api.post('/face/train')
export const getModelInfo  = ()          => api.get('/face/model-info')

// ── Dataset ───────────────────────────────────────────────────
export const uploadImages  = (formData) => api.post('/dataset/upload', formData)
export const getPersons    = ()         => api.get('/dataset/persons')
export const getDatasetStats = ()       => api.get('/dataset/stats')
export const deletePerson  = (name)     => api.delete(`/dataset/delete/${name}`)

// ── Stream ────────────────────────────────────────────────────
export const setStreamMode = (mode) => api.post(`/stream/mode/${mode}`)
export const getStreamStatus = ()   => api.get('/stream/status')
export const STREAM_URL = '/api/stream/video_feed'

export default api
