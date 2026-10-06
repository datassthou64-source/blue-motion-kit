#!/usr/bin/env python3
"""fetch-logo.py — resolve a brand to a local, full-colour logo file for a HyperFrames project.

    python3 tools/fetch-logo.py <name> <ref> <out-dir>
    python3 tools/fetch-logo.py --manifest logos.txt <out-dir>

<ref> is one of:
    https://…/logo.svg      an explicit image URL (highest trust — use when you have a press kit)
    wikipedia:Gmail         a Wikipedia page title      -> full-colour Wikimedia asset
    commons:LinkedIn logo   a Wikimedia Commons search  -> full-colour SVG/PNG
    lemlist.com             a bare domain               -> the site's own app icon / og:image
    figma                   a simple-icons slug         -> brand-coloured monochrome SVG

Ladder: explicit URL -> Wikipedia -> Commons -> site scrape -> simple-icons -> Google favicon.
Within the site-scrape tier every candidate is measured and the largest real raster/vector wins,
so you get the 512px app icon rather than a 16px favicon.

This style leans on full-colour app icons. Prefer wikipedia:/commons:/domain over simple-icons,
and always eyeball the result before building with it.

A manifest file is one `name<space>ref` per line; `#` comments and blank lines are ignored.

Authoring-time only. Files land locally and provenance is appended to <out-dir>/SOURCES.md;
nothing here runs at render time.
"""
import sys, os, re, json, datetime, urllib.parse, urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")
MIN_BYTES = 900
EXTS = ("svg", "png", "jpg", "jpeg", "webp", "ico")


def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("Content-Type", "")


def ext_of(url, ctype=""):
    e = os.path.splitext(urllib.parse.urlparse(url).path)[1].lstrip(".").lower()
    if e in EXTS:
        return e
    for k, v in (("svg", "svg"), ("png", "png"), ("webp", "webp"), ("jpeg", "jpg"), ("icon", "ico")):
        if k in ctype:
            return v
    return "png"


def usable(data):
    if not data or len(data) < MIN_BYTES:
        return False
    head = data[:512].lstrip().lower()
    return not (head.startswith(b"<!doctype html") or head.startswith(b"<html"))


def try_fetch(url):
    try:
        data, ctype = get(url)
    except Exception:
        return None
    if not usable(data):
        return None
    return data, ext_of(url, ctype)


# ---------------------------------------------------------------- resolvers
def from_wikipedia(title):
    api = ("https://en.wikipedia.org/w/api.php?action=query&titles="
           + urllib.parse.quote(title) + "&prop=pageimages&pithumbsize=1024&format=json")
    try:
        page = list(json.loads(get(api)[0])["query"]["pages"].values())[0]
        return [page["thumbnail"]["source"]]
    except Exception:
        return []


def from_commons(query):
    """Commons full-text search is noisy, so only keep files whose title actually names the brand."""
    api = ("https://commons.wikimedia.org/w/api.php?action=query&generator=search"
           "&gsrnamespace=6&gsrlimit=20&gsrsearch=" + urllib.parse.quote(query)
           + "&prop=imageinfo&iiprop=url&iiurlwidth=1024&format=json")
    try:
        pages = json.loads(get(api)[0])["query"]["pages"].values()
    except Exception:
        return []
    tokens = [t for t in re.findall(r"[a-z0-9]+", query.lower()) if t not in ("logo", "icon", "svg", "png")]
    scored = []
    for p in pages:
        title = re.sub(r"^File:", "", p.get("title", "")).lower()
        if tokens and not all(t in re.sub(r"[^a-z0-9]+", "", title) for t in tokens):
            continue
        info = (p.get("imageinfo") or [{}])[0]
        u = info.get("thumburl") or info.get("url")
        if not u or ext_of(u) not in EXTS:
            continue
        score = 0
        if ".svg" in title:
            score += 3
        if "logo" in title or "icon" in title:
            score += 2
        scored.append((score, u))
    return [u for _, u in sorted(scored, key=lambda c: -c[0])]


def from_site(domain):
    """Every icon the site declares, best-first."""
    cands = []
    for base in ("https://" + domain, "https://www." + domain):
        try:
            html = get(base)[0].decode("utf-8", "ignore")
        except Exception:
            continue
        for tag in re.findall(r"<link[^>]+>", html, re.I):
            if not re.search(r'rel=["\']?[^"\'>]*icon', tag, re.I):
                continue
            href = re.search(r'href=["\']([^"\']+)', tag, re.I)
            if not href:
                continue
            url = urllib.parse.urljoin(base, href.group(1))
            size = re.search(r'sizes=["\']?(\d+)', tag, re.I)
            score = int(size.group(1)) if size else 0
            if re.search(r"apple-touch", tag, re.I):
                score += 600
            if url.lower().endswith(".svg"):
                score += 900
            if url.lower().endswith(".ico"):
                score -= 900
            cands.append((score, url))
        og = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', html, re.I)
        if og:
            cands.append((-200, urllib.parse.urljoin(base, og.group(1))))
        for guess in ("/apple-touch-icon.png", "/favicon.svg"):
            cands.append((-400, base + guess))
        if cands:
            break
    seen, out = set(), []
    for _, u in sorted(cands, key=lambda c: -c[0]):
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def resolve(ref):
    """-> ordered list of candidate URLs."""
    if ref.startswith(("http://", "https://")):
        return [ref]
    if ref.startswith("wikipedia:"):
        return from_wikipedia(ref.split(":", 1)[1])
    if ref.startswith("commons:"):
        return from_commons(ref.split(":", 1)[1])
    urls = []
    domain = re.sub(r"^https?://", "", ref).split("/")[0]
    if "." in domain:
        urls += from_site(domain)
    slug = re.sub(r"[^a-z0-9]+", "", ref.split(".")[0].lower())
    urls.append("https://cdn.simpleicons.org/" + slug)
    if "." in domain:
        urls.append("https://www.google.com/s2/favicons?domain=%s&sz=256" % domain)
    return urls


def to_png(path):
    """.ico is a last-resort format; flatten its largest frame to PNG when ImageMagick is around."""
    if not path.lower().endswith(".ico"):
        return path
    d = os.path.dirname(path) or "."
    stem = os.path.basename(path)[:-4]
    png = os.path.join(d, stem + ".png")
    for cmd in ("magick", "convert"):
        if os.system("command -v %s >/dev/null 2>&1" % cmd) != 0:
            continue
        os.system('%s "%s" -coalesce "%s" 2>/dev/null' % (cmd, path, png))
        # ImageMagick writes one file per .ico frame as stem-0.png, stem-1.png, …
        frames = sorted((f for f in os.listdir(d)
                         if re.fullmatch(re.escape(stem) + r"(-\d+)?\.png", f)),
                        key=lambda f: os.path.getsize(os.path.join(d, f)))
        if not frames:
            continue
        os.replace(os.path.join(d, frames[-1]), png)
        for f in frames[:-1]:
            if f != stem + ".png":
                os.remove(os.path.join(d, f))
        os.remove(path)
        return png
    return path


def log(out_dir, path, name, url):
    md = os.path.join(out_dir, "SOURCES.md")
    if not os.path.exists(md):
        with open(md, "w") as f:
            f.write("# Logo provenance\n\n| File | Brand | Source | Fetched |\n|---|---|---|---|\n")
    with open(md, "a") as f:
        f.write("| `%s` | %s | %s | %s |\n"
                % (os.path.basename(path), name, url, datetime.date.today().isoformat()))


def fetch(name, ref, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    for url in resolve(ref):
        got = try_fetch(url)
        if not got:
            continue
        data, ext = got
        path = os.path.join(out_dir, "%s.%s" % (slug, ext))
        with open(path, "wb") as f:
            f.write(data)
        path = to_png(path)
        log(out_dir, path, name, url)
        size = os.path.getsize(path)
        note = "  ** small — eyeball it, and prefer an explicit press-kit URL **" if size < 6000 else ""
        print("saved %s (%d bytes)  <-  %s%s" % (path, size, url, note))
        return True
    print("FAILED  %s  (ref: %s) — try an explicit image URL, wikipedia:<Title>, or commons:<query>"
          % (name, ref), file=sys.stderr)
    return False


def main(argv):
    if len(argv) >= 3 and argv[0] == "--manifest":
        manifest, out_dir = argv[1], argv[2]
        ok = True
        for line in open(manifest):
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            parts = line.split(None, 1)
            if len(parts) != 2:
                print("skipping malformed line: %r" % line, file=sys.stderr)
                ok = False
                continue
            ok &= fetch(parts[0], parts[1], out_dir)
        return 0 if ok else 1
    if len(argv) != 3:
        print(__doc__)
        return 2
    return 0 if fetch(argv[0], argv[1], argv[2]) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
