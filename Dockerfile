# 不要用 Python 3.13，discord.py 目前最穩是 3.12
FROM python:3.12-slim

# Python 行為設定（Docker 標準）
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 先複製 requirements，利用 Docker cache
COPY requirements.txt .

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 再複製其他程式碼
COPY . .

# 啟動 bot
CMD ["python", "bot.py"]
