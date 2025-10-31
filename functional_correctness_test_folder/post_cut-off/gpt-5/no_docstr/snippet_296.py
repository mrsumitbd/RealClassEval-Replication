import os
import json
import base64
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union, List


class BenchmarkVisualizer:

    def __init__(self, output_dir=None):
        self.output_dir = Path(output_dir or os.getcwd())
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _escape_html(self, text: Any) -> str:
        s = str(text)
        return (
            s.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )

    def _img_to_data_uri(self, path: Union[str, Path]) -> Optional[str]:
        p = Path(path)
        if not p.is_file():
            return None
        ext = p.suffix.lower().lstrip(".")
        mime = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
            "svg": "image/svg+xml",
            "webp": "image/webp",
        }.get(ext)
        if not mime:
            return None
        try:
            if ext == "svg":
                data = p.read_text(encoding="utf-8")
                b64 = base64.b64encode(data.encode("utf-8")).decode("ascii")
            else:
                data = p.read_bytes()
                b64 = base64.b64encode(data).decode("ascii")
            return f"data:{mime};base64,{b64}"
        except Exception:
            return None

    def _dict_to_kv_list_html(self, d: Dict[str, Any]) -> str:
        items = []
        for k in sorted(d.keys(), key=lambda x: str(x).lower()):
            v = d[k]
            if isinstance(v, (dict, list)):
                v_str = self._escape_html(json.dumps(
                    v, indent=2, ensure_ascii=False))
                items.append(
                    f"<div class='kv'><div class='k'>{self._escape_html(k)}</div><pre class='v'>{v_str}</pre></div>")
            else:
                items.append(
                    f"<div class='kv'><div class='k'>{self._escape_html(k)}</div><div class='v'>{self._escape_html(v)}</div></div>")
        return "\n".join(items)

    def _results_to_table_html(self, results_data: Any) -> str:
        # Normalize to list of rows with consistent columns
        rows: List[Dict[str, Any]] = []
        if isinstance(results_data, list):
            for item in results_data:
                if isinstance(item, dict):
                    rows.append(item)
                else:
                    rows.append({"value": item})
        elif isinstance(results_data, dict):
            # assume mapping of problem -> metrics
            for k, v in results_data.items():
                if isinstance(v, dict):
                    r = {"problem": k, **v}
                else:
                    r = {"problem": k, "value": v}
                rows.append(r)
        else:
            rows.append({"value": results_data})

        # Determine columns
        cols = set()
        for r in rows:
            cols.update(r.keys())
        # Prefer common column ordering
        preferred = ["problem", "status", "score", "accuracy", "pass_rate",
                     "runtime", "time", "latency", "memory", "attempts", "error", "value"]
        ordered = [c for c in preferred if c in cols] + \
            [c for c in sorted(cols) if c not in preferred]
        # Build table
        thead = "<tr>" + \
            "".join(
                f"<th>{self._escape_html(c)}</th>" for c in ordered) + "</tr>"
        trs = []
        for r in rows:
            tds = []
            for c in ordered:
                v = r.get(c, "")
                if isinstance(v, float):
                    # nice formatting
                    v_str = f"{v:.6g}"
                elif isinstance(v, (dict, list)):
                    v_str = json.dumps(v, ensure_ascii=False)
                else:
                    v_str = str(v)
                tds.append(f"<td>{self._escape_html(v_str)}</td>")
            trs.append("<tr>" + "".join(tds) + "</tr>")
        tbody = "\n".join(trs)
        return f"<table class='data'>\n<thead>{thead}</thead>\n<tbody>\n{tbody}\n</tbody>\n</table>"

    def generate_summary_html(self, summary_data, results_data, problem_visualizations=None, title=None):
        title = title or "Benchmark Summary"
        generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Build problem visualizations section
        viz_html = ""
        if problem_visualizations:
            cards = []
            # attempt deterministic order
            for key in sorted(problem_visualizations.keys(), key=lambda x: str(x).lower()):
                path = problem_visualizations[key]
                data_uri = self._img_to_data_uri(path)
                caption = self._escape_html(str(key))
                if data_uri:
                    img_el = f"<img src='{data_uri}' alt='{caption}'/>"
                else:
                    path_disp = self._escape_html(str(path))
                    img_el = f"<div class='img-missing'>Image not available: {path_disp}</div>"
                cards.append(
                    f"<div class='card'><div class='card-img'>{img_el}</div><div class='card-caption'>{caption}</div></div>")
            viz_html = "<div class='cards'>\n" + "\n".join(cards) + "\n</div>"

        # Summary key-values
        summary_section = ""
        if isinstance(summary_data, dict):
            summary_section = self._dict_to_kv_list_html(summary_data)
        else:
            summary_section = f"<pre>{self._escape_html(summary_data)}</pre>"

        # Results table
        results_section = self._results_to_table_html(results_data)

        css = """
<style>
:root {
  color-scheme: light dark;
}
body {
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 0;
  line-height: 1.5;
}
.header {
  padding: 24px 20px 10px 20px;
  background: linear-gradient(90deg, #1f6feb 0%, #7944e3 100%);
  color: white;
}
.header h1 {
  margin: 0;
  font-size: 28px;
}
.header .meta {
  opacity: 0.9;
  font-size: 13px;
}
.container {
  padding: 20px;
}
.section {
  margin: 20px 0 28px 0;
}
.section h2 {
  margin: 0 0 12px 0;
  font-size: 20px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 6px;
}
.kv {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 8px 16px;
  align-items: start;
  padding: 6px 0;
  border-bottom: 1px dashed rgba(128,128,128,0.3);
}
.kv .k {
  font-weight: 600;
}
.kv .v {
  overflow: auto;
}
pre {
  white-space: pre-wrap;
  margin: 0;
}
table.data {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}
table.data th, table.data td {
  border: 1px solid rgba(128,128,128,0.3);
  padding: 6px 8px;
  text-align: left;
  vertical-align: top;
}
table.data thead th {
  background: rgba(127,127,127,0.1);
}
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}
.card {
  border: 1px solid rgba(128,128,128,0.3);
  border-radius: 8px;
  overflow: hidden;
  background: rgba(127,127,127,0.05);
}
.card-img {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
}
.card-img img {
  width: 100%;
  height: 180px;
  object-fit: contain;
  display: block;
  background: white;
}
.img-missing {
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  font-size: 13px;
  padding: 8px;
}
.card-caption {
  padding: 8px 10px;
  font-size: 14px;
  font-weight: 600;
}
.footer {
  font-size: 12px;
  color: #666;
  border-top: 1px solid rgba(128,128,128,0.3);
  padding: 14px 20px;
}
@media (prefers-color-scheme: dark) {
  .card-img { background: #111; }
  .card { background: rgba(255,255,255,0.03); border-color: rgba(255,255,255,0.12); }
  table.data th, table.data td { border-color: rgba(255,255,255,0.12); }
  table.data thead th { background: rgba(255,255,255,0.07); }
  .kv { border-bottom-color: rgba(255,255,255,0.12); }
}
</style>
"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{self._escape_html(title)}</title>
{css}
</head>
<body>
  <div class="header">
    <h1>{self._escape_html(title)}</h1>
    <div class="meta">Generated at {self._escape_html(generated_at)}</div>
  </div>
  <div class="container">
    <div class="section">
      <h2>Summary</h2>
      {summary_section}
    </div>
    <div class="section">
      <h2>Results</h2>
      {results_section}
    </div>
    {f"<div class='section'><h2>Problem Visualizations</h2>{viz_html}</div>" if viz_html else ""}
  </div>
  <div class="footer">
    Created by BenchmarkVisualizer
  </div>
</body>
</html>"""
        return html

    def visualize_benchmark(self, summary_file, results_file=None, visualizations_dir=None, output_file=None):
        summary_path = Path(summary_file)
        if not summary_path.is_file():
            raise FileNotFoundError(f"Summary file not found: {summary_file}")
        with summary_path.open("r", encoding="utf-8") as f:
            try:
                summary_data = json.load(f)
            except json.JSONDecodeError:
                # fallback: read as text
                summary_data = {"raw": f.read()}

        results_data: Any = {}
        if results_file:
            results_path = Path(results_file)
            if not results_path.is_file():
                raise FileNotFoundError(
                    f"Results file not found: {results_file}")
            with results_path.open("r", encoding="utf-8") as f:
                try:
                    results_data = json.load(f)
                except json.JSONDecodeError:
                    results_data = {"raw": f.read()}
        else:
            # if results missing, attempt to extract from summary
            results_data = summary_data.get(
                "results") if isinstance(summary_data, dict) else {}

        problem_visualizations: Dict[str, Path] = {}
        if visualizations_dir:
            vdir = Path(visualizations_dir)
            if vdir.is_dir():
                # Map by stem name
                exts = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")
                for p in vdir.iterdir():
                    if p.is_file() and p.suffix.lower() in exts:
                        problem_visualizations[p.stem] = p

        title = None
        if isinstance(summary_data, dict):
            title = summary_data.get("title") or summary_data.get(
                "name") or summary_data.get("benchmark") or None
        title = title or "Benchmark Summary"

        html = self.generate_summary_html(
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations if problem_visualizations else None,
            title=title,
        )

        out_path = Path(output_file) if output_file else (
            self.output_dir / "benchmark_summary.html")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        return str(out_path)
