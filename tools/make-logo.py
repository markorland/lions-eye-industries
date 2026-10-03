"""Draw the images the email signatures need.

Run from the repo root: python3 tools/make-logo.py

Writes assets/img/logo-email.png (the eye) and assets/img/spacer.png (a 1x1
transparent pixel, stretched with width and height attributes to hold gaps
open where a mail client has stripped the CSS padding).

The site's logo is an SVG, which almost no mail client renders, so the email
signatures need a PNG. Two things differ from assets/img/logo.svg: the
background is transparent rather than near-black, and the slit pupil is filled
dark rather than knocked out, so the eye reads the same on a white message and
in dark mode. No dependencies — the PNG is encoded here with zlib.
"""

import zlib, struct, math

# The logo, in the same 64-unit space as assets/img/logo.svg.
# Lens outline = intersection of two circles (half-width 26, sagitta 16.5).
A, H = 26.0, 16.5
R = (A*A + H*H) / (2*H)                 # 28.735
CY1, CY2 = 32.0 + (R - H), 32.0 - (R - H)
CX = 32.0
STROKE = 2.5
IRIS_RX, IRIS_RY = 5.5, 13.0
PUP_RX, PUP_RY = 1.6, 8.0

GOLD = (0xd2, 0xa2, 0x4c)
SLIT = (0x0e, 0x10, 0x14)   # opaque, so the eye reads on light and dark alike

# Tight crop around the artwork rather than the square favicon box.
X0, X1 = 3.5, 60.5
Y0, Y1 = 13.0, 51.0
SCALE = 4                                # 4x for retina
W = int(round((X1 - X0) * SCALE))
HGT = int(round((Y1 - Y0) * SCALE))
SS = 4                                   # supersamples per axis

def ink(x, y):
    """Colour at this point, or None for transparent."""
    iris = ((x - CX) / IRIS_RX) ** 2 + ((y - 32.0) / IRIS_RY) ** 2 <= 1.0
    if iris:
        pupil = ((x - CX) / PUP_RX) ** 2 + ((y - 32.0) / PUP_RY) ** 2 <= 1.0
        return SLIT if pupil else GOLD
    d1 = math.hypot(x - CX, y - CY1) - R
    d2 = math.hypot(x - CX, y - CY2) - R
    d_lens = max(d1, d2)                 # negative inside the lens
    return GOLD if abs(d_lens) <= STROKE / 2.0 else None

rows = []
for py in range(HGT):
    row = bytearray()
    for px in range(W):
        r = g = b = 0.0
        hits = 0
        n = SS * SS
        for sy in range(SS):
            for sx in range(SS):
                ux = X0 + (px + (sx + 0.5) / SS) / SCALE
                uy = Y0 + (py + (sy + 0.5) / SS) / SCALE
                c = ink(ux, uy)
                if c is not None:
                    r += c[0]; g += c[1]; b += c[2]
                    hits += 1
        if hits:
            # average the covered samples only, so edges keep their own colour
            row += bytes((int(round(r / hits)), int(round(g / hits)),
                          int(round(b / hits)), int(round(255 * hits / n))))
        else:
            row += b"\x00\x00\x00\x00"
    rows.append(bytes(row))

def chunk(tag, data):
    return (struct.pack('>I', len(data)) + tag + data
            + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff))

raw = b''.join(b'\x00' + r for r in rows)
png = (b'\x89PNG\r\n\x1a\n'
       + chunk(b'IHDR', struct.pack('>IIBBBBB', W, HGT, 8, 6, 0, 0, 0))
       + chunk(b'IDAT', zlib.compress(raw, 9))
       + chunk(b'IEND', b''))

open('assets/img/logo-email.png', 'wb').write(png)
print(f"wrote assets/img/logo-email.png  {W}x{HGT}  {len(png)} bytes  (display {W//SCALE}x{HGT//SCALE})")

# A single transparent pixel. Mail clients honour an image's width and height
# attributes even when they have thrown away every scrap of CSS, so one of
# these scaled to 18x1 is a gap that cannot be sanitised away.
spacer = (b'\x89PNG\r\n\x1a\n'
          + chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 6, 0, 0, 0))
          + chunk(b'IDAT', zlib.compress(b'\x00\x00\x00\x00\x00', 9))
          + chunk(b'IEND', b''))
open('assets/img/spacer.png', 'wb').write(spacer)
print(f"wrote assets/img/spacer.png  1x1  {len(spacer)} bytes")
