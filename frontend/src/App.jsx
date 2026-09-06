import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import "./App.css";

function Sidebar() {
  return (
    <aside className="sidebar">
      <h2>WorkSphere</h2>

      <nav>
        <Link to="/">Dashboard</Link>
        <Link to="/companies">Companies</Link>
        <Link to="/resume">Resume Analysis</Link>
        <Link to="/recommendations">Recommendations</Link>
        <Link to="/compare">Compare</Link>
        <Link to="/assistant">AI Assistant</Link>
        <Link to="/profile">Profile</Link>
      </nav>

      <Link to="/login">Logout</Link>
    </aside>
  );
}

function Dashboard() {
  return (
    <main className="page">
      <h1>Welcome back, Tanu!</h1>
      <p>Here&apos;s an overview of your career journey.</p>

      <div className="stats">

        <div className="card">
          <span>Resume Score</span>
          <h2>86%</h2>
          <small>Good Score</small>
        </div>

        <div className="card">
          <span>Companies Matched</span>
          <h2>24</h2>
          <small>High Match</small>
        </div>

        <div className="card">
          <span>Skills Detected</span>
          <h2>18</h2>
          <small>Strong Skills</small>
        </div>

        <div className="card">
          <span>Saved Companies</span>
          <h2>12</h2>
          <small>Saved companies</small>
        </div>

      </div>

      <div className="content">

        <section className="panel">
          <h2>Recommended Companies</h2>

          <div className="company">
            <h3>Microsoft</h3>
            <p>Rating: ★ 4.6</p>
            <span>93% Match</span>
          </div>

          <div className="company">
            <h3>Google</h3>
            <p>Rating: ★ 4.5</p>
            <span>92% Match</span>
          </div>

          <div className="company">
            <h3>Adobe</h3>
            <p>Rating: ★ 4.4</p>
            <span>90% Match</span>
          </div>

        </section>

        <section className="panel resume">
          <h2>Your Resume Score</h2>
          <div className="score">86%</div>
          <p>Good Score</p>
          <Link to="/resume">View Full Analysis</Link>
        </section>

      </div>

      <section className="panel">
        <h2>Recent Searches</h2>

        <div className="searches">
          <span>Data Scientist</span>
          <span>Machine Learning Engineer</span>
          <span>Microsoft</span>
          <span>Google</span>
          <span>Product Manager</span>
        </div>
      </section>

    </main>
  );
}

function Page({ title }) {
  return (
    <main className="page">
      <h1>{title}</h1>
      <p>This page will be connected to the WorkSphere backend later.</p>
    </main>
  );
}

function App() {
  return (
    <BrowserRouter>

      <div className="app">

        <Sidebar />

        <Routes>

          <Route path="/" element={<Dashboard />} />

          <Route
            path="/companies"
            element={<Page title="Companies" />}
          />

          <Route
            path="/resume"
            element={<Page title="Resume Analysis" />}
          />

          <Route
            path="/recommendations"
            element={<Page title="Recommendations" />}
          />

          <Route
            path="/compare"
            element={<Page title="Compare Companies" />}
          />

          <Route
            path="/assistant"
            element={<Page title="AI Assistant" />}
          />

          <Route
            path="/profile"
            element={<Page title="Profile" />}
          />

          <Route
            path="/login"
            element={<Page title="Login" />}
          />

        </Routes>

      </div>

    </BrowserRouter>
  );
}

export default App;