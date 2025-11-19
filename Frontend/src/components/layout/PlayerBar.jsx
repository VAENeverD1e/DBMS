import React from "react";
import {
  FaPlay,
  FaPause,
  FaRandom,
  FaStepBackward,
  FaStepForward,
  FaRedo,
  FaVolumeUp,
  FaList,
  FaFileAlt,
} from "react-icons/fa";

/**
 * formatTime - Helper function to format seconds to MM:SS
 */
const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, "0")}`;
};

/**
 * PlayerBar Component
 * Reusable bottom player bar with playback controls
 */
const PlayerBar = ({
  isPlaying = false,
  onTogglePlay,
  currentTime = 0,
  duration = 0,
  trackTitle = "Song name",
  trackArtist = "Artist Name",
  trackImage = null,
  volume = 70,
  onVolumeChange,
}) => {
  const progress = duration > 0 ? (currentTime / duration) * 100 : 0;

  return (
    <div className="border-t border-[#2A2820] bg-[#2A2820] p-4">
      <div className="flex items-center justify-between">
        {/* Left: Current Song Info */}
        <div className="flex items-center gap-4 flex-1">
          {trackImage ? (
            <img
              src={trackImage}
              alt={trackTitle}
              className="w-14 h-14 rounded object-cover"
            />
          ) : (
            <div className="w-14 h-14 bg-[#F6A661] rounded"></div>
          )}
          <div>
            <p className="text-white font-semibold">{trackTitle}</p>
            <p className="text-gray-400 text-sm">{trackArtist}</p>
          </div>
        </div>

        {/* Center: Playback Controls */}
        <div className="flex flex-col items-center gap-2 flex-1">
          <div className="flex items-center gap-4">
            <FaRandom className="w-5 h-5 text-gray-400 cursor-pointer hover:text-[#F6A661]" />
            <FaStepBackward className="w-5 h-5 text-gray-400 cursor-pointer hover:text-[#F6A661]" />
            <button
              onClick={onTogglePlay}
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
                className="h-full bg-[#F6A661] rounded-full transition-all"
                style={{ width: `${progress}%` }}
              />
            </div>
            <span className="text-xs text-gray-400">{formatTime(duration)}</span>
          </div>
        </div>

        {/* Right: Additional Controls */}
        <div className="flex items-center gap-4 flex-1 justify-end">
          <FaFileAlt className="w-5 h-5 text-gray-400 cursor-pointer hover:text-[#F6A661]" />
          <FaList className="w-5 h-5 text-gray-400 cursor-pointer hover:text-[#F6A661]" />
          <div className="flex items-center gap-2">
            <FaVolumeUp className="w-5 h-5 text-gray-400 cursor-pointer hover:text-[#F6A661]" />
            <div className="w-24 h-1 bg-gray-600 rounded-full">
              <div
                className="h-full bg-[#F6A661] rounded-full transition-all"
                style={{ width: `${volume}%` }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlayerBar;

