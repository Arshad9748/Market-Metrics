import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
    // Check if user is authenticated
    const isAuthenticated = localStorage.getItem('token');

    if (!isAuthenticated) {
        // Redirect to signin page if not authenticated
        return <Navigate to="/signin" replace />;
    }

    return children;
};

export default ProtectedRoute; 