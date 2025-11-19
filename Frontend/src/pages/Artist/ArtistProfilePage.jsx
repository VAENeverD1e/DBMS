import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { motion } from "framer-motion";
import { FaHome, FaPlay, FaHeart, FaArrowLeft, FaUserCircle } from "react-icons/fa";
import { Sidebar, TopBar, RightSidebar, PlayerBar } from "@components/layout";

/**
 * ArtistProfilePage Component
 * 
 * Displays detailed information about an artist
 * Features:
 * - Artist profile image and metadata
 * - Popular songs list
 * - Discography, Albums, and Songs sections
 * - Follow and Play buttons
 */
const ArtistProfilePage = () => {
  const navigate = useNavigate();
  const { id } = useParams(); // Get artist ID from URL for backend integration
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(102);
  const [duration] = useState(240);
  const [searchValue, setSearchValue] = useState("");
  const [isFollowing, setIsFollowing] = useState(false);
  const [isLiked, setIsLiked] = useState(false);
  const [currentSongId, setCurrentSongId] = useState(null);

  // Sample data - This will be replaced with API call using the id parameter
  const artistData = {
    id: id || 1,
    name: "Artist name",
    followers: 1000,
    reactions: 15000,
    image: "/ProfilePicArtist.png",
  };

  // Popular songs - This will be fetched from backend
  const popularSongs = [
    { id: 1, number: 1, title: "Song name", image: "/ArtworkImage1.png", likes: 3000, duration: "3:09" },
    { id: 2, number: 2, title: "Song name", image: "/ArtworkImage1.png", likes: 3000, duration: "3:09" },
    { id: 3, number: 3, title: "Song name", image: "/ArtworkImage1.png", likes: 3000, duration: "3:09" },
    { id: 4, number: 4, title: "Song name", image: "/ArtworkImage1.png", likes: 3000, duration: "3:09" },
    { id: 5, number: 5, title: "Song name", image: "/ArtworkImage1.png", likes: 3000, duration: "3:09" },
  ];

  // Discography - New Release
  const discography = [
    { id: 1, name: "Artwork 1", image: "/ArtworkImage1.png" },
    { id: 2, name: "Artwork 2", image: "/ArtworkImage2.png" },
    { id: 3, name: "Artwork 3", image: "/ArtworkImage3.png" },
    { id: 4, name: "Artwork 4", image: "/ArtworkImage4.png" },
  ];

  // Albums
  const albums = [
    { id: 1, name: "Album 1", image: "/ArtworkImage5.png" },
    { id: 2, name: "Album 2", image: "/ArtworkImage6.png" },
    { id: 3, name: "Album 3", image: "/ArtworkImage7.png" },
    { id: 4, name: "Album 4", image: "/ArtworkImage8.png" },
  ];

  // Songs
  const songs = [
    { id: 1, name: "Song 1", image: "/ArtworkImage1.png" },
    { id: 2, name: "Song 2", image: "/ArtworkImage2.png" },
    { id: 3, name: "Song 3", image: "/ArtworkImage3.png" },
    { id: 4, name: "Song 4", image: "/ArtworkImage4.png" },
  ];

  const relatedArtworks = [
    { id: 1, name: "The ReVe Festival Day...", image: "/ArtworkImage5.png" },
    { id: 2, name: "The ReVe Festival 202...", image: "/ArtworkImage6.png" },
    { id: 3, name: "Artwork 7", image: "/ArtworkImage7.png" },
    { id: 4, name: "Artwork 8", image: "/ArtworkImage8.png" },
  ];

  const currentSong = {
    title: "About Love",
    artist: artistData.name,
    image: "/RightBarImage.png",
  };

  const upcomingSong = {
    title: "Moonlight Melody",
    artist: artistData.name,
    image: "/RightBarImage.png",
  };

  const artistInfo = {
    name: artistData.name,
    description:
      "Artist description will be fetched from backend. This is a placeholder text for the artist information that will be displayed in the right sidebar.",
    image: "/WelcomeTo.png",
    buttonLabel: "Follow",
  };

  const handleLogout = () => {
    navigate("/");
  };

  const handleBack = () => {
    navigate(-1);
  };

  const handleSongClick = (songId) => {
    setCurrentSongId(songId);
    setIsPlaying(true);
  };

  const handleItemClick = (itemId, type) => {
    if (type === "album" || type === "artwork") {
      navigate(`/album/${itemId}`);
    } else if (type === "song") {
      handleSongClick(itemId);
    }
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
          {/* Artist Header */}
          <div className="flex gap-6 mb-8">
            <motion.img
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
              src={artistData.image}
              alt={artistData.name}
              className="w-64 h-64 rounded-full object-cover flex-shrink-0"
              onError={(e) => {
                e.target.src = `https://via.placeholder.com/256x256/3E3B2C/F6A661?text=${artistData.name}`;
              }}
            />
            <div className="flex-1 flex flex-col justify-end">
              <h1 className="text-6xl font-bold text-white mb-4">{artistData.name}</h1>
              <div className="flex items-center gap-6 mb-6">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-[#F6A661] rounded-full"></div>
                  <span className="text-white">{artistData.followers} Followers</span>
                </div>
                <div className="flex items-center gap-2">
                  <FaHeart className="w-4 h-4 text-red-500" />
                  <span className="text-white">{artistData.reactions.toLocaleString()} Reactions</span>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <button className="bg-[#F6A661] text-[#3E3B2C] px-8 py-3 rounded-full font-bold hover:bg-[#E5954F] transition-colors flex items-center gap-2">
                  <FaPlay className="w-5 h-5" />
                  Play
                </button>
                <button
                  onClick={() => setIsFollowing(!isFollowing)}
                  className={`px-8 py-3 rounded-full font-bold transition-colors flex items-center gap-2 ${
                    isFollowing
                      ? "bg-[#2A2820] border-2 border-[#F6A661] text-[#F6A661]"
                      : "bg-[#2A2820] border-2 border-[#F6A661] text-[#F6A661] hover:bg-[#F6A661] hover:text-[#3E3B2C]"
                  }`}
                >
                  Follow
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

          {/* Popular Songs */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-white mb-4">Popular Songs</h2>
            <div className="bg-[#2A2820] rounded-2xl p-6">
              {popularSongs.map((song, index) => (
                <motion.div
                  key={song.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  onClick={() => handleSongClick(song.id)}
                  className={`flex items-center gap-4 p-4 rounded-xl cursor-pointer hover:bg-[#3E3B2C]/50 transition-colors mb-2 ${
                    currentSongId === song.id ? "bg-[#F6A661]/20" : ""
                  }`}
                >
                  <span className={`text-lg font-bold w-8 ${currentSongId === song.id ? "text-[#F6A661]" : "text-gray-400"}`}>
                    {song.number}
                  </span>
                  <img
                    src={song.image}
                    alt={song.title}
                    className="w-16 h-16 rounded-xl object-cover"
                    onError={(e) => {
                      e.target.src = `https://via.placeholder.com/64x64/3E3B2C/F6A661?text=${song.title}`;
                    }}
                  />
                  <div className="flex-1">
                    <p className={`font-semibold ${currentSongId === song.id ? "text-[#F6A661]" : "text-white"}`}>
                      {song.title}
                    </p>
                  </div>
                  <span className="text-gray-400">{song.likes} likes</span>
                  <span className="text-gray-400">{song.duration}</span>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Discography */}
          <div className="mb-8">
          <h2 className="text-2xl font-bold text-white mb-4">Discography</h2>
            <div className="flex items-center gap-4 mb-4">
              <span className="bg-[#F6A661] text-[#3E3B2C] px-4 py-1 rounded-full font-bold text-lg">
                New Release
              </span>
            </div>
            <div className="overflow-x-auto scrollbar-hide">
              <div className="flex gap-4 min-w-max pb-2">
                {discography.map((item, index) => (
                  <motion.div
                    key={item.id}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    onClick={() => handleItemClick(item.id, "artwork")}
                    className="flex-shrink-0 w-64 cursor-pointer hover:scale-105 transition-transform"
                  >
                    <div className="bg-[#2A2820] rounded-2xl p-4">
                      <img
                        src={item.image}
                        alt={item.name}
                        className="w-full aspect-square object-cover rounded-xl mb-2"
                        onError={(e) => {
                          e.target.src = `https://via.placeholder.com/300x300/3E3B2C/F6A661?text=Cover+Image`;
                        }}
                      />
                      <p className="text-white text-base font-semibold text-center">{item.name}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>

          {/* Albums */}
          <div className="mb-8">
            <div className="flex items-center gap-4 mb-4">
              <span className="bg-[#F6A661] text-[#3E3B2C] px-4 py-1 rounded-full font-bold text-lg">
                Albums
              </span>
            </div>
            <div className="overflow-x-auto scrollbar-hide">
              <div className="flex gap-4 min-w-max pb-2">
                {albums.map((album, index) => (
                  <motion.div
                    key={album.id}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    onClick={() => handleItemClick(album.id, "album")}
                    className="flex-shrink-0 w-64 cursor-pointer hover:scale-105 transition-transform"
                  >
                    <div className="bg-[#2A2820] rounded-2xl p-4">
                      <img
                        src={album.image}
                        alt={album.name}
                        className="w-full aspect-square object-cover rounded-xl mb-2"
                        onError={(e) => {
                          e.target.src = `https://via.placeholder.com/300x300/3E3B2C/F6A661?text=Cover+Image`;
                        }}
                      />
                      <p className="text-white text-base font-semibold text-center">{album.name}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>

          {/* Songs */}
          <div className="mb-8">
            <div className="flex items-center gap-4 mb-4">
              <span className="bg-[#F6A661] text-[#3E3B2C] px-4 py-1 rounded-full font-bold text-lg">
                Songs
              </span>
            </div>
            <div className="overflow-x-auto scrollbar-hide">
              <div className="flex gap-4 min-w-max pb-2">
                {songs.map((song, index) => (
                  <motion.div
                    key={song.id}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    onClick={() => handleItemClick(song.id, "song")}
                    className="flex-shrink-0 w-64 cursor-pointer hover:scale-105 transition-transform"
                  >
                    <div className="bg-[#2A2820] rounded-2xl p-4">
                      <img
                        src={song.image}
                        alt={song.name}
                        className="w-full aspect-square object-cover rounded-xl mb-2"
                        onError={(e) => {
                          e.target.src = `https://via.placeholder.com/300x300/3E3B2C/F6A661?text=Cover+Image`;
                        }}
                      />
                      <p className="text-white text-base font-semibold text-center">{song.name}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
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

export default ArtistProfilePage;

