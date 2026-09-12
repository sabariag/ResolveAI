import { useState } from "react";
import { resolveCustomerIssue } from "./services/api";

const workflow = [
  ["01", "Understand", "Identify customer intent"],
  ["02", "Investigate", "Retrieve customer & order data"],
  ["03", "Evaluate", "Check policy & constraints"],
  ["04", "Decide", "Select the best resolution"],
  ["05", "Execute", "Perform the required action"],
  ["06", "Verify", "Confirm the final outcome"],
];

function App() {
  const [issue, setIssue] = useState("");
  const [status, setStatus] = useState("idle");
  const [step, setStep] = useState(-1);

  const handleResolve = async () => {
    if (!issue.trim()) {
      setStatus("error");
      return;
    }

    setStatus("loading");
    setStep(0);

    const timer = setInterval(() => {
      setStep((prev) => {
        if (prev >= workflow.length - 1) {
          clearInterval(timer);
          return prev;
        }
        return prev + 1;
      });
    }, 650);

    try {
      await resolveCustomerIssue(issue);

      clearInterval(timer);
      setStep(workflow.length - 1);

      setTimeout(() => {
        setStatus("success");
      }, 500);
    } catch {
      clearInterval(timer);
      setStatus("error");
    }
  };

  const reset = () => {
    setIssue("");
    setStep(-1);
    setStatus("idle");
  };

  return (
    <div className="resolve-app">

      {/* SIDEBAR */}

      <aside className="sidebar">

        <div className="side-logo">
          <div className="logo-mark">R</div>
          <div>
            <strong>ResolveAI</strong>
            <span>Agent Platform</span>
          </div>
        </div>

        <nav>
          <div className="nav-item active">
            <span>⌂</span>
            Resolution Center
          </div>

          <div className="nav-item">
            <span>◈</span>
            Agent Activity
          </div>

          <div className="nav-item">
            <span>▣</span>
            Customer Cases
          </div>

          <div className="nav-item">
            <span>⚙</span>
            Settings
          </div>
        </nav>

        <div className="side-bottom">
          <div className="system-status">
            <span className="live-dot"></span>

            <div>
              <strong>All systems operational</strong>
              <small>Agent infrastructure online</small>
            </div>
          </div>
        </div>

      </aside>


      {/* MAIN */}

      <div className="main-area">

        {/* TOPBAR */}

        <header className="topbar">

          <div>
            <span className="breadcrumb">AI AGENT /</span>
            <strong> Resolution Center</strong>
          </div>

          <div className="top-actions">
            <span className="live-pill">
              <i></i> LIVE
            </span>

            <div className="avatar">RA</div>
          </div>

        </header>


        {/* HERO */}

        <section className="hero-section">

          <div className="hero-copy">

            <div className="ai-badge">
              <span>✦</span>
              AUTONOMOUS AI AGENT
            </div>

            <h1>
              Resolve issues.
              <br />
              <em>Automatically.</em>
            </h1>

            <p>
              ResolveAI investigates customer requests, reasons over
              enterprise data, executes actions and verifies the outcome.
            </p>

          </div>

          <div className="hero-orb">
            <div className="orb-ring ring-one"></div>
            <div className="orb-ring ring-two"></div>
            <div className="orb-core">
              <span>✦</span>
            </div>
          </div>

        </section>


        {/* METRICS */}

        <section className="metrics">

          <div className="metric">
            <span>AGENT STATUS</span>
            <strong className="green-text">● ONLINE</strong>
          </div>

          <div className="metric">
            <span>ACTIVE CASE</span>
            <strong>{status === "idle" ? "—" : "CASE-10245"}</strong>
          </div>

          <div className="metric">
            <span>DECISION MODE</span>
            <strong>Autonomous</strong>
          </div>

          <div className="metric">
            <span>VERIFICATION</span>
            <strong>Required</strong>
          </div>

        </section>


        {/* REQUEST */}

        <section className="workspace">

          <div className="request-panel">

            <div className="panel-header">

              <div>
                <span className="panel-label">01 / CUSTOMER INPUT</span>
                <h2>What happened?</h2>
              </div>

              <div className="panel-number">01</div>

            </div>

            <p>
              Describe the customer's problem in natural language.
              The agent will determine what needs to be done.
            </p>

            <div className="input-wrapper">

              <textarea
                value={issue}
                onChange={(e) => setIssue(e.target.value)}
                disabled={status === "loading"}
                placeholder="My headphones arrived damaged. I want a replacement..."
              />

              <div className="input-hint">
                <span>AI understands natural language</span>
                <span>{issue.length} characters</span>
              </div>

            </div>

            <button
              className="resolve-btn"
              onClick={handleResolve}
              disabled={status === "loading"}
            >
              <span>
                {status === "loading"
                  ? "Agent working..."
                  : "Start autonomous resolution"}
              </span>

              <b>→</b>
            </button>

          </div>


          {/* AGENT BRAIN */}

          <div className="agent-panel">

            <div className="panel-header">

              <div>
                <span className="panel-label">02 / AGENT BRAIN</span>
                <h2>Decision pipeline</h2>
              </div>

              <div className="thinking">
                <span></span>
                {status === "loading" ? "THINKING" : "READY"}
              </div>

            </div>

            <div className="pipeline">

              {workflow.map((item, index) => {

                const complete =
                  status === "success" || index < step;

                const active =
                  status === "loading" && index === step;

                return (
                  <div
                    className={`pipeline-item ${
                      complete ? "complete" : ""
                    } ${active ? "current" : ""}`}
                    key={item[0]}
                  >

                    <div className="pipeline-line">

                      <div className="pipeline-circle">
                        {complete ? "✓" : item[0]}
                      </div>

                    </div>

                    <div className="pipeline-content">

                      <strong>{item[1]}</strong>

                      <span>{item[2]}</span>

                      {active && (
                        <small>Agent is processing...</small>
                      )}

                    </div>

                  </div>
                );
              })}

            </div>

          </div>

        </section>


        {/* EVIDENCE */}

        <section className="evidence-section">

          <div className="section-heading">

            <div>
              <span className="panel-label">03 / REASONING CONTEXT</span>
              <h2>Evidence collected</h2>
            </div>

            <span className="source-count">
              {status === "idle" ? "Awaiting request" : "4 sources"}
            </span>

          </div>


          <div className="evidence-grid">

            <div className="evidence-card">
              <div className="e-icon">👤</div>
              <div>
                <span>CRM</span>
                <strong>Customer profile</strong>
                <small>
                  Identity & account information
                </small>
              </div>
              <b>✓</b>
            </div>

            <div className="evidence-card">
              <div className="e-icon">📦</div>
              <div>
                <span>ORDERS</span>
                <strong>Order information</strong>
                <small>
                  Product & purchase details
                </small>
              </div>
              <b>✓</b>
            </div>

            <div className="evidence-card">
              <div className="e-icon">📋</div>
              <div>
                <span>RAG / POLICY</span>
                <strong>Resolution policy</strong>
                <small>
                  Eligibility & constraints
                </small>
              </div>
              <b>✓</b>
            </div>

            <div className="evidence-card">
              <div className="e-icon">🏭</div>
              <div>
                <span>INVENTORY</span>
                <strong>Availability</strong>
                <small>
                  Warehouse stock information
                </small>
              </div>
              <b>✓</b>
            </div>

          </div>

        </section>


        {/* FINAL RESULT */}

        <section className="result-section">

          <div className="section-heading">

            <div>
              <span className="panel-label">04 / FINAL OUTCOME</span>
              <h2>Resolution</h2>
            </div>

            {status === "success" && (
              <span className="verified">
                ✓ VERIFIED
              </span>
            )}

          </div>


          {status === "idle" && (

            <div className="result-empty">

              <div className="empty-orb">✦</div>

              <h3>Agent ready</h3>

              <p>
                Submit a customer issue to begin autonomous investigation.
              </p>

            </div>

          )}


          {status === "loading" && (

            <div className="result-loading">

              <div className="loader-ring"></div>

              <div>
                <span>AI AGENT ACTIVE</span>
                <h3>Investigating customer issue...</h3>
                <p>
                  Retrieving information, evaluating constraints and
                  selecting the best action.
                </p>
              </div>

            </div>

          )}


          {status === "success" && (

            <div className="success-result">

              <div className="success-main">

                <div className="success-symbol">
                  ✓
                </div>

                <div>
                  <span>RESOLUTION VERIFIED</span>
                  <h3>Replacement successfully processed</h3>
                  <p>
                    ResolveAI completed the requested action and
                    verified the final outcome.
                  </p>
                </div>

              </div>

              <div className="result-data">

                <div>
                  <span>ACTION</span>
                  <strong>Replacement</strong>
                </div>

                <div>
                  <span>ORDER</span>
                  <strong>ORD-10245</strong>
                </div>

                <div>
                  <span>DECISION</span>
                  <strong>Autonomous</strong>
                </div>

                <div>
                  <span>STATUS</span>
                  <strong className="green-text">Confirmed</strong>
                </div>

              </div>

              <button className="new-case" onClick={reset}>
                + Start new case
              </button>

            </div>

          )}


          {status === "error" && (

            <div className="error-result">

              <div>!</div>

              <section>
                <span>AGENT ERROR</span>
                <h3>Unable to resolve this request</h3>
                <p>
                  Please provide a customer issue and try again.
                </p>
              </section>

            </div>

          )}

        </section>


        <footer>
          <span>ResolveAI</span>
          <span>Autonomous Customer Resolution Agent</span>
          <span>Agentic AI • RAG • Enterprise Tools</span>
        </footer>

      </div>

    </div>
  );
}

export default App;