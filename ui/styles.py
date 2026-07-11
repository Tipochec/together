CSS = r"""

  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:-apple-system,'Segoe UI',sans-serif;background:#0f0f13;color:#e8e6f0;height:100vh;overflow:hidden;user-select:none}
  .titlebar{height:40px;background:#0f0f13;display:flex;align-items:center;padding:0 16px;
    -webkit-app-region:drag;border-bottom:0.5px solid rgba(255,255,255,0.06);justify-content:space-between}
  .titlebar-title{font-size:13px;color:rgba(255,255,255,0.4);display:flex;align-items:center;gap:8px}
  .heart{color:#d4537e}
  .titlebar-btns{-webkit-app-region:no-drag;display:flex;gap:4px}
  .titlebar-close{width:28px;height:28px;border-radius:6px;border:none;
    background:transparent;color:rgba(255,255,255,0.3);cursor:pointer;font-size:15px;
    display:flex;align-items:center;justify-content:center;transition:all .15s}
  .titlebar-close:hover{background:rgba(255,255,255,0.07);color:rgba(255,255,255,0.7)}
  .content{padding:16px;height:calc(100vh - 40px);overflow-y:auto}
  .cards{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px}
  .card{background:#1a1820;border:0.5px solid rgba(255,255,255,0.07);border-radius:14px;
    padding:14px;border-top:2.5px solid transparent;transition:opacity .3s,filter .3s}
  .card-you{border-top-color:#534ab7}.card-her{border-top-color:#d4537e}
  .offline-card{opacity:.4;filter:grayscale(40%)}
  .avatar{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;
    justify-content:center;font-weight:600;font-size:13px;margin-bottom:10px}
  .avatar-you{background:rgba(83,74,183,0.2);color:#a89ef0}
  .avatar-her{background:rgba(212,83,126,0.2);color:#e891b0}
  .card-label{font-size:10px;color:rgba(255,255,255,0.25);margin-bottom:4px;
    text-transform:uppercase;letter-spacing:.05em}
  .card-app{font-size:14px;font-weight:500;color:#f0eeff;margin-bottom:3px;
    word-break:break-word;line-height:1.3;max-height:2.6em;overflow:hidden}
  .card-title{font-size:11px;color:rgba(255,255,255,0.3);
    word-break:break-word;line-height:1.3;max-height:2.6em;overflow:hidden;min-height:14px}
  .card-time{font-size:10px;color:rgba(255,255,255,0.2);margin-top:6px}
  .badge{display:inline-flex;align-items:center;gap:4px;font-size:10px;
    padding:2px 8px;border-radius:20px;margin-top:6px}
  .badge-gaming{background:rgba(83,74,183,0.2);color:#a89ef0}
  .badge-browser{background:rgba(23,100,165,0.2);color:#7ab8ef}
  .badge-chat{background:rgba(29,158,117,0.2);color:#5ddaaa}
  .badge-music{background:rgba(186,117,23,0.2);color:#f0b352}
  .badge-video{background:rgba(162,45,45,0.2);color:#f08080}
  .badge-work{background:rgba(99,152,34,0.2);color:#a8d865}
  .badge-idle,.badge-other,.badge-streaming{background:rgba(100,100,100,0.15);color:rgba(255,255,255,0.3)}
  .status-row{display:flex;align-items:center;gap:6px;margin-bottom:14px}
  .dot{width:7px;height:7px;border-radius:50%;flex-shrink:0}
  .dot-online{background:#1d9e75;box-shadow:0 0 6px #1d9e75}
  .dot-waiting{background:#b87c1a;box-shadow:0 0 6px #b87c1a}
  .status-text{font-size:12px;color:rgba(255,255,255,0.3)}
  .history-cols{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:8px}
  .history-col-title{font-size:10px;color:rgba(255,255,255,0.2);text-transform:uppercase;
    letter-spacing:.06em;margin-bottom:6px}
  .section-title{font-size:10px;color:rgba(255,255,255,0.2);
    text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px}
  .timeline{display:flex;flex-direction:column;gap:5px}
  .tl-item{display:flex;align-items:flex-start;gap:8px;padding:7px 10px;
    background:#1a1820;border-radius:9px;border:0.5px solid rgba(255,255,255,0.05)}
  .tl-dot{width:5px;height:5px;border-radius:50%;flex-shrink:0;margin-top:4px}
  .tl-dot-you{background:#534ab7}.tl-dot-her{background:#d4537e}
  .tl-time{font-size:11px;color:rgba(255,255,255,0.2);min-width:36px;flex-shrink:0}
  .tl-app{font-size:12px;color:rgba(255,255,255,0.6);word-break:break-word;line-height:1.4}
  @keyframes slideIn{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:translateY(0)}}
  .tl-item-new{animation:slideIn 0.25s ease}
  @keyframes fadeUpdate{0%{background:rgba(83,74,183,0.15)}100%{background:#1a1820}}
  .card-updated{animation:fadeUpdate 0.8s ease}
  #page-settings,#page-stats{display:none}
  .settings-row{display:flex;justify-content:space-between;align-items:center;
    padding:11px 0;border-bottom:0.5px solid rgba(255,255,255,0.05);font-size:13px}
  .settings-label{color:rgba(255,255,255,0.55)}
  input.si{background:#1a1820;border:0.5px solid rgba(255,255,255,0.1);border-radius:6px;
    padding:4px 10px;color:#e8e6f0;font-size:12px;width:140px;outline:none}
  input.si:focus{border-color:rgba(83,74,183,0.5)}
  .toggle{position:relative;width:36px;height:20px;flex-shrink:0}
  .toggle input{opacity:0;width:0;height:0}
  .toggle-slider{position:absolute;cursor:pointer;inset:0;background:rgba(255,255,255,0.1);
    border-radius:20px;transition:.2s}
  .toggle-slider:before{content:'';position:absolute;width:14px;height:14px;left:3px;bottom:3px;
    background:rgba(255,255,255,0.4);border-radius:50%;transition:.2s}
  .toggle input:checked+.toggle-slider{background:rgba(83,74,183,0.6)}
  .toggle input:checked+.toggle-slider:before{transform:translateX(16px);background:#a89ef0}
  .btn{padding:7px 14px;border-radius:8px;border:0.5px solid rgba(255,255,255,0.1);
    background:rgba(255,255,255,0.05);color:rgba(255,255,255,0.55);cursor:pointer;
    font-size:12px;transition:all .15s}
  .btn:hover{background:rgba(255,255,255,0.09)}
  .btn-primary{background:rgba(83,74,183,0.2);border-color:rgba(83,74,183,0.4);color:#a89ef0}
  .btn-primary:hover{background:rgba(83,74,183,0.3)}
  .btn-danger{border-color:rgba(212,83,126,0.3);color:#d4537e}
  .btn-danger:hover{background:rgba(212,83,126,0.1)}
  .nav{display:flex;gap:4px;margin-bottom:16px}
  .nav-btn{flex:1;padding:6px;border-radius:8px;border:none;background:transparent;
    color:rgba(255,255,255,0.3);cursor:pointer;font-size:12px;transition:all .15s}
  .nav-btn.active{background:rgba(255,255,255,0.07);color:rgba(255,255,255,0.8)}
  ::-webkit-scrollbar{width:3px}
  ::-webkit-scrollbar-track{background:transparent}
  ::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.08);border-radius:2px}
    .titlebar-btn{
        width:28px;
        height:28px;
        border:none;
        border-radius:6px;
        background:transparent;
        color:rgba(255,255,255,.3);
        cursor:pointer;
        font-size:15px;
        display:flex;
        align-items:center;
        justify-content:center;
        transition:.15s;
    }

    .titlebar-btn:hover{
        background:rgba(255,255,255,.07);
        color:rgba(255,255,255,.7);
    }
"""