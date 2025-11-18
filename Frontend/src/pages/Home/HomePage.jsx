import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { 
  FaHome,
  FaBell,
  FaSearch,
  FaSignOutAlt,
  FaPlay,
  FaPause,
  FaStepBackward,
  FaStepForward,
  FaRandom,
  FaRedo,
  FaVolumeUp,
  FaList,
  FaFileAlt
} from "react-icons/fa";

/**
 * HomePage Component
 * 
 * This is the main home page for logged-in users (Guest Home Page)
 * Features:
 * - Left Sidebar: Navigation menu
 * - Main Content: Welcome banner, New Songs, Playlists
 * - Right Sidebar: Current song, Artist info, Related artworks
 * - Footer: Music player controls
 * 
 * Background color: #3E3B2C (dark olive green)
 * Accent color: #F6A661 (orange)
 */
const HomePage = () => {
  const navigate = useNavigate();
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(102); // 1:42 in seconds
  const [duration] = useState(240); // 4:00 in seconds

  // Sample data for songs and playlists
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

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleLogout = () => {
    navigate('/');
  };

  return (
    <div className="flex h-screen bg-[#3E3B2C] overflow-hidden">
      {/* Left Sidebar */}
      <div className="w-64 bg-black rounded-xl flex flex-col p-6">
        {/* Logo Section */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
              <img 
                src="/Logo.png"
                alt="Logo" 
                className="w-18 h-18 rounded-full object-cover"
              />
            <div>
              <h1 className="font-karantina text-3xl text-[#F6A661]">HEADPHONES ON</h1>
              <p className="text-2xl font-karantina font-thin text-[#F6A661]">GUEST</p>
            </div>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="flex flex-col gap-4">
          <Link
            to="/home"
            className="flex items-center gap-3 text-[#F6A661] text-xl font-bold hover:text-[#FFFBEF] transition-colors"
          >
            <FaHome className="w-6 h-6" />
            <span>Home</span>
          </Link>
          <Link
            to="/subscription"
            className="flex items-center gap-3 text-[#F6A661] text-xl font-bold hover:text-[#FFFBEF] transition-colors"
          >
            <span>Subscription</span>
          </Link>
          <Link
            to="/support"
            className="flex items-center gap-3 text-[#F6A661] text-xl font-bold hover:text-[#FFFBEF] transition-colors"
          >
            <span>Support</span>
          </Link>
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 text-[#F6A661] text-xl font-bold hover:text-[#FFFBEF] transition-colors"
          >
            <FaSignOutAlt className="w-6 h-6" />
            <span>Log out</span>
          </button>
        </nav>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col bg-[#3E3B2C] overflow-hidden">
        {/* Top Bar */}
        <div className="flex items-center justify-between p-6 border-b border-[#3E3B2C]">
          <FaHome className="w-6 h-6 text-[#F6A661] mr-4" />
          <div className="flex-1 max-w-2xl ml-4">
            <div className="relative">
              <FaSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="What do you want to play today?"
                className="w-full bg-[#2A2820] text-white rounded-full px-10 py-3 focus:outline-none focus:ring-2 focus:ring-[#F6A661]"
              />
            </div>
          </div>
          <div className="flex items-center gap-4">
            <FaBell className="w-6 h-6 text-[#F6A661] cursor-pointer" />
            <div className="w-10 h-10 rounded-full bg-blue-500 cursor-pointer"></div>
          </div>
        </div>

        {/* Main Content - Scrollable */}
        <div className="flex-1 overflow-y-auto p-6 scrollbar-hide">
          {/* Welcome Banner */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            // Đã thêm 'relative' để định vị lớp phủ và văn bản
            // Đã đổi rounded-lg thành rounded-2xl để bo tròn nhiều hơn
            className="mb-8 rounded-2xl overflow-hidden relative" 
          >
            {/* Ảnh nền */}
            <img
              src="/WelcomeTo.png"
              alt="Welcome to Headphones On"
              className="w-full h-64 object-cover"
            />
            
            {/* Lớp phủ màu đen bán trong suốt */}
            <div className="absolute inset-0 bg-black opacity-50 flex items-center justify-center">
              {/* Dòng chữ "Welcome to Headphones On!" */}
              <h2 className="text-white text-4xl font-inter text-center font-inter">
                Welcome to Headphones On!
              </h2>
            </div>
          </motion.div>

          {/* New Song Section */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-white mb-4">New Song</h2>
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
                    <p className="text-white text-sm font-semibold text-center">{song.name}</p>
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
              className="bg-gray-600 rounded-lg p-8 cursor-pointer hover:bg-gray-500 transition-colors"
            >
              <p className="text-white text-lg font-semibold text-center">
                Create a new playlist
              </p>
            </motion.div>
          </div>
        </div>

        {/* Footer Player Bar */}
        <div className="border-t border-[#2A2820] bg-[#2A2820] p-4">
          <div className="flex items-center justify-between">
            {/* Left: Current Song Info */}
            <div className="flex items-center gap-4 flex-1">
              <div className="w-14 h-14 bg-[#F6A661] rounded"></div>
              <div>
                <p className="text-white font-semibold">Song name</p>
                <p className="text-gray-400 text-sm">Artist Name</p>
              </div>
            </div>

            {/* Center: Playback Controls */}
            <div className="flex flex-col items-center gap-2 flex-1">
              <div className="flex items-center gap-4">
                <FaRandom className="w-5 h-5 text-gray-400 cursor-pointer hover:text-[#F6A661]" />
                <FaStepBackward className="w-5 h-5 text-gray-400 cursor-pointer hover:text-[#F6A661]" />
                <button
                  onClick={() => setIsPlaying(!isPlaying)}
                  className="w-10 h-10 rounded-full bg-[#F6A661] flex items-center justify-center hover:bg-[#E5954F] transition-colors"
                >
                  {isPlaying ? (
                    <FaPause className="w-5 h-5 text-white" />
                  ) : (
                    <FaPlay className="w-5 h-5 text-white ml-1" />
                  )}
                </button>
                <FaStepForward className="w-5 h-5 text-gray-400 cursor-pointer hover:text-[#F6A661]" />
                <FaRedo className="w-5 h-5 text-gray-400 cursor-pointer hover:text-[#F6A661]" />
              </div>
              <div className="flex items-center gap-2 w-full max-w-md">
                <span className="text-xs text-gray-400">{formatTime(currentTime)}</span>
                <div className="flex-1 h-1 bg-gray-600 rounded-full relative">
                  <div
                    className="h-full bg-[#F6A661] rounded-full"
                    style={{ width: `${(currentTime / duration) * 100}%` }}
                  ></div>
                </div>
                <span className="text-xs text-gray-400">{formatTime(duration)}</span>
              </div>
            </div>

            {/* Right: Additional Controls (only visible in main area) */}
            <div className="flex items-center gap-4 flex-1 justify-end">
              <FaFileAlt className="w-5 h-5 text-gray-400 cursor-pointer hover:text-[#F6A661]" />
              <FaList className="w-5 h-5 text-gray-400 cursor-pointer hover:text-[#F6A661]" />
              <div className="flex items-center gap-2">
                <FaVolumeUp className="w-5 h-5 text-gray-400 cursor-pointer hover:text-[#F6A661]" />
                <div className="w-24 h-1 bg-gray-600 rounded-full">
                  <div className="h-full bg-[#F6A661] rounded-full" style={{ width: '70%' }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Sidebar */}
      <div className="w-90 bg-black rounded-xl border-l-4 flex flex-col overflow-hidden">
        {/* Current Song Album Art */}
        <div className="p-6">
          <img
            src="/Artwork_cover.png"
            alt="Current Song"
            className="w-full aspect-square rounded-lg mb-4 object-cover"
            onError={(e) => {
              e.target.src = 'https://via.placeholder.com/300x300/F6A661/3E3B2C?text=Artwork+cover';
            }}
          />
          <div className="mb-2">
            <p className="text-white text-xl font-bold">Song name</p>
            <p className="text-gray-400 text-sm">Artist name</p>
          </div>
        </div>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto px-6 pb-6 scrollbar-hide">
          {/* Upcoming Song */}
          <div className="mb-6">
            <h3 className="text-white font-bold mb-3">Upcoming Song:</h3>
            <div className="flex items-center gap-3 bg-[#F6A661] rounded-lg p-2">
              <img
                src="/ArtworkImage1.png"
                alt="Upcoming"
                className="w-10 h-10 rounded object-cover"
                onError={(e) => {
                  e.target.src = 'https://via.placeholder.com/64x64/3E3B2C/F6A661?text=Upcoming';
                }}
              />
              <div className="flex-1">
                <p className="text-white text-sm font-semibold">Song name</p>
                <p className="text-gray-300 text-xs">Artist name</p>
              </div>
            </div>
          </div>

          {/* About Artist */}
          <div className="mb-6 rounded-lg border-t-2 border-b-2 border-[#F6A661] bg-[#2A2820] p-4">
            <h3 className="text-white font-bold mb-3">About Artist:</h3>
            <img
              src="/WelcomeTo.png"
              alt="Artist"
              className="w-full h-32 object-cover rounded-lg mb-3"
              onError={(e) => {
                e.target.src = 'https://via.placeholder.com/300x128/3E3B2C/F6A661?text=Artist';
              }}
            />
            {/* Orange background section for artist name and description */}
            <div className="bg-[#F6A661] rounded-lg p-4">
              <div className="flex items-center justify-between mb-4">
                <h4 className="text-#3E3B2C text-2xl font-bold">Red Velvet</h4>
                <button className="bg-white border-2 border-black text-black px-4 py-0.5 rounded-full text-sm font-bold hover:bg-gray-100 transition-colors">
                  Follow
                </button>
              </div>
              <p className="text-[#3F3C35] text-xs leading-relaxed">
                Red Velvet is a South Korean girl group formed by SM Entertainment in 2014. 
                The group is known for its versatile music style and dual concept — the 'Red' 
                side represents bright, energetic pop and dance music, while the 'Velvet' side 
                showcases smooth R&B and soulful sounds. With hits like 'Bad Boy,' 'Red Flavor,' 
                and 'Psycho,' Red Velvet has gained international recognition for their vocal 
                talent, innovative concepts, and diverse discography.
              </p>
            </div>
          </div>

          {/* Related Artworks */}
          <div>
            <h3 className="text-white font-semibold mb-3">Related Artworks:</h3>
            <div className="space-y-3">
              {relatedArtworks.map((artwork) => (
                <div key={artwork.id} className="bg-[#2A2820] rounded-lg p-3">
                  <img
                    src={artwork.image}
                    alt={artwork.name}
                    className="w-full aspect-square object-cover rounded-lg mb-2"
                    onError={(e) => {
                      e.target.src = `https://via.placeholder.com/300x300/3E3B2C/F6A661?text=${artwork.name}`;
                    }}
                  />
                  <p className="text-white text-sm font-semibold text-center">{artwork.name}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;

