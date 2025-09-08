# Lototata — WhatsApp Lotto Bot

Sends lotto numbers to WhatsApp automatically every Tuesday and Friday using GitHub Actions and Twilio Sandbox.

## What it does
- 5 main numbers (1–50) + 2 extra (1–12), sorted ascending
- Friendly message with date (Europe/Berlin)
- Automatic schedule: Tue & Fri at 08:00 UTC
- Retries on failure, exits with non‑zero code if sending fails

## Files
- `lototata.py` — main bot script
- `requirements.txt` — Python dependencies
- `.github/workflows/lotto.yml` — GitHub Actions schedule and run

## Prerequisites
1. Twilio account and WhatsApp Sandbox enabled
2. Your dad has joined the Twilio WhatsApp Sandbox (QR or join code)
3. Your Twilio Account SID and Auth Token

## Setup (step by step)
1) Add repository secrets (Settings → Secrets and variables → Actions):
- `TWILIO_ACCOUNT_SID` — from Twilio console (starts with AC...)
- `TWILIO_AUTH_TOKEN` — from Twilio console
- `DAD_NUMBER` — your dad's number in E.164, e.g. `+3859XXXXXXXX`
- Optional: `TWILIO_WHATSAPP_FROM` — if your sandbox sender differs (e.g. `whatsapp:+14155238886`)

2) Verify Sandbox join
- In Twilio Console → Messaging → Try it out → WhatsApp Sandbox
- Ensure your dad's number is listed as a participant (or have him re‑join with the code)

## Test now (manual run)
- Go to the Actions tab → "Send Lotto Numbers" → Run workflow
- Open the latest run → check logs under "Run bot"
- If successful, your dad receives a WhatsApp message

## Automatic schedule (timezones)
- Cron: `0 8 * * 2,5` → runs Tue/Fri at 08:00 UTC
- Berlin local time: 10:00 in summer (CEST), 09:00 in winter (CET)
- Change time by editing `.github/workflows/lotto.yml`

## Troubleshooting
- Not a sandbox participant: Have your dad re‑join the sandbox (QR/join code)
- Auth errors: Re‑copy `TWILIO_ACCOUNT_SID`/`TWILIO_AUTH_TOKEN` without spaces
- Wrong number format: `DAD_NUMBER` must be `+<country><number>` (no spaces)
- Dependencies error: Ensure `requirements.txt` is present
- Workflow not running: File must be `.github/workflows/lotto.yml`; repository Actions enabled

## Notes
- Twilio Sandbox participation may expire after inactivity; re‑join if messages stop arriving
- For permanent messaging without re‑join, use WhatsApp Business API (paid, outside scope here)
