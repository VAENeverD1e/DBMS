import { useState } from "react";
import { Link } from "react-router-dom";
import { Plus, X } from "lucide-react";

export default function FloatingMenu() {
  const [open, setOpen] = useState(false);

  const menuItems = [
    { label: "Landing", path: "/" },
    { label: "Login", path: "/login" },
    { label: "Signup", path: "/signup" },
    { label: "Home", path: "/home" },
    { label: "Listener", path: "/listener" },
    { label: "Subscription", path: "/subscription" },
    { label: "Profile", path: "/profile" },
    {label : "Album Detail", path: "/album/1" },
    {label : "Artist Profile", path: "/artist/1" }
  ];

  return (
    <div className="fixed bottom-8 right-8 z-40">
      {/* FAB button */}
      <button
        onClick={() => setOpen(!open)}
        className="w-14 h-14 rounded-full bg-gradient-to-r from-purple-600 to-blue-600 text-white text-2xl flex items-center justify-center shadow-lg hover:shadow-xl hover:scale-110 transition-all duration-300"
      >
        {open ? <X className="h-6 w-6" /> : <Plus className="h-6 w-6" />}
      </button>

      {/* Modal overlay */}
      {open && (
        <>
          <div
            className="fixed inset-0 bg-black bg-opacity-30 z-40"
            onClick={() => setOpen(false)}
          ></div>
          <div className="absolute bottom-20 right-0 bg-white rounded-2xl shadow-2xl w-72 p-6 z-50 animate-in fade-in slide-in-from-bottom-4 duration-300">
            <h2 className="text-lg font-bold mb-4 text-gray-800">Navigate To</h2>
            <div className="grid grid-cols-1 gap-2 max-h-96 overflow-y-auto">
              {menuItems.map((item, index) => (
                <Link
                  key={index}
                  to={item.path}
                  className="block px-4 py-3 text-sm font-medium text-gray-700 rounded-lg border border-gray-200 hover:bg-purple-50 hover:border-purple-300 hover:text-purple-600 transition-colors"
                  onClick={() => setOpen(false)}
                >
                  {item.label}
                </Link>
              ))}
            </div>

            <button
              onClick={() => setOpen(false)}
              className="mt-4 w-full px-4 py-2 rounded-lg bg-gradient-to-r from-purple-600 to-blue-600 text-white font-medium hover:shadow-lg transition-shadow"
            >
              Close
            </button>
          </div>
        </>
      )}
    </div>
  );
}
