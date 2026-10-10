"""Render a preview image: mid-morph and final frames of the best harden replay of a cell.
Usage: python3 scripts/render_preview.py <replay.json> <out.png>"""
import json, math, sys
from PIL import Image, ImageDraw

rep_path, out_path = sys.argv[1], sys.argv[2]
rep = json.load(open(rep_path))
pieces = json.load(open('site/pieces.json'))
P = pieces[rep['piece']]
n = rep['n']

W = 1400
frames = rep['frames']
# pick a mid-morph frame (u closest to 0.5) and the final legal frame
mid = min([f for f in frames if f['ph'] == 'morph'], key=lambda f: abs(f['u'] - 0.5))
final = frames[-1]
picks = [('soft: tau=%.2f' % mid['u'], mid, (232, 145, 45)), ('hard: tau=0', final, (45, 111, 232))]

img = Image.new('RGB', (W, W // 2 + 60), 'white')
d = ImageDraw.Draw(img)

def draw_frame(f, color, x0, size):
    L = f['L']
    sc = size / L
    cx, cy = x0 + size / 2, size / 2 + 20
    # container
    d.rectangle([cx - L * sc / 2, cy - L * sc / 2, cx + L * sc / 2, cy + L * sc / 2], outline=(180, 180, 180), width=2)
    g, u = f['g'], f['u']
    core_s = g * (1 - u)
    lw = max(1, int(2 * g * u * P['rho'] * sc))
    p = f['p']
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
    d.text((x0 + 10, 10), 'L=%.4f' % f['L'], fill=(60, 60, 60))

size = W // 2 - 20
for k, (label, f, color) in enumerate(picks):
    d.text((k * (W // 2) + 10, size + 30), label, fill=(60, 60, 60))
    draw_frame(f, color, k * (W // 2) + 10, size)
d.text((10, W // 2 + 30), '%s n=%d harden (%s)' % (rep['piece'], n, rep['id']), fill=(60, 60, 60))
img.save(out_path)
print('wrote', out_path)
