import os
import random
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

RETRY_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 5

def gen_numbers():
    main = sorted(random.sample(range(1, 51), 5))
    extra = sorted(random.sample(range(1, 13), 2))
    return main, extra

def build_message(tz="Europe/Berlin"):
    try:
        now = datetime.now(ZoneInfo(tz))
    except:
        # Fallback to UTC if timezone not available
        now = datetime.now()
    date_str = now.strftime("%A, %d %B %Y")
    main, extra = gen_numbers()
    main_str = " - ".join(f"{n:02d}" for n in main)
    extra_str = " - ".join(f"{n:02d}" for n in extra)
    return (
        f"🎰 *Lotto numbers — {date_str}*\n\n"
        f"📍 Main (1–50): {main_str}\n"
        f"⭐ Extra (1–12): {extra_str}\n\n"
        "Good luck! 🍀\n_Automated Lotto Bot_"
    )

def send():
    sid = os.getenv("AC8791f70edd64db6e26ac016681d07335")
    tok = os.getenv("1780aa886302c3397d7076f8689f297a")
    dad = os.getenv("+385998167000")
    from_whatsapp = os.getenv("+14155238886")

    if not sid or not tok or not dad:
        print("❌ Missing env: TWILIO_ACCOUNT_SID / TWILIO_AUTH_TOKEN / DAD_NUMBER")
        return 2

    client = Client(sid, tok)
    body = build_message()

    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            msg = client.messages.create(
                from_=from_whatsapp,
                to=f"whatsapp:{dad}",
                body=body
            )
            print(f"✅ Sent (SID: {msg.sid})")
            return 0
        except TwilioRestException as e:
            print(f"❌ Twilio error (attempt {attempt}): {e}")
            if attempt < RETRY_ATTEMPTS:
                time.sleep(RETRY_DELAY_SECONDS)
        except Exception as e:
            print(f"❌ Unexpected error (attempt {attempt}): {e}")
            if attempt < RETRY_ATTEMPTS:
                time.sleep(RETRY_DELAY_SECONDS)
    return 1

if __name__ == "__main__":
    rc = send()
    raise SystemExit(rc)
