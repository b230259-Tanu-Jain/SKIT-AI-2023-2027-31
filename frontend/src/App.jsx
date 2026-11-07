import { BrowserRouter, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import Recommendations from "./pages/Recommendations";
import Companies from "./pages/Companies";
import CompanyDetails from "./pages/CompanyDetails";
export default function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Sidebar />
        <main className="main-content">
          <Navbar />
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/companies" element={<Companies />} />
            <Route path="/recommendations" element={<Recommendations />} />
            <Route path="/company-details" element={<CompanyDetails />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
