import React from 'react'

export default function ContactDetails() {
  return (
    <section className="contacts">
      <h2>Contact & Details</h2>
      <p>
        Support: <a href="tel:+15555555555">+1 555 555 5555</a>
      </p>
      <p>
        Email: <a href="mailto:support@example.com">support@example.com</a>
      </p>
      <p>Office: 123 Network Ave, City</p>
      <div className="social">
        <a href="#">Facebook</a> · <a href="#">Twitter</a>
      </div>
    </section>
  )
}
