import React from "react";
import { Link } from "react-router-dom";
import "../App.css";;
import CompanyCard from "../components/CompanyCard";

const companies = [
  {
    name: "Microsoft",
    score: 92,
    workLife: 88,
    culture: 90,
    career: 91,
    reviews: 1250
  },
  {
    name: "Google",
    score: 90,
    workLife: 85,
    culture: 92,
    career: 94,
    reviews: 1100
  },
  {
    name: "Adobe",
    score: 87,
    workLife: 89,
    culture: 88,
    career: 85,
    reviews: 850
  }
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
            <CompanyCard
              key={company.name}
              name={company.name}
              score={company.score}
              reviews={company.reviews}
              workLife={company.workLife}
              culture={company.culture}
              career={company.career}
            />
          ))}
        </div>
      </section>
    </div>
  );
}

export default Dashboard;
