import React, { useMemo, useState } from "react";
import "./Companies.css";
const companyData = [
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

function Companies() {
  const [search, setSearch] = useState("");
  const [minScore, setMinScore] = useState(0);
  const [sortOrder, setSortOrder] = useState("high");

  const filteredCompanies = useMemo(() => {
    return companyData
      .filter((company) =>
        company.name.toLowerCase().includes(search.toLowerCase())
      )
      .filter((company) => company.score >= minScore)
      .sort((a, b) =>
        sortOrder === "high"
          ? b.score - a.score
          : a.score - b.score
      );
  }, [search, minScore, sortOrder]);

  return (
    <div className="companies-page">
      <h1>Explore Companies</h1>
      <p>Compare workplace ratings and company insights.</p>

      <div className="company-filters">
        <input
          type="search"
          placeholder="Search companies..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <select
          value={minScore}
          onChange={(e) => setMinScore(Number(e.target.value))}
        >
          <option value={0}>All scores</option>
          <option value={70}>Score 70+</option>
          <option value={80}>Score 80+</option>
          <option value={90}>Score 90+</option>
        </select>

        <select
          value={sortOrder}
          onChange={(e) => setSortOrder(e.target.value)}
        >
          <option value="high">Highest score first</option>
          <option value="low">Lowest score first</option>
        </select>
      </div>

      <div className="companies-grid">
        {filteredCompanies.map((company) => (
          <article className="company-card" key={company.name}>
            <div className="company-card-heading">
              <h2>{company.name}</h2>
              <span>{company.score}/100</span>
            </div>

            <p>Employee reviews: {company.reviews.toLocaleString()}</p>

            <div className="rating-row">
              <span>Work-life balance</span>
              <strong>{company.workLife}/100</strong>
            </div>
            <div className="rating-row">
              <span>Culture & values</span>
              <strong>{company.culture}/100</strong>
            </div>
            <div className="rating-row">
              <span>Career opportunities</span>
              <strong>{company.career}/100</strong>
            </div>
          </article>
        ))}
      </div>

      {filteredCompanies.length === 0 && (
        <p>No companies match your search or filters.</p>
      )}
    </div>
  );
}
export default Companies;
