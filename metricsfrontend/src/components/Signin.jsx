import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { signin, signup } from '../services/api';

const Signin = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [isSignin, setSignin] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token');
    if (token) {
      navigate('/dashboard');
      return;
    }

    const params = new URLSearchParams(location.search);
    if (params.get('mode') === 'signup') {
      setSignin(false);
    } else {
      setSignin(true);
    }
  }, [location.search, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    const formData = new FormData(e.target);
    const name = formData.get("name");
    const email = formData.get("email");
    const password = formData.get("password");
    const confirmPassword = formData.get("confirmPassword");

    if (!isSignin && password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    try {
      if (isSignin) {
        const response = await signin(email, password);
        if (response.success) {
          navigate('/dashboard');
        } else {
          setError(response.message || 'Sign in failed');
        }
      } else {
        const response = await signup(name, email, password);
        if (response.success) {
          setSignin(true);
          setError('Account created successfully! Please sign in.');
        } else {
          setError(response.message || 'Sign up failed');
        }
      }
    } catch (err) {
      setError('Network error. Please try again later.');
      console.error('Authentication error:', err);
    }
  };

  return (
    <div className="grid w-full min-h-screen place-items-center bg-[url('src/assets/Back.jpg')] bg-cover bg-center px-4 py-6">
      <div className="w-full max-w-[430px] bg-white p-4 sm:p-8 rounded-2xl shadow-2xl border border-white/50 backdrop-blur-lg relative overflow-hidden">
        <div className="flex justify-center mb-4 sm:mb-6">
          <h2 className="text-2xl sm:text-3xl font-semibold text-neutral-600">{isSignin ? "Sign In" : "Sign Up"}</h2>
        </div>
        <div className="relative mb-6 sm:mb-8 border border-[#D50B8B] rounded-full overflow-hidden flex">
          <button
            onClick={() => setSignin(true)}
            className={`w-1/2 py-1.5 sm:py-2 z-10 font-medium text-sm sm:text-base transition-colors ${
              isSignin ? "text-white" : "text-black"
            }`}
          >
            Sign In
          </button>
          <button
            onClick={() => setSignin(false)}
            className={`w-1/2 py-1.5 sm:py-2 z-10 font-medium text-sm sm:text-base transition-colors ${
              !isSignin ? "text-white" : "text-black"
            }`}
          >
            Sign Up
          </button>
          <div
            className={`absolute top-0 h-full w-1/2 bg-[#D50B8B] rounded-full transition-all duration-300 ${
              isSignin ? "left-0" : "left-1/2"
            }`}
          ></div>
        </div>
        <form className="space-y-3 sm:space-y-4 relative z-10" onSubmit={handleSubmit}>
          {error && (
            <div className={`p-2 sm:p-3 rounded-lg text-xs sm:text-sm ${error.includes('successfully') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
              {error}
            </div>
          )}
          {!isSignin && (
            <input
              type="text"
              placeholder="Name"
              name="name" 
              required
              className="w-full p-2 sm:p-3 text-sm sm:text-base border-b-2 border-[#D50B8B] outline-none focus:border-[#D50B8B] placeholder-gray-500"
            />
          )}

          <input
            type="email"
            placeholder="Email"
            name="email" 
            required
            className="w-full p-2 sm:p-3 text-sm sm:text-base border-b-2 border-[#D50B8B] outline-none focus:border-[#D50B8B] placeholder-gray-500"
          />

          <input
            type="password"
            placeholder="Password"
            name="password"
            required
            className="w-full p-2 sm:p-3 text-sm sm:text-base border-b-2 border-[#D50B8B] outline-none focus:border-[#D50B8B] placeholder-gray-500"
          />
          {!isSignin && (
            <input
              type="password"
              placeholder="Confirm Password"
              name="confirmPassword"
              required
              className="w-full p-2 sm:p-3 text-sm sm:text-base border-b-2 border-[#D50B8B] outline-none focus:border-[#D50B8B] placeholder-gray-500"
            />
          )}

          <button
            type="submit"
            className="w-full py-2.5 sm:py-3 bg-[#D50B8B] text-white rounded-full text-sm sm:text-lg font-medium hover:opacity-90 transition mt-6"
          >
            {isSignin ? "Sign In" : "Sign Up"}
          </button>

          <p className="text-center text-gray-600 text-sm sm:text-base">
            {isSignin ? "Don't have an account?" : "Already have an account?"}{" "}
            <span
              onClick={() => setSignin(!isSignin)}
              className="text-[#D50B8B] hover:underline cursor-pointer"
            >
              {isSignin ? "Sign Up" : "Sign In"}
            </span>
          </p>
        </form>
      </div>
    </div>
  );
};

export default Signin;
