import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { FaHome } from "react-icons/fa";
import { Sidebar, TopBar, RightSidebar, PlayerBar } from "@components/layout";
import { AccessModal } from "@components/common";

/**
 * HomePage Component
 * 
 * Main home page for logged-in users (Guest Home Page)
 * Features:
 * - Left Sidebar: Navigation menu
 * - Main Content: Welcome banner, New Songs, Playlists
 * - Right Sidebar: Current song, Artist info, Related artworks
 * - Footer: Music player controls
 */
const HomePage = () => {
  const navigate = useNavigate();
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(102); // 1:42 in seconds
  const [duration] = useState(240); // 4:00 in seconds
  const [showAccessModal, setShowAccessModal] = useState(false);
  const [searchValue, setSearchValue] = useState("");

  // Sample data
  const newSongs = [
    { id: 1, name: "The Perfect Velvet", image: "/ArtworkImage1.png" },
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
    title: "Song name",
    artist: "Artist name",
    image: "/Artwork_cover.png",
  };

  const upcomingSong = {
    title: "Song name",
    artist: "Artist name",
    image: "/ArtworkImage1.png",
  };

  const artistInfo = {
    name: "Red Velvet",
    description:
      "Red Velvet is a South Korean girl group formed by SM Entertainment in 2014. The group is known for its versatile music style and dual concept — the 'Red' side represents bright, energetic pop and dance music, while the 'Velvet' side showcases smooth R&B and soulful sounds. With hits like 'Bad Boy,' 'Red Flavor,' and 'Psycho,' Red Velvet has gained international recognition for their vocal talent, innovative concepts, and diverse discography.",
    image: "/WelcomeTo.png",
    buttonLabel: "Follow",
  };

  const handleLogout = () => {
    navigate("/");
  };

  const handleBecomeMember = () => {
    setShowAccessModal(true);
  };

  const handleSelectAccess = (type) => {
    navigate("/subscription", { state: { selectedType: type } });
  };

  return (
    <div className="flex h-screen bg-[#3E3B2C] overflow-hidden">
      {/* Left Sidebar */}
      <Sidebar userRole="GUEST" onLogout={handleLogout} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col bg-[#3E3B2C] overflow-hidden">
        {/* Top Bar */}
        <TopBar
          leftContent={<FaHome className="w-6 h-6 text-[#F6A661]" />}
          searchValue={searchValue}
          onSearchChange={setSearchValue}
          onProfileClick={() => navigate("/profile")}
        />

        {/* Main Content - Scrollable */}
        <div className="flex-1 overflow-y-auto p-6 scrollbar-hide">
          {/* Welcome Banner */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-8 rounded-2xl overflow-hidden relative"
          >
            <img
              src="/WelcomeTo.png"
              alt="Welcome to Headphones On"
              className="w-full h-64 object-cover"
            />
            <div className="absolute inset-0 bg-black opacity-50 flex items-center justify-center">
              <h2 className="text-white text-4xl font-inter text-center">
                Welcome to Headphones On!
              </h2>
            </div>
          </motion.div>

          {/* New Song Section */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-white mb-4">New Release</h2>
            <div className="grid grid-cols-4 gap-4">
              {newSongs.map((song, index) => (
                <motion.div
                  key={song.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  className="cursor-pointer hover:scale-105 transition-transform"
                >
                  <div className="bg-[#2A2820] rounded-lg p-4">
                    <img
                      src={song.image}
                      alt={song.name}
                      className="w-full aspect-square object-cover rounded-lg mb-2"
                      onError={(e) => {
                        e.target.src = `https://via.placeholder.com/300x300/3E3B2C/F6A661?text=${song.name}`;
                      }}
                    />
                    <p className="text-white text-base font-semibold text-center">
                      {song.name}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* My Playlist Section */}
          <div>
            <h2 className="text-2xl font-bold text-white mb-4">My Playlist</h2>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5, duration: 0.5 }}
              className="bg-[#2A2820] rounded-lg p-8 cursor-pointer hover:bg-[#F6A661] transition-colors"
              onClick={handleBecomeMember}
            >
              <p className="text-white text-lg font-semibold text-center">
                Become a member for fully access!
              </p>
            </motion.div>
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

      {/* Access Modal */}
      <AccessModal
        isOpen={showAccessModal}
        onClose={() => setShowAccessModal(false)}
        onSelect={handleSelectAccess}
      />
    </div>
  );
};

export default HomePage;
