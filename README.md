# Memos to iCal Bridge

A lightweight Flask application that exposes Memos entries as a dynamic iCalendar (`.ics`) feed.

## Motivation
Memos is used as a daily diary. This bridge allows entries to be displayed alongside regular schedule items on a personal calendar grid.

## Functionality
* Queries the Memos v1 API for recent entries.
* Formats content into iCalendar-compliant `VEVENT` objects.
* Serves a live `.ics` feed on `/memos.ics` for calendar clients to poll automatically.

## Installation & Configuration

### Prerequisites
* Docker and Docker Compose
* A running Memos instance
* A Memos Personal Access Token (PAT)

### Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/memos-to-ical-bridge.git](https://github.com/YOUR_USERNAME/memos-to-ical-bridge.git)
   cd memos-to-ical-bridge
