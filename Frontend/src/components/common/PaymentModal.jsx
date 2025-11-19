import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";

/**
 * PaymentModal Component
 * Modal for processing subscription payments
 */
const PaymentModal = ({ isOpen, onClose, packageType = "listener" }) => {
  const navigate = useNavigate();
  const [paymentMethod, setPaymentMethod] = useState(null);
  const [subscriptionTime, setSubscriptionTime] = useState("1 month");
  const [cardInfo, setCardInfo] = useState({
    cardNumber: "",
    date: "",
    cvv: "",
    cardholderName: "",
  });

  if (!isOpen) return null;

  const subscriptionPrices = {
    "1 month": "20 000",
    "3 months": "55 000",
    "12 months": "200 000",
  };

  const totalAmount = subscriptionPrices[subscriptionTime] || "20 000";

  const handleCardInfoChange = (field, value) => {
    setCardInfo((prev) => ({ ...prev, [field]: value }));
  };

  const handlePaymentMethodSelect = (method) => {
    setPaymentMethod(method);
  };

  const handlePaymentComplete = () => {
    // After payment, navigate to listener home page
    onClose();
    navigate("/listener");
  };

  return (
    <div
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 backdrop-blur-md"
      onClick={onClose}
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
        className="bg-white rounded-3xl overflow-hidden max-w-5xl w-full mx-4 flex"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Left Panel - Payment Details */}
        <div className="bg-[#3E3B2C] flex-1 p-8 flex flex-col">
          <h2 className="text-5xl font-bold text-[#F6A661] font-karantina mb-8">
            PAYMENT
          </h2>

          {/* Payment Type Selection */}
          <div className="mb-8">
            <p className="text-white font-bold text-lg mb-4">Choose your type of payment:</p>
            <div className="flex gap-4">
              <motion.button
                onClick={() => handlePaymentMethodSelect("momo")}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className={`p-4 rounded-lg border-2 transition-all ${
                  paymentMethod === "momo"
                    ? "border-[#F6A661] bg-[#F6A661]/20"
                    : "border-gray-600 hover:border-[#F6A661]"
                }`}
              >
                <motion.img
                  src="/Momo.png"
                  alt="MoMo"
                  className="w-20 h-12 object-contain"
                  animate={{
                    scale: paymentMethod === "momo" ? 1.1 : 1,
                  }}
                  transition={{ duration: 0.2 }}
                />
              </motion.button>
              <motion.button
                onClick={() => handlePaymentMethodSelect("mastercard")}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className={`p-4 rounded-lg border-2 transition-all ${
                  paymentMethod === "mastercard"
                    ? "border-[#F6A661] bg-[#F6A661]/20"
                    : "border-gray-600 hover:border-[#F6A661]"
                }`}
              >
                <motion.img
                  src="/MastercardLogo.png"
                  alt="MasterCard"
                  className="w-20 h-12 object-contain"
                  animate={{
                    scale: paymentMethod === "mastercard" ? 1.1 : 1,
                  }}
                  transition={{ duration: 0.2 }}
                />
              </motion.button>
              <motion.button
                onClick={() => handlePaymentMethodSelect("visa")}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className={`p-4 rounded-lg border-2 transition-all ${
                  paymentMethod === "visa"
                    ? "border-[#F6A661] bg-[#F6A661]/20"
                    : "border-gray-600 hover:border-[#F6A661]"
                }`}
              >
                <motion.img
                  src="/VIsa.png"
                  alt="VISA"
                  className="w-20 h-12 object-contain"
                  animate={{
                    scale: paymentMethod === "visa" ? 1.1 : 1,
                  }}
                  transition={{ duration: 0.2 }}
                />
              </motion.button>
            </div>
          </div>

          {/* Card Information */}
          <AnimatePresence mode="wait">
            {paymentMethod && paymentMethod !== "momo" && (
              <motion.div
                key="card-info"
                initial={{ opacity: 0, height: 0, y: -20 }}
                animate={{ opacity: 1, height: "auto", y: 0 }}
                exit={{ opacity: 0, height: 0, y: -20 }}
                transition={{
                  duration: 0.3,
                  ease: "easeInOut",
                }}
                className="mb-8 overflow-hidden"
              >
                <motion.h3
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.1, duration: 0.3 }}
                  className="text-3xl font-bold font-karantina text-[#F6A661] mb-2"
                >
                  CARD INFORMATION
                </motion.h3>
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.2, duration: 0.3 }}
                  className="space-y-4"
                >
                  <motion.input
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.2, duration: 0.3 }}
                    type="text"
                    placeholder="Card Number"
                    value={cardInfo.cardNumber}
                    onChange={(e) =>
                      handleCardInfoChange("cardNumber", e.target.value)
                    }
                    className="w-full bg-white rounded-lg px-4 py-3 text-[#3E3B2C] focus:outline-none focus:ring-2 focus:ring-[#F6A661]"
                  />
                  <div className="flex gap-4">
                    <motion.div
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.3, duration: 0.3 }}
                      className="flex-1"
                    >
                      <label className="text-3xl font-bold font-karantina text-[#F6A661] mb-2 block">DATE</label>
                      <input
                        type="text"
                        placeholder="MM/YY"
                        value={cardInfo.date}
                        onChange={(e) => handleCardInfoChange("date", e.target.value)}
                        className="w-full bg-white rounded-lg px-4 py-3 text-[#3E3B2C] focus:outline-none focus:ring-2 focus:ring-[#F6A661]"
                      />
                    </motion.div>
                    <motion.div
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.35, duration: 0.3 }}
                      className="flex-1"
                    >
                      <label className="text-3xl font-bold font-karantina text-[#F6A661] mb-2 block">CVS/CVV:</label>
                      <input
                        type="text"
                        placeholder="CVV"
                        value={cardInfo.cvv}
                        onChange={(e) => handleCardInfoChange("cvv", e.target.value)}
                        className="w-full bg-white rounded-lg px-4 py-3 text-[#3E3B2C] focus:outline-none focus:ring-2 focus:ring-[#F6A661]"
                      />
                    </motion.div>
                  </div>
                  <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.4, duration: 0.3 }}
                  >
                    <label className="text-3xl font-bold font-karantina text-[#F6A661] mb-2 block">
                      CARDHOLDER NAME
                    </label>
                    <input
                      type="text"
                      placeholder="Cardholder Name"
                      value={cardInfo.cardholderName}
                      onChange={(e) =>
                        handleCardInfoChange("cardholderName", e.target.value)
                      }
                      className="w-full bg-white rounded-lg px-4 py-3 text-[#3E3B2C] focus:outline-none focus:ring-2 focus:ring-[#F6A661]"
                    />
                  </motion.div>
                </motion.div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Subscription Time */}
          <div className="mb-8">
            <h3 className="text-3xl font-karantina font-bold text-[#F6A661] mb-4">
              SUBSCRIPTION TIME
            </h3>
            <div className="flex gap-4">
              {Object.keys(subscriptionPrices).map((time) => (
                <motion.button
                  key={time}
                  onClick={() => setSubscriptionTime(time)}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className={`px-6 py-2 rounded-full font-bold text-xl transition-all ${
                    subscriptionTime === time
                      ? "bg-[#F6A661] text-[#3E3B2C]"
                      : "bg-white text-[#3E3B2C] hover:bg-gray-100"
                  }`}
                >
                  {time}
                </motion.button>
              ))}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="mt-auto flex gap-4">
            <button
              onClick={onClose}
              className="bg-[#F6A661] text-[#3E3B2C] px-6 py-1 rounded-full font-bold hover:bg-[#E5954F] transition-colors"
            >
              Back
            </button>
            {paymentMethod && (
              <button
                onClick={handlePaymentComplete}
                className="bg-white text-[#3E3B2C] px-6 py-1 rounded-full font-bold hover:bg-gray-100 transition-colors"
              >
                Pay
              </button>
            )}
          </div>
        </div>

        {/* Right Panel - QR Code and Total */}
        <div className="bg-[#F6A661] flex-1 p-8 flex flex-col items-center justify-center">
          <div className="mb-8">
            <img
              src="/QR code.png"
              alt="QR Code"
              className="w-64 h-64 object-contain bg-white p-2 rounded-lg"
            />
          </div>
          <div className="bg-white rounded-3xl p-6 w-96">
            <p className="text-[#3E3B2C] text-3xl font-bold font-karantina mb-2">TOTAL:</p>
            <p className="text-[#3E3B2C] text-4xl font-bold">
              {totalAmount} VND
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default PaymentModal;

