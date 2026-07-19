import asyncio
import json
import os
import hashlib
import secrets
import time
import aiofiles
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import quote
from collections import deque, defaultdict
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import Response, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import httpx
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Tk-Ui")

IRAN_TZ = ZoneInfo("Asia/Tehran")

app = FastAPI(title="Tk-Ui", docs_url=None, redoc_url=None)

# ── Persistence ───────────────────────────────────────────────────────────────
DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
DATA_FILE = DATA_DIR / "tkui_state.json"
SECRET_FILE = DATA_DIR / "tkui_secret.key"
SAVE_LOCK = asyncio.Lock()

def _load_or_create_secret() -> str:
    env_secret = os.environ.get("SECRET_KEY")
    if env_secret:
        return env_secret
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if SECRET_FILE.exists():
            existing = SECRET_FILE.read_text(encoding="utf-8").strip()
            if existing:
                return existing
        new_secret = secrets.token_urlsafe(32)
        SECRET_FILE.write_text(new_secret, encoding="utf-8")
        return new_secret
    except Exception as e:
        logger.warning(f"Could not persist SECRET_KEY: {e}")
        return secrets.token_urlsafe(32)

CONFIG = {
    "port": int(os.environ.get("PORT", 8000)),
    "secret": _load_or_create_secret(),
    "host": os.environ.get("RAILWAY_PUBLIC_DOMAIN", "localhost"),
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── State ────────────────────────────────────────────────────────────────────
LINKS: dict = {}
LINKS_LOCK = asyncio.Lock()
SUBS: dict = {}
SUBS_LOCK = asyncio.Lock()
NODES: dict = {}
NODES_LOCK = asyncio.Lock()
PRODUCTS: dict = {}
PRODUCTS_LOCK = asyncio.Lock()
ORDERS: dict = {}
ORDERS_LOCK = asyncio.Lock()
TEST_USERS: dict = {}
USER_CODES: dict = {}
FEEDBACKS: list = []
REYMIT_LINKS: list = ["https://reymit.ir/itzjusteren"]
TUTORIAL_CHANNEL: str = "@TaaKaaOrg"
ADMIN_GROUP_ID = int(os.environ.get("ADMIN_GROUP_ID", 0)) or None

CARD_NUMBER = os.environ.get("CARD_NUMBER", "6037-9910-1234-5678")
CARD_OWNER_NAME = os.environ.get("CARD_OWNER_NAME", "نام صاحب کارت")
PRICE_PER_GB = float(os.environ.get("PRICE_PER_GB", "6"))
ADMIN_IDS = set()
OWNER_ID = None

# ── Auth ──────────────────────────────────────────────────────────────────────
SESSION_COOKIE = "tkui_session"
SESSION_TTL = 60 * 60 * 24 * 365
AUTH = {"password_hash": hashlib.sha256(f"taakaa{CONFIG['secret']}".encode()).hexdigest()}
SESSIONS: dict = {}
SESSIONS_LOCK = asyncio.Lock()

def hash_password(pw: str) -> str:
    return hashlib.sha256(f"{pw}{CONFIG['secret']}".encode()).hexdigest()

async def create_session() -> str:
    token = secrets.token_urlsafe(32)
    async with SESSIONS_LOCK:
        SESSIONS[token] = time.time() + SESSION_TTL
    return token

async def is_valid_session(token: str | None) -> bool:
    if not token:
        return False
    async with SESSIONS_LOCK:
        exp = SESSIONS.get(token)
        if exp is None:
            return False
        if exp < time.time():
            SESSIONS.pop(token, None)
            return False
        return True

async def destroy_session(token: str | None):
    if not token:
        return
    async with SESSIONS_LOCK:
        SESSIONS.pop(token, None)

async def require_auth(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    if not await is_valid_session(token):
        raise HTTPException(status_code=401, detail="unauthorized")
    return token

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_host(request: Request | None = None) -> str:
    if request is not None:
        h = request.headers.get("x-forwarded-host") or request.headers.get("host")
        if h:
            h = h.split(":")[0]
            CONFIG["host"] = h
            return h
    return os.environ.get("RAILWAY_PUBLIC_DOMAIN", CONFIG["host"])

def generate_uuid() -> str:
    h = secrets.token_hex(16)
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"

def now_ir() -> datetime:
    return datetime.now(IRAN_TZ)

def fmt_bytes(b: int) -> str:
    if b < 1024: return f"{b} B"
    if b < 1024**2: return f"{b/1024:.1f} KB"
    if b < 1024**3: return f"{b/1024**2:.2f} MB"
    return f"{b/1024**3:.2f} GB"

def uptime() -> str:
    secs = int(time.time() - stats["start_time"])
    h, m, s = secs // 3600, (secs % 3600) // 60, secs % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def generate_random_password(length: int = 8) -> str:
    import string
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def generate_user_code() -> str:
    import string
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def parse_size_to_bytes(value: float, unit: str) -> int:
    unit = unit.upper()
    if unit == "GB": return int(value * 1024 ** 3)
    if unit == "MB": return int(value * 1024 ** 2)
    if unit == "KB": return int(value * 1024)
    return int(value)

def parse_speed_to_bytes(value: float, unit: str) -> int:
    if value <= 0:
        return 0
    unit = (unit or "MBIT").upper()
    if unit == "MBIT":
        return int(value * 1024 * 1024 / 8)
    if unit == "KB":
        return int(value * 1024)
    if unit == "MB":
        return int(value * 1024 * 1024)
    return int(value)

def is_link_expired(link: dict) -> bool:
    exp = link.get("expires_at")
    if not exp:
        return False
    try:
        return datetime.now() > datetime.fromisoformat(exp)
    except Exception:
        return False

def is_link_allowed(link: dict | None) -> bool:
    if link is None:
        return False
    if not link.get("active", True):
        return False
    if is_link_expired(link):
        return False
    lb = link.get("limit_bytes", 0)
    if lb > 0 and link.get("used_bytes", 0) >= lb:
        return False
    return True

def unique_ips_for_uuid(uuid: str) -> set:
    return {c.get("ip") for c in connections.values() if c.get("uuid") == uuid and c.get("ip")}

def is_ip_allowed(link: dict | None, uuid: str, ip: str) -> bool:
    if link is None:
        return False
    limit = int(link.get("ip_limit", 0) or 0)
    if limit <= 0:
        return True
    ips = unique_ips_for_uuid(uuid)
    if ip in ips:
        return True
    return len(ips) < limit

def client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return request.client.host if request.client else "نامشخص"

def log_activity(kind: str, message: str, level: str = "info"):
    activity_logs.append({
        "kind": kind,
        "level": level,
        "message": message,
        "time": datetime.now().isoformat(),
    })

def generate_vless_link(uuid: str, host: str, remark: str = "Tk-Ui", protocol: str = "vless-ws", fingerprint: str | None = None, alpn: str | None = None, port: int | None = None) -> str:
    fp = (fingerprint or "chrome").strip() or "chrome"
    alpn_val = (alpn or "").strip() or "http/1.1"
    port_val = port or 443
    if protocol == "vless-ws":
        path = f"/ws/{uuid}"
        params = {"encryption": "none", "security": "tls", "type": "ws", "host": host, "path": path, "sni": host, "fp": fp, "alpn": alpn_val}
    else:
        mode = protocol.replace("xhttp-", "")
        path = f"/xhttp-siz10/{mode}/{uuid}"
        params = {"encryption": "none", "security": "tls", "type": "xhttp", "mode": mode, "host": host, "path": path, "sni": host, "fp": fp, "alpn": alpn_val}
    query = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
    return f"vless://{uuid}@{host}:{port_val}?{query}#{quote(remark)}"

def vless_link_for_link(link: dict, uid: str, host: str) -> str:
    return generate_vless_link(uid, host, remark=f"Tk-Ui-{link.get('label','')}", protocol=link.get("protocol", "vless-ws"), fingerprint=link.get("fingerprint"), alpn=link.get("alpn"), port=link.get("port"))

# ── Node helper ──────────────────────────────────────────────────────────────
async def send_config_to_node(node_id: str, uuid: str, link: dict) -> bool:
    node = NODES.get(node_id)
    if not node:
        return False
    url = f"http://{node['address']}:{node['port']}/api/config"
    payload = {
        "uuid": uuid,
        "label": link.get("label"),
        "limit_bytes": link.get("limit_bytes"),
        "used_bytes": link.get("used_bytes", 0),
        "expires_at": link.get("expires_at"),
        "protocol": link.get("protocol"),
        "fingerprint": link.get("fingerprint"),
        "alpn": link.get("alpn"),
        "port": link.get("port"),
        "ip_limit": link.get("ip_limit"),
        "speed_limit_bytes": link.get("speed_limit_bytes"),
        "active": link.get("active", True),
    }
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(url, json=payload)
        return resp.status_code == 200
    except Exception as e:
        logger.warning(f"send_config_to_node error: {e}")
        return False

# ── In-memory state ───────────────────────────────────────────────────────────
connections: dict = {}
stats = {"total_bytes": 0, "total_requests": 0, "total_errors": 0, "start_time": time.time()}
error_logs: deque = deque(maxlen=50)
activity_logs: deque = deque(maxlen=200)
hourly_traffic: dict = defaultdict(int)
http_client: httpx.AsyncClient | None = None

PROTOCOLS = ("vless-ws", "xhttp-packet-up", "xhttp-stream-up")
DEFAULT_PROTOCOL = "vless-ws"
FINGERPRINTS = ("chrome", "firefox", "safari", "ios", "android", "edge", "360", "qq", "random", "randomized")
DEFAULT_FINGERPRINT = "chrome"
DEFAULT_ALPN_BY_PROTOCOL = {"vless-ws": "http/1.1", "xhttp-packet-up": "h2,http/1.1", "xhttp-stream-up": "h2,http/1.1"}
DEFAULT_PORT = 443

# ── load/save state ──────────────────────────────────────────────────────────
async def load_state():
    global LINKS, SUBS, NODES, PRODUCTS, ORDERS, CARD_NUMBER, CARD_OWNER_NAME, PRICE_PER_GB, ADMIN_IDS, OWNER_ID, TEST_USERS, USER_CODES, REYMIT_LINKS, FEEDBACKS, TUTORIAL_CHANNEL
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if DATA_FILE.exists():
            async with aiofiles.open(DATA_FILE, "r", encoding="utf-8") as f:
                raw = await f.read()
            data = json.loads(raw)
            LINKS.update(data.get("links", {}))
            SUBS.update(data.get("subs", {}))
            NODES.update(data.get("nodes", {}))
            PRODUCTS.update(data.get("products", {}))
            ORDERS.update(data.get("orders", {}))
            TEST_USERS.update(data.get("test_users", {}))
            USER_CODES.update(data.get("user_codes", {}))
            REYMIT_LINKS = data.get("reymit_links", ["https://reymit.ir/itzjusteren"])
            FEEDBACKS = data.get("feedbacks", [])
            TUTORIAL_CHANNEL = data.get("tutorial_channel", "@TaaKaaOrg")
            if "password_hash" in data:
                AUTH["password_hash"] = data["password_hash"]
            if "card_number" in data:
                CARD_NUMBER = data["card_number"]
            if "card_owner_name" in data:
                CARD_OWNER_NAME = data["card_owner_name"]
            if "price_per_gb" in data:
                PRICE_PER_GB = data["price_per_gb"]
            if "admin_ids" in data:
                ADMIN_IDS = set(data["admin_ids"])
            if "owner_id" in data:
                OWNER_ID = data["owner_id"]
            logger.info(f"State loaded: {len(LINKS)} links, {len(SUBS)} subs, {len(NODES)} nodes, {len(PRODUCTS)} products")
    except Exception as e:
        logger.warning(f"Could not load state: {e}")

async def save_state():
    async with SAVE_LOCK:
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            data = {
                "links": dict(LINKS),
                "subs": dict(SUBS),
                "nodes": dict(NODES),
                "products": dict(PRODUCTS),
                "orders": dict(ORDERS),
                "test_users": dict(TEST_USERS),
                "user_codes": dict(USER_CODES),
                "reymit_links": REYMIT_LINKS,
                "feedbacks": FEEDBACKS,
                "tutorial_channel": TUTORIAL_CHANNEL,
                "password_hash": AUTH["password_hash"],
                "card_number": CARD_NUMBER,
                "card_owner_name": CARD_OWNER_NAME,
                "price_per_gb": PRICE_PER_GB,
                "admin_ids": list(ADMIN_IDS),
                "owner_id": OWNER_ID,
                "saved_at": datetime.now().isoformat(),
            }
            tmp = DATA_FILE.with_suffix(".tmp")
            async with aiofiles.open(tmp, "w", encoding="utf-8") as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=2))
            tmp.replace(DATA_FILE)
        except Exception as e:
            logger.warning(f"Could not save state: {e}")

# ── Startup / Shutdown ────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    global http_client
    limits = httpx.Limits(max_connections=500, max_keepalive_connections=100)
    timeout = httpx.Timeout(30.0, connect=10.0)
    http_client = httpx.AsyncClient(limits=limits, timeout=timeout, follow_redirects=True)
    await load_state()
    await _tg_start_bot()
    log_activity("system", "سرور راه‌اندازی شد", "ok")
    logger.info(f"Tk-Ui v10 started on port {CONFIG['port']}")

@app.on_event("shutdown")
async def shutdown():
    await save_state()
    await _tg_stop_bot()
    if http_client:
        await http_client.aclose()

# ── Telegram bot ─────────────────────────────────────────────────────────────
from telegram_bot import start_bot as _tg_start_bot, stop_bot as _tg_stop_bot

# ── Basic endpoints ──────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {"service": "Tk-Ui", "version": "10", "status": "active", "channel": "https://t.me/TaaKaaOrg"}

@app.get("/health")
async def health():
    return {"status": "ok", "connections": len(connections), "uptime": uptime()}

# ── Auth endpoints ───────────────────────────────────────────────────────────
@app.post("/api/login")
async def api_login(request: Request):
    body = await request.json()
    ip = client_ip(request)
    if hash_password(str(body.get("password", ""))) != AUTH["password_hash"]:
        log_activity("auth", f"تلاش ورود ناموفق از {ip}", "err")
        raise HTTPException(status_code=401, detail="رمز عبور اشتباه است")
    token = await create_session()
    log_activity("auth", f"ورود موفق به پنل از {ip}", "ok")
    resp = JSONResponse({"ok": True})
    resp.set_cookie(SESSION_COOKIE, token, max_age=SESSION_TTL, httponly=True, samesite="lax", path="/")
    return resp

@app.post("/api/logout")
async def api_logout(request: Request):
    await destroy_session(request.cookies.get(SESSION_COOKIE))
    resp = JSONResponse({"ok": True})
    resp.delete_cookie(SESSION_COOKIE, path="/")
    return resp

@app.get("/api/me")
async def api_me(request: Request):
    return {"authenticated": await is_valid_session(request.cookies.get(SESSION_COOKIE))}

@app.post("/api/change-password")
async def api_change_password(request: Request, token=Depends(require_auth)):
    body = await request.json()
    if hash_password(str(body.get("current_password", ""))) != AUTH["password_hash"]:
        raise HTTPException(status_code=400, detail="رمز فعلی اشتباه است")
    new = str(body.get("new_password", ""))
    if len(new) < 4:
        raise HTTPException(status_code=400, detail="رمز جدید باید حداقل ۴ کاراکتر باشد")
    AUTH["password_hash"] = hash_password(new)
    async with SESSIONS_LOCK:
        SESSIONS.clear()
        SESSIONS[token] = time.time() + SESSION_TTL
    await save_state()
    log_activity("auth", "رمز عبور پنل تغییر کرد", "ok")
    return {"ok": True}

# ── Stats ────────────────────────────────────────────────────────────────────
@app.get("/stats")
async def get_stats(_=Depends(require_auth)):
    async with LINKS_LOCK:
        snap = dict(LINKS)
    return {
        "active_connections": len(connections),
        "total_traffic_mb": round(stats["total_bytes"] / (1024 ** 2), 2),
        "total_requests": stats["total_requests"],
        "total_errors": stats["total_errors"],
        "uptime": uptime(),
        "timestamp": datetime.now().isoformat(),
        "hourly": dict(hourly_traffic),
        "recent_errors": list(error_logs)[-10:],
        "links_count": len(snap),
        "active_links": sum(1 for l in snap.values() if is_link_allowed(l)),
        "expired_links": sum(1 for l in snap.values() if is_link_expired(l)),
        "subs_count": len(SUBS),
        "nodes_count": len(NODES),
    }

# ── Activity Logs ────────────────────────────────────────────────────────────
@app.get("/api/activity")
async def get_activity(_=Depends(require_auth)):
    return {"logs": list(activity_logs)[-150:]}

# ── Live connections ────────────────────────────────────────────────────────
@app.get("/api/connections")
async def get_connections(_=Depends(require_auth)):
    async with LINKS_LOCK:
        snap = dict(LINKS)
    result = []
    for conn_id, c in connections.items():
        link = snap.get(c.get("uuid"))
        result.append({
            "ip": c.get("ip", "نامشخص"),
            "label": link.get("label") if link else "نامشخص",
            "transport": c.get("transport", "vless-ws"),
            "bytes": c.get("bytes", 0),
            "bytes_fmt": fmt_bytes(c.get("bytes", 0)),
            "connected_at": c.get("connected_at"),
        })
    result.sort(key=lambda x: x.get("connected_at") or "", reverse=True)
    return {"connections": result, "count": len(result)}

# ── Link Management ──────────────────────────────────────────────────────────
async def make_link(label: str = "لینک جدید", limit_bytes: int = 0, expires_at: str | None = None, note: str = "", sub_id: str | None = None, protocol: str = DEFAULT_PROTOCOL, fingerprint: str = DEFAULT_FINGERPRINT, alpn: str = "", port: int = DEFAULT_PORT, ip_limit: int = 0, speed_limit_bytes: int = 0, node_id: str | None = None) -> tuple[str, dict]:
    if protocol not in PROTOCOLS:
        protocol = DEFAULT_PROTOCOL
    fingerprint = (fingerprint or DEFAULT_FINGERPRINT).strip().lower()
    if fingerprint not in FINGERPRINTS:
        fingerprint = DEFAULT_FINGERPRINT
    uid = generate_uuid()
    async with LINKS_LOCK:
        LINKS[uid] = {
            "label": (label or "لینک جدید").strip()[:60] or "لینک جدید",
            "limit_bytes": max(0, limit_bytes),
            "used_bytes": 0,
            "created_at": datetime.now().isoformat(),
            "active": True,
            "expires_at": expires_at,
            "note": (note or "").strip()[:200],
            "is_default": False,
            "sub_id": sub_id,
            "protocol": protocol,
            "fingerprint": fingerprint,
            "alpn": (alpn or "").strip()[:100],
            "port": port,
            "ip_limit": max(0, ip_limit),
            "speed_limit_bytes": max(0, speed_limit_bytes),
            "node_id": node_id,
        }
    if sub_id:
        async with SUBS_LOCK:
            if sub_id in SUBS:
                ids = SUBS[sub_id].setdefault("link_ids", [])
                if uid not in ids:
                    ids.append(uid)
    if node_id:
        await send_config_to_node(node_id, uid, LINKS[uid])
    asyncio.create_task(save_state())
    log_activity("link", f"کانفیگ «{LINKS[uid]['label']}» ساخته شد", "ok")
    return uid, LINKS[uid]

@app.post("/api/links")
async def create_link(request: Request, _=Depends(require_auth)):
    body = await request.json()
    lv = float(body.get("limit_value") or 0)
    lu = body.get("limit_unit") or "GB"
    limit_bytes = 0 if lv <= 0 else parse_size_to_bytes(lv, lu)
    exp_days = int(body.get("expires_days") or 0)
    expires_at = (datetime.now() + timedelta(days=exp_days)).isoformat() if exp_days > 0 else None
    port = int(body.get("port") or DEFAULT_PORT)
    ip_limit = int(body.get("ip_limit") or 0)
    sv = float(body.get("speed_limit_value") or 0)
    su = body.get("speed_limit_unit") or "MBIT"
    speed_limit_bytes = 0 if sv <= 0 else parse_speed_to_bytes(sv, su)
    node_id = body.get("node_id") or None

    uid, link = await make_link(
        label=body.get("label") or "لینک جدید",
        limit_bytes=limit_bytes,
        expires_at=expires_at,
        note=body.get("note") or "",
        sub_id=body.get("sub_id") or None,
        protocol=body.get("protocol") or DEFAULT_PROTOCOL,
        fingerprint=body.get("fingerprint") or DEFAULT_FINGERPRINT,
        alpn=body.get("alpn") or "",
        port=port,
        ip_limit=ip_limit,
        speed_limit_bytes=speed_limit_bytes,
        node_id=node_id,
    )
    host = get_host(request)
    return {
        "uuid": uid,
        **link,
        "expired": False,
        "vless_link": vless_link_for_link(link, uid, host),
        "sub_url": f"https://{host}/sub/{uid}",
    }

@app.get("/api/links")
async def list_links(request: Request, _=Depends(require_auth)):
    host = get_host(request)
    async with LINKS_LOCK:
        snap = dict(LINKS)
    result = []
    for uid, d in snap.items():
        result.append({
            "uuid": uid,
            **d,
            "expired": is_link_expired(d),
            "vless_link": vless_link_for_link(d, uid, host),
            "sub_url": f"https://{host}/sub/{uid}",
            "connected_ips": len(unique_ips_for_uuid(uid)),
        })
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return {"links": result}

@app.patch("/api/links/{uid}")
async def update_link(uid: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    async with LINKS_LOCK:
        if uid not in LINKS:
            raise HTTPException(status_code=404, detail="link not found")
        link = LINKS[uid]
        old_node = link.get("node_id")
        if "active" in body:
            link["active"] = bool(body["active"])
        if "label" in body:
            link["label"] = str(body["label"])[:60]
        if "note" in body:
            link["note"] = str(body["note"])[:200]
        if "reset_usage" in body and body["reset_usage"]:
            link["used_bytes"] = 0
        if "limit_value" in body:
            lv = float(body.get("limit_value") or 0)
            lu = body.get("limit_unit") or "GB"
            link["limit_bytes"] = 0 if lv <= 0 else parse_size_to_bytes(lv, lu)
        if "expires_days" in body:
            ed = int(body["expires_days"] or 0)
            link["expires_at"] = (datetime.now() + timedelta(days=ed)).isoformat() if ed > 0 else None
        if "fingerprint" in body:
            fp = str(body.get("fingerprint") or DEFAULT_FINGERPRINT).strip().lower()
            link["fingerprint"] = fp if fp in FINGERPRINTS else DEFAULT_FINGERPRINT
        if "alpn" in body:
            link["alpn"] = str(body.get("alpn") or "").strip()[:100]
        if "port" in body:
            link["port"] = int(body.get("port") or DEFAULT_PORT)
        if "ip_limit" in body:
            link["ip_limit"] = max(0, int(body.get("ip_limit") or 0))
        if "speed_limit_value" in body:
            sv = float(body.get("speed_limit_value") or 0)
            su = body.get("speed_limit_unit") or "MBIT"
            link["speed_limit_bytes"] = 0 if sv <= 0 else parse_speed_to_bytes(sv, su)
            from speed_limit import reset_bucket
            reset_bucket(uid)
        new_node = body.get("node_id", "UNCHANGED")
        if new_node != "UNCHANGED":
            link["node_id"] = new_node or None
            if new_node:
                await send_config_to_node(new_node, uid, link)
    if new_node != "UNCHANGED":
        asyncio.create_task(save_state())
    log_activity("link", f"کانفیگ «{link['label']}» ویرایش شد", "info")
    return {"ok": True}

@app.delete("/api/links/{uid}")
async def delete_link(uid: str, _=Depends(require_auth)):
    async with LINKS_LOCK:
        if uid not in LINKS:
            raise HTTPException(status_code=404, detail="link not found")
        label = LINKS[uid].get("label", uid)
        sub_id = LINKS[uid].get("sub_id")
        del LINKS[uid]
    if sub_id:
        async with SUBS_LOCK:
            if sub_id in SUBS:
                ids = SUBS[sub_id].get("link_ids", [])
                if uid in ids:
                    ids.remove(uid)
    asyncio.create_task(save_state())
    log_activity("link", f"کانفیگ «{label}» حذف شد", "err")
    return {"ok": True}

# ── Sub Group Management ────────────────────────────────────────────────────
@app.post("/api/subs")
async def create_sub(request: Request, _=Depends(require_auth)):
    body = await request.json()
    name = (body.get("name") or "گروه جدید").strip()[:60]
    desc = (body.get("desc") or "").strip()[:200]
    password = (body.get("password") or "").strip()
    sub_id = generate_uuid()
    uuid_key = secrets.token_urlsafe(16)
    async with SUBS_LOCK:
        SUBS[sub_id] = {
            "name": name,
            "desc": desc,
            "password_hash": hash_password(password) if password else None,
            "uuid_key": uuid_key,
            "created_at": datetime.now().isoformat(),
            "link_ids": [],
        }
    asyncio.create_task(save_state())
    log_activity("sub", f"گروه «{name}» ساخته شد", "ok")
    host = get_host(request)
    return {
        "sub_id": sub_id,
        **SUBS[sub_id],
        "public_url": f"https://{host}/p/{uuid_key}",
        "sub_url": f"https://{host}/sub-group/{uuid_key}",
    }

@app.get("/api/subs")
async def list_subs(request: Request, _=Depends(require_auth)):
    host = get_host(request)
    async with SUBS_LOCK:
        snap_subs = dict(SUBS)
    async with LINKS_LOCK:
        snap_links = dict(LINKS)
    result = []
    for sid, s in snap_subs.items():
        link_ids = s.get("link_ids", [])
        active_count = sum(1 for lid in link_ids if is_link_allowed(snap_links.get(lid)))
        total_used = sum(snap_links[lid].get("used_bytes", 0) for lid in link_ids if lid in snap_links)
        result.append({
            "sub_id": sid,
            **s,
            "password_hash": None,
            "has_password": s.get("password_hash") is not None,
            "links_count": len(link_ids),
            "active_count": active_count,
            "total_used_bytes": total_used,
            "total_used_fmt": fmt_bytes(total_used),
            "public_url": f"https://{host}/p/{s['uuid_key']}",
            "sub_url": f"https://{host}/sub-group/{s['uuid_key']}",
        })
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return {"subs": result}

@app.patch("/api/subs/{sub_id}")
async def update_sub(sub_id: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(status_code=404, detail="sub not found")
        s = SUBS[sub_id]
        if "name" in body:
            s["name"] = str(body["name"])[:60]
        if "desc" in body:
            s["desc"] = str(body["desc"])[:200]
        if "password" in body:
            pw = str(body["password"]).strip()
            s["password_hash"] = hash_password(pw) if pw else None
        if "link_ids" in body:
            s["link_ids"] = list(body["link_ids"])
    asyncio.create_task(save_state())
    return {"ok": True}

@app.delete("/api/subs/{sub_id}")
async def delete_sub(sub_id: str, _=Depends(require_auth)):
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(status_code=404, detail="sub not found")
        name = SUBS[sub_id].get("name", sub_id)
        del SUBS[sub_id]
    async with LINKS_LOCK:
        for link in LINKS.values():
            if link.get("sub_id") == sub_id:
                link["sub_id"] = None
    asyncio.create_task(save_state())
    log_activity("sub", f"گروه «{name}» حذف شد", "warn")
    return {"ok": True}

# ── Node Management APIs ────────────────────────────────────────────────────
@app.get("/api/nodes")
async def list_nodes(_=Depends(require_auth)):
    return {"nodes": list(NODES.values())}

@app.post("/api/nodes")
async def add_node(request: Request, _=Depends(require_auth)):
    body = await request.json()
    node_id = generate_uuid()
    node = {
        "id": node_id,
        "name": body.get("name", f"Node-{node_id[:8]}"),
        "address": body.get("address"),
        "port": int(body.get("port", 62050)),
        "cert": body.get("cert"),
        "status": "pending",
        "usage_coefficient": float(body.get("usage_coefficient", 1.0)),
        "created_at": datetime.now().isoformat(),
    }
    async with NODES_LOCK:
        NODES[node_id] = node
    asyncio.create_task(save_state())
    log_activity("node", f"Node «{node['name']}» اضافه شد", "ok")
    return {"ok": True, "node": node}

@app.patch("/api/nodes/{node_id}")
async def update_node(node_id: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    async with NODES_LOCK:
        if node_id not in NODES:
            raise HTTPException(status_code=404, detail="Node not found")
        node = NODES[node_id]
        for key in ("name", "address", "port", "cert", "status", "usage_coefficient"):
            if key in body:
                node[key] = body[key]
    asyncio.create_task(save_state())
    log_activity("node", f"Node «{node['name']}» به‌روزرسانی شد", "info")
    return {"ok": True}

@app.delete("/api/nodes/{node_id}")
async def delete_node(node_id: str, _=Depends(require_auth)):
    async with NODES_LOCK:
        if node_id not in NODES:
            raise HTTPException(status_code=404, detail="Node not found")
        name = NODES[node_id]["name"]
        del NODES[node_id]
    asyncio.create_task(save_state())
    log_activity("node", f"Node «{name}» حذف شد", "warn")
    return {"ok": True}

# ── Subscription endpoints ──────────────────────────────────────────────────
@app.get("/sub/{uuid}")
async def subscription_single(uuid: str, request: Request):
    import base64
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
    if not link or not is_link_allowed(link):
        raise HTTPException(status_code=404, detail="not found or inactive")
    host = get_host(request)
    vless = vless_link_for_link(link, uuid, host)
    content = base64.b64encode(vless.encode()).decode()
    return Response(content=content, media_type="text/plain", headers={"profile-title": quote(link["label"]), "support-url": "https://t.me/ItzJustEren"})

@app.get("/sub-all")
async def subscription_all(request: Request, _=Depends(require_auth)):
    import base64
    host = get_host(request)
    async with LINKS_LOCK:
        lines = [vless_link_for_link(d, uid, host) for uid, d in LINKS.items() if is_link_allowed(d)]
    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain")

@app.get("/sub-group/{uuid_key}")
async def sub_group_subscription(uuid_key: str, request: Request):
    import base64
    async with SUBS_LOCK:
        sub = next((s for s in SUBS.values() if s.get("uuid_key") == uuid_key), None)
    if not sub:
        raise HTTPException(status_code=404, detail="not found")
    if sub.get("password_hash"):
        pw = request.query_params.get("pw", "")
        if hash_password(pw) != sub["password_hash"]:
            raise HTTPException(status_code=403, detail="wrong password")
    host = get_host(request)
    link_ids = sub.get("link_ids", [])
    async with LINKS_LOCK:
        lines = [vless_link_for_link(LINKS[lid], lid, host) for lid in link_ids if lid in LINKS and is_link_allowed(LINKS[lid])]
    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain", headers={"profile-title": quote(sub["name"]), "support-url": "https://t.me/ItzJustEren"})

# ── Public sub page ─────────────────────────────────────────────────────────
@app.get("/p/{uuid_key}", response_class=HTMLResponse)
async def public_sub_page(uuid_key: str, request: Request):
    from pages import get_public_page_html
    async with SUBS_LOCK:
        sub = next(({"sub_id": sid, **s} for sid, s in SUBS.items() if s.get("uuid_key") == uuid_key), None)
    if not sub:
        return HTMLResponse("<h2 style='font-family:sans-serif;padding:40px'>گروه پیدا نشد</h2>", status_code=404)
    return HTMLResponse(content=get_public_page_html(uuid_key))

@app.get("/api/public/sub/{uuid_key}")
async def public_sub_data(uuid_key: str, request: Request):
    async with SUBS_LOCK:
        sub_entry = next(((sid, s) for sid, s in SUBS.items() if s.get("uuid_key") == uuid_key), None)
    if not sub_entry:
        raise HTTPException(status_code=404, detail="not found")
    sub_id, sub = sub_entry
    has_pw = sub.get("password_hash") is not None
    if has_pw:
        pw = request.query_params.get("pw", "")
        if hash_password(pw) != sub["password_hash"]:
            return JSONResponse({"locked": True, "name": sub["name"]})
    host = get_host(request)
    link_ids = sub.get("link_ids", [])
    async with LINKS_LOCK:
        snap = dict(LINKS)
    links_out = []
    active_conns = 0
    for lid in link_ids:
        link = snap.get(lid)
        if not link:
            continue
        allowed = is_link_allowed(link)
        conn_count = sum(1 for c in connections.values() if c.get("uuid") == lid)
        active_conns += conn_count
        links_out.append({
            "uuid": lid,
            "label": link["label"],
            "active": allowed,
            "protocol": link.get("protocol", DEFAULT_PROTOCOL),
            "used_bytes": link.get("used_bytes", 0),
            "used_fmt": fmt_bytes(link.get("used_bytes", 0)),
            "limit_bytes": link.get("limit_bytes", 0),
            "limit_fmt": "∞" if link.get("limit_bytes", 0) == 0 else fmt_bytes(link["limit_bytes"]),
            "expires_at": link.get("expires_at"),
            "vless_link": vless_link_for_link(link, lid, host),
            "sub_url": f"https://{host}/sub/{lid}",
            "connections": conn_count,
        })
    total_used = sum(l["used_bytes"] for l in links_out)
    return {
        "locked": False,
        "name": sub["name"],
        "desc": sub.get("desc", ""),
        "sub_url": f"https://{host}/sub-group/{uuid_key}",
        "active_connections": active_conns,
        "total_used_fmt": fmt_bytes(total_used),
        "links": links_out,
    }

# ── Product APIs ────────────────────────────────────────────────────────────
@app.get("/api/products")
async def list_products(_=Depends(require_auth)):
    return {"products": list(PRODUCTS.values())}

@app.post("/api/products")
async def create_product(request: Request, _=Depends(require_auth)):
    body = await request.json()
    name = body.get("name", "").strip()
    if not name:
        raise HTTPException(400, "نام محصول الزامی است")
    volume_gb = float(body.get("volume_gb", 0))
    duration_days = int(body.get("duration_days", 0))
    speed_mbps = float(body.get("speed_mbps", 0))
    if volume_gb <= 0 or duration_days <= 0:
        raise HTTPException(400, "حجم و مدت باید مثبت باشند")
    price = volume_gb * PRICE_PER_GB
    product_id = secrets.token_hex(8)
    async with PRODUCTS_LOCK:
        PRODUCTS[product_id] = {"product_id": product_id, "name": name, "volume_gb": volume_gb, "duration_days": duration_days, "speed_mbps": speed_mbps, "price": price, "created_at": datetime.now().isoformat()}
    asyncio.create_task(save_state())
    log_activity("product", f"محصول «{name}» با قیمت {price} تومان اضافه شد", "ok")
    return {"ok": True, "product_id": product_id}

@app.delete("/api/products/{product_id}")
async def delete_product(product_id: str, _=Depends(require_auth)):
    async with PRODUCTS_LOCK:
        if product_id not in PRODUCTS:
            raise HTTPException(404, "محصول یافت نشد")
        name = PRODUCTS[product_id]["name"]
        del PRODUCTS[product_id]
    asyncio.create_task(save_state())
    log_activity("product", f"محصول «{name}» حذف شد", "warn")
    return {"ok": True}

# ── Order APIs ──────────────────────────────────────────────────────────────
@app.get("/api/orders")
async def list_orders(_=Depends(require_auth)):
    return {"orders": list(ORDERS.values())}

@app.patch("/api/orders/{order_id}")
async def update_order(order_id: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    status = body.get("status")
    async with ORDERS_LOCK:
        if order_id not in ORDERS:
            raise HTTPException(404, "سفارش یافت نشد")
        if status:
            ORDERS[order_id]["status"] = status
    asyncio.create_task(save_state())
    return {"ok": True}

# ── Admin APIs ──────────────────────────────────────────────────────────────
@app.get("/api/admins")
async def list_admins(_=Depends(require_auth)):
    return {"admins": list(ADMIN_IDS), "owner_id": OWNER_ID}

@app.post("/api/admins")
async def add_admin(request: Request, _=Depends(require_auth)):
    body = await request.json()
    user_id = int(body.get("user_id"))
    if not user_id:
        raise HTTPException(400, "user_id الزامی است")
    global ADMIN_IDS
    ADMIN_IDS.add(user_id)
    os.environ["TELEGRAM_ADMIN_IDS"] = ",".join(str(x) for x in ADMIN_IDS)
    asyncio.create_task(save_state())
    log_activity("admin", f"ادمین جدید اضافه شد: {user_id}", "ok")
    return {"ok": True}

@app.delete("/api/admins/{user_id}")
async def remove_admin(user_id: int, _=Depends(require_auth)):
    if user_id == OWNER_ID:
        raise HTTPException(400, "نمی‌توان اونر را حذف کرد")
    global ADMIN_IDS
    if user_id not in ADMIN_IDS:
        raise HTTPException(404, "ادمین یافت نشد")
    ADMIN_IDS.remove(user_id)
    os.environ["TELEGRAM_ADMIN_IDS"] = ",".join(str(x) for x in ADMIN_IDS)
    asyncio.create_task(save_state())
    log_activity("admin", f"ادمین حذف شد: {user_id}", "warn")
    return {"ok": True}

# ── Settings APIs ────────────────────────────────────────────────────────────
@app.get("/api/settings/card")
async def get_card_settings(_=Depends(require_auth)):
    return {"card_number": CARD_NUMBER, "card_owner_name": CARD_OWNER_NAME}

@app.post("/api/settings/card")
async def set_card_settings(request: Request, _=Depends(require_auth)):
    body = await request.json()
    new_card = body.get("card_number", "").strip()
    if not new_card:
        raise HTTPException(400, "شماره کارت نمی‌تواند خالی باشد")
    global CARD_NUMBER, CARD_OWNER_NAME
    CARD_NUMBER = new_card
    CARD_OWNER_NAME = body.get("card_owner_name", "").strip() or CARD_OWNER_NAME
    os.environ["CARD_NUMBER"] = new_card
    os.environ["CARD_OWNER_NAME"] = CARD_OWNER_NAME
    asyncio.create_task(save_state())
    return {"ok": True}

# ── WebSocket VLESS ──────────────────────────────────────────────────────────
from relay_vless import websocket_tunnel
app.add_api_websocket_route("/ws/{uuid}", websocket_tunnel)

# ── XHTTP ────────────────────────────────────────────────────────────────────
from xhttp_siz10 import router as xhttp_router
app.include_router(xhttp_router)

# ── HTTP Proxy ──────────────────────────────────────────────────────────────
_HOP = {"connection","keep-alive","proxy-authenticate","proxy-authorization","te","trailers","transfer-encoding","upgrade","content-encoding","content-length"}

@app.api_route("/proxy/{target_url:path}", methods=["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS"])
async def http_proxy(target_url: str, request: Request):
    if not target_url.startswith("http"):
        target_url = "https://" + target_url
    try:
        body = await request.body()
        headers = {k: v for k, v in request.headers.items() if k.lower() not in _HOP and k.lower() != "host"}
        resp = await http_client.request(method=request.method, url=target_url, headers=headers, content=body)
        stats["total_bytes"] += len(resp.content)
        stats["total_requests"] += 1
        hourly_traffic[now_ir().strftime("%H:00")] += len(resp.content)
        return Response(content=resp.content, status_code=resp.status_code, headers={k: v for k, v in resp.headers.items() if k.lower() not in _HOP})
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "url": target_url, "time": datetime.now().isoformat()})
        raise HTTPException(status_code=502, detail=f"Proxy error: {exc}")

# ── HTML Pages ──────────────────────────────────────────────────────────────
from pages import LOGIN_HTML, DASHBOARD_HTML

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse(url="/dashboard")
    return HTMLResponse(content=LOGIN_HTML)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse(url="/login")
    return HTMLResponse(content=DASHBOARD_HTML)

@app.get("/test-ws", response_class=HTMLResponse)
async def test_ws_redirect():
    return HTMLResponse(content="<script>location.href='/dashboard'</script>")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=CONFIG["port"], log_level="info", workers=1)
