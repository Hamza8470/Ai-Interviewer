import { Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import ResumeUpload from './pages/ResumeUpload';
import Interview from './pages/Interview';
import Results from './pages/Results';
import Profile from './pages/Profile';
import CompanyBank from './pages/CompanyBank';

export default function App() {
  return (
    <div className="min-h-screen text-slate-100">
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/resume-upload" element={<ProtectedRoute><ResumeUpload /></ProtectedRoute>} />
        <Route path="/interview" element={<ProtectedRoute><Interview /></ProtectedRoute>} />
        <Route path="/results" element={<ProtectedRoute><Results /></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
        <Route path="/company-bank" element={<ProtectedRoute><CompanyBank /></ProtectedRoute>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}
