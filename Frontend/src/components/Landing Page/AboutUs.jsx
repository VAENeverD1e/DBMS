import React from "react";
import { motion } from "framer-motion";

/**
 * AboutUs Component
 * 
 * This section displays information about the platform:
 * - Left side: Large circular portrait image (grayscale)
 * - Right side: Custom orange (#F6A661) "ABOUT US" heading (Karantina font) and description text
 * 
 * Background color: #FFFBEF (light cream/beige)
 * Image: Mac Miller.png (circular, grayscale, with white border)
 */
const AboutUs = () => {
  return (
    <div className="min-h-screen bg-[#FFFBEF] flex items-center justify-center py-16">
      <div className="container mx-auto px-8">
        <div className="grid items-center gap-8 lg:grid-cols-2">
          {/* Left Section - Circular Portrait Image */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="flex justify-center"
          >
            <motion.div
              whileHover={{ scale: 1.12, rotate: 10 }}
              transition={{ duration: 0.5, ease: "easeOut" }}
              className="relative"
            >
              {/* 
                Circular portrait image
                - Grayscale filter applied
                - White border (4px) for visual emphasis
                - Rounded-full makes it circular
                - Shadow for depth
                Note: Image path uses '/' because it's in the public folder
              */}
              <img
                src="/Mac Miller.png"
                alt="About Us"
                className="w-128 h-128 rounded-full object-cover grayscale border-4 border-white shadow-2xl"
              />
            </motion.div>
          </motion.div>

          {/* Right Section - Content */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="space-y-6"
          >
            {/* Section Title - Custom orange (#F6A661) heading using Karantina font */}
            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="text-8xl font-bold text-[#F6A661] font-karantina"
            >
              ABOUT US
            </motion.h2>

            {/* Description Paragraphs - Dark text explaining the platform's mission */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.6 }}
              className="space-y-4 max-w-2xl"
            >
              <p className="text-[#3F3C35] text-[20px] leading-relaxed mb-8">
                At Headphones On, we believe music is more than sound — it’s connection, emotion, and creativity. Our platform was built to bridge the gap between listeners, artists, and record labels, creating a digital space where everyone can share and experience music freely.
              </p>

              <p className="text-[#3F3C35] text-[20px] leading-relaxed mb-8">
                Inspired by platforms like Spotify, Apple Music, and SoundCloud, Headphones On combines personalized playlists, artist collaboration, and performance analytics into one seamless experience. Whether you’re an independent artist hoping to reach new audiences or a listener searching for your next favorite song, we’re here to make every moment sound better.
              </p>

              <p className="text-[#3F3C35] text-[20px] leading-relaxed">
                Our mission is simple: empower artists, inspire listeners, and keep the music playing — everywhere, anytime.
              </p>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default AboutUs;
