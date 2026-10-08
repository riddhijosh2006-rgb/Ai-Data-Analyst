"""Run: python check_models.py  -> shows which Gemini models WORK with your key right now."""
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
c = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
skip = ("tts", "live", "image", "audio", "embedding", "robotics", "omni", "translate", "deep-research")
names = [m.name.replace("models/", "") for m in c.models.list()
         if "generateContent" in (m.supported_actions or [])]
cands = [n for n in names if "flash" in n and not any(x in n for x in skip)][:15]
print("Testing:", cands, "\n")
for n in cands:
    try:
        c.models.generate_content(model=n, contents="say ok")
        print("WORKS  ", n)
    except Exception as e:
        print("FAILED ", n, "-", str(e)[:70].replace("\n", " "))
