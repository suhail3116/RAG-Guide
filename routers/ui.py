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
      padding: 14px 24px;
      background: rgba(9, 13, 22, 0.88);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.07);
    }

    .header-left {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 600;
      font-size: 1.08rem;
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

    .history-toggle-btn {
      font-size: 0.8rem;
      font-weight: 500;
      padding: 6px 12px;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #cbd5e1;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }

    .history-toggle-btn:hover {
      background: rgba(255, 255, 255, 0.12);
      color: #ffffff;
    }

    .nav-meta {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .new-chat-btn {
      font-size: 0.81rem;
      font-weight: 500;
      padding: 6px 14px;
      border-radius: 9999px;
      background: rgba(124, 58, 237, 0.15);
      border: 1px solid rgba(124, 58, 237, 0.35);
      color: #ffffff;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }

    .new-chat-btn:hover {
      background: linear-gradient(135deg, #7c3aed 0%, #06b6d4 100%);
      border-color: transparent;
      box-shadow: 0 0 16px rgba(124, 58, 237, 0.45);
      transform: translateY(-1px);
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

    /* App Main Body Layout with Left History Sidebar */
    .app-body {
      flex: 1;
      display: flex;
      overflow: hidden;
      position: relative;
      z-index: 10;
    }

    /* Left Previous Chats History Sidebar */
    .history-sidebar {
      width: 280px;
      flex-shrink: 0;
      background: rgba(12, 16, 26, 0.95);
      backdrop-filter: blur(20px);
      border-right: 1px solid rgba(255, 255, 255, 0.08);
      display: flex;
      flex-direction: column;
      transition: margin-left 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .history-sidebar.collapsed {
      margin-left: -280px;
    }

    .sidebar-header {
      padding: 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.07);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .sidebar-title {
      font-size: 0.85rem;
      font-weight: 600;
      color: #e2e8f0;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .clear-history-btn {
      font-size: 0.75rem;
      color: var(--text-muted);
      background: none;
      border: none;
      cursor: pointer;
      transition: color 0.2s ease;
    }

    .clear-history-btn:hover {
      color: #ef4444;
    }

    .history-list {
      flex: 1;
      overflow-y: auto;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .history-item {
      padding: 10px 12px;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.06);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: all 0.2s ease;
    }

    .history-item:hover {
      background: rgba(124, 58, 237, 0.12);
      border-color: rgba(124, 58, 237, 0.3);
    }

    .history-item.active {
      background: rgba(124, 58, 237, 0.2);
      border-color: var(--accent-cyan);
    }

    .history-item-info {
      display: flex;
      flex-direction: column;
      gap: 2px;
      overflow: hidden;
    }

    .history-item-title {
      font-size: 0.83rem;
      font-weight: 500;
      color: #f1f5f9;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .history-item-date {
      font-size: 0.72rem;
      color: #64748b;
    }

    .history-delete-btn {
      background: none;
      border: none;
      color: #64748b;
      font-size: 0.85rem;
      cursor: pointer;
      padding: 2px 4px;
      border-radius: 4px;
      opacity: 0;
      transition: opacity 0.2s ease, color 0.2s ease;
    }

    .history-item:hover .history-delete-btn {
      opacity: 1;
    }

    .history-delete-btn:hover {
      color: #ef4444;
    }

    .empty-history-msg {
      font-size: 0.8rem;
      color: #64748b;
      text-align: center;
      margin: 20px 0;
    }

    /* Main Content Column */
    .main-content-col {
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      position: relative;
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
      max-height: 240px;
      cursor: pointer;
      position: relative;
    }

    .answer-reference-img {
      width: 100%;
      height: 100%;
      max-height: 240px;
      object-fit: cover;
      display: block;
      transition: transform 0.3s ease, filter 0.3s ease;
    }

    .answer-reference-card:hover .answer-reference-img {
      transform: scale(1.03);
      filter: brightness(1.05);
    }

    .source-thumb {
      width: 55px;
      height: 55px;
      object-fit: cover;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.15);
      background: #1e293b;
      flex-shrink: 0;
      cursor: pointer;
      transition: transform 0.2s ease;
    }

    .source-thumb:hover {
      transform: scale(1.08);
    }

    /* Full-Size Lightbox Modal */
    .lightbox-modal {
      position: fixed;
      inset: 0;
      z-index: 100;
      background: rgba(5, 7, 12, 0.92);
      backdrop-filter: blur(16px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s ease;
    }

    .lightbox-modal.active {
      opacity: 1;
      pointer-events: auto;
    }

    .lightbox-content {
      max-width: 92vw;
      max-height: 88vh;
      border-radius: 16px;
      border: 1px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 25px 70px rgba(0, 0, 0, 0.85);
      object-fit: contain;
      animation: zoomIn 0.25s ease-out;
    }

    @keyframes zoomIn {
      from { transform: scale(0.92); opacity: 0; }
      to { transform: scale(1); opacity: 1; }
    }

    .lightbox-close {
      position: absolute;
      top: 24px;
      right: 28px;
      background: rgba(255, 255, 255, 0.12);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #ffffff;
      width: 42px;
      height: 42px;
      border-radius: 50%;
      font-size: 1.2rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.2s ease, transform 0.2s ease;
    }

    .lightbox-close:hover {
      background: rgba(232, 134, 84, 0.85);
      transform: scale(1.08);
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
    @media (max-width: 768px) {
      .history-sidebar {
        position: absolute;
        inset: 0 auto 0 0;
        z-index: 30;
      }
    }

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

  <!-- Lightbox Modal for Full-Size Image Viewing -->
  <div class="lightbox-modal" id="lightbox-modal" onclick="closeLightbox()">
    <button type="button" class="lightbox-close" onclick="closeLightbox()" title="Close (Esc)">✕</button>
    <img src="" alt="Full Size Media" class="lightbox-content" id="lightbox-img" onclick="event.stopPropagation()" />
  </div>

  <!-- Header Nav -->
  <header>
    <div class="header-left">
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

      <button type="button" class="history-toggle-btn" onclick="toggleHistorySidebar()" title="Toggle Previous Chats Sidebar">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 8v4l3 3m6-3a9 9 0 1 1-18 0 9 9 0 0 1 18 0z"/></svg>
        History
      </button>
    </div>
    
    <div class="nav-meta">
      <button type="button" class="new-chat-btn" onclick="startNewChat()" title="Start New Chat">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
        New Chat
      </button>
      <span class="stat-badge">37 Topics • 1,445 Chunks</span>
      <div class="status-pill">
        <span class="status-dot"></span>
        <span>llama3.2:1b Grounded RAG</span>
      </div>
    </div>
  </header>

  <!-- App Body Layout with Left Previous Chats Sidebar -->
  <div class="app-body">
    <!-- Left History Sidebar -->
    <aside class="history-sidebar" id="history-sidebar">
      <div class="sidebar-header">
        <span class="sidebar-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 8v4l3 3m6-3a9 9 0 1 1-18 0 9 9 0 0 1 18 0z"/></svg>
          Previous Chats
        </span>
        <button type="button" class="clear-history-btn" onclick="clearAllHistory()" title="Clear All Saved History">Clear All</button>
      </div>
      <div class="history-list" id="history-list">
        <!-- Rendered dynamically from localStorage -->
      </div>
    </aside>

    <!-- Main Content Column -->
    <div class="main-content-col">
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
    </div>
  </div>

  <script>
    const chatStage = document.getElementById('chat-stage');
    const heroGreeting = document.getElementById('hero-greeting');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const lightboxModal = document.getElementById('lightbox-modal');
    const lightboxImg = document.getElementById('lightbox-img');
    const historySidebar = document.getElementById('history-sidebar');
    const historyList = document.getElementById('history-list');

    const STORAGE_KEY = 'wikiagent_previous_chats';
    let currentSessionId = null;
    let currentMessages = [];

    // Initialize History on Load
    document.addEventListener('DOMContentLoaded', () => {
      renderHistorySidebar();
    });

    function toggleHistorySidebar() {
      historySidebar.classList.toggle('collapsed');
    }

    function getStoredSessions() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        return raw ? JSON.parse(raw) : [];
      } catch (e) {
        console.error("Error reading localStorage:", e);
        return [];
      }
    }

    function saveStoredSessions(sessions) {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(sessions));
      } catch (e) {
        console.error("Error saving to localStorage:", e);
      }
    }

    function renderHistorySidebar() {
      const sessions = getStoredSessions();
      if (!sessions || sessions.length === 0) {
        historyList.innerHTML = '<div class="empty-history-msg">No previous chats saved</div>';
        return;
      }

      historyList.innerHTML = sessions.map(s => `
        <div class="history-item ${s.id === currentSessionId ? 'active' : ''}" onclick="loadSession('${s.id}')">
          <div class="history-item-info">
            <div class="history-item-title">${escapeHtml(s.title || 'Conversation')}</div>
            <div class="history-item-date">${s.dateStr || ''}</div>
          </div>
          <button type="button" class="history-delete-btn" onclick="deleteSession(event, '${s.id}')" title="Delete chat">✕</button>
        </div>
      `).join('');
    }

    function escapeHtml(text) {
      return text.replace(/[&<>"']/g, function(m) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[m];
      });
    }

    function saveCurrentSessionState() {
      if (currentMessages.length === 0) return;

      const sessions = getStoredSessions();
      if (!currentSessionId) {
        currentSessionId = 'chat_' + Date.now();
      }

      const firstUserMsg = currentMessages.find(m => m.role === 'user');
      const title = firstUserMsg ? firstUserMsg.text.substring(0, 30) : 'Chat Conversation';
      const now = new Date();
      const dateStr = now.toLocaleDateString() + ' ' + now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

      const existingIdx = sessions.findIndex(s => s.id === currentSessionId);
      const sessionData = {
        id: currentSessionId,
        title: title,
        dateStr: dateStr,
        messages: currentMessages
      };

      if (existingIdx >= 0) {
        sessions[existingIdx] = sessionData;
      } else {
        sessions.unshift(sessionData); // newest first
      }

      saveStoredSessions(sessions);
      renderHistorySidebar();
    }

    function loadSession(id) {
      const sessions = getStoredSessions();
      const session = sessions.find(s => s.id === id);
      if (!session) return;

      // Save current active before switching
      saveCurrentSessionState();

      currentSessionId = session.id;
      currentMessages = session.messages || [];

      // Clear chat stage
      const msgs = chatStage.querySelectorAll('.message');
      msgs.forEach(m => m.remove());
      if (heroGreeting) heroGreeting.style.display = 'none';

      // Render loaded messages
      currentMessages.forEach(m => {
        renderMessageToStage(m.text, m.role, m.sources || []);
      });

      renderHistorySidebar();
    }

    function deleteSession(e, id) {
      e.stopPropagation();
      let sessions = getStoredSessions();
      sessions = sessions.filter(s => s.id !== id);
      saveStoredSessions(sessions);

      if (currentSessionId === id) {
        startNewChat(false);
      } else {
        renderHistorySidebar();
      }
    }

    function clearAllHistory() {
      if (confirm("Are you sure you want to clear all saved previous chats?")) {
        localStorage.removeItem(STORAGE_KEY);
        startNewChat(false);
      }
    }

    function startNewChat(autoSave = true) {
      if (autoSave) {
        saveCurrentSessionState();
      }

      currentSessionId = null;
      currentMessages = [];

      const messages = chatStage.querySelectorAll('.message');
      messages.forEach(msg => msg.remove());
      
      if (heroGreeting) {
        heroGreeting.style.display = 'flex';
      }
      
      userInput.value = '';
      sendBtn.disabled = false;
      userInput.focus();
      renderHistorySidebar();
    }

    function openLightbox(src) {
      if (!src) return;
      lightboxImg.src = src;
      lightboxModal.classList.add('active');
    }

    function closeLightbox() {
      lightboxModal.classList.remove('active');
      lightboxImg.src = '';
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeLightbox();
    });

    function toggleSources(btn) {
      const dropdown = btn.nextElementSibling;
      const isHidden = dropdown.classList.toggle('hidden');
      const arrow = btn.querySelector('.arrow');
      if (arrow) arrow.textContent = isHidden ? '▸' : '▾';
    }

    function renderMessageToStage(text, role, sources = []) {
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
            <div class="answer-reference-card" onclick="openLightbox('${primaryImg}')" title="Click to view full size">
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
            ${s.image_url ? `<img src="${s.image_url}" alt="${s.source}" class="source-thumb" onclick="openLightbox('${s.image_url}')" title="Click to view full size" />` : ''}
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

    function addMessage(text, role, sources = []) {
      // Add to memory state
      currentMessages.push({ role, text, sources });
      renderMessageToStage(text, role, sources);
      saveCurrentSessionState();
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
