import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { FaPlay, FaHeart, FaUpload } from "react-icons/fa";
import { Sidebar, ArtistRightSidebar } from "@components/layout";
import { UploadArtworkModal, JoinRecordLabelModal } from "@components/common";
import artistService from "@services/artistService";
import labelService from "@services/labelService";

/**
 * ArtistHomePage Component
 * 
 * Home page for artists
 * Features:
 * - Artist profile and metadata
 * - Popular songs list
 * - Discography, Albums, and Songs sections
 * - Upload artwork button
 * - Join record label option
 * - Statistics in right sidebar
 */
const ArtistHomePage = () => {
  const navigate = useNavigate();
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [showJoinLabelModal, setShowJoinLabelModal] = useState(false);
  const [statMode, setStatMode] = useState("reactions");
  const [currentSongId, setCurrentSongId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Artist data from API
  const [artistData, setArtistData] = useState({
    id: null,
    name: "Loading...",
    followers: 0,
    reactions: 0,
    image: "/ProfilePicArtist.png",
  });

  // Artworks from API
  const [artworks, setArtworks] = useState([]);
  const [albums, setAlbums] = useState([]);
  const [singles, setSingles] = useState([]);

  // Fetch artist data on mount
  useEffect(() => {
    const fetchArtistData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch current artist profile, stats, and recent artworks
        const response = await artistService.getCurrentArtist();

        if (response) {
          const { artist, stats, recent_artworks } = response;

          // Map artist data
          setArtistData({
            id: artist.ArtistID,
            name: artist.Username || `${artist.FirstName} ${artist.LastName}`,
            followers: stats.followers_count || 0,
            reactions: stats.total_likes || 0,
            image: "/ProfilePicArtist.png", // TODO: Add profile image field to backend
            genre: artist.Genre,
            verifiedStatus: artist.VerifiedStatus,
            labelId: artist.LabelID,
            labelName: null, // Will be fetched separately if labelId exists
          });

          // Fetch label information if artist has a label
          if (artist.LabelID) {
            try {
              const labelResponse = await labelService.getLabelById(artist.LabelID);
              if (labelResponse && labelResponse.label) {
                setArtistData(prev => ({
                  ...prev,
                  labelName: labelResponse.label.Name,
                }));
              }
            } catch (err) {
              console.error("Error fetching label:", err);
            }
          }

          // Process artworks
          const allArtworks = recent_artworks || [];
          setArtworks(allArtworks);

          // Separate albums and singles
          setAlbums(allArtworks.filter((a) => a.Type === "Album"));
          setSingles(allArtworks.filter((a) => a.Type === "Single"));
        }
      } catch (err) {
        console.error("Error fetching artist data:", err);
        setError(err.message || "Failed to load artist data");
      } finally {
        setLoading(false);
      }
    };

    fetchArtistData();
  }, []);

  // Refresh data after upload
  const refreshData = async () => {
    try {
      const response = await artistService.getCurrentArtist();
      if (response) {
        const { artist, stats, recent_artworks } = response;
        setArtistData({
          id: artist.ArtistID,
          name: artist.Username || `${artist.FirstName} ${artist.LastName}`,
          followers: stats.followers_count || 0,
          reactions: stats.total_likes || 0,
          image: "/ProfilePicArtist.png",
          genre: artist.Genre,
          verifiedStatus: artist.VerifiedStatus,
          labelId: artist.LabelID,
          labelName: null,
        });

        // Fetch label information if artist has a label
        if (artist.LabelID) {
          try {
            const labelResponse = await labelService.getLabelById(artist.LabelID);
            if (labelResponse && labelResponse.label) {
              setArtistData(prev => ({
                ...prev,
                labelName: labelResponse.label.Name,
              }));
            }
          } catch (err) {
            console.error("Error fetching label:", err);
          }
        }
        const allArtworks = recent_artworks || [];
        setArtworks(allArtworks);
        setAlbums(allArtworks.filter((a) => a.Type === "Album"));
        setSingles(allArtworks.filter((a) => a.Type === "Single"));
      }
    } catch (err) {
      console.error("Error refreshing data:", err);
    }
  };

  // Map artworks to display format
  const discography = artworks.slice(0, 4).map((artwork, index) => ({
    id: artwork.ArtworkID,
    name: artwork.Title,
    image: artwork.CoverImage || `/ArtworkImage${(index % 8) + 1}.png`,
  }));

  // Popular songs placeholder (would need a songs endpoint)
  const popularSongs = artworks.slice(0, 5).map((artwork, index) => ({
    id: artwork.ArtworkID,
    number: index + 1,
    title: artwork.Title,
    image: artwork.CoverImage || `/ArtworkImage${(index % 8) + 1}.png`,
    likes: artwork.TotalLike || 0,
    duration: artwork.Duration || "0:00",
  }));

  // Songs section (singles)
  const songs = singles.slice(0, 4).map((artwork, index) => ({
    id: artwork.ArtworkID,
    name: artwork.Title,
    image: artwork.CoverImage || `/ArtworkImage${(index % 8) + 1}.png`,
  }));

  // Statistics data
  const activitiesData = {
    months: ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"],
    reactions: [50, 60, 70, 80, 90, 150],
    followers: [100, 120, 140, 160, 180, 200],
  };

  const followerStats = {
    newFollowers: 10,
    reactions: 1000,
  };

  const genreData = {
    pop: 25,
    rock: 20,
    rnb: 15,
    ballad: 12,
    folk: 8,
    alternative: 7,
    electronic: 5,
    hyperpop: 4,
    experimental: 2,
    rap: 2,
  };

  const handleLogout = () => {
    navigate("/");
  };

  const handleSongClick = (songId) => {
    setCurrentSongId(songId);
  };

  const handleItemClick = (itemId, type) => {
    if (type === "album" || type === "artwork") {
      navigate(`/artist/artwork/${itemId}`);
    } else if (type === "song") {
      handleSongClick(itemId);
    }
  };

  const handleUpload = async (artworkData) => {
    console.log("Uploading artwork:", artworkData);
    
    try {
      // Build FormData from artworkData
      const formData = new FormData();
      
      // Required fields
      formData.append('mode', artworkData.mode);
      formData.append('title', artworkData.title);
      formData.append('genre', artworkData.genre);
      
      // Cover image
      if (artworkData.coverImage) {
        formData.append('cover_image', artworkData.coverImage);
      } else {
        console.error('Cover image is required');
        alert('Please upload a cover image');
        return;
      }
      
      // Track files and titles
      const tracks = artworkData.tracks || [];
      if (tracks.length === 0 || !tracks.some(t => t.file)) {
        console.error('At least one track file is required');
        alert('Please upload at least one track file');
        return;
      }
      
      tracks.forEach((track, index) => {
        if (track.file) {
          formData.append('track_files[]', track.file);
          formData.append('track_titles[]', track.title || `Track ${index + 1}`);
          formData.append('track_numbers[]', String(index + 1));
        }
      });
      
      // Collaborations (remove @ prefix if present)
      const collaborations = artworkData.collaborations || [];
      collaborations.forEach(collab => {
        const username = collab.replace(/^@/, '');
        if (username) {
          formData.append('collaborations[]', username);
        }
      });
      
      // Call API
      const response = await artistService.createArtwork(formData);
      console.log('Artwork created successfully:', response);
      
      // Close modal and refresh data
      setShowUploadModal(false);
      await refreshData();
      
    } catch (error) {
      console.error('Error uploading artwork:', error);
      alert('Failed to upload artwork: ' + (error.message || 'Unknown error'));
    }
  };

  const handleJoinLabel = async (label) => {
    try {
      if (!label || !label.LabelID) {
        console.error("Invalid label data");
        return;
      }

      // Update artist's label
      await artistService.updateArtistLabel(label.LabelID);
      
      // Refresh data to show updated label
      await refreshData();
      
      setShowJoinLabelModal(false);
    } catch (err) {
      console.error("Error joining label:", err);
      alert("Failed to join label: " + (err.message || "Unknown error"));
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
          {/* Artist Header */}
          <div className="flex gap-6 mb-8 relative">
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
              <p className="text-white text-sm mb-2">Artist</p>
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
                <button
                  onClick={() => setShowUploadModal(true)}
                  className="bg-[#F6A661] text-[#3E3B2C] px-8 py-3 rounded-full font-bold hover:bg-[#E5954F] transition-colors flex items-center gap-2"
                >
                  <FaUpload className="w-5 h-5" />
                  Upload An Artwork
                </button>
              </div>
            </div>
            {/* Join Record Label Link / Current Label */}
            {artistData.labelName ? (
              <div className="absolute top-0 right-0 flex items-center gap-2">
                <span className="text-white text-sm">Label:</span>
                <button
                  onClick={() => setShowJoinLabelModal(true)}
                  className="text-[#F6A661] hover:text-[#FFFBEF] text-sm font-semibold underline transition-colors"
                >
                  {artistData.labelName}
                </button>
              </div>
            ) : (
              <button
                onClick={() => setShowJoinLabelModal(true)}
                className="absolute top-0 right-0 text-gray-300 hover:text-white text-sm transition-colors"
              >
                I want to join a record label
              </button>
            )}
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
                    key={album.ArtworkID}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    onClick={() => handleItemClick(album.ArtworkID, "album")}
                    className="flex-shrink-0 w-64 cursor-pointer hover:scale-105 transition-transform"
                  >
                    <div className="bg-[#2A2820] rounded-2xl p-4">
                      <img
                        src={album.CoverImage || `/ArtworkImage${(index % 8) + 1}.png`}
                        alt={album.Title}
                        className="w-full aspect-square object-cover rounded-xl mb-2"
                        onError={(e) => {
                          e.target.src = `https://via.placeholder.com/300x300/3E3B2C/F6A661?text=Cover+Image`;
                        }}
                      />
                      <p className="text-white text-base font-semibold text-center">{album.Title}</p>
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
      </div>

      {/* Right Sidebar - Statistics */}
      <ArtistRightSidebar
        activitiesData={activitiesData}
        currentMode={statMode}
        onModeChange={setStatMode}
        followerStats={followerStats}
        genreData={genreData}
      />

      {/* Modals */}
      <UploadArtworkModal
        isOpen={showUploadModal}
        onClose={() => setShowUploadModal(false)}
        onUpload={handleUpload}
      />
      <JoinRecordLabelModal
        isOpen={showJoinLabelModal}
        onClose={() => setShowJoinLabelModal(false)}
        onJoin={handleJoinLabel}
      />
    </div>
  );
};

export default ArtistHomePage;

