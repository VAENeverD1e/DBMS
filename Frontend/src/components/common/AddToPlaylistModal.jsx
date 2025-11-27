import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FaTimes, FaPlus } from "react-icons/fa";
import { usePlaylist } from "../../contexts/PlaylistContext";
import { useToast } from "../../contexts/ToastContext";

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
  onSuccess,
  onError,
  songId,
}) => {
  const { playlists: contextPlaylists, loading, addSongToPlaylist, fetchPlaylists } = usePlaylist();
  const { addToast } = useToast();
  const [selectedPlaylistId, setSelectedPlaylistId] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);
  const [successMsg, setSuccessMsg] = useState(null);

  // Fetch playlists when modal opens
  useEffect(() => {
    if (isOpen && contextPlaylists.length === 0) {
      fetchPlaylists();
    }
  }, [isOpen, contextPlaylists.length, fetchPlaylists]);

  const userPlaylists = playlists.length > 0 ? playlists : contextPlaylists;

  const handleAdd = async () => {
    if (!selectedPlaylistId || !songId) return;

    setIsSubmitting(true);
    setErrorMsg(null);
    setSuccessMsg(null);

    try {
      const result = await addSongToPlaylist(selectedPlaylistId, songId);
      if (result.success) {
        const successMessage = "Song added to playlist successfully!";
        setSuccessMsg(successMessage);
        addToast(successMessage, "success");
        onSuccess?.(selectedPlaylistId);
        onAddToPlaylist?.(selectedPlaylistId);
        setSelectedPlaylistId(null);
        setTimeout(() => onClose(), 500);
      } else {
        const msg = result.isDuplicate
          ? "This song is already in the playlist"
          : result.error || "Failed to add song to playlist";
        setErrorMsg(msg);
        addToast(msg, "error");
        onError?.(msg);
      }
    } catch (error) {
      const msg = error.message || "An error occurred while adding the song";
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
            {/* Error Message */}
            {errorMsg && (
              <div className="bg-red-500/20 border border-red-500 text-red-300 px-4 py-3 rounded-lg mb-4">
                {errorMsg}
              </div>
            )}
            
            {/* Success Message */}
            {successMsg && (
              <div className="bg-green-500/20 border border-green-500 text-green-300 px-4 py-3 rounded-lg mb-4">
                {successMsg}
              </div>
            )}
            
            {/* Create New Playlist Button */}
            <button
              onClick={() => {
                onCreateNew?.();
                onClose();
              }}
              disabled={isSubmitting || loading}
              className="w-full bg-[#F6A661] text-[#3E3B2C] px-6 py-4 rounded-xl font-bold hover:bg-[#E5954F] transition-colors flex items-center justify-center gap-2 mb-6 disabled:opacity-50"
            >
              <FaPlus className="w-5 h-5" />
              Create New Playlist
            </button>

            {/* Loading State */}
            {loading && contextPlaylists.length === 0 && (
              <div className="text-center text-gray-400 py-8">
                <p>Loading playlists...</p>
              </div>
            )}

            {/* Empty State */}
            {!loading && userPlaylists.length === 0 && (
              <div className="text-center text-gray-400 py-8">
                <p>No playlists yet. Create one to get started!</p>
              </div>
            )}

            {/* Playlists List */}
            {userPlaylists.length > 0 && (
            <div className="space-y-3">
              {userPlaylists.map((playlist) => (
                <motion.div
                  key={playlist.playlist_id || playlist.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  onClick={() => !isSubmitting && setSelectedPlaylistId(playlist.playlist_id || playlist.id)}
                  className={`flex items-center gap-4 p-4 rounded-xl cursor-pointer transition-colors ${
                    selectedPlaylistId === (playlist.playlist_id || playlist.id)
                      ? "bg-[#F6A661]/20 border-2 border-[#F6A661]"
                      : "bg-[#3E3B2C] hover:bg-[#3E3B2C]/80"
                  } ${isSubmitting ? "opacity-50" : ""}`}
                >
                  <img
                    src={playlist.image || playlist.cover_image}
                    alt={playlist.name}
                    className="w-16 h-16 rounded-xl object-cover"
                    onError={(e) => {
                      e.target.src = `https://via.placeholder.com/64x64/3E3B2C/F6A661?text=${playlist.name}`;
                    }}
                  />
                  <div className="flex-1">
                    <p className="text-white font-semibold">{playlist.name}</p>
                    {(playlist.song_count !== undefined || playlist.songs) && (
                      <p className="text-gray-400 text-sm">
                        {playlist.song_count || playlist.songs?.length || 0} songs
                      </p>
                    )}
                  </div>
                  {selectedPlaylistId === (playlist.playlist_id || playlist.id) && (
                    <div className="w-6 h-6 rounded-full bg-[#F6A661] flex items-center justify-center">
                      <div className="w-2 h-2 rounded-full bg-[#3E3B2C]"></div>
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
            )}
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
              onClick={handleAdd}
              disabled={!selectedPlaylistId || isSubmitting || loading || !songId}
              className={`px-6 py-2 rounded-full font-bold transition-colors ${
                selectedPlaylistId && !isSubmitting && !loading && songId
                  ? "bg-[#F6A661] text-[#3E3B2C] hover:bg-[#E5954F]"
                  : "bg-gray-600 text-gray-400 cursor-not-allowed"
              }`}
            >
              {isSubmitting ? "Adding..." : "Add"}
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

export default AddToPlaylistModal;

