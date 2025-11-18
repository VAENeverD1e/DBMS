import React from "react";
import { motion } from "framer-motion";
import { COMMUNITY_IMAGES, COMMUNITY_LABELS } from "@utils/data";

/**
 * Community Component
 * 
 * This section displays the community features:
 * - Centered custom orange (#F6A661) "OUR COMMUNITY" heading (Karantina font)
 * - Three polaroid-style images in a row (grayscale with white borders)
 * - Three labels below the images describing community features
 * 
 * Background color: #3F3C35 (dark brown/olive)
 * Images: Guitar2.png, Singer.png, Drum.png
 */
const Community = () => {
  return (
    <div className="min-h-screen bg-[#3E3B2C] flex items-center justify-center py-16">
      <div className="container mx-auto px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.8 }}
          className="space-y-12"
        >
          {/* Section Heading - Centered custom orange (#F6A661) title using Karantina font */}
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2, duration: 0.6 }}
            className="text-8xl font-bold text-[#F6A661] text-center font-karantina"
          >
            OUR COMMUNITY
          </motion.h2>

          {/* Polaroid Images Section */}
          {/* 
            Three images displayed in a row with slight rotation
            Each image has a white border (polaroid effect) and grayscale filter
            Images rotate slightly on hover and scale up
          */}
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ delay: 0.4, duration: 0.8 }}
            className="flex justify-center items-center gap-10 flex-wrap"
          >
            {COMMUNITY_IMAGES.map((image, index) => (
              <motion.div
                key={image.id}
                initial={{ opacity: 0, y: 30, rotate: -5 + index * 5 }}
                whileInView={{ opacity: 1, y: 0, rotate: -5 + index * 5 }}
                viewport={{ once: true }}
                transition={{ delay: 0, duration: 0.6 }}
                whileHover={{ scale: 1.05, rotate: 0 }}
                className="bg-white p-4 shadow-2xl"
              >
                {/* Polaroid frame - white padding creates the border effect */}
                <img
                  src={image.src}
                  alt={image.alt}
                  className="w-100 h-100 object-cover grayscale"
                />
              </motion.div>
            ))}
          </motion.div>

          {/* Community Labels Section */}
          {/* 
            Three labels displayed below the images
            These describe the community features: Support Small Artists, Music Connection, For Music Lovers
            Using Karantina font with larger size and increased letter spacing
          */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.8, duration: 0.6 }}
            className="flex justify-center items-center gap-24 flex-wrap mt-16"
          >
            {COMMUNITY_LABELS.map((label, index) => (
              <motion.p
                key={label.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.9 + index * 0.1, duration: 0.6 }}
                className="text-white text-6xl font-bold font-karantina"
              >
                {label.label}
              </motion.p>
            ))}
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default Community;
