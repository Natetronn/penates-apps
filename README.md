# Penates apps

The shared catalog of app presets for [Penates](https://github.com/Natetronn/penates), which turns
websites into desktop apps. A preset holds the small fixes a site needs to work well as an app, such as
which sign-in pages should stay inside the window.

Penates downloads [`catalog.json`](catalog.json) when you create or update an app, and applies the preset
whose site matches. From Penates 0.1.3, its **Catalog** tab lists these apps by category, with the popular ones
first. Changes here reach every Penates install without a
new Penates release.

## Apps

| App | Category | Site | What the preset does |
|---|---|---|---|
| ChatGPT ★ | AI | chatgpt.com | Keep OpenAI, Google, Microsoft or Apple sign-in inside the window. Voice needs "Allow camera and microphone" in the app's settings. |
| Claude ★ | AI | claude.ai | Keep Google sign-in inside the window. |
| Cloudflare | Developer Tools | dash.cloudflare.com | Keep the Zero Trust dashboard and Google, Apple or GitHub sign-in inside the window; docs open in your browser. |
| Discord ★ | Communication | discord.com/app | Invite links open in the app. Voice and video need "Allow camera and microphone" in the app's settings. |
| Figma | Design | figma.com/files | Keep Google sign-in inside the window. |
| GitHub ★ | Developer Tools | github.com | Keep gists and other github.com pages in the window. |
| Gmail ★ | Email | mail.google.com | Keep Google sign-in inside the window; Calendar, Drive and other Google apps open in your browser. |
| Google Calendar | Productivity | calendar.google.com | Keep Google sign-in inside the window; Meet links open in your browser. |
| Google Drive | Productivity | drive.google.com | Keep Google sign-in and Docs, Sheets and Slides inside the window. |
| Linear | Productivity | linear.app | Keep Google sign-in inside the window. |
| Notion ★ | Productivity | notion.so | Keep Notion pages and Google or Apple sign-in inside the window. |
| Outlook | Email | outlook.live.com/mail | Keep Microsoft sign-in inside the window, for personal and work or school accounts. |
| Proton Mail | Email | mail.proton.me | Keep Proton sign-in, Calendar and Drive inside the window. |
| Slack ★ | Communication | app.slack.com/client | Keep your workspaces and Google or Apple sign-in inside the window. Huddles need "Allow camera and microphone" in the app's settings. |
| Spotify | Media | open.spotify.com | Keep Spotify sign-in inside the window. On Linux, music playback needs Widevine DRM, which WebKitGTK does not support. |
| Tailscale | Developer Tools | login.tailscale.com/admin | Keep Google, Microsoft, GitHub or Apple sign-in inside the window; docs open in your browser. |
| Telegram | Communication | web.telegram.org/a | Sign in with the code Telegram sends you, or by scanning the QR code with your phone. |
| Todoist | Productivity | app.todoist.com | Keep Google or Apple sign-in inside the window. |
| Trello | Productivity | trello.com | Keep Atlassian, Google, Microsoft or Apple sign-in inside the window. |
| WhatsApp | Communication | web.whatsapp.com | Sign in by scanning the QR code with your phone. |
| YouTube ★ | Media | youtube.com | Keep Google sign-in inside the window. |
| YouTube Music | Media | music.youtube.com | Keep Google sign-in inside the window. |

★ Shown under **Popular** in the App Catalog.

## Add or fix an app

**From Penates:** an app's ⋮ menu → **Share with the app catalog…** shows the entry for review and opens
GitHub with it filled in: a new file for a new site (choose **Propose changes**), or an issue suggesting a change
for a site that is already here. `penates submit <id> --notes "…"` does the same from the command line.

**By hand:**
1. Add or edit `apps/<id>.json` (the file name is the id).
2. Bump `version` whenever you change an app; Penates only applies a preset that is newer than the one an
   app already has.
3. Open a pull request with the app file. CI checks it (and that a changed app has a new version);
   `catalog.json` is rebuilt automatically once it is merged. `python3 scripts/build.py` checks and rebuilds
   it locally if you want to look.

```json
{
  "id": "github",
  "version": "1.1.0",
  "name": "GitHub",
  "url": "https://github.com/",
  "internal_hosts": ["*.github.com"],
  "notes": "Keep gists and other github.com pages in the window",
  "category": "Developer Tools",
  "tags": ["code", "git", "pull requests"],
  "popular": true
}
```

| Field | |
|---|---|
| `id` | lowercase letters, digits and dashes |
| `version` | `MAJOR.MINOR.PATCH` |
| `name` | display name |
| `url` | the address the app opens; Penates matches presets to apps by this site's host |
| `notes` | one line saying what the preset does, shown in Penates's Updates tab |
| `internal_hosts` | optional: other sites that stay in the app window when a link or popup goes there, e.g. a sign-in page (`*.example.com` matches it and its subdomains). Images and scripts load from anywhere regardless |
| `user_agent` | optional: only when a site refuses Penates's own; say why in `notes` |
| `inject_css` | optional: small style fixes |
| `icon_url` | optional: an https:// icon when the site's own is poor |
| `category` | optional, for the App Catalog: one of AI, Communication, Design, Developer Tools, Email, Media, Productivity |
| `tags` | optional, for the App Catalog's search: up to 8 lowercase words, e.g. `["chat", "work"]` |
| `popular` | optional, for the App Catalog: `true` puts the app under Popular (chosen here, not counted: Penates has no telemetry) |

`category`, `tags` and `popular` only place an app in the App Catalog; they are not part of the preset, so
changing them needs no new `version`.

Custom JavaScript is never accepted: Penates ignores it in presets, and the check rejects it.

## License

MIT
