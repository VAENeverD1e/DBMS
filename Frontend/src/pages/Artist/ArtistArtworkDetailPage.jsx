import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { motion } from "framer-motion";
import { FaPlay, FaHeart, FaEdit, FaTrash } from "react-icons/fa";
import { Sidebar } from "@components/layout";
import { UploadArtworkModal } from "@components/common";

/**
 * ArtistArtworkDetailPage Component
 * 
 * Displays detailed information about an artwork for artists
 * Features:
 * - Album cover and metadata
 * - Tracklist with play controls
 * - Edit button for artist to edit artwork
 * - Delete functionality
 * - No top bar, no bottom player bar
 */
const ArtistArtworkDetailPage = () => {
  const navigate = useNavigate();
  const { id } = useParams(); // Get artwork ID from URL for backend integration
  const [isLiked, setIsLiked] = useState(false);
  const [currentTrackId, setCurrentTrackId] = useState(null);
  const [showEditModal, setShowEditModal] = useState(false);

  // Sample data - This will be replaced with API call using the id parameter
  const albumData = {
    id: id || 1,
    title: "Song name",
    artist: "Artist name",
    year: 2017,
    image: "/ProfilePicArtist.png",
    songCount: 9,
    duration: "31 min",
  };

  // Tracklist data - This will be fetched from backend using artwork id
  const tracks = [
    { id: 1, number: 1, title: "Song name", artist: "Artist name", plays: 3000, duration: "3:09" },
    { id: 2, number: 2, title: "Song name", artist: "Artist name", plays: 3000, duration: "3:09" },
    { id: 3, number: 3, title: "Song name", artist: "Artist name", plays: 3000, duration: "3:09" },
    { id: 4, number: 4, title: "Song name", artist: "Artist name", plays: 3000, duration: "3:09" },
    { id: 5, number: 5, title: "Song name", artist: "Artist name", plays: 3000, duration: "3:09" },
    { id: 6, number: 6, title: "Song name", artist: "Artist name", plays: 3000, duration: "3:09" },
    { id: 7, number: 7, title: "Song name", artist: "Artist name", plays: 3000, duration: "3:09" },
    { id: 8, number: 8, title: "Song name", artist: "Artist name", plays: 3000, duration: "3:09" },
    { id: 9, number: 9, title: "Song name", artist: "Artist name", plays: 3000, duration: "3:09" },
  ];

  const handleLogout = () => {
    navigate("/");
  };

  const handleTrackClick = (trackId) => {
    setCurrentTrackId(trackId);
  };

  const handleEdit = () => {
    setShowEditModal(true);
  };

  const handleSaveEdit = (artworkData) => {
    console.log("Saving edited artwork:", artworkData);
    // Here you would send the updated data to the backend
    setShowEditModal(false);
    // Optionally refresh the page data
  };

  // Prepare initial data for edit modal
  const getEditModalData = () => {
    return {
      mode: albumData.songCount === 1 ? "single" : "album",
      genre: "pop", // This should come from backend
      collaborations: [], // This should come from backend
      title: albumData.title,
      coverImageUrl: albumData.image,
      tracks: tracks.map((track) => ({
        id: track.id,
        fileName: `${track.title}.mp3`,
        title: track.title,
      })),
    };
  };

  const handleDelete = () => {
    if (window.confirm("Are you sure you want to delete this artwork?")) {
      // Delete artwork
      console.log("Deleting artwork:", albumData.id);
      navigate("/artist/home");
    }
  };

  const handleDeleteTrack = (trackId) => {
    if (window.confirm("Are you sure you want to delete this track?")) {
      // Delete track
      console.log("Deleting track:", trackId);
    }
  };

  const artistNavItems = [
    { label: "Home", path: "/artist/home" },
    { label: "Subscription", path: "/subscription" },
    { label: "Support", path: "/support" },
  ];

  return (
    <div className="flex h-screen bg-[#3E3B2C] overflow-hidden">
      {/* Left Sidebar */}
      <Sidebar userRole="ARTIST" navItems={artistNavItems} onLogout={handleLogout} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col bg-[#3E3B2C] overflow-hidden">
        {/* Main Content - Scrollable */}
        <div className="flex-1 overflow-y-auto p-6 scrollbar-hide">
          {/* Album Header */}
          <div className="flex gap-6 mb-8">
            <motion.img
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
              src={albumData.image}
              alt={albumData.title}
              className="w-64 h-64 rounded-2xl object-cover flex-shrink-0"
              onError={(e) => {
                e.target.src = `https://via.placeholder.com/400x400/3E3B2C/F6A661?text=${albumData.title}`;
              }}
            />
            <div className="flex-1 flex flex-col justify-end">
              <p className="text-white text-sm mb-2">Album</p>
              <h1 className="text-6xl font-bold text-white mb-4">{albumData.title}</h1>
              <div className="flex items-center gap-2 mb-6">
                <div className="w-2 h-2 bg-[#F6A661] rounded-full"></div>
                <span className="text-white">
                  {albumData.artist} • {albumData.year} • {albumData.songCount} songs, {albumData.duration}
                </span>
              </div>
              <div className="flex items-center gap-4">
                <button className="bg-[#F6A661] text-[#3E3B2C] px-8 py-2 rounded-full font-bold hover:bg-[#E5954F] transition-colors flex items-center gap-2">
                  <FaPlay className="w-4 h-4" />
                  Play
                </button>
                <button
                  onClick={handleEdit}
                  className="bg-transparent border-2 border-[#F6A661] text-[#F6A661] px-8 py-2 rounded-full font-bold hover:bg-[#F6A661] hover:text-[#3E3B2C] transition-colors flex items-center gap-2"
                >
                  <FaEdit className="w-4 h-4" />
                  Edit
                </button>
                <button
                  onClick={handleDelete}
                  className="bg-transparent border-2 border-red-500 text-red-500 px-8 py-2 rounded-full font-bold hover:bg-red-500 hover:text-white transition-colors flex items-center gap-2"
                >
                  <FaTrash className="w-4 h-4" />
                  Delete
                </button>
                <button
                  onClick={() => setIsLiked(!isLiked)}
                  className={`p-3 rounded-full transition-colors ${
                    isLiked
                      ? "bg-[#F6A661] text-[#3E3B2C]"
                      : "bg-transparent border-2 border-[#F6A661] text-[#F6A661] hover:bg-[#F6A661] hover:text-[#3E3B2C]"
                  }`}
                >
                  <FaHeart className="w-6 h-6" />
                </button>
              </div>
            </div>
          </div>

          {/* Tracklist */}
          <div className="bg-[#2A2820] rounded-2xl p-6">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-600">
                  <th className="text-left text-gray-400 font-bold pb-4">#</th>
                  <th className="text-left text-gray-400 font-bold pb-4">Title</th>
                  <th className="text-left text-gray-400 font-bold pb-4">Liked</th>
                  <th className="text-right text-gray-400 font-bold pb-4">Duration</th>
                  <th className="text-right text-gray-400 font-bold pb-4">Actions</th>
                </tr>
              </thead>
              <tbody>
                {tracks.map((track) => (
                  <motion.tr
                    key={track.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: track.number * 0.05 }}
                    onClick={() => handleTrackClick(track.id)}
                    className={`border-b border-gray-700/50 cursor-pointer hover:bg-[#3E3B2C]/50 transition-colors ${
                      currentTrackId === track.id ? "bg-[#F6A661]/20" : ""
                    }`}
                  >
                    <td className={`py-4 ${currentTrackId === track.id ? "text-[#F6A661]" : "text-gray-400"}`}>
                      {track.number}
                    </td>
                    <td className="py-4">
                      <div>
                        <p className={`font-semibold ${currentTrackId === track.id ? "text-[#F6A661]" : "text-white"}`}>
                          {track.title}
                        </p>
                        <p className="text-sm text-gray-400">{track.artist}</p>
                      </div>
                    </td>
                    <td className="py-4 text-gray-400">{track.plays} likes</td>
                    <td className="py-4 text-right text-gray-400">{track.duration}</td>
                    <td className="py-4 text-right">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDeleteTrack(track.id);
                        }}
                        className="text-red-500 hover:text-red-400 transition-colors p-2"
                        title="Delete track"
                      >
                        <FaTrash className="w-4 h-4" />
                      </button>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Edit Modal */}
      <UploadArtworkModal
        isOpen={showEditModal}
        onClose={() => setShowEditModal(false)}
        onUpload={handleSaveEdit}
        initialData={getEditModalData()}
        isEditMode={true}
      />
    </div>
  );
};

export default ArtistArtworkDetailPage;

