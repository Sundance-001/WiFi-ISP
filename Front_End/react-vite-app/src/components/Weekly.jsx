import React from 'react'

const speedTiers = [
  { id: '5mbps', speed: '5 Mbps', price: '$7' },
  { id: '20mbps', speed: '20 Mbps', price: '$12' },
  { id: '100mbps', speed: '100 Mbps', price: '$20' }
]

export default function Weekly() {
  return (
    <div className="weekly-plans">
      <h3>Weekly Plans</h3>
      <div className="plan-row">
        {speedTiers.map((t) => (
          <div key={t.id} className="plan-card">
            <div className="plan-title">{t.speed}</div>
            <div className="plan-price">{t.price}</div>
            <ul className="plan-features">
              <li>Valid for 7 days</li>
              <li>Fair use policy applies</li>
              <li>Standard support</li>
            </ul>
            <button className="select" data-plan={"weekly-" + t.id}>
              Select
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
