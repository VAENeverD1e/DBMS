import React from "react";
import { motion } from "framer-motion";
import { FaHeadphones, FaMicrophone } from "react-icons/fa";

/**
 * AccessModal Component
 * Modal for selecting between LISTENER and ARTIST access
 */
const AccessModal = ({ isOpen, onClose, onSelect }) => {
  if (!isOpen) return null;

  const handleSelect = (type) => {
    onSelect(type);
    onClose();
  };

  return (
    <div
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 backdrop-blur-md"
      onClick={onClose}
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
        className="bg-[#FFFBEF] rounded-3xl p-12 border-2 border-[#3E3B2C] max-w-2xl w-full mx-4"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="text-5xl font-bold text-[#F6A661] font-karantina text-center mb-8">
          HAVE A FULL ACCESS!
        </h2>
        <div className="flex gap-8 justify-center">
          {/* Become Listener Button */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => handleSelect("listener")}
            className="bg-[#F6A661] rounded-3xl p-10 flex flex-col items-center gap-4 hover:bg-[#E5954F] transition-colors w-64"
          >
            <FaHeadphones className="w-20 h-20 text-[#3E3B2C]" />
            <span className="text-[#3E3B2C] font-bold text-xl">BECOME LISTENER</span>
          </motion.button>

          {/* Become Artist Button */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => handleSelect("artist")}
            className="bg-[#F6A661] rounded-3xl p-10 flex flex-col items-center gap-4 hover:bg-[#E5954F] transition-colors w-64"
          >
            <FaMicrophone className="w-20 h-20 text-[#3E3B2C]" />
            <span className="text-[#3E3B2C] font-bold text-xl">BECOME ARTIST</span>
          </motion.button>
        </div>
      </motion.div>
    </div>
  );
};

export default AccessModal;

