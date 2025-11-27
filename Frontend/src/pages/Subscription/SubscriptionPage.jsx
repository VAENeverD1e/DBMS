import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { FaHome } from "react-icons/fa";
import { Sidebar, TopBar, RightSidebar, PlayerBar } from "@components/layout";
import { PaymentModal } from "@components/common";
import subscriptionService from "@/services/subscriptionService";

/**
 * SubscriptionPage Component
 *
 * Subscription page where users can choose between LISTENER and ARTIST packages
 */
const SubscriptionPage = () => {
  const navigate = useNavigate();
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(102); // 1:42 in seconds
  const [duration] = useState(240); // 4:00 in seconds
  const [searchValue, setSearchValue] = useState("");
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [selectedPackage, setSelectedPackage] = useState(null);
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeSubscriptions, setActiveSubscriptions] = useState([]);
  const [subscribedTypes, setSubscribedTypes] = useState([]);

  // Sample data
  const relatedArtworks = [
    { id: 1, name: "The ReVe Festival Day...", image: "/ArtworkImage5.png" },
    { id: 2, name: "The ReVe Festival 202...", image: "/ArtworkImage6.png" },
    { id: 3, name: "Artwork 7", image: "/ArtworkImage7.png" },
    { id: 4, name: "Artwork 8", image: "/ArtworkImage8.png" },
  ];

  const currentSong = {
    title: "About Love",
    artist: "Red Velvet",
    image: "/RightBarImage.png",
  };

  const upcomingSong = {
    title: "Moonlight Melody",
    artist: "Red Velvet",
    image: "/RightBarImage.png",
  };

  const artistInfo = {
    name: "Red Velvet",
    description:
      "Red Velvet is a South Korean girl group formed by SM Entertainment in 2014. The group is known for its versatile music style and dual concept — the 'Red' side represents bright, energetic pop and dance music, while the 'Velvet' side showcases smooth R&B and soulful sounds. With hits like 'Bad Boy,' 'Red Flavor,' and 'Psycho,' Red Velvet has gained international recognition for their vocal talent, innovative concepts, and diverse discography.",
    image: "/RightBarImage.png",
    buttonLabel: "Follow",
  };

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);

      // Fetch plans and active subscriptions in parallel
      const [plansResponse, subsResponse] = await Promise.all([
        subscriptionService.getPlans(),
        subscriptionService.getMyActiveSubscriptions().catch(() => ({ subscriptions: [] }))
      ]);

      setPlans(plansResponse.plans || []);

      const subs = subsResponse.subscriptions || [];
      setActiveSubscriptions(subs);

      // Extract subscribed types (Listener, Artist)
      const types = subs.map(sub => sub.PlanType);
      setSubscribedTypes(types);

      setError(null);
    } catch (err) {
      console.error("Error fetching data:", err);
      setError("Failed to load subscription plans. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    navigate("/");
  };

  const handlePackageSelect = (plan) => {
    setSelectedPackage(plan);
    setShowPaymentModal(true);
  };

  // Separate plans by type
  const listenerPlans = plans.filter(
    (plan) => plan.Type === "Listener"
  );
  const artistPlans = plans.filter((plan) => plan.Type === "Artist");

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
          <h2 className="text-3xl font-bold text-white mb-8">
            Choose your subscription package
          </h2>

          {loading && (
            <div className="text-white text-center py-12">
              Loading subscription plans...
            </div>
          )}

          {error && (
            <div className="bg-red-500/20 text-red-200 p-4 rounded-lg mb-6">
              {error}
            </div>
          )}

          {!loading && !error && (
            <div className="grid grid-cols-2 gap-6">
              {/* LISTENER PACKAGE */}
              {listenerPlans.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                  className={`bg-[#F6A661] rounded-xl p-6 transition-transform relative ${
                    subscribedTypes.includes('Listener')
                      ? 'opacity-50 cursor-not-allowed'
                      : 'cursor-pointer hover:scale-105'
                  }`}
                  onClick={() => {
                    if (!subscribedTypes.includes('Listener')) {
                      handlePackageSelect(listenerPlans[0]);
                    }
                  }}
                >
                  {subscribedTypes.includes('Listener') && (
                    <div className="absolute top-4 right-4 bg-green-500 text-white px-3 py-1 rounded-full text-sm font-bold">
                      Subscribed
                    </div>
                  )}
              <div className="flex items-start gap-6 mb-6">
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
                    <div className="bg-white p-2 rounded shadow-2xl">
                      <img
                        src="/Guitar.png"
                        alt="Guitar"
                        className="w-28 h-28 object-cover"
                      />
                    </div>
                  </div>
                </div>
                <div className="flex-1">
                  <h3 className="text-5xl font-bold text-[#3E3B2C] font-karantina mb-4">
                    LISTENER PACKAGE
                  </h3>
                  <ul className="space-y-3 text-[#3E3B2C] text-lg font-semibold">
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
              )}

              {/* ARTIST PACKAGE */}
              {artistPlans.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.1 }}
                  className={`bg-[#F6A661] rounded-xl p-6 transition-transform relative ${
                    subscribedTypes.includes('Artist')
                      ? 'opacity-50 cursor-not-allowed'
                      : 'cursor-pointer hover:scale-105'
                  }`}
                  onClick={() => {
                    if (!subscribedTypes.includes('Artist')) {
                      handlePackageSelect(artistPlans[0]);
                    }
                  }}
                >
                  {subscribedTypes.includes('Artist') && (
                    <div className="absolute top-4 right-4 bg-green-500 text-white px-3 py-1 rounded-full text-sm font-bold">
                      Subscribed
                    </div>
                  )}
              <div className="flex items-start gap-6 mb-6">
                <div className="flex-1">
                  <h3 className="text-5xl font-bold text-[#3E3B2C] font-karantina mb-4">
                    ARTIST PACKAGE
                  </h3>
                  <ul className="space-y-3 text-[#3E3B2C] text-lg font-semibold">
                    <li className="flex items-start">
                      <span className="mr-2">•</span>
                      <span>Upload any songs that you want</span>
                    </li>
                    <li className="flex items-start">
                      <span className="mr-2">•</span>
                      <span>Fully promotion</span>
                    </li>
                    <li className="flex items-start">
                      <span className="mr-2">•</span>
                      <span>Under the management of label</span>
                    </li>
                  </ul>
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
                        className="w-28 h-28 object-cover"
                      />
                    </div>
                  </div>
                  <div
                    className="absolute bottom-0 right-0"
                    style={{ transform: "rotate(8deg)", zIndex: 1 }}
                  >
                    <div className="bg-white p-2 rounded shadow-2xl">
                      <img
                        src="/Guitar2.png"
                        alt="Guitar"
                        className="w-28 h-28 object-cover"
                      />
                    </div>
                  </div>
                </div>
              </div>
                </motion.div>
              )}
            </div>
          )}
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

      {/* Payment Modal */}
      <PaymentModal
        isOpen={showPaymentModal}
        onClose={() => setShowPaymentModal(false)}
        selectedPlan={selectedPackage}
      />
    </div>
  );
};

export default SubscriptionPage;
