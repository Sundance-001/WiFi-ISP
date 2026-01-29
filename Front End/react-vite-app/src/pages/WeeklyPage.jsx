import React from 'react'
import Weekly from '../components/Weekly'
import PaymentForm from '../components/PaymentForm'
import ContactDetails from '../components/ContactDetails'

export default function WeeklyPage() {
  return (
    <main className="page-content">
      <section className="page-header">
        <h1>Weekly Plans</h1>
        <p>7 days of fast & reliable WiFi — choose your speed</p>
      </section>
      <Weekly />
      <PaymentForm />
      <ContactDetails />
    </main>
  )
}
