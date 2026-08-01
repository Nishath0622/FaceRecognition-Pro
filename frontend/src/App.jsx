import { Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import RecognizePage from './pages/RecognizePage'
import DatasetPage from './pages/DatasetPage'
import LivePage from './pages/LivePage'

export default function App() {
  return (
    <div className="min-h-screen bg-gray-950">
      <Toaster
        position="top-right"
        toastOptions={{
          style: { background: '#1f2937', color: '#f3f4f6', border: '1px solid #374151' }
        }}
      />
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Routes>
          <Route path="/"           element={<Dashboard />} />
          <Route path="/recognize"  element={<RecognizePage />} />
          <Route path="/dataset"    element={<DatasetPage />} />
          <Route path="/live"       element={<LivePage />} />
        </Routes>
      </main>
    </div>
  )
}
