# Discord 公告機器人 (Announce Bot)

一個多功能的 Discord 機器人，專為伺服器管理設計。它提供格式化的公告、成員資訊匯出以及完整的 Docker 部署支援，讓您的伺服器管理更加輕鬆高效。

---

## 目錄
- [主要特色](#主要特色)
- [可用指令](#可用指令)
- [安裝與設定](#安裝與設定)
  - [第一步：在 Discord 建立機器人](#第一步在-discord-建立機器人)
  - [第二步：設定環境變數](#第二步設定環境變數)
  - [第三步：準備本地環境](#第三步準備本地環境)
- [運行方式](#運行方式)
  - [本地運行](#本地運行)
  - [使用 Docker 部署 (推薦)](#使用-docker-部署-推薦)
- [進階設定](#進階設定)
  - [自定義管理員角色](#自定義管理員角色)
  - [版本控制建議 (`.gitignore`)](#版本控制建議-gitignore)

---

## 主要特色

- **現代化斜線指令**：所有功能均透過易於使用的斜線指令 (`/`) 進行操作。
- **專業級公告**：發布美觀的嵌入式 (Embed) 公告，提升資訊傳達的專業度。
- **成員資料匯出**：一鍵將伺服器所有成員的名稱及身份組匯出為 CSV 檔案，便於管理和分析。
- **權限控管**：核心功能 (`/announce`, `/members`) 僅限伺服器管理員或指定角色使用，確保安全。
- **Docker 支援**：內建 `Dockerfile`，支援一鍵部署，實現 24/7 全天候穩定運行。

## 可用指令

| 指令 | 說明 | 權限要求 |
| --- | --- | --- |
| `/announce <頻道> <訊息> [mention_everyone]` | 發布一則格式化的公告到指定的文字頻道，可選是否 `@everyone`。 | **管理員** |
| `/members` | 匯出伺服器所有成員的名稱及身份組為 `members_export.csv` 檔案。 | **管理員** |
| `/help` | 顯示所有可用指令的說明訊息。 | 所有使用者 |

## 安裝與設定

### 第一步：在 Discord 建立機器人

1.  **建立應用程式**：前往 [Discord Developer Portal](https://discord.com/developers/applications) 並點擊 "New Application"。
2.  **命名並建立**：為您的機器人命名，然後點擊 "Create"。
3.  **新增 Bot**：在左側導航欄選擇 "Bot"，點擊 "Add Bot"，然後確認 "Yes, do it!"。
4.  **啟用 Privileged Intents**：
    > 這是最重要的一步！如果未啟用，機器人將無法正常工作。
    *   向下滾動到 "Privileged Gateway Intents"。
    *   啟用 `SERVER MEMBERS INTENT`。
    *   啟用 `MESSAGE CONTENT INTENT`。
5.  **獲取 Token**：在 "Token" 區塊點擊 "Reset Token" (或 "Copy") 來獲取您的機器人 Token。
    > **警告**：此 Token 等同於您機器人的密碼，**絕對不要**與任何人分享或上傳到公開的程式碼倉庫 (如 GitHub)。

6.  **邀請機器人到伺服器**：
    > **重要提示：請只使用此「URL Generator」頁面！**
    > 如果您在生成邀請連結時遇到「Please enter a redirect uri」的錯誤，表示您可能誤觸了 `OAuth2 -> General` 頁面的設定。我們的機器人僅使用 Bot Token 登入，不需要 OAuth2 的使用者登入流程。
    > **請勿在 `OAuth2 -> General` 頁面設定或儲存任何 Redirect URIs。**
    *   在左側導航欄選擇 "OAuth2" -> "URL Generator"。
    *   在 "SCOPES" 下勾選 `bot` 和 `applications.commands`。
    *   在 "BOT PERMISSIONS" 下，選擇您希望賦予的權限。為了方便，您可以選擇 `Administrator` (管理員)，或者手動選擇以下必要權限：
        - `View Channels` (查看頻道)
        - `Send Messages` (發送訊息)
        - `Embed Links` (嵌入連結)
        - `Use Slash Commands` (使用斜線指令)
        - `Read Message History` (讀取訊息歷史)
        - `Mention Everyone` (提及所有人)
    *   複製頁面下方生成的 URL，在瀏覽器中打開它，然後選擇您的伺服器進行邀請。

### 第二步：設定環境變數

在專案的根目錄中建立一個名為 `.env` 的檔案。此檔案用於存放您的敏感資訊。

```
DISCORD_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
GUILD_ID="YOUR_GUILD_ID_HERE"
ALLOWED_ANNOUNCE_CHANNELS="YOUR_CHANNEL_ID_1,YOUR_CHANNEL_ID_2"
```

- **`DISCORD_BOT_TOKEN`**：貼上您在上一步中獲取的機器人 Token。
- **`GUILD_ID`**：您希望機器人主要在哪個伺服器運作的 ID。
- **`ALLOWED_ANNOUNCE_CHANNELS`**：`(選填)` 允許發布公告的頻道 ID 列表，用逗號分隔。如果留空，則所有頻道都允許。

### 第三步：準備本地環境

1.  **安裝 Python**：確保您的系統已安裝 Python 3.8 或更高版本。
2.  **建立虛擬環境** (推薦)：
    ```bash
    python -m venv .venv
    ```
3.  **啟動虛擬環境**：
    -   Windows: `.venv\Scripts\activate`
    -   macOS/Linux: `source .venv/bin/activate`
4.  **安裝依賴套件**：
    ```bash
    pip install -r requirements.txt
    ```

## 運行方式

### 本地運行
確保您已啟動虛擬環境，然後運行：
```bash
python bot.py
```
您應該會在終端機中看到 `Logged in as ...` 的訊息，表示機器人已成功上線。

### 使用 Docker 部署 (推薦)
Docker 是實現 24/7 運行的最佳方式。

1.  **安裝 Docker**：請從 [Docker 官方網站](https://www.docker.com/get-started) 下載並安裝 Docker。
2.  **建置映像**：在專案根目錄下執行此指令。
    ```bash
    docker build -t announce-bot .
    ```
3.  **運行容器**：
    ```bash
    docker run -d --name my-announce-bot --env-file .env --restart unless-stopped announce-bot
    ```
    - `-d`：在背景運行。
    - `--name my-announce-bot`：為您的容器取一個名字。
    - `--env-file .env`：從 `.env` 檔案載入環境變數。
    - `--restart unless-stopped`：確保容器在意外關閉或重啟時自動重新啟動。

4.  **管理容器**：
    -   查看日誌：`docker logs -f my-announce-bot`
    -   停止容器：`docker stop my-announce-bot`
    -   移除容器：`docker rm my-announce-bot`

## 進階設定

### 自定義管理員角色
您可以修改 `config.py` 中的 `ADMIN_ROLE_NAME` 變數，以指定除了伺服器管理員外，哪個角色可以使用管理指令 (`/announce`, `/members`)。
```python
# config.py
ADMIN_ROLE_NAME = "Mods" # 將 'Admin' 改為 'Mods'
```

### 限定公告頻道
您可以透過設定 `.env` 檔案中的 `ALLOWED_ANNOUNCE_CHANNELS` 變數來限制 `/announce` 指令可以發布公告的頻道。

- **如何設定**：
    1.  在 Discord 中，對您想要允許的文字頻道點擊右鍵，選擇「複製 ID」。
    2.  將這個 ID 貼到 `.env` 檔案的 `ALLOWED_ANNOUNCE_CHANNELS` 變數中。
    3.  如果您想允許多個頻道，請用逗號 (`,`) 分隔每個 ID，例如：
        ```
        ALLOWED_ANNOUNCE_CHANNELS=123456789012345678,876543210987654321
        ```
- **留空的效果**：如果您將 `ALLOWED_ANNOUNCE_CHANNELS` 留空，機器人將允許在伺服器的任何頻道中使用 `/announce` 指令。

### 版本控制建議 (`.gitignore`)
如果您使用 Git 進行版本控制，強烈建議您建立一個 `.gitignore` 檔案，以防止敏感資訊和不必要的檔案被上傳。
```gitignore
# .gitignore

# 虛擬環境
.venv/

# 環境變數檔案
.env

# Python 緩存
__pycache__/
*.pyc
```