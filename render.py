"""Deterministic raster engine for the news-image-20261126 entry.

Pure stdlib: an RGB framebuffer, a hand-drawn 5x7 pixel font, simple
vector shapes and a hand-rolled PNG encoder. No network, no files read,
no clock, no randomness -- two runs write byte-identical output.
"""

import math
import struct
import zlib

# ---------------------------------------------------------------- font
# Each glyph is 7 rows of 5 bits, top row first, MSB = leftmost pixel.
# Only capitals, digits and common punctuation are covered; text is
# rendered upper-cased and any unknown character becomes a blank cell.
_G = {
    "A": (0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001),
    "B": (0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110),
    "C": (0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110),
    "D": (0b11110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11110),
    "E": (0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111),
    "F": (0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000),
    "G": (0b01110, 0b10001, 0b10000, 0b10111, 0b10001, 0b10001, 0b01111),
    "H": (0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001),
    "I": (0b01110, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110),
    "J": (0b00111, 0b00010, 0b00010, 0b00010, 0b00010, 0b10010, 0b01100),
    "K": (0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001),
    "L": (0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111),
    "M": (0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001),
    "N": (0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001, 0b10001),
    "O": (0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110),
    "P": (0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000),
    "Q": (0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101),
    "R": (0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001),
    "S": (0b01111, 0b10000, 0b10000, 0b01110, 0b00001, 0b00001, 0b11110),
    "T": (0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100),
    "U": (0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110),
    "V": (0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100),
    "W": (0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b11011, 0b10001),
    "X": (0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001),
    "Y": (0b10001, 0b10001, 0b01010, 0b00100, 0b00100, 0b00100, 0b00100),
    "Z": (0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111),
    "0": (0b01110, 0b10001, 0b10011, 0b10101, 0b11001, 0b10001, 0b01110),
    "1": (0b00100, 0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110),
    "2": (0b01110, 0b10001, 0b00001, 0b00110, 0b01000, 0b10000, 0b11111),
    "3": (0b11111, 0b00010, 0b00100, 0b00010, 0b00001, 0b10001, 0b01110),
    "4": (0b00010, 0b00110, 0b01010, 0b10010, 0b11111, 0b00010, 0b00010),
    "5": (0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b10001, 0b01110),
    "6": (0b00110, 0b01000, 0b10000, 0b11110, 0b10001, 0b10001, 0b01110),
    "7": (0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b01000, 0b01000),
    "8": (0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110),
    "9": (0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00010, 0b01100),
    " ": (0, 0, 0, 0, 0, 0, 0),
    ".": (0, 0, 0, 0, 0, 0b01100, 0b01100),
    ",": (0, 0, 0, 0, 0b01100, 0b00100, 0b01000),
    ";": (0, 0b01100, 0, 0, 0b01100, 0b00100, 0b01000),
    ":": (0, 0b01100, 0, 0, 0, 0b01100, 0),
    "!": (0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0, 0b00100),
    "?": (0b01110, 0b10001, 0b00001, 0b00110, 0b00100, 0, 0b00100),
    "-": (0, 0, 0, 0b01110, 0, 0, 0),
    "\u2013": (0, 0, 0, 0b11111, 0, 0, 0),
    "\u2014": (0, 0, 0, 0b11111, 0, 0, 0),
    "'": (0b00100, 0b00100, 0b01000, 0, 0, 0, 0),
    '"': (0b01010, 0b01010, 0, 0, 0, 0, 0),
    "(": (0b00010, 0b00100, 0b01000, 0b01000, 0b01000, 0b00100, 0b00010),
    ")": (0b01000, 0b00100, 0b00010, 0b00010, 0b00010, 0b00100, 0b01000),
    "/": (0b00001, 0b00010, 0b00010, 0b00100, 0b01000, 0b01000, 0b10000),
    "%": (0b11001, 0b11010, 0b00010, 0b00100, 0b01000, 0b01011, 0b10011),
    "$": (0b00100, 0b01111, 0b10100, 0b01110, 0b00101, 0b11110, 0b00100),
    "&": (0b01100, 0b10010, 0b10100, 0b01000, 0b10101, 0b10010, 0b01101),
    "+": (0, 0b00100, 0b00100, 0b11111, 0b00100, 0b00100, 0),
    "=": (0, 0, 0b11111, 0, 0b11111, 0, 0),
    "#": (0b01010, 0b01010, 0b11111, 0b01010, 0b11111, 0b01010, 0b01010),
    "*": (0, 0b00100, 0b10101, 0b01110, 0b10101, 0b00100, 0),
    "\u2022": (0, 0, 0b01100, 0b01100, 0, 0, 0),
    "\u00b7": (0, 0, 0, 0b01100, 0b01100, 0, 0),
    "\u00d7": (0, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0),
    "<": (0b00010, 0b00100, 0b01000, 0b10000, 0b01000, 0b00100, 0b00010),
    ">": (0b01000, 0b00100, 0b00010, 0b00001, 0b00010, 0b00100, 0b01000),
}

_BLANK = (0, 0, 0, 0, 0, 0, 0)


def _glyph(ch):
    return _G.get(ch, _BLANK)


# ---------------------------------------------------------------- page
class Page:
    """An RGB framebuffer with drawing primitives."""

    def __init__(self, w, h, paper):
        self.w = w
        self.h = h
        self.buf = bytearray(paper * (w * h))

    def _off(self, x, y):
        return (y * self.w + x) * 3

    def dot(self, x, y, rgb):
        if 0 <= x < self.w and 0 <= y < self.h:
            o = self._off(x, y)
            self.buf[o:o + 3] = rgb

    def box(self, x, y, w, h, rgb):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            o = self._off(x0, yy)
            self.buf[o:o + (x1 - x0) * 3] = rgb * (x1 - x0)

    def hrule(self, x, y, w, rgb, thick=1):
        self.box(x, y, w, thick, rgb)

    def vrule(self, x, y, h, rgb, thick=1):
        self.box(x, y, thick, h, rgb)

    def seg(self, x0, y0, x1, y1, rgb):
        """Bresenham line, clipped by dot()."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.dot(x0, y0, rgb)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, rgb):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.dot(xx, yy, rgb)

    def ring(self, cx, cy, r, rgb, thick=2):
        for t in range(thick):
            rr = r - t
            for a in range(360):
                rad = math.radians(a)
                self.dot(cx + int(rr * math.cos(rad)),
                         cy + int(rr * math.sin(rad)), rgb)

    def tri(self, ax, ay, bx, by, cx, cy, rgb):
        """Filled triangle via scanline fill."""
        pts = sorted([(ax, ay), (bx, by), (cx, cy)], key=lambda p: p[1])
        (x0, y0), (x1, y1), (x2, y2) = pts

        def edge(xa, ya, xb, yb, y):
            if yb == ya:
                return xa
            return xa + (xb - xa) * (y - ya) / (yb - ya)

        for y in range(y0, y2 + 1):
            if y < y1:
                xa = edge(x0, y0, x1, y1, y)
                xb = edge(x0, y0, x2, y2, y)
            else:
                xa = edge(x1, y1, x2, y2, y)
                xb = edge(x0, y0, x2, y2, y)
            lo, hi = (xa, xb) if xa <= xb else (xb, xa)
            self.box(int(lo), y, int(hi) - int(lo) + 1, 1, rgb)

    def frame(self, x, y, w, h, rgb, thick=2):
        self.box(x, y, w, thick, rgb)
        self.box(x, y + h - thick, w, thick, rgb)
        self.box(x, y, thick, h, rgb)
        self.box(x + w - thick, y, thick, h, rgb)

    def stipple(self, x, y, w, h, rgb, step=4):
        """Light checker tint inside a rectangle."""
        for yy in range(y, y + h, step):
            for xx in range(x + ((yy // step) % 2) * step // 2, x + w, step):
                self.dot(xx, yy, rgb)

    # ------------------------------------------------------------ text
    def put_glyph(self, x, y, ch, rgb, scale=1):
        rows = _glyph(ch)
        for r in range(7):
            bits = rows[r]
            for c in range(5):
                if bits & (1 << (4 - c)):
                    self.box(x + c * scale, y + r * scale, scale, scale, rgb)

    def text_w(self, s, scale=1):
        """Pixel width of s at scale (6 px per cell)."""
        return len(s) * 6 * scale - scale

    def put_text(self, x, y, s, rgb, scale=1):
        s = s.upper()
        cx = x
        for ch in s:
            self.put_glyph(cx, y, ch, rgb, scale)
            cx += 6 * scale
        return cx

    def put_center(self, cx, y, s, rgb, scale=1):
        self.put_text(cx - self.text_w(s, scale) // 2, y, s, rgb, scale)

    def flow(self, x, y, w, s, rgb, scale=1, leading=None):
        """Greedy word wrap; over-wide words are hard-split. Returns
        the y just below the last line. Empty input yields one blank
        line (no crash, no overflow)."""
        if leading is None:
            leading = 9 * scale
        cell = 6 * scale
        max_chars = max(1, w // cell)
        words = []
        for raw in s.upper().split(" "):
            while len(raw) > max_chars:
                words.append(raw[:max_chars])
                raw = raw[max_chars:]
            words.append(raw)
        lines = [""]
        for word in words:
            if word == "":
                continue
            trial = word if lines[-1] == "" else lines[-1] + " " + word
            if len(trial) <= max_chars:
                lines[-1] = trial
            else:
                lines.append(word)
        yy = y
        for line in lines:
            self.put_text(x, yy, line, rgb, scale)
            yy += leading
        return yy


# ---------------------------------------------------------------- png
def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(page, path):
    raw = bytearray()
    stride = page.w * 3
    for y in range(page.h):
        raw.append(0)
        raw += page.buf[y * stride:(y + 1) * stride]
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", struct.pack(">IIBBBBB", page.w, page.h, 8, 2, 0, 0, 0))
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)
    return len(png)
