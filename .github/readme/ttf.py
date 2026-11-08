"""Glyph outlines from a TrueType font, as SVG path data, with no dependencies.

Reads the `cmap`, `hmtx`, `loca` and `glyf` tables of a .ttf with TrueType
outlines, so README text can be drawn as vector paths that look the same in
every browser. Kerning is not applied; `tracking` adds even spacing instead.
"""
import struct


class Font:
    def __init__(self, path):
        with open(path, "rb") as fh:
            self.data = fh.read()
        self.tables = {}
        num = struct.unpack(">H", self.data[4:6])[0]
        for i in range(num):
            tag, _check, offset, length = struct.unpack(">4sIII", self.data[12 + i * 16 : 28 + i * 16])
            self.tables[tag.decode("latin-1")] = (offset, length)
        head = self.tables["head"][0]
        self.units = struct.unpack(">H", self.data[head + 18 : head + 20])[0]
        self.loc_long = struct.unpack(">h", self.data[head + 50 : head + 52])[0] == 1
        hhea = self.tables["hhea"][0]
        self.n_hmetrics = struct.unpack(">H", self.data[hhea + 34 : hhea + 36])[0]
        maxp = self.tables["maxp"][0]
        self.n_glyphs = struct.unpack(">H", self.data[maxp + 4 : maxp + 6])[0]
        self.cmap = self._cmap()

    def _cmap(self):
        base = self.tables["cmap"][0]
        count = struct.unpack(">H", self.data[base + 2 : base + 4])[0]
        for i in range(count):
            pid, eid, off = struct.unpack(">HHI", self.data[base + 4 + i * 8 : base + 12 + i * 8])
            if (pid, eid) in ((3, 1), (0, 3), (0, 4)):
                sub = base + off
                if struct.unpack(">H", self.data[sub : sub + 2])[0] == 4:
                    return self._format4(sub)
        raise ValueError("no format 4 cmap")

    def _format4(self, sub):
        seg = struct.unpack(">H", self.data[sub + 6 : sub + 8])[0] // 2
        ends = struct.unpack(f">{seg}H", self.data[sub + 14 : sub + 14 + seg * 2])
        starts_at = sub + 16 + seg * 2
        starts = struct.unpack(f">{seg}H", self.data[starts_at : starts_at + seg * 2])
        deltas = struct.unpack(f">{seg}h", self.data[starts_at + seg * 2 : starts_at + seg * 4])
        ranges_at = starts_at + seg * 4
        ranges = struct.unpack(f">{seg}H", self.data[ranges_at : ranges_at + seg * 2])
        out = {}
        for i in range(seg):
            for code in range(starts[i], ends[i] + 1):
                if code == 0xFFFF:
                    continue
                if ranges[i] == 0:
                    gid = (code + deltas[i]) & 0xFFFF
                else:
                    at = ranges_at + i * 2 + ranges[i] + (code - starts[i]) * 2
                    gid = struct.unpack(">H", self.data[at : at + 2])[0]
                    if gid:
                        gid = (gid + deltas[i]) & 0xFFFF
                out[code] = gid
        return out

    def advance(self, gid):
        hmtx = self.tables["hmtx"][0]
        i = min(gid, self.n_hmetrics - 1)
        return struct.unpack(">H", self.data[hmtx + i * 4 : hmtx + i * 4 + 2])[0]

    def _loca(self, gid):
        loca = self.tables["loca"][0]
        if self.loc_long:
            a, b = struct.unpack(">II", self.data[loca + gid * 4 : loca + gid * 4 + 8])
        else:
            a, b = struct.unpack(">HH", self.data[loca + gid * 2 : loca + gid * 2 + 4])
            a, b = a * 2, b * 2
        return a, b

    def contours(self, gid):
        """Each contour as a list of (x, y, on_curve) in font units."""
        start, end = self._loca(gid)
        if start == end:
            return []
        g = self.tables["glyf"][0] + start
        n = struct.unpack(">h", self.data[g : g + 2])[0]
        if n < 0:
            return self._composite(g)
        p = g + 10
        ends = struct.unpack(f">{n}H", self.data[p : p + n * 2])
        p += n * 2
        ilen = struct.unpack(">H", self.data[p : p + 2])[0]
        p += 2 + ilen
        count = ends[-1] + 1
        flags = []
        while len(flags) < count:
            f = self.data[p]
            p += 1
            flags.append(f)
            if f & 8:
                rep = self.data[p]
                p += 1
                flags.extend([f] * rep)
        xs, ys = [], []
        v = 0
        for f in flags:
            if f & 2:
                d = self.data[p]
                p += 1
                v += d if f & 16 else -d
            elif not f & 16:
                v += struct.unpack(">h", self.data[p : p + 2])[0]
                p += 2
            xs.append(v)
        v = 0
        for f in flags:
            if f & 4:
                d = self.data[p]
                p += 1
                v += d if f & 32 else -d
            elif not f & 32:
                v += struct.unpack(">h", self.data[p : p + 2])[0]
                p += 2
            ys.append(v)
        out, s = [], 0
        for e in ends:
            out.append([(xs[i], ys[i], bool(flags[i] & 1)) for i in range(s, e + 1)])
            s = e + 1
        return out

    def _composite(self, g):
        p = g + 10
        out = []
        while True:
            flags, gid = struct.unpack(">HH", self.data[p : p + 4])
            p += 4
            if flags & 1:
                dx, dy = struct.unpack(">hh", self.data[p : p + 4])
                p += 4
            else:
                dx, dy = struct.unpack(">bb", self.data[p : p + 2])
                p += 2
            if flags & 8:
                p += 2
            elif flags & 64:
                p += 4
            elif flags & 128:
                p += 8
            for c in self.contours(gid):
                out.append([(x + dx, y + dy, on) for x, y, on in c])
            if not flags & 32:
                break
        return out


def contour_path(points, ox, oy, k):
    """One closed quadratic contour as SVG path data, y flipped, scaled by k."""
    pts = [(ox + x * k, oy - y * k, on) for x, y, on in points]
    if not pts:
        return ""
    start = next((i for i, pt in enumerate(pts) if pt[2]), None)
    if start is None:
        a, b = pts[0], pts[1]
        first = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, True)
        pts = [first] + pts[1:] + [pts[0]]
        start = 0
    pts = pts[start:] + pts[:start]
    f = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")
    d = [f"M{f(pts[0][0])} {f(pts[0][1])}"]
    i, n = 1, len(pts)
    while i <= n:
        cur = pts[i % n]
        if cur[2]:
            d.append(f"L{f(cur[0])} {f(cur[1])}")
            i += 1
            continue
        nxt = pts[(i + 1) % n]
        if nxt[2]:
            d.append(f"Q{f(cur[0])} {f(cur[1])} {f(nxt[0])} {f(nxt[1])}")
            i += 2
        else:
            mid = ((cur[0] + nxt[0]) / 2, (cur[1] + nxt[1]) / 2)
            d.append(f"Q{f(cur[0])} {f(cur[1])} {f(mid[0])} {f(mid[1])}")
            i += 1
    d.append("Z")
    return "".join(d)


def text_path(font, text, x, baseline, size, tracking=0.0):
    """`text` as SVG path data starting at `x` on `baseline`, and its width."""
    k = size / font.units
    pen = x
    parts = []
    for ch in text:
        gid = font.cmap.get(ord(ch), 0)
        for c in font.contours(gid):
            parts.append(contour_path(c, pen, baseline, k))
        pen += font.advance(gid) * k + tracking
    return "".join(parts), pen - x - tracking


def text_width(font, text, size, tracking=0.0):
    return text_path(font, text, 0, 0, size, tracking)[1]
