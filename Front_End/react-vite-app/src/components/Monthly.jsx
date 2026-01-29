import React from 'react'

const monthlyTiers = [
  { id: 'm-5', speed: '5 Mbps', price: '$25' },
  { id: 'm-20', speed: '20 Mbps', price: '$45' },
  { id: 'm-100', speed: '100 Mbps', price: '$90' }
]

export default function Monthly() {
  return (
    <div className="monthly-plans">
      <h3>Monthly Plans</h3>
      <div className="plan-row">
        {monthlyTiers.map((t) => (
          <div key={t.id} className="plan-card">
            <div className="plan-title">{t.speed}</div>
            <div className="plan-price">{t.price}</div>
            <ul className="plan-features">
              <li>Valid for 30 days</li>
              <li>Priority support</li>
              <li>Higher speed burst available</li>
            </ul>
            <button className="select" data-plan={"monthly-" + t.id}>
              Select
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
