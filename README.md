# Penates apps

The shared catalog of app presets for [Penates](https://github.com/Natetronn/penates), which turns
websites into desktop apps. A preset holds the small fixes a site needs to work well as an app, such as
which sign-in pages should stay inside the window.

Penates downloads [`catalog.json`](catalog.json) when you create or update an app, and applies the preset
whose site matches. Changes here reach every Penates install without a new Penates release.

## Apps

| App | Site | What the preset does |
|---|---|---|
| Discord | discord.com/app | Invite links open in the app. Voice and video need "Allow camera and microphone" in the app's settings. |
| GitHub | github.com | Keeps avatars and assets in-app. |
| Notion | notion.so | Keeps Notion pages and Google or Apple sign-in inside the window. |
| Proton Mail | mail.proton.me | Keeps Proton sign-in, Calendar and Drive inside the window. |
| Spotify | open.spotify.com | Keeps Spotify sign-in inside the window. On Linux, music playback needs Widevine DRM, which WebKitGTK does not support. |
| WhatsApp | web.whatsapp.com | Sign in by scanning the QR code with your phone. |
| YouTube | youtube.com | Keeps Google sign-in inside the window. |
| YouTube Music | music.youtube.com | Keeps Google sign-in inside the window. |

## Add or fix an app

1. Add or edit `apps/<id>.json` (the file name is the id).
2. Bump `version` whenever you change an app; Penates only applies a preset that is newer than the one an
   app already has.
3. Run `python3 scripts/build.py` to check your change and regenerate `catalog.json`, then open a pull request
   with both files.

```json
{
  "id": "github",
  "version": "1.0.0",
  "name": "GitHub",
  "url": "https://github.com/",
  "internal_hosts": ["*.githubusercontent.com", "githubassets.com"],
  "notes": "Keep avatars and assets in-app"
}
```

| Field | |
|---|---|
| `id` | lowercase letters, digits and dashes |
| `version` | `MAJOR.MINOR.PATCH` |
| `name` | display name |
| `url` | the address the app opens; Penates matches presets to apps by this site's host |
| `notes` | one line saying what the preset does, shown in Penates's Updates tab |
| `internal_hosts` | optional: other sites that stay in the app window, e.g. a sign-in page (`*.example.com` matches subdomains) |
| `user_agent` | optional: only when a site refuses Penates's own; say why in `notes` |
| `inject_css` | optional: small style fixes |
| `icon_url` | optional: an https:// icon when the site's own is poor |

Custom JavaScript is never accepted: Penates ignores it in presets, and the check rejects it.

## License

MIT
