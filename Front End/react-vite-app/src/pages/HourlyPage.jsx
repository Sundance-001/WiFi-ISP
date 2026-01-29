import React from 'react'
import Hourly from '../components/Hourly'
import PaymentForm from '../components/PaymentForm'
import ContactDetails from '../components/ContactDetails'

export default function HourlyPage() {
  return (
    <main className="page-content">
      <section className="page-header">
        <h1>Hourly Plans</h1>
        <p>Pay by the hour — perfect for short-term access</p>
      </section>
      <Hourly />
      <PaymentForm />
      <ContactDetails />
    </main>
  )
}
