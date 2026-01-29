import React, { useState } from 'react'
import { apiService } from '../services/apiService'

export default function PaymentForm() {
  const [phone, setPhone] = useState('')
  const [selectedPlan, setSelectedPlan] = useState('1')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      // Step 1: Create a session
      const sessionData = await apiService.createSession(phone, parseInt(selectedPlan), 1)
      if (!sessionData || !sessionData.id) {
        setMessage('❌ Failed to create session')
        return
      }

      // Step 2: Create payment for the session
      const paymentData = await apiService.createPayment(sessionData.id, phone, 10)
      if (!paymentData || !paymentData.id) {
        setMessage('❌ Failed to create payment')
        return
      }

      setMessage(`✅ Payment initiated! Session: ${sessionData.session_token}`)
      setPhone('')
      setSelectedPlan('1')
    } catch (error) {
      setMessage('❌ Error: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="payment">
      <h2>Pay & Activate</h2>
      <form onSubmit={handleSubmit} className="payment-form">
        <label>
          Phone number
          <input
            type="tel"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder="+254 700 000 000"
            required
            disabled={loading}
          />
        </label>

        <label>
          Plan
          <select value={selectedPlan} onChange={(e) => setSelectedPlan(e.target.value)} disabled={loading}>
            <option value="1">Hourly</option>
            <option value="2">Weekly</option>
            <option value="3">Monthly</option>
          </select>
        </label>

        <button type="submit" className="pay-btn" disabled={loading}>
          {loading ? 'Processing...' : 'Pay'}
        </button>
      </form>
      {message && <p className={`note ${message.includes('✅') ? 'success' : 'error'}`}>{message}</p>}
    </section>
  )
}
