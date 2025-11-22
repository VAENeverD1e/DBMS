import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FaTimes, FaPlus, FaUpload, FaTrash } from "react-icons/fa";

/**
 * UploadArtworkModal Component
 * 
 * Modal for artists to upload or edit artwork (Single or Album)
 * Features:
 * - Single/Album mode toggle
 * - Genre selection
 * - Collaboration tags
 * - Multiple track uploads (with delete)
 * - Cover image upload
 * - Title input for both single and album
 * - Edit mode support
 */
const UploadArtworkModal = ({
  isOpen,
  onClose,
  onUpload,
  initialData = null, // For edit mode
  isEditMode = false,
}) => {
  const [mode, setMode] = useState("single"); // "single" or "album"
  const [genre, setGenre] = useState("");
  const [collaborations, setCollaborations] = useState([
    "@TaylorSwift",
    "@Drake",
  ]);
  const [tracks, setTracks] = useState([
    { id: 1, file: null, fileName: "Song_name.mp3", title: "Track 1" },
  ]);
  const [coverImage, setCoverImage] = useState(null);
  const [coverImageUrl, setCoverImageUrl] = useState(null); // For existing images
  const [title, setTitle] = useState(""); // Title for both single and album
  const trackFileInputRefs = useRef({});
  const coverInputRef = useRef(null);

  // Genres from the right sidebar
  const genres = [
    "pop",
    "rock",
    "rnb",
    "ballad",
    "folk",
    "alternative",
    "electronic",
    "hyperpop",
    "experimental",
    "rap",
  ];

  // Initialize with existing data if in edit mode
  useEffect(() => {
    if (isOpen && initialData) {
      setMode(initialData.mode || "single");
      setGenre(initialData.genre || "");
      setCollaborations(initialData.collaborations || []);
      setTitle(initialData.title || "");
      setCoverImageUrl(initialData.coverImageUrl || null);
      if (initialData.tracks && initialData.tracks.length > 0) {
        setTracks(
          initialData.tracks.map((track, index) => ({
            id: track.id || index + 1,
            file: null,
            fileName: track.fileName || `Song_name.mp3`,
            title: track.title || `Track ${index + 1}`,
          }))
        );
      } else {
        setTracks([
          { id: 1, file: null, fileName: "Song_name.mp3", title: "Track 1" },
        ]);
      }
    } else if (isOpen && !initialData) {
      // Reset for new upload
      setMode("single");
      setGenre("");
      setCollaborations(["@TaylorSwift", "@Drake"]);
      setTracks([{ id: 1, file: null, fileName: "Song_name.mp3", title: "Track 1" }]);
      setTitle("");
      setCoverImage(null);
      setCoverImageUrl(null);
    }
  }, [isOpen, initialData]);

  const handleAddCollaboration = () => {
    const newCollab = prompt("Enter collaborator username (e.g., @username):");
    if (newCollab && !collaborations.includes(newCollab)) {
      setCollaborations([...collaborations, newCollab]);
    }
  };

  const handleRemoveCollaboration = (collab) => {
    setCollaborations(collaborations.filter((c) => c !== collab));
  };

  const handleAddTrack = () => {
    // Only allow adding tracks in album mode
    if (mode === "album") {
      const newTrack = {
        id: tracks.length + 1,
        file: null,
        fileName: "Song_name.mp3",
        title: `Track ${tracks.length + 1}`,
      };
      setTracks([...tracks, newTrack]);
    }
  };

  const handleDeleteTrack = (trackId) => {
    // Don't allow deleting if it's the only track
    if (tracks.length > 1) {
      setTracks(tracks.filter((track) => track.id !== trackId));
      // Clean up ref
      delete trackFileInputRefs.current[trackId];
    }
  };

  const handleTrackFileChange = (trackId, file) => {
    if (file) {
      setTracks(
        tracks.map((track) =>
          track.id === trackId
            ? { ...track, file, fileName: file.name }
            : track
        )
      );
    }
  };

  const handleTrackTitleChange = (trackId, title) => {
    setTracks(
      tracks.map((track) =>
        track.id === trackId ? { ...track, title } : track
      )
    );
  };

  const handleCoverImageChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      setCoverImage(file);
    }
  };

  const handleUpload = () => {
    const artworkData = {
      mode,
      genre,
      collaborations,
      tracks: tracks.map((t) => ({
        id: t.id,
        file: t.file,
        fileName: t.fileName,
        title: t.title,
      })),
      coverImage,
      coverImageUrl,
      title,
      isEditMode,
    };
    onUpload?.(artworkData);
    // Reset form
    setMode("single");
    setGenre("");
    setCollaborations(["@TaylorSwift", "@Drake"]);
    setTracks([{ id: 1, file: null, fileName: "Song_name.mp3", title: "Track 1" }]);
    setCoverImage(null);
    setCoverImageUrl(null);
    setTitle("");
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
          className="bg-[#2A2820] rounded-2xl w-full max-w-5xl max-h-[90vh] overflow-hidden flex flex-col"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-[#3E3B2C]">
            <h2 className="text-5xl font-bold font-karantina text-[#F6A661]">
              ARTWORK INFORMATION
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <FaTimes className="w-6 h-6" />
            </button>
          </div>

          {/* Mode Toggle */}
          <div className="p-6 border-b border-[#3E3B2C]">
            <div className="flex gap-4">
              <button
                onClick={() => {
                  setMode("single");
                  // In single mode, keep only 1 track
                  if (tracks.length > 1) {
                    setTracks([tracks[0]]);
                  }
                }}
                className={`flex-1 px-6 py-3 rounded-full font-bold transition-colors ${
                  mode === "single"
                    ? "bg-white text-[#3E3B2C]"
                    : "bg-[#F6A661] text-white"
                }`}
              >
                Single
              </button>
              <button
                onClick={() => setMode("album")}
                className={`flex-1 px-6 py-3 rounded-full font-bold transition-colors ${
                  mode === "album"
                    ? "bg-white text-[#3E3B2C]"
                    : "bg-[#F6A661] text-white"
                }`}
              >
                Album
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-6 scrollbar-hide">
            <div className="grid grid-cols-2 gap-6">
              {/* Left Panel */}
              <div className="space-y-6">
                {/* Genre */}
                <div>
                  <label className="block text-white font-bold mb-2">
                    GENRE:
                  </label>
                  <select
                    value={genre}
                    onChange={(e) => setGenre(e.target.value)}
                    className="w-full bg-white text-[#3E3B2C] px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#F6A661]"
                  >
                    <option value="">Select a genre</option>
                    {genres.map((g) => (
                      <option key={g} value={g}>
                        {g.charAt(0).toUpperCase() + g.slice(1)}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Collaboration */}
                <div>
                  <label className="block text-white font-bold mb-2">
                    COLLABORATION:
                  </label>
                  <div className="flex flex-wrap gap-2 mb-2">
                    {collaborations.map((collab) => (
                      <div
                        key={collab}
                        className="bg-[#3E3B2C] text-white px-4 py-2 rounded-full flex items-center gap-2"
                      >
                        <span>{collab}</span>
                        <button
                          onClick={() => handleRemoveCollaboration(collab)}
                          className="text-gray-400 hover:text-white"
                        >
                          <FaTimes className="w-3 h-3" />
                        </button>
                      </div>
                    ))}
                  </div>
                  <button
                    onClick={handleAddCollaboration}
                    className="bg-gray-600 text-white px-4 py-2 rounded-full text-sm hover:bg-gray-500 transition-colors"
                  >
                    Add a new one
                  </button>
                </div>

                {/* Upload Music Track */}
                <div>
                  <label className="block text-white font-bold mb-2">
                    UPLOAD MUSIC TRACK:
                  </label>
                  <div className="space-y-3">
                    {tracks.map((track) => (
                      <div key={track.id} className="grid grid-cols-[1fr_1fr_auto] gap-2 items-center">
                        <div className="relative">
                          <button
                            type="button"
                            onClick={() => {
                              const input = trackFileInputRefs.current[track.id];
                              if (input) {
                                input.click();
                              }
                            }}
                            className="w-full bg-[#3E3B2C] text-white px-4 py-2 rounded-lg text-sm flex items-center justify-center hover:bg-[#3E3B2C]/80 transition-colors cursor-pointer"
                          >
                            {track.file ? track.fileName : "Upload MP3"}
                          </button>
                          <input
                            ref={(el) =>
                              (trackFileInputRefs.current[track.id] = el)
                            }
                            type="file"
                            accept="audio/mpeg,audio/mp3"
                            onChange={(e) =>
                              handleTrackFileChange(
                                track.id,
                                e.target.files?.[0]
                              )
                            }
                            className="hidden"
                          />
                        </div>
                        <input
                          type="text"
                          value={track.title}
                          onChange={(e) =>
                            handleTrackTitleChange(track.id, e.target.value)
                          }
                          placeholder={track.title}
                          className="bg-white text-[#3E3B2C] px-4 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#F6A661]"
                        />
                        {tracks.length > 1 && (
                          <button
                            type="button"
                            onClick={() => handleDeleteTrack(track.id)}
                            className="text-red-500 hover:text-red-400 transition-colors p-2"
                            title="Delete track"
                          >
                            <FaTrash className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    ))}
                  </div>
                  {mode === "album" && (
                    <button
                      onClick={handleAddTrack}
                      className="mt-2 bg-gray-600 text-white px-4 py-2 rounded-full text-sm hover:bg-gray-500 transition-colors flex items-center gap-2"
                    >
                      <FaPlus className="w-3 h-3" />
                      Add a new one
                    </button>
                  )}
                </div>

                {/* Warning and Upload Button */}
                <div className="space-y-4">
                  <p className="text-[#F6A661] text-sm">
                    Please check all the information again carefully
                  </p>
                  <button
                    onClick={handleUpload}
                    className="w-full bg-[#F6A661] text-[#3E3B2C] px-6 py-3 rounded-full font-bold hover:bg-[#E5954F] transition-colors flex items-center justify-center gap-2"
                  >
                    <FaUpload className="w-5 h-5" />
                    Upload
                  </button>
                </div>
              </div>

              {/* Right Panel - Fixed height */}
              <div className="bg-[#F6A661] rounded-2xl p-6 flex flex-col h-full">
                {/* Cover Image Upload */}
                <div className="flex-shrink-0 mb-6">
                  <div
                    onClick={() => coverInputRef.current?.click()}
                    className="w-full aspect-square bg-[#2A2820] rounded-xl flex items-center justify-center cursor-pointer hover:bg-[#3E3B2C] transition-colors relative"
                  >
                    {coverImage ? (
                      <img
                        src={URL.createObjectURL(coverImage)}
                        alt="Cover"
                        className="w-full h-full object-cover rounded-xl"
                      />
                    ) : coverImageUrl ? (
                      <img
                        src={coverImageUrl}
                        alt="Cover"
                        className="w-full h-full object-cover rounded-xl"
                      />
                    ) : (
                      <p className="text-white text-lg font-semibold">
                        Upload Cover Image
                      </p>
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

                {/* Title - For both Single and Album */}
                <div className="flex-shrink-0">
                  <label className="block text-[#3E3B2C] font-karantina font-bold text-3xl mb-2">
                    {mode === "album" ? "ALBUM TITLE:" : "TITLE:"}
                  </label>
                  <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder={
                      mode === "album"
                        ? "Enter album title"
                        : "Enter song title"
                    }
                    className="w-full bg-transparent border-b-2 border-[#3E3B2C] text-[#3E3B2C] px-2 py-2 focus:outline-none focus:border-[#2A2820]"
                  />
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

export default UploadArtworkModal;

