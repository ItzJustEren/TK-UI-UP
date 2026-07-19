# pages.py - Tk-Ui v10 - کامل و بی‌نقص

LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ورود · Tk-Ui v10</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0a0a0a;--card:rgba(20,20,20,0.88);--accent:#F97316;--accent2:#FB923C;--text:#F5F5F5;--dim:#6B6B6B;--mid:#B0B0B0;--border:rgba(249,115,22,0.3);--shadow:0 8px 40px rgba(0,0,0,0.6);--glow:0 0 60px rgba(249,115,22,0.1)}
[data-theme="light"]{--bg:#f0f0f0;--card:rgba(255,255,255,0.92);--text:#1a1a1a;--dim:#888;--mid:#666;--border:rgba(249,115,22,0.3);--shadow:0 8px 30px rgba(0,0,0,0.08);--glow:0 0 40px rgba(249,115,22,0.05)}
html,body{height:100%;overflow:hidden;font-family:'Vazirmatn',sans-serif;background:var(--bg);color:var(--text);transition:background .3s}
.bg-canvas{position:fixed;inset:0;z-index:0;background:radial-gradient(ellipse 70% 50% at 50% 0%,rgba(249,115,22,0.12),transparent 65%),radial-gradient(ellipse 40% 30% at 80% 80%,rgba(251,146,60,0.06),transparent 60%),var(--bg)}
.glow{position:fixed;border-radius:50%;filter:blur(100px);z-index:0;animation:floatGlow 14s ease-in-out infinite}
.g1{width:500px;height:500px;background:rgba(249,115,22,0.08);top:-200px;right:-100px}
.g2{width:400px;height:400px;background:rgba(251,146,60,0.05);bottom:-200px;left:-100px;animation-delay:5s}
.g3{width:300px;height:300px;background:rgba(249,115,22,0.04);top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:8s}
@keyframes floatGlow{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-40px) scale(1.08)}}
.particles{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.particle{position:absolute;width:3px;height:3px;background:var(--accent);border-radius:50%;opacity:0;animation:particleFloat 12s linear infinite}
.particle:nth-child(1){left:10%;animation-delay:0s;width:2px;height:2px}
.particle:nth-child(2){left:25%;animation-delay:2s;width:4px;height:4px;background:var(--accent2)}
.particle:nth-child(3){left:40%;animation-delay:4s;width:2px;height:2px}
.particle:nth-child(4){left:55%;animation-delay:1s;width:3px;height:3px}
.particle:nth-child(5){left:70%;animation-delay:3s;width:2px;height:2px;background:var(--accent2)}
.particle:nth-child(6){left:85%;animation-delay:5s;width:4px;height:4px}
.particle:nth-child(7){left:15%;animation-delay:6s;width:2px;height:2px}
.particle:nth-child(8){left:50%;animation-delay:2.5s;width:3px;height:3px}
@keyframes particleFloat{0%{top:100%;opacity:0;transform:translateX(0)}10%{opacity:1}90%{opacity:1}100%{top:-10%;opacity:0;transform:translateX(40px)}}
.wrap{position:relative;z-index:10;display:flex;align-items:center;justify-content:center;height:100vh;padding:20px}
.card{background:var(--card);border:1px solid var(--border);border-radius:28px;padding:44px 38px 36px;max-width:420px;width:100%;backdrop-filter:blur(32px);box-shadow:var(--shadow),var(--glow);position:relative;overflow:hidden}
.card::before{content:'';position:absolute;top:-50%;right:-50%;width:200%;height:200%;background:radial-gradient(circle at 70% 30%,rgba(249,115,22,0.03),transparent 60%);pointer-events:none}
.card-border-glow{position:absolute;inset:-2px;border-radius:30px;background:linear-gradient(135deg,var(--accent),transparent 50%,var(--accent2));opacity:0.15;z-index:-1;filter:blur(4px)}
.brand{display:flex;align-items:center;gap:16px;margin-bottom:34px;position:relative}
.brand-icon{width:56px;height:56px;border-radius:16px;background:linear-gradient(135deg,#F97316,#EA580C);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:22px;box-shadow:0 0 40px rgba(249,115,22,0.35),inset 0 0 20px rgba(255,255,255,0.1);flex-shrink:0;transition:transform .3s}
.brand-icon:hover{transform:scale(1.05) rotate(-3deg)}
.brand-text{font-size:20px;font-weight:800;letter-spacing:-.02em;background:linear-gradient(135deg,#F97316,#FB923C,#EA580C);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-size:200% 200%;animation:gradientShift 4s ease-in-out infinite}
@keyframes gradientShift{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.brand-sub{font-size:11px;color:var(--dim);margin-top:2px;-webkit-text-fill-color:var(--dim)}
h1{font-size:22px;font-weight:700;margin-bottom:6px;letter-spacing:-.02em;color:var(--text)}
.sub{font-size:13px;color:var(--mid);margin-bottom:30px;line-height:1.7}
.hint{display:flex;align-items:center;gap:12px;background:rgba(249,115,22,0.06);border:1px solid rgba(249,115,22,0.12);border-radius:14px;padding:10px 16px;margin-bottom:24px;backdrop-filter:blur(8px)}
.hint-label{font-size:11px;color:var(--dim);flex:1}
.hint-val{font-family:ui-monospace,monospace;font-size:14px;font-weight:700;color:#FB923C;background:rgba(249,115,22,0.12);border:1px solid rgba(249,115,22,0.2);padding:4px 14px;border-radius:9px;cursor:pointer;transition:.2s}
.hint-val:hover{background:rgba(249,115,22,0.25);box-shadow:0 0 20px rgba(249,115,22,0.15)}
.field{margin-bottom:20px}
.field label{display:block;font-size:11px;font-weight:600;color:var(--dim);margin-bottom:6px;text-transform:uppercase;letter-spacing:.08em}
.inp-wrap{position:relative}
input[type=password]{width:100%;padding:14px 48px 14px 16px;border-radius:14px;border:1.5px solid var(--border);background:rgba(0,0,0,0.25);color:var(--text);font-family:inherit;font-size:14px;outline:none;transition:.25s}
input[type=password]:focus{border-color:#FB923C;box-shadow:0 0 0 4px rgba(249,115,22,0.12),var(--glow);background:rgba(0,0,0,0.35)}
.ic{position:absolute;left:16px;top:50%;transform:translateY(-50%);color:var(--dim);font-size:18px;pointer-events:none;transition:.25s}
input:focus~.ic{color:var(--accent2)}
.err{display:none;background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.2);border-radius:12px;padding:10px 14px;margin-bottom:14px;font-size:12px;color:#F87171;align-items:center;gap:8px;animation:shake .4s ease}
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
.err.show{display:flex}
.btn{width:100%;padding:15px;border-radius:14px;border:none;cursor:pointer;background:linear-gradient(135deg,#F97316,#EA580C);color:#fff;font-family:inherit;font-size:14px;font-weight:700;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 28px rgba(249,115,22,0.35);transition:.25s;position:relative;overflow:hidden}
.btn::after{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,255,255,0.15),transparent 60%);opacity:0;transition:.3s}
.btn:hover{transform:translateY(-3px);box-shadow:0 8px 40px rgba(249,115,22,0.45)}
.btn:hover::after{opacity:1}
.btn:active{transform:translateY(0) scale(.98)}
.btn:disabled{opacity:.5;cursor:not-allowed;transform:none}
.footer{margin-top:26px;padding-top:20px;border-top:1px solid var(--border);display:flex;align-items:center;justify-content:center;gap:14px;font-size:11px;color:var(--dim);flex-wrap:wrap}
.footer a{color:#FB923C;font-weight:600;text-decoration:none;display:flex;align-items:center;gap:4px;transition:.2s}
.footer a:hover{color:#F97316;text-shadow:0 0 20px rgba(249,115,22,0.3)}
.theme-toggle{position:fixed;top:18px;left:18px;z-index:20;background:var(--card);border:1px solid var(--border);color:var(--text);width:42px;height:42px;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:20px;border:none;backdrop-filter:blur(12px);box-shadow:var(--shadow);transition:.25s}
.theme-toggle:hover{transform:rotate(30deg) scale(1.05);border-color:var(--accent2)}
@keyframes spin{to{transform:rotate(360deg)}}
@media(max-width:480px){.card{padding:28px 20px 24px}.brand-icon{width:44px;height:44px;font-size:18px}.brand-text{font-size:17px}}
</style>
</head>
<body>
<div class="bg-canvas"></div>
<div class="glow g1"></div><div class="glow g2"></div><div class="glow g3"></div>
<div class="particles">
  <div class="particle"></div><div class="particle"></div><div class="particle"></div>
  <div class="particle"></div><div class="particle"></div><div class="particle"></div>
  <div class="particle"></div><div class="particle"></div>
</div>
<button class="theme-toggle" id="themeBtn" onclick="toggleTheme()"><i class="ti ti-moon"></i></button>
<div class="wrap">
  <div class="card">
    <div class="card-border-glow"></div>
    <div class="brand">
      <div class="brand-icon">Tk</div>
      <div><div class="brand-text">Tk-Ui</div><div class="brand-sub">v10 · نئون</div></div>
    </div>
    <h1>خوش آمدید</h1>
    <p class="sub">رمز عبور را برای ورود به پنل مدیریت وارد کنید</p>
    <div class="err" id="err"><i class="ti ti-alert-circle"></i><span id="err-text"></span></div>
    <div class="hint">
      <span class="hint-label">رمز پیش‌فرض</span>
      <span class="hint-val" onclick="document.getElementById('pw').value='taakaa';document.getElementById('pw').focus()">taakaa</span>
    </div>
    <form id="form">
      <div class="field">
        <label>رمز عبور</label>
        <div class="inp-wrap">
          <input type="password" id="pw" placeholder="••••••••" autofocus required>
          <i class="ti ti-lock ic"></i>
        </div>
      </div>
      <button class="btn" type="submit" id="btn"><i class="ti ti-login-2"></i> ورود به پنل</button>
    </form>
    <div class="footer">
      <span>پشتیبانی: <a href="https://t.me/ItzJustEren" target="_blank"><i class="ti ti-brand-telegram"></i>@ItzJustEren</a></span>
      <span>کانال: <a href="https://t.me/TaaKaaOrg" target="_blank"><i class="ti ti-brand-telegram"></i>@TaaKaaOrg</a></span>
    </div>
  </div>
</div>
<script>
let isDark = localStorage.getItem('tk-theme') !== 'light';
function applyTheme(dark){document.documentElement.setAttribute('data-theme',dark?'dark':'light');document.getElementById('themeBtn').innerHTML='<i class="ti '+(dark?'ti-moon':'ti-sun')+'"></i>'}
function toggleTheme(){isDark=!isDark;localStorage.setItem('tk-theme',isDark?'dark':'light');applyTheme(isDark)}
applyTheme(isDark);
document.getElementById('form').addEventListener('submit',async e=>{
  e.preventDefault();
  const btn=document.getElementById('btn'),err=document.getElementById('err'),et=document.getElementById('err-text');
  err.classList.remove('show');btn.disabled=true;
  btn.innerHTML='<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i> در حال ورود...';
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:document.getElementById('pw').value})});
    if(!r.ok){const d=await r.json().catch(()=>({}));throw new Error(d.detail||'خطا');}
    location.href='/dashboard';
  }catch(e){
    et.textContent=e.message;err.classList.add('show');
    btn.disabled=false;btn.innerHTML='<i class="ti ti-login-2"></i> ورود به پنل';
  }
});
</script>
</body></html>"""

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tk-Ui v10 · پنل مدیریت</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
:root{--bg:#0a0a0a;--bg2:#121212;--bg3:#1a1a1a;--card:rgba(26,26,26,0.85);--card-b:rgba(249,115,22,0.2);--card-bh:rgba(249,115,22,0.45);--accent:#F97316;--accent2:#FB923C;--accent-d:rgba(249,115,22,0.1);--green:#34D399;--green-bg:rgba(52,211,153,0.1);--green-t:#34D399;--red:#F87171;--red-bg:rgba(248,113,113,0.1);--red-t:#F87171;--amber:#FBBF24;--amber-bg:rgba(251,191,36,0.1);--amber-t:#FBBF24;--purple:#A78BFA;--purple-bg:rgba(167,139,250,0.1);--t1:#F5F5F5;--t2:#B0B0B0;--t3:#6B6B6B;--sidebar-w:260px;--radius:16px;--shadow:0 8px 32px rgba(0,0,0,0.5);--glow:0 0 40px rgba(249,115,22,0.12)}
[data-theme="light"]{--bg:#f0f0f0;--bg2:#e8e8e8;--bg3:#ddd;--card:rgba(255,255,255,0.9);--card-b:rgba(249,115,22,0.2);--card-bh:rgba(249,115,22,0.4);--accent:#EA580C;--accent2:#F97316;--accent-d:rgba(234,88,12,0.08);--green:#059669;--green-bg:rgba(5,150,105,0.08);--green-t:#065F46;--red:#DC2626;--red-bg:rgba(220,38,38,0.08);--red-t:#991B1B;--amber:#D97706;--amber-bg:rgba(217,119,6,0.08);--amber-t:#92400E;--purple:#7C3AED;--purple-bg:rgba(124,58,237,0.08);--t1:#1a1a1a;--t2:#444;--t3:#777;--shadow:0 8px 24px rgba(0,0,0,0.08);--glow:0 0 30px rgba(234,88,12,0.05)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;font-family:'Vazirmatn',sans-serif;background:var(--bg);color:var(--t1);font-size:14px;transition:background .3s,color .3s}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--bg3);border-radius:3px}
a{color:inherit;text-decoration:none}
.sidebar{width:var(--sidebar-w);min-height:100vh;background:var(--card);backdrop-filter:blur(24px);border-left:1px solid var(--card-b);display:flex;flex-direction:column;flex-shrink:0;position:fixed;right:0;top:0;bottom:0;z-index:200;transition:transform .3s cubic-bezier(.4,0,.2,1),background .3s}
.logo{display:flex;align-items:center;gap:12px;padding:24px 20px 16px;border-bottom:1px solid var(--card-b)}
.logo-icon{width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,#F97316,#EA580C);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:18px;box-shadow:0 0 30px rgba(249,115,22,0.35)}
.logo-name{font-size:15px;font-weight:800;background:linear-gradient(135deg,#F97316,#FB923C);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.logo-sub{font-size:10px;color:var(--t3);margin-top:1px;-webkit-text-fill-color:var(--t3)}
.sb-close{display:none;position:absolute;left:12px;top:20px;background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:30px;height:30px;border-radius:8px;font-size:16px;align-items:center;justify-content:center;cursor:pointer}
.nav-wrap{flex:1;overflow-y:auto;padding:10px 0 8px}
.nav-sec{padding:14px 20px 6px;font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:var(--t3);font-weight:700}
.nav-it{display:flex;align-items:center;gap:10px;padding:10px 18px;color:var(--t3);font-size:12.5px;cursor:pointer;border-right:2px solid transparent;transition:all .15s;margin:1px 8px;border-radius:0 8px 8px 0}
.nav-it i{font-size:17px;width:20px;text-align:center;flex-shrink:0}
.nav-it:hover{background:var(--accent-d);color:var(--t2)}
.nav-it.on{background:var(--accent-d);color:var(--t1);border-right-color:var(--accent);font-weight:600}
.nav-badge{margin-right:auto;background:var(--accent-d);color:var(--accent2);font-size:9px;padding:1px 8px;border-radius:20px;font-weight:700}
.sb-foot{padding:14px 18px;border-top:1px solid var(--card-b);display:flex;flex-direction:column;gap:6px}
.tg-btn{display:flex;align-items:center;justify-content:center;gap:8px;background:linear-gradient(135deg,#F97316,#EA580C);color:#fff;border-radius:10px;padding:10px;font-size:12.5px;font-weight:600;font-family:inherit;border:none;cursor:pointer;width:100%;transition:.15s}
.tg-btn:hover{filter:brightness(1.1)}
.theme-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:var(--accent-d);color:var(--t2);border-radius:9px;padding:8px;font-size:12px;font-weight:500;font-family:inherit;border:1px solid var(--card-b);cursor:pointer;width:100%;transition:.15s}
.theme-btn:hover{background:var(--card-b);color:var(--t1)}
.logout-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:var(--red-bg);color:var(--red-t);border-radius:9px;padding:8px;font-size:12px;font-weight:500;font-family:inherit;border:1px solid rgba(248,113,113,0.2);cursor:pointer;width:100%;transition:.15s}
.logout-btn:hover{background:rgba(248,113,113,0.2)}
.mob-top{display:none;position:fixed;top:0;right:0;left:0;height:54px;background:var(--card);backdrop-filter:blur(12px);border-bottom:1px solid var(--card-b);z-index:150;align-items:center;justify-content:space-between;padding:0 14px}
.mob-logo{width:32px;height:32px;border-radius:10px;background:linear-gradient(135deg,#F97316,#EA580C);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:15px}
.mob-title{font-size:14px;font-weight:700;background:linear-gradient(135deg,#F97316,#FB923C);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.mob-right{display:flex;gap:6px}
.menu-btn,.theme-mob{background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:34px;height:34px;border-radius:8px;font-size:17px;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:.15s}
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:190;backdrop-filter:blur(4px)}
.overlay.show{display:block}
.main{margin-right:var(--sidebar-w);flex:1;padding:28px 32px 60px;min-width:0;transition:margin .25s}
.pg{display:none}
.pg.on{display:block;animation:fade .2s ease}
@keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.topbar{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:24px;flex-wrap:wrap;gap:12px}
.tb-title{font-size:20px;font-weight:800;color:var(--t1);display:flex;align-items:center;gap:8px;letter-spacing:-.02em}
.tb-title i{color:var(--accent);font-size:22px}
.tb-sub{font-size:12px;color:var(--t3);margin-top:4px}
.tb-right{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.badge{font-size:10px;padding:4px 12px;border-radius:20px;font-weight:700;display:inline-flex;align-items:center;gap:5px;white-space:nowrap}
.bg-green{background:var(--green-bg);color:var(--green-t)}
.bg-blue{background:var(--accent-d);color:var(--accent2)}
.bg-amber{background:var(--amber-bg);color:var(--amber-t)}
.bg-red{background:var(--red-bg);color:var(--red-t)}
.bg-purple{background:var(--purple-bg);color:var(--purple)}
.dot{width:7px;height:7px;border-radius:50%;flex-shrink:0;display:inline-block}
.dg{background:var(--green)}.dr{background:var(--red)}.da{background:var(--amber)}.db{background:var(--accent)}
.pulse{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:22px}
.metric{background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:18px 18px 14px;transition:all .25s;position:relative;overflow:hidden;backdrop-filter:blur(12px)}
.metric:hover{border-color:var(--card-bh);transform:translateY(-3px);box-shadow:var(--glow),var(--shadow)}
.metric::after{content:'';position:absolute;top:0;right:0;width:4px;height:100%;background:linear-gradient(180deg,var(--accent),#EA580C);opacity:0;transition:.2s}
.metric:hover::after{opacity:1}
.metric .m-icon{width:40px;height:40px;border-radius:12px;background:var(--accent-d);display:flex;align-items:center;justify-content:center;margin-bottom:12px;color:var(--accent);font-size:20px}
.metric .m-icon.green{background:var(--green-bg);color:var(--green-t)}
.metric .m-icon.pink{background:rgba(236,72,153,0.1);color:#EC4899}
.metric .m-icon.amber{background:var(--amber-bg);color:var(--amber-t)}
.m-label{font-size:10px;color:var(--t3);font-weight:600;text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px}
.m-val{font-size:26px;font-weight:800;color:var(--t1);line-height:1;letter-spacing:-.02em}
.m-unit{font-size:13px;font-weight:400;color:var(--t3)}
.m-sub{font-size:10px;color:var(--t3);margin-top:6px;display:flex;align-items:center;gap:3px}
.card{background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:18px 20px;transition:border-color .2s,background .3s;backdrop-filter:blur(12px)}
.card:hover{border-color:var(--card-bh)}
.card-title{font-size:13px;font-weight:700;color:var(--t1);margin-bottom:16px;display:flex;align-items:center;gap:8px}
.card-title i{font-size:17px;color:var(--accent)}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:18px}
.g3{display:grid;grid-template-columns:2fr 1fr;gap:14px;margin-bottom:18px}
.ch{height:220px}
.ch-sm{height:180px}
.ch-lg{height:300px}
.vless-box{background:linear-gradient(135deg,var(--card),var(--bg3));border:1px solid var(--card-b);border-radius:20px;padding:22px 24px;margin-bottom:20px;position:relative;overflow:hidden;box-shadow:var(--shadow)}
.vless-box::before{content:'';position:absolute;top:-80px;right:-80px;width:250px;height:250px;background:radial-gradient(circle,rgba(249,115,22,0.08),transparent 70%);pointer-events:none}
.vl-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;flex-wrap:wrap;gap:8px}
.vl-title{font-size:12px;color:var(--t2);display:flex;align-items:center;gap:6px;font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.vl-title i{color:var(--accent);font-size:16px}
.vl-code{background:rgba(0,0,0,0.3);border:1px solid var(--card-b);border-radius:12px;padding:12px 16px;font-size:11px;font-family:ui-monospace,monospace;color:var(--accent2);word-break:break-all;line-height:1.8}
.vl-actions{display:flex;gap:8px;margin-top:14px;flex-wrap:wrap}
.btn{font-family:inherit;font-size:12px;font-weight:600;border-radius:10px;padding:8px 16px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;border:none;transition:all .15s;white-space:nowrap}
.btn i{font-size:14px}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn-p{background:linear-gradient(135deg,#F97316,#EA580C);color:#fff;box-shadow:0 4px 20px rgba(249,115,22,0.35)}
.btn-p:hover{transform:translateY(-2px);box-shadow:0 6px 28px rgba(249,115,22,0.45)}
.btn-o{background:transparent;border:1px solid var(--card-b);color:var(--t2)}
.btn-o:hover{background:var(--accent-d);border-color:var(--card-bh)}
.btn-g{background:var(--accent-d);color:var(--accent2);border:1px solid rgba(249,115,22,0.15)}
.btn-g:hover{background:rgba(249,115,22,0.2)}
.btn-d{background:var(--red-bg);color:var(--red-t);border:1px solid rgba(248,113,113,0.2)}
.btn-d:hover{background:rgba(248,113,113,0.2)}
.btn-pur{background:var(--purple-bg);color:var(--purple);border:1px solid rgba(167,139,250,0.2)}
.btn-pur:hover{background:rgba(167,139,250,0.22)}
.btn-amber{background:var(--amber-bg);color:var(--amber-t);border:1px solid rgba(251,191,36,0.2)}
.btn-amber:hover{background:rgba(251,191,36,0.22)}
.btn-sm{padding:5px 10px;font-size:10.5px;border-radius:8px}
.btn-icon{width:32px;height:32px;padding:0;justify-content:center;border-radius:6px}
.sr{display:flex;align-items:center;justify-content:space-between;padding:9px 0;border-bottom:1px solid rgba(249,115,22,0.05);font-size:12px}
.sr:last-child{border-bottom:none}
.sr-k{color:var(--t2);display:flex;align-items:center;gap:6px}
.sr-k i{font-size:14px;color:var(--t3)}
.sr-v{color:var(--t1);font-weight:600;font-size:11.5px}
.spbar{height:4px;border-radius:3px;background:var(--accent-d);margin-top:4px;overflow:hidden}
.spfill{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--accent),#EA580C);transition:width .8s ease}
.badge-chip{font-size:9px;padding:2px 9px;border-radius:6px;font-weight:700;display:inline-flex;align-items:center;gap:3px}
.bc-green{background:var(--green-bg);color:var(--green-t)}
.bc-red{background:var(--red-bg);color:var(--red-t)}
.bc-amber{background:var(--amber-bg);color:var(--amber-t)}
.bc-purple{background:var(--purple-bg);color:var(--purple)}
.tog{width:20px;height:34px;border-radius:20px;background:rgba(100,116,139,0.25);position:relative;cursor:pointer;transition:.2s;flex-shrink:0;border:none}
.tog::after{content:'';position:absolute;width:14px;height:14px;border-radius:50%;background:#fff;left:3px;bottom:3px;transition:.2s;box-shadow:0 1px 4px rgba(0,0,0,0.3)}
.tog.on::after{bottom:17px}
.tog.on{background:var(--green)}
.empty{text-align:center;padding:50px 20px;color:var(--t3)}
.empty i{font-size:40px;opacity:.3;margin-bottom:12px;display:block}
.empty p{font-size:12.5px;margin-top:4px}
.cfg-grid{display:flex;flex-direction:column;gap:10px}
.cfg-card{background:var(--card);border:1px solid var(--card-b);border-radius:14px;padding:0;transition:all .2s;overflow:hidden}
.cfg-card:hover{border-color:var(--card-bh);box-shadow:var(--glow),var(--shadow)}
.cfg-row{display:flex;align-items:center;gap:16px;padding:14px 18px;flex-wrap:wrap}
.cfg-status-dot{width:10px;height:10px;border-radius:50%;background:var(--green);flex-shrink:0;box-shadow:0 0 0 3px var(--green-bg)}
.cfg-card.inactive .cfg-status-dot{background:var(--red);box-shadow:0 0 0 3px var(--red-bg)}
.cfg-card.expired .cfg-status-dot{background:var(--amber);box-shadow:0 0 0 3px var(--amber-bg)}
.cfg-identity{flex:1;min-width:150px}
.cfg-label{font-size:13.5px;font-weight:700;color:var(--t1)}
.cfg-sub-meta{font-size:10px;color:var(--t3);margin-top:2px;display:flex;gap:8px;align-items:center}
.cfg-usage-col{flex:1;min-width:120px}
.ubar{height:5px;border-radius:4px;background:rgba(249,115,22,0.08);overflow:hidden}
.ubar-f{height:100%;border-radius:4px;transition:width .5s ease}
.utxt{font-size:10px;color:var(--t3);display:flex;justify-content:space-between;margin-top:3px}
.cfg-exp-col{min-width:90px}
.cfg-badges-col{display:flex;flex-wrap:wrap;gap:4px;min-width:100px}
.proto-chip{font-size:9px;padding:2px 8px;border-radius:5px;font-weight:700}
.pc-ws{background:var(--accent-d);color:var(--accent2)}
.pc-xhttp{background:var(--purple-bg);color:var(--purple)}
.cfg-actions{display:flex;gap:4px;flex-wrap:wrap}
@media(max-width:1024px){.sidebar{transform:translateX(100%)}.sidebar.open{transform:translateX(0)}.sb-close{display:flex}.main{margin-right:0;padding-top:70px}.mob-top{display:flex}.metrics{grid-template-columns:1fr 1fr}.g2,.g3{grid-template-columns:1fr}}
@media(max-width:600px){.metrics{grid-template-columns:1fr}.main{padding:62px 12px 50px}.cfg-row{flex-direction:column;align-items:stretch}}
</style>
</head>
<body>
<div class="mob-top"><div class="ml"><div class="mob-logo">Tk</div><span class="mob-title">Tk-Ui</span></div><div class="mob-right"><button class="theme-mob" onclick="toggleTheme()"><i class="ti ti-sun"></i></button><button class="menu-btn" onclick="document.getElementById('sb').classList.add('open');document.getElementById('overlay').classList.add('show')"><i class="ti ti-menu-2"></i></button></div></div>
<div class="overlay" id="overlay" onclick="document.getElementById('sb').classList.remove('open');this.classList.remove('show')"></div>
<aside class="sidebar" id="sb"><button class="sb-close" onclick="document.getElementById('sb').classList.remove('open');document.getElementById('overlay').classList.remove('show')"><i class="ti ti-x"></i></button>
<div class="logo"><div class="logo-icon">Tk</div><div><div class="logo-name">Tk-Ui</div><div class="logo-sub">v10 · نئون</div></div></div>
<div class="nav-wrap">
<div class="nav-sec">پنل</div>
<div class="nav-it on" data-pg="overview"><i class="ti ti-dashboard"></i> داشبورد</div>
<div class="nav-it" data-pg="links"><i class="ti ti-link"></i> کانفیگ‌ها <span class="nav-badge" id="links-nb">0</span></div>
<div class="nav-it" data-pg="subgroups"><i class="ti ti-folders"></i> گروه‌ها <span class="nav-badge" id="subs-nb">0</span></div>
<div class="nav-it" data-pg="nodes"><i class="ti ti-server"></i> Node‌ها <span class="nav-badge" id="nodes-nb">0</span></div>
<div class="nav-it" data-pg="traffic"><i class="ti ti-chart-area"></i> ترافیک</div>
<div class="nav-it" data-pg="connections"><i class="ti ti-plug-connected"></i> اتصالات <span class="nav-badge" id="conns-nb">0</span></div>
<div class="nav-it" data-pg="bot"><i class="ti ti-robot"></i> ربات</div>
<div class="nav-sec">سیستم</div>
<div class="nav-it" data-pg="security"><i class="ti ti-shield-lock"></i> امنیت</div>
<div class="nav-it" data-pg="logs"><i class="ti ti-history"></i> لاگ‌ها</div>
<div class="nav-it" data-pg="errors"><i class="ti ti-alert-triangle"></i> خطاها</div>
<div class="nav-it" data-pg="settings"><i class="ti ti-settings"></i> تنظیمات</div>
<div class="nav-it" data-pg="support"><i class="ti ti-headset"></i> پشتیبانی</div>
</div>
<div class="sb-foot">
<button class="theme-btn" onclick="toggleTheme()"><i class="ti ti-moon"></i> <span id="theme-label">تم روشن</span></button>
<button class="logout-btn" onclick="logout()"><i class="ti ti-logout"></i> خروج</button>
</div>
</aside>
<main class="main">
<section class="pg on" id="pg-overview">
<div class="topbar"><div><div class="tb-title"><i class="ti ti-dashboard"></i> داشبورد</div><div class="tb-sub" id="last-upd">در حال بارگذاری...</div></div><div class="tb-right"><span class="badge bg-green"><span class="dot dg pulse"></span> فعال</span><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> رفرش</button></div></div>
<div class="metrics">
<div class="metric"><div class="m-icon"><i class="ti ti-plug-connected"></i></div><div class="m-label">اتصالات فعال</div><div class="m-val" id="m-conns">—</div></div>
<div class="metric"><div class="m-icon"><i class="ti ti-transfer"></i></div><div class="m-label">کل ترافیک</div><div class="m-val" id="m-traffic">—<span class="m-unit">MB</span></div></div>
<div class="metric"><div class="m-icon green"><i class="ti ti-link"></i></div><div class="m-label">کانفیگ فعال</div><div class="m-val" id="m-alinks">—</div></div>
<div class="metric"><div class="m-icon amber"><i class="ti ti-folders"></i></div><div class="m-label">گروه‌ها</div><div class="m-val" id="m-subs">—</div></div>
</div>
<div class="vless-box"><div class="vl-header"><div class="vl-title"><i class="ti ti-link"></i> لینک پیش‌فرض</div><span class="badge bg-blue">TLS 443 · WS</span></div><div class="vl-code" id="vless-main">در حال دریافت...</div><div class="vl-actions"><button class="btn btn-p" onclick="copyText('vless-main')"><i class="ti ti-copy"></i> کپی</button><button class="btn btn-g" onclick="qrFor('vless-main')"><i class="ti ti-qrcode"></i> QR</button></div></div>
<div class="g3"><div class="card"><div class="card-title"><i class="ti ti-chart-area"></i> ترافیک ساعتی (MB)</div><div class="ch"><canvas id="ch1"></canvas></div></div><div class="card"><div class="card-title"><i class="ti ti-chart-donut"></i> توزیع</div><div class="ch-sm"><canvas id="ch2"></canvas></div></div></div>
<div class="g2"><div class="card"><div class="card-title"><i class="ti ti-activity"></i> وضعیت سرویس</div><div class="sr"><span class="sr-k"><i class="ti ti-shield-check"></i> UUID Auth</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div><div class="sr"><span class="sr-k"><i class="ti ti-circle-check"></i> VLESS/WS</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div><div class="sr"><span class="sr-k"><i class="ti ti-bolt"></i> XHTTP Ultra</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div><div class="sr"><span class="sr-k"><i class="ti ti-server"></i> Node Support</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div><div class="sr"><span class="sr-k"><i class="ti ti-clock"></i> آپتایم</span><span class="sr-v" id="uptime-inline">—</span></div></div><div class="card"><div class="card-title"><i class="ti ti-list"></i> خلاصه کانفیگ‌ها <span class="badge bg-blue" id="lsummary-badge">0</span></div><div id="lsummary">—</div></div></div>
</section>
<section class="pg" id="pg-links"><div class="topbar"><div><div class="tb-title"><i class="ti ti-link"></i> کانفیگ‌ها</div></div></div><div id="links-grid"><div class="empty"><i class="ti ti-link-off"></i><p>کانفیگی وجود ندارد</p></div></div></section>
<section class="pg" id="pg-subgroups"><div class="topbar"><div><div class="tb-title"><i class="ti ti-folders"></i> گروه‌ها</div></div></div><div id="subs-grid"><div class="empty"><i class="ti ti-folder-off"></i><p>گروهی وجود ندارد</p></div></div></section>
<section class="pg" id="pg-nodes"><div class="topbar"><div><div class="tb-title"><i class="ti ti-server"></i> Node‌ها</div></div></div><div id="nodes-grid"><div class="empty"><i class="ti ti-server-off"></i><p>هیچ Node ای ثبت نشده</p></div></div></section>
<section class="pg" id="pg-traffic"><div class="topbar"><div><div class="tb-title"><i class="ti ti-chart-area"></i> ترافیک</div></div></div><div class="card"><div class="ch-lg"><canvas id="ch3"></canvas></div></div></section>
<section class="pg" id="pg-connections"><div class="topbar"><div><div class="tb-title"><i class="ti ti-plug-connected"></i> اتصالات</div></div></div><div id="conns-grid"><div class="empty"><i class="ti ti-plug-off"></i><p>هیچ اتصالی وجود ندارد</p></div></div></section>
<section class="pg" id="pg-bot"><div class="topbar"><div><div class="tb-title"><i class="ti ti-robot"></i> ربات تلگرام</div></div></div><div class="card"><p style="color:var(--t2)">مدیریت ربات از طریق پنل ادمین تلگرام انجام می‌شود.</p></div></section>
<section class="pg" id="pg-security"><div class="topbar"><div><div class="tb-title"><i class="ti ti-shield-lock"></i> امنیت</div></div></div><div class="card"><div class="sr"><span class="sr-k"><i class="ti ti-lock"></i> رمزنگاری</span><span class="sr-v" style="color:var(--green-t)">● TLS 443</span></div><div class="sr"><span class="sr-k"><i class="ti ti-key"></i> هش رمز</span><span class="sr-v">SHA-256+Salt</span></div></div></section>
<section class="pg" id="pg-logs"><div class="topbar"><div><div class="tb-title"><i class="ti ti-history"></i> لاگ‌ها</div></div></div><div id="logs-list"><div class="empty"><i class="ti ti-history-toggle"></i><p>لاگی ثبت نشده</p></div></div></section>
<section class="pg" id="pg-errors"><div class="topbar"><div><div class="tb-title"><i class="ti ti-alert-triangle"></i> خطاها</div></div></div><div id="errs-list"><div class="empty"><i class="ti ti-check-circle"></i><p>هیچ خطایی نیست</p></div></div></section>
<section class="pg" id="pg-settings"><div class="topbar"><div><div class="tb-title"><i class="ti ti-settings"></i> تنظیمات</div></div></div><div class="g2"><div class="card"><div class="card-title"><i class="ti ti-key"></i> تغییر رمز</div><input type="password" id="cp-cur" placeholder="رمز فعلی" style="width:100%;padding:10px;border-radius:8px;border:1px solid var(--card-b);background:var(--bg2);color:var(--t1);margin-bottom:10px"><input type="password" id="cp-new" placeholder="رمز جدید" style="width:100%;padding:10px;border-radius:8px;border:1px solid var(--card-b);background:var(--bg2);color:var(--t1);margin-bottom:10px"><input type="password" id="cp-cf" placeholder="تکرار رمز جدید" style="width:100%;padding:10px;border-radius:8px;border:1px solid var(--card-b);background:var(--bg2);color:var(--t1);margin-bottom:10px"><button class="btn btn-p" onclick="changePw()"><i class="ti ti-check"></i> تغییر رمز</button></div><div class="card"><div class="card-title"><i class="ti ti-server"></i> اطلاعات سرور</div><div class="sr"><span class="sr-k">نسخه</span><span class="sr-v">v10</span></div><div class="sr"><span class="sr-k">هاست</span><span class="sr-v" id="set-host">—</span></div></div></div></section>
<section class="pg" id="pg-support"><div class="topbar"><div><div class="tb-title"><i class="ti ti-headset"></i> پشتیبانی</div></div></div><div class="card"><p style="color:var(--t2)">ارتباط از طریق:<br><a href="https://t.me/ItzJustEren" style="color:var(--accent2)">@ItzJustEren</a><br><a href="https://t.me/TaaKaaOrg" style="color:var(--accent2)">@TaaKaaOrg</a></p></div></section>
</main>
<script>
let isDark=localStorage.getItem('tk-theme')!=='light';
function applyTheme(d){document.documentElement.setAttribute('data-theme',d?'dark':'light')}
function toggleTheme(){isDark=!isDark;localStorage.setItem('tk-theme',isDark?'dark':'light');applyTheme(isDark)}
applyTheme(isDark);
function toast(msg,t){const el=document.getElementById('toast')||document.createElement('div');el.id='toast';el.style.position='fixed';el.style.bottom='20px';el.style.left='50%';el.style.transform='translateX(-50%)';el.style.background='var(--card)';el.style.padding='10px 20px';el.style.borderRadius='10px';el.style.border='1px solid var(--card-b)';el.style.zIndex='999';el.style.color='var(--t1)';el.textContent=msg;document.body.appendChild(el);setTimeout(()=>el.remove(),2500)}
function copyText(id){navigator.clipboard.writeText(document.getElementById(id).textContent).then(()=>toast('کپی شد ✓'))}
function qrFor(id){window.open('https://api.qrserver.com/v1/create-qr-code/?size=300x300&data='+encodeURIComponent(document.getElementById(id).textContent),'_blank')}
async function logout(){await fetch('/api/logout',{method:'POST'});location.href='/login'}
function navTo(name){document.querySelectorAll('.nav-it').forEach(n=>n.classList.toggle('on',n.dataset.pg===name));document.querySelectorAll('.pg').forEach(p=>p.classList.toggle('on',p.id==='pg-'+name));document.getElementById('sb').classList.remove('open');document.getElementById('overlay').classList.remove('show')}
document.querySelectorAll('.nav-it').forEach(el=>el.addEventListener('click',()=>navTo(el.dataset.pg)));
let ch1,ch2,ch3;
async function fetchStats(){
 try{
  const r=await fetch('/stats');if(!r.ok)throw new Error();const d=await r.json();
  document.getElementById('m-conns').textContent=d.active_connections;document.getElementById('conns-nb').textContent=d.active_connections;
  document.getElementById('m-traffic').innerHTML=d.total_traffic_mb.toFixed(1)+'<span class="m-unit">MB</span>';
  document.getElementById('m-alinks').textContent=d.active_links||0;document.getElementById('m-subs').textContent=d.subs_count||0;
  document.getElementById('uptime-inline').textContent=d.uptime;document.getElementById('last-upd').textContent='آخرین بروزرسانی: '+new Date().toLocaleTimeString('fa-IR');
  if(d.hourly){const labels=Object.keys(d.hourly).sort(),vals=labels.map(k=>+(d.hourly[k]/1024/1024).toFixed(2));
   if(ch1){ch1.data.labels=labels;ch1.data.datasets[0].data=vals;ch1.update()}
   if(ch3){ch3.data.labels=labels;ch3.data.datasets[0].data=vals;ch3.update()}
  }
 }catch(e){console.error(e)}
}
async function loadLinks(){
 try{
  const r=await fetch('/api/links');if(!r.ok)throw new Error();const d=await r.json();const links=d.links||[];
  document.getElementById('links-nb').textContent=links.length;const grid=document.getElementById('links-grid');
  if(!links.length){grid.innerHTML='<div class="empty"><i class="ti ti-link-off"></i><p>کانفیگی وجود ندارد</p></div>';return}
  grid.innerHTML=links.map(l=>`<div class="cfg-card ${!l.active?'inactive':(l.expired?'expired':'')}"><div class="cfg-row"><span class="cfg-status-dot ${l.active&&!l.expired?'pulse':''}"></span><div class="cfg-identity"><div class="cfg-label">${l.label}</div><div class="cfg-sub-meta">${l.uuid.slice(0,12)}…</div></div><div class="cfg-usage-col"><div class="ubar"><div class="ubar-f" style="width:${l.limit_bytes?Math.min(100,l.used_bytes/l.limit_bytes*100):0}%;background:${l.limit_bytes&&l.used_bytes/l.limit_bytes>0.9?'var(--red)':l.limit_bytes&&l.used_bytes/l.limit_bytes>0.7?'var(--amber)':'var(--accent)'}"></div></div><div class="utxt"><span>${l.used_bytes?Math.round(l.used_bytes/1024/1024)+'MB':'0'}</span><span>${l.limit_bytes?Math.round(l.limit_bytes/1024/1024)+'MB':'∞'}</span></div></div><div class="cfg-exp-col">${l.expires_at?new Date(l.expires_at).toLocaleDateString('fa-IR'):'∞'}</div><div class="cfg-actions"><button class="btn btn-sm btn-g" onclick="copyText('vless-main')"><i class="ti ti-copy"></i></button></div></div></div>`).join('');
 }catch(e){console.error(e)}
}
async function loadSubs(){
 try{const r=await fetch('/api/subs');if(!r.ok)throw new Error();const d=await r.json();const subs=d.subs||[];document.getElementById('subs-nb').textContent=subs.length;const grid=document.getElementById('subs-grid');if(!subs.length){grid.innerHTML='<div class="empty"><i class="ti ti-folder-off"></i><p>گروهی وجود ندارد</p></div>';return}grid.innerHTML=subs.map(s=>`<div class="card" style="margin-bottom:8px"><div class="sr"><span class="sr-k"><i class="ti ti-folder"></i> ${s.name}</span><span class="sr-v">${s.links_count||0} کانفیگ</span></div></div>`).join('')}catch(e){console.error(e)}}
async function loadNodes(){
 try{const r=await fetch('/api/nodes');if(!r.ok)throw new Error();const d=await r.json();const nodes=d.nodes||[];document.getElementById('nodes-nb').textContent=nodes.length;const grid=document.getElementById('nodes-grid');if(!nodes.length){grid.innerHTML='<div class="empty"><i class="ti ti-server-off"></i><p>هیچ Node ای ثبت نشده</p></div>';return}grid.innerHTML=nodes.map(n=>`<div class="card" style="margin-bottom:8px"><div class="sr"><span class="sr-k"><i class="ti ti-server"></i> ${n.name}</span><span class="sr-v">${n.address}:${n.port}</span></div></div>`).join('')}catch(e){console.error(e)}}
async function loadConns(){
 try{const r=await fetch('/api/connections');if(!r.ok)throw new Error();const d=await r.json();const conns=d.connections||[];document.getElementById('conns-nb').textContent=conns.length;const grid=document.getElementById('conns-grid');if(!conns.length){grid.innerHTML='<div class="empty"><i class="ti ti-plug-off"></i><p>هیچ اتصالی وجود ندارد</p></div>';return}grid.innerHTML=conns.map(c=>`<div class="card" style="margin-bottom:6px"><div class="sr"><span class="sr-k"><i class="ti ti-user"></i> ${c.ip}</span><span class="sr-v">${c.bytes_fmt||'0 B'}</span></div></div>`).join('')}catch(e){console.error(e)}}
async function changePw(){
 const cur=document.getElementById('cp-cur').value,nw=document.getElementById('cp-new').value,cf=document.getElementById('cp-cf').value;
 if(!cur||!nw||!cf){toast('همه فیلدها را پر کنید');return}
 if(nw!==cf){toast('تکرار رمز اشتباه');return}
 try{const r=await fetch('/api/change-password',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({current_password:cur,new_password:nw})});if(!r.ok)throw new Error();toast('رمز تغییر کرد ✓');document.getElementById('cp-cur').value='';document.getElementById('cp-new').value='';document.getElementById('cp-cf').value=''}catch(e){toast('خطا در تغییر رمز')}
}
function refreshAll(){fetchStats();loadLinks();loadSubs();loadNodes();loadConns();toast('رفرش شد ✓')}
document.addEventListener('DOMContentLoaded',()=>{
 document.getElementById('set-host').textContent=location.host;
 const ctx1=document.getElementById('ch1')?.getContext('2d');if(ctx1){ch1=new Chart(ctx1,{type:'line',data:{labels:[],datasets:[{label:'MB',data:[],borderColor:'#F97316',backgroundColor:'rgba(249,115,22,0.1)',fill:true,tension:.4,pointRadius:0}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{grid:{color:'rgba(249,115,22,0.05)'}}}}})}
 const ctx3=document.getElementById('ch3')?.getContext('2d');if(ctx3){ch3=new Chart(ctx3,{type:'line',data:{labels:[],datasets:[{label:'MB',data:[],borderColor:'#F97316',backgroundColor:'rgba(249,115,22,0.05)',fill:true,tension:.4,pointRadius:0}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{grid:{color:'rgba(249,115,22,0.05)'}}}}})}
 const ctx2=document.getElementById('ch2')?.getContext('2d');if(ctx2){ch2=new Chart(ctx2,{type:'doughnut',data:{labels:['VLESS/WS','XHTTP','Node'],datasets:[{data:[50,30,20],backgroundColor:['#F97316','#FB923C','#A78BFA']}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom',labels:{color:'var(--t2)',font:{size:10}}}}})}
 fetchStats();loadLinks();loadSubs();loadNodes();loadConns();setInterval(fetchStats,5000)
})
</script>
</body></html>"""

def get_public_page_html(uuid_key: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Tk-Ui Sub</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#0a0a0a;--card:#1a1a1a;--card-b:rgba(249,115,22,0.15);--accent:#F97316;--accent2:#FB923C;--t1:#F5F5F5;--t2:#B0B0B0;--t3:#6B6B6B;--shadow:0 12px 40px rgba(0,0,0,0.5)}}
[data-theme="light"]{{--bg:#f5f5f5;--card:#ffffff;--card-b:rgba(249,115,22,0.2);--accent:#EA580C;--accent2:#F97316;--t1:#1a1a1a;--t2:#444;--t3:#777;--shadow:0 12px 36px rgba(0,0,0,0.08)}}
html,body{{min-height:100%;background:var(--bg);font-family:'Vazirmatn',sans-serif;color:var(--t1);font-size:14px;transition:background .3s,color .3s}}
.bg-fx{{position:fixed;inset:0;background:radial-gradient(ellipse 70% 45% at 50% -8%,rgba(249,115,22,0.13),transparent 62%),var(--bg);z-index:0;pointer-events:none}}
.wrap{{position:relative;z-index:10;max-width:800px;margin:0 auto;padding:24px 16px 64px}}
.top{{display:flex;align-items:center;justify-content:space-between;margin-bottom:26px}}
.brand{{display:flex;align-items:center;gap:11px}}
.brand-img{{width:40px;height:40px;border-radius:50%;border:1px solid var(--card-b);box-shadow:0 0 14px rgba(249,115,22,.3);display:flex;align-items:center;justify-content:center;background:var(--bg);color:var(--accent);font-weight:900;font-size:18px}}
.brand-name{{font-size:14.5px;font-weight:800;color:var(--t1)}}
.sub-info{{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:24px;margin-bottom:16px;box-shadow:var(--shadow)}}
.sub-name{{font-size:23px;font-weight:800;color:var(--t1);margin-bottom:6px}}
.sub-sub-box{{background:rgba(249,115,22,0.08);border:1px solid var(--card-b);border-radius:13px;padding:12px 14px;display:flex;align-items:center;gap:9px;flex-wrap:wrap}}
.sub-sub-url{{font-family:ui-monospace,monospace;font-size:10px;color:var(--accent2);word-break:break-all;flex:1;min-width:140px}}
.stats-bar{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:18px}}
.stat-card{{background:var(--card);border:1px solid var(--card-b);border-radius:16px;padding:16px}}
.stat-label{{font-size:9px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.07em;margin-bottom:7px}}
.stat-val{{font-size:22px;font-weight:800;color:var(--t1);line-height:1}}
.cfg-grid{{display:grid;gap:13px}}
.cfg-card{{background:var(--card);border:1px solid var(--card-b);border-radius:18px;padding:18px;transition:.2s}}
.cfg-card:hover{{border-color:rgba(249,115,22,0.4);box-shadow:var(--shadow)}}
.cfg-head{{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:12px;flex-wrap:wrap}}
.cfg-label{{font-size:14.5px;font-weight:700;color:var(--t1)}}
.cfg-status{{font-size:10px;font-weight:700;padding:4px 10px;border-radius:20px}}
.cfg-status.ok{{background:rgba(16,185,129,0.1);color:#34D399}}
.cfg-status.no{{background:rgba(239,68,68,0.1);color:#F87171}}
.ubar{{height:6px;border-radius:4px;background:rgba(249,115,22,0.1);overflow:hidden;margin-bottom:5px}}
.ubar-f{{height:100%;border-radius:4px;background:linear-gradient(90deg,var(--accent),var(--accent2));transition:width .5s ease}}
.utxt{{font-size:10px;color:var(--t3);display:flex;justify-content:space-between}}
.cfg-actions{{display:flex;gap:7px;flex-wrap:wrap;margin-top:11px}}
.btn{{font-family:inherit;font-size:11.5px;font-weight:700;border-radius:10px;padding:8px 15px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;border:none;transition:all .15s;white-space:nowrap}}
.btn-p{{background:linear-gradient(135deg,#F97316,#EA580C);color:#fff;box-shadow:0 3px 14px rgba(249,115,22,.35)}}
.btn-p:hover{{transform:translateY(-2px);box-shadow:0 6px 20px rgba(249,115,22,.45)}}
.btn-g{{background:rgba(249,115,22,0.1);color:var(--accent2);border:1px solid rgba(249,115,22,0.15)}}
.dot{{width:6px;height:6px;border-radius:50%;background:#34D399;display:inline-block;animation:pulse 2s infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
.toast{{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(40px);background:var(--card);border:1px solid var(--card-b);color:var(--t1);border-radius:12px;padding:10px 20px;font-size:12.5px;font-weight:600;opacity:0;transition:all .25s;z-index:999;pointer-events:none;display:flex;align-items:center;gap:7px;box-shadow:var(--shadow)}}
.toast.show{{opacity:1;transform:translateX(-50%) translateY(0)}}.toast.ok{{border-color:rgba(16,185,129,.35);background:rgba(16,185,129,.1);color:#34D399}}
.empty{{text-align:center;padding:60px 20px;color:var(--t3)}}.empty i{{font-size:40px;opacity:.3;display:block;margin-bottom:12px}}
.lock-stage{{display:flex;align-items:center;justify-content:center;min-height:70vh}}
.lock-card{{background:var(--card);border:1px solid var(--card-b);border-radius:26px;padding:0;max-width:380px;width:100%;text-align:center;box-shadow:var(--shadow)}}
.lock-banner{{padding:38px 30px 26px}}.lock-shield{{width:64px;height:64px;border-radius:18px;background:rgba(249,115,22,0.1);border:1px solid var(--card-b);display:flex;align-items:center;justify-content:center;margin:0 auto 18px}}.lock-shield i{{font-size:28px;color:var(--accent2)}}
.lock-title{{font-size:18px;font-weight:800;color:var(--t1)}}.lock-form{{padding:24px 30px 30px}}
.lock-inp{{width:100%;padding:13px 44px;border-radius:13px;border:1px solid var(--card-b);background:rgba(0,0,0,.2);color:var(--t1);font-family:inherit;font-size:14px;outline:none;text-align:center;letter-spacing:.14em}}
.lock-inp:focus{{border-color:var(--accent);box-shadow:0 0 0 3px rgba(249,115,22,.15)}}
.lock-btn{{width:100%;justify-content:center;padding:13px;font-size:13px;border-radius:13px}}
.footer{{text-align:center;padding-top:28px;font-size:10.5px;color:var(--t3)}}.footer a{{color:var(--accent2);font-weight:700}}
@media(max-width:520px){{.stats-bar{{grid-template-columns:1fr 1fr}}}}
</style>
</head>
<body>
<div class="bg-fx"></div><div class="toast" id="toast"></div>
<div class="wrap"><div class="top"><div class="brand"><div class="brand-img">Tk</div><div><div class="brand-name">Tk-Ui</div></div></div><button style="background:none;border:none;color:var(--t2);font-size:20px;cursor:pointer" onclick="toggleTheme()"><i class="ti ti-sun" id="themeIcon"></i></button></div>
<div id="root"><div class="empty"><i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i>در حال بارگذاری...</div></div>
<div class="footer">پشتیبانی: <a href="https://t.me/ItzJustEren" target="_blank">@ItzJustEren</a> · کانال: <a href="https://t.me/TaaKaaOrg" target="_blank">@TaaKaaOrg</a></div></div>
<script>
const UUID_KEY='{uuid_key}';let isDark=localStorage.getItem('tk-pub-theme')!=='light',savedPw='';
function applyTheme(d){{document.documentElement.setAttribute('data-theme',d?'dark':'light');document.getElementById('themeIcon').className='ti '+(d?'ti-moon':'ti-sun')}}
function toggleTheme(){{isDark=!isDark;localStorage.setItem('tk-pub-theme',isDark?'dark':'light');applyTheme(isDark)}}applyTheme(isDark);
function toast(m,t=''){{const el=document.getElementById('toast');el.textContent=m;el.className='toast show'+(t?' '+t:'');setTimeout(()=>el.classList.remove('show'),2400)}}
function esc(s){{return String(s||'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]))}}
function fmtB(b){{if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB'}}
async function loadData(pw=''){{const r=await fetch('/api/public/sub/'+UUID_KEY+(pw?'?pw='+encodeURIComponent(pw):''));return r.json()}}
function renderLock(name){{document.getElementById('root').innerHTML='<div class="lock-stage"><div class="lock-card"><div class="lock-banner"><div class="lock-shield"><i class="ti ti-shield-lock"></i></div><div class="lock-title">'+esc(name)+'</div></div><div class="lock-form"><div style="color:var(--red);font-size:12px;margin-bottom:10px" id="lockErr"></div><input class="lock-inp" type="password" id="lockPw" placeholder="••••••••" autofocus><button class="btn btn-p lock-btn" style="margin-top:13px" onclick="submitLock()"><i class="ti ti-lock-open"></i> ورود</button></div></div></div>';document.getElementById('lockPw').addEventListener('keydown',e=>{{if(e.key==='Enter')submitLock()}})}}
async function submitLock(){{const pw=document.getElementById('lockPw').value;const data=await loadData(pw);if(data.locked){{document.getElementById('lockErr').textContent='رمز اشتباه است';return}}savedPw=pw;renderContent(data)}}
function renderContent(d){{const activeCount=d.links.filter(l=>l.active).length;document.getElementById('root').innerHTML='<div class="sub-info"><div class="sub-name">'+esc(d.name)+'</div><div class="sub-sub-box"><span class="sub-sub-url">'+esc(d.sub_url+(savedPw?'?pw='+encodeURIComponent(savedPw):''))+'</span><button class="btn btn-g" onclick="navigator.clipboard.writeText(window._subUrl).then(()=>toast(\'کپی شد ✓\',\'ok\'))"><i class="ti ti-copy"></i></button></div></div><div class="stats-bar"><div class="stat-card"><div class="stat-label">فعال</div><div class="stat-val">'+activeCount+'</div></div><div class="stat-card"><div class="stat-label">اتصالات</div><div class="stat-val">'+(d.active_connections||0)+'</div></div><div class="stat-card"><div class="stat-label">مصرف</div><div class="stat-val">'+esc(d.total_used_fmt||'0')+'</div></div></div><div class="cfg-grid">'+d.links.map((l,i)=>'<div class="cfg-card"><div class="cfg-head"><div class="cfg-label">'+esc(l.label)+'</div><span class="cfg-status '+(l.active?'ok':'no')+'">'+(l.active?'فعال':'غیرفعال')+'</span></div><div class="ubar"><div class="ubar-f" style="width:'+(l.limit_bytes?Math.min(100,l.used_bytes/l.limit_bytes*100):0)+'%"></div></div><div class="utxt"><span>'+fmtB(l.used_bytes)+'</span><span>'+(l.limit_bytes?'از '+fmtB(l.limit_bytes):'∞')+'</span></div><div class="cfg-actions"><button class="btn btn-p" onclick="navigator.clipboard.writeText(\''+esc(l.vless_link)+'\').then(()=>toast(\'کپی شد ✓\',\'ok\'))"><i class="ti ti-copy"></i> کپی</button></div></div>').join('')+'</div>';window._subUrl=d.sub_url+(savedPw?'?pw='+encodeURIComponent(savedPw):'')}}
async function init(){{const data=await loadData();if(data.locked){{renderLock(data.name);return}}renderContent(data)}}init();
</script>
</body></html>"""
