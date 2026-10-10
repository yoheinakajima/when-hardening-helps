"""Render static thumbnails and the hero comparison image for the front page.
Usage:
  python3 scripts/render_thumbs.py   # family thumbs -> site/assets/thumbs/<family>.png
                                     # hero compare  -> site/assets/hero-compare.png
Picks are curated in FAMILY_PICK / HERO below.
"""
import json, math, os, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pieces = json.load(open(os.path.join(ROOT, 'site', 'pieces.json')))

FAMILY_PICK = {  # family -> (replay path relative to ROOT, )
    'ltri-in-squ': 'campaigns/C02a-baselines-replication/replays/ltri-in-squ_n5_harden_B1_default.json',
    'cross-in-squ': 'campaigns/C01-concave-pilot/replays/cross-in-squ_n5_harden_B1_default.json',
    'star5-in-squ': 'campaigns/C02a-baselines-replication/replays/star5-in-squ_n9_harden_B1_default.json',
    'squ-in-squ': 'campaigns/C02a-baselines-replication/replays/squ-in-squ_n11_harden_B1_default.json',
    'tri-in-squ': 'campaigns/C04-convex-rare/replays/tri-in-squ_n11_harden_B1_default.json',
    'pen-in-squ': 'campaigns/C04-convex-rare/replays/pen-in-squ_n11_harden_B1_default.json',
    'hex-in-squ': 'campaigns/C04-convex-rare/replays/hex-in-squ_n11_rigid_B1_default.json',
    'pen-in-pen': 'campaigns/C06-pen-in-pen/replays/pen-in-pen_n8_harden_B1_default.json',
}
HERO = ('campaigns/C02a-baselines-replication/replays/ltri-in-squ_n5_harden_B1_default.json',
        'campaigns/C02a-baselines-replication/replays/ltri-in-squ_n5_rigid_B1_default.json')

COLORS = {'harden': (232, 145, 45), 'rigid': (45, 111, 232)}


def draw_packing(d, rep, frame, color, x0, y0, size):
    P = pieces[rep['piece']]
    n = rep['n']
    L = frame['L']
    sc = size / L
    cx, cy = x0 + size / 2, y0 + size / 2
    d.rectangle([cx - L * sc / 2, cy - L * sc / 2, cx + L * sc / 2, cy + L * sc / 2],
                outline=(180, 180, 180), width=2)
    g, u = frame['g'], frame['u']
    core_s = g * (1 - u)
    lw = max(1, int(2 * g * u * P['rho'] * sc))
    p = frame['p']
    for i in range(n):
        x, y, t = p[3 * i], p[3 * i + 1], p[3 * i + 2]
        c, s = math.cos(t), math.sin(t)
        for part in P['parts']:
            pts = []
            for m in range(len(part) // 2):
                vx, vy = part[2 * m] * core_s, part[2 * m + 1] * core_s
                wx = x + vx * c - vy * s
                wy = y + vx * s + vy * c
                pts.append((cx + wx * sc, cy - wy * sc))
            if len(pts) > 2:
                d.polygon(pts, outline=color, width=lw)


def final_frame(rep):
    return rep['frames'][-1]


def make_thumbs():
    outdir = os.path.join(ROOT, 'site', 'assets', 'thumbs')
    os.makedirs(outdir, exist_ok=True)
    for fam, rel in FAMILY_PICK.items():
        fp = os.path.join(ROOT, rel)
        if not os.path.exists(fp):
            print('missing', rel); continue
        rep = json.load(open(fp))
        img = Image.new('RGB', (480, 480), 'white')
        d = ImageDraw.Draw(img)
        draw_packing(d, rep, final_frame(rep), COLORS['harden'], 0, 0, 480)
        d.text((12, 12), 'L=%.4f' % final_frame(rep)['L'], fill=(60, 60, 60))
        out = os.path.join(outdir, fam + '.png')
        img.save(out)
        print('wrote', out)


def make_hero():
    rep_h = json.load(open(os.path.join(ROOT, HERO[0])))
    rep_r = json.load(open(os.path.join(ROOT, HERO[1])))
    W = 1200
    img = Image.new('RGB', (W, W // 2 + 70), 'white')
    d = ImageDraw.Draw(img)
    size = W // 2 - 20
    for k, (rep, method, label) in enumerate([
            (rep_h, 'harden', 'hardening: L=%.4f' % final_frame(rep_h)['L']),
            (rep_r, 'rigid', 'rigid start: L=%.4f' % final_frame(rep_r)['L'])]):
        draw_packing(d, rep, final_frame(rep), COLORS[method], k * (W // 2) + 10, 10, size)
        d.text((k * (W // 2) + 12, size + 22), label, fill=(60, 60, 60))
    d.text((12, W // 2 + 44), 'L-trominoes, n=5 — the pinwheel hardening finds and rigid starts miss',
           fill=(90, 90, 90))
    out = os.path.join(ROOT, 'site', 'assets', 'hero-compare.png')
    img.save(out)
    print('wrote', out)


if __name__ == '__main__':
    make_thumbs()
    make_hero()
