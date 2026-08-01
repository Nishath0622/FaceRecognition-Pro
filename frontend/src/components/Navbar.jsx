import { Link, useLocation } from 'react-router-dom'
import { ScanFace, LayoutDashboard, Database, Video } from 'lucide-react'

const links = [
  { to: '/',          label: 'Dashboard', icon: LayoutDashboard },
  { to: '/recognize', label: 'Recognize',  icon: ScanFace },
  { to: '/live',      label: 'Live Feed',  icon: Video },
  { to: '/dataset',   label: 'Dataset',    icon: Database },
]

export default function Navbar() {
  const { pathname } = useLocation()

  return (
    <nav className="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 bg-brand-500 rounded-xl flex items-center justify-center shadow-lg shadow-brand-500/30">
              <ScanFace className="w-5 h-5 text-white" />
            </div>
            <span className="text-lg font-bold text-white tracking-tight">
              FaceRecog <span className="text-brand-400">Pro</span>
            </span>
          </Link>

          {/* Nav links */}
          <div className="flex items-center gap-1">
            {links.map(({ to, label, icon: Icon }) => {
              const active = pathname === to
              return (
                <Link
                  key={to}
                  to={to}
                  className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200
                    ${active
                      ? 'bg-brand-500/20 text-brand-400 border border-brand-500/30'
                      : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800'
                    }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="hidden sm:inline">{label}</span>
                </Link>
              )
            })}
          </div>
        </div>
      </div>
    </nav>
  )
}
