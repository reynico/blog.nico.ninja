#!/usr/bin/env python3
"""Interactive waterfall viewer for rtl_power CSV output.

Usage:
    python3 waterfall.py [--dir DIR] [--host HOST] [--port PORT]

Then open http://127.0.0.1:8000 in a browser.
"""

import argparse
import glob
import json
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


def parse_rtl_power(path):
    """Parse an rtl_power CSV into a waterfall matrix.

    Returns dict with frequency axis (MHz), time labels, and 2D power grid.
    """
    sweeps = []          # list of (label, {freq_hz: power_db})
    freqs = set()
    start_low = None
    current = None
    current_label = None

    with open(path, "r") as fh:
        for line in fh:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 7:
                continue
            date, time_s = parts[0], parts[1]
            try:
                f_low = float(parts[2])
                f_high = float(parts[3])
                f_step = float(parts[4])
                # parts[5] = samples
                values = [float(v) for v in parts[6:] if v != ""]
            except ValueError:
                continue

            if start_low is None:
                start_low = f_low

            # A new sweep starts when the segment wraps back to the range start.
            if f_low == start_low:
                if current:
                    sweeps.append((current_label, current))
                current = {}
                current_label = f"{date} {time_s}"

            n = len(values)
            span = f_high - f_low
            for i, val in enumerate(values):
                # Bin center frequency.
                freq = f_low + (i + 0.5) * (span / n) if n else f_low
                freq = round(freq)
                current[freq] = val
                freqs.add(freq)

    if current:
        sweeps.append((current_label, current))

    freq_axis = sorted(freqs)
    freq_index = {f: i for i, f in enumerate(freq_axis)}

    grid = []
    times = []
    for label, mapping in sweeps:
        row = [None] * len(freq_axis)
        for f, val in mapping.items():
            row[freq_index[f]] = val
        grid.append(row)
        times.append(label)

    return {
        "file": os.path.basename(path),
        "freqs_mhz": [round(f / 1e6, 6) for f in freq_axis],
        "times": times,
        "power": grid,
    }


def list_csvs(directory):
    files = sorted(glob.glob(os.path.join(directory, "*.csv")))
    return [os.path.basename(f) for f in files]


PAGE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>rtl_power waterfall</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
  body { font-family: system-ui, sans-serif; margin: 0; background: #111; color: #eee; }
  header { padding: 12px 16px; background: #1c1c1c; display: flex; gap: 16px; align-items: center; flex-wrap: wrap; }
  select, input, button { background: #2a2a2a; color: #eee; border: 1px solid #444; border-radius: 4px; padding: 6px 8px; }
  label { font-size: 13px; color: #bbb; }
  #plot { width: 100vw; height: calc(100vh - 60px); }
  .stat { font-size: 13px; color: #9cf; }
</style>
</head>
<body>
<header>
  <label>File <select id="file"></select></label>
  <label>Colorscale
    <select id="scale">
      <option>Jet</option><option>Viridis</option><option>Hot</option>
      <option>Electric</option><option>Portland</option><option>Greys</option>
    </select>
  </label>
  <label>Min dB <input id="zmin" type="number" step="1" style="width:70px"></label>
  <label>Max dB <input id="zmax" type="number" step="1" style="width:70px"></label>
  <button id="reset">Auto range</button>
  <span class="stat" id="stat"></span>
</header>
<div id="plot"></div>
<script>
let raw = null;

async function loadFiles() {
  const r = await fetch('/files');
  const files = await r.json();
  const sel = document.getElementById('file');
  sel.innerHTML = files.map(f => `<option>${f}</option>`).join('');
  if (files.length) load(files[0]);
}

async function load(name) {
  document.getElementById('stat').textContent = 'loading ' + name + '...';
  const r = await fetch('/data?file=' + encodeURIComponent(name));
  raw = await r.json();
  autoRange();
  render();
}

function flatVals() {
  const out = [];
  for (const row of raw.power) for (const v of row) if (v !== null) out.push(v);
  return out;
}

function autoRange() {
  const vals = flatVals().sort((a, b) => a - b);
  if (!vals.length) return;
  const lo = vals[Math.floor(vals.length * 0.02)];
  const hi = vals[Math.floor(vals.length * 0.98)];
  document.getElementById('zmin').value = Math.round(lo);
  document.getElementById('zmax').value = Math.round(hi);
}

function render() {
  if (!raw) return;
  const zmin = parseFloat(document.getElementById('zmin').value);
  const zmax = parseFloat(document.getElementById('zmax').value);
  const data = [{
    z: raw.power,
    x: raw.freqs_mhz,
    y: raw.times,
    type: 'heatmap',
    colorscale: document.getElementById('scale').value,
    zmin: zmin, zmax: zmax,
    colorbar: { title: 'dB' },
    hovertemplate: '%{x:.3f} MHz<br>%{y}<br>%{z:.1f} dB<extra></extra>'
  }];
  const layout = {
    paper_bgcolor: '#111', plot_bgcolor: '#111',
    font: { color: '#eee' },
    margin: { l: 160, r: 20, t: 20, b: 50 },
    xaxis: { title: 'Frequency (MHz)' },
    yaxis: { title: 'Time', autorange: 'reversed' }
  };
  Plotly.react('plot', data, layout, { responsive: true });
  document.getElementById('stat').textContent =
    `${raw.file} - ${raw.times.length} sweeps x ${raw.freqs_mhz.length} bins`;
}

document.getElementById('file').addEventListener('change', e => load(e.target.value));
document.getElementById('scale').addEventListener('change', render);
document.getElementById('zmin').addEventListener('change', render);
document.getElementById('zmax').addEventListener('change', render);
document.getElementById('reset').addEventListener('click', () => { autoRange(); render(); });

loadFiles();
</script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    directory = "."

    def log_message(self, *args):
        pass

    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send(200, PAGE.encode(), "text/html; charset=utf-8")
        elif parsed.path == "/files":
            body = json.dumps(list_csvs(self.directory)).encode()
            self._send(200, body, "application/json")
        elif parsed.path == "/data":
            qs = parse_qs(parsed.query)
            name = os.path.basename(qs.get("file", [""])[0])
            path = os.path.join(self.directory, name)
            if not name or not os.path.isfile(path):
                self._send(404, b'{"error":"not found"}', "application/json")
                return
            body = json.dumps(parse_rtl_power(path)).encode()
            self._send(200, body, "application/json")
        else:
            self._send(404, b"not found", "text/plain")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=".", help="directory with rtl_power CSVs")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()

    Handler.directory = os.path.abspath(args.dir)
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Serving {Handler.directory} at http://{args.host}:{args.port}")
    print("Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
