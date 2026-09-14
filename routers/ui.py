from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Web UI"])

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>WikiAgent — Grounded Technical RAG Assistant</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    
    :root {
      --bg-dark: #090d16;
      --card-bg: rgba(22, 27, 40, 0.85);
      --card-border: rgba(124, 58, 237, 0.22);
      --card-border-hover: rgba(56, 189, 248, 0.35);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent-purple: #7c3aed;
      --accent-cyan: #06b6d4;
      --accent-blue: #38bdf8;
      --accent-orange: linear-gradient(163deg, #fbbc94 0%, #f49d70 46%, #e88654 100%);
      --ring-focus: rgba(56, 189, 248, 0.4);
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--bg-dark);
      color: var(--text-main);
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    /* Custom Sleek Animated Scrollbars */
    ::-webkit-scrollbar {
      width: 7px;
      height: 5px;
    }

    ::-webkit-scrollbar-track {
      background: rgba(9, 13, 22, 0.6);
      border-radius: 9999px;
    }

    ::-webkit-scrollbar-thumb {
      background: rgba(124, 58, 237, 0.45);
      border-radius: 9999px;
      transition: background 0.3s ease, box-shadow 0.3s ease;
    }

    ::-webkit-scrollbar-thumb:hover {
      background: rgba(56, 189, 248, 0.75);
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
    }

    * {
      scrollbar-width: thin;
      scrollbar-color: rgba(124, 58, 237, 0.45) rgba(9, 13, 22, 0.6);
    }

    /* Ambient Glow Effects */
    .ambient-glow {
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 0;
      background: 
        radial-gradient(circle at 50% 15%, rgba(124, 58, 237, 0.12) 0%, transparent 60%),
        radial-gradient(circle at 85% 85%, rgba(6, 182, 212, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 15% 75%, rgba(232, 134, 84, 0.06) 0%, transparent 50%);
    }

    /* Header Nav */
    header {
      position: relative;
      z-index: 10;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 28px;
      background: rgba(9, 13, 22, 0.85);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.07);
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 600;
      font-size: 1.1rem;
      letter-spacing: -0.015em;
    }

    .brand-mark {
      width: 34px;
      height: 34px;
      border-radius: 10px;
      background: linear-gradient(135deg, #7c3aed 0%, #06b6d4 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 20px rgba(124, 58, 237, 0.4);
    }

    .nav-meta {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .status-pill {
      font-size: 0.8rem;
      font-weight: 500;
      padding: 6px 14px;
      border-radius: 9999px;
      background: rgba(124, 58, 237, 0.12);
      border: 1px solid rgba(124, 58, 237, 0.3);
      color: #c4b5fd;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 10px #10b981;
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.6; transform: scale(0.9); }
    }

    .stat-badge {
      font-size: 0.78rem;
      color: var(--text-muted);
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      padding: 5px 12px;
      border-radius: 9999px;
    }

    /* Main Chat Display Stage */
    #chat-stage {
      flex: 1;
      position: relative;
      z-index: 10;
      overflow-y: auto;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 20px;
      max-width: 980px;
      width: 100%;
      margin: 0 auto;
      scroll-behavior: smooth;
    }

    /* Initial Hero State */
    .hero-greeting {
      margin: auto 0;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 16px;
      padding: 40px 20px;
    }

    .hero-badge {
      font-size: 0.8rem;
      font-weight: 500;
      color: var(--accent-cyan);
      background: rgba(6, 182, 212, 0.1);
      border: 1px solid rgba(6, 182, 212, 0.25);
      padding: 6px 14px;
      border-radius: 9999px;
    }

    .hero-title {
      font-size: 2.3rem;
      font-weight: 600;
      letter-spacing: -0.025em;
      background: linear-gradient(180deg, #FFFFFF 0%, #CBD5E1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      line-height: 1.2;
    }

    .hero-sub {
      font-size: 1.02rem;
      color: var(--text-muted);
      max-width: 560px;
      line-height: 1.6;
    }

    /* Message Bubbles */
    .message {
      display: flex;
      flex-direction: column;
      gap: 8px;
      max-width: 85%;
      animation: fadeIn 0.25s ease-out;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .message.user { align-self: flex-end; }
    .message.bot { align-self: flex-start; }

    .bubble {
      padding: 15px 20px;
      border-radius: 20px;
      line-height: 1.6;
      font-size: 0.96rem;
    }

    .message.user .bubble {
      background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
      color: #ffffff;
      border-bottom-right-radius: 4px;
      box-shadow: 0 4px 16px rgba(2, 132, 199, 0.3);
    }

    .message.bot .bubble {
      background: var(--card-bg);
      backdrop-filter: blur(20px);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      border-bottom-left-radius: 4px;
      box-shadow: 0 12px 35px rgba(0, 0, 0, 0.4);
    }

    /* Reference Hero Image in Main Answer */
    .answer-reference-card {
      margin-bottom: 12px;
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.14);
      background: #0f172a;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
      max-height: 220px;
    }

    .answer-reference-img {
      width: 100%;
      height: 100%;
      max-height: 220px;
      object-fit: cover;
      display: block;
      transition: transform 0.3s ease;
    }

    .answer-reference-card:hover .answer-reference-img {
      transform: scale(1.02);
    }

    /* Collapsible Sources Accordion */
    .sources-toggle-btn {
      align-self: flex-start;
      margin-top: 4px;
      background: rgba(124, 58, 237, 0.08);
      border: 1px solid rgba(124, 58, 237, 0.25);
      color: #c4b5fd;
      font-size: 0.83rem;
      font-weight: 500;
      padding: 7px 14px;
      border-radius: 8px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
    }

    .sources-toggle-btn:hover {
      background: rgba(124, 58, 237, 0.18);
      border-color: var(--accent-purple);
      color: #ffffff;
    }

    .sources-dropdown {
      margin-top: 8px;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid rgba(124, 58, 237, 0.2);
      border-radius: 14px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      width: 100%;
      max-width: 640px;
    }

    .source-item {
      display: flex;
      gap: 14px;
      align-items: center;
      background: rgba(255, 255, 255, 0.03);
      border-radius: 10px;
      padding: 12px;
      border-left: 3px solid var(--accent-cyan);
      transition: background 0.2s ease;
    }

    .source-item:hover {
      background: rgba(255, 255, 255, 0.06);
    }

    .source-thumb {
      width: 55px;
      height: 55px;
      object-fit: cover;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.15);
      background: #1e293b;
      flex-shrink: 0;
    }

    .source-title {
      font-weight: 600;
      font-size: 0.9rem;
      margin-bottom: 4px;
    }

    .source-title a {
      color: var(--accent-blue);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .source-title a:hover {
      text-decoration: underline;
    }

    .source-snippet {
      font-size: 0.82rem;
      color: var(--text-muted);
      line-height: 1.45;
    }

    .hidden { display: none !important; }

    /* Composer Floating Container */
    .composer-container {
      position: relative;
      z-index: 20;
      max-width: 980px;
      width: 100%;
      margin: 0 auto;
      padding: 0 24px 24px 24px;
    }

    /* Composer Card */
    .composer-card {
      background: var(--card-bg);
      backdrop-filter: blur(24px) saturate(110%);
      border: 1px solid var(--card-border);
      border-radius: 24px;
      padding: 18px 22px;
      box-shadow: 0 22px 60px rgba(0, 0, 0, 0.5);
      display: flex;
      flex-direction: column;
      gap: 14px;
      transition: border-color 0.2s ease;
    }

    .composer-card:focus-within {
      border-color: var(--card-border-hover);
    }

    .input-field {
      width: 100%;
      background: transparent;
      border: none;
      outline: none;
      color: var(--text-main);
      font-size: 1.05rem;
      font-family: inherit;
      resize: none;
    }

    .input-field::placeholder {
      color: #64748b;
    }

    /* One-Row Toolbar (.tools) */
    .tools {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }

    /* Left Chips */
    .chips {
      display: flex;
      align-items: center;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 6px;
      scrollbar-width: thin;
      scrollbar-color: rgba(124, 58, 237, 0.45) rgba(255, 255, 255, 0.04);
    }

    .chips::-webkit-scrollbar {
      height: 4px;
      display: block;
    }

    .chips::-webkit-scrollbar-track {
      background: rgba(255, 255, 255, 0.04);
      border-radius: 9999px;
    }

    .chips::-webkit-scrollbar-thumb {
      background: rgba(124, 58, 237, 0.45);
      border-radius: 9999px;
      transition: background 0.25s ease, box-shadow 0.25s ease;
    }

    .chips::-webkit-scrollbar-thumb:hover {
      background: rgba(56, 189, 248, 0.8);
      box-shadow: 0 0 8px rgba(56, 189, 248, 0.6);
    }

    .chip {
      height: 32px;
      padding: 0 14px;
      border-radius: 9999px;
      font-size: 0.81rem;
      font-weight: 500;
      color: #cbd5e1;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      white-space: nowrap;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .chip:hover {
      background: rgba(124, 58, 237, 0.15);
      color: #ffffff;
      border-color: rgba(124, 58, 237, 0.35);
    }

    /* Right Cluster */
    .right-cluster {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-shrink: 0;
    }

    .model-label {
      font-size: 0.81rem;
      font-weight: 500;
      color: #94a3b8;
      display: flex;
      align-items: center;
      gap: 5px;
      background: rgba(255, 255, 255, 0.04);
      padding: 5px 10px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Circular Send Button */
    .send-btn {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      background: var(--accent-orange);
      border: none;
      color: #ffffff;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 16px rgba(232, 134, 84, 0.4);
      transition: transform 0.15s ease, filter 0.15s ease;
      flex-shrink: 0;
    }

    .send-btn:hover {
      filter: brightness(1.08);
      transform: scale(1.04);
    }

    .send-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
      filter: none;
    }

    /* Responsive Design */
    @media (max-width: 640px) {
      header { padding: 14px 18px; }
      #chat-stage { padding: 16px; }
      .composer-container { padding: 0 16px 16px 16px; }
      .hero-title { font-size: 1.7rem; }
      .tools { flex-direction: column; align-items: stretch; gap: 10px; }
      .right-cluster { justify-content: flex-end; }
      .stat-badge { display: none; }
    }
  </style>
</head>
<body>
  <div class="ambient-glow"></div>

  <!-- Header Nav -->
  <header>
    <div class="brand">
      <div class="brand-mark">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 2a10 10 0 1 0 10 10H12V2z"></path>
          <path d="M12 12L2.5 7.5"></path>
          <path d="M12 12v10"></path>
        </svg>
      </div>
      <span>WikiAgent</span>
    </div>
    
    <div class="nav-meta">
      <span class="stat-badge">37 Topics • 1,445 Chunks</span>
      <div class="status-pill">
        <span class="status-dot"></span>
        <span>llama3.2:1b Grounded RAG</span>
      </div>
    </div>
  </header>

  <!-- Main Chat Stage -->
  <main id="chat-stage">
    <div class="hero-greeting" id="hero-greeting">
      <span class="hero-badge">AI-Native Grounded RAG</span>
      <h1 class="hero-title">Describe a topic. We'll synthesize it.</h1>
      <p class="hero-sub">Grounded local AI assistant powered by Wikipedia, ChromaDB, and Ollama. Ask technical questions or explore 37 indexed domains.</p>
    </div>
  </main>

  <!-- Composer Floating Card -->
  <div class="composer-container">
    <form class="composer-card" id="chat-form" onsubmit="handleSubmit(event)">
      <input type="text" class="input-field" id="user-input" placeholder="Ask a question or topic (e.g. 'What is Python?')..." autocomplete="off" required />
      
      <!-- One-Row Toolbar -->
      <div class="tools">
        <!-- Left Quick Chips -->
        <div class="chips">
          <button type="button" class="chip" onclick="ask('python')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            Python
          </button>
          <button type="button" class="chip" onclick="ask('What is a binary search tree?')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v18M5 12h14"/></svg>
            Data Structures
          </button>
          <button type="button" class="chip" onclick="ask('What is React and how do components work?')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><ellipse cx="12" cy="12" rx="10" ry="4"/></svg>
            React.js
          </button>
          <button type="button" class="chip" onclick="ask('What is an AI agent and multi-agent system?')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/></svg>
            AI Agents
          </button>
          <button type="button" class="chip" onclick="ask('What is 21st.dev?')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            21st.dev
          </button>
          <button type="button" class="chip" onclick="ask('How is Blender used in software engineering?')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
            Blender
          </button>
          <button type="button" class="chip" onclick="ask('What are the steps to build a modern website?')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.71 1.13-1.6 1.4-2.5-1.12-.55-2.05-1.48-2.6-2.6-.9.27-1.79.69-2.5 1.4z"/><path d="M12 15l-3-3 7.5-7.5a2.12 2.12 0 0 1 3 3L12 15z"/></svg>
            SDLC Steps
          </button>
          <button type="button" class="chip" onclick="ask('What is ethical hacking?')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            Cybersecurity
          </button>
        </div>

        <!-- Right Controls Cluster -->
        <div class="right-cluster">
          <span class="model-label">
            llama3.2:1b
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
          </span>
          <button type="submit" class="send-btn" id="send-btn" title="Send query" aria-label="Send query">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="19" x2="12" y2="5"></line>
              <polyline points="5 12 12 5 19 12"></polyline>
            </svg>
          </button>
        </div>
      </div>
    </form>
  </div>

  <script>
    const chatStage = document.getElementById('chat-stage');
    const heroGreeting = document.getElementById('hero-greeting');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    function toggleSources(btn) {
      const dropdown = btn.nextElementSibling;
      const isHidden = dropdown.classList.toggle('hidden');
      const arrow = btn.querySelector('.arrow');
      if (arrow) arrow.textContent = isHidden ? '▸' : '▾';
    }

    function addMessage(text, role, sources = []) {
      if (heroGreeting) heroGreeting.style.display = 'none';

      const msgDiv = document.createElement('div');
      msgDiv.className = `message ${role}`;
      
      const bubble = document.createElement('div');
      bubble.className = 'bubble';

      if (role === 'bot' && sources && sources.length > 0) {
        const primaryImg = sources.find(s => s.image_url)?.image_url;
        let contentHTML = '';
        if (primaryImg) {
          contentHTML += `
            <div class="answer-reference-card">
              <img src="${primaryImg}" alt="Reference Media" class="answer-reference-img" />
            </div>
          `;
        }
        contentHTML += `<div>${text.replace(/\\n/g, '<br>')}</div>`;
        bubble.innerHTML = contentHTML;
      } else {
        bubble.innerHTML = text.replace(/\\n/g, '<br>');
      }

      msgDiv.appendChild(bubble);

      if (role === 'bot' && sources && sources.length > 0) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'sources-toggle-btn';
        btn.innerHTML = `<span>📚 Sources (${sources.length})</span> <span class="arrow">▸</span>`;
        btn.onclick = () => toggleSources(btn);
        msgDiv.appendChild(btn);

        const dropdown = document.createElement('div');
        dropdown.className = 'sources-dropdown hidden';
        dropdown.innerHTML = sources.map((s, idx) => `
          <div class="source-item">
            ${s.image_url ? `<img src="${s.image_url}" alt="${s.source}" class="source-thumb" />` : ''}
            <div style="flex: 1;">
              <div class="source-title">
                ${idx + 1}. <a href="${s.url || '#'}" target="_blank" rel="noopener">${s.source || 'Wikipedia'} ↗</a>
              </div>
              <div class="source-snippet">"${(s.chunk_preview || '').substring(0, 180)}..."</div>
            </div>
          </div>
        `).join('');
        msgDiv.appendChild(dropdown);
      }

      chatStage.appendChild(msgDiv);
      chatStage.scrollTop = chatStage.scrollHeight;
    }

    async function ask(query) {
      userInput.value = query;
      handleSubmit(new Event('submit'));
    }

    async function handleSubmit(e) {
      if (e) e.preventDefault();
      const q = userInput.value.trim();
      if (!q) return;

      addMessage(q, 'user');
      userInput.value = '';
      sendBtn.disabled = true;

      const loadingDiv = document.createElement('div');
      loadingDiv.className = 'message bot';
      loadingDiv.id = 'temp-loading';
      loadingDiv.innerHTML = '<div class="bubble" style="color: #94a3b8;"><i>Searching Wikipedia & synthesizing answer...</i></div>';
      chatStage.appendChild(loadingDiv);
      chatStage.scrollTop = chatStage.scrollHeight;

      try {
        const res = await fetch('/chat/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: q, top_k: 2 })
        });
        const data = await res.json();
        loadingDiv.remove();

        if (res.ok) {
          addMessage(data.answer, 'bot', data.sources || []);
        } else {
          addMessage(`Error: ${data.detail || 'Service unavailable'}`, 'bot');
        }
      } catch (err) {
        loadingDiv.remove();
        addMessage(`Connection error: ${err.message}`, 'bot');
      } finally {
        sendBtn.disabled = false;
        userInput.focus();
      }
    }
  </script>
</body>
</html>
"""

@router.get("/", response_class=HTMLResponse)
@router.get("/app", response_class=HTMLResponse)
async def web_ui():
    return HTML_TEMPLATE
