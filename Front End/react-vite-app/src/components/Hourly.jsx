import React from 'react'

const hourlyPlans = [
  { id: 'h1', title: '1 hour', price: '$0.50' },
  { id: 'h3', title: '3 hours', price: '$1.25' },
  { id: 'h8', title: '8 hours', price: '$2.50' },
  { id: 'h16', title: '16 hours', price: '$4.00' },
  { id: 'h24', title: '24 hours', price: '$6.00' }
]

export default function Hourly() {
  return (
    <div className="hourly-plans">
      <h3>Hourly Plans</h3>
      <div className="plan-row">
        {hourlyPlans.map((p) => (
          <div key={p.id} className="plan-card small">
            <div className="plan-title">{p.title}</div>
            <div className="plan-price">{p.price}</div>
            <div className="plan-meta">Pay as you go — ideal for visitors</div>
            <button className="select" data-plan={p.id}>
              Select
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
