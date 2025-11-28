import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FaTimes } from "react-icons/fa";
import labelService from "@services/labelService";

/**
 * JoinRecordLabelModal Component
 * 
 * Modal for artists to join a record label
 * Features:
 * - List of record labels from database
 * - Information display for selected label
 */
const JoinRecordLabelModal = ({ isOpen, onClose, onJoin }) => {
  const [labels, setLabels] = useState([]);
  const [selectedLabel, setSelectedLabel] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch labels from backend when modal opens
  useEffect(() => {
    if (isOpen) {
      const fetchLabels = async () => {
        try {
          setLoading(true);
          setError(null);
          const response = await labelService.getLabels();
          if (response && response.labels) {
            setLabels(response.labels);
            if (response.labels.length > 0) {
              setSelectedLabel(response.labels[0]);
            }
          }
        } catch (err) {
          console.error("Error fetching labels:", err);
          setError("Failed to load labels");
        } finally {
          setLoading(false);
        }
      };
      fetchLabels();
    }
  }, [isOpen]);

  const handleJoin = () => {
    if (!selectedLabel) {
      alert("Please select a label");
      return;
    }
    onJoin?.(selectedLabel);
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
            {loading ? (
              <div className="text-white text-center py-8">Loading labels...</div>
            ) : error ? (
              <div className="text-red-400 text-center py-8">{error}</div>
            ) : (
              <>
                <div className="flex-1 overflow-y-auto scrollbar-hide mb-6">
                  <div className="flex flex-wrap gap-3">
                    {labels.map((label) => (
                      <button
                        key={label.LabelID}
                        onClick={() => setSelectedLabel(label)}
                        className={`px-6 py-3 rounded-lg font-bold transition-colors ${
                          selectedLabel?.LabelID === label.LabelID
                            ? "bg-[#F6A661] text-[#3E3B2C]"
                            : "bg-white text-[#3E3B2C] hover:bg-gray-100"
                        }`}
                      >
                        {label.Name}
                      </button>
                    ))}
                  </div>
                </div>
              </>
            )}
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
            {selectedLabel ? (
              <>
                <div className="space-y-4 flex-1">
                  <div>
                    <label className="block text-[#3E3B2C] font-bold mb-2">
                      Name
                    </label>
                    <div className="w-full bg-[#FFF8E7] text-[#3E3B2C] px-4 py-2 rounded-lg">
                      {selectedLabel.Name}
                    </div>
                  </div>
                  <div>
                    <label className="block text-[#3E3B2C] font-bold mb-2">
                      Founded Year
                    </label>
                    <div className="w-full bg-[#FFF8E7] text-[#3E3B2C] px-4 py-2 rounded-lg">
                      {selectedLabel.FoundedYear || "N/A"}
                    </div>
                  </div>
                  <div>
                    <label className="block text-[#3E3B2C] font-bold mb-2">
                      Country
                    </label>
                    <div className="w-full bg-[#FFF8E7] text-[#3E3B2C] px-4 py-2 rounded-lg">
                      {selectedLabel.Country || "N/A"}
                    </div>
                  </div>
                  <div>
                    <label className="block text-[#3E3B2C] font-bold mb-2">
                      Contact Email
                    </label>
                    <div className="w-full bg-[#FFF8E7] text-[#3E3B2C] px-4 py-2 rounded-lg">
                      {selectedLabel.ContactEmail || "N/A"}
                    </div>
                  </div>
                </div>
                <button
                  onClick={handleJoin}
                  className="mt-6 w-full bg-[#FFF8E7] text-[#3E3B2C] px-6 py-3 rounded-full font-bold hover:bg-[#F5F0D8] transition-colors"
                >
                  Join
                </button>
              </>
            ) : (
              <div className="flex-1 flex items-center justify-center text-[#3E3B2C]">
                {loading ? "Loading..." : "Select a label to view information"}
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

export default JoinRecordLabelModal;

