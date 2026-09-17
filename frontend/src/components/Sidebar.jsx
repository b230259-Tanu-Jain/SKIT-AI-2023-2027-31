import React from "react";
import { Link, useLocation } from "react-router-dom";

function Sidebar() {
  const location = useLocation();

  const menuItems = [
    { name: "Dashboard", path: "/" },
    { name: "Companies", path: "/companies" },
    { name: "Recommendations", path: "/recommendations" },
    { name: "Resume Analysis", path: "/resume-analysis" },
    { name: "Skill Gap", path: "/skill-gap" },
    { name: "Compare", path: "/compare" },
    { name: "AI Assistant", path: "/ai-assistant" },
    { name: "Profile", path: "/profile" }
  ];

  return (
    <aside className="sidebar">

      <div className="logo">
        WorkSphere
      </div>

      <nav className="nav-menu">

        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={
              location.pathname === item.path
                ? "nav-link active"
                : "nav-link"
            }
          >
            {item.name}
          </Link>
        ))}

      </nav>

    </aside>
  );
}

export default Sidebar;