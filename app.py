# app.py
# This file exists to make Render's default command "gunicorn app:app" work.
from rayex_bot.webhook import app

if __name__ == "__main__":
    app.run()
