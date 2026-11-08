# Memos to iCal Bridge (`memos-to-ics`)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

A lightweight, security-hardened Python service that bridges your self-hosted [Memos](https://github.com/usememos/memos) notes into a dynamic iCalendar (`.ics`) feed. Display your daily notes, journal entries, and quick captures alongside regular schedule items on any personal calendar grid.

---

## Features

- **Multi-Version Memos API Compatibility**: Built-in fallback routing supports both legacy (`/api/v1/memos`) and updated (`/api/v1/memo`) endpoint structures across Memos releases.
- **Security-Hardened Docker Base**: Built on `python:3.12-slim` and executes as an unprivileged, non-root user (`appuser`, UID `10001`) with pinned dependencies for SonarCloud/SAST compliance.
- **Production-Grade Server**: Powered by Gunicorn with tuned request timeouts (`--timeout 60` and 3s socket connections) to eliminate worker timeouts and `SIGKILL` events during network latency.
- **Dockhand & Homelab Friendly**: Pre-configured with local image tagging support (`local/memo-to-ics:latest`) and strict `pull_policy: never` declarations for offline or local-first stack managers.

---

## Architecture & Configuration

The application queries your internal Memos instance on port `5320` (or custom IP) and outputs a valid `.ics` feed on port `5321`.

### 1. Generate Memos Access Token
1. In your Memos web interface, navigate to **Settings** $\rightarrow$ **Access Tokens**.
2. Click **Create Token** and copy your generated Personal Access Token (PAT).

### 2. Configure `app.py`
Open `app.py` and set your internal Memos instance URL and access token:

```python
# ================= CONFIGURATION =================
MEMOS_BASE_URL = "http://192.168.68.102:5320"  # Your Memos instance URL (no trailing slash)
MEMOS_API_TOKEN = "memos_pat_xxxxxxxxxxxxxxxxxxxxxx"  # Your Memos PAT
# =================================================
```

---

## Quick Start (Docker Build & Deployment)

### 1. Build and Tag the Image Locally
Execute the build command on your host machine to compile the pinned dependencies and generate the local tag:

```bash
docker build -t memo-to-ics:latest /srv/ssd/Appdata/local/memos-to-ics-bridge-app
docker tag memo-to-ics:latest local/memo-to-ics:latest
```

### 2. Deploy via Docker Compose

Use the following `compose.yaml` (compatible with Dockhand, Portainer, or CLI):

```yaml
services:
  memo-to-ics:
    image: local/memo-to-ics:latest
    pull_policy: never
    container_name: memo-to-ics
    ports:
      - "5321:5321"
    restart: unless-stopped
    networks:
      apps_default:

networks:
  apps_default:
    external: true
```

Start the container stack:

```bash
docker compose -f /srv/ssd/Appdata/stacks/stacks/RWPI/memos-to-ics-bridge-app/compose.yaml up -d --force-recreate
```

> **Dockhand Note**: When deploying or force-recreating inside the Dockhand UI, ensure the **"Pull images"** option is turned **OFF** so Dockhand uses the locally built image tag (`local/memo-to-ics:latest`).

---

## Verification & Testing

### Test Feed Generation
Verify the container process status and query the live endpoint:

```bash
# Verify container is executing as non-root user 'appuser'
docker exec memo-to-ics whoami
# Output: appuser

# Fetch calendar feed output
curl -s http://localhost:5321/memos.ics
```

*Expected Output*: A valid iCalendar payload starting with `BEGIN:VCALENDAR` and listing your recent Memos entries as `VEVENT` objects.

---

## Calendar Client Setup

Expose `http://<PI_IP>:5321/memos.ics` directly on your LAN or route it through a reverse proxy/tunnel (e.g., Nginx, Traefik, Cloudflare Tunnel) to obtain a public HTTPS URL (`https://your-domain.com/memos.ics`).

### Subscribing to the Feed

- **Apple Calendar (iOS / macOS)**:
  1. Open Calendar $\rightarrow$ **File** $\rightarrow$ **New Calendar Subscription...** (or **Add Calendar** $\rightarrow$ **Add Subscription Calendar** on iOS).
  2. Enter your feed URL and set the auto-refresh frequency (e.g., Every Hour).

- **Google Calendar (Web)**:
  1. In the left sidebar, click **`+`** next to **Other calendars**.
  2. Select **From URL**.
  3. Paste your public HTTPS feed URL and click **Add calendar**.

- **Proton Calendar (Web)**:
  1. Click **`+`** next to **My calendars** $\rightarrow$ **Add calendar from URL**.
  2. Paste your feed URL, assign a calendar title, and click **Add calendar**.

- **Outlook (Web)**:
  1. Click **Add calendar** in the left navigation panel.
  2. Select **Subscribe from web**, paste your feed URL, enter a name, and click **Import**.

---

## Security & Compliance

- **Non-Root Execution**: Runs under a dedicated system user (`UID 10001`, `appuser`) inside the container layer.
- **SonarCloud Rule docker:S8544 Compliance**: Package management layers explicitly enforce clean caching (`--no-cache-dir`) and pinned requirement specifications (`--only-binary :all:`).

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
