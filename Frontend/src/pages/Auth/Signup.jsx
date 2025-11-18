import React, { useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

const inputClasses =
  "w-full rounded-full bg-[#FFF1D6] text-[#3F3C35] px-4 py-3 text-lg font-semibold focus:outline-none focus:ring-2 focus:ring-[#F6A661]";

const Signup = () => {
  const [formData, setFormData] = useState({
    username: "",
    firstName: "",
    lastName: "",
    email: "",
    birthDate: "",
    password: "",
    confirmPassword: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setTimeout(() => setIsSubmitting(false), 1500);
  };

  return (
    <div
      className="relative min-h-screen bg-cover bg-center bg-no-repeat"
      style={{
        backgroundImage: "url('/LoginBackground.png')",
      }}
    >
      <div className="absolute inset-0" />
      <div className="relative z-10 flex min-h-screen flex-col items-center justify-center px-4 py-12">
        {/* Logo */}
        <Link to="/" className="absolute left-6 top-6 flex items-center gap-3">
          <img src="/Logo.png" alt="Headphones On" className="h-16 w-16" />
          <span className="font-karantina text-4xl text-[#F6A661]">
            HEADPHONES ON
          </span>
        </Link>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="w-full max-w-3xl rounded-[32px] bg-[#0F0B05]/90 p-10 text-[#FFFBEF] shadow-[0_20px_80px_rgba(0,0,0,0.8)]"
        >
          <h1 className="mb-8 text-center font-karantina text-6xl tracking-wider text-[#F6A661]">
            CREATE A NEW ACCOUNT
          </h1>

          <form className="space-y-6" onSubmit={handleSubmit}>
            <div className="space-y-2">
              <label className="block text-3xl font-karantina tracking-wide text-[#F6A661]">
                USERNAME:
              </label>
              <input
                name="username"
                value={formData.username}
                onChange={handleChange}
                className={inputClasses}
                placeholder="Enter your username"
                required
              />
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <label className="block text-3xl font-karantina tracking-wide text-[#F6A661]">
                  FIRST NAME:
                </label>
                <input
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleChange}
                  className={inputClasses}
                  placeholder="Enter your first name"
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="block text-3xl font-karantina tracking-wide text-[#F6A661]">
                  LAST NAME:
                </label>
                <input
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleChange}
                  className={inputClasses}
                  placeholder="Enter your last name"
                  required
                />
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <label className="block text-3xl font-karantina tracking-wide text-[#F6A661]">
                  EMAIL:
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className={inputClasses}
                  placeholder="Enter your email"
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="block text-3xl font-karantina tracking-wide text-[#F6A661]">
                  DAY OF BIRTH:
                </label>
                <input
                  type="date"
                  name="birthDate"
                  value={formData.birthDate}
                  onChange={handleChange}
                  className={inputClasses}
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="block text-3xl font-karantina tracking-wide text-[#F6A661]">
                PASSWORD:
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className={inputClasses}
                placeholder="Enter your password"
                required
              />
            </div>

            <div className="space-y-2">
              <label className="block text-3xl font-karantina tracking-wide text-[#F6A661]">
                CONFIRM YOUR PASSWORD:
              </label>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className={inputClasses}
                placeholder="Re-enter your password"
                required
              />
            </div>

            <p className="text-center text-sm font-semibold text-[#F6A661]">
              Please read all the information again carefully
            </p>

            <div className="flex flex-col items-center gap-4 sm:flex-row sm:justify-between">
              <Link
                to="/login"
                className="text-sm font-semibold text-[#FFFBEF] underline"
              >
                Already have an account? Log in
              </Link>
              <button
                type="submit"
                disabled={isSubmitting}
                className="rounded-full bg-[#F6A661] px-10 py-3 text-lg font-bold text-[#1F130B] transition-transform hover:scale-105 disabled:opacity-60"
              >
                {isSubmitting ? "Creating..." : "Create My Account"}
              </button>
            </div>
          </form>
        </motion.div>
      </div>
    </div>
  );
};

export default Signup;

