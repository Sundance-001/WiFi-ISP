import React from 'react'
import Hourly from './Hourly'
import Weekly from './Weekly'
import Monthly from './Monthly'

export default function Packages() {
  return (
    <section className="packages">
      <h2>Packages</h2>
      <Hourly />
      <Weekly />
      <Monthly />
    </section>
  )
}
