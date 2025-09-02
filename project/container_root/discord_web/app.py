from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv
import os
import time
import random

# .envファイルを読み込み、環境変数を設定
load_dotenv()

app = FastAPI()

# 環境変数からCORSのオリジンを読み込む
origins = os.getenv("CORS_ORIGINS", "").split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 起動時間を記録
start_time = time.time()

# 稼働時間を計算するヘルパー関数
def get_uptime():
    uptime_seconds = time.time() - start_time
    days = int(uptime_seconds // (24 * 3600))
    hours = int((uptime_seconds % (24 * 3600)) // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)
    return f"{days}日 {hours}時間 {minutes}分 {seconds}秒"

# APIエンドポイント
@app.get("/api/status")
async def get_bot_status():
    status_data = {
        "ping": random.randint(50, 250),
        "servers": random.randint(1000, 5000),
        "users": random.randint(5000, 15000),
        "uptime": get_uptime(),
        "status": "Online",
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    return status_data

# HTMLファイルを配置するディレクトリ
templates = Jinja2Templates(directory="templates")

# 静的ファイルのルーティング
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTMLページのルーティング
@app.get("/", response_class=HTMLResponse)
async def serve_home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/commands", response_class=HTMLResponse)
async def serve_commands_page(request: Request):
    return templates.TemplateResponse("commands.html", {"request": request})

@app.get("/status", response_class=HTMLResponse)
async def serve_status_page(request: Request):
    return templates.TemplateResponse("status.html", {"request": request})

@app.get("/{path:path}", response_class=HTMLResponse)
async def serve_all_pages(request: Request, path: str):
    # 例外的なパスを処理
    if path.startswith("api/"):
        return {"error": "Not Found"} # or some other error response
        
    return templates.TemplateResponse("404.html", {"request": request})