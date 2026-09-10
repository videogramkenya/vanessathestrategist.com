# Vanessa The Strategist, website

One self-contained HTML file. Five pages at clean addresses: `/`, `/build-and-transfer`,
`/acquire-and-close`, `/strategy-day` and `/about`. Fonts and photographs are embedded,
so the file works offline and can be hosted anywhere that serves a file.

- `index.html`: the site. This is the one to publish.
- `vercel.json`: serves the page at each clean address, and permanently redirects the
  old WordPress pages to their nearest new page.
- `favicon.ico`, `favicon-32x32.png`, `apple-touch-icon.png`, `icon-192.png`: the icons.
- `reference/original-handover-2026-09-03.html`: exactly what Alex handed over on
  3 Sep 2026, untouched, so any change can be diffed against it.

Preview it with the `vanessa-site` entry in `.claude/launch.json`, which serves this
folder on port 8791. That is a plain file server, so it does not know the clean
addresses: open `/` and use the menu, or open an old style `/#/build-and-transfer`
link, which the page converts. Opening the file directly with `file://` is not a fair
test.

## Mobile pass, 3 September 2026

Design, layout, colours, type and copy are unchanged. Desktop was measured before and
after at 1280px: **zero geometry differences and the same page height, 7304px.**

**The one thing that actually mattered.** The file was exported as a fragment with no
`<head>`, so it carried no viewport instruction. Phones therefore assumed a 980px wide
screen and shrank the whole page to fit, which is why it looked tiny. It also meant not
one of the breakpoints already written into the CSS was ever reached. The file now has
a proper document shell with `<meta name="viewport">`, plus `charset`, `lang`,
`description` and `theme-color`.

**Weight.** Eight embedded font files (Archivo, IBM Plex Sans, IBM Plex Mono) were
declared and never used by any rule. Removed: 1.27 MB to 1.09 MB.

**Touch targets**, all done without moving anything on screen:

| control | before | after |
|---|---|---|
| Menu button, the only navigation on a phone | 35px | 45px |
| Card links, "Build & Transfer" | 24px | 45px |
| Breadcrumb "Home" | 14px | 44px |

**Small mobile fixes.** Stopped iOS enlarging body text in landscape, replaced the
browser's grey tap flash with Vanessa's pink, and stopped a long unbroken word being
able to drag the page sideways.

## Checked and deliberately left alone

- The mobile menu is fully opaque. A screenshot suggested otherwise; sweeping the
  panel with `elementFromPoint` found zero holes, so nothing was changed.
- The comparison tables already sit in their own horizontal scroll box, so they do
  not push the page sideways. Verified at 320px on all five pages.
- No `100vh` anywhere, so none of the usual iOS viewport bugs apply.
- The hero caption sitting over the corner of the photograph is intentional design.

## Open, needs a decision rather than a fix

- **Page weight is still 1.09 MB**, and 0.77 MB of that is seven photographs embedded
  as base64 inside the file. They cannot be lazy loaded or cached while they live in
  the HTML. Pulling them out into image files would roughly halve what a phone
  downloads before the page appears, and would let the browser cache them between
  visits. That turns one file into a folder, so it is Alex's call.
- **The copy uses em dashes throughout.** Left exactly as written, since this is
  Vanessa's voice and the brief was mobile only, but flagging it against the
  no-em-dash rule.

## Logo, 3 September 2026

Vanessa's gold wordmark now sits in the header and again in the footer. The source
file `vanessa Logo Gold (1).png` is 2000x1059 with the mark floating in the middle of
a lot of empty transparency, so it was trimmed to the ink, the wordmark cut away from
the tagline, and resized to 520px wide. Saved beside this file as
`logo-vanessa-gold.png` and also embedded in the page, so the site stays one file.

**The tagline half of her lockup was deliberately left out.** At the 30px a 64px
header allows, "THE SOCIAL MEDIA STRATEGIST" renders about four pixels tall and cannot
be read, which looks like a mistake rather than a logo. The small "THE STRATEGIST"
line under the mark is the site's own text and is exactly as it was before.

The footer keeps the full name as hidden text for screen readers and search engines,
since the picture above it now carries the name visually.

### Worth raising with Vanessa

Her logo says **the social media strategist**. The site says **the strategist**, and
its whole argument is that she is a Revenue Architect who does far more than social.
The About page makes a point of it. So her logo and her positioning now disagree, and
that is her decision rather than a thing to quietly fix in code.

## Favicon, clean addresses and the real domain, 10 September 2026

**The site is live at https://www.vanessathestrategist.com.** The bare domain redirects
to www. DNS is managed in Vanessa's Namecheap account; her email still lives on the old
host's server until it is moved separately. Full record list and the order of the move
are kept outside this repo, in Alex's project notes.

**Favicon.** There was none: nothing linked and `/favicon.ico` returned 404. Cropped from
her portrait, round for browser tabs and square for phone home screens, which round their
own corners and paint any see through area black.

**Clean addresses.** Pages moved from `/#/build-and-transfer` to `/build-and-transfer`.
Old `#/` links still work, because the WhatsApp bot, her brief and Kommo messages all use
them: the page rewrites them on arrival and keeps any `#section` on the end. Menu and quiz
links change the address without reloading, and the back button works. The `#personas`
jump on the home page is unchanged.

**Old WordPress pages** redirect permanently: `/real-estate/` to `/build-and-transfer`,
`/trainings-corporate-workshops/` to `/acquire-and-close`, `/masterclasses/` to
`/strategy-day`, `/clients/` and `/testimonials/` to `/about`, `/work-with-me/` and
`/appointment-type-01/` to home.

**Why this repository is public.** On Vercel's free plan a private repository only deploys
commits made by the Vercel account's owner, so a change pushed by anyone else is blocked
with "Deployment was blocked". Collaboration is free for public repositories. Nothing
private lives here: the page itself is public, and the only personal detail is the
business WhatsApp number that the site already shows.
