import React from 'react'
import { HEADER_NAV_ITEMS } from '@utils/data'
import { Link } from 'react-router-dom'

/**
 * Header Component
 * 
 * This component displays the top navigation bar with:
 * - Logo (two circular headphones icons + "HEADPHONES ON" text)
 * - Navigation menu items (Home, About Us, Community, Support)
 * - Sign Up and Sign In buttons
 * 
 * Background color: #3F3C35 (dark brown/olive)
 */
const Header = () => {
  /**
   * Handles smooth scrolling when clicking on anchor links (#section)
   * Prevents default anchor behavior and smoothly scrolls to the target section
   */
  const handleNavClick = (e, path) => {
    if (path.startsWith('#')) {
      e.preventDefault()
      const element = document.querySelector(path)
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' })
      }
    }
  }

  return (
    <div className="flex items-center justify-between px-8 py-4 bg-[#3E3B2C]">
      {/* Logo Section - Logo image + brand name */}
      <div className="flex items-center gap-2">
        {/* Logo image from public folder */}
        <img src="/Logo.png" alt="Logo" className="w-15 h-15" />
        {/* Brand name - using Karantina font for title consistency, color: #F6A661 */}
        <h1 className="text-[#F6A661] text-[40px] font-karantina">HEADPHONES ON</h1>  
      </div>

      {/* Navigation Menu - Center section with menu items */}
      <div className="flex items-center gap-8">
        {HEADER_NAV_ITEMS.map((item) => (
          <a
            key={item.id}
            href={item.path}
            onClick={(e) => handleNavClick(e, item.path)}
            className="text-[#F6A661] font-bold text-[20px] hover:text-[#FFFBEF] transition-colors cursor-pointer"
          >
            {item.label}
          </a>
        ))}
      </div>

      {/* Action Buttons - Sign Up (white) and Sign In (custom orange #F6A661) */}
      <div className="flex items-center gap-4">
        {/* Sign Up button - white background with dark text */}
        <Link
          to="/signup"
          className="bg-white text-[#3F3C35] px-8 py-1.5 text-xl rounded-full font-bold hover:bg-gray-200 transition-colors"
        >
          Sign Up
        </Link>
        {/* Sign In button - custom orange (#F6A661) background with white text */}
        <Link
          to="/login"
          className="bg-[#F6A661] text-white px-8 py-1.5 text-xl rounded-full font-bold hover:bg-[#E5954F] transition-colors"
        >
          Sign In
        </Link>
      </div>
    </div>
  )
}

export default Header
