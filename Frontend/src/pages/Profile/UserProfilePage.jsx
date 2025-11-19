import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { FaHome, FaPlay, FaArrowLeft, FaCamera } from "react-icons/fa";
import { Sidebar, TopBar, RightSidebar, PlayerBar } from "@components/layout";

/**
 * UserProfilePage Component
 * 
 * Displays user profile information
 * Features:
 * - User profile picture (editable on hover)
 * - Recently Played songs
 * - My Playlist
 * - Favorite Artists
 */
const UserProfilePage = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(102);
  const [duration] = useState(240);
  const [searchValue, setSearchValue] = useState("");
  const [profileImage, setProfileImage] = useState("/ProfilePicArtist.png");
  const [isHoveringProfile, setIsHoveringProfile] = useState(false);

  // Sample data - This will be replaced with API call
  const userData = {
    name: "Nguyễn Trường An",
    image: profileImage,
  };

  // Recently Played - History of 5 nearest songs
  const recentlyPlayed = [
    { id: 1, name: "The Perfect Velvet", artist: "Artist name", image: "/ArtworkImage1.png" },
    { id: 2, name: "Song 2", artist: "Artist name", image: "/ArtworkImage2.png" },
    { id: 3, name: "Song 3", artist: "Artist name", image: "/ArtworkImage3.png" },
    { id: 4, name: "Song 4", artist: "Artist name", image: "/ArtworkImage4.png" },
    { id: 5, name: "Song 5", artist: "Artist name", image: "/ArtworkImage5.png" },
  ];

  // My Playlist
  const myPlaylists = [
    { id: 1, name: "My Liked Song", image: "/ArtworkImage5.png" },
    { id: 2, name: "Playlist 1", image: "/ArtworkImage6.png" },
    { id: 3, name: "Playlist 2", image: "/ArtworkImage7.png" },
    { id: 4, name: "Playlist 3", image: "/ArtworkImage8.png" },
  ];

  // Favorite Artists
  const favoriteArtists = [
    { id: 1, name: "Artist name", image: "/ProfilePicArtist.png" },
    { id: 2, name: "Artist name", image: "/ArtworkImage2.png" },
    { id: 3, name: "Artist name", image: "/ArtworkImage3.png" },
    { id: 4, name: "Artist name", image: "/ArtworkImage4.png" },
  ];

  const relatedArtworks = [
    { id: 1, name: "The ReVe Festival Day...", image: "/ArtworkImage5.png" },
    { id: 2, name: "The ReVe Festival 202...", image: "/ArtworkImage6.png" },
    { id: 3, name: "Artwork 7", image: "/ArtworkImage7.png" },
    { id: 4, name: "Artwork 8", image: "/ArtworkImage8.png" },
  ];

  const currentSong = {
    title: "About Love",
    artist: "Artist name",
    image: "/RightBarImage.png",
  };

  const upcomingSong = {
    title: "Moonlight Melody",
    artist: "Artist name",
    image: "/RightBarImage.png",
  };

  const artistInfo = {
    name: "Artist name",
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

  const handleProfileImageClick = () => {
    fileInputRef.current?.click();
  };

  const handleProfileImageChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setProfileImage(reader.result);
        // Here you would upload to backend
      };
      reader.readAsDataURL(file);
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
          {/* Profile Section */}
          <div className="flex gap-6 mb-8">
            <div
              className="relative flex-shrink-0"
              onMouseEnter={() => setIsHoveringProfile(true)}
              onMouseLeave={() => setIsHoveringProfile(false)}
            >
              <motion.img
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
                src={userData.image}
                alt={userData.name}
                className="w-64 h-64 rounded-full object-cover cursor-pointer"
                onClick={handleProfileImageClick}
                onError={(e) => {
                  e.target.src = `https://via.placeholder.com/256x256/3E3B2C/F6A661?text=${userData.name}`;
                }}
              />
              {/* Overlay on hover */}
              {isHoveringProfile && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="absolute inset-0 bg-black/60 rounded-full flex items-center justify-center cursor-pointer"
                  onClick={handleProfileImageClick}
                >
                  <FaCamera className="w-12 h-12 text-white" />
                </motion.div>
              )}
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleProfileImageChange}
                className="hidden"
              />
            </div>
            <div className="flex-1 flex flex-col justify-end">
              <p className="text-white text-sm mb-2">Profile</p>
              <h1 className="text-6xl font-bold text-white mb-6">{userData.name}</h1>
              <button className="bg-[#F6A661] text-[#3E3B2C] px-8 py-3 rounded-full font-bold hover:bg-[#E5954F] transition-colors flex items-center gap-2 self-start">
                <FaPlay className="w-5 h-5" />
                Play Shuffle
              </button>
            </div>
          </div>

          {/* Recently Played */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-white mb-4">Recently Played</h2>
            <div className="grid grid-cols-4 gap-4">
              {recentlyPlayed.map((item, index) => (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  onClick={() => navigate(`/album/${item.id}`)}
                  className="cursor-pointer hover:scale-105 transition-transform"
                >
                  <div className="bg-[#2A2820] rounded-2xl p-4">
                    <img
                      src={item.image}
                      alt={item.name}
                      className="w-full aspect-square object-cover rounded-xl mb-2"
                      onError={(e) => {
                        e.target.src = `https://via.placeholder.com/300x300/3E3B2C/F6A661?text=${item.name}`;
                      }}
                    />
                    <p className="text-white text-base font-semibold text-center">{item.name}</p>
                    <p className="text-gray-400 text-sm text-center">{item.artist}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* My Playlist */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-white mb-4">My Playlist</h2>
            <div className="grid grid-cols-4 gap-4">
              {myPlaylists.map((playlist, index) => (
                <motion.div
                  key={playlist.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="cursor-pointer hover:scale-105 transition-transform"
                >
                  <div className="bg-[#2A2820] rounded-2xl p-4">
                    <img
                      src={playlist.image}
                      alt={playlist.name}
                      className="w-full aspect-square object-cover rounded-xl mb-2"
                      onError={(e) => {
                        e.target.src = `https://via.placeholder.com/300x300/3E3B2C/F6A661?text=${playlist.name}`;
                      }}
                    />
                    <p className="text-white text-base font-semibold text-center">{playlist.name}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Favorite Artists */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-white mb-4">Favorite Artists</h2>
            <div className="overflow-x-auto scrollbar-hide">
              <div className="flex gap-4 min-w-max pb-2">
                {favoriteArtists.map((artist, index) => (
                  <motion.div
                    key={artist.id}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    onClick={() => navigate(`/artist/${artist.id}`)}
                    className="flex-shrink-0 cursor-pointer hover:scale-105 transition-transform"
                  >
                    <div className="bg-[#2A2820] rounded-2xl p-4 flex flex-col items-center">
                      <img
                        src={artist.image}
                        alt={artist.name}
                        className="w-44 h-44 rounded-full object-cover mb-2"
                        onError={(e) => {
                          e.target.src = `https://via.placeholder.com/176x176/3E3B2C/F6A661?text=${artist.name}`;
                        }}
                      />
                      <p className="text-white text-base font-semibold text-center">{artist.name}</p>
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

export default UserProfilePage;

