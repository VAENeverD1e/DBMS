import React, { useState } from "react";
import { motion } from "framer-motion";

/**
 * ArtistRightSidebar Component
 * 
 * Right sidebar for artist home page showing statistics and analytics
 * Features:
 * - Activities Statistic line chart
 * - Follower This Month section
 * - Genre distribution pie chart
 */
const ArtistRightSidebar = ({
  activitiesData = {
    months: ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"],
    reactions: [50, 60, 70, 80, 90, 150],
    followers: [100, 120, 140, 160, 180, 200],
  },
  currentMode = "reactions", // "reactions" or "followers"
  onModeChange,
  followerStats = {
    newFollowers: 10,
    reactions: 1000,
  },
  genreData = {
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
  },
}) => {
  const [selectedMode, setSelectedMode] = useState(currentMode);

  const handleModeChange = (mode) => {
    setSelectedMode(mode);
    onModeChange?.(mode);
  };

  // Calculate max value for chart scaling
  const maxValue = Math.max(
    ...activitiesData[selectedMode === "reactions" ? "reactions" : "followers"]
  );

  // Genre colors
  const genreColors = {
    pop: "#3B82F6", // blue
    rock: "#EF4444", // red
    rnb: "#F59E0B", // yellow
    ballad: "#10B981", // green
    folk: "#8B5CF6", // purple
    alternative: "#EC4899", // pink
    electronic: "#06B6D4", // cyan
    hyperpop: "#F97316", // orange
    experimental: "#84CC16", // lime
    rap: "#6366F1", // indigo
  };

  // Calculate pie chart segments
  const total = Object.values(genreData).reduce((sum, val) => sum + val, 0);
  let currentAngle = 0;
  const segments = Object.entries(genreData).map(([genre, value]) => {
    const percentage = (value / total) * 100;
    const angle = (value / total) * 360;
    const startAngle = currentAngle;
    currentAngle += angle;
    return {
      genre,
      value,
      percentage,
      startAngle,
      angle,
      color: genreColors[genre] || "#666",
    };
  });

  return (
    <div className="w-90 bg-[#2A2820] rounded-xl border-l-4 border-[#F6A661] flex flex-col overflow-hidden">
      <div className="flex-1 overflow-y-auto px-6 py-6 scrollbar-hide">
        {/* Activities Statistic */}
        <div className="mb-8">
          <h3 className="text-[#F6A661] font-bold text-lg mb-4">
            Activities Statistic
          </h3>
          <div className="bg-[#3E3B2C] rounded-lg p-4 mb-4">
            {/* Line Chart */}
            <div className="relative h-48">
              <svg className="w-full h-full" viewBox="0 0 400 200" preserveAspectRatio="none">
                {/* Grid lines */}
                {[0, 1, 2, 3, 4].map((i) => (
                  <line
                    key={i}
                    x1="0"
                    y1={40 + i * 40}
                    x2="400"
                    y2={40 + i * 40}
                    stroke="#3E3B2C"
                    strokeWidth="1"
                  />
                ))}
                {/* Data line */}
                <polyline
                  points={activitiesData.months
                    .map((month, index) => {
                      const value =
                        activitiesData[
                          selectedMode === "reactions" ? "reactions" : "followers"
                        ][index];
                      const x = (index / (activitiesData.months.length - 1)) * 400;
                      const y = 200 - (value / maxValue) * 160;
                      return `${x},${y}`;
                    })
                    .join(" ")}
                  fill="none"
                  stroke={selectedMode === "reactions" ? "#F6A661" : "#F6A661"}
                  strokeWidth="3"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                {/* Highlighted segment (Oct-Nov) */}
                <polyline
                  points={activitiesData.months
                    .slice(4)
                    .map((month, index) => {
                      const actualIndex = index + 4;
                      const value =
                        activitiesData[
                          selectedMode === "reactions" ? "reactions" : "followers"
                        ][actualIndex];
                      const x = (actualIndex / (activitiesData.months.length - 1)) * 400;
                      const y = 200 - (value / maxValue) * 160;
                      return `${x},${y}`;
                    })
                    .join(" ")}
                  fill="none"
                  stroke="#F6A661"
                  strokeWidth="4"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                {/* Data points */}
                {activitiesData.months.map((month, index) => {
                  const value =
                    activitiesData[
                      selectedMode === "reactions" ? "reactions" : "followers"
                    ][index];
                  const x = (index / (activitiesData.months.length - 1)) * 400;
                  const y = 200 - (value / maxValue) * 160;
                  const isHighlighted = index >= 4;

                  return (
                    <circle
                      key={month}
                      cx={x}
                      cy={y}
                      r="4"
                      fill={isHighlighted ? "#F6A661" : "#FFFFFF"}
                      stroke={isHighlighted ? "#F6A661" : "#FFFFFF"}
                      strokeWidth="2"
                    />
                  );
                })}
              </svg>
              {/* Month labels */}
              <div className="absolute bottom-0 left-0 right-0 flex justify-between px-2">
                {activitiesData.months.map((month) => (
                  <span key={month} className="text-white text-xs">
                    {month}
                  </span>
                ))}
              </div>
            </div>
          </div>
          {/* Mode Selector */}
          <div className="flex gap-2">
            <button
              onClick={() => handleModeChange("reactions")}
              className={`flex-1 px-4 py-2 rounded-full font-bold transition-colors ${
                selectedMode === "reactions"
                  ? "bg-[#F6A661] text-[#3E3B2C]"
                  : "bg-[#3E3B2C] text-white hover:bg-[#3E3B2C]/80"
              }`}
            >
              Reactions
            </button>
            <button
              onClick={() => handleModeChange("followers")}
              className={`flex-1 px-4 py-2 rounded-full font-bold transition-colors ${
                selectedMode === "followers"
                  ? "bg-[#F6A661] text-[#3E3B2C]"
                  : "bg-[#3E3B2C] text-white hover:bg-[#3E3B2C]/80"
              }`}
            >
              Followers
            </button>
          </div>
        </div>

        {/* Follower This Month */}
        <div className="mb-8">
          <h3 className="text-white font-bold text-lg mb-4">
            Follower This Month
          </h3>
          <div className="space-y-3">
            <button className="w-full bg-[#F6A661] text-[#3E3B2C] px-4 py-3 rounded-full font-bold hover:bg-[#E5954F] transition-colors">
              {followerStats.newFollowers} New Followers
            </button>
            <button className="w-full bg-[#F6A661] text-[#3E3B2C] px-4 py-3 rounded-full font-bold hover:bg-[#E5954F] transition-colors">
              {followerStats.reactions >= 1000
                ? `${(followerStats.reactions / 1000).toFixed(1)}K`
                : followerStats.reactions}{" "}
              Reaction
            </button>
          </div>
        </div>

        {/* Your Genre */}
        <div>
          <h3 className="text-white font-bold text-lg mb-4">Your Genre</h3>
          <div className="bg-[#3E3B2C] rounded-lg p-4">
            {/* Pie Chart */}
            <div className="relative w-48 h-48 mx-auto mb-4">
              <svg
                viewBox="0 0 200 200"
                className="transform -rotate-90"
                style={{ width: "100%", height: "100%" }}
              >
                {segments.map((segment, index) => {
                  const startAngleRad = (segment.startAngle * Math.PI) / 180;
                  const endAngleRad =
                    ((segment.startAngle + segment.angle) * Math.PI) / 180;
                  const largeArcFlag = segment.angle > 180 ? 1 : 0;

                  const x1 = 100 + 80 * Math.cos(startAngleRad);
                  const y1 = 100 + 80 * Math.sin(startAngleRad);
                  const x2 = 100 + 80 * Math.cos(endAngleRad);
                  const y2 = 100 + 80 * Math.sin(endAngleRad);

                  const pathData = [
                    `M 100 100`,
                    `L ${x1} ${y1}`,
                    `A 80 80 0 ${largeArcFlag} 1 ${x2} ${y2}`,
                    `Z`,
                  ].join(" ");

                  return (
                    <path
                      key={segment.genre}
                      d={pathData}
                      fill={segment.color}
                      stroke="#2A2820"
                      strokeWidth="2"
                    />
                  );
                })}
              </svg>
            </div>
            {/* Genre Labels */}
            <div className="space-y-2">
              {segments
                .filter((s) => s.percentage > 0)
                .map((segment) => (
                  <div
                    key={segment.genre}
                    className="flex items-center justify-between text-sm"
                  >
                    <div className="flex items-center gap-2">
                      <div
                        className="w-4 h-4 rounded"
                        style={{ backgroundColor: segment.color }}
                      />
                      <span className="text-white capitalize">
                        {segment.genre}
                      </span>
                    </div>
                    <span className="text-gray-400">
                      {segment.percentage.toFixed(1)}%
                    </span>
                  </div>
                ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArtistRightSidebar;

