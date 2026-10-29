import React from "react";
function formatRating(value) {
  if (value === null || value === undefined || value === "") {
    return "N/A";
  }
  const rating = Number(value);
  return Number.isFinite(rating) ? `${rating}/100` : "N/A";
}
function CompanyCard({
  name,
  score,
  reviews,
  workLife,
  culture,
  career
}) {
  const ratings = [
    ["Work-life balance", workLife],
    ["Culture & values", culture],
    ["Career opportunities", career]
  ];

  const reviewCount = Number(reviews);
  const displayedReviews =
    Number.isFinite(reviewCount) && reviewCount >= 0
      ? reviewCount.toLocaleString()
      : "N/A";

  return (
    <article className="company-card">
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
    </article>
  );
}

export default CompanyCard;
