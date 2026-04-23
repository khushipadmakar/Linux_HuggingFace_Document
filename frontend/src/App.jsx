import React from "react";
import { HashRouter, NavLink, Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Documents from "./pages/Documents";
import Search from "./pages/Search";
import QA from "./pages/QA";

class AppErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, message: "" };
  }

  static getDerivedStateFromError(error) {
    return {
      hasError: true,
      message: error instanceof Error ? error.message : "Unknown render error",
    };
  }

  render() {
    if (this.state.hasError) {
      return (
        <section className="panel">
          <h2>Frontend Error</h2>
          <p className="error">
            UI render karte waqt issue aaya: {this.state.message}
          </p>
          <p className="hint">
            DevTools console kholke exact stack dekh sakte ho. Ab blank screen
            nahi aayegi.
          </p>
        </section>
      );
    }

    return this.props.children;
  }
}

function App() {
  console.log("App mounted");
  const navClass = ({ isActive }) => (isActive ? "active" : "");

  return (
    <HashRouter>
      <AppErrorBoundary>
        <div className="layout">
          <header className="topbar">
            <h1>AI Document Intelligence</h1>
            <nav>
              <NavLink className={navClass} to="/">
                Dashboard
              </NavLink>
              <NavLink className={navClass} to="/documents">
                Documents
              </NavLink>
              <NavLink className={navClass} to="/search">
                Semantic Search
              </NavLink>
              <NavLink className={navClass} to="/qa">
                Q&A
              </NavLink>
            </nav>
          </header>

          <main className="page-shell">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/documents" element={<Documents />} />
              <Route path="/search" element={<Search />} />
              <Route path="/qa" element={<QA />} />
            </Routes>
          </main>
        </div>
      </AppErrorBoundary>
    </HashRouter>
  );
}

export default App;
