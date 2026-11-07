import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./CompanyDetails.css";

function CompanyDetails() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const company = state?.company;

  if (!company) {
    return (
      <div className="company-details">
        <h2>Company details not available</h2>
        <button onClick={() => navigate("/companies")}>
          Back to Companies
        </button>
      </div>
    );
  }

  const ratings = [
    ["Work-Life Balance", company.workLife],
    ["Culture & Values", company.culture],
    ["Career Opportunities", company.career]
  ];

  const formatRating = (value) => {
    const rating = Number(value);
    return value !== null && value !== undefined &&
      value !== "" && Number.isFinite(rating)
      ? `${rating}/100`
      : "N/A";
  };

  return (
    <div className="company-details">
      <button className="back-btn" onClick={() => navigate("/companies")}>
        ← Back to Companies
      </button>

      <div className="details-header">
        <div>
          <h1>{company.name}</h1>
          <p>Company Intelligence Overview</p>
        </div>
        <div className="details-score">
          <h2>{formatRating(company.score)}</h2>
          <span>Overall Score</span>
        </div>
      </div>

      <div className="details-stats">
        <div className="detail-box">
          <h2>{Number.isFinite(Number(company.reviews))
               ? Number(company.reviews).toLocaleString()
                : "N/A"}</h2>
          <p>Employee Reviews</p>
        </div>

        <div className="detail-box">
          <h2>{formatRating(company.score)}</h2>
          <p>Company Score</p>
        </div>
      </div>

      <h2 className="section-heading">Rating Breakdown</h2>

      <div className="details-ratings">
        {ratings.map(([label, value]) => {
          const rating = Number(value);
          const valid = value !== null && value !== undefined &&
            value !== "" && Number.isFinite(rating);

          return (
            <div className="details-rating" key={label}>
              <div>
                <span>{label}</span>
                <strong>{formatRating(value)}</strong>
              </div>
              <progress value={valid ? Math.max(0, Math.min(100, rating)) : 0}
                max="100" />
            </div>
          );
        })}
      </div>
    </div>
  );
}
export default CompanyDetails;
