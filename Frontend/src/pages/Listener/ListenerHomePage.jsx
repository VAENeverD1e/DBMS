import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { FaHome } from "react-icons/fa";
import { Sidebar, TopBar, RightSidebar, PlayerBar } from "@components/layout";
import songsService from "@services/songsService";
import artworksService from "@services/artworksService";

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
  const audioRef = useRef(null);
  
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [searchValue, setSearchValue] = useState("");
  const [currentSong, setCurrentSong] = useState(null);
  const [volume, setVolume] = useState(70);
  
  const [popularSongs, setPopularSongs] = useState([]);
  const [rockSongs, setRockSongs] = useState([]);
  const [jazzSongs, setJazzSongs] = useState([]);
  const [electronicSongs, setElectronicSongs] = useState([]);
  const [popularAlbums, setPopularAlbums] = useState([]);
  const [loading, setLoading] = useState(true);

  const mostFollowedArtists = [
    { id: 1, name: "Central C", image: "/ProfilePicArtist.png" },
    { id: 2, name: "Kendrick Lamar", image: "/ArtworkImage2.png" },
    { id: 3, name: "NCT U", image: "/ArtworkImage3.png" },
    { id: 4, name: "BTS", image: "/ArtworkImage4.png" },
    { id: 5, name: "J97", image: "/ArtworkImage5.png" },
  ];

  const genres = [
    { id: 1, name: "Rock", image: "/ArtworkImage5.png" },
    { id: 2, name: "Jazz", image: "/ArtworkImage6.png" },
    { id: 3, name: "Electronic", image: "/ArtworkImage7.png" },
    { id: 4, name: "Pop", image: "/ArtworkImage8.png" },
  ];

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
      console.log('🎵 Fetching songs and albums from API...');
      
      const [popularRes, rockRes, jazzRes, electronicRes, albumRes] = await Promise.all([
        songsService.searchSongs({ query: 'popular', limit: 10 }),
        songsService.getSongsByGenre({ genre: 'rock', limit: 10 }),
        songsService.getSongsByGenre({ genre: 'jazz', limit: 10 }),
        songsService.getSongsByGenre({ genre: 'electronic', limit: 10 }),
        artworksService.searchAlbums({ query: 'popular', limit: 10 }),
      ]);

      console.log('✅ API Responses:', { popularRes, rockRes, jazzRes, electronicRes, albumRes });
      console.log('🔍 Popular Response Structure:', popularRes);
      console.log('🔍 Popular has songs?', popularRes?.songs);
      console.log('🔍 Popular songs length:', popularRes?.songs?.length);

      if (popularRes && popularRes.songs && popularRes.songs.length > 0) {
        console.log('✅ Popular songs:', popularRes.songs.length);
        setPopularSongs(popularRes.songs);
      } else {
        console.log('⚠️ No popular songs found');
      }
      
      if (rockRes && rockRes.songs && rockRes.songs.length > 0) {
        console.log('✅ Rock songs:', rockRes.songs.length);
        setRockSongs(rockRes.songs);
      } else {
        console.log('⚠️ No rock songs found');
      }
      
      if (jazzRes && jazzRes.songs && jazzRes.songs.length > 0) {
        console.log('✅ Jazz songs:', jazzRes.songs.length);
        setJazzSongs(jazzRes.songs);
      } else {
        console.log('⚠️ No jazz songs found');
      }
      
      if (electronicRes && electronicRes.songs && electronicRes.songs.length > 0) {
        console.log('✅ Electronic songs:', electronicRes.songs.length);
        setElectronicSongs(electronicRes.songs);
      } else {
        console.log('⚠️ No electronic songs found');
      }

      if (albumRes && albumRes.albums && albumRes.albums.length > 0) {
        console.log('✅ Popular albums:', albumRes.albums.length);
        setPopularAlbums(albumRes.albums);
      } else {
        console.log('⚠️ No popular albums found');
      }
    } catch (error) {
      console.error('❌ Error fetching songs and albums:', error);
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

          {/* Most Popular Songs */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-white">Popular Tracks</h2>
              <button className="text-[#F6A661] hover:text-[#FFFBEF] underline transition-colors font-semibold">
                Show all
              </button>
            </div>
            {loading ? (
              <div className="text-white text-center py-8">Loading songs...</div>
            ) : (
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
                          className="w-full aspect-square object-cover rounded-xl mb-2"
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
              </div>
            )}
          </div>

          {/* Popular Albums */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-white">Popular Albums</h2>
              <button className="text-[#F6A661] hover:text-[#FFFBEF] underline transition-colors font-semibold">
                Show all
              </button>
            </div>
            {loading ? (
              <div className="text-white text-center py-8">Loading albums...</div>
            ) : (
              <div className="overflow-x-auto scrollbar-hide">
                <div className="flex gap-4 min-w-max pb-2">
                  {popularAlbums.map((album, index) => (
                    <motion.div
                      key={album.jamendo_id}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1, duration: 0.5 }}
                      className="flex-shrink-0 w-64 cursor-pointer hover:scale-105 transition-transform"
                      onClick={() => navigate(`/album/${album.jamendo_id}`)}
                    >
                      <div className="bg-[#2A2820] rounded-2xl p-4">
                        <img
                          src={album.image_url}
                          alt={album.title}
                          className="w-full aspect-square object-cover rounded-xl mb-2"
                          onError={(e) => {
                            // e.target.src = `https://via.placeholder.com/300x300/3E3B2C/F6A661?text=${album.title}`;
                          }}
                        />
                        <p className="text-white text-base font-semibold text-center truncate">
                          {album.title}
                        </p>
                        <p className="text-gray-400 text-sm text-center truncate">
                          {album.artist}
                        </p>
                        <p className="text-gray-500 text-xs text-center mt-1">
                          {album.track_count} tracks
                        </p>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Rock Music */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-white">Rock Music</h2>
              <button className="text-[#F6A661] hover:text-[#FFFBEF] underline transition-colors font-semibold">
                Show all
              </button>
            </div>
            {loading ? (
              <div className="text-white text-center py-8">Loading songs...</div>
            ) : (
              <div className="overflow-x-auto scrollbar-hide">
                <div className="flex gap-4 min-w-max pb-2">
                  {rockSongs.map((song, index) => (
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
                          className="w-full aspect-square object-cover rounded-xl mb-2"
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
              </div>
            )}
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
                          // e.target.src = `https://via.placeholder.com/128x128/3E3B2C/F6A661?text=${artist.name}`;
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

          {/* Jazz Music */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-white">Jazz Music</h2>
              <button className="text-[#F6A661] hover:text-[#FFFBEF] underline transition-colors font-semibold">
                Show all
              </button>
            </div>
            {loading ? (
              <div className="text-white text-center py-8">Loading songs...</div>
            ) : (
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
                          className="w-full aspect-square object-cover rounded-xl mb-2"
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
              </div>
            )}
          </div>

          {/* Electronic Music */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-white">Electronic Music</h2>
              <button className="text-[#F6A661] hover:text-[#FFFBEF] underline transition-colors font-semibold">
                Show all
              </button>
            </div>
            {loading ? (
              <div className="text-white text-center py-8">Loading songs...</div>
            ) : (
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
                          className="w-full aspect-square object-cover rounded-xl mb-2"
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
              </div>
            )}
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
    </div>
  );
};

export default ListenerHomePage;

