import React from "react";
import { useNavigate } from "react-router-dom";

function formatRating(value) {
  if (value === null || value === undefined || value === "") return "N/A";
  const rating = Number(value);
  return Number.isFinite(rating) ? `${rating}/100` : "N/A";
}

function CompanyCard({
  name, score, reviews, workLife, culture, career, compBenefits
}) {
  const navigate = useNavigate();

  const ratings = [
  ["Work-life balance", workLife],
  ["Culture & values", culture],
  ["Career opportunities", career],
  ["Compensation & benefits", compBenefits]
];

  const reviewCount = Number(reviews);
  const displayedReviews =
    Number.isFinite(reviewCount) && reviewCount >= 0
      ? reviewCount.toLocaleString()
      : "N/A";
  
  const company = {
  name, score, reviews, workLife, culture, career, compBenefits
};

  return (
    <article
      className="company-card"
      onClick={() => navigate("/company-details", { state: { company } })}
      role="button"
      tabIndex={0}
      onKeyDown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          navigate("/company-details", { state: { company } });
        }
      }}
    >
      <div className="company-card-heading">
        <h3>{name}</h3>
        <span className="company-score">{formatRating(score)}</span>
      </div>

      <p className="review-count">
        Employee reviews: {displayedReviews}
      </p>

      <div className="company-ratings">
        {ratings.map(([label, value]) => (
          <div className="rating-row" key={label}>
            <span>{label}</span>
            <strong>{formatRating(value)}</strong>
          </div>
        ))}
      </div>

      <p className="view-details">View Company Details →</p>
    </article>
  );
}
export default CompanyCard;
