#!/usr/bin/env python3
"""Builds index.html from src/template.html.

Injects the world map (src/world.topo.json) and the source list for every
figure (src/sources.json) into the template.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).parent
geo = (ROOT / "src" / "world.topo.json").read_text(encoding="utf-8").strip()
cards = json.loads((ROOT / "src" / "sources.json").read_text(encoding="utf-8"))

tpl = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
out = tpl.replace("/*GEO*/", geo).replace("/*CARDS*/", json.dumps(cards, ensure_ascii=False, separators=(",", ":")))
(ROOT / "index.html").write_text(out, encoding="utf-8")
print("index.html", len(out) // 1024, "KB,", len(cards), "source entries")
