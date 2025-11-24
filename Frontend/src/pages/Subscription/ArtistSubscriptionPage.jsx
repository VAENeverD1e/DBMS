import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { FaHome } from "react-icons/fa";
import { Sidebar, TopBar, ArtistRightSidebar, PlayerBar } from "@components/layout";
import { PaymentModal } from "@components/common";

/**
 * ArtistSubscriptionPage Component
 * 
 * Subscription status page for artists who have already purchased a subscription
 * Shows current subscription information and RENEW button
 */
const ArtistSubscriptionPage = () => {
  const navigate = useNavigate();
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(102);
  const [duration] = useState(240);
  const [searchValue, setSearchValue] = useState("");
  const [showPaymentModal, setShowPaymentModal] = useState(false);

  // Sample subscription data - This will be fetched from backend
  const subscriptionData = {
    packageType: "artist",
    expiryDate: "Dec 31st",
    status: "active", // active, expired, cancelled
  };

  // Sample data for ArtistRightSidebar
  const activitiesData = {
    months: ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"],
    reactions: [100, 120, 150, 130, 180, 250],
    followers: [50, 60, 75, 65, 90, 120],
  };

  const followerStats = {
    newFollowers: 10,
    newReactions: 1000,
  };

  const genreData = {
    pop: 30,
    rock: 20,
    rnb: 15,
    ballad: 10,
    folk: 8,
    alternative: 5,
    electronic: 4,
    hyperpop: 3,
    experimental: 3,
    rap: 2,
  };

  const currentSong = {
    title: "About Love",
    artist: "Artist name",
    image: "/RightBarImage.png",
  };

  const handleLogout = () => {
    navigate("/");
  };

  const handleRenew = () => {
    setShowPaymentModal(true);
  };

  const artistNavItems = [
    { label: "Home", path: "/artist/home" },
    { label: "Subscription", path: "/artist/subscription" },
    { label: "Support", path: "/support" },
  ];

  return (
    <div className="flex h-screen bg-[#3E3B2C] overflow-hidden">
      {/* Left Sidebar */}
      <Sidebar userRole="ARTIST" navItems={artistNavItems} onLogout={handleLogout} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col bg-[#3E3B2C] overflow-hidden">
        {/* Top Bar */}
        <TopBar
          leftContent={<FaHome className="w-6 h-6 text-[#F6A661]" />}
          searchValue={searchValue}
          onSearchChange={setSearchValue}
          onProfileClick={() => navigate("/listener/profile")}
        />

        {/* Main Content - Scrollable */}
        <div className="flex-1 overflow-y-auto p-6 scrollbar-hide">
          <h2 className="text-3xl font-bold text-white mb-8">
            Choose your subscription package
          </h2>

          <div className="grid grid-cols-2 gap-6">
            {/* LISTENER PACKAGE - Available for Downgrade */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="bg-[#2A2820] rounded-xl p-6 cursor-pointer hover:scale-105 transition-transform border-2 border-[#3E3B2C]"
              onClick={() => navigate("/subscription")}
            >
              <div className="flex items-start gap-6 mb-6">
                <div
                  className="relative flex-shrink-0"
                  style={{ width: "140px", height: "180px" }}
                >
                  <div
                    className="absolute"
                    style={{ transform: "rotate(-8deg)", zIndex: 2 }}
                  >
                    <div className="bg-white p-2 rounded shadow-2xl opacity-80">
                      <img
                        src="/Singer.png"
                        alt="Singer"
                        className="w-28 h-28 object-cover"
                      />
                    </div>
                  </div>
                  <div
                    className="absolute bottom-0 right-0"
                    style={{ transform: "rotate(8deg)", zIndex: 1 }}
                  >
                    <div className="bg-white p-2 rounded shadow-2xl opacity-80">
                      <img
                        src="/Guitar.png"
                        alt="Guitar"
                        className="w-28 h-28 object-cover"
                      />
                    </div>
                  </div>
                </div>
                <div className="flex-1">
                  <h3 className="text-5xl font-bold text-white font-karantina mb-4">
                    LISTENER PACKAGE
                  </h3>
                  <ul className="space-y-3 text-gray-300 text-lg font-semibold">
                    <li className="flex items-start">
                      <span className="mr-2">•</span>
                      <span>Unlimited playlist creations</span>
                    </li>
                    <li className="flex items-start">
                      <span className="mr-2">•</span>
                      <span>Fully access to all the songs</span>
                    </li>
                    <li className="flex items-start">
                      <span className="mr-2">•</span>
                      <span>Keep up with your favourite artists</span>
                    </li>
                  </ul>
                </div>
              </div>
            </motion.div>

            {/* ARTIST PACKAGE - Current Subscription */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="bg-[#F6A661] rounded-xl p-6"
            >
              <div className="flex items-start gap-6 mb-6">
                <div className="flex-1">
                  <h3 className="text-5xl font-bold text-[#3E3B2C] font-karantina mb-4">
                    ARTIST PACKAGE
                  </h3>
                  <p className="text-[#3E3B2C] text-lg font-semibold mb-8">
                    The subscription is up to: {subscriptionData.expiryDate}
                  </p>
                  <button
                    onClick={handleRenew}
                    className="bg-[#3E3B2C] text-white px-8 py-2 rounded-full font-bold hover:bg-[#2A2820] transition-colors"
                  >
                    RENEW
                  </button>
                </div>
                <div
                  className="relative flex-shrink-0"
                  style={{ width: "140px", height: "180px" }}
                >
                  <div
                    className="absolute"
                    style={{ transform: "rotate(-8deg)", zIndex: 2 }}
                  >
                    <div className="bg-white p-2 rounded shadow-2xl">
                      <img
                        src="/Drum.png"
                        alt="Drum"
                        className="w-40 h-40 object-cover"
                      />
                    </div>
                  </div>
                </div>
              </div>
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

      {/* Right Sidebar - Artist Statistics */}
      <ArtistRightSidebar
        artistName="Artist name"
        activitiesData={activitiesData}
        followerStats={followerStats}
        genreData={genreData}
      />

      {/* Payment Modal */}
      <PaymentModal
        isOpen={showPaymentModal}
        onClose={() => setShowPaymentModal(false)}
        packageType="artist"
        isRenewal={true}
      />
    </div>
  );
};

export default ArtistSubscriptionPage;

