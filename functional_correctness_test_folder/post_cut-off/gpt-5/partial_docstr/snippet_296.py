
import json
import os
import tempfile
from pathlib import Path
from html import escape
from datetime import datetime


class BenchmarkVisualizer:
    '''Utility for visualizing benchmark results and agent interactions across multiple problems'''

    def __init__(self, output_dir=None):
        '''
        Initialize the benchmark visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix="benchmark_viz_")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _find_problem_visualizations(self, visualizations_dir):
        mapping = {}
        if not visualizations_dir:
            return mapping
        vdir = Path(visualizations_dir)
        if not vdir.exists():
            return mapping
        # Search for .html files; map by stem and also by parent directory name
        for path in vdir.rglob("*.html"):
            stem = path.stem
            mapping.setdefault(stem, str(path.resolve()))
            # Also map directory name if it looks like a problem id
            parent_name = path.parent.name
            mapping.setdefault(parent_name, str(path.resolve()))
        return mapping

    def _extract_problem_id(self, item):
        # Try common keys for problem id
        for key in ("problem_id", "id", "problem", "name", "task_id", "task"):
            if key in item and item[key] is not None:
                return str(item[key])
        # Fallback to index hash
        return None

    def _format_value(self, v):
        if isinstance(v, float):
            return f"{v:.4f}"
        return str(v)

    def generate_summary_html(self, summary_data, results_data, problem_visualizations=None, title=None):
        '''
        Generate HTML for visualizing benchmark summary with links to problem visualizations.
        Args:
            summary_data: Dictionary with benchmark summary data
            results_data: List of problem results data
            problem_visualizations: Optional dictionary mapping problem_id to visualization file paths
            title: Optional title for the visualization
        Returns:
            HTML string
        '''
        title = title or "Benchmark Summary"
        problem_visualizations = problem_visualizations or {}

        # Determine common result columns
        columns = set()
        for item in results_data or []:
            for k in item.keys():
                if k not in {"trace", "log", "artifacts"}:
                    columns.add(k)
        # Ensure problem_id column first
        preferred_order = ["problem_id", "id", "name", "status",
                           "success", "score", "accuracy", "latency", "runtime", "cost"]
        ordered_cols = []
        for c in preferred_order:
            if c in columns:
                ordered_cols.append(c)
                columns.discard(c)
        ordered_cols.extend(sorted(columns))

        # Build summary section
        summary_items = []
        if isinstance(summary_data, dict):
            for k, v in summary_data.items():
                if isinstance(v, (dict, list)):
                    continue
                summary_items.append((str(k), self._format_value(v)))

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Build HTML
        def esc(s):
            return escape(str(s)) if s is not None else ""

        # Table rows
        rows_html = []
        for idx, item in enumerate(results_data or []):
            pid = self._extract_problem_id(item)
            link = None
            if pid and pid in problem_visualizations:
                link = problem_visualizations[pid]
            # Construct cells
            cells = []
            for col in ordered_cols:
                val = item.get(col, "")
                cells.append(f"<td>{esc(self._format_value(val))}</td>")
            # Add link cell
            if link:
                link_cell = f'<td><a href="{esc(link)}" target="_blank">View</a></td>'
            else:
                link_cell = "<td><span class='muted'>N/A</span></td>"
            # Fallback if no columns
            if not ordered_cols:
                cells.append(f"<td>{esc(pid or idx)}</td>")
                cells.append(link_cell)
            else:
                cells.append(link_cell)
            row_class = "odd" if idx % 2 else "even"
            rows_html.append(
                f"<tr class='{row_class}'>" + "".join(cells) + "</tr>")

        # Headers
        headers = [esc(c)
                   for c in ordered_cols] if ordered_cols else ["problem"]
        headers.append("visualization")

        summary_kv_html = ""
        if summary_items:
            summary_kv_html = "".join(
                f"<div class='kv'><span class='k'>{esc(k)}</span><span class='v'>{esc(v)}</span></div>"
                for k, v in sorted(summary_items)
            )

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(title)}</title>
<style>
:root {{
  --bg: #0b0c10;
  --panel: #12141a;
  --text: #e5e7eb;
  --muted: #9aa3af;
  --accent: #60a5fa;
  --ok: #34d399;
  --warn: #f59e0b;
  --bad: #ef4444;
  --border: #1f2937;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; padding: 0; font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Apple Color Emoji", "Segoe UI Emoji";
  background: radial-gradient(1200px 800px at 20% -10%, #1b2435 0%, #0b0c10 40%) fixed;
  color: var(--text);
}}
.container {{
  max-width: 1200px; margin: 24px auto; padding: 0 16px 40px;
}}
.header {{
  display: flex; align-items: baseline; justify-content: space-between; gap: 12px; margin: 24px 0 12px;
}}
.title {{
  font-size: 28px; font-weight: 700; letter-spacing: 0.2px;
}}
.meta {{
  font-size: 13px; color: var(--muted);
}}
.panel {{
  background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
  border: 1px solid var(--border);
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
  overflow: hidden;
}}
.section-title {{
  font-size: 15px; font-weight: 600; color: var(--muted); padding: 14px 16px; border-bottom: 1px solid var(--border);
  background: rgba(0,0,0,0.15);
}}
.summary-grid {{
  display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; padding: 14px;
}}
.kv {{
  display: flex; justify-content: space-between; gap: 12px; background: rgba(255,255,255,0.03); border: 1px solid var(--border);
  border-radius: 10px; padding: 10px 12px;
}}
.kv .k {{ color: var(--muted); }}
.kv .v {{ font-weight: 600; }}

.table-wrap {{ overflow: auto; }}
table {{
  width: 100%; border-collapse: collapse; font-size: 14px;
}}
thead th {{
  position: sticky; top: 0; background: rgba(0,0,0,0.3); border-bottom: 1px solid var(--border); text-align: left; padding: 10px;
}}
tbody td {{
  border-bottom: 1px solid var(--border); padding: 10px;
}}
tr.even {{ background: rgba(255,255,255,0.02); }}
tr.odd {{ background: rgba(255,255,255,0.01); }}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.muted {{ color: var(--muted); }}
.footer {{
  margin-top: 18px; color: var(--muted); font-size: 12px; text-align: right;
}}
</style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="title">{esc(title)}</div>
      <div class="meta">Generated {esc(now_str)}</div>
    </div>

    <div class="panel">
      <div class="section-title">Summary</div>
      <div class="summary-grid">
        {summary_kv_html if summary_kv_html else "<div class='muted' style='padding:12px'>No summary data.</div>"}
      </div>
    </div>

    <div style="height: 16px"></div>

    <div class="panel">
      <div class="section-title">Problems</div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>{"".join(f"<th>{h}</th>" for h in headers)}</tr>
          </thead>
          <tbody>
            {''.join(rows_html) if rows_html else "<tr><td class='muted' style='padding:12px' colspan='99'>No results available.</td></tr>"}
          </tbody>
        </table>
      </div>
    </div>

    <div class="footer">
      BenchmarkVisualizer
    </div>
  </div>
</body>
</html>"""
        return html

    def visualize_benchmark(self, summary_file, results_file=None, visualizations_dir=None, output_file=None):
        """
        Create a summary HTML file from provided JSON files and optional per-problem visualizations.
        Returns the path to the generated HTML file.
        """
        summary_path = Path(summary_file)
        if not summary_path.exists():
            raise FileNotFoundError(f"Summary file not found: {summary_path}")
        with open(summary_path, "r", encoding="utf-8") as f:
            summary_data = json.load(f)

        results_data = []
        if results_file:
            rpath = Path(results_file)
            if not rpath.exists():
                raise FileNotFoundError(f"Results file not found: {rpath}")
            with open(rpath, "r", encoding="utf-8") as f:
                results_data = json.load(f)
            if not isinstance(results_data, list):
                # Try common wrapper keys
                if isinstance(results_data, dict):
                    for k in ("results", "problems", "items", "data"):
                        if k in results_data and isinstance(results_data[k], list):
                            results_data = results_data[k]
                            break
                if not isinstance(results_data, list):
                    results_data = []

        pv_map = self._find_problem_visualizations(
            visualizations_dir) if visualizations_dir else {}

        title = None
        if isinstance(summary_data, dict):
            title = summary_data.get("title") or summary_data.get(
                "name") or "Benchmark Summary"

        html = self.generate_summary_html(
            summary_data=summary_data, results_data=results_data, problem_visualizations=pv_map, title=title)

        if output_file:
            out_path = Path(output_file)
            out_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            out_path = self.output_dir / "benchmark_summary.html"

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

        return str(out_path.resolve())
