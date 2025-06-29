import React from 'react';
import { Link } from 'react-router-dom';

const DashboardCard = ({ title, description, link }) => (
    <Link
        to={link}
        className="bg-black/50 p-6 rounded-lg hover:bg-[#D50B8B]/10 transition-colors border border-[#D50B8B]/20 hover:border-[#D50B8B]"
    >
        <h3 className="text-xl font-semibold mb-2 text-[#D50B8B]">{title}</h3>
        <p className="text-gray-300">{description}</p>
    </Link>
);

const DashboardHome = () => {
    const cards = [
        {
            title: 'Price Prediction',
            description: 'Predict the optimal price to make maximum profit.',
            link: '/dashboard/prediction/price'
        },
        {
            title: 'Quantity Prediction',
            description: 'Predict the optimal quantity to stock based on various factors.',
            link: '/dashboard/prediction/quantity'
        },
        // {
        //     title: 'Sales Growth',
        //     description: 'View and analyze your sales growth over time.',
        //     link: '/dashboard/sales'
        // },
        // {
        //     title: 'Analytics',
        //     description: 'Explore detailed graphs and analytics of your sales data.',
        //     link: '/dashboard/graphs'
        // }
    ];

    return (
        <div className="p-8">
            <h1 className="text-3xl font-bold mb-8 text-[#D50B8B]">Welcome to Market Metrics</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {cards.map((card, index) => (
                    <DashboardCard key={index} {...card} />
                ))}
            </div>
        </div>
    );
};

export default DashboardHome; 