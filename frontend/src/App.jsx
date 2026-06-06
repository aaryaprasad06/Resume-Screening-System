import { useState, useRef } from "react";
import axios from "axios";
import "./App.css";

const API = "http://localhost:8000";

function ScoreRing({ score }) {
  const r = 26;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  const color =
    score >= 75 ? "#4ade80" : score >= 50 ? "#fbbf24" : "#f87171";

  return (
    <svg
      width="68"
      height="68"
      viewBox="0 0 68 68"
      style={{ flexShrink: 0, display: "block" }}
    >
      <circle
        cx="34" cy="34" r={r}
        stroke="#1e1e28" strokeWidth="5" fill="none"
      />
      <circle
        cx="34" cy="34" r={r}
        stroke={color} strokeWidth="5" fill="none"
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 34 34)"
        style={{ transition: "stroke-dasharray 0.9s ease" }}
      />
      <text
        x="34" y="30"
        textAnchor="middle"
        fill={color}
        fontSize="13"
        fontWeight="700"
        fontFamily="DM Sans, sans-serif"
      >
        {score}%
      </text>
      <text
        x="34" y="44"
        textAnchor="middle"
        fill="#7a7889"
        fontSize="9"
        fontFamily="DM Sans, sans-serif"
      >
        match
      </text>
    </svg>
  );
}

function CandidateCard({ candidate, rank, isOpen, onToggle }) {
  const score = candidate.match_score;
  const tier =
    score >= 75 ? "strong-match" : score >= 50 ? "mid-match" : "weak-match";

  const strengths = Array.isArray(candidate.strengths) ? candidate.strengths : [];
  const weaknesses = Array.isArray(candidate.weaknesses) ? candidate.weaknesses : [];
  const questions = Array.isArray(candidate.interview_questions)
    ? candidate.interview_questions
    : [];

  return (
    <div className={`candidate-card ${tier} ${isOpen ? "open" : ""}`}>
      <button className="card-header" onClick={onToggle} type="button">
        <span className="rank-badge">#{rank}</span>

        <div className="card-meta">
          <span className="candidate-name">
            {candidate.filename.replace(/\.pdf$/i, "")}
          </span>
          <span className="candidate-summary-short">{candidate.summary}</span>
        </div>

        <ScoreRing score={score} />

        <span className="chevron">{isOpen ? "▲" : "▼"}</span>
      </button>

      {isOpen && (
        <div className="card-body">
          <div className="two-col">
            <div className="detail-section strengths-section">
              <h4>✦ Strengths</h4>
              <ul>
                {strengths.length > 0
                  ? strengths.map((s, i) => <li key={i}>{s}</li>)
                  : <li className="empty-item">None identified</li>}
              </ul>
            </div>

            <div className="detail-section weaknesses-section">
              <h4>✦ Weaknesses</h4>
              <ul>
                {weaknesses.length > 0
                  ? weaknesses.map((w, i) => <li key={i}>{w}</li>)
                  : <li className="empty-item">None identified</li>}
              </ul>
            </div>
          </div>

          {questions.length > 0 && (
            <div className="detail-section questions-section">
              <h4>✦ Suggested Interview Questions</h4>
              <ol>
                {questions.map((q, i) => (
                  <li key={i}>{q}</li>
                ))}
              </ol>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function App() {
  const [jobDescription, setJobDescription] = useState("");
  const [files, setFiles] = useState([]);
  const [candidates, setCandidates] = useState([]);
  const [openIndex, setOpenIndex] = useState(null);
  const [stage, setStage] = useState("idle");
  const [errorMsg, setErrorMsg] = useState("");
  const fileInputRef = useRef();

  const handleFiles = (incoming) => {
    const pdfs = Array.from(incoming).filter(
      (f) => f.type === "application/pdf" || f.name.toLowerCase().endsWith(".pdf")
    );
    setFiles((prev) => {
      const existing = new Set(prev.map((f) => f.name));
      return [...prev, ...pdfs.filter((f) => !existing.has(f.name))];
    });
  };

  const removeFile = (name) =>
    setFiles((prev) => prev.filter((f) => f.name !== name));

  const handleDrop = (e) => {
    e.preventDefault();
    handleFiles(e.dataTransfer.files);
  };

  const handleAnalyze = async () => {
    if (!jobDescription.trim()) return alert("Please enter a job description.");
    if (files.length === 0) return alert("Please upload at least one resume.");

    try {
      setStage("uploading");
      setCandidates([]);
      setOpenIndex(null);

      const formData = new FormData();
      files.forEach((f) => formData.append("files", f));

      const uploadRes = await axios.post(`${API}/upload-resumes`, formData);
      const resumes = uploadRes.data.resumes;

      setStage("ranking");

      const rankRes = await axios.post(`${API}/rank-candidates`, {
        job_description: jobDescription,
        resumes,
      });

      // Backend already sorts by match_score descending — trust it
      const ranked = rankRes.data.candidates;
      setCandidates(ranked);
      setStage("done");
    } catch (err) {
      console.error(err);
      setErrorMsg(
        err?.response?.data?.detail || err?.message || "Something went wrong."
      );
      setStage("error");
    }
  };

  const busy = stage === "uploading" || stage === "ranking";

  return (
    <div
      className="app"
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
    >
      <div className="mesh-bg" />

      {/* NAV */}
      <nav className="navbar">
        <div className="logo">
          <span className="logo-mark">H</span>
          <span>HireMind</span>
          <span className="logo-tag">AI</span>
        </div>
        <div className="nav-pill">Candidate Screener</div>
      </nav>

      {/* HERO */}
      <header className="hero">
        <p className="hero-eyebrow">Intelligent Hiring</p>
        <h1>
          Find your best candidates,<br />
          <em>instantly.</em>
        </h1>
        <p className="hero-sub">
          Upload multiple resumes, describe the role, and let AI rank, score,
          and dissect every candidate for you.
        </p>
      </header>

      {/* WORKSPACE */}
      <main className="workspace">
        {/* LEFT */}
        <div className="pane left-pane">
          <section className="card">
            <div className="card-label">Job Description</div>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the full job description here — requirements, responsibilities, preferred skills…"
              rows={10}
            />
          </section>

          <section className="card upload-card">
            <div className="card-label">Resumes</div>

            <div
              className="dropzone"
              onClick={() => fileInputRef.current.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                multiple
                style={{ display: "none" }}
                onChange={(e) => handleFiles(e.target.files)}
              />
              <span className="drop-icon">⬆</span>
              <p>
                Drop PDFs here or <u>browse</u>
              </p>
              <span className="drop-hint">Multiple files supported</span>
            </div>

            {files.length > 0 && (
              <ul className="file-list">
                {files.map((f) => (
                  <li key={f.name}>
                    <span className="file-icon">📄</span>
                    <span className="file-name">{f.name}</span>
                    <button
                      className="remove-btn"
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        removeFile(f.name);
                      }}
                    >
                      ✕
                    </button>
                  </li>
                ))}
              </ul>
            )}

            <button
              className="cta-btn"
              type="button"
              onClick={handleAnalyze}
              disabled={busy}
            >
              {busy
                ? stage === "uploading"
                  ? "Uploading resumes…"
                  : "Ranking candidates…"
                : `Rank ${files.length > 0 ? files.length + " " : ""}Candidate${files.length !== 1 ? "s" : ""}`}
            </button>
          </section>
        </div>

        {/* RIGHT */}
        <div className="pane right-pane">
          <section className="card results-card">
            <div className="card-label">
              <span>Results</span>
              {candidates.length > 0 && (
                <span className="result-count">
                  {candidates.length} candidates
                </span>
              )}
            </div>

            {stage === "idle" && (
              <div className="placeholder">
                <div className="placeholder-icon">◎</div>
                <p>Your ranked candidates will appear here.</p>
              </div>
            )}

            {busy && (
              <div className="loading-state">
                <div className="pulse-ring" />
                <p>
                  {stage === "uploading"
                    ? "Extracting text from PDFs…"
                    : "AI is scoring every candidate…"}
                </p>
              </div>
            )}

            {stage === "error" && (
              <div className="error-state">
                <p>⚠ {errorMsg}</p>
                <button
                  className="retry-btn"
                  type="button"
                  onClick={() => setStage("idle")}
                >
                  Retry
                </button>
              </div>
            )}

            {stage === "done" && candidates.length === 0 && (
              <div className="placeholder">
                <p>No results returned.</p>
              </div>
            )}

            {stage === "done" && candidates.length > 0 && (
              <div className="candidate-list">
                {candidates.map((c, i) => (
                  <CandidateCard
                    key={c.filename}
                    candidate={c}
                    rank={i + 1}
                    isOpen={openIndex === i}
                    onToggle={() =>
                      setOpenIndex(openIndex === i ? null : i)
                    }
                  />
                ))}
              </div>
            )}
          </section>
        </div>
      </main>
    </div>
  );
}