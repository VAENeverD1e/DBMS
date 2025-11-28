import React, { useState, useEffect, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { motion } from "framer-motion";
import { FaHome, FaPlay, FaHeart, FaArrowLeft } from "react-icons/fa";
import { Sidebar, TopBar, RightSidebar, PlayerBar } from "@components/layout";
import { AddToPlaylistModal, CreatePlaylistModal } from "@components/common";
import artworksService from "@services/artworksService";
import playHistoryService from "@services/playHistoryService";

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
  const audioRef = useRef(null);
  const { id } = useParams(); // Get album ID from URL for backend integration
  
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [searchValue, setSearchValue] = useState("");
  const [currentTrackId, setCurrentTrackId] = useState(null);
  const [isLiked, setIsLiked] = useState(false);
  const [showAddToPlaylistModal, setShowAddToPlaylistModal] = useState(false);
  const [showCreatePlaylistModal, setShowCreatePlaylistModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [albumData, setAlbumData] = useState(null);
  const [tracks, setTracks] = useState([]);
  const [currentSong, setCurrentSong] = useState(null);
  const [error, setError] = useState(null);

  const relatedArtworks = [
    { id: 1, name: "The ReVe Festival Day...", image: "/ArtworkImage5.png" },
    { id: 2, name: "The ReVe Festival 202...", image: "/ArtworkImage6.png" },
    { id: 3, name: "Artwork 7", image: "/ArtworkImage7.png" },
    { id: 4, name: "Artwork 8", image: "/ArtworkImage8.png" },
  ];

  useEffect(() => {
    fetchAlbumData();
  }, [id]);

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

  const fetchAlbumData = async () => {
    try {
      setLoading(true);
      setError(null);
      console.log(`🎵 Fetching album ${id} data...`);

      // Clear previous data
      setAlbumData(null);
      setTracks([]);
      setCurrentSong(null);

      const [albumRes, tracksRes] = await Promise.all([
        artworksService.getAlbumById(id),
        artworksService.getAlbumTracks(id),
      ]);

      console.log('✅ Album Response:', albumRes);
      console.log('✅ Tracks Response:', tracksRes);

      // Handle album data
      if (albumRes && albumRes.album) {
        setAlbumData(albumRes.album);
      } else {
        throw new Error('No album data received from server');
      }

      // Handle tracks data
      if (tracksRes && Array.isArray(tracksRes.tracks)) {
        setTracks(tracksRes.tracks);
        if (tracksRes.tracks.length > 0) {
          setCurrentTrackId(tracksRes.tracks[0].jamendo_id);
          setCurrentSong(tracksRes.tracks[0]);
        }
      } else {
        console.warn('No tracks found for this album');
        setTracks([]);
      }
    } catch (err) {
      console.error('❌ Error fetching album data:', err);
      setError(err.message || 'Failed to load album. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const playSong = async (track) => {
    if (currentSong?.jamendo_id === track.jamendo_id && isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      setCurrentSong(track);
      setCurrentTrackId(track.jamendo_id);
      if (audioRef.current) {
        audioRef.current.src = track.audio_url;
        audioRef.current.play();
        setIsPlaying(true);

        // Record play in history
        try {
          if (track.ArtworkID) {
            await playHistoryService.recordPlay(track.ArtworkID);
          }
        } catch (error) {
          console.error('Failed to record play history:', error);
          // Don't stop playback if history recording fails
        }
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

  // Sample playlists - This will be fetched from backend
  const myPlaylists = [
    { id: 1, name: "My Liked Song", image: "/ArtworkImage5.png" },
    { id: 2, name: "Playlist 1", image: "/ArtworkImage6.png" },
    { id: 3, name: "Playlist 2", image: "/ArtworkImage7.png" },
    { id: 4, name: "Playlist 3", image: "/ArtworkImage8.png" },
  ];

  const handleLogout = () => {
    navigate("/");
  };

  const handleBack = () => {
    navigate(-1); // Go back to previous page
  };

  const handleTrackClick = (track) => {
    playSong(track);
  };

  if (loading) {
    return (
      <div className="flex h-screen bg-[#3E3B2C] items-center justify-center">
        <div className="text-white text-center">
          <p className="text-2xl font-bold">Loading album...</p>
        </div>
      </div>
    );
  }

  if (error || !albumData) {
    return (
      <div className="flex h-screen bg-[#3E3B2C] items-center justify-center">
        <div className="text-white text-center">
          <p className="text-2xl font-bold text-red-500">Error loading album</p>
          <p className="text-gray-400 mt-2">{error}</p>
          <button
            onClick={() => navigate(-1)}
            className="mt-4 bg-[#F6A661] text-[#3E3B2C] px-6 py-2 rounded-full font-bold hover:bg-[#E5954F] transition-colors"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  const upcomingSong = tracks.length > 1 ? {
    title: tracks[1].title,
    artist: tracks[1].artist,
    image: albumData.image_url,
  } : {
    title: "No more tracks",
    artist: albumData.artist,
    image: albumData.image_url,
  };

  const artistInfo = {
    name: albumData.artist,
    description:
      "Discover amazing music from independent artists around the world. All tracks are licensed under Creative Commons, supporting free culture and artistic expression.",
    image: albumData.image_url,
    buttonLabel: "Follow",
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
          onProfileClick={() => navigate("/listener/profile")}
        />

        {/* Main Content - Scrollable */}
        <div className="flex-1 overflow-y-auto p-6 scrollbar-hide">
          {/* Album Header */}
          <div className="flex gap-6 mb-8">
            <motion.img
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
              src={albumData.image_url}
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
                  {albumData.artist} • {albumData.release_date ? new Date(albumData.release_date).getFullYear() : 'N/A'} • {albumData.track_count} songs
                </span>
              </div>
              <div className="flex items-center gap-4">
                <button 
                  onClick={() => {
                    if (tracks.length > 0) {
                      playSong(tracks[0]);
                    }
                  }}
                  className="bg-[#F6A661] text-[#3E3B2C] px-8 py-2 rounded-full font-bold hover:bg-[#E5954F] transition-colors flex items-center gap-2"
                >
                  <FaPlay className="w-4 h-4" />
                  Play
                </button>
                <button
                  onClick={() => setShowAddToPlaylistModal(true)}
                  className="bg-transparent border-2 border-[#F6A661] text-[#F6A661] px-8 py-2 rounded-full font-bold hover:bg-[#F6A661] hover:text-[#3E3B2C] transition-colors"
                >
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
                  <th className="text-left text-gray-400 font-bold pb-4">Duration</th>
                </tr>
              </thead>
              <tbody>
                {tracks.map((track, index) => (
                  <motion.tr
                    key={track.jamendo_id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    onClick={() => handleTrackClick(track)}
                    className={`border-b border-gray-700/50 cursor-pointer hover:bg-[#3E3B2C]/50 transition-colors ${
                      currentTrackId === track.jamendo_id ? "bg-[#F6A661]/20" : ""
                    }`}
                  >
                    <td className={`py-4 ${currentTrackId === track.jamendo_id ? "text-[#F6A661]" : "text-gray-400"}`}>
                      {index + 1}
                    </td>
                    <td className="py-4">
                      <div>
                        <p className={`font-semibold ${currentTrackId === track.jamendo_id ? "text-[#F6A661]" : "text-white"}`}>
                          {track.title}
                        </p>
                        <p className="text-sm text-gray-400">{track.artist}</p>
                      </div>
                    </td>
                    <td className="py-4 text-right text-gray-400">
                      {track.duration ? `${Math.floor(track.duration / 60)}:${String(track.duration % 60).padStart(2, '0')}` : 'N/A'}
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Footer Player Bar */}
        <PlayerBar
          isPlaying={isPlaying}
          onTogglePlay={togglePlay}
          currentTime={currentTime}
          duration={duration}
          onSeek={handleSeek}
          trackTitle={currentSong ? currentSong.title : "Select a track"}
          trackArtist={currentSong ? currentSong.artist : "No artist"}
          trackImage={currentSong ? currentSong.image_url : null}
          volume={70}
          onVolumeChange={() => {}}
          onAddToPlaylist={() => setShowAddToPlaylistModal(true)}
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
          artist: "Select a track to play",
          image: albumData?.image_url || "/Artwork_cover.png"
        }}
        upcomingSong={upcomingSong}
        artistInfo={artistInfo}
        relatedArtworks={relatedArtworks}
      />

      {/* Add to Playlist Modal */}
      <AddToPlaylistModal
        isOpen={showAddToPlaylistModal}
        onClose={() => setShowAddToPlaylistModal(false)}
        playlists={myPlaylists}
        onCreateNew={() => {
          setShowAddToPlaylistModal(false);
          setShowCreatePlaylistModal(true);
        }}
        onAddToPlaylist={(playlistId) => {
          console.log("Adding album to playlist:", playlistId);
          // Add logic to add album to playlist
        }}
      />

      {/* Create Playlist Modal */}
      <CreatePlaylistModal
        isOpen={showCreatePlaylistModal}
        onClose={() => setShowCreatePlaylistModal(false)}
        onCreate={(playlistData) => {
          console.log("Creating playlist:", playlistData);
          // Add logic to create new playlist
        }}
      />
    </div>
  );
};

export default AlbumDetailPage;

