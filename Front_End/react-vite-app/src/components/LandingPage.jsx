import React from 'react'
import { Link } from 'react-router-dom'
import ContactDetails from './ContactDetails'

export default function LandingPage() {
  return (
    <div className="landing">
      <header className="hero">
        <h1>Fast & Reliable WiFi</h1>
        <p>Affordable plans for every need — hourly, weekly, and monthly.</p>
      </header>

      <main className="content">
        <section className="plan-overview">
          <h2>Choose Your Plan</h2>
          <div className="plan-cards-grid">
            <Link to="/hourly" className="plan-overview-card hourly-card">
              <h3>Hourly</h3>
              <p>1 hour to 24 hours</p>
              <p className="price">From $0.50</p>
              <button>View Plans →</button>
            </Link>
            <Link to="/weekly" className="plan-overview-card weekly-card">
              <h3>Weekly</h3>
              <p>7 days access</p>
              <p className="price">From $7</p>
              <button>View Plans →</button>
            </Link>
            <Link to="/monthly" className="plan-overview-card monthly-card">
              <h3>Monthly</h3>
              <p>30 days access</p>
              <p className="price">From $25</p>
              <button>View Plans →</button>
            </Link>
          </div>
        </section>

        <ContactDetails />
      </main>
    </div>
  )
}
