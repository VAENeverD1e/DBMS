import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { motion } from "framer-motion";
import { FaHome, FaPlay, FaHeart, FaArrowLeft } from "react-icons/fa";
import { Sidebar, TopBar, RightSidebar, PlayerBar } from "@components/layout";

/**
 * AlbumDetailPage Component
 * 
 * Displays detailed information about an album/artwork
 * Features:
 * - Album cover and metadata
 * - Tracklist with play controls
 * - Play and Add to playlist buttons
 * - Like functionality
 */
const AlbumDetailPage = () => {
  const navigate = useNavigate();
  const { id } = useParams(); // Get album ID from URL for backend integration
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(102);
  const [duration] = useState(240);
  const [searchValue, setSearchValue] = useState("");
  const [currentTrackId, setCurrentTrackId] = useState(8); // Currently playing track
  const [isLiked, setIsLiked] = useState(false);

  // Sample data - This will be replaced with API call using the id parameter
  const albumData = {
    id: id || 1,
    title: "The Perfect Velvet",
    artist: "Artist name",
    year: 2017,
    image: "/ProfilePicArtist.png",
    songCount: 9,
    duration: "31 min",
  };

  // Tracklist data - This will be fetched from backend using album id
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

  const relatedArtworks = [
    { id: 1, name: "The ReVe Festival Day...", image: "/ArtworkImage5.png" },
    { id: 2, name: "The ReVe Festival 202...", image: "/ArtworkImage6.png" },
    { id: 3, name: "Artwork 7", image: "/ArtworkImage7.png" },
    { id: 4, name: "Artwork 8", image: "/ArtworkImage8.png" },
  ];

  const currentSong = {
    title: tracks.find(t => t.id === currentTrackId)?.title || "Song name",
    artist: albumData.artist,
    image: albumData.image,
  };

  const upcomingSong = {
    title: "Moonlight Melody",
    artist: albumData.artist,
    image: albumData.image,
  };

  const artistInfo = {
    name: albumData.artist,
    description:
      "Artist description will be fetched from backend. This is a placeholder text for the artist information that will be displayed in the right sidebar.",
    image: "/WelcomeTo.png",
    buttonLabel: "Follow",
  };

  const handleLogout = () => {
    navigate("/");
  };

  const handleBack = () => {
    navigate(-1); // Go back to previous page
  };

  const handleTrackClick = (trackId) => {
    setCurrentTrackId(trackId);
    setIsPlaying(true);
  };

  const topBarLeftContent = (
    <div className="flex items-center gap-4">
      <button
        onClick={handleBack}
        className="bg-[#F6A661] text-[#3E3B2C] px-4 py-2 rounded-full font-bold hover:bg-[#E5954F] transition-colors flex items-center gap-2"
      >
        <FaArrowLeft className="w-4 h-4" />
        Back
      </button>
      <FaHome className="w-6 h-6 text-[#F6A661]" />
    </div>
  );

  return (
    <div className="flex h-screen bg-[#3E3B2C] overflow-hidden">
      {/* Left Sidebar */}
      <Sidebar userRole="LISTENER" onLogout={handleLogout} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col bg-[#3E3B2C] overflow-hidden">
        {/* Top Bar */}
        <TopBar
          leftContent={topBarLeftContent}
          searchValue={searchValue}
          onSearchChange={setSearchValue}
          onProfileClick={() => navigate("/profile")}
        />

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
                <button className="bg-transparent border-2 border-[#F6A661] text-[#F6A661] px-8 py-2 rounded-full font-bold hover:bg-[#F6A661] hover:text-[#3E3B2C] transition-colors">
                  Add to my playlist
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
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Footer Player Bar */}
        <PlayerBar
          isPlaying={isPlaying}
          onTogglePlay={() => setIsPlaying(!isPlaying)}
          currentTime={currentTime}
          duration={duration}
          trackTitle={currentSong.title}
          trackArtist={currentSong.artist}
          trackImage={currentSong.image}
        />
      </div>

      {/* Right Sidebar */}
      <RightSidebar
        currentSong={currentSong}
        upcomingSong={upcomingSong}
        artistInfo={artistInfo}
        relatedArtworks={relatedArtworks}
      />
    </div>
  );
};

export default AlbumDetailPage;

