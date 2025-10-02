import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Login from "./pages/login";
import Register from "./pages/register";
import Dashboard from "./pages/Dashboard";
import PrivateRoute from "./components/PrivateRoute";
import './App.css';
import SummaryDetail from "./pages/SummaryDetail"; // ✅ importer le composant
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        } />
        <Route path="/summary/:id" element={<SummaryDetail />} />  {/* ✅ nouvelle route */}
        <Route path="*" element={<Login />} /> {/* redirection par défaut */}
      </Routes>
    </Router>
  );
}

export default App;
