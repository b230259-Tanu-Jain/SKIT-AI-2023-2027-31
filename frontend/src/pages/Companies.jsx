import React, { useMemo, useState } from "react";
import CompanyCard from "../components/CompanyCard";
const companyData = [
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

function Companies() {
  const [search, setSearch] = useState("");
  const [minScore, setMinScore] = useState("0");
  const [sortOrder, setSortOrder] = useState("high");

  const filteredCompanies = useMemo(() => {
    return companyData
      .filter((company) =>
        company.name.toLowerCase().includes(search.trim().toLowerCase())
      )
      .filter((company) => {
        const score = Number(company.score);
        return Number.isFinite(score) && score >= Number(minScore);
      })
      .sort((a, b) =>
        sortOrder === "high"
          ? Number(b.score) - Number(a.score)
          : Number(a.score) - Number(b.score)
      );
  }, [search, minScore, sortOrder]);

  return (
    <div className="companies-page">
      <h1>Explore Companies</h1>
      <p className="page-subtitle">
        Compare workplace ratings and company insights.
      </p>

      <div className="company-filters">
        <input
          type="search"
          placeholder="Search companies..."
          aria-label="Search companies"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />

        <select
          aria-label="Filter by minimum company score"
          value={minScore}
          onChange={(event) => setMinScore(event.target.value)}
        >
          <option value="0">All scores</option>
          <option value="70">Score 70+</option>
          <option value="80">Score 80+</option>
          <option value="90">Score 90+</option>
        </select>

        <select
          aria-label="Sort companies by score"
          value={sortOrder}
          onChange={(event) => setSortOrder(event.target.value)}
        >
          <option value="high">Highest score first</option>
          <option value="low">Lowest score first</option>
        </select>
      </div>

      <p className="results-count" aria-live="polite">
        {filteredCompanies.length} compan{filteredCompanies.length === 1 ? "y" : "ies"} found
      </p>

      {filteredCompanies.length > 0 ? (
        <div className="companies-grid">
          {filteredCompanies.map((company) => (
            <CompanyCard key={company.name} {...company} />
          ))}
        </div>
      ) : (
        <div className="empty-results">
          No companies match your search or filters.
          <button
            type="button"
            className="secondary-btn"
            onClick={() => {
              setSearch("");
              setMinScore("0");
              setSortOrder("high");
            }}
          >
            Clear filters
          </button>
        </div>
      )}
    </div>
  );
}

export default Companies;