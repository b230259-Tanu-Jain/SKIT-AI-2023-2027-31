import React from "react";
import { Link } from "react-router-dom";
import "./Dashboard.css";
const companies = [
  { name: "Microsoft", score: 92, reviews: 1250 },
  { name: "Google", score: 90, reviews: 1100 },
  { name: "Adobe", score: 87, reviews: 850 }
];
function Dashboard() {
  return (
    <div className="dashboard">
      <div className="dashboard-heading">
        <div>
          <h1>Welcome to WorkSphere</h1>
          <p>Discover companies that match your career goals.</p>
        </div>
        <Link to="/companies" className="primary-btn">
          Explore Companies
        </Link>
      </div>

      <div className="dashboard-stats">
        <div className="stat-card">
          <span>Companies Listed</span>
          <h2>91</h2>
        </div>
        <div className="stat-card">
          <span>Employee Reviews</span>
          <h2>20,000</h2>
        </div>
        <div className="stat-card">
          <span>Job Roles</span>
          <h2>1,167</h2>
        </div>
      </div>

      <section className="dashboard-section">
        <div className="section-heading">
          <h2>Top Companies</h2>
          <Link to="/companies">View all</Link>
        </div>

        <div className="dashboard-company-list">
          {companies.map((company) => (
            <div className="dashboard-company-card" key={company.name}>
              <div>
                <h3>{company.name}</h3>
                <p>{company.reviews.toLocaleString()} reviews</p>
              </div>
              <div className="company-score">
                <strong>{company.score}</strong>
                <span>/100</span>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
export default Dashboard;
