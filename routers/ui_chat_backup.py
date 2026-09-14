from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Web UI"])

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WikiAgent - Local Wikipedia Chatbot</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: #0f172a;
      color: #f8fafc;
      display: flex;
      flex-direction: column;
      height: 100vh;
    }
    header {
      background: #1e293b;
      border-bottom: 1px solid #475569;
      padding: 14px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .brand { display: flex; align-items: center; gap: 10px; font-weight: bold; font-size: 1.1rem; }
    .status-pill {
      font-size: 0.8rem;
      padding: 4px 10px;
      border-radius: 9999px;
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }
    #chat-container {
      flex: 1;
      overflow-y: auto;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .message {
      max-width: 800px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .message.user { align-self: flex-end; }
    .message.bot { align-self: flex-start; }
    .bubble {
      padding: 12px 16px;
      border-radius: 12px;
      line-height: 1.5;
      font-size: 0.95rem;
    }
    .message.user .bubble {
      background: #0284c7;
      color: #fff;
      border-bottom-right-radius: 2px;
    }
    .message.bot .bubble {
      background: #334155;
      color: #f8fafc;
      border-bottom-left-radius: 2px;
    }
    /* Collapsible Sources Button */
    .sources-toggle-btn {
      align-self: flex-start;
      margin-top: 4px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid #475569;
      color: #38bdf8;
      font-size: 0.82rem;
      font-weight: 500;
      padding: 6px 12px;
      border-radius: 6px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }
    .sources-toggle-btn:hover {
      background: rgba(56, 189, 248, 0.2);
      border-color: #38bdf8;
    }
    .sources-dropdown {
      margin-top: 6px;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid #475569;
      border-radius: 8px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      max-width: 600px;
    }
    .source-item {
      border-left: 3px solid #38bdf8;
      padding-left: 10px;
    }
    .source-title {
      font-weight: 600;
      font-size: 0.85rem;
      margin-bottom: 3px;
    }
    .source-title a {
      color: #38bdf8;
      text-decoration: none;
    }
    .source-title a:hover {
      text-decoration: underline;
    }
    .source-snippet {
      font-size: 0.8rem;
      color: #94a3b8;
      line-height: 1.4;
    }
    .hidden { display: none !important; }
    footer {
      background: #1e293b;
      border-top: 1px solid #475569;
      padding: 14px 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .chips {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 2px;
    }
    .chip {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid #475569;
      color: #94a3b8;
      font-size: 0.78rem;
      padding: 4px 10px;
      border-radius: 9999px;
      cursor: pointer;
      white-space: nowrap;
      transition: background 0.2s;
    }
    .chip:hover {
      background: rgba(255, 255, 255, 0.12);
      color: #f8fafc;
    }
    form {
      display: flex;
      gap: 10px;
    }
    input {
      flex: 1;
      background: #0f172a;
      border: 1px solid #475569;
      border-radius: 8px;
      padding: 12px 16px;
      color: #f8fafc;
      font-size: 0.95rem;
      outline: none;
    }
    input:focus {
      border-color: #38bdf8;
    }
    button[type='submit'] {
      background: #38bdf8;
      color: #0f172a;
      border: none;
      border-radius: 8px;
      padding: 0 20px;
      font-weight: 600;
      cursor: pointer;
      transition: opacity 0.2s;
    }
    button[type='submit']:hover { opacity: 0.9; }
    button[type='submit']:disabled { opacity: 0.5; cursor: not-allowed; }
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <span>🧠</span>
      <span>WikiAgent Web</span>
    </div>
    <div class="status-pill" id="status-pill">⚡ llama3.2:1b Ready</div>
  </header>

  <div id="chat-container">
    <div class="message bot">
      <div class="bubble">
        Hello! I am your local Wikipedia RAG assistant. Ask me anything about indexed topics like <b>Python</b>, <b>Machine Learning</b>, <b>Artificial Intelligence</b>, or <b>Deep Learning</b>.
      </div>
    </div>
  </div>

  <footer>
    <div class="chips">
      <span class="chip" onclick="ask('python')">🐍 Python</span>
      <span class="chip" onclick="ask('What is a binary search tree?')">🌳 Data Structures</span>
      <span class="chip" onclick="ask('What is React and how do components work?')">⚛️ React.js</span>
      <span class="chip" onclick="ask('What is an AI agent and multi-agent system?')">🤖 AI Agents</span>
      <span class="chip" onclick="ask('What is 21st.dev?')">🎨 21st.dev</span>
      <span class="chip" onclick="ask('How is Blender used in software engineering?')">🧊 Blender in Engineering</span>
      <span class="chip" onclick="ask('What are the steps to build a modern website?')">🚀 Website Steps</span>
      <span class="chip" onclick="ask('What is ethical hacking?')">🛡️ Cybersecurity</span>
    </div>
    <form id="chat-form" onsubmit="handleSubmit(event)">
      <input type="text" id="user-input" placeholder="Ask a question or topic (e.g. 'python')..." autocomplete="off" required />
      <button type="submit" id="send-btn">Send</button>
    </form>
  </footer>

  <script>
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    function toggleSources(btn) {
      const dropdown = btn.nextElementSibling;
      const isHidden = dropdown.classList.toggle('hidden');
      const arrow = btn.querySelector('.arrow');
      if (arrow) arrow.textContent = isHidden ? '▸' : '▾';
    }

    function addMessage(text, role, sources = []) {
      const msgDiv = document.createElement('div');
      msgDiv.className = `message ${role}`;
      
      const bubble = document.createElement('div');
      bubble.className = 'bubble';
      bubble.innerHTML = text.replace(/\\n/g, '<br>');
      msgDiv.appendChild(bubble);

      if (role === 'bot' && sources && sources.length > 0) {
        const btn = document.createElement('button');
        btn.className = 'sources-toggle-btn';
        btn.innerHTML = `<span>📚 Sources (${sources.length})</span> <span class="arrow">▸</span>`;
        btn.onclick = () => toggleSources(btn);
        msgDiv.appendChild(btn);

        const dropdown = document.createElement('div');
        dropdown.className = 'sources-dropdown hidden';
        dropdown.innerHTML = sources.map((s, idx) => `
          <div class="source-item" style="display: flex; gap: 12px; align-items: center;">
            ${s.image_url ? `<img src="${s.image_url}" alt="${s.source}" style="width: 55px; height: 55px; object-fit: cover; border-radius: 6px; border: 1px solid #475569; background: #1e293b;" />` : ''}
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

      chatContainer.appendChild(msgDiv);
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function ask(query) {
      userInput.value = query;
      handleSubmit(new Event('submit'));
    }

    async function handleSubmit(e) {
      e.preventDefault();
      const q = userInput.value.trim();
      if (!q) return;

      addMessage(q, 'user');
      userInput.value = '';
      sendBtn.disabled = true;

      const loadingDiv = document.createElement('div');
      loadingDiv.className = 'message bot';
      loadingDiv.id = 'temp-loading';
      loadingDiv.innerHTML = '<div class="bubble" style="color: #94a3b8;"><i>Searching Wikipedia & generating answer...</i></div>';
      chatContainer.appendChild(loadingDiv);
      chatContainer.scrollTop = chatContainer.scrollHeight;

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
