import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { RiHome5Line, RiLineChartLine, RiBarChartBoxLine, RiRobot2Line, RiMenuLine, RiLogoutBoxRLine } from 'react-icons/ri';
import logo from '../assets/acme.svg';

const navItems = [
    { icon: <RiHome5Line className="text-xl" />, name: "Home", path: "/dashboard" },
    { icon: <RiLineChartLine className="text-xl" />, name: "Analytics", path: "/dashboard/analytics" },
    { icon: <RiRobot2Line className="text-xl" />, name: "Price Prediction", path: "/dashboard/prediction/price" },
    { icon: <RiRobot2Line className="text-xl" />, name: "Quantity Prediction", path: "/dashboard/prediction/quantity" }
];

const Dashboard = () => {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/signin');
    };

    return (
        <>
            {/* Mobile Header */}
            <div className="lg:hidden fixed top-0 left-0 right-0 bg-neutral-900 text-white p-4 flex items-center justify-between z-50 border-b border-[#D50B8B]/20">
                <div className="flex items-center gap-3">
                    <img src={logo} alt="Market Metrics" className="w-6 h-6" />
                    <h2 className="text-lg font-bold">Market Metrics</h2>
                </div>
                <button 
                    onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                    className="p-2 hover:bg-[#D50B8B]/10 rounded-lg"
                >
                    <RiMenuLine className="text-xl" />
                </button>
            </div>

            {/* Desktop Sidebar */}
            <div className="hidden lg:flex w-64 min-h-screen bg-neutral-900 text-white flex-col p-6 border-r border-[#D50B8B]/20">
                <div className="flex items-center gap-3 mb-8">
                    <img src={logo} alt="Market Metrics" className="w-8 h-8" />
                    <h2 className="text-xl font-bold">Market Metrics</h2>
                </div>
                
                <nav className="flex flex-col space-y-2 flex-grow">
                    {navItems.map((item) => (
                        <NavLink
                            key={item.path}
                            to={item.path}
                            className={({ isActive }) =>
                                `flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                                    isActive 
                                        ? 'bg-[#D50B8B] text-white' 
                                        : 'text-gray-300 hover:bg-[#D50B8B]/10 hover:text-white'
                                }`
                            }
                        >
                            {item.icon}
                            <span>{item.name}</span>
                        </NavLink>
                    ))}
                </nav>

                {/* Desktop Logout Button */}
                <button
                    onClick={handleLogout}
                    className="flex items-center gap-3 px-4 py-3 rounded-lg transition-colors text-gray-300 hover:bg-[#D50B8B]/10 hover:text-white mt-auto"
                >
                    <RiLogoutBoxRLine className="text-xl" />
                    <span>Logout</span>
                </button>
            </div>

            {/* Mobile Navigation */}
            <div className={`lg:hidden fixed inset-0 bg-neutral-900/95 transform ${isMobileMenuOpen ? 'translate-x-0' : 'translate-x-full'} transition-transform duration-200 ease-in-out z-40`}>
                <nav className="flex flex-col space-y-2 p-6 pt-20">
                    {navItems.map((item) => (
                        <NavLink
                            key={item.path}
                            to={item.path}
                            onClick={() => setIsMobileMenuOpen(false)}
                            className={({ isActive }) =>
                                `flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                                    isActive 
                                        ? 'bg-[#D50B8B] text-white' 
                                        : 'text-gray-300 hover:bg-[#D50B8B]/10 hover:text-white'
                                }`
                            }
                        >
                            {item.icon}
                            <span>{item.name}</span>
                        </NavLink>
                    ))}
                </nav>
            </div>

            {/* Bottom Navigation Bar for Mobile */}
            <div className="lg:hidden fixed bottom-0 left-0 right-0 bg-neutral-900 border-t border-[#D50B8B]/20">
                <nav className="flex justify-around items-center h-16">
                    {navItems.map((item) => (
                        <NavLink
                            key={item.path}
                            to={item.path}
                            className={({ isActive }) =>
                                `flex flex-col items-center justify-center flex-1 py-2 ${
                                    isActive 
                                        ? 'text-[#D50B8B]' 
                                        : 'text-gray-300 hover:text-white'
                                }`
                            }
                        >
                            {item.icon}
                            <span className="text-xs mt-1">{item.name}</span>
                        </NavLink>
                    ))}
                </nav>
            </div>
        </>
    );
};

export default Dashboard;
