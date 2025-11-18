import AboutUs from '@components/Landing Page/AboutUs'
import Community from '@components/Landing Page/Community'
import Contact from '@components/Landing Page/Contact'
import Header from '@components/Landing Page/Header'
import Hero from '@components/Landing Page/Hero'
import React from 'react'

const LandingPage = () => {
  return (
    <div className='min-h-screen bg-[#3F3C35]'>
      <Header />
      <Hero />
      <div id="about">
        <AboutUs />
      </div>
      <div id="community">
        <Community />
      </div>
      <div id="support">
        <Contact />
      </div>
    </div>
  )
}

export default LandingPage