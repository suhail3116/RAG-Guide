from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Web UI"])

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>Fastshot — Describe an app. We'll build it.</title>
  <meta name="description" content="Fastshot turns a written description into a working app.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,100..900&display=block" rel="stylesheet">
  <style>
    :root {
      --u: min(0.06410256vw, 0.12400794vh);
      --vu: 0.09920635vh;
      --inset-top: 41; --inset-bottom: 106;
      --font-text: Inter, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      --font-display: Inter, var(--font-text);
      --brand-x:225; --brand-y:45; --mark:34; --brand-gap:12; --brand-fs:18.49;
      --links-y:50.5; --links-gap:50; --links-fs:21.69;
      --cta-x:1195; --cta-y:42; --cta-w:140; --cta-h:43; --cta-r:12; --cta-fs:15.70; --cta-dy:2;
      --hero-gap:51;
      --h1-y:323; --h1-fs:36.25; --display-ls:0.0018em;
      --nav-ls:-0.0115em; --brand-ls:-0.0154em; --cta-ls:-0.0127em; --body-ls:0.007em;
      --label-ls:normal; --model-ls:normal; --proof-ls:0.0065em;
      --w-regular:400; --w-display-wght:410; --w-medium:500; --w-semibold:600;
      --w-display:var(--w-display-wght); --w-nav:400; --w-brand:500; --w-cta:520;
      --w-body:var(--w-regular); --w-label:var(--w-medium);
      --w-model:var(--w-regular); --w-proof:480;
      --card-x:425; --card-y:413; --card-w:708; --card-h:143; --card-r:26;
      --ph-x:452; --ph-y:446; --ph-fs:9.97;
      --chips-x:444; --chips-y:505; --chip-h:30; --chip-r:9; --chip-fs:9.0; --chip-gap:5.5;
      --son-fs:10.4; --son-top:15.5; --chev-gap:6.2;
      --chev-x:1013.5; --chev-y:522.3;
      --att-x:1043.2; --att-y:515.1;
      --send-x:1084; --send-y:507; --send-d:35;
      --by-y:799; --by-fs:14.01; --logo-y:867; --logo-gap:62;
    }
    @supports (height:100dvh) {
      --u: min(0.06410256vw, 0.12400794dvh);
      --vu: 0.09920635dvh;
    }
    @media (min-width:1561px) { --inset-top:27; --inset-bottom:74; }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html, body {
      height: 100%;
      width: 100%;
      overflow: hidden;
      background: #0a0d12;
      font-family: var(--font-text);
      font-synthesis: none;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-rendering: geometricPrecision;
      color: #fff;
    }
    button, input, textarea { font: inherit; color: inherit; background: none; border: 0; }
    img, svg { display: block; }

    :focus-visible { outline: 2px solid #F8B285; outline-offset: 3px; border-radius: 4px; }

    .stage {
      position: fixed;
      inset: 0;
      overflow: hidden;
      background: #0a0d12;
    }
    .stage-video {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      z-index: 0;
    }
    .frame {
      position: absolute;
      inset: 0;
      z-index: 1;
      display: flex;
      flex-direction: column;
      padding: calc(var(--inset-top) * var(--vu)) calc(225 * var(--u)) calc(var(--inset-bottom) * var(--vu));
    }

    /* HEADER / NAV */
    header.nav {
      height: calc(43 * var(--u));
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: relative;
    }
    .brand {
      display: inline-flex;
      align-items: center;
      gap: calc(var(--brand-gap) * var(--u));
      text-decoration: none;
      color: #fff;
    }
    .mark-svg {
      width: calc(var(--mark) * var(--u));
      height: calc(var(--mark) * var(--u));
    }
    .wordmark {
      font-family: var(--font-display);
      font-size: calc(var(--brand-fs) * var(--u));
      font-weight: var(--w-brand);
      letter-spacing: var(--brand-ls);
      transform: translateY(calc(1 * var(--u)));
      font-variation-settings: "opsz" 32;
      text-shadow: 0 calc(1 * var(--u)) calc(10 * var(--u)) rgba(0,0,0,0.30);
    }
    .links {
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
      top: calc((50.5 - 41) * var(--u));
      display: flex;
      align-items: center;
      gap: calc(var(--links-gap) * var(--u));
    }
    .links a {
      font-size: calc(var(--links-fs) * var(--u));
      font-weight: var(--w-nav);
      letter-spacing: var(--nav-ls);
      line-height: 1.2;
      color: #ffffff;
      text-decoration: none;
      text-shadow: 0 calc(1 * var(--u)) calc(12 * var(--u)) rgba(0,0,0,0.32);
      transition: opacity 0.18s ease;
    }
    .links a:hover { opacity: 0.72; }

    .cta {
      width: calc(var(--cta-w) * var(--u));
      height: calc(var(--cta-h) * var(--u));
      border-radius: calc(var(--cta-r) * var(--u));
      font-size: calc(var(--cta-fs) * var(--u));
      font-weight: var(--w-cta);
      letter-spacing: var(--cta-ls);
      align-self: flex-start;
      margin-top: calc((42 - 41) * var(--u));
      background: linear-gradient(180deg, #3d3d3f 0%, #1d1d20 100%);
      box-shadow: inset 0 calc(1 * var(--u)) 0 rgba(255,255,255,0.10), 0 calc(2 * var(--u)) calc(14 * var(--u)) rgba(0,0,0,0.28);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      text-decoration: none;
      color: #fff;
      transition: filter 0.18s ease, transform 0.1s ease;
    }
    .cta span { transform: translateY(calc(var(--cta-dy) * var(--u))); }
    .cta:hover { filter: brightness(1.16); }
    .cta:active { transform: translateY(1px); }

    #menu { display: none; }
    .burger { display: none; }
    .sheet { display: none; }

    /* MAIN HERO */
    main.hero {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: calc(var(--hero-gap) * var(--vu));
      padding-bottom: calc(4 * var(--vu));
    }

    .h1 {
      font-family: var(--font-display);
      font-size: calc(var(--h1-fs) * var(--u));
      font-weight: var(--w-display);
      line-height: 1.10;
      letter-spacing: var(--display-ls);
      color: #ffffff;
      font-variation-settings: "opsz" 32;
      text-shadow: 0 calc(2 * var(--u)) calc(22 * var(--u)) rgba(0,0,0,0.30);
      text-align: center;
    }

    /* COMPOSER CARD */
    .card {
      width: calc(var(--card-w) * var(--u));
      height: calc(var(--card-h) * var(--u));
      border-radius: calc(var(--card-r) * var(--u));
      margin-right: calc(3 * var(--u));
      background: rgba(41,41,43,0.955);
      backdrop-filter: blur(calc(26 * var(--u))) saturate(112%);
      -webkit-backdrop-filter: blur(calc(26 * var(--u))) saturate(112%);
      box-shadow: inset 0 0 0 1px rgba(214,228,255,0.14), 0 calc(22 * var(--u)) calc(60 * var(--u)) rgba(0,0,0,0.30);
      position: relative;
    }

    .ph {
      position: absolute;
      left: calc((452 - 425) * var(--u));
      top: calc((446 - 413) * var(--u));
      right: calc(24 * var(--u));
      height: calc(40 * var(--u));
      color: #fff;
      font-size: calc(var(--ph-fs) * var(--u));
      font-weight: 400;
      line-height: 1.35;
      letter-spacing: var(--body-ls);
      background: transparent;
      border: none;
      outline: none;
      resize: none;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
    .ph::placeholder { color: #8B8C8E; }

    /* TOOLBAR STRIP */
    .tools {
      position: absolute;
      left: calc((444 - 425) * var(--u));
      top: calc((505 - 413) * var(--u));
      height: calc(var(--chip-h) * var(--u));
      right: calc((425 + 708 - 1134) * var(--u));
    }

    /* CHIPS */
    .chips {
      display: flex;
      align-items: center;
      gap: calc(var(--chip-gap) * var(--u));
    }
    .chip {
      height: calc(var(--chip-h) * var(--u));
      border-radius: calc(var(--chip-r) * var(--u));
      font-size: calc(var(--chip-fs) * var(--u));
      font-weight: 500;
      color: #909093;
      line-height: 1;
      background: linear-gradient(180deg, rgba(255,255,255,0.088) 0%, rgba(255,255,255,0.050) 45%, rgba(255,255,255,0.038) 100%);
      border: 1px solid rgba(255,255,255,0.05);
      display: inline-flex;
      align-items: center;
      padding: 0 calc(12 * var(--u));
      cursor: pointer;
      transition: all 0.18s ease;
      text-decoration: none;
    }
    .chip span { transform: translateY(calc(2 * var(--u))); }
    .chip:hover {
      background: linear-gradient(180deg, rgba(255,255,255,0.14), rgba(255,255,255,0.07));
      color: #c8c8cb;
    }

    /* RIGHT CLUSTER - ABSOLUTE DESKTOP */
    .right {
      position: absolute;
      inset: 0;
      pointer-events: none;
    }
    .right > * {
      position: absolute;
      pointer-events: auto;
    }

    .model-select {
      left: calc(510.2 * var(--u));
      top: calc(15.5 * var(--u));
      font-size: calc(var(--son-fs) * var(--u));
      font-weight: 400;
      color: #98999C;
      line-height: 1;
      display: inline-flex;
      align-items: center;
      gap: calc(var(--chev-gap) * var(--u));
      cursor: pointer;
      user-select: none;
    }
    .model-select:hover { color: #fff; }

    .attach {
      left: calc(599.15 * var(--u));
      top: calc(10.14 * var(--u));
      color: #A9AAAD;
      cursor: pointer;
      transition: color 0.18s ease;
    }
    .attach:hover { color: #fff; }
    .attach svg {
      width: calc(19.79 * var(--u));
      height: auto;
    }

    .send {
      left: calc(640 * var(--u));
      top: calc(2 * var(--u));
      width: calc(var(--send-d) * var(--u));
      height: calc(var(--send-d) * var(--u));
      border-radius: 50%;
      background: linear-gradient(163deg, #FBBC94 0%, #F49D70 46%, #E88654 100%);
      box-shadow: 0 calc(3 * var(--u)) calc(12 * var(--u)) rgba(210,110,60,0.34);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: filter 0.18s ease, transform 0.1s ease;
    }
    .send svg {
      width: calc(11.66 * var(--u));
      height: auto;
      fill: #fff;
    }
    .send:hover { filter: brightness(1.07); }
    .send:active { transform: scale(0.95); }

    /* FOOTER PROOF */
    footer.proof {
      flex: none;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: calc(14 * var(--vu));
    }
    .proof-caption {
      font-family: var(--font-display);
      font-size: calc(var(--by-fs) * var(--u));
      font-weight: var(--w-proof);
      letter-spacing: var(--proof-ls);
      color: rgba(255,255,255,0.95);
      font-variation-settings: "opsz" 32;
      text-shadow: 0 calc(1 * var(--u)) calc(12 * var(--u)) rgba(0,0,0,0.35);
    }
    .logos {
      display: flex;
      align-items: center;
      gap: calc(var(--logo-gap) * var(--u));
      filter: drop-shadow(0 calc(1 * var(--u)) calc(10 * var(--u)) rgba(0,0,0,0.30));
    }
    .logo-google { width: calc(96.84 * var(--u)); fill: #fff; }
    .logo-cisco { width: calc(67.29 * var(--u)); fill: #fff; }
    .logo-adobe { width: calc(88.68 * var(--u)); fill: #fff; }

    /* FLOATING RAG ANSWER CONTAINER OVERLAY */
    .rag-results-overlay {
      position: absolute;
      top: calc(100% + calc(12 * var(--u)));
      left: 0;
      width: 100%;
      max-height: calc(260 * var(--u));
      overflow-y: auto;
      background: rgba(24, 24, 27, 0.95);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: calc(16 * var(--u));
      padding: calc(16 * var(--u));
      box-shadow: 0 calc(20 * var(--u)) calc(50 * var(--u)) rgba(0,0,0,0.5);
      z-index: 20;
    }
    .rag-answer {
      font-size: calc(11 * var(--u));
      line-height: 1.5;
      color: #f8fafc;
      margin-bottom: calc(12 * var(--u));
    }
    .sources-toggle-btn {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #F49D70;
      font-size: calc(9.5 * var(--u));
      font-weight: 500;
      padding: calc(4 * var(--u)) calc(10 * var(--u));
      border-radius: calc(6 * var(--u));
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: calc(6 * var(--u));
    }
    .sources-dropdown {
      margin-top: calc(8 * var(--u));
      display: flex;
      flex-direction: column;
      gap: calc(8 * var(--u));
    }
    .source-item {
      display: flex;
      gap: calc(10 * var(--u));
      align-items: center;
      background: rgba(0, 0, 0, 0.3);
      padding: calc(8 * var(--u));
      border-radius: calc(8 * var(--u));
      border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .hidden { display: none !important; }

    /* RESPONSIVE TABLET */
    @media (min-width:600px) and (max-width:1180px) and (min-height:600px) {
      :root { --u: 1px; }
      .burger { display: none; }
      .sheet { display: none; }
      .frame {
        padding: clamp(24px,3.4vh,44px) clamp(28px,4.2vw,60px) clamp(26px,4.4vh,56px);
      }
      .h1 { font-size: clamp(27px,4.3vw,44px); line-height: 1.12; }
      .card {
        width: min(100%, clamp(516px,74vw,760px));
        height: auto;
        margin-right: 0;
        padding: clamp(15px,1.9vw,24px);
        border-radius: clamp(17px,2.1vw,26px);
        display: flex;
        flex-direction: column;
        gap: clamp(20px,3.2vh,44px);
      }
      .ph {
        position: static;
        white-space: normal;
        font-size: clamp(11px,1.35vw,14px);
        line-height: 1.4;
        width: 100%;
        height: auto;
      }
      .tools {
        position: static;
        height: auto;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: clamp(10px,1.4vw,18px);
        right: auto;
      }
      .chips { flex-wrap: nowrap; gap: clamp(6px,0.85vw,10px); }
      .chip {
        width: auto;
        height: clamp(29px,3.4vh,34px);
        padding: 0 clamp(7px,1vw,13px);
        font-size: clamp(9.6px,1.12vw,12.5px);
      }
      .right {
        position: static;
        display: flex;
        align-items: center;
        margin-left: auto;
        gap: 0;
      }
      .right > * { position: static; }
      .model-select { font-size: clamp(9.8px,1.12vw,12.5px); }
      .attach { margin-left: clamp(9px, 1.4vw, 20px); }
      .send {
        margin-left: clamp(9px, 1.3vw, 18px);
        width: clamp(32px, 3.5vw, 38px);
        height: clamp(32px, 3.5vw, 38px);
      }
      footer.proof { gap: clamp(15px,2.5vh,30px); }
    }

    /* RESPONSIVE PHONE / COMPACT */
    @media (max-width:599px), (max-height:599px) and (max-width:1180px) {
      :root { --u: 1px; }
      .links, header.nav .cta { display: none; }
      .burger {
        display: flex;
        width: 38px;
        height: 38px;
        border-radius: 11px;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.14);
        align-items: center;
        justify-content: center;
        cursor: pointer;
      }
      #menu:checked ~ header .sheet {
        grid-template-rows: 1fr;
      }
      .sheet {
        display: grid;
        grid-template-rows: 0fr;
        transition: grid-template-rows 0.32s cubic-bezier(.4,0,.2,1);
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        z-index: 50;
      }
      .sheet-inner {
        overflow: hidden;
        background: rgba(24,24,27,0.86);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.09);
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }
      .sheet-inner a {
        color: #fff;
        text-decoration: none;
        font-size: 15px;
      }
      .sheet-inner .cta {
        display: flex;
        height: 40px;
        width: 100%;
        border-radius: 11px;
        font-size: 15px;
        margin-top: 0;
      }
      .frame {
        padding:
          max(18px, env(safe-area-inset-top))
          max(clamp(18px,5.2vw,40px), env(safe-area-inset-right))
          max(20px, env(safe-area-inset-bottom))
          max(clamp(18px,5.2vw,40px), env(safe-area-inset-left));
      }
      .h1 {
        width: 100%;
        max-width: 15ch;
        font-size: clamp(29px,7.6vw,50px);
        line-height: 1.14;
        letter-spacing: -0.012em;
      }
      .card {
        width: 100%;
        max-width: 600px;
        height: auto;
        display: flex;
        flex-direction: column;
        gap: clamp(16px,4.6vh,34px);
        padding: clamp(13px,3.4vw,18px);
      }
      .ph {
        position: static;
        white-space: nowrap;
        text-overflow: ellipsis;
        font-size: clamp(9.4px,2.95vw,14px);
        width: 100%;
        height: auto;
      }
      .tools {
        position: static;
        height: auto;
        display: flex;
        flex-direction: column;
        align-items: stretch;
        gap: 12px;
        right: auto;
      }
      .chips { flex-wrap: wrap; }
      .right {
        position: static;
        display: flex;
        align-items: center;
        justify-content: flex-start;
      }
      .right > * { position: static; }
      .attach { margin-left: auto; }
      .send { margin-left: 14px; width: 40px; height: 40px; }
    }

    @media (max-width:1180px) and (max-height:560px) {
      main.hero { gap: 16px; }
      .h1 { font-size: clamp(24px,5.4vh,34px); }
      footer.proof { gap: 10px; }
      .frame { padding-top: 10px; }
    }

    /* ENTRANCE ANIMATIONS */
    html.anim .brand { animation: e-settle-down 0.58s cubic-bezier(.22,1,.36,1) 0.06s both; }
    html.anim .mark-svg { animation: e-mark 0.62s cubic-bezier(.16,1,.3,1) 0.06s both; }
    html.anim .links a:nth-child(1) { animation: e-settle-down 0.50s cubic-bezier(.22,1,.36,1) 0.16s both; }
    html.anim .links a:nth-child(2) { animation: e-settle-down 0.50s cubic-bezier(.22,1,.36,1) 0.21s both; }
    html.anim .links a:nth-child(3) { animation: e-settle-down 0.50s cubic-bezier(.22,1,.36,1) 0.26s both; }
    html.anim .links a:nth-child(4) { animation: e-settle-down 0.50s cubic-bezier(.22,1,.36,1) 0.31s both; }
    html.anim header.nav .cta { animation: e-settle-down 0.55s cubic-bezier(.22,1,.36,1) 0.34s both; }
    html.anim .h1 { animation: e-focus 1.00s cubic-bezier(.16,1,.3,1) 0.30s both; will-change: transform, opacity; }
    html.anim .card { animation: e-panel 0.90s cubic-bezier(.16,1,.3,1) 0.62s both; will-change: transform, opacity; }
    html.anim .ph { animation: e-populate 0.50s cubic-bezier(.22,1,.36,1) 0.88s both; }
    html.anim .chips { animation: e-populate 0.50s cubic-bezier(.22,1,.36,1) 0.94s both; }
    html.anim .right { animation: e-populate 0.50s cubic-bezier(.22,1,.36,1) 1.00s both; }
    html.anim .send { animation: e-send 0.50s cubic-bezier(.16,1,.3,1) 1.00s both; }
    html.anim .proof-caption { animation: e-settle-up 0.55s cubic-bezier(.22,1,.36,1) 1.08s both; }
    html.anim .logo-google { animation: e-settle-up 0.55s cubic-bezier(.22,1,.36,1) 1.16s both; }
    html.anim .logo-cisco { animation: e-settle-up 0.55s cubic-bezier(.22,1,.36,1) 1.22s both; }
    html.anim .logo-adobe { animation: e-settle-up 0.55s cubic-bezier(.22,1,.36,1) 1.28s both; }

    @keyframes e-settle-down {
      from { opacity: 0; transform: translateY(calc(-5 * var(--u))); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes e-settle-up {
      from { opacity: 0; transform: translateY(calc(6 * var(--u))); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes e-mark {
      from { transform: scale(0.9); }
      to { transform: scale(1); }
    }
    @keyframes e-focus {
      from { opacity: 0; transform: translateY(calc(14 * var(--u))); filter: blur(calc(6 * var(--u))); }
      to { opacity: 1; transform: translateY(0); filter: blur(0); }
    }
    @keyframes e-panel {
      from { opacity: 0; transform: translateY(calc(18 * var(--u))) scale(0.985); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }
    @keyframes e-populate {
      from { opacity: 0; transform: translateY(calc(4 * var(--u))); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes e-send {
      from { transform: scale(0.82); }
      to { transform: scale(1); }
    }

    @media (prefers-reduced-motion: reduce) {
      html.anim * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
    }
  </style>
  <script>
    if (window.matchMedia('(prefers-reduced-motion: no-preference)').matches) {
      document.documentElement.classList.add('anim');
    }
  </script>
</head>
<body>
  <input type="checkbox" id="menu">
  
  <div class="stage">
    <video class="stage-video" autoplay muted loop playsinline src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260826_124724_bc041163-d651-425f-aea3-2acc1efc2c96.mp4"></video>
    
    <div class="frame">
      <header class="nav">
        <a href="#" class="brand" aria-label="Fastshot home">
          <svg class="mark-svg" viewBox="0 0 34 34" fill="none">
            <circle cx="17" cy="17" r="17" fill="#9C86CE"/>
            <circle cx="17" cy="17" r="8.6" fill="#FFFFFF"/>
            <circle cx="17" cy="17" r="3.7" fill="#151519"/>
          </svg>
          <span class="wordmark">Fastshot</span>
        </a>

        <nav class="links">
          <a href="#">Features</a>
          <a href="#">Examples</a>
          <a href="#">Pricing</a>
          <a href="#">Docs</a>
        </nav>

        <a href="#" class="cta"><span>Get Started</span></a>

        <label for="menu" class="burger" aria-label="Open menu">
          <svg width="17" height="12" viewBox="0 0 17 12" fill="none">
            <path d="M0 1H17M0 11H17" stroke="white" stroke-width="2"/>
          </svg>
        </label>

        <div class="sheet">
          <div class="sheet-inner">
            <a href="#">Features</a>
            <a href="#">Examples</a>
            <a href="#">Pricing</a>
            <a href="#">Docs</a>
            <a href="#" class="cta"><span>Get Started</span></a>
          </div>
        </div>
      </header>

      <main class="hero">
        <h1 class="h1">Describe an app. We'll build it.</h1>

        <form class="card" id="chat-form" onsubmit="handleSubmit(event)">
          <input type="text" class="ph" id="user-input" placeholder="Build a fintech tracking app with bank level privacy and..." autocomplete="off" required />

          <div class="tools">
            <div class="chips">
              <button type="button" class="chip" onclick="ask('What is Python?')">
                <span>Attach Screens</span>
              </button>
              <button type="button" class="chip" onclick="ask('What is React and components?')">
                <span>Attach a Figma</span>
              </button>
              <button type="button" class="chip" onclick="ask('What is an AI agent?')">
                <span>Today's Theme</span>
              </button>
            </div>

            <div class="right">
              <div class="model-select">
                <span>Sonnet 4.5</span>
                <svg width="7" height="4" viewBox="0 0 7 4" fill="none">
                  <path d="M0.5 0.5L3.5 3.5L6.5 0.5" stroke="currentColor" stroke-width="1.2"/>
                </svg>
              </div>

              <div class="attach" aria-label="Attach file">
                <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M14.5 7.5L8.2 13.8C7.2 14.8 5.6 14.8 4.6 13.8C3.6 12.8 3.6 11.2 4.6 10.2L11 3.8C12.4 2.4 14.6 2.4 16 3.8C17.4 5.2 17.4 7.4 16 8.8L9.5 15.3C7.6 17.2 4.4 17.2 2.5 15.3C0.6 13.4 0.6 10.2 2.5 8.3L8.5 2.3"/>
                </svg>
              </div>

              <button type="submit" class="send" id="send-btn" aria-label="Build it">
                <svg viewBox="0 0 12 12" fill="currentColor">
                  <path d="M6 1L11 6L9.6 7.4L7 4.8V11H5V4.8L2.4 7.4L1 6L6 1Z"/>
                </svg>
              </button>
            </div>
          </div>

          <div id="rag-results-container" class="rag-results-overlay hidden">
            <div id="rag-answer" class="rag-answer"></div>
            <div id="rag-sources"></div>
          </div>
        </form>
      </main>

      <footer class="proof">
        <div class="proof-caption">Built by engineers from</div>
        <div class="logos">
          <!-- Google SVG -->
          <svg class="logo-google" viewBox="0 0 97 32">
            <path d="M12.5 14.4v3.5h8.4c-.3 2.1-2.4 6.1-8.4 6.1-5.1 0-9.2-4.2-9.2-9.4s4.1-9.4 9.2-9.4c2.9 0 4.9 1.2 6 2.3l2.8-2.7C19.5 3.2 16.3 2 12.5 2 6.7 2 2 6.7 2 12.5S6.7 23 12.5 23c6 0 10-4.2 10-10.2 0-.7-.1-1.3-.2-1.9h-9.8z"/>
          </svg>
          <!-- Cisco SVG -->
          <svg class="logo-cisco" viewBox="0 0 68 32">
            <path d="M5 20h4v10H5V20zm14-8h4v18h-4V12zm14-8h4v26h-4V4zm14 8h4v18h-4V12zm14 8h4v10h-4V20z"/>
          </svg>
          <!-- Adobe SVG -->
          <svg class="logo-adobe" viewBox="0 0 89 32">
            <path d="M0 0h28v32H0V0zm38 0h14l14 32H52l-3-8H41l-3 8H24L38 0zm43 0h16v32H81V0z"/>
          </svg>
        </div>
      </footer>
    </div>
  </div>

  <script>
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const resultsContainer = document.getElementById('rag-results-container');
    const answerDiv = document.getElementById('rag-answer');
    const sourcesDiv = document.getElementById('rag-sources');

    setTimeout(() => {
      document.documentElement.classList.remove('anim');
    }, 2600);

    function toggleSources(btn) {
      const dropdown = btn.nextElementSibling;
      const isHidden = dropdown.classList.toggle('hidden');
      const arrow = btn.querySelector('.arrow');
      if (arrow) arrow.textContent = isHidden ? '▸' : '▾';
    }

    async function ask(query) {
      userInput.value = query;
      handleSubmit(new Event('submit'));
    }

    async function handleSubmit(e) {
      if (e) e.preventDefault();
      const q = userInput.value.trim();
      if (!q) return;

      sendBtn.disabled = true;
      resultsContainer.classList.remove('hidden');
      answerDiv.innerHTML = '<i style="color: #909093;">Searching knowledge base & generating answer...</i>';
      sourcesDiv.innerHTML = '';

      try {
        const res = await fetch('/chat/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: q, top_k: 2 })
        });
        const data = await res.json();

        if (res.ok) {
          answerDiv.innerHTML = data.answer.replace(/\\n/g, '<br>');
          
          if (data.sources && data.sources.length > 0) {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'sources-toggle-btn';
            btn.innerHTML = `<span>📚 Sources (${data.sources.length})</span> <span class="arrow">▸</span>`;
            btn.onclick = () => toggleSources(btn);
            sourcesDiv.appendChild(btn);

            const dropdown = document.createElement('div');
            dropdown.className = 'sources-dropdown hidden';
            dropdown.innerHTML = data.sources.map((s, idx) => `
              <div class="source-item">
                ${s.image_url ? `<img src="${s.image_url}" alt="${s.source}" style="width: 48px; height: 48px; object-fit: cover; border-radius: 6px;" />` : ''}
                <div style="flex: 1;">
                  <div style="font-weight: 600; font-size: 13px;">
                    ${idx + 1}. <a href="${s.url || '#'}" target="_blank" rel="noopener" style="color: #F49D70; text-decoration: none;">${s.source || 'Wikipedia'} ↗</a>
                  </div>
                  <div style="font-size: 11px; color: #909093;">"${(s.chunk_preview || '').substring(0, 140)}..."</div>
                </div>
              </div>
            `).join('');
            sourcesDiv.appendChild(dropdown);
          }
        } else {
          answerDiv.innerHTML = `<span style="color: #ef4444;">Error: ${data.detail || 'Service unavailable'}</span>`;
        }
      } catch (err) {
        answerDiv.innerHTML = `<span style="color: #ef4444;">Connection error: ${err.message}</span>`;
      } finally {
        sendBtn.disabled = false;
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
