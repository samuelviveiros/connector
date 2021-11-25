#!/usr/bin/env python
import os

from dotenv import load_dotenv
from telethon import TelegramClient


load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")

client = TelegramClient("telegram", api_id, api_hash)

with client:  # Telethon will request phone and code to log in
    print("[+] `telegram.session` was generated in the project root directory.")
    print("[+] ** Now we are good to go **")
