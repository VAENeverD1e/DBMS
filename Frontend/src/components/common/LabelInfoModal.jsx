import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FaTimes } from "react-icons/fa";

/**
 * LabelInfoModal Component
 * 
 * Modal displaying label information and all artists belonging to the label
 */
const LabelInfoModal = ({ isOpen, onClose, labelData }) => {
  if (!isOpen) return null;

  // Sample data structure - will be replaced with actual data from props
  const label = labelData || {
    name: "SM Entertainment",
    description: "SM Entertainment is a South Korean entertainment company established in 1995 by Lee Soo-man. It is one of the largest entertainment companies in South Korea and has produced numerous successful K-pop groups and solo artists.",
    artists: [
      { id: 1, name: "Red Velvet", image: "/ProfilePicArtist.png" },
      { id: 2, name: "Artist 2", image: "/ArtworkImage2.png" },
      { id: 3, name: "Artist 3", image: "/ArtworkImage3.png" },
      { id: 4, name: "Artist 4", image: "/ArtworkImage4.png" },
    ],
  };

  return (
    <AnimatePresence>
      <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          className="bg-[#2A2820] rounded-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-[#3E3B2C]">
            <h2 className="text-4xl font-bold text-[#F6A661]">{label.name}</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <FaTimes className="w-6 h-6" />
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-6 scrollbar-hide">
            {/* Label Description */}
            <div className="mb-6">
              <p className="text-white text-base leading-relaxed">{label.description}</p>
            </div>

            {/* Artists Section */}
            <div>
              <h3 className="text-2xl font-bold text-white mb-4">Artists</h3>
              <div className="grid grid-cols-4 gap-4">
                {label.artists.map((artist, index) => (
                  <motion.div
                    key={artist.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="cursor-pointer hover:scale-105 transition-transform"
                  >
                    <div className="bg-[#3E3B2C] rounded-2xl p-4 flex flex-col items-center">
                      <img
                        src={artist.image}
                        alt={artist.name}
                        className="w-32 h-32 rounded-full object-cover mb-2"
                        onError={(e) => {
                          e.target.src = `https://via.placeholder.com/128x128/3E3B2C/F6A661?text=${artist.name}`;
                        }}
                      />
                      <p className="text-white text-sm font-semibold text-center">{artist.name}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

export default LabelInfoModal;

