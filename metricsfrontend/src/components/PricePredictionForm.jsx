import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { predictPrice } from '../services/api';

const categories = {
    "Flower/Leaf Vegetables": [
        "Niushou Shengcai",
        "Sichuan Red Cedar",
        "Local Xiaomao Cabbage",
        "White Caitai",
        "Amaranth",
        "Yunnan Shengcai",
        "Zhuyecai",
        "Chinese Cabbage",
        "Nanguajian",
        "Shanghaiqing"
    ],
    "Cabbage": [
        "Broccoli",
        "Purple Cabbage",
        "Qinggengsanhua",
        "Zhijiang Qinggengsanhua"
    ],
    "Aquatic Tuberous Vegetables": [
        "Lotus Root",
        "Net Lotus Root",
        "High Melon",
        "Water Chestnut",
        "Red Lotus Root Zone",
        "Wild Pink Lotus Root",
        "Honghu Lotus Root",
        "Lotus Root Tip"
    ],
    "Solanum": [
        "Eggplant",
        "Green Eggplant",
        "Round Eggplant",
        "Dalong Eggplant",
        "Hua Eggplant",
        "Changxianqie"
    ],
    "Capsicum": [
        "Red Hot Peppers",
        "Green Hot Peppers",
        "Red Pepper",
        "Green Hangjiao",
        "Bell Pepper",
        "Millet Pepper",
        "Purple Hot Peppers",
        "Fruit Chili"
    ],
    "Edible Mushroom": [
        "Xixia Black Mushroom",
        "Needle Mushroom",
        "Ping Mushroom",
        "Jigu Mushroom",
        "White Mushroom",
        "Agaricus Bisporus",
        "Tremella",
        "Hericium",
        "Black Fungus"
    ]
};

const PricePredictionForm = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [prediction, setPrediction] = useState(null);

    const [formData, setFormData] = useState({
        quantity_sold: '',
        wholesale_price: '',
        loss_rate: '',
        date: new Date().toISOString().split('T')[0],
        time: new Date().toTimeString().split(' ')[0],
        category_name: '',
        item_name: ''
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));

        if (name === 'category_name') {
            setFormData(prev => ({
                ...prev,
                item_name: ''
            }));
        }
    };

    const validateForm = () => {
        const errors = [];

        if (!formData.quantity_sold || formData.quantity_sold <= 0)
            errors.push('Quantity sold must be a positive number');

        if (!formData.wholesale_price || formData.wholesale_price <= 0)
            errors.push('Wholesale price must be a positive number');

        if (!formData.loss_rate || formData.loss_rate < 0 || formData.loss_rate > 100)
            errors.push('Loss rate must be between 0 and 100');

        const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
        if (!dateRegex.test(formData.date))
            errors.push('Invalid date format. Use YYYY-MM-DD');

        const timeRegex = /^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$/;
        if (!timeRegex.test(formData.time))
            errors.push('Invalid time format. Use HH:MM:SS (24-hour)');

        if (!formData.category_name)
            errors.push('Category name is required');

        if (!formData.item_name)
            errors.push('Item name is required');

        return errors;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setPrediction(null);

        const errors = validateForm();
        if (errors.length > 0) {
            setError(errors.join('\n'));
            return;
        }

        setLoading(true);
        try {
            const data = await predictPrice(formData);
            setPrediction(data);
        } catch (err) {
            if (err.message === 'No authentication token found') {
                navigate('/signin');
                return;
            }
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-black text-white p-1">
            <div className="container mx-auto">
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-4xl font-bold font-serif text-[#D50B8B]">
                        Price Prediction
                    </h1>
                </div>
                
                {error && (
                    <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded mb-6 whitespace-pre-line">
                        {error}
                    </div>
                )}
                
                <div className="bg-neutral-900 p-6 rounded-lg shadow-lg max-w-2xl mx-auto">
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium mb-1">Category Name</label>
                            <select
                                name="category_name"
                                value={formData.category_name}
                                onChange={handleInputChange}
                                className="w-full p-3 bg-black/50 border border-[#D50B8B] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#D50B8B] text-white"
                                required
                            >
                                <option value="" className="bg-black">Select Category</option>
                                {Object.keys(categories).map(category => (
                                    <option key={category} value={category} className="bg-black">
                                        {category}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-1">Item Name</label>
                            <select
                                name="item_name"
                                value={formData.item_name}
                                onChange={handleInputChange}
                                className="w-full p-3 bg-black/50 border border-[#D50B8B] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#D50B8B] text-white"
                                required
                                disabled={!formData.category_name}
                            >
                                <option value="" className="bg-black">Select Item</option>
                                {formData.category_name && categories[formData.category_name].map(item => (
                                    <option key={item} value={item} className="bg-black">
                                        {item}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-1">How much Quantity planing to sell (kg)</label>
                            <input
                                type="number"
                                step="0.01"
                                min="0"
                                name="quantity_sold"
                                value={formData.quantity_sold}
                                onChange={handleInputChange}
                                className="w-full p-3 bg-black/50 border border-[#D50B8B] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#D50B8B] text-white"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-1">Wholesale Price (INR/kg)</label>
                            <input
                                type="number"
                                step="0.01"
                                min="0"
                                max="30"
                                name="wholesale_price"
                                value={formData.wholesale_price}
                                onChange={handleInputChange}
                                className="w-full p-3 bg-black/50 border border-[#D50B8B] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#D50B8B] text-white"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-1">Loss Rate (%)</label>
                            <input
                                type="number"
                                step="0.1"
                                min="0"
                                max="100"
                                name="loss_rate"
                                value={formData.loss_rate}
                                onChange={handleInputChange}
                                className="w-full p-3 bg-black/50 border border-[#D50B8B] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#D50B8B] text-white"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-1">Date</label>
                            <input
                                type="date"
                                name="date"
                                value={formData.date}
                                onChange={handleInputChange}
                                min={new Date().toISOString().split('T')[0]}
                                className="w-full p-3 bg-black/50 border border-[#D50B8B] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#D50B8B] text-white"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-1">Time</label>
                            <input
                                type="time"
                                step="1"
                                name="time"
                                value={formData.time}
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
                            {loading ? 'Predicting...' : 'Predict Price'}
                        </button>
                    </form>

                    {prediction && (
                        <div className="mt-6">
                            <h3 className="text-xl font-semibold mb-3 text-[#D50B8B]">Predicted Price</h3>
                            <div className="bg-black/50 p-4 rounded-lg">
                                <p className="text-2xl font-bold">
                                ₹{prediction.predicted_price.toFixed(2)} INR
                                </p>
                                <div className="mt-4">
                                    <h4 className="text-sm font-semibold mb-2 text-[#D50B8B]">Input Features:</h4>
                                    <pre className="text-sm overflow-auto">
                                        {JSON.stringify(prediction.input_features, null, 2)}
                                    </pre>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default PricePredictionForm; 