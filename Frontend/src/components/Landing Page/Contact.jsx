import React from "react";
import { motion } from "framer-motion";
import { FaLinkedin, FaFacebookSquare, FaYoutube, FaInstagram } from "react-icons/fa";
import { AiFillTikTok } from "react-icons/ai";

/**
 * Contact Component (Footer Section)
 * 
 * This is the footer section that displays:
 * - Left side: University information with logo and addresses
 * - Right side: "SUPPORT" heading (Karantina font) and social media icons
 * 
 * Background color: #FFFBEF (light cream/beige)
 * Social media icons: Facebook, Instagram, YouTube, LinkedIn, TikTok
 */
const Contact = () => {
  return (
    <motion.div
      className="bg-[#FFFBEF] p-12"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      viewport={{ once: true }}
    >
      <div className="container mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
          {/* Left Section - University Information */}
          <motion.div
            className="text-[#3F3C35] space-y-4"
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            viewport={{ once: true }}
          >
            {/* University Logo and Name */}
            <div className="flex items-center gap-3">
              {/* University logo - BachkhoaLogo.png from public folder */}
              <img src="/BachkhoaLogo.png" alt="HCMUT Logo" className="w-12 h-12" />
              <div>
                <p className="text-sm">Vietnam National University</p>
                <p className="font-bold text-lg">
                  Ho Chi Minh City University of Technology
                </p>
              </div>
            </div>
            {/* University Addresses - Two campus locations */}
            <div className="space-y-2 text-sm">
              <p>
                Campus 1: 268 Ly Thuong Kiet Street, District 10, Ho Chi Minh
                City, Vietnam.
              </p>
              <p>
                Campus 2: Vietnam National University – Ho Chi Minh City Urban
                Area, Thu Duc City, Ho Chi Minh City, Vietnam.
              </p>
            </div>
          </motion.div>

          {/* Right Section - Support & Social Media */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            viewport={{ once: true }}
            className="space-y-6"
          >
            {/* Support Heading - Custom orange (#F6A661) title using Karantina font */}
            <motion.h3
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.4, duration: 0.5 }}
              className="text-4xl font-bold text-[#F6A661] font-karantina"
            >
              SUPPORT
            </motion.h3>
            {/* Social Media Label */}
            <motion.p
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.5, duration: 0.5 }}
              className="text-[#3F3C35] text-lg mb-4"
            >
              Social Media:
            </motion.p>
            {/* Social Media Icons - Five platforms with hover effects */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.6, duration: 0.5 }}
              className="flex items-center gap-6"
            >
              {/* Facebook Icon */}
              <motion.a
                href="#"
                whileHover={{ scale: 1.1 }}
                transition={{ duration: 0.2 }}
              >
                <FaFacebookSquare className="w-12 h-12 text-blue-600" />
              </motion.a>
              {/* Instagram Icon */}
              <motion.a
                href="#"
                whileHover={{ scale: 1.1 }}
                transition={{ duration: 0.2 }}
              >
                <FaInstagram className="w-12 h-12 text-pink-500" />
              </motion.a>
              {/* YouTube Icon */}
              <motion.a
                href="#"
                whileHover={{ scale: 1.1 }}
                transition={{ duration: 0.2 }}
              >
                <FaYoutube className="w-12 h-12 text-red-700" />
              </motion.a>
              {/* LinkedIn Icon */}
              <motion.a
                href="#"
                whileHover={{ scale: 1.1 }}
                transition={{ duration: 0.2 }}
              >
                <FaLinkedin className="w-12 h-12 text-[#0072b1]" />
              </motion.a>
              {/* TikTok Icon */}
              <motion.a
                href="#"
                whileHover={{ scale: 1.1 }}
                transition={{ duration: 0.2 }}
              >
                <AiFillTikTok className="w-12 h-12 text-white" />
              </motion.a>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
};

export default Contact;
