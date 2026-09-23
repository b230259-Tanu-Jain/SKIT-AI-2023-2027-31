import React from "react";
function Navbar() {
  return (
    <header className="navbar">

      <div>
        <h2>WorkSphere</h2>
      </div>

      <div className="navbar-right">
        <span>Welcome, User</span>
        <button>Profile</button>
      </div>

    </header>
  );
}

export default Navbar;