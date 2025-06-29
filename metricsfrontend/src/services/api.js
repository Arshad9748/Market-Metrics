const API_BASE_URL = 'http://localhost:5000';


const setToken = (token) => localStorage.setItem('token', token);
const removeToken = () => localStorage.removeItem('token');

// Authentication endpoints
export const signup = async (name, email, password) => {
    try {
        const response = await fetch(`${API_BASE_URL}/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, email, password }),
        });
        const data = await response.json();
        if (data.success && data.token) {
            setToken(data.token);
        }
        return data;
    } catch (error) {
        console.error('Error signing up:', error);
        throw error;
    }
};

export const signin = async (email, password) => {
    try {
        const response = await fetch(`${API_BASE_URL}/signin`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });
        const data = await response.json();
        if (data.success && data.token) {
            setToken(data.token);
        }
        return data;
    } catch (error) {
        console.error('Error signing in:', error);
        throw error;
    }
};

export const signout = () => {
    removeToken();
};

export const predictPrice = async (formData) => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('No authentication token found');
        }

        const response = await fetch(`${API_BASE_URL}/api/predict-price`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Failed to get prediction');
        }

        return data;
    } catch (error) {
        console.error('Error predicting price:', error);
        throw error;
    }
};

export const predictQuantity = async (formData) => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('No authentication token found');
        }

        const response = await fetch(`${API_BASE_URL}/api/predict-quantity`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Failed to get prediction');
        }

        return data;
    } catch (error) {
        console.error('Error predicting quantity:', error);
        throw error;
    }
};
