import React from 'react'
import Monthly from '../components/Monthly'
import PaymentForm from '../components/PaymentForm'
import ContactDetails from '../components/ContactDetails'

export default function MonthlyPage() {
  return (
    <main className="page-content">
      <section className="page-header">
        <h1>Monthly Plans</h1>
        <p>30 days of premium WiFi — best value with priority support</p>
      </section>
      <Monthly />
      <PaymentForm />
      <ContactDetails />
    </main>
  )
}
