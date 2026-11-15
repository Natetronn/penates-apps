# Penates apps

The shared catalog of app presets for [Penates](https://github.com/Natetronn/penates), which turns
websites into desktop apps. A preset holds the small fixes a site needs to work well as an app, such as
which sign-in pages should stay inside the window.

Penates downloads [`catalog.json`](catalog.json) when you create or update an app, and applies the preset
whose site matches. Changes here reach every Penates install without a new Penates release.

## Apps

| App | Site | What the preset does |
|---|---|---|
| Cloudflare | dash.cloudflare.com | Keeps the Zero Trust dashboard and Google, Apple or GitHub sign-in inside the window; docs open in your browser. |
| Discord | discord.com/app | Invite links open in the app. Voice and video need "Allow camera and microphone" in the app's settings. |
| GitHub | github.com | Keeps gists and other github.com pages in the window. |
| Notion | notion.so | Keeps Notion pages and Google or Apple sign-in inside the window. |
| Proton Mail | mail.proton.me | Keeps Proton sign-in, Calendar and Drive inside the window. |
| Spotify | open.spotify.com | Keeps Spotify sign-in inside the window. On Linux, music playback needs Widevine DRM, which WebKitGTK does not support. |
| Tailscale | login.tailscale.com/admin | Keeps Google, Microsoft, GitHub or Apple sign-in inside the window; docs open in your browser. |
| WhatsApp | web.whatsapp.com | Sign in by scanning the QR code with your phone. |
| YouTube | youtube.com | Keeps Google sign-in inside the window. |
| YouTube Music | music.youtube.com | Keeps Google sign-in inside the window. |

## Add or fix an app

1. Add or edit `apps/<id>.json` (the file name is the id).
2. Bump `version` whenever you change an app; Penates only applies a preset that is newer than the one an
   app already has.
3. Run `python3 scripts/build.py` to check your change and regenerate `catalog.json`, then open a pull request
   with both files. CI also checks that every changed app has a new version.

```json
{
  "id": "github",
  "version": "1.1.0",
  "name": "GitHub",
  "url": "https://github.com/",
  "internal_hosts": ["*.github.com"],
  "notes": "Keep gists and other github.com pages in the window"
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

Custom JavaScript is never accepted: Penates ignores it in presets, and the check rejects it.

## License

MIT
