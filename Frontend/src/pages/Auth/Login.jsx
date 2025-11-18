import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

const inputClasses =
  "w-full rounded-full bg-[#FFF1D6] text-[#3F3C35] px-4 py-3 text-lg font-semibold focus:outline-none focus:ring-2 focus:ring-[#F6A661]";

const Login = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    password: "",
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
    // Simulate login process, then redirect to home
    setTimeout(() => {
      setIsSubmitting(false);
      navigate('/home');
    }, 1200);
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
          className="w-full max-w-xl rounded-[32px] bg-[#0F0B05]/90 p-10 text-[#FFFBEF] shadow-[0_20px_80px_rgba(0,0,0,0.8)]"
        >
          <h1 className="mb-8 text-center font-karantina text-6xl tracking-wider text-[#F6A661]">
            SIGN IN MY ACCOUNT
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

            <div className="flex items-center justify-between text-sm font-semibold text-[#F6A661]">
              <Link to="#" className="hover:underline">
                * Forgot the password?
              </Link>
              <Link to="/signup" className="text-[#FFFBEF] hover:underline">
                Create a new account
              </Link>
            </div>

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={isSubmitting}
                className="rounded-full bg-[#F6A661] px-10 py-1 text-lg font-bold text-[#1F130B] transition-transform hover:scale-105 disabled:opacity-60"
              >
                {isSubmitting ? "Logging In..." : "Log In"}
              </button>
            </div>
          </form>
        </motion.div>
      </div>
    </div>
  );
};

export default Login;
