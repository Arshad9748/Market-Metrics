import React from 'react';
import { Outlet } from 'react-router-dom';
import Dashboard from './Dashboard';

const DashboardLayout = () => {
    return (
        <div className="flex min-h-screen bg-black">
            {/* Sidebar */}
            <Dashboard />
            
            {/* Main Content */}
            <div className="flex-1 p-8">
                <div className="bg-neutral-900 rounded-lg shadow-lg">
                    <Outlet />
                </div>
            </div>
        </div>
    );
};

export default DashboardLayout; 