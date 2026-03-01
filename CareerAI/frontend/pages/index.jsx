import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import Head from 'next/head'

export default function Home() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [formData, setFormData] = useState({ technicalSkills: '', cgpa: '', githubUsername: '' })
  const canvasRef = useRef(null)

  /* ── Particle canvas ── */
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')

    function resize() {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    resize()
    window.addEventListener('resize', resize)

    const PALETTE = ['124,58,237', '168,85,247', '59,130,246', '236,72,153']
    const rand = (a, b) => Math.random() * (b - a) + a

    class Dot {
      constructor() { this.reset() }
      reset() {
        this.x = rand(0, canvas.width)
        this.y = rand(0, canvas.height)
        this.r = rand(0.5, 2.2)
        this.vx = rand(-0.18, 0.18)
        this.vy = rand(-0.22, -0.04)
        this.a = rand(0.15, 0.5)
        this.c = PALETTE[Math.floor(rand(0, 4))]
      }
      draw() {
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(${this.c},${this.a})`
        ctx.fill()
      }
      update() {
        this.x += this.vx; this.y += this.vy
        if (this.y < -4 || this.x < -4 || this.x > canvas.width + 4) this.reset()
      }
    }

    const dots = Array.from({ length: 80 }, () => new Dot())
    let raf
    const loop = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      dots.forEach(d => { d.update(); d.draw() })
      raf = requestAnimationFrame(loop)
    }
    loop()

    return () => { cancelAnimationFrame(raf); window.removeEventListener('resize', resize) }
  }, [])

  /* ── Scroll-reveal ── */
  useEffect(() => {
    const els = document.querySelectorAll('.reveal')
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible') })
    }, { threshold: 0.1 })
    els.forEach(el => io.observe(el))
    return () => io.disconnect()
  }, [])

  /* ── Form submit ── */
  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const skills = formData.technicalSkills.split(',').map(s => s.trim()).filter(Boolean)
      const cgpa = parseFloat(formData.cgpa) || 7.0
      const res = await axios.post('http://localhost:8000/predict-career', {
        profile: { technical_skills: skills, cgpa, soft_skills: [], certifications: [], internships: [], projects: [] },
        github_data: formData.githubUsername ? { github_username: formData.githubUsername } : null
      })
      setResults(res.data)
      setTimeout(() => document.getElementById('results-area')?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100)
    } catch (err) {
      console.error(err)
      alert('Could not reach the API. Make sure backend is running on localhost:8000.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Head>
        <title>CareerAI — Intelligent Career Path Prediction</title>
        <meta name="description" content="AI-powered career predictions, salary insights, skill gap analysis, and personalized roadmaps." />
      </Head>

      {/* Canvas */}
      <canvas ref={canvasRef} style={{ position:'fixed', inset:0, width:'100%', height:'100%', pointerEvents:'none', zIndex:0 }} />

      {/* Ambient blobs */}
      <div className="blob blob-1" />
      <div className="blob blob-2" />
      <div className="blob blob-3" />

      <div style={{ position:'relative', zIndex:1 }}>

        {/* ── Navbar ── */}
        <nav className="c-nav">
          <a href="#" className="c-brand">
            <div className="c-logo-box">🎯</div>
            <span className="c-brand-name">CareerAI</span>
          </a>
          <ul className="c-nav-links">
            <li><a href="#features">Features</a></li>
            <li><a href="#predict">Predict</a></li>
            <li><a href="#about">About</a></li>
          </ul>
          <a href="#predict" className="c-cta">Get Started →</a>
        </nav>

        {/* ── Hero ── */}
        <section className="c-hero">
          <div className="c-badge animate-fadeIn">
            <span className="c-dot" />
            AI-Powered Career Intelligence
          </div>

          <h1 className="c-hero-h1 animate-fadeIn" style={{ animationDelay:'.12s' }}>
            Discover Your<br />
            <span className="grad-text">Perfect Career Path</span>
          </h1>

          <p className="c-hero-sub animate-fadeIn" style={{ animationDelay:'.25s' }}>
            Get AI-powered career predictions, salary insights, skill gap analysis, and personalized roadmaps — all tailored to your unique skills and GitHub profile.
          </p>

          <div className="c-hero-actions animate-fadeIn" style={{ animationDelay:'.38s' }}>
            <button
              onClick={() => document.getElementById('predict')?.scrollIntoView({ behavior:'smooth' })}
              className="c-btn-primary"
            >
              <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
              Start Prediction
            </button>
            <a href="#features" className="c-btn-ghost">Explore Features</a>
          </div>
        </section>

        {/* ── Stats ── */}
        <div className="c-stats reveal">
          {[['10+','Career Tracks'],['95%','Prediction Accuracy'],['5k+','Profiles Analyzed'],['3s','Avg Response']].map(([v,l]) => (
            <div key={l} className="c-stat">
              <div className="c-stat-val">{v}</div>
              <div className="c-stat-lbl">{l}</div>
            </div>
          ))}
        </div>

        {/* ── Features ── */}
        <section id="features" className="c-section">
          <div className="c-section-hdr reveal">
            <span className="c-section-label">What we offer</span>
            <h2 className="c-section-title">Powerful Features,<br />Built for Your Growth</h2>
            <p className="c-section-sub">Everything you need to navigate your career journey with confidence.</p>
          </div>

          <div className="c-feat-grid reveal">
            {[
              { icon:'🔮', color:'purple', title:'Career Prediction',    desc:'AI classification into 10+ tracks with confidence scores and ranked alternatives.' },
              { icon:'💰', color:'green',  title:'Salary Insights',      desc:'Entry-level and 5-year projections calculated from real market data and your skills.' },
              { icon:'🗺️', color:'blue',   title:'Personalized Roadmap', desc:'3, 6, and 12-month plans with curated projects, certs, and learning resources.' },
              { icon:'📊', color:'amber',  title:'Skill Gap Analysis',   desc:'Pinpoint missing skills for your target role with prioritized recommendations.' },
              { icon:'🐙', color:'pink',   title:'GitHub Integration',   desc:'Auto-analyze your repos and activity to enrich your profile with real evidence.' },
              { icon:'⚡', color:'teal',   title:'Job Readiness Score',  desc:'A composite 0–100 score showing how market-ready you are right now.' },
            ].map(f => (
              <div key={f.title} className={`c-feat-card glass feat-${f.color}`}>
                <div className={`c-feat-icon icon-${f.color}`}>{f.icon}</div>
                <h4 className="c-feat-title">{f.title}</h4>
                <p className="c-feat-desc">{f.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* ── Prediction Form ── */}
        <section id="predict" className="c-section c-predict-bg">
          <div className="c-predict-wrap">
            <div className="c-section-hdr reveal">
              <span className="c-section-label">Try it now</span>
              <h2 className="c-section-title">Get Your Career Prediction</h2>
              <p className="c-section-sub">Fill in your profile — results in under 5 seconds.</p>
            </div>

            <div className="c-form-card reveal">
              <form onSubmit={handleSubmit}>
                <div className="c-form-grid">
                  <div className="c-fg c-full">
                    <label htmlFor="ts">Technical Skills</label>
                    <input
                      id="ts" type="text" className="c-input"
                      placeholder="python, javascript, machine_learning, react…"
                      value={formData.technicalSkills}
                      onChange={e => setFormData({ ...formData, technicalSkills: e.target.value })}
                    />
                    <span className="c-hint">Separate each skill with a comma.</span>
                  </div>

                  <div className="c-fg">
                    <label htmlFor="cgpa">CGPA / GPA</label>
                    <input
                      id="cgpa" type="number" className="c-input"
                      placeholder="e.g. 8.5" step="0.1" min="0" max="10"
                      value={formData.cgpa}
                      onChange={e => setFormData({ ...formData, cgpa: e.target.value })}
                    />
                    <span className="c-hint">Scale 0–10</span>
                  </div>

                  <div className="c-fg">
                    <label htmlFor="gh">GitHub Username <span className="c-opt">(optional)</span></label>
                    <input
                      id="gh" type="text" className="c-input"
                      placeholder="octocat"
                      value={formData.githubUsername}
                      onChange={e => setFormData({ ...formData, githubUsername: e.target.value })}
                    />
                    <span className="c-hint">Enhances accuracy.</span>
                  </div>

                  <div className="c-fg c-full">
                    <button type="submit" className="c-submit" disabled={loading}>
                      {loading
                        ? <><span className="c-spinner" /> Analyzing your profile…</>
                        : '🚀  Analyze My Profile'
                      }
                    </button>
                  </div>
                </div>
              </form>

              {/* Results */}
              {results && (
                <div id="results-area" className="c-results animate-fadeIn">

                  {/* Career Prediction */}
                  <div className="r-card r-purple">
                    <h4 className="r-title">🎯 Career Prediction</h4>
                    <div className="r-career-name">{results.career_prediction}</div>
                    <div className="r-confidence">
                      Confidence:&nbsp;
                      <strong style={{ color:'#c4b5fd' }}>{(results.confidence * 100).toFixed(1)}%</strong>
                    </div>
                    {results.alternative_careers?.length > 0 && (
                      <div style={{ marginTop:16 }}>
                        <p className="r-alt-label">Alternatives</p>
                        <div>
                          {results.alternative_careers.slice(0, 3).map(a => (
                            <span key={a.career} className="tag tag-purple">
                              {a.career} · {(a.confidence * 100).toFixed(0)}%
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Salary + Readiness */}
                  <div className="r-grid-2">
                    <div className="r-card r-green">
                      <h4 className="r-title">💰 Salary Projection</h4>
                      <div className="r-salary-row">
                        <span>Entry Level</span>
                        <span className="r-money">${results.salary_prediction?.entry_level?.toLocaleString()}</span>
                      </div>
                      <div className="r-salary-row">
                        <span>5-Year Projection</span>
                        <span className="r-money">${results.salary_prediction?.five_year?.toLocaleString()}</span>
                      </div>
                    </div>

                    <div className="r-card r-blue">
                      <h4 className="r-title">📊 Job Readiness</h4>
                      <div className="r-score">
                        <div className="r-score-num">{results.job_readiness_score?.toFixed(1)}</div>
                        <div className="r-score-lbl">out of 100</div>
                        <div className="r-bar-bg">
                          <div className="r-bar-fill" style={{ width:`${results.job_readiness_score}%` }} />
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Skill Gap */}
                  <div className="r-card r-amber">
                    <h4 className="r-title">🎓 Skill Gap Analysis</h4>
                    {results.skill_gap?.missing_skills?.length > 0 ? (
                      <div style={{ marginBottom:14 }}>
                        <p className="r-section-label" style={{ color:'#f87171' }}>MISSING SKILLS</p>
                        <div>{results.skill_gap.missing_skills.map(s => <span key={s} className="tag tag-red">{s}</span>)}</div>
                      </div>
                    ) : (
                      <p style={{ color:'#34d399', fontWeight:600 }}>✓ You already have the essential skills!</p>
                    )}
                    {results.skill_gap?.improvement_priority?.length > 0 && (
                      <div>
                        <p className="r-section-label" style={{ color:'#fbbf24' }}>PRIORITY LEARNING</p>
                        <div>{results.skill_gap.improvement_priority.slice(0, 6).map(s => <span key={s} className="tag tag-amber">{s}</span>)}</div>
                      </div>
                    )}
                  </div>

                  {/* Roadmap */}
                  <div className="r-card r-indigo">
                    <h4 className="r-title">🗺️ Your Learning Roadmap</h4>
                    <div className="r-roadmap">
                      {[['📅','3 Months','3_months','Focus on building fundamental skills.'],
                        ['🚀','6 Months','6_months','Develop intermediate expertise and real projects.'],
                        ['🏆','12 Months','12_months','Achieve advanced mastery and a strong portfolio.']
                      ].map(([ico, label, key, fallback]) => (
                        <div key={key} className="r-rm-item">
                          <div className="r-rm-period">{ico} {label}</div>
                          <p className="r-rm-text">{results.roadmap?.[key] || fallback}</p>
                        </div>
                      ))}
                    </div>
                  </div>

                </div>
              )}
            </div>
          </div>
        </section>

        {/* ── Footer ── */}
        <footer id="about" className="c-footer">
          <div style={{ fontSize:'1.4rem', marginBottom:10 }}>🎯</div>
          <p className="c-footer-brand">CareerAI</p>
          <p className="c-footer-sub">Built with ❤️ using Next.js &amp; FastAPI · {new Date().getFullYear()}</p>
        </footer>

      </div>

      {/* ══════ All scoped styles ══════ */}
      <style jsx global>{`
        /* Blobs */
        .blob {
          position: fixed;
          border-radius: 50%;
          filter: blur(110px);
          opacity: .11;
          pointer-events: none;
          animation: blobDrift 18s ease-in-out infinite alternate;
        }
        .blob-1 { width:580px; height:580px; background:#7c3aed; top:-130px; left:-130px; animation-delay:0s; }
        .blob-2 { width:480px; height:480px; background:#3b82f6; bottom:-90px; right:-90px; animation-delay:5s; }
        .blob-3 { width:380px; height:380px; background:#ec4899; top:50%; left:42%; animation-delay:10s; }
        @keyframes blobDrift {
          0%   { transform:translate(0,0) scale(1); }
          100% { transform:translate(38px,-38px) scale(1.08); }
        }

        /* Navbar */
        .c-nav {
          position: sticky; top:0; z-index:100;
          display: flex; align-items:center; justify-content:space-between;
          padding: 0 6%; height:68px;
          background: rgba(8,11,20,.72);
          backdrop-filter: blur(20px);
          border-bottom: 1px solid rgba(255,255,255,.07);
        }
        .c-brand { display:flex; align-items:center; gap:12px; text-decoration:none; }
        .c-logo-box {
          width:40px; height:40px;
          background: linear-gradient(135deg,#7c3aed,#a855f7);
          border-radius:10px; font-size:20px;
          display:flex; align-items:center; justify-content:center;
          box-shadow: 0 0 20px rgba(124,58,237,.4);
        }
        .c-brand-name {
          font-family:'Outfit',sans-serif; font-size:1.35rem; font-weight:700;
          background: linear-gradient(90deg,#c4b5fd,#f0abfc);
          -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
        }
        .c-nav-links { display:flex; gap:28px; list-style:none; }
        .c-nav-links a {
          color:#8b9dc3; text-decoration:none; font-size:.88rem; font-weight:500;
          position:relative; transition:color .2s;
        }
        .c-nav-links a::after {
          content:''; position:absolute; bottom:-4px; left:0; width:0; height:2px;
          background:linear-gradient(90deg,#7c3aed,#a855f7); border-radius:2px;
          transition:width .3s ease;
        }
        .c-nav-links a:hover { color:#c4b5fd; }
        .c-nav-links a:hover::after { width:100%; }
        .c-cta {
          background:linear-gradient(135deg,#7c3aed,#a855f7);
          color:#fff; padding:10px 22px; border-radius:9px; font-size:.85rem; font-weight:600;
          text-decoration:none; transition:all .3s; box-shadow:0 0 16px rgba(124,58,237,.3);
        }
        .c-cta:hover { transform:translateY(-2px); box-shadow:0 0 28px rgba(124,58,237,.55); }

        /* Hero */
        .c-hero {
          min-height:88vh; display:flex; flex-direction:column;
          align-items:center; justify-content:center;
          text-align:center; padding:60px 6% 80px;
        }
        .c-badge {
          display:inline-flex; align-items:center; gap:9px;
          background:rgba(124,58,237,.14); border:1px solid rgba(124,58,237,.35);
          color:#c4b5fd; padding:7px 18px; border-radius:999px;
          font-size:.77rem; font-weight:600; letter-spacing:.07em; text-transform:uppercase;
          margin-bottom:26px;
        }
        .c-dot {
          width:7px; height:7px; background:#a855f7; border-radius:50%;
          animation: pulseDot 2s ease-in-out infinite;
        }
        @keyframes pulseDot {
          0%,100% { opacity:1; transform:scale(1); }
          50%      { opacity:.5; transform:scale(.65); }
        }
        .c-hero-h1 {
          font-family:'Outfit',sans-serif;
          font-size:clamp(2.6rem,5.5vw,4.6rem);
          font-weight:800; line-height:1.1; letter-spacing:-.02em;
          margin-bottom:22px;
        }
        .c-hero-sub {
          font-size:clamp(.95rem,1.8vw,1.15rem);
          color:#8b9dc3; max-width:620px; line-height:1.72;
          margin:0 auto 38px;
        }
        .c-hero-actions { display:flex; gap:14px; flex-wrap:wrap; justify-content:center; }
        .c-btn-primary {
          display:inline-flex; align-items:center; gap:8px;
          background:linear-gradient(135deg,#7c3aed,#a855f7);
          color:#fff; padding:14px 30px; border-radius:12px;
          font-size:.95rem; font-weight:600; border:none; cursor:pointer;
          text-decoration:none; transition:all .3s;
          box-shadow:0 0 28px rgba(124,58,237,.35),0 4px 14px rgba(0,0,0,.28);
        }
        .c-btn-primary:hover { transform:translateY(-3px); box-shadow:0 0 46px rgba(124,58,237,.55),0 8px 24px rgba(0,0,0,.4); }
        .c-btn-ghost {
          display:inline-flex; align-items:center; gap:8px;
          background:rgba(255,255,255,.04); color:#f0f4ff;
          padding:14px 30px; border-radius:12px; font-size:.95rem; font-weight:600;
          border:1px solid rgba(255,255,255,.09); cursor:pointer;
          text-decoration:none; transition:all .3s;
        }
        .c-btn-ghost:hover { background:rgba(255,255,255,.08); border-color:rgba(124,58,237,.4); transform:translateY(-2px); }

        /* Stats */
        .c-stats {
          display:flex; justify-content:center; flex-wrap:wrap;
          border-top:1px solid rgba(255,255,255,.07);
          border-bottom:1px solid rgba(255,255,255,.07);
          background:rgba(255,255,255,.02); padding:24px 6%;
        }
        .c-stat { flex:1; min-width:140px; text-align:center; padding:14px 20px; border-right:1px solid rgba(255,255,255,.07); }
        .c-stat:last-child { border-right:none; }
        .c-stat-val {
          font-family:'Outfit',sans-serif; font-size:1.85rem; font-weight:700;
          background:linear-gradient(135deg,#a78bfa,#f0abfc);
          -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
        }
        .c-stat-lbl { font-size:.75rem; color:#4a5a7a; text-transform:uppercase; letter-spacing:.08em; margin-top:3px; }

        /* Section */
        .c-section { padding:96px 6%; }
        .c-section-hdr { text-align:center; margin-bottom:56px; }
        .c-section-label { display:inline-block; color:#a78bfa; font-size:.75rem; font-weight:600; text-transform:uppercase; letter-spacing:.12em; margin-bottom:12px; }
        .c-section-title { font-family:'Outfit',sans-serif; font-size:clamp(1.75rem,3.2vw,2.5rem); font-weight:700; line-height:1.2; margin-bottom:14px; }
        .c-section-sub { color:#8b9dc3; font-size:1rem; max-width:520px; margin:0 auto; }

        /* Feature grid */
        .c-feat-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(275px,1fr)); gap:22px; max-width:1080px; margin:0 auto; }
        .c-feat-card { padding:34px 30px; border-radius:20px; position:relative; overflow:hidden; }
        .c-feat-icon { width:54px; height:54px; border-radius:13px; display:flex; align-items:center; justify-content:center; font-size:22px; margin-bottom:20px; }
        .c-feat-title { font-family:'Outfit',sans-serif; font-size:1.05rem; font-weight:700; margin-bottom:9px; }
        .c-feat-desc { color:#8b9dc3; font-size:.875rem; line-height:1.65; }

        .icon-purple { background:linear-gradient(135deg,rgba(124,58,237,.3),rgba(168,85,247,.15)); }
        .icon-green  { background:linear-gradient(135deg,rgba(16,185,129,.3),rgba(52,211,153,.15)); }
        .icon-blue   { background:linear-gradient(135deg,rgba(59,130,246,.3),rgba(99,183,255,.15)); }
        .icon-amber  { background:linear-gradient(135deg,rgba(245,158,11,.3),rgba(252,211,77,.15)); }
        .icon-pink   { background:linear-gradient(135deg,rgba(236,72,153,.3),rgba(249,168,212,.15)); }
        .icon-teal   { background:linear-gradient(135deg,rgba(20,184,166,.3),rgba(45,212,191,.15)); }

        /* Predict */
        .c-predict-bg { background:linear-gradient(180deg,transparent 0%,rgba(124,58,237,.04) 50%,transparent 100%); }
        .c-predict-wrap { max-width:800px; margin:0 auto; }
        .c-form-card {
          background:rgba(255,255,255,.03);
          border:1px solid rgba(255,255,255,.08);
          border-radius:24px; padding:44px;
          backdrop-filter:blur(12px);
          box-shadow:0 24px 80px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.06);
        }
        .c-form-grid { display:grid; grid-template-columns:1fr 1fr; gap:18px; }
        .c-full { grid-column:1/-1; }
        .c-fg { display:flex; flex-direction:column; gap:7px; }
        .c-fg label { font-size:.82rem; font-weight:600; color:#8b9dc3; letter-spacing:.03em; }
        .c-opt { font-weight:400; color:#4a5a7a; }
        .c-hint { font-size:.73rem; color:#4a5a7a; }
        .c-input {
          background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.08);
          border-radius:11px; padding:12px 15px;
          color:#f0f4ff; font-family:'Inter',sans-serif; font-size:.92rem; outline:none;
          transition:all .25s;
        }
        .c-input::placeholder { color:#4a5a7a; }
        .c-input:focus {
          border-color:rgba(124,58,237,.6);
          background:rgba(124,58,237,.07);
          box-shadow:0 0 0 3px rgba(124,58,237,.13);
        }
        .c-submit {
          width:100%; background:linear-gradient(135deg,#7c3aed,#a855f7);
          color:#fff; border:none; border-radius:12px; padding:15px;
          font-family:'Inter',sans-serif; font-size:.97rem; font-weight:600; cursor:pointer;
          transition:all .3s; box-shadow:0 4px 20px rgba(124,58,237,.35);
          display:flex; align-items:center; justify-content:center; gap:10px;
        }
        .c-submit:hover { transform:translateY(-2px); box-shadow:0 8px 30px rgba(124,58,237,.5); }
        .c-submit:disabled { opacity:.6; cursor:not-allowed; transform:none; }
        .c-spinner {
          width:18px; height:18px;
          border:2px solid rgba(255,255,255,.25); border-top-color:#fff;
          border-radius:50%; animation:spin .8s linear infinite;
          display:inline-block; flex-shrink:0;
        }
        @keyframes spin { to { transform:rotate(360deg); } }

        /* Results */
        .c-results { margin-top:34px; display:flex; flex-direction:column; gap:18px; }
        .r-card { border-radius:16px; padding:26px; border:1px solid; }
        .r-purple { background:linear-gradient(135deg,rgba(124,58,237,.13),rgba(168,85,247,.06)); border-color:rgba(124,58,237,.25); }
        .r-green  { background:linear-gradient(135deg,rgba(16,185,129,.11),rgba(52,211,153,.05)); border-color:rgba(16,185,129,.22); }
        .r-blue   { background:linear-gradient(135deg,rgba(59,130,246,.11),rgba(99,183,255,.05)); border-color:rgba(59,130,246,.22); }
        .r-amber  { background:linear-gradient(135deg,rgba(245,158,11,.1),rgba(252,211,77,.04)); border-color:rgba(245,158,11,.22); }
        .r-indigo { background:linear-gradient(135deg,rgba(99,102,241,.1),rgba(129,140,248,.04)); border-color:rgba(99,102,241,.22); }
        .r-title { font-family:'Outfit',sans-serif; font-size:.98rem; font-weight:700; margin-bottom:16px; display:flex; align-items:center; gap:9px; }
        .r-career-name {
          font-family:'Outfit',sans-serif; font-size:1.9rem; font-weight:800;
          background:linear-gradient(135deg,#c4b5fd,#f0abfc);
          -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
          margin-bottom:5px;
        }
        .r-confidence { color:#8b9dc3; font-size:.88rem; }
        .r-alt-label { font-size:.72rem; color:#4a5a7a; text-transform:uppercase; letter-spacing:.08em; margin-bottom:7px; }
        .r-grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:18px; }
        .r-salary-row { display:flex; justify-content:space-between; align-items:center; padding:9px 0; border-bottom:1px solid rgba(255,255,255,.06); }
        .r-salary-row:last-child { border-bottom:none; }
        .r-salary-row span:first-child { color:#8b9dc3; font-size:.88rem; }
        .r-money { font-family:'Outfit',sans-serif; font-weight:700; font-size:.98rem; color:#34d399; }
        .r-score { text-align:center; }
        .r-score-num {
          font-family:'Outfit',sans-serif; font-size:2.3rem; font-weight:800;
          background:linear-gradient(135deg,#10b981,#34d399);
          -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
        }
        .r-score-lbl { color:#4a5a7a; font-size:.78rem; margin-bottom:14px; }
        .r-bar-bg { background:rgba(255,255,255,.07); border-radius:999px; height:8px; overflow:hidden; }
        .r-bar-fill { height:100%; border-radius:999px; background:linear-gradient(90deg,#10b981,#34d399); transition:width 1.2s ease-out; }
        .r-section-label { font-size:.72rem; font-weight:600; text-transform:uppercase; letter-spacing:.08em; margin-bottom:8px; }
        .r-roadmap { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }
        .r-rm-item { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.07); border-radius:12px; padding:16px; }
        .r-rm-period { font-family:'Outfit',sans-serif; font-weight:700; font-size:.9rem; color:#a78bfa; margin-bottom:9px; }
        .r-rm-text { font-size:.82rem; color:#8b9dc3; line-height:1.6; }

        /* Footer */
        .c-footer { border-top:1px solid rgba(255,255,255,.07); padding:40px 6%; text-align:center; }
        .c-footer-brand { font-family:'Outfit',sans-serif; font-size:1.1rem; font-weight:700; color:#c4b5fd; margin-bottom:6px; }
        .c-footer-sub { color:#4a5a7a; font-size:.82rem; }

        /* Responsive */
        @media(max-width:760px) {
          .c-nav-links { display:none; }
          .c-form-grid, .r-grid-2, .r-roadmap { grid-template-columns:1fr; }
          .c-form-card { padding:26px 18px; }
          .c-stats { flex-direction:column; }
          .c-stat { border-right:none; border-bottom:1px solid rgba(255,255,255,.07); }
          .c-stat:last-child { border-bottom:none; }
        }
      `}</style>
    </>
  )
}
