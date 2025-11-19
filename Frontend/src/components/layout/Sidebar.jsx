import React from "react";
import { Link, useLocation } from "react-router-dom";

const DEFAULT_NAV_ITEMS = [
  { label: "Home", path: "/home" },
  { label: "Subscription", path: "/subscription" },
  { label: "Support", path: "/support" },
];

/**
 * Sidebar Component
 * Reusable left sidebar with navigation and logo
 */
const Sidebar = ({
  userRole = "GUEST",
  navItems = DEFAULT_NAV_ITEMS,
  onLogout,
}) => {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <div className="w-64 bg-black rounded-xl flex flex-col p-6">
      {/* Logo Section */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-3">
          <img
            src="/Logo.png"
            alt="Logo"
            className="w-18 h-18 rounded-full object-cover"
          />
          <div>
            <h1 className="font-karantina text-3xl text-[#F6A661]">
              HEADPHONES ON
            </h1>
            <p className="text-2xl font-karantina font-thin text-[#F6A661]">
              {userRole}
            </p>
          </div>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex flex-col gap-4 flex-1">
        {navItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`flex items-center gap-3 text-xl font-bold transition-colors ${
              isActive(item.path)
                ? "text-[#FFFBEF]"
                : "text-[#F6A661] hover:text-[#FFFBEF]"
            }`}
          >
            {item.icon && <item.icon className="w-6 h-6" />}
            <span>{item.label}</span>
          </Link>
        ))}

        {onLogout && (
          <button
            onClick={onLogout}
            className="flex items-center gap-3 text-[#F6A661] text-xl font-bold hover:text-[#FFFBEF] transition-colors text-left"
          >
            <span>Log out</span>
          </button>
        )}
      </nav>
    </div>
  );
};

export default Sidebar;

