import React, { useState, useEffect, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { motion } from "framer-motion";
import { FaHome, FaPlay, FaHeart, FaArrowLeft, FaTrash, FaEdit } from "react-icons/fa";
import { Sidebar, TopBar, RightSidebar, PlayerBar } from "@components/layout";
import { usePlaylist } from "../../contexts/PlaylistContext";
import { useToast } from "../../contexts/ToastContext";
import playlistService from "@services/playlistService";

/**
 * PlaylistDetailPage Component
 * 
 * Displays detailed information about a playlist
 * Features:
 * - Playlist cover and metadata
 * - Tracklist with play controls
 * - Delete playlist button
 * - Rename playlist functionality
 * - Play and Like buttons
 */
const PlaylistDetailPage = () => {
  const navigate = useNavigate();
  const { id } = useParams(); // Get playlist ID from URL for backend integration
  const { playlists, deletePlaylist, updatePlaylist, fetchPlaylists } = usePlaylist();
  const { addToast } = useToast();
  const playlistId = Number(id);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(102);
  const [duration] = useState(240);
  const [searchValue, setSearchValue] = useState("");
  const [currentTrackId, setCurrentTrackId] = useState(8); // Currently playing track
  const [isLiked, setIsLiked] = useState(false);
  const [isEditingName, setIsEditingName] = useState(false);
  const [playlistName, setPlaylistName] = useState("My Liked Song");
  const [editingName, setEditingName] = useState("");
  const [originalName, setOriginalName] = useState("");
  const [nameError, setNameError] = useState("");
  const [shake, setShake] = useState(false);
  const nameInputRef = useRef(null);
  const [sortConfig, setSortConfig] = useState({
    key: 'number',
    direction: 'asc'
  });
  const [isSortOpen, setIsSortOpen] = useState(false);
  const sortOptions = [
    { key: 'number', label: '#' },
    { key: 'title', label: 'Title' },
    { key: 'artist', label: 'Artist' },
    { key: 'plays', label: 'Liked' },
    { key: 'duration', label: 'Duration' },
    { key: 'id', label: 'Recently added' }
  ];
  const getSortLabel = (key) => sortOptions.find(o => o.key === key)?.label || key;
  const handleSelectSort = (key) => {
    if (sortConfig.key === key) {
      setSortConfig({ key, direction: sortConfig.direction === 'asc' ? 'desc' : 'asc' });
    } else {
      setSortConfig({ key, direction: 'asc' });
    }
    setIsSortOpen(false);
  };
  const parseDuration = (d) => {
    if (!d || typeof d !== 'string') return 0;
    const [m, s] = d.split(':').map(Number);
    if (Number.isNaN(m) || Number.isNaN(s)) return 0;
    return m * 60 + s;
  };

  const [playlistData, setPlaylistData] = useState({
    title: playlistName,
    owner: "",
    songCount: 0,
    duration: "",
    coverImage: "/ArtworkImage5.png",
  });

  const [allTracks, setAllTracks] = useState([]);

  useEffect(() => {
    let isMounted = true;
    const fetchDetails = async () => {
      if (!playlistId) return;
      try {
        const res = await playlistService.getPlaylist(playlistId);
        if (!res.success || !res.playlist) return;

        const p = res.playlist;
        const songs = Array.isArray(p.songs) ? p.songs : [];

        const mmss = (seconds) => {
          if (!seconds && seconds !== 0) return "";
          const m = Math.floor(seconds / 60);
          const s = Math.floor(seconds % 60);
          return `${String(m)}:${String(s).padStart(2, "0")}`;
        };

        const mappedTracks = songs.map((s, idx) => ({
          id: s.SingleID,
          number: s.TrackNumber ?? idx + 1,
          title: s.song_title || `Track ${idx + 1}`,
          artist: s.artist_username || s.artist_full_name || "Unknown Artist",
          plays: 0,
          duration: typeof s.Duration === "number" ? mmss(s.Duration) : (s.Duration || ""),
          coverImage: s.CoverImage,
        }));

        const firstCover = songs[0]?.CoverImage;
        const totalDurationSec = songs
          .map((s) => (typeof s.Duration === "number" ? s.Duration : 0))
          .reduce((a, b) => a + b, 0);
        const totalDuration = totalDurationSec
          ? `${Math.floor(totalDurationSec / 60)}:${String(Math.floor(totalDurationSec % 60)).padStart(2, "0")}`
          : "";

        if (isMounted) {
          setPlaylistName(p.name || playlistName);
          setPlaylistData({
            title: p.name || playlistName,
            owner: p.owner?.username || "",
            songCount: songs.length,
            duration: totalDuration,
            coverImage: firstCover || "/ArtworkImage5.png",
          });
          setAllTracks(mappedTracks);
        }
      } catch (e) {
        // Optionally show a toast
      }
    };

    fetchDetails();
    return () => { isMounted = false; };
  }, [playlistId]);

  // Handle sort request
  const requestSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const getFilteredAndSortedTracks = () => {
    const filteredTracks = allTracks.filter(track => 
      track.title.toLowerCase().includes(searchValue.toLowerCase()) ||
      track.artist.toLowerCase().includes(searchValue.toLowerCase())
    );

    const dir = sortConfig.direction === 'asc' ? 1 : -1;
    const key = sortConfig.key;
    return [...filteredTracks].sort((a, b) => {
      if (key === 'title' || key === 'artist') {
        return a[key].localeCompare(b[key]) * dir;
      }
      if (key === 'duration') {
        const da = parseDuration(a.duration);
        const db = parseDuration(b.duration);
        if (da < db) return -1 * dir;
        if (da > db) return 1 * dir;
        return 0;
      }
      const va = a[key];
      const vb = b[key];
      if (va < vb) return -1 * dir;
      if (va > vb) return 1 * dir;
      return 0;
    });
  };

  const tracks = getFilteredAndSortedTracks();

  const relatedArtworks = [
    { id: 1, name: "The ReVe Festival Day...", image: "/ArtworkImage5.png" },
    { id: 2, name: "The ReVe Festival 202...", image: "/ArtworkImage6.png" },
    { id: 3, name: "Artwork 7", image: "/ArtworkImage7.png" },
    { id: 4, name: "Artwork 8", image: "/ArtworkImage8.png" },
  ];

  const currentSong = {
    title: tracks.find(t => t.id === currentTrackId)?.title || "Song name",
    artist: tracks.find(t => t.id === currentTrackId)?.artist || "Artist name",
    image: playlistData.coverImage,
  };

  const upcomingSong = {
    title: "Moonlight Melody",
    artist: "Artist name",
    image: playlistData.coverImage,
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
    navigate(-1); // Go back to previous page
  };

  const handleTrackClick = (trackId) => {
    setCurrentTrackId(trackId);
    setIsPlaying(true);
  };

  const handleDeletePlaylist = async () => {
    if (!playlistId) return;

    if (!window.confirm("Are you sure you want to delete this playlist?")) {
      return;
    }

    const result = await deletePlaylist(playlistId);
    if (result.success) {
      addToast("Playlist deleted successfully", "success");
      // Refresh playlists list so profile and modals stay in sync
      fetchPlaylists();
      navigate("/listener/profile");
    } else {
      addToast(result.error || "Failed to delete playlist", "error");
    }
  };

  const startOrSubmitRename = async (isBlur = false) => {
    if (!isEditingName) {
      setOriginalName(playlistName);
      setEditingName(playlistName);
      setNameError("");
      setIsEditingName(true);
      return;
    }

    const newName = (editingName || "").trim();
    if (!playlistId) return;

    if (!newName) {
      setNameError("Name cannot be empty");
      setEditingName(originalName);
      setShake(true);
      setTimeout(() => nameInputRef.current?.focus(), 0);
      return;
    }

    const duplicate = (playlists || []).some(
      (p) => p.playlist_id !== playlistId && (p.name || "").trim().toLowerCase() === newName.toLowerCase()
    );
    if (duplicate) {
      setNameError("Duplicate name");
      setEditingName(originalName);
      setShake(true);
      setTimeout(() => nameInputRef.current?.focus(), 0);
      addToast("You already have a playlist with this name", "error");
      return;
    }

    const result = await updatePlaylist(playlistId, newName);
    if (result.success) {
      setPlaylistName(newName);
      setIsEditingName(false);
      setNameError("");
      addToast("Playlist updated successfully", "success");
      fetchPlaylists();
    } else {
      setNameError("Update failed");
      setEditingName(originalName);
      setShake(true);
      setTimeout(() => nameInputRef.current?.focus(), 0);
      addToast(result.error || "Failed to update playlist", "error");
      if (!isBlur) return;
    }
  };

  const handleRenamePlaylist = async () => {
    if (!isEditingName) {
      setIsEditingName(true);
      return;
    }

    const newName = playlistName.trim();
    if (!newName || !playlistId) {
      setIsEditingName(false);
      return;
    }

    const result = await updatePlaylist(playlistId, newName);
    if (result.success) {
      addToast("Playlist updated successfully", "success");
      // Optionally refresh playlists so other views see the new name
      fetchPlaylists();
    } else {
      addToast(result.error || "Failed to update playlist", "error");
    }

    setIsEditingName(false);
  };

  const handleNameChange = (e) => {
    setEditingName(e.target.value);
    if (nameError) setNameError("");
  };

  const handleNameKeyPress = (e) => {
    if (e.key === "Enter") {
      startOrSubmitRename();
    } else if (e.key === "Escape") {
      setIsEditingName(false);
      setEditingName(originalName);
      setNameError("");
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
          onProfileClick={() => navigate("/listener/profile")}
        />

        {/* Main Content - Scrollable */}
        <div className="flex-1 overflow-y-auto p-6 scrollbar-hide">
          {/* Playlist Header */}
          <div className="flex gap-6 mb-8">
            <motion.img
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
              src={playlistData.coverImage}
              alt={playlistData.title}
              className="w-64 h-64 rounded-2xl object-cover flex-shrink-0"
              onError={(e) => {
                // e.target.src = `https://via.placeholder.com/400x400/3E3B2C/F6A661?text=${playlistData.title}`;
              }}
            />
            <div className="flex-1 flex flex-col justify-end">
              <p className="text-white text-sm mb-2">Playlist</p>
              <div className="flex items-center gap-4 mb-4">
                {isEditingName ? (
                  <motion.input
                    ref={nameInputRef}
                    type="text"
                    value={editingName}
                    onChange={handleNameChange}
                    onKeyDown={handleNameKeyPress}
                    onBlur={() => startOrSubmitRename(true)}
                    animate={shake ? { x: [0, -8, 8, -8, 8, 0] } : {}}
                    onAnimationComplete={() => setShake(false)}
                    className={`text-6xl font-bold bg-transparent rounded-lg px-4 py-2 focus:outline-none ${
                      nameError ? "border-2 border-red-500 text-red-200 focus:ring-2 focus:ring-red-500" : "border-2 border-[#F6A661] text-white focus:ring-2 focus:ring-[#F6A661]"
                    }`}
                    autoFocus
                  />
                ) : (
                  <h1 className="text-6xl font-bold text-white">{playlistName}</h1>
                )}
                <button
                  onClick={() => startOrSubmitRename()}
                  className="p-2 text-[#F6A661] hover:text-[#FFFBEF] transition-colors"
                  title="Rename playlist"
                >
                  <FaEdit className="w-6 h-6" />
                </button>
              </div>
              <div className="flex items-center gap-2 mb-6">
                <div className="w-2 h-2 bg-[#F6A661] rounded-full"></div>
                <span className="text-white">
                  {playlistData.songCount} songs, {playlistData.duration}
                </span>
              </div>
              <div className="flex items-center gap-4">
                <button className="bg-[#F6A661] text-[#3E3B2C] px-8 py-2 rounded-full font-bold hover:bg-[#E5954F] transition-colors flex items-center gap-2">
                  <FaPlay className="w-4 h-4" />
                  Play
                </button>
                <button
                  onClick={handleDeletePlaylist}
                  className="bg-transparent border-2 border-red-500 text-red-500 px-8 py-2 rounded-full font-bold hover:bg-red-500 hover:text-white transition-colors flex items-center gap-2"
                >
                  <FaTrash className="w-4 h-4" />
                  Delete Playlist
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

          <div className="bg-[#2A2820] rounded-2xl p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="text-white font-semibold">Tracklist</div>
              <div className="relative">
                <button
                  onClick={() => setIsSortOpen(!isSortOpen)}
                  className="bg-transparent border-2 border-[#F6A661] text-[#F6A661] px-4 py-1 rounded-full font-bold hover:bg-[#F6A661] hover:text-[#3E3B2C] transition-colors"
                >
                  Sort: {getSortLabel(sortConfig.key)} {sortConfig.direction === 'asc' ? '↑' : '↓'}
                </button>
                {isSortOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.15 }}
                    className="absolute right-0 mt-2 w-56 bg-[#3E3B2C] rounded-xl shadow-lg z-10 border border-[#2A2820]"
                  >
                    <div className="px-4 py-2 text-gray-400 text-sm">Sort by</div>
                    {sortOptions.map((opt) => (
                      <button
                        key={opt.key}
                        onClick={() => handleSelectSort(opt.key)}
                        className={`w-full text-left px-4 py-2 transition-colors flex items-center justify-between ${
                          sortConfig.key === opt.key ? 'text-[#F6A661]' : 'text-white'
                        } hover:bg-[#2A2820]`}
                      >
                        <span>{opt.label}</span>
                        {sortConfig.key === opt.key && <span>✓</span>}
                      </button>
                    ))}
                    <button
                      onClick={() => setIsSortOpen(false)}
                      className="w-full px-4 py-2 text-gray-400 hover:text-white hover:bg-[#2A2820] rounded-b-xl"
                    >
                      Cancel
                    </button>
                  </motion.div>
                )}
              </div>
            </div>
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

export default PlaylistDetailPage;

