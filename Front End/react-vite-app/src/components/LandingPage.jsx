import React from 'react'
import Packages from './Packages'
import PaymentForm from './PaymentForm'
import ContactDetails from './ContactDetails'

export default function LandingPage() {
  return (
    <div className="landing">
      <header className="hero">
        <h1>Fast & Reliable WiFi</h1>
        <p>Affordable plans for every need — hourly, weekly, and monthly.</p>
      </header>

      <main className="content">
        <Packages />
        <PaymentForm />
        <ContactDetails />
      </main>
    </div>
  )
}
