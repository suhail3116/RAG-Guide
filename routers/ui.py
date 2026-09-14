from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Web UI"])

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>Fastshot WikiAgent — Grounded Technical RAG</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    
    :root {
      --bg-dark: #0a0d12;
      --card-bg: rgba(28, 30, 36, 0.88);
      --card-border: rgba(255, 255, 255, 0.12);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent-orange: linear-gradient(163deg, #FBBC94 0%, #F49D70 46%, #E88654 100%);
      --accent-blue: #38bdf8;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg-dark);
      color: var(--text-main);
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      -webkit-font-smoothing: antialiased;
    }

    /* Ambient Background Glow */
    .ambient-glow {
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 0;
      background: 
        radial-gradient(circle at 50% 20%, rgba(56, 189, 248, 0.08) 0%, transparent 60%),
        radial-gradient(circle at 80% 80%, rgba(232, 134, 84, 0.06) 0%, transparent 50%);
    }

    /* Header Nav */
    header {
      position: relative;
      z-index: 10;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 24px;
      background: rgba(10, 13, 18, 0.8);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 600;
      font-size: 1.05rem;
      letter-spacing: -0.01em;
    }

    .brand-mark {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: radial-gradient(circle, #FBBC94 0%, #E88654 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 16px rgba(232, 134, 84, 0.35);
    }

    .status-pill {
      font-size: 0.8rem;
      font-weight: 500;
      padding: 5px 12px;
      border-radius: 9999px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #cbd5e1;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .status-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
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
      max-width: 960px;
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

    .hero-title {
      font-size: 2.2rem;
      font-weight: 500;
      letter-spacing: -0.02em;
      background: linear-gradient(180deg, #FFFFFF 0%, #94A3B8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-sub {
      font-size: 1rem;
      color: var(--text-muted);
      max-width: 540px;
      line-height: 1.5;
    }

    /* Message Bubbles */
    .message {
      display: flex;
      flex-direction: column;
      gap: 8px;
      max-width: 85%;
      animation: fadeIn 0.3s ease-out;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .message.user { align-self: flex-end; }
    .message.bot { align-self: flex-start; }

    .bubble {
      padding: 14px 18px;
      border-radius: 18px;
      line-height: 1.55;
      font-size: 0.95rem;
    }

    .message.user .bubble {
      background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
      color: #ffffff;
      border-bottom-right-radius: 4px;
      box-shadow: 0 4px 14px rgba(2, 132, 199, 0.25);
    }

    .message.bot .bubble {
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      border-bottom-left-radius: 4px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    /* Collapsible Sources Accordion */
    .sources-toggle-btn {
      align-self: flex-start;
      margin-top: 4px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--accent-blue);
      font-size: 0.82rem;
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
      background: rgba(56, 189, 248, 0.12);
      border-color: var(--accent-blue);
    }

    .sources-dropdown {
      margin-top: 8px;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      width: 100%;
      max-width: 620px;
    }

    .source-item {
      display: flex;
      gap: 14px;
      align-items: center;
      background: rgba(255, 255, 255, 0.03);
      border-radius: 8px;
      padding: 10px;
      border-left: 3px solid var(--accent-blue);
    }

    .source-thumb {
      width: 55px;
      height: 55px;
      object-fit: cover;
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.15);
      background: #1e293b;
      flex-shrink: 0;
    }

    .source-title {
      font-weight: 600;
      font-size: 0.88rem;
      margin-bottom: 4px;
    }

    .source-title a {
      color: var(--accent-blue);
      text-decoration: none;
    }

    .source-title a:hover {
      text-decoration: underline;
    }

    .source-snippet {
      font-size: 0.8rem;
      color: var(--text-muted);
      line-height: 1.4;
    }

    .hidden { display: none !important; }

    /* Composer Floating Container */
    .composer-container {
      position: relative;
      z-index: 20;
      max-width: 960px;
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
      padding: 16px 20px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45);
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .input-field {
      width: 100%;
      background: transparent;
      border: none;
      outline: none;
      color: var(--text-main);
      font-size: 1.02rem;
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
      gap: 6px;
      overflow-x: auto;
      scrollbar-width: none; /* Firefox */
      -ms-overflow-style: none; /* IE/Edge */
    }

    .chips::-webkit-scrollbar { display: none; }

    .chip {
      height: 32px;
      padding: 0 12px;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 500;
      color: #cbd5e1;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.08);
      white-space: nowrap;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
    }

    .chip:hover {
      background: rgba(255, 255, 255, 0.14);
      color: #ffffff;
      border-color: rgba(255, 255, 255, 0.2);
    }

    /* Right Cluster */
    .right-cluster {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-shrink: 0;
    }

    .model-label {
      font-size: 0.8rem;
      font-weight: 500;
      color: #94a3b8;
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .attach-btn {
      background: none;
      border: none;
      color: #94a3b8;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: color 0.2s ease;
    }

    .attach-btn:hover { color: #ffffff; }

    /* Orange Circular Send Button */
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
      box-shadow: 0 4px 14px rgba(232, 134, 84, 0.35);
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

    /* Responsive adjustments */
    @media (max-width: 640px) {
      header { padding: 12px 16px; }
      #chat-stage { padding: 16px; }
      .composer-container { padding: 0 16px 16px 16px; }
      .hero-title { font-size: 1.6rem; }
      .tools { flex-direction: column; align-items: stretch; gap: 10px; }
      .right-cluster { justify-content: flex-end; }
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
          <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
        </svg>
      </div>
      <span>WikiAgent</span>
    </div>
    <div class="status-pill">
      <span class="status-dot"></span>
      <span>llama3.2:1b Grounded RAG</span>
    </div>
  </header>

  <!-- Main Chat Stage -->
  <main id="chat-stage">
    <div class="hero-greeting" id="hero-greeting">
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
          <button type="button" class="chip" onclick="ask('python')">🐍 Python</button>
          <button type="button" class="chip" onclick="ask('What is a binary search tree?')">🌳 Data Structures</button>
          <button type="button" class="chip" onclick="ask('What is React and how do components work?')">⚛️ React.js</button>
          <button type="button" class="chip" onclick="ask('What is an AI agent and multi-agent system?')">🤖 AI Agents</button>
          <button type="button" class="chip" onclick="ask('What is 21st.dev?')">🎨 21st.dev</button>
          <button type="button" class="chip" onclick="ask('How is Blender used in software engineering?')">🧊 Blender</button>
          <button type="button" class="chip" onclick="ask('What are the steps to build a modern website?')">🚀 SDLC Steps</button>
          <button type="button" class="chip" onclick="ask('What is ethical hacking?')">🛡️ Cybersecurity</button>
        </div>

        <!-- Right Controls Cluster -->
        <div class="right-cluster">
          <span class="model-label">
            llama3.2:1b
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
          </span>
          <button type="submit" class="send-btn" id="send-btn" title="Send query">
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
      bubble.innerHTML = text.replace(/\\n/g, '<br>');
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
