import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navigation from './components/Navigation'
import HourlyPage from './pages/HourlyPage'
import WeeklyPage from './pages/WeeklyPage'
import MonthlyPage from './pages/MonthlyPage'
import LandingPage from './components/LandingPage'
import './index.css'

export default function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/hourly" element={<HourlyPage />} />
        <Route path="/weekly" element={<WeeklyPage />} />
        <Route path="/monthly" element={<MonthlyPage />} />
      </Routes>
    </BrowserRouter>
  )
}
