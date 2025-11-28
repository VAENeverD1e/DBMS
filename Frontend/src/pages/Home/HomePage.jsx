import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { FaHome } from "react-icons/fa";
import { Sidebar, TopBar, RightSidebar, PlayerBar } from "@components/layout";
import { AccessModal } from "@components/common";
import songsService from "@services/songsService";

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
  const audioRef = useRef(null);
  
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [showAccessModal, setShowAccessModal] = useState(false);
  const [searchValue, setSearchValue] = useState("");
  const [currentSong, setCurrentSong] = useState(null);
  const [volume, setVolume] = useState(70);
  const [newSongs, setNewSongs] = useState([]);
  const [popularSongs, setPopularSongs] = useState([]);
  const [kpopSongs, setKpopSongs] = useState([]);
  const [jazzSongs, setJazzSongs] = useState([]);
  const [electronicSongs, setElectronicSongs] = useState([]);
  const [loading, setLoading] = useState(true);

  const relatedArtworks = [
    { id: 1, name: "The ReVe Festival Day...", image: "/ArtworkImage5.png" },
    { id: 2, name: "The ReVe Festival 202...", image: "/ArtworkImage6.png" },
    { id: 3, name: "Artwork 7", image: "/ArtworkImage7.png" },
    { id: 4, name: "Artwork 8", image: "/ArtworkImage8.png" },
  ];

  const upcomingSong = {
    title: "Song name",
    artist: "Artist name",
    image: "/ArtworkImage1.png",
  };

  const artistInfo = {
    name: currentSong ? currentSong.artist : "Artist",
    description:
      "Discover amazing music from independent artists around the world. All tracks are licensed under Creative Commons, supporting free culture and artistic expression.",
    image: currentSong ? currentSong.image_url : "/WelcomeTo.png",
    buttonLabel: "Follow",
  };

  useEffect(() => {
    fetchSongs();
  }, []);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const updateTime = () => setCurrentTime(Math.floor(audio.currentTime));
    const updateDuration = () => setDuration(Math.floor(audio.duration));
    const handleEnded = () => setIsPlaying(false);

    audio.addEventListener('timeupdate', updateTime);
    audio.addEventListener('loadedmetadata', updateDuration);
    audio.addEventListener('ended', handleEnded);

    return () => {
      audio.removeEventListener('timeupdate', updateTime);
      audio.removeEventListener('loadedmetadata', updateDuration);
      audio.removeEventListener('ended', handleEnded);
    };
  }, []);

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = volume / 100;
    }
  }, [volume]);

  const fetchSongs = async () => {
    try {
      setLoading(true);
      console.log('🎵 Fetching songs from both database and Jamendo...');

      // Fetch songs from multiple sources in parallel
      const [
        newSongsRes,
        popularRes,
        kpopRes,
        jazzRes,
        electronicRes,
      ] = await Promise.all([
        // New release songs
        songsService.searchSongs({ query: 'new', limit: 8, source: 'both' }),
        // Popular songs
        songsService.searchSongs({ query: 'popular', limit: 10, source: 'both' }),
        // Genre-specific songs
        songsService.getSongsByGenre({ genre: 'K-Pop', limit: 10, source: 'both' }),
        songsService.getSongsByGenre({ genre: 'jazz', limit: 10, source: 'both' }),
        songsService.getSongsByGenre({ genre: 'electronic', limit: 10, source: 'both' }),
      ]);

      console.log('✅ API Responses:', { newSongsRes, popularRes, kpopRes, jazzRes, electronicRes });

      // Helper function to set songs
      const setSongs = (res, setter, name) => {
        if (res?.songs?.length > 0) {
          console.log(`✅ ${name} songs:`, res.songs.length);
          setter(res.songs);
        } else {
          console.log(`⚠️ No ${name} songs found`);
          setter([]);
        }
      };

      // Set all song categories
      setSongs(newSongsRes, setNewSongs, 'New release');
      setSongs(popularRes, setPopularSongs, 'Popular');
      setSongs(kpopRes, setKpopSongs, 'K-Pop');
      setSongs(jazzRes, setJazzSongs, 'Jazz');
      setSongs(electronicRes, setElectronicSongs, 'Electronic');

    } catch (error) {
      console.error('❌ Error fetching songs:', error);
      console.error('Error details:', error.message);
    } finally {
      setLoading(false);
    }
  };

  const playSong = (song) => {
    if (currentSong?.jamendo_id === song.jamendo_id && isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      setCurrentSong(song);
      if (audioRef.current) {
        audioRef.current.src = song.audio_url;
        audioRef.current.play();
        setIsPlaying(true);
      }
    }
  };

  const togglePlay = () => {
    if (!audioRef.current || !currentSong) return;
    
    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setIsPlaying(!isPlaying);
  };

  const handleSeek = (newTime) => {
    if (audioRef.current) {
      audioRef.current.currentTime = newTime;
      setCurrentTime(newTime);
    }
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
            {loading ? (
              <div className="text-white text-center py-8">Loading songs...</div>
            ) : (
              <div className="grid grid-cols-4 gap-4">
                {newSongs.map((song, index) => (
                  <motion.div
                    key={song.jamendo_id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1, duration: 0.5 }}
                    className="cursor-pointer hover:scale-105 transition-transform"
                    onClick={() => playSong(song)}
                  >
                    <div className={`bg-[#2A2820] rounded-lg p-4 ${
                      currentSong?.jamendo_id === song.jamendo_id ? 'ring-2 ring-[#F6A661]' : ''
                    }`}>
                      <img
                        src={song.image_url}
                        alt={song.title}
                        className="w-full aspect-square object-cover rounded-lg mb-2"
                        onError={(e) => {
                          // e.target.src = `https://via.placeholder.com/300x300/3E3B2C/F6A661?text=${song.title}`;
                        }}
                      />
                      <p className="text-white text-base font-semibold text-center truncate">
                        {song.title}
                      </p>
                      <p className="text-gray-400 text-sm text-center truncate">
                        {song.artist}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </div>
            )}
          </div>

          {/* Popular Songs Section */}
          {popularSongs.length > 0 && (
            <div className="mb-8">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold text-white">Popular Songs</h2>
              </div>
              <div className="overflow-x-auto scrollbar-hide">
                <div className="flex gap-4 min-w-max pb-2">
                  {popularSongs.map((song, index) => (
                    <motion.div
                      key={song.jamendo_id}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1, duration: 0.5 }}
                      className="flex-shrink-0 w-64 cursor-pointer hover:scale-105 transition-transform"
                      onClick={() => playSong(song)}
                    >
                      <div className={`bg-[#2A2820] rounded-2xl p-4 ${
                        currentSong?.jamendo_id === song.jamendo_id ? 'ring-2 ring-[#F6A661]' : ''
                      }`}>
                        <img
                          src={song.image_url}
                          alt={song.title}
                          className="w-full aspect-square object-cover rounded-xl mb-3"
                        />
                        <p className="text-white text-base font-semibold truncate">
                          {song.title}
                        </p>
                        <p className="text-gray-400 text-sm truncate">
                          {song.artist}
                        </p>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* K-Pop Section */}
          {kpopSongs.length > 0 && (
            <div className="mb-8">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold text-white">K-Pop</h2>
              </div>
              <div className="overflow-x-auto scrollbar-hide">
                <div className="flex gap-4 min-w-max pb-2">
                  {kpopSongs.map((song, index) => (
                    <motion.div
                      key={song.jamendo_id}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1, duration: 0.5 }}
                      className="flex-shrink-0 w-64 cursor-pointer hover:scale-105 transition-transform"
                      onClick={() => playSong(song)}
                    >
                      <div className={`bg-[#2A2820] rounded-2xl p-4 ${
                        currentSong?.jamendo_id === song.jamendo_id ? 'ring-2 ring-[#F6A661]' : ''
                      }`}>
                        <img
                          src={song.image_url}
                          alt={song.title}
                          className="w-full aspect-square object-cover rounded-xl mb-3"
                        />
                        <p className="text-white text-base font-semibold truncate">
                          {song.title}
                        </p>
                        <p className="text-gray-400 text-sm truncate">
                          {song.artist}
                        </p>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Jazz Section */}
          {jazzSongs.length > 0 && (
            <div className="mb-8">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold text-white">Jazz</h2>
              </div>
              <div className="overflow-x-auto scrollbar-hide">
                <div className="flex gap-4 min-w-max pb-2">
                  {jazzSongs.map((song, index) => (
                    <motion.div
                      key={song.jamendo_id}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1, duration: 0.5 }}
                      className="flex-shrink-0 w-64 cursor-pointer hover:scale-105 transition-transform"
                      onClick={() => playSong(song)}
                    >
                      <div className={`bg-[#2A2820] rounded-2xl p-4 ${
                        currentSong?.jamendo_id === song.jamendo_id ? 'ring-2 ring-[#F6A661]' : ''
                      }`}>
                        <img
                          src={song.image_url}
                          alt={song.title}
                          className="w-full aspect-square object-cover rounded-xl mb-3"
                        />
                        <p className="text-white text-base font-semibold truncate">
                          {song.title}
                        </p>
                        <p className="text-gray-400 text-sm truncate">
                          {song.artist}
                        </p>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Electronic Section */}
          {electronicSongs.length > 0 && (
            <div className="mb-8">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold text-white">Electronic</h2>
              </div>
              <div className="overflow-x-auto scrollbar-hide">
                <div className="flex gap-4 min-w-max pb-2">
                  {electronicSongs.map((song, index) => (
                    <motion.div
                      key={song.jamendo_id}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1, duration: 0.5 }}
                      className="flex-shrink-0 w-64 cursor-pointer hover:scale-105 transition-transform"
                      onClick={() => playSong(song)}
                    >
                      <div className={`bg-[#2A2820] rounded-2xl p-4 ${
                        currentSong?.jamendo_id === song.jamendo_id ? 'ring-2 ring-[#F6A661]' : ''
                      }`}>
                        <img
                          src={song.image_url}
                          alt={song.title}
                          className="w-full aspect-square object-cover rounded-xl mb-3"
                        />
                        <p className="text-white text-base font-semibold truncate">
                          {song.title}
                        </p>
                        <p className="text-gray-400 text-sm truncate">
                          {song.artist}
                        </p>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </div>
          )}

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
          onTogglePlay={togglePlay}
          currentTime={currentTime}
          duration={duration}
          onSeek={handleSeek}
          trackTitle={currentSong ? currentSong.title : "Select a song"}
          trackArtist={currentSong ? currentSong.artist : "No artist"}
          trackImage={currentSong ? currentSong.image_url : null}
          volume={volume}
          onVolumeChange={setVolume}
        />
        
        {/* Hidden Audio Element */}
        <audio ref={audioRef} />
      </div>

      {/* Right Sidebar */}
      <RightSidebar
        currentSong={currentSong ? {
          title: currentSong.title,
          artist: currentSong.artist,
          image: currentSong.image_url
        } : {
          title: "No song playing",
          artist: "Select a song to play",
          image: "/Artwork_cover.png"
        }}
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
