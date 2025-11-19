import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { FaHome } from "react-icons/fa";
import { Sidebar, TopBar, RightSidebar, PlayerBar } from "@components/layout";

/**
 * ListenerHomePage Component
 * 
 * Home page for listeners after subscription
 * Features:
 * - Left Sidebar: Navigation menu
 * - Main Content: Most Popular Albums, New Release, Most Followed Artist, Genre
 * - Right Sidebar: Current song, Artist info, Related artworks
 * - Footer: Music player controls
 */
const ListenerHomePage = () => {
  const navigate = useNavigate();
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(102);
  const [duration] = useState(240);
  const [searchValue, setSearchValue] = useState("");

  // Sample data
  const mostPopularAlbums = [
    { id: 1, name: "The Perfect Velvet", image: "/ArtworkImage1.png" },
    { id: 2, name: "Album 2", image: "/ArtworkImage2.png" },
    { id: 3, name: "Album 3", image: "/ArtworkImage3.png" },
    { id: 4, name: "Album 4", image: "/ArtworkImage4.png" },
    { id: 5, name: "Album 5", image: "/ArtworkImage5.png" },
  ];

  const newReleases = [
    { id: 1, name: "Song 1", image: "/ArtworkImage5.png" },
    { id: 2, name: "Album 1", image: "/ArtworkImage6.png" },
    { id: 3, name: "Song 2", image: "/ArtworkImage7.png" },
    { id: 4, name: "Album 2", image: "/ArtworkImage8.png" },
    { id: 5, name: "Album 5", image: "/ArtworkImage5.png" },
  ];

  const mostFollowedArtists = [
    { id: 1, name: "Central C", image: "/ProfilePicArtist.png" },
    { id: 2, name: "Kendrick Lamar", image: "/ArtworkImage2.png" },
    { id: 3, name: "NCT U", image: "/ArtworkImage3.png" },
    { id: 4, name: "BTS", image: "/ArtworkImage4.png" },
    { id: 5, name: "J97", image: "/ArtworkImage5.png" },
  ];

  const genres = [
    { id: 1, name: "RnB", image: "/ArtworkImage5.png" },
    { id: 2, name: "Rock", image: "/ArtworkImage6.png" },
    { id: 3, name: "Ballad", image: "/ArtworkImage7.png" },
    { id: 4, name: "Folk", image: "/ArtworkImage8.png" },
    { id: 5, name: "Album 5", image: "/ArtworkImage5.png" },
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

  return (
    <div className="flex h-screen bg-[#3E3B2C] overflow-hidden">
      {/* Left Sidebar */}
      <Sidebar userRole="LISTENER" onLogout={handleLogout} />

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

          {/* Most Popular Albums */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-white">Most Popular Albums</h2>
              <button className="text-[#F6A661] hover:text-[#FFFBEF] underline transition-colors font-semibold">
                Show all
              </button>
            </div>
            <div className="overflow-x-auto scrollbar-hide">
              <div className="flex gap-4 min-w-max pb-2">
                {mostPopularAlbums.map((album, index) => (
                  <motion.div
                    key={album.id}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1, duration: 0.5 }}
                    className="flex-shrink-0 w-64 cursor-pointer hover:scale-105 transition-transform"
                    onClick={() => navigate(`/album/${album.id}`)}
                  >
                    <div className="bg-[#2A2820] rounded-2xl p-4">
                      <img
                        src={album.image}
                        alt={album.name}
                        className="w-full aspect-square object-cover rounded-xl mb-2"
                        onError={(e) => {
                          e.target.src = `https://via.placeholder.com/300x300/3E3B2C/F6A661?text=${album.name}`;
                        }}
                      />
                      <p className="text-white text-base font-semibold text-center">
                        {album.name}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>

          {/* New Release */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-white">New Release</h2>
              <button className="text-[#F6A661] hover:text-[#FFFBEF] underline transition-colors font-semibold">
                Show all
              </button>
            </div>
            <div className="overflow-x-auto scrollbar-hide">
              <div className="flex gap-4 min-w-max pb-2">
                {newReleases.map((item, index) => (
                  <motion.div
                    key={item.id}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1, duration: 0.5 }}
                    className="flex-shrink-0 w-64 cursor-pointer hover:scale-105 transition-transform"
                    onClick={() => navigate(`/album/${item.id}`)}
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
                      <p className="text-white text-base font-semibold text-center">
                        {item.name}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>

          {/* Most Followed Artist */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-white">Most Followed Artist</h2>
              <button className="text-[#F6A661] hover:text-[#FFFBEF] underline transition-colors font-semibold">
                Show all
              </button>
            </div>
            <div className="overflow-x-auto scrollbar-hide">
              <div className="flex gap-4 min-w-max pb-2">
                {mostFollowedArtists.map((artist, index) => (
                  <motion.div
                    key={artist.id}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1, duration: 0.5 }}
                    className="flex-shrink-0 cursor-pointer hover:scale-105 transition-transform"
                    onClick={() => navigate(`/artist/${artist.id}`)}
                  >
                    <div className="bg-[#2A2820] rounded-2xl p-4 flex flex-col items-center">
                      <img
                        src={artist.image}
                        alt={artist.name}
                         className="w-44 h-44 rounded-full object-cover mb-2"
                        onError={(e) => {
                          e.target.src = `https://via.placeholder.com/128x128/3E3B2C/F6A661?text=${artist.name}`;
                        }}
                      />
                      <p className="text-white text-base font-semibold text-center">
                        {artist.name}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>

          {/* Genre */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-white">Genre</h2>
              <button className="text-[#F6A661] hover:text-[#FFFBEF] underline transition-colors font-semibold">
                Show all
              </button>
            </div>
            <div className="overflow-x-auto scrollbar-hide">
              <div className="flex gap-4 min-w-max pb-2">
                {genres.map((genre, index) => (
                  <motion.div
                    key={genre.id}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1, duration: 0.5 }}
                    className="flex-shrink-0 w-64 cursor-pointer hover:scale-105 transition-transform"
                    onClick={() => navigate(`/album/${genre.id}`)}
                  >
                    <div className="bg-[#2A2820] rounded-2xl p-4">
                      <img
                        src={genre.image}
                        alt={genre.name}
                        className="w-full aspect-square object-cover rounded-xl mb-2"
                        onError={(e) => {
                          e.target.src = `https://via.placeholder.com/300x300/3E3B2C/F6A661?text=${genre.name}`;
                        }}
                      />
                      <p className="text-white text-base font-semibold text-center">
                        {genre.name}
                      </p>
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

export default ListenerHomePage;

