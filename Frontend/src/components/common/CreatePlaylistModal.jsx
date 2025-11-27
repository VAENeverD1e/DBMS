import React, { useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FaTimes, FaUpload } from "react-icons/fa";
import { usePlaylist } from "../../contexts/PlaylistContext";
import { useToast } from "../../contexts/ToastContext";

/**
 * CreatePlaylistModal Component
 * 
 * Modal for creating a new playlist
 */
const CreatePlaylistModal = ({ isOpen, onClose, onCreate, onSuccess, onError }) => {
  const { createPlaylist, loading } = usePlaylist();
  const { addToast } = useToast();
  const [playlistName, setPlaylistName] = useState("");
  const [coverImage, setCoverImage] = useState(null);
  const [coverImageUrl, setCoverImageUrl] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);
  const coverInputRef = useRef(null);

  const handleCoverImageChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      setCoverImage(file);
      setCoverImageUrl(URL.createObjectURL(file));
    }
  };

  const handleCreate = async () => {
    if (!playlistName.trim()) return;

    setIsSubmitting(true);
    setErrorMsg(null);

    try {
      const result = await createPlaylist(playlistName);
      if (result.success) {
        addToast(`Playlist "${playlistName}" created successfully!`, "success");
        // Call parent onCreate callback if provided (for backward compatibility)
        onCreate?.({
          name: playlistName,
          coverImage,
          coverImageUrl,
        });
        // Call success callback
        onSuccess?.(result.playlist);
        // Reset form
        setPlaylistName("");
        setCoverImage(null);
        setCoverImageUrl(null);
        onClose();
      } else {
        const msg = result.error || "Failed to create playlist";
        setErrorMsg(msg);
        addToast(msg, "error");
        onError?.(msg);
      }
    } catch (error) {
      const msg = error.message || "An error occurred while creating the playlist";
      setErrorMsg(msg);
      addToast(msg, "error");
      onError?.(msg);
    } finally {
      setIsSubmitting(false);
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
            <h2 className="text-3xl font-bold text-[#F6A661]">Create New Playlist</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <FaTimes className="w-6 h-6" />
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-6 scrollbar-hide">
            <div className="space-y-6">
              {/* Error Message */}
              {errorMsg && (
                <div className="bg-red-500/20 border border-red-500 text-red-300 px-4 py-3 rounded-lg">
                  {errorMsg}
                </div>
              )}
              
              {/* Playlist Name */}
              <div>
                <label className="block text-white font-bold mb-2">Playlist Name</label>
                <input
                  type="text"
                  value={playlistName}
                  onChange={(e) => setPlaylistName(e.target.value)}
                  placeholder="Enter playlist name"
                  disabled={isSubmitting || loading}
                  className="w-full bg-white text-[#3E3B2C] px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#F6A661] disabled:opacity-50"
                />
              </div>

              {/* Cover Image */}
              <div>
                <label className="block text-white font-bold mb-2">Cover Image (Optional)</label>
                <div
                  onClick={() => coverInputRef.current?.click()}
                  className="w-full aspect-square bg-[#3E3B2C] rounded-xl flex items-center justify-center cursor-pointer hover:bg-[#3E3B2C]/80 transition-colors"
                >
                  {coverImageUrl ? (
                    <img
                      src={coverImageUrl}
                      alt="Cover"
                      className="w-full h-full object-cover rounded-xl"
                    />
                  ) : (
                    <div className="flex flex-col items-center gap-2">
                      <FaUpload className="w-8 h-8 text-gray-400" />
                      <p className="text-gray-400 text-sm">Upload Cover Image</p>
                    </div>
                  )}
                </div>
                <input
                  ref={coverInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleCoverImageChange}
                  className="hidden"
                />
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="p-6 border-t border-[#3E3B2C] flex items-center justify-end gap-4">
            <button
              onClick={onClose}
              disabled={isSubmitting || loading}
              className="px-6 py-2 text-white hover:text-gray-300 transition-colors disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              onClick={handleCreate}
              disabled={!playlistName.trim() || isSubmitting || loading}
              className={`px-6 py-2 rounded-full font-bold transition-colors ${
                playlistName.trim() && !isSubmitting && !loading
                  ? "bg-[#F6A661] text-[#3E3B2C] hover:bg-[#E5954F]"
                  : "bg-gray-600 text-gray-400 cursor-not-allowed"
              }`}
            >
              {isSubmitting || loading ? "Creating..." : "Create"}
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

export default CreatePlaylistModal;

