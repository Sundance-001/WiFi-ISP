import React, { useState } from 'react'

export default function PaymentForm() {
  const [phone, setPhone] = useState('')
  const [selected, setSelected] = useState('monthly')

  function handleSubmit(e) {
    e.preventDefault()
    // Placeholder: integrate real payment in production
    alert(`Paying for ${selected} plan with phone ${phone}`)
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
            placeholder="+1 555 555 5555"
            required
          />
        </label>

        <label>
          Plan
          <select value={selected} onChange={(e) => setSelected(e.target.value)}>
            <option value="hourly">Hourly</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        </label>

        <button type="submit" className="pay-btn">
          Pay
        </button>
      </form>
      <p className="note">Payment handled externally in production.</p>
    </section>
  )
}
