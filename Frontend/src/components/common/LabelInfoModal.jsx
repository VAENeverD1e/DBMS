import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FaTimes } from "react-icons/fa";
import labelService from "@services/labelService";

/**
 * LabelInfoModal Component
 * 
 * Modal displaying label information and all artists belonging to the label
 */
const LabelInfoModal = ({ isOpen, onClose, labelId }) => {
  const [label, setLabel] = useState(null);
  const [artists, setArtists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isOpen && labelId) {
      const fetchLabelData = async () => {
        try {
          setLoading(true);
          setError(null);
          
          // Fetch label and artists in parallel
          const [labelRes, artistsRes] = await Promise.all([
            labelService.getLabelById(labelId),
            labelService.getLabelArtists(labelId),
          ]);

          if (labelRes && labelRes.label) {
            setLabel(labelRes.label);
          }

          if (artistsRes && artistsRes.artists) {
            setArtists(artistsRes.artists);
          }
        } catch (err) {
          console.error("Error fetching label data:", err);
          setError("Failed to load label information");
        } finally {
          setLoading(false);
        }
      };

      fetchLabelData();
    }
  }, [isOpen, labelId]);

  if (!isOpen) return null;

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
            <h2 className="text-4xl font-bold text-[#F6A661]">
              {loading ? "Loading..." : label ? label.Name : "Label"}
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <FaTimes className="w-6 h-6" />
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-6 scrollbar-hide">
            {loading ? (
              <div className="text-white text-center py-8">Loading label information...</div>
            ) : error ? (
              <div className="text-red-400 text-center py-8">{error}</div>
            ) : label ? (
              <>
                {/* Label Information */}
                <div className="mb-6 space-y-2">
                  {label.Country && (
                    <p className="text-white text-base">
                      <span className="font-semibold">Country:</span> {label.Country}
                    </p>
                  )}
                  {label.FoundedYear && (
                    <p className="text-white text-base">
                      <span className="font-semibold">Founded:</span> {label.FoundedYear}
                    </p>
                  )}
                  {label.ContactEmail && (
                    <p className="text-white text-base">
                      <span className="font-semibold">Contact:</span> {label.ContactEmail}
                    </p>
                  )}
                </div>

                {/* Artists Section */}
                <div>
                  <h3 className="text-2xl font-bold text-white mb-4">Artists</h3>
                  {artists.length > 0 ? (
                    <div className="grid grid-cols-4 gap-4">
                      {artists.map((artist, index) => (
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
                  ) : (
                    <p className="text-gray-400">No artists in this label yet.</p>
                  )}
                </div>
              </>
            ) : (
              <div className="text-white text-center py-8">Label not found</div>
            )}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

export default LabelInfoModal;

