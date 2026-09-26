import React from "react";
import CompanyCard from "../components/CompanyCard";

function Dashboard() {
  return (
    <div>
      <h1 className="page-title">
        Welcome to WorkSphere
      </h1>
      <p className="page-subtitle">
        Your AI-powered career intelligence platform
      </p>
      <div className="card-container">
        <div className="card">
          <h3>Resume Score</h3>
          <div className="card-value">86%</div>
        </div>
        <div className="card">
          <h3>Recommended Companies</h3>
          <div className="card-value">12</div>
        </div>
        <div className="card">
          <h3>Skills Matched</h3>
          <div className="card-value">18</div>
        </div>
      </div>
      <div className="section">
        <h2>Recommended Companies</h2>
        <div className="company-grid">
          <CompanyCard
            name="Microsoft"
            industry="Technology"
            rating="4.5"
            description="Technology and software company."
          />
          <CompanyCard
            name="Google"
            industry="Technology"
            rating="4.6"
            description="Technology and digital services company."
          />
          <CompanyCard
            name="Adobe"
            industry="Technology"
            rating="4.4"
            description="Software and creative technology company."
          />
        </div>
      </div>
    </div>
  );
}
export default Dashboard;