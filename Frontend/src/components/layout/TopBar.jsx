import React from "react";
import { FaSearch, FaBell } from "react-icons/fa";

/**
 * TopBar Component
 * Reusable top bar with search and notifications
 */
const TopBar = ({
  leftContent = null,
  searchPlaceholder = "What do you want to play today?",
  onSearchChange,
  searchValue = "",
  onProfileClick,
}) => {
  return (
    <div className="flex items-center justify-between p-6 border-b border-[#3E3B2C]">
      {/* Left side - empty space */}
      <div className="w-0"></div>

      {/* Center - Search bar with home icon nearby */}
      <div className="flex-1 max-w-2xl flex items-center gap-8">
        {leftContent && (
          <div className="flex-shrink-0">{leftContent}</div>
        )}
        <div className="flex-1 relative">
          <FaSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder={searchPlaceholder}
            value={searchValue}
            onChange={(e) => onSearchChange?.(e.target.value)}
            className="w-full bg-[#2A2820] text-white rounded-full px-10 py-3 focus:outline-none focus:ring-2 focus:ring-[#F6A661]"
          />
        </div>
      </div>

      {/* Right side - Notifications */}
      <div className="flex items-center gap-4">
        <FaBell className="w-6 h-6 text-[#F6A661] cursor-pointer" />
        <div
          className="w-10 h-10 rounded-full bg-blue-500 cursor-pointer hover:ring-2 hover:ring-[#F6A661] transition-all"
          onClick={onProfileClick}
        ></div>
      </div>
    </div>
  );
};

export default TopBar;

