#!/usr/bin/env python3
"""Validate apps/*.json and write catalog.json (the file Penates downloads).

    python3 scripts/build.py                         # write catalog.json
    python3 scripts/build.py --check                 # fail if an app file is invalid or catalog.json is out of date
    python3 scripts/build.py --validate --base REF   # pull requests: app files only, and changed apps need a new version
                                                     # (catalog.json is rebuilt automatically after merging)
"""
import json, pathlib, re, subprocess, sys
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Listing fields place an app in Penates's App Catalog (and the website's); they are not part of the preset, so
# changing them needs no new version.
LISTING = {"category", "tags", "popular"}
ALLOWED = {"id", "version", "name", "url", "notes", "internal_hosts", "user_agent", "inject_css", "icon_url"} | LISTING
CATEGORIES = ["AI", "Communication", "Design", "Developer Tools", "Email", "Media", "Productivity"]
TAG = re.compile(r"^[a-z0-9][a-z0-9 -]{0,23}$")
REQUIRED = {"id", "version", "name", "url", "notes"}
ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
VER = re.compile(r"^\d+\.\d+\.\d+$")
HOST = re.compile(r"^(\*\.)?[a-z0-9-]+(\.[a-z0-9-]+)+$")


def check(path, e):
    errs = []
    def err(msg): errs.append(f"{path.name}: {msg}")
    if not isinstance(e, dict):
        return [f"{path.name}: must be a JSON object"]
    if extra := set(e) - ALLOWED:
        err(f"unknown fields {sorted(extra)} (inject_js is never allowed)")
    if missing := REQUIRED - set(e):
        err(f"missing fields {sorted(missing)}")
    if not ID.match(str(e.get("id", ""))):
        err("id must be lowercase letters, digits and dashes")
    elif path.stem != e["id"]:
        err(f"file name must be {e['id']}.json")
    if not VER.match(str(e.get("version", ""))):
        err("version must be MAJOR.MINOR.PATCH (bump it whenever you change an app)")
    for key in ("url", "icon_url"):
        if key in e:
            u = urlparse(str(e[key]))
            if u.scheme != "https" or not u.hostname:
                err(f"{key} must be an https:// URL")
    hosts = e.get("internal_hosts", [])
    if not isinstance(hosts, list) or not all(isinstance(h, str) and HOST.match(h) for h in hosts):
        err("internal_hosts must be host names like example.com or *.example.com")
    if "category" in e and e["category"] not in CATEGORIES:
        err(f"category must be one of {', '.join(CATEGORIES)}")
    tags = e.get("tags", [])
    if not isinstance(tags, list) or len(tags) > 8 or not all(isinstance(t, str) and TAG.match(t) for t in tags) \
            or len(set(tags)) != len(tags):
        err("tags must be up to 8 different lowercase words (letters, digits, spaces and dashes)")
    if "popular" in e and not isinstance(e["popular"], bool):
        err("popular must be true or false")
    for key in ("name", "notes", "user_agent", "inject_css"):
        if key in e and (not isinstance(e[key], str) or not e[key].strip()):
            err(f"{key} must be a non-empty string")
    return errs


def build():
    entries, errs, hosts = [], [], {}
    for path in sorted((ROOT / "apps").glob("*.json")):
        try:
            e = json.loads(path.read_text())
        except json.JSONDecodeError as x:
            errs.append(f"{path.name}: not valid JSON ({x})")
            continue
        errs += check(path, e)
        if isinstance(e, dict) and "url" in e:
            h = (urlparse(str(e["url"])).hostname or "").removeprefix("www.")
            if h in hosts:
                errs.append(f"{path.name}: same site as {hosts[h]} (Penates matches apps to presets by host)")
            hosts[h] = path.name
        entries.append(e)
    catalog = {"schema": 1, "catalog": entries}
    return json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", errs, len(entries)


def ver(v):
    return tuple(int(x) for x in v.split("."))


def unbumped(base):
    """Apps whose preset changed since git ref `base` (listing fields aside) but whose version did not go up."""
    errs = []
    for path in sorted((ROOT / "apps").glob("*.json")):
        old = subprocess.run(["git", "show", f"{base}:apps/{path.name}"], cwd=ROOT, capture_output=True, text=True)
        if old.returncode != 0:
            continue  # a new app
        try:
            before, now = json.loads(old.stdout), json.loads(path.read_text())
        except json.JSONDecodeError:
            continue  # reported by build()
        preset = lambda x: {k: v for k, v in x.items() if k not in LISTING} if isinstance(x, dict) else x
        if preset(before) != preset(now) and VER.match(str(now.get("version", ""))) and VER.match(str(before.get("version", ""))) \
                and ver(now["version"]) <= ver(before["version"]):
            errs.append(f"{path.name}: changed but version is still {now['version']} (bump it so installed apps get the change)")
    return errs


def main():
    text, errs, count = build()
    if "--base" in sys.argv:
        errs += unbumped(sys.argv[sys.argv.index("--base") + 1])
    if errs:
        sys.exit("\n".join(errs))
    out = ROOT / "catalog.json"
    if "--validate" in sys.argv:
        print(f"ok: {count} apps")
        return
    if "--check" in sys.argv:
        if not out.exists() or out.read_text() != text:
            sys.exit("catalog.json is out of date: run python3 scripts/build.py and commit it")
        print(f"ok: {count} apps")
        return
    out.write_text(text)
    print(f"wrote catalog.json ({count} apps)")


if __name__ == "__main__":
    main()
