#!/usr/bin/env python3
"""Convert an HLG / BT.2020 clip (iPhone footage) to SDR BT.709.

Why: one HDR source anywhere in a render flips HyperFrames into an HDR (BT.2020 HLG, 10-bit)
output. The whole render then shifts purple against the blue gradient, and it drops to the
slow layered-composite path, roughly 10x slower.

How: the local ffmpeg has no zscale/libplacebo, so the maths runs in numpy. HLG is
backwards-compatible with SDR, so its tone curve is kept (read as display gamma 2.4) and
only the primaries are converted from BT.2020 to BT.709. A full HLG-to-reference-white tone
map was tried on the a past build road footage and blew out the sky.

Usage: hlg_to_sdr.py SRC DST
"""
import subprocess, sys
import numpy as np

M_2020_TO_709 = np.array([[1.6605, -0.5876, -0.0728],
                          [-0.1246, 1.1329, -0.0083],
                          [-0.0182, -0.1006, 1.1187]])


def _probe(src, entries):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v",
                                   "-show_entries", f"stream={entries}", "-of", "csv=p=0", src])
    return out.decode().strip().strip(",").split(",")


def transfer(src):
    """Return the video stream's colour transfer tag (e.g. 'bt709', 'arib-std-b67')."""
    return _probe(src, "color_transfer")[0]


def convert(src, dst):
    W, H = map(int, _probe(src, "width,height")[:2])
    fps = _probe(src, "r_frame_rate")[0]
    raw = dst + ".raw.mp4"
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf",
                            "scale=in_color_matrix=bt2020:in_range=tv:out_range=full,format=rgb48le",
                            "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le",
                            "-s", f"{W}x{H}", "-r", fps, "-i", "-",
                            "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
                            "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-an", raw],
                           stdin=subprocess.PIPE)
    n, size = 0, W * H * 6
    while True:
        buf = dec.stdout.read(size)
        if len(buf) < size:
            break
        e = np.frombuffer(buf, np.uint16).reshape(H, W, 3).astype(np.float32) / 65535.0
        x = np.power(e, 2.4) @ M_2020_TO_709.T
        out = np.power(np.clip(x, 0, 1), 1 / 2.4)
        enc.stdin.write((out * 65535 + .5).astype(np.uint16).tobytes())
        n += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    # libx264 drops the -color_* tags here; write BT.709 into the bitstream itself
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", raw, "-c", "copy", "-bsf:v",
                           "h264_metadata=colour_primaries=1:transfer_characteristics=1:"
                           "matrix_coefficients=1:video_full_range_flag=0", dst])
    subprocess.call(["rm", "-f", raw])
    return n


if __name__ == "__main__":
    print(sys.argv[2], convert(sys.argv[1], sys.argv[2]), "frames")
