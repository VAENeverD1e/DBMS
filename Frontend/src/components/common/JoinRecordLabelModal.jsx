import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FaTimes } from "react-icons/fa";

/**
 * JoinRecordLabelModal Component
 * 
 * Modal for artists to join a record label
 * Features:
 * - List of record labels
 * - Information form for selected label
 */
const JoinRecordLabelModal = ({ isOpen, onClose, onJoin }) => {
  const [selectedLabel, setSelectedLabel] = useState("Universal");
  const [formData, setFormData] = useState({
    name: "",
    foundedYear: "",
    country: "",
    contactEmail: "",
  });

  const recordLabels = ["Universal", "HYBE", "Vevo"];

  const handleInputChange = (field, value) => {
    setFormData({ ...formData, [field]: value });
  };

  const handleJoin = () => {
    onJoin?.({
      label: selectedLabel,
      ...formData,
    });
    // Reset form
    setFormData({
      name: "",
      foundedYear: "",
      country: "",
      contactEmail: "",
    });
    onClose();
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          className="bg-[#2A2820] rounded-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex"
        >
          {/* Left Panel - List of Record Labels */}
          <div className="w-1/2 p-6 border-r border-[#3E3B2C] flex flex-col">
            <h2 className="text-4xl font-bold font-karantina text-[#F6A661] mb-6">
              LIST OF RECORD LABEL
            </h2>
            <div className="flex flex-wrap gap-3 mb-6">
              {recordLabels.map((label) => (
                <button
                  key={label}
                  onClick={() => setSelectedLabel(label)}
                  className={`px-6 py-3 rounded-lg font-bold transition-colors ${
                    selectedLabel === label
                      ? "bg-[#F6A661] text-[#3E3B2C]"
                      : "bg-white text-[#3E3B2C] hover:bg-gray-100"
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>
            {/* Scrollable area for more labels */}
            <div className="flex-1 overflow-y-auto scrollbar-hide">
              {/* Additional labels can be added here */}
            </div>
          </div>

          {/* Right Panel - Information */}
          <div className="w-1/2 bg-[#F6A661] p-6 flex flex-col">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-4xl font-bold font-karantina text-[#3E3B2C]">INFORMATION</h2>
              <button
                onClick={onClose}
                className="text-[#3E3B2C] hover:text-[#2A2820] transition-colors"
              >
                <FaTimes className="w-6 h-6" />
              </button>
            </div>
            <div className="space-y-4 flex-1">
              <div>
                <label className="block text-[#3E3B2C] font-bold mb-2">
                  Name
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => handleInputChange("name", e.target.value)}
                  placeholder="label's name"
                  className="w-full bg-[#FFF8E7] text-[#3E3B2C] px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#3E3B2C]"
                />
              </div>
              <div>
                <label className="block text-[#3E3B2C] font-bold mb-2">
                  Founded Year
                </label>
                <input
                  type="text"
                  value={formData.foundedYear}
                  onChange={(e) =>
                    handleInputChange("foundedYear", e.target.value)
                  }
                  placeholder="label founded year"
                  className="w-full bg-[#FFF8E7] text-[#3E3B2C] px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#3E3B2C]"
                />
              </div>
              <div>
                <label className="block text-[#3E3B2C] font-bold mb-2">
                  Country
                </label>
                <input
                  type="text"
                  value={formData.country}
                  onChange={(e) => handleInputChange("country", e.target.value)}
                  placeholder="label country"
                  className="w-full bg-[#FFF8E7] text-[#3E3B2C] px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#3E3B2C]"
                />
              </div>
              <div>
                <label className="block text-[#3E3B2C] font-bold mb-2">
                  Contact Email
                </label>
                <input
                  type="email"
                  value={formData.contactEmail}
                  onChange={(e) =>
                    handleInputChange("contactEmail", e.target.value)
                  }
                  placeholder="label record contact email"
                  className="w-full bg-[#FFF8E7] text-[#3E3B2C] px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#3E3B2C]"
                />
              </div>
            </div>
            <button
              onClick={handleJoin}
              className="mt-6 w-full bg-[#FFF8E7] text-[#3E3B2C] px-6 py-3 rounded-full font-bold hover:bg-[#F5F0D8] transition-colors"
            >
              Join
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

export default JoinRecordLabelModal;

