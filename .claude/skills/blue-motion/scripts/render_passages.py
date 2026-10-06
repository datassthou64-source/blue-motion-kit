#!/usr/bin/env python3
"""Default export for Blue Motion graphics: render each motion-graphics passage as its own
MP4 and write a Premiere XML that places every file at its real position on the VO timeline.

Why this and not one full-timeline render: a Blue Motion body project is mostly empty timeline
between passages (a past build: 148s of graphics inside 482s). The full render still captures every
empty frame, and ran about 1 hour. Per-passage renders took about 20s each.

What it does, for PROJECT_DIR/index.html:
  1. Passages = one per blue-gradient clip. If there is a single gradient clip, the passages
     are instead the runs of back-to-back composition clips.
  2. For each passage it writes _render-NN.html. This holds every parent clip overlapping the
     window (gradient, shade, footage, VO slice, scene compositions), shifted to start at 0.
     The parent's main timeline is scrubbed from start to end with tweenFromTo placed at 0, so
     parent-level footage tweens still land. A child added at a negative start does NOT render.
  3. HDR guard: any HLG footage is converted to SDR BT.709 in place, with the original kept
     in <dir>/_hdr-originals/. One HDR source makes the whole render HDR (purple cast, slow).
  4. Renders renders/MGNN-<label>.mp4 at high quality, 30 fps.
  5. Verifies each file: 1920x1080, 30/1, expected frame count, audio present, SDR BT.709.
  6. Writes premiere-cuts.xml (xmeml v4, 30 fps NDF, one clip per passage, VO-length sequence).

Usage:
  render_passages.py PROJECT_DIR               render all passages, then write the XML
  render_passages.py PROJECT_DIR --only 3,8    re-render some passages, then rewrite the XML
  render_passages.py PROJECT_DIR --dry-run     list the passages and exit
  render_passages.py PROJECT_DIR --xml-only    rewrite the XML from existing renders
  --keep keeps the _render-NN.html entry files (deleted by default).
"""
import argparse, glob, json, os, re, shutil, subprocess, sys, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hlg_to_sdr  # noqa: E402

FPS = 30
HDR_TRC = {"arib-std-b67", "smpte2084"}
TAG = re.compile(r'<(video|audio|div)\b([^>]*\bdata-start="[^"]*"[^>]*)>\s*</\1>')


def attr(a, name):
    m = re.search(r'\b' + name + r'="([^"]*)"', a)
    return m.group(1) if m else None


def set_attr(a, name, value):
    if attr(a, name) is None:
        return a + f' {name}="{value}"'
    return re.sub(r'\b' + name + r'="[^"]*"', f'{name}="{value}"', a, count=1)


def parse(project):
    html = open(os.path.join(project, "index.html")).read()
    head, body = html.split("<body>", 1)
    root = re.search(r'<div\b[^>]*data-composition-id="main"[^>]*>', body).group(0)
    clips = []
    for m in TAG.finditer(body):
        tag, a = m.group(1), m.group(2)
        if 'data-composition-id="main"' in a:
            continue
        st, du = attr(a, "data-start"), attr(a, "data-duration")
        if st is None or du is None:
            continue
        clips.append(dict(tag=tag, a=a, st=float(st), du=float(du), en=float(st) + float(du),
                          comp=attr(a, "data-composition-src") is not None,
                          bg=tag == "video" and "blue-gradient-loop" in (attr(a, "src") or ""),
                          id=attr(a, "id") or ""))
    scripts = re.findall(r'<script>(.*?)</script>', body, re.S)
    return head, root, clips, scripts


def passages(clips):
    bgs = sorted((c for c in clips if c["bg"]), key=lambda c: c["st"])
    comps = sorted((c for c in clips if c["comp"]), key=lambda c: c["st"])
    if len(bgs) > 1:
        return [(b["st"], b["en"], b["id"].replace("-bg", "")) for b in bgs]
    runs = []
    for c in comps:
        if runs and c["st"] - runs[-1][1] < 0.05:
            runs[-1][1] = max(runs[-1][1], c["en"])
        else:
            runs.append([c["st"], c["en"], attr(c["a"], "data-composition-id")])
    return [tuple(r) for r in runs]


def entry(head, root, clips, scripts, a, b):
    D = round(b - a, 3)
    lines = []
    for c in clips:
        if c["en"] <= a + 1e-3 or c["st"] >= b - 1e-3:
            continue
        s, e = max(c["st"], a), min(c["en"], b)
        at = c["a"]
        if c["comp"] and c["st"] < a - 0.02:
            print(f"  ! {c['id']} starts before the passage; its scene time will be offset", file=sys.stderr)
        at = set_attr(at, "data-start", f"{s - a:.3f}")
        at = set_attr(at, "data-duration", f"{e - s:.3f}")
        if c["tag"] in ("video", "audio"):
            ms = float(attr(at, "data-media-start") or 0) + (s - c["st"])
            at = set_attr(at, "data-media-start", f"{ms:.3f}")
        lines.append(f'      <{c["tag"]}{at}></{c["tag"]}>')
    r = set_attr(set_attr(root, "data-start", "0"), "data-duration", f"{D}")
    parent = "\n".join(f"<script>{s}</script>" for s in scripts)
    wrap = ("<script>(function(){const P=window.__timelines&&window.__timelines.main;"
            "const tl=gsap.timeline({paused:true});"
            f"if(P){{P.pause();tl.add(P.tweenFromTo({a},{a + D:.3f},{{ease:'none'}}),0);}}tl.set({{}},{{}},{D});"
            "window.__timelines.main=tl;})();</script>")
    return f"{head}<body>\n    {r}\n" + "\n".join(lines) + f"\n    </div>\n    {parent}\n    {wrap}\n  </body>\n</html>\n"


def hdr_guard(project, html):
    for src in sorted(set(re.findall(r'<video\b[^>]*\bsrc="([^"]+)"', html))):
        p = os.path.join(project, src)
        if "blue-gradient-loop" in src or not os.path.exists(p):
            continue
        trc = hlg_to_sdr.transfer(p)
        if trc == "smpte2084":
            sys.exit(f"PQ HDR footage is not handled by hlg_to_sdr: {src}. Convert it to SDR first.")
        if trc in HDR_TRC:
            keep = os.path.join(os.path.dirname(p), "_hdr-originals", os.path.basename(p))
            os.makedirs(os.path.dirname(keep), exist_ok=True)
            if not os.path.exists(keep):
                shutil.copy2(p, keep)
            print(f"  HDR ({trc}) -> SDR BT.709: {src}  (original kept in _hdr-originals/)")
            hlg_to_sdr.convert(keep, p)


def probe(path):
    j = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-count_packets", "-show_entries",
        "stream=codec_type,width,height,r_frame_rate,nb_read_packets,color_transfer:format=duration",
        "-of", "json", path]))
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    return dict(w=v["width"], h=v["height"], fps=v["r_frame_rate"], frames=int(v["nb_read_packets"]),
                trc=v.get("color_transfer", "unknown"),
                audio=any(s["codec_type"] == "audio" for s in j["streams"]))


def hf_cmd(project):
    try:
        m = re.search(r'hyperframes@[\w.\-]+', json.load(open(os.path.join(project, "package.json")))["scripts"]["render"])
        return ["npx", "--yes", m.group(0)]
    except Exception:
        return ["npx", "--yes", "hyperframes"]


def write_xml(project, plist, vo_dur):
    rate = f"<rate><timebase>{FPS}</timebase><ntsc>FALSE</ntsc></rate>"
    sc = f"<samplecharacteristics>{rate}<width>1920</width><height>1080</height></samplecharacteristics>"
    items = []
    for n, (a, b, label) in enumerate(plist, 1):
        found = glob.glob(os.path.join(project, "renders", f"MG{n:02d}-*.mp4"))
        if not found:
            sys.exit(f"missing render for passage {n}")
        path = os.path.abspath(found[0]); fr = probe(path)["frames"]
        s = round(a * FPS)
        items.append(f'<clipitem id="mg-{n}"><name>{n:03d} MG {n:02d}</name><enabled>TRUE</enabled><duration>{fr}</duration>{rate}'
                     f'<start>{s}</start><end>{s + fr}</end><in>0</in><out>{fr}</out>'
                     f'<file id="file-{n}"><name>{os.path.basename(path)}</name><pathurl>file://localhost{urllib.parse.quote(path)}</pathurl>{rate}'
                     f'<duration>{fr}</duration><media><video>{sc}</video><audio><samplecharacteristics><depth>16</depth>'
                     f'<samplerate>48000</samplerate></samplecharacteristics><channelcount>2</channelcount></audio></media></file>'
                     f'<compositemode>normal</compositemode></clipitem>')
    total = round(vo_dur * FPS)
    name = os.path.basename(os.path.abspath(project))
    xml = (f'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n<xmeml version="4"><sequence id="seq-mg">'
           f'<name>{name} - Motion Graphics (cut)</name><duration>{total}</duration>{rate}'
           f'<timecode>{rate}<string>00:00:00:00</string><frame>0</frame><displayformat>NDF</displayformat></timecode>'
           f'<media><video><format><samplecharacteristics>{rate}<width>1920</width><height>1080</height>'
           f'<pixelaspectratio>square</pixelaspectratio></samplecharacteristics></format>'
           f'<track>{"".join(items)}<enabled>TRUE</enabled><locked>FALSE</locked></track></video>'
           f'<audio><numOutputChannels>2</numOutputChannels></audio></media></sequence></xmeml>\n')
    out = os.path.join(project, "premiere-cuts.xml")
    open(out, "w").write(xml)
    print(f"wrote {out}  ({len(items)} clips, sequence {total} frames = VO length)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--only", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--xml-only", action="store_true")
    ap.add_argument("--keep", action="store_true")
    o = ap.parse_args()
    P = o.project
    head, root, clips, scripts = parse(P)
    plist = passages(clips)
    audio = [c for c in clips if c["tag"] == "audio"]
    vo_dur = max((c["en"] for c in audio), default=max(c["en"] for c in clips))
    for n, (a, b, label) in enumerate(plist, 1):
        print(f"MG{n:02d}  {label:<14} {a:8.2f}-{b:8.2f}s  ({b - a:5.2f}s, frames {round(a*FPS)}-{round(b*FPS)})")
    if o.dry_run:
        return
    only = {int(x) for x in o.only.split(",") if x.strip()}
    if not o.xml_only:
        hdr_guard(P, open(os.path.join(P, "index.html")).read())
        os.makedirs(os.path.join(P, "renders"), exist_ok=True)
        cmd, bad = hf_cmd(P), []
        for n, (a, b, label) in enumerate(plist, 1):
            if only and n not in only:
                continue
            ent = f"_render-{n:02d}.html"
            open(os.path.join(P, ent), "w").write(entry(head, root, clips, scripts, a, b))
            for old in glob.glob(os.path.join(P, "renders", f"MG{n:02d}-*.mp4")):
                os.remove(old)
            out = f"renders/MG{n:02d}-{label}.mp4"
            r = subprocess.run(cmd + ["render", ".", "-c", ent, "-o", out, "-q", "high", "-f", str(FPS)],
                               cwd=P, capture_output=True, text=True)
            done = re.search(r'rendered in ([^\n]+)', r.stdout + r.stderr)
            if not o.keep:
                os.remove(os.path.join(P, ent))
            if r.returncode or not os.path.exists(os.path.join(P, out)):
                print((r.stdout + r.stderr)[-2000:]); sys.exit(f"render failed: {out}")
            p = probe(os.path.join(P, out)); want = round((b - a) * FPS)
            ok = (p["w"], p["h"], p["fps"]) == (1920, 1080, "30/1") and abs(p["frames"] - want) <= 1 \
                and p["audio"] and p["trc"] not in HDR_TRC
            print(f"{'OK ' if ok else 'BAD'} {out}  {p['frames']}f/{want}f  {p['w']}x{p['h']} {p['fps']} "
                  f"audio={p['audio']} trc={p['trc']}  ({done.group(1).strip() if done else '?'})")
            if not ok:
                bad.append(out)
        if bad:
            sys.exit("verification failed: " + ", ".join(bad))
    write_xml(P, plist, vo_dur)


if __name__ == "__main__":
    main()
