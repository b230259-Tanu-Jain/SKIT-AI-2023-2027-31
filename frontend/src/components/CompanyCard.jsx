import React from "react";
import "../App.css";
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

  return (
    <article className="company-card">
      <div className="company-card-heading">
        <h2>{name}</h2>
        <span>
          {score == null ? "N/A" : `${score}/100`}
        </span>
      </div>

      <p>
        Employee reviews: {Number(reviews || 0).toLocaleString()}
      </p>

      {ratings.map(([label, value]) => (
        <div className="rating-row" key={label}>
          <span>{label}</span>
          <strong>
            {value == null || value === "" ? "N/A" : `${value}/100`}
          </strong>
        </div>
      ))}
    </article>
  );
}

export default CompanyCard;
