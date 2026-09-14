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
