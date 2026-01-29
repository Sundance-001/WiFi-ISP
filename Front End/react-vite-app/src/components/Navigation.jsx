import React from 'react'
import { Link, useLocation } from 'react-router-dom'

export default function Navigation() {
  const location = useLocation()

  return (
    <nav className="navbar">
      <div className="nav-container">
        <div className="nav-logo">
          <Link to="/">WiFi ISP</Link>
        </div>
        <div className="nav-tabs">
          <Link
            to="/"
            className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
          >
            Home
          </Link>
          <Link
            to="/hourly"
            className={`nav-link ${location.pathname === '/hourly' ? 'active' : ''}`}
          >
            Hourly
          </Link>
          <Link
            to="/weekly"
            className={`nav-link ${location.pathname === '/weekly' ? 'active' : ''}`}
          >
            Weekly
          </Link>
          <Link
            to="/monthly"
            className={`nav-link ${location.pathname === '/monthly' ? 'active' : ''}`}
          >
            Monthly
          </Link>
        </div>
      </div>
    </nav>
  )
}
