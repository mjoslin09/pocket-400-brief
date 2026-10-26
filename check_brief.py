"""Validate brief.json before it is published. Exits non-zero with a reason if anything is off.

    python3 check_brief.py            checks ./brief.json
"""
import json
import re
import sys
from datetime import date, datetime

path = sys.argv[1] if len(sys.argv) > 1 else "brief.json"
errors = []


def need(cond, msg):
    if not cond:
        errors.append(msg)


def check_src(s, where, required=True):
    if s is None:
        need(not required, f"{where}: missing src")
        return
    need(isinstance(s, dict), f"{where}: src must be an object")
    if isinstance(s, dict):
        need(isinstance(s.get("t"), str) and s["t"].strip(), f"{where}: src.t (source name) required")
        need(isinstance(s.get("u"), str) and re.match(r"^https://", s.get("u", "")), f"{where}: src.u must be an https URL")
        need(isinstance(s.get("paywall", False), bool), f"{where}: src.paywall must be true/false")


try:
    b = json.load(open(path, encoding="utf-8"))
except Exception as e:
    print(f"brief.json is not valid JSON: {e}")
    sys.exit(1)

need(re.match(r"^\d{4}-\d{2}-\d{2}$", str(b.get("date", ""))), "date must be YYYY-MM-DD (the market day the brief covers)")
try:
    d = date.fromisoformat(b["date"])
    need(d <= date.today(), "date is in the future")
except Exception:
    pass
need(isinstance(b.get("asof"), str) and b["asof"].strip(), "asof required, e.g. 'Markets as of the Fri 23 Oct close'")
need(isinstance(b.get("refreshed"), str) and b["refreshed"].strip(), "refreshed required, e.g. 'Mon 26 Oct, 6:30am CT'")

nums = b.get("numbers", [])
need(isinstance(nums, list) and 5 <= len(nums) <= 8, "numbers: 5 to 8 items")
for i, n in enumerate(nums if isinstance(nums, list) else []):
    w = f"numbers[{i}]"
    for k in ("label", "value"):
        need(isinstance(n.get(k), str) and n[k].strip(), f"{w}.{k} required")
    need(n.get("dir", "flat") in ("up", "down", "flat"), f"{w}.dir must be up, down or flat")
    if "asof" in n:
        need(re.match(r"^\d{4}-\d{2}-\d{2}$", str(n["asof"])) and str(n["asof"]) <= str(b.get("date", "")), f"{w}.asof must be YYYY-MM-DD, no later than date")
    check_src(n.get("src"), w)

drv = b.get("drivers", [])
need(isinstance(drv, list) and len(drv) == 3, "drivers: exactly 3 items")
for i, x in enumerate(drv if isinstance(drv, list) else []):
    w = f"drivers[{i}]"
    need(isinstance(x.get("title"), str) and 0 < len(x["title"]) <= 40, f"{w}.title required, 40 chars max")
    need(isinstance(x.get("text"), str) and 0 < len(x["text"]) <= 320, f"{w}.text required, 320 chars max")
    check_src(x.get("src"), w)

for i, x in enumerate(b.get("deals", [])):
    w = f"deals[{i}]"
    need(isinstance(x.get("name"), str) and x["name"].strip(), f"{w}.name required")
    need(isinstance(x.get("parties", []), list), f"{w}.parties must be a list")
    need(isinstance(x.get("banks", []), list), f"{w}.banks must be a list")
    check_src(x.get("src"), w)

sw = b.get("sowhat")
need(isinstance(sw, dict) and isinstance(sw.get("text"), str) and 0 < len(sw["text"]) <= 360, "sowhat.text required, 360 chars max")
need(isinstance(b.get("pitch"), str) and 200 <= len(b["pitch"]) <= 1100, "pitch required: a 30-second script, 200 to 1100 chars")

quiz = b.get("quiz", [])
need(isinstance(quiz, list) and len(quiz) == 3, "quiz: exactly 3 questions")
for i, q in enumerate(quiz if isinstance(quiz, list) else []):
    w = f"quiz[{i}]"
    need(isinstance(q.get("q"), str) and q["q"].strip(), f"{w}.q required")
    need(isinstance(q.get("a"), str) and q["a"].strip(), f"{w}.a required")
    if "options" in q:
        need(isinstance(q["options"], list) and len(q["options"]) == 4, f"{w}.options must have 4 choices")
        need(isinstance(q.get("correct"), int) and 0 <= q["correct"] <= 3, f"{w}.correct must be 0-3")

srcs = b.get("sources", [])
need(isinstance(srcs, list) and len(srcs) >= 3, "sources: at least 3")
for i, s in enumerate(srcs if isinstance(srcs, list) else []):
    check_src(s, f"sources[{i}]")

if errors:
    print("brief.json failed checks:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"brief.json OK: {b['date']}, {len(nums)} numbers, {len(b.get('deals', []))} deals, {len(srcs)} sources")
