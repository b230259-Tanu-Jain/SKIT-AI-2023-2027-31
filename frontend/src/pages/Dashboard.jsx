import React from "react";
import { Link } from "react-router-dom";
import CompanyCard from "../components/CompanyCard";

const companies = [
  {
    name: "Microsoft",
    score: 92,
    reviews: 1250,
    workLife: 88,
    culture: 90,
    career: 91
  },
  {
    name: "Google",
    score: 90,
    reviews: 1100,
    workLife: 85,
    culture: 92,
    career: 94
  },
  {
    name: "Adobe",
    score: 87,
    reviews: 850,
    workLife: 89,
    culture: 88,
    career: 85
  }
];

function Dashboard() {
  return (
    <div className="dashboard">
      <section className="dashboard-heading">
        <div>
          <h1>Welcome to WorkSphere</h1>
          <p>Discover companies that match your career goals.</p>
        </div>

        <Link to="/companies" className="primary-btn">
          Explore Companies
        </Link>
      </section>

      <section className="dashboard-stats" aria-label="Platform statistics">
        <article className="stat-card">
          <span>Companies Listed</span>
          <h2>91</h2>
        </article>

        <article className="stat-card">
          <span>Employee Reviews</span>
          <h2>20,000</h2>
        </article>

        <article className="stat-card">
          <span>Job Roles</span>
          <h2>1,167</h2>
        </article>
      </section>

      <section className="dashboard-section">
        <div className="section-heading">
          <h2>Top Companies</h2>
          <Link to="/companies">View all</Link>
        </div>

        <div className="dashboard-company-list">
          {companies.map((company) => (
            <CompanyCard key={company.name} {...company} />
          ))}
        </div>
      </section>
    </div>
  );
}

export default Dashboard;
