import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import "./App.css";

function Dashboard() {
  return (
    <div>
      <h1 className="page-title">Welcome to WorkSphere</h1>
      <p className="page-subtitle">
        Your AI-powered career intelligence platform
      </p>

      <div className="card-container">
        <div className="card">
          <h3>Resume Score</h3>
          <div className="card-value">86%</div>
        </div>

        <div className="card">
          <h3>Recommended Companies</h3>
          <div className="card-value">12</div>
        </div>

        <div className="card">
          <h3>Skills Matched</h3>
          <div className="card-value">18</div>
        </div>
      </div>

      <div className="section">
        <h2>Recommended Companies</h2>

        <div className="company-grid">
          <div className="company-card">
            <h3>Microsoft</h3>
            <p>Technology</p>
            <p>Culture Score: 4.5/5</p>
            <button>View Details</button>
          </div>

          <div className="company-card">
            <h3>Google</h3>
            <p>Technology</p>
            <p>Culture Score: 4.6/5</p>
            <button>View Details</button>
          </div>

          <div className="company-card">
            <h3>Adobe</h3>
            <p>Technology</p>
            <p>Culture Score: 4.4/5</p>
            <button>View Details</button>
          </div>
        </div>
      </div>
    </div>
  );
}

function Companies() {
  return (
    <div>
      <h1 className="page-title">Companies</h1>
      <p className="page-subtitle">
        Explore companies based on culture, work-life balance and career opportunities.
      </p>

      <input
        type="text"
        className="search-box"
        placeholder="Search companies..."
      />

      <div className="company-grid">
        <div className="company-card">
          <h3>Microsoft</h3>
          <p>Technology</p>
          <p>Overall Rating: 4.5/5</p>
          <button>View Details</button>
        </div>

        <div className="company-card">
          <h3>Google</h3>
          <p>Technology</p>
          <p>Overall Rating: 4.6/5</p>
          <button>View Details</button>
        </div>

        <div className="company-card">
          <h3>Adobe</h3>
          <p>Technology</p>
          <p>Overall Rating: 4.4/5</p>
          <button>View Details</button>
        </div>
      </div>
    </div>
  );
}

function Recommendations() {
  return (
    <div>
      <h1 className="page-title">Recommendations</h1>
      <p className="page-subtitle">
        Companies and roles matched to your skills and preferences.
      </p>

      <div className="section">
        <h2>Top Recommendations</h2>
        <p>Personalized recommendations will appear here.</p>
      </div>
    </div>
  );
}

function ResumeAnalysis() {
  return (
    <div>
      <h1 className="page-title">Resume Analysis</h1>
      <p className="page-subtitle">
        Upload your resume to analyze your skills and profile.
      </p>

      <div className="section">
        <h2>Resume Upload</h2>
        <input type="file" />
        <br />
        <br />
        <button>Analyze Resume</button>
      </div>
    </div>
  );
}

function SkillGap() {
  return (
    <div>
      <h1 className="page-title">Skill Gap Analysis</h1>
      <p className="page-subtitle">
        Identify missing skills for your target role.
      </p>

      <div className="section">
        <h2>Target Role</h2>

        <input
          type="text"
          className="search-box"
          placeholder="Enter target role..."
        />

        <h3>Matched Skills</h3>

        <div className="skill-list">
          <span className="skill">Python</span>
          <span className="skill">SQL</span>
          <span className="skill">Machine Learning</span>
        </div>

        <br />

        <h3>Missing Skills</h3>

        <div className="skill-list">
          <span className="skill">Docker</span>
          <span className="skill">AWS</span>
        </div>
      </div>
    </div>
  );
}

function Compare() {
  return (
    <div>
      <h1 className="page-title">Compare Companies</h1>
      <p className="page-subtitle">
        Compare companies across different career factors.
      </p>

      <div className="section">
        <h2>Company Comparison</h2>
        <p>Select companies to compare their ratings and insights.</p>
      </div>
    </div>
  );
}

function AIAssistant() {
  return (
    <div>
      <h1 className="page-title">AI Assistant</h1>
      <p className="page-subtitle">
        Ask questions about companies, jobs and your career.
      </p>

      <div className="chat-container">
        <p>How can I help you with your career?</p>

        <input
          type="text"
          className="chat-input"
          placeholder="Ask something..."
        />

        <br />
        <br />

        <button>Send</button>
      </div>
    </div>
  );
}

function Profile() {
  return (
    <div>
      <h1 className="page-title">Profile</h1>
      <p className="page-subtitle">
        Manage your skills, preferences and career goals.
      </p>

      <div className="section">
        <h2>Career Profile</h2>
        <p><strong>Name:</strong> User</p>
        <p><strong>Skills:</strong> Python, Java, SQL, Machine Learning</p>
        <p><strong>Career Goal:</strong> Software / AI Engineer</p>
      </div>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="app">

        <Sidebar />

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/companies" element={<Companies />} />
            <Route path="/recommendations" element={<Recommendations />} />
            <Route path="/resume-analysis" element={<ResumeAnalysis />} />
            <Route path="/skill-gap" element={<SkillGap />} />
            <Route path="/compare" element={<Compare />} />
            <Route path="/ai-assistant" element={<AIAssistant />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </main>

      </div>
    </BrowserRouter>
  );
}

export default App;