#!/usr/bin/env python3
"""Builds index.html from src/template.html.

Injects the world TopoJSON (src/world.topo.json, the same map as the original
essay) and a compact source catalogue for every evidence card in the content bank.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).parent
BANK = ROOT / "poland_positive_content_bank_merged.json"

geo = (ROOT / "src" / "world.topo.json").read_text(encoding="utf-8").strip()

bank = json.loads(BANK.read_text(encoding="utf-8"))
cards = {}
for c in bank["evidence_cards"]:
    cards[c["id"]] = {
        "st": c["evidence_status"],
        "p": c.get("reference_period", ""),
        "s": [[s.get("publisher", ""), s.get("url", "")] for s in c.get("sources", []) if s.get("url")],
    }
cards["ESSAY"] = {
    "st": "essay",
    "p": "September 2026",
    "s": [["Tom Wojcik: September 2026, the world today", "https://tomwojcik.com/posts/2026-09-21/september-2026-the-world-today/"]],
}

tpl = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
out = tpl.replace("/*GEO*/", geo).replace("/*CARDS*/", json.dumps(cards, ensure_ascii=False, separators=(",", ":")))
(ROOT / "index.html").write_text(out, encoding="utf-8")
print("index.html", len(out) // 1024, "KB,", len(cards), "cards")
