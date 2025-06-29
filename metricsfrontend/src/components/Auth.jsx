import React, { useState } from 'react';
import { signup, signin } from '../services/api';

const Auth = ({ onAuthSuccess }) => {
    const [isSignup, setIsSignup] = useState(false);
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setLoading(true);

        try {
            const authFunction = isSignup ? signup : signin;
            const response = await authFunction(formData.username, formData.password);
            
            if (response.success) {
                onAuthSuccess();
            } else {
                setError(response.error);
            }
        } catch (error) {
            setError('An error occurred during authentication');
            console.error('Auth error:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    return (
        <div className="min-h-screen bg-black text-white flex items-center justify-center">
            <div className="bg-neutral-900 p-8 rounded-lg shadow-lg w-full max-w-md">
                <h2 className="text-3xl font-bold text-center mb-8 text-[#D50B8B]">
                    {isSignup ? 'Create Account' : 'Sign In'}
                </h2>

                {error && (
                    <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded mb-6">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium mb-2">Username</label>
                        <input
                            type="text"
                            name="username"
                            value={formData.username}
                            onChange={handleInputChange}
                            className="w-full p-3 bg-black/50 border border-[#D50B8B] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#D50B8B] text-white"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium mb-2">Password</label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleInputChange}
                            className="w-full p-3 bg-black/50 border border-[#D50B8B] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#D50B8B] text-white"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="w-full py-3 bg-[#D50B8B] text-white rounded-lg font-medium hover:bg-[#b40878] transition-colors disabled:opacity-50"
                        disabled={loading}
                    >
                        {loading ? 'Processing...' : (isSignup ? 'Sign Up' : 'Sign In')}
                    </button>
                </form>

                <div className="mt-6 text-center">
                    <button
                        onClick={() => setIsSignup(!isSignup)}
                        className="text-[#D50B8B] hover:text-[#b40878] transition-colors"
                    >
                        {isSignup
                            ? 'Already have an account? Sign In'
                            : "Don't have an account? Sign Up"}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Auth; 