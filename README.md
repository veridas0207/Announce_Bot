# Discord 公告機器人 (Announce Bot)

這是一個多功能的 Discord 機器人，專為伺服器管理設計。它提供格式化的公告、成員資訊匯出以及完整的 Docker 部署支援，讓您的伺服器管理更加輕鬆高效。

---

## 目錄
- [事前準備](#-事前準備)
- [安裝與設定 (五步驟)](#-安裝與設定-五步驟)
  - [步驟一：建立 Discord 機器人](#步驟一建立-discord-機器人)
  - [步驟二：取得機器人程式碼](#步驟二取得機器人程式碼)
  - [步驟三：設定機器人](#步驟三設定機器人)
  - [步驟四：安裝與執行](#步驟四安裝與執行)
  - [步驟五：邀請機器人至伺服器](#步驟五邀請機器人至伺服器)
- [使用指令](#-使用指令)
- [機器人權限設定](#-機器人權限設定)
- [進階部署 (Docker)](#-進階部署-docker)
- [進階設定](#-進階設定)

---

## 📝 事前準備

在開始之前，請確保您擁有：
1.  一個 Discord 帳號。
2.  已安裝 Python 3.8 或更高版本。
3.  已安裝 Git。
4.  (選用) 已安裝 Docker，用於生產環境部署。

---

## 🚀 安裝與設定 (五步驟)

請依照以下五個步驟來完成設定：

### 步驟一：建立 Discord 機器人

1.  **建立應用程式**：前往 [Discord Developer Portal](https://discord.com/developers/applications) 並點擊 "New Application"。
2.  **命名並建立**：為您的機器人命名，然後點擊 "Create"。
3.  **新增 Bot**：在左側導覽欄選擇 "Bot"，點擊 "Add Bot"，然後確認 "Yes, do it!"。
4.  **取得 Token**：在 "Token" 區塊點擊 "Reset Token" (或 "Copy") 來獲取您的機器人 Token。
    > **⚠️ 警告**：此 Token 等同於您機器人的密碼，**絕對不要**與任何人分享或上傳到公開的程式碼倉庫。
5.  **啟用 Privileged Intents**：
    > 這是最重要的一步！如果未啟用，機器人將無法正常工作。
    *   向下滾動到 "Privileged Gateway Intents"。
    *   啟用 `SERVER MEMBERS INTENT`。
    *   啟用 `MESSAGE CONTENT INTENT`。

### 步驟二：取得機器人程式碼
在您的電腦上打開終端機 (Terminal)，並執行以下指令：
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 步驟三：設定機器人
在專案的根目錄中，建立一個名為 `.env` 的檔案，並填入以下內容。這是您的機器人設定檔。

```
DISCORD_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
GUILD_ID="YOUR_GUILD_ID_HERE"
ADMIN_ROLE_NAME="Admin"
ALLOWED_ANNOUNCE_CHANNELS="YOUR_CHANNEL_ID_1,YOUR_CHANNEL_ID_2"
```

**變數說明：**
- `DISCORD_BOT_TOKEN`：(必須) 貼上您在**步驟一**中獲取的機器人 Token。
- `GUILD_ID`：(必須) 您的 Discord 伺服器 ID。
- `ADMIN_ROLE_NAME` (選填): 具有管理權限的角色名稱 (預設為 "Admin")。
- `ALLOWED_ANNOUNCE_CHANNELS` (選填)：允許發布公告的頻道 ID 列表，用逗號分隔。如果留空，則所有頻道都允許。

### 步驟四：安裝與執行

1.  **建立並啟動虛擬環境** (推薦)：
    ```bash
    # 建立虛擬環境
    python -m venv .venv

    # 啟動虛擬環境 (請根據您的作業系統選擇)
    # Windows:
    .venv\Scripts\activate
    # macOS/Linux:
    source .venv/bin/activate
    ```
2.  **安裝依賴套件**：
    ```bash
    pip install -r requirements.txt
    ```
3.  **執行機器人**：
    ```bash
    python bot.py
    ```
    當您在終端機中看到 `Logged in as ...` 的訊息時，表示機器人已成功上線。

### 步驟五：邀請機器人至伺服器

1.  **產生邀請連結**：
    *   回到 [Discord Developer Portal](https://discord.com/developers/applications)。
    *   在左側導覽欄選擇 "OAuth2" -> "URL Generator"。
2.  **設定權限**：
    *   在 "SCOPES" 下勾選 `bot` 和 `applications.commands`。
    *   在 "BOT PERMISSIONS" 下，選擇您希望賦予的權限。為了方便，您可以選擇 `Administrator` (管理員)，或者手動選擇以下必要權限 (詳見 [機器人權限設定](#-機器人權限設定))：
        - `View Channels` (查看頻道)
        - `Send Messages` (發送訊息)
        - `Embed Links` (嵌入連結)
        - `Use Slash Commands` (使用斜線指令)
        - `Read Message History` (讀取訊息歷史)
        - `Mention Everyone` (提及所有人)
3.  **邀請**：
    *   複製頁面下方生成的 URL，在瀏覽器中打開它，然後選擇您的伺服器進行邀請。

---

## 🤖 使用指令

| 指令 | 說明 | 權限要求 |
| --- | --- | --- |
| `/announce <頻道> [mention_everyone]` | 彈出一個表單，讓您輸入多行文字來發布公告。 | **管理員** |
| `/members` | 匯出伺服器所有成員的名稱及身份組為 `members_export.csv` 檔案。 | **管理員** |
| `/help` | 顯示所有可用指令的說明訊息。 | 所有使用者 |

---

## 🔒 機器人權限設定

為了讓機器人能正常運作，您需要在邀請機器人時賦予它以下權限。您可以選擇直接賦予 `Administrator` 權限，或者手動勾選以下必要權限：

-   `View Channels` (查看頻道)：機器人需要查看頻道才能接收指令和發送訊息。
-   `Send Messages` (發送訊息)：機器人需要發送訊息來回應指令和發布公告。
-   `Embed Links` (嵌入連結)：發布公告時會使用嵌入式訊息 (Embed)，需要此權限才能正常顯示。
-   `Use Slash Commands` (使用斜線指令)：機器人所有功能都透過斜線指令操作。
-   `Read Message History` (讀取訊息歷史)：在某些情況下，機器人可能需要讀取訊息歷史（例如，為了更好的上下文處理，雖然此機器人目前主要依賴斜線指令，但為了未來擴展性建議賦予）。
-   `Mention Everyone` (提及所有人)：`/announce` 指令中如果選擇 `@everyone` 功能，需要此權限。

---

## 🚢 進階部署 (Docker)

如果您希望機器人 24/7 全天候運行，推薦使用 Docker。

1.  **建置映像**：
    ```bash
    docker build -t announce-bot .
    ```
2.  **運行容器**：
    ```bash
    docker run -d --name my-announce-bot --env-file .env --restart unless-stopped announce-bot
    ```
    - `-d`：在背景運行。
    - `--name my-announce-bot`：為您的容器取一個名字。
    - `--env-file .env`：從 `.env` 檔案載入環境變數。
    - `--restart unless-stopped`：確保容器在意外關閉或重啟時自動重新啟動。

---

## 🔧 進階設定

### 自定義管理員角色
您可以修改 `.env` 檔案中的 `ADMIN_ROLE_NAME` 變數，以指定除了伺服器擁有者外，哪個角色可以使用管理指令。

### 限定公告頻道
您可以透過設定 `.env` 檔案中的 `ALLOWED_ANNOUNCE_CHANNELS` 變數來限制 `/announce` 指令可以發布公告的頻道。請將您想允許的頻道 ID 填入，並用逗號 (`,`) 分隔。

### 版本控制 (`.gitignore`)
建議將以下內容加入 `.gitignore` 檔案，以避免敏感資訊和不必要的檔案被上傳。
```gitignore
# 虛擬環境
.venv/

# 環境變數檔案
.env

# Python 緩存
__pycache__/
*.pyc
```
