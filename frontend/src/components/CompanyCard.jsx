import React from "react";

function CompanyCard({
  name,
  industry,
  rating,
  description
}) {
  return (
    <div className="company-card">

      <h3>{name}</h3>

      <p>{industry}</p>

      <p>
        Overall Rating: {rating}/5
      </p>

      <p>{description}</p>

      <button>View Details</button>

    </div>
  );
}

export default CompanyCard;