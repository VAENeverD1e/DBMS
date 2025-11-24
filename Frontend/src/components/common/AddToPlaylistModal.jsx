import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FaTimes, FaPlus } from "react-icons/fa";

/**
 * AddToPlaylistModal Component
 * 
 * Modal for adding songs/albums to playlists
 */
const AddToPlaylistModal = ({
  isOpen,
  onClose,
  playlists = [],
  onCreateNew,
  onAddToPlaylist,
}) => {
  const [selectedPlaylistId, setSelectedPlaylistId] = useState(null);

  // Sample playlists - will be replaced with actual data from props
  const userPlaylists = playlists.length > 0 ? playlists : [
    { id: 1, name: "My Liked Song", image: "/ArtworkImage5.png" },
    { id: 2, name: "Playlist 1", image: "/ArtworkImage6.png" },
    { id: 3, name: "Playlist 2", image: "/ArtworkImage7.png" },
    { id: 4, name: "Playlist 3", image: "/ArtworkImage8.png" },
  ];

  const handleAdd = () => {
    if (selectedPlaylistId) {
      onAddToPlaylist?.(selectedPlaylistId);
      setSelectedPlaylistId(null);
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          className="bg-[#2A2820] rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-[#3E3B2C]">
            <h2 className="text-3xl font-bold text-[#F6A661]">Add to Playlist</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <FaTimes className="w-6 h-6" />
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-6 scrollbar-hide">
            {/* Create New Playlist Button */}
            <button
              onClick={() => {
                onCreateNew?.();
                onClose();
              }}
              className="w-full bg-[#F6A661] text-[#3E3B2C] px-6 py-4 rounded-xl font-bold hover:bg-[#E5954F] transition-colors flex items-center justify-center gap-2 mb-6"
            >
              <FaPlus className="w-5 h-5" />
              Create New Playlist
            </button>

            {/* Playlists List */}
            <div className="space-y-3">
              {userPlaylists.map((playlist) => (
                <motion.div
                  key={playlist.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  onClick={() => setSelectedPlaylistId(playlist.id)}
                  className={`flex items-center gap-4 p-4 rounded-xl cursor-pointer transition-colors ${
                    selectedPlaylistId === playlist.id
                      ? "bg-[#F6A661]/20 border-2 border-[#F6A661]"
                      : "bg-[#3E3B2C] hover:bg-[#3E3B2C]/80"
                  }`}
                >
                  <img
                    src={playlist.image}
                    alt={playlist.name}
                    className="w-16 h-16 rounded-xl object-cover"
                    onError={(e) => {
                      e.target.src = `https://via.placeholder.com/64x64/3E3B2C/F6A661?text=${playlist.name}`;
                    }}
                  />
                  <div className="flex-1">
                    <p className="text-white font-semibold">{playlist.name}</p>
                  </div>
                  {selectedPlaylistId === playlist.id && (
                    <div className="w-6 h-6 rounded-full bg-[#F6A661] flex items-center justify-center">
                      <div className="w-2 h-2 rounded-full bg-[#3E3B2C]"></div>
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          </div>

          {/* Footer */}
          <div className="p-6 border-t border-[#3E3B2C] flex items-center justify-end gap-4">
            <button
              onClick={onClose}
              className="px-6 py-2 text-white hover:text-gray-300 transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={handleAdd}
              disabled={!selectedPlaylistId}
              className={`px-6 py-2 rounded-full font-bold transition-colors ${
                selectedPlaylistId
                  ? "bg-[#F6A661] text-[#3E3B2C] hover:bg-[#E5954F]"
                  : "bg-gray-600 text-gray-400 cursor-not-allowed"
              }`}
            >
              Add
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

export default AddToPlaylistModal;

