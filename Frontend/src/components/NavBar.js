import { Link } from "react-router-dom";
import { Bell, MessageSquare } from "lucide-react"; // icons
import { useState } from "react";

export default function Navbar() {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  return (
    <nav className="bg-[#0388B4] text-white px-6 py-2 flex justify-between items-center shadow-md">
      {/* Left: Logo */}
      <div className="flex items-center space-x-3">
        <img src="/assets/bk_logo.png" alt="Logo" className="h-10 w-10" />
        <span className="font-bold text-lg">HCMUT Portal</span>
      </div>

      {/* Center: Links */}
      <div className="flex space-x-6">
        <Link to="/home" className="hover:text-gray-300">
          Home
        </Link>
        <Link to="/classes" className="hover:text-gray-300">
          Classes
        </Link>
        <Link to="/schedule" className="hover:text-gray-300">
          Schedule
        </Link>
        <Link to="/support" className="hover:text-gray-300">
          Support
        </Link>
      </div>

      {/* Right: Notifications, Messages, Avatar */}
      <div className="flex items-center space-x-5">
        {/* Notification Icon */}
        <button className="relative hover:text-gray-300">
          <Bell className="h-5 w-5" />
          {/* Red dot for new notifications */}
          <span className="absolute top-0 right-0 inline-block h-2 w-2 bg-red-500 rounded-full"></span>
        </button>

        {/* Message Icon */}
        <button className="relative hover:text-gray-300">
          <MessageSquare className="h-5 w-5" />
          <span className="absolute top-0 right-0 inline-block h-2 w-2 bg-red-500 rounded-full"></span>
        </button>
        {/* Avatar  */}
        <div className="relative">
          <img
            src="/assets/truongan.jpg"
            alt="User Avatar"
            className="h-9 w-9 rounded-full cursor-pointer"
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
          />
          {/* Drop Down Menu When Avatar is Clicked  */}
          {isDropdownOpen && (
            <div className="absolute right-0 mt-2 w-40 bg-white text-black rounded-md shadow-lg py-2 z-50">
              <Link to="/profile" className="block px-4 py-2 hover:bg-gray-100">
                Profile
              </Link>
              <Link to="/grades" className="block px-4 py-2 hover:bg-gray-100">
                Grades
              </Link>
              <Link
                to="/settings"
                className="block px-4 py-2 hover:bg-gray-100"
              >
                Settings
              </Link>
              <button
                onClick={() => console.log("Exit clicked")}
                className="w-full text-left px-4 py-2 hover:bg-gray-100"
              >
                Exit
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
