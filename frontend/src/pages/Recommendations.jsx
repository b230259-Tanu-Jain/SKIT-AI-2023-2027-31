
import React, { useState } from "react";
import "../App.css";

const sampleCompanies = [
  {
    name: "Microsoft",
    score: 92,
    workLife: 88,
    culture: 90,
    career: 91,
    reason: "Strong overall company intelligence score."
  },
  {
    name: "Google",
    score: 90,
    workLife: 85,
    culture: 92,
    career: 94,
    reason: "Strong culture and career opportunity ratings."
  },
  {
    name: "Adobe",
    score: 87,
    workLife: 89,
    culture: 88,
    career: 85,
    reason: "Good work-life balance and workplace ratings."
  }
];

export default function Recommendations() {
  const [skills, setSkills] = useState("Python, Java, SQL");
  const [workLife, setWorkLife] = useState(80);
  const [culture, setCulture] = useState(80);
  const [career, setCareer] = useState(80);
  const [results, setResults] = useState([]);

  function generateRecommendations(event) {
    event.preventDefault();

    const preferences = [
      ["workLife", Number(workLife)],
      ["culture", Number(culture)],
      ["career", Number(career)]
    ];

    const ranked = sampleCompanies.map((company) => {
      const preferenceScore =
        preferences.reduce(
          (total, [key, desired]) =>
            total + (100 - Math.abs(company[key] - desired)),
          0
        ) / preferences.length;

      return {
        ...company,
        preferenceScore: Number(preferenceScore.toFixed(2)),
        recommendationScore: Number(
          (company.score * 0.7 + preferenceScore * 0.3).toFixed(2)
        )
      };
    });

    setResults(
      ranked.sort((a, b) => b.recommendationScore - a.recommendationScore)
    );
  }

  return (
    <div className="recommendations-page">
      <h1 className="page-title">Personalized Recommendations</h1>
      <p className="page-subtitle">
        Explore companies based on your workplace preferences and skills.
      </p>

      <form className="section" onSubmit={generateRecommendations}>
        <h2>Your Career Preferences</h2>

        <label htmlFor="skills">Your skills</label>
        <input
          id="skills"
          className="search-box"
          value={skills}
          onChange={(event) => setSkills(event.target.value)}
          placeholder="Python, Java, SQL"
        />

        <label htmlFor="workLife">Desired work-life balance: {workLife}</label>
        <input
          id="workLife"
          type="range"
          min="0"
          max="100"
          value={workLife}
          onChange={(event) => setWorkLife(Number(event.target.value))}
        />

        <label htmlFor="culture">Desired culture: {culture}</label>
        <input
          id="culture"
          type="range"
          min="0"
          max="100"
          value={culture}
          onChange={(event) => setCulture(Number(event.target.value))}
        />

        <label htmlFor="career">Desired career opportunities: {career}</label>
        <input
          id="career"
          type="range"
          min="0"
          max="100"
          value={career}
          onChange={(event) => setCareer(Number(event.target.value))}
        />

        <button type="submit">Generate Recommendations</button>
      </form>

      <section className="recommendation-results">
        <h2>Recommended Companies</h2>

        {results.length === 0 ? (
          <p>Set your preferences and click Generate Recommendations.</p>
        ) : (
          <div className="company-grid">
            {results.map((company) => (
              <article className="company-card" key={company.name}>
                <h3>{company.name}</h3>
                <p>Recommendation score: {company.recommendationScore}/100</p>
                <p>Company intelligence: {company.score}/100</p>
                <p>Preference match: {company.preferenceScore}/100</p>
                <p>{company.reason}</p>
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
