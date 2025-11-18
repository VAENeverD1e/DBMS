import React from "react";
import { motion } from "framer-motion";

/**
 * Hero Component
 * 
 * This is the main landing section that displays:
 * - Left side: Large custom orange (#F6A661) title "WELCOME TO HEADPHONES ON" (Karantina font)
 * - Description text about the platform
 * - "TRY IT NOW" button (custom orange #F6A661)
 * - Right side: Single polaroid-style image (HomeImage.png) with animations
 * 
 * Background color: #3F3C35 (dark brown/olive)
 * Image is displayed in grayscale with white polaroid border
 */
const Hero = () => {
  return (
    <div className="min-h-screen bg-[#3E3B2C] flex items-center justify-center pt-2 pb-16">
      <div className="container mx-auto px-1">
        <div className="grid items-center gap-12 lg:grid-cols-2">
          {/* Left Section - Text Content */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="space-y-6"
          >
            {/* Main Title - Large heading using Karantina font, color: #F6A661 */}
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="text-7xl font-bold text-[#F6A661] leading-tight font-karantina"
            >
              WELCOME TO HEADPHONES ON
            </motion.h1>

            {/* Description Text - White text explaining the platform */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.6 }}
              className="space-y-4"
            >
              <p className="text-white text-[20px] leading-relaxed mb-8">
              Headphones On is a vibrant music streaming platform where listeners and artists
              come together in one connected community. Discover songs you love, explore new
              releases, and follow your favorite artists — all in one place. 
              </p>


              <p className="text-white text-[20px] leading-relaxed">
                Whether you’re here to enjoy music or share your own, Headphones On offers
                a personalized experience with curated playlists, premium subscriptions, 
                and seamless interaction between creators and fans. Put your headphones on, 
                and let the music take over.
              </p>
            </motion.div>

            {/* Call-to-Action Button - Custom orange (#F6A661) button to encourage user action */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6, duration: 0.6 }}
              className="mt-8 flex justify-center"
            >
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-[#F6A661] text-white px-20 py-3 text-2xl font-bold rounded-full hover:bg-[#E5954F] transition-colors"
              >
                TRY IT NOW
              </motion.button>
            </motion.div>
          </motion.div>

          {/* Right Section - Single Polaroid Image */}
          {/* 
            Single image displayed in polaroid-style with animations
            Image is grayscale with white border to create the polaroid effect
            All animations are preserved: fade in, scale, and rotation
          */}
          <motion.div
            initial={{ opacity: 0, x: 70 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="flex justify-center items-center"
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.8, rotate: -10 }}
              animate={{ opacity: 1, scale: 1, rotate: -10 }}
              transition={{ delay: 0, duration: 0.8 }}
              whileHover={{ scale: 1.05, rotate: 0 }}
            >
              {/* Polaroid frame - white border around image */}
              <div className="bg-transparent p-2">
                {/* 
                  Single HomeImage.png displayed with animations
                  Image uses object-cover for consistent display
                  Sized appropriately with grayscale filter
                */}
                <img
                  src="/HomeImage.png"
                  alt="Headphones On"
                  className="w-180 h-180 object-cover grayscale"
                />
              </div>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
