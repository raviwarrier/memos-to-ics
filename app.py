from datetime import datetime, timezone
from flask import Flask, Response
import requests

# ================= CONFIGURATION =================
# Cloudflare public endpoint (or container internal name if preferred)
MEMOS_BASE_URL = "https://m8k9v2x7q1z4.raviwarrier.net"
MEMOS_API_TOKEN = "memos_pat_aveUGX2SHx06LReqzcp496j56hmsUA5S"
# =================================================

app = Flask(__name__)


def clean_memo_content(content: str) -> str:
    """Escapes special characters required by the iCalendar standard."""
    if not content:
        return ""
    content = content.replace("\r\n", "\\n").replace("\n", "\\n")
    content = content.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")
    return content


def extract_summary(content: str) -> str:
    """Uses the first non-empty line of the memo as the event title."""
    lines = [line.strip() for line in content.split("\n") if line.strip()]
    if not lines:
        return "Untitled Memo"
    summary = lines[0]
    return summary[:60] + "..." if len(summary) > 60 else summary


@app.route("/memos.ics", methods=["GET"])
def get_ics_feed():
    headers = {"Authorization": f"Bearer {MEMOS_API_TOKEN}"}
    target_url = f"{MEMOS_BASE_URL}/api/v1/memos?pageSize=100"

    try:
        response = requests.get(target_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return Response(
                f"Error fetching memos from API (Status {response.status_code})",
                status=500,
                mimetype="text/plain",
            )
        data = response.json()
        memos = data.get("memos", [])
    except Exception as e:
        return Response(
            f"Failed to connect to Memos URL: {str(e)}",
            status=500,
            mimetype="text/plain",
        )

    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//My Memos Journal//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Journal Memos",
    ]

    for memo in memos:
        memo_name = memo.get("name", "")
        raw_content = memo.get("content", "")
        create_time_str = memo.get("createTime")

        try:
            dt = datetime.fromisoformat(create_time_str.replace("Z", "+00:00"))
        except Exception:
            dt = datetime.now(timezone.utc)

        dt_stamp = dt.strftime("%Y%m%dT%H%M%SZ")
        uid = f"memo-{memo_name.replace('/', '-')}"
        summary = clean_memo_content(extract_summary(raw_content))
        description = clean_memo_content(raw_content)

        ics_lines.extend(
            [
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTAMP:{dt_stamp}",
                f"DTSTART:{dt_stamp}",
                f"DTEND:{dt_stamp}",
                f"SUMMARY:{summary}",
                f"DESCRIPTION:{description}",
                "END:VEVENT",
            ]
        )

    ics_lines.append("END:VCALENDAR")
    return Response("\r\n".join(ics_lines), mimetype="text/calendar")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5321)
