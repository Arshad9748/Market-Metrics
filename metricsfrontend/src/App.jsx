import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Landingpage from './components/Landingpage';
import Signin from './components/Signin';
import DashboardLayout from './components/DashboardLayout';
import DashboardHome from './components/DashboardHome';
import PricePredictionForm from './components/PricePredictionForm';
import QuantityPredictionForm from './components/QuantityPredictionForm';
import Analytics from './components/Analytics';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Landingpage />} />
        <Route path="/signin" element={<Signin />} />

        {/* Protected dashboard routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<DashboardHome />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="prediction/price" element={<PricePredictionForm />} />
          <Route path="prediction/quantity" element={<QuantityPredictionForm />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
