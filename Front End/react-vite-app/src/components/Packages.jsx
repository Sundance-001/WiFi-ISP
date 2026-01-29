import React from 'react'

const plans = [
  { id: 'hourly', title: 'Hourly', price: '$1', desc: '1 hour access', features: ['1GB data', 'No auto-renew'] },
  { id: 'weekly', title: 'Weekly', price: '$7', desc: '7 days access', features: ['10GB data', 'Standard support'] },
  { id: 'monthly', title: 'Monthly', price: '$25', desc: '30 days access', features: ['50GB data', 'Priority support'] }
]

export default function Packages() {
  return (
    <section className="packages">
      <h2>Packages</h2>
      <div className="package-list">
        {plans.map((p) => (
          <div key={p.id} className="package-card">
            <h3>{p.title}</h3>
            <div className="price">{p.price}</div>
            <p className="desc">{p.desc}</p>
            <ul>
              {p.features.map((f, i) => (
                <li key={i}>{f}</li>
              ))}
            </ul>
            <button className="select" data-plan={p.id}>
              Select
            </button>
          </div>
        ))}
      </div>
    </section>
  )
}
