# Memos to iCal Bridge

A lightweight Flask application that exposes [Memos](https://github.com/usememos/memos) entries as a dynamic iCalendar (`.ics`) feed.

## Motivation
[Memos](https://github.com/usememos/memos) is an open-source, self-hosted note-taking application designed for quick capture and daily logs. This bridge queries your Memos instance and transforms entries into iCalendar-compliant events so they can be displayed alongside regular schedule items on your personal calendar grid.

## Functionality
* Queries the Memos v1 API for recent entries.
* Formats content into iCalendar-compliant `VEVENT` objects.
* Serves a live `.ics` feed on `/memos.ics` for calendar clients to poll automatically.

## Prerequisites
* Docker and Docker Compose
* A running [Memos](https://github.com/usememos/memos) instance
* A Memos Personal Access Token (PAT)

---

## Configuration

1. Generate a Personal Access Token in Memos:
   * Go to **Settings** -> **Access Tokens**.
   * Click **Create Token** and copy the generated token string.

2. Open `app.py` in a text editor and update the configuration section at the top:
   ```python
   # ================= CONFIGURATION =================
   MEMOS_BASE_URL = "http://memos:5230"  # URL or container name of your Memos instance
   MEMOS_API_TOKEN = "your_memos_pat_here"  # Your Memos Personal Access Token
   # =================================================
   ```

---

## Installation & Testing

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/memos-to-ical-bridge.git
   cd memos-to-ical-bridge
   ```

2. Build and start the container using Docker Compose:
   ```bash
   docker compose up -d --build
   ```

3. Test local functionality:
   * **Linux / macOS:**
     ```bash
     curl -s http://localhost:5321/memos.ics
     ```
   * **Windows (PowerShell):**
     ```powershell
     curl.exe -s "http://localhost:5321/memos.ics"
     ```
   * If working properly, the output will start with `BEGIN:VCALENDAR` and list your memos as events.

---

## Calendar Integration

Expose `http://localhost:5321/memos.ics` via a reverse proxy or tunnel (e.g., Cloudflare Tunnel) to generate a public HTTPS URL (e.g., `https://your-domain.com/memos.ics`).

### Subscribing to the Feed

#### Proton Calendar
1. Open Proton Calendar on the web.
2. In the left sidebar, click **`+`** (Add calendar) next to **My calendars**.
3. Select **Add calendar from URL**.
4. Paste your public HTTPS feed URL, set a calendar name, and click **Add calendar**.

#### Google Calendar
1. Open Google Calendar on the web.
2. In the left sidebar, click **`+`** next to **Other calendars**.
3. Select **From URL**.
4. Paste your public HTTPS feed URL and click **Add calendar**.

#### Outlook (Web)
1. Open Outlook Calendar on the web.
2. Click **Add calendar** in the left navigation panel.
3. Select **Subscribe from web**.
4. Paste your public HTTPS feed URL, type a calendar name, and click **Import**.

---

## License
Distributed under the MIT License.
