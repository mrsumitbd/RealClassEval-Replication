import os
import json
import glob
import datetime
from pathlib import Path
from html import escape


class BenchmarkVisualizer:
    """Utility for visualizing benchmark results and agent interactions across multiple problems"""

    def __init__(self, output_dir=None):
        """
        Initialize the benchmark visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        """
        self.output_dir = Path(output_dir) if output_dir else None
        if self.output_dir:
            self.output_dir.mkdir(parents=True, exist_ok=True)

    def _format_number(self, v):
        try:
            if isinstance(v, int):
                return f'{v:,}'
            if isinstance(v, float):
                return f'{v:,.4f}'.rstrip('0').rstrip('.')
        except Exception:
            pass
        return str(v)

    def _normalize_results(self, results_data):
        if results_data is None:
            return []
        if isinstance(results_data, dict):
            # Could be mapping problem_id -> result or structure with 'results' key
            if 'results' in results_data and isinstance(results_data['results'], list):
                results = results_data['results']
            else:
                # values are results
                results = list(results_data.values())
        elif isinstance(results_data, list):
            results = results_data
        else:
            results = []

        norm = []
        for item in results:
            if not isinstance(item, dict):
                continue
            pid = item.get('problem_id') or item.get('id') or item.get(
                'problem') or item.get('name') or item.get('task_id')
            status = item.get('status')
            if status is None and 'success' in item:
                status = 'success' if bool(item.get('success')) else 'failed'
            # score candidates
            score = None
            for k in ['score', 'final_score', 'avg_score', 'reward', 'accuracy', 'metric', 'grade', 'result_score']:
                if k in item:
                    score = item[k]
                    break
            # runtime candidates (seconds)
            runtime = None
            for k in ['runtime_seconds', 'duration', 'time', 'elapsed', 'wall_time', 'run_time_s', 'total_time_s']:
                if k in item:
                    runtime = item[k]
                    break
            # steps
            steps = None
            for k in ['steps', 'num_steps', 'turns', 'messages', 'iterations']:
                if k in item:
                    steps = item[k]
                    break
            # agent
            agent = None
            for k in ['agent', 'agent_name', 'model', 'runner']:
                if k in item:
                    agent = item[k]
                    break
            viz = item.get('visualization') or item.get(
                'viz_path') or item.get('html_path')
            norm.append({
                'problem_id': str(pid) if pid is not None else '',
                'status': status if status is not None else '',
                'score': score,
                'success': item.get('success'),
                'runtime_seconds': runtime,
                'steps': steps,
                'agent': agent,
                'visualization': viz,
                '_raw': item
            })
        return norm

    def _slugify(self, s):
        s = str(s).strip().lower()
        out = []
        for ch in s:
            if ch.isalnum():
                out.append(ch)
            elif ch in (' ', '-', '_', '.', ':'):
                out.append('-')
        slug = ''.join(out)
        while '--' in slug:
            slug = slug.replace('--', '-')
        return slug.strip('-')

    def _collect_visualizations(self, visualizations_dir, summary_mapping=None):
        mapping = {}
        if isinstance(summary_mapping, dict):
            mapping.update(summary_mapping)
        if visualizations_dir:
            vdir = Path(visualizations_dir)
            if vdir.is_dir():
                for path in glob.glob(str(vdir / '**' / '*.html'), recursive=True):
                    p = Path(path)
                    base = p.stem
                    keys = set([base, base.lower(), self._slugify(base)])
                    # also add variant without common prefixes
                    for prefix in ['problem-', 'task-', 'prob-', 'id-']:
                        if base.lower().startswith(prefix):
                            keys.add(self._slugify(base[len(prefix):]))
                    for k in keys:
                        mapping[k] = str(p)
        return mapping

    def _match_viz(self, pid, mapping):
        if not pid:
            return None
        candidates = [
            pid,
            str(pid).lower(),
            self._slugify(pid),
        ]
        for c in candidates:
            if c in mapping:
                return mapping[c]
        # try contains
        for k, v in mapping.items():
            if k in candidates:
                return v
            if k in candidates[-1] or candidates[-1] in k:
                return v
        return None

    def _derive_summary_stats(self, summary_data, results_norm):
        stats = {}
        if isinstance(summary_data, dict):
            for k, v in summary_data.items():
                # Skip potentially large nested items
                if isinstance(v, (list, dict)) and k.lower() in {'results', 'problems', 'problem_results', 'details'}:
                    continue
                stats[k] = v
        # Add derived stats if not present
        if results_norm:
            total = len(results_norm)
            success_count = sum(1 for r in results_norm if (
                r.get('success') is True) or (str(r.get('status')).lower() == 'success'))
            if 'total_problems' not in stats:
                stats['total_problems'] = total
            if 'solved' not in stats and 'success_count' not in stats:
                stats['solved'] = success_count
            if 'success_rate' not in stats and total > 0:
                stats['success_rate'] = success_count / total
            # average score if numeric
            scores = []
            for r in results_norm:
                try:
                    val = r.get('score')
                    if isinstance(val, (int, float)):
                        scores.append(val)
                except Exception:
                    pass
            if scores and 'avg_score' not in stats:
                stats['avg_score'] = sum(scores) / len(scores)
            # total runtime
            runtimes = []
            for r in results_norm:
                val = r.get('runtime_seconds')
                try:
                    if isinstance(val, (int, float)):
                        runtimes.append(val)
                except Exception:
                    pass
            if runtimes and 'total_runtime_seconds' not in stats:
                stats['total_runtime_seconds'] = sum(runtimes)
        return stats

    def generate_summary_html(self, summary_data, results_data, problem_visualizations=None, title=None):
        """
        Generate HTML for visualizing benchmark summary with links to problem visualizations.
        Args:
            summary_data: Dictionary with benchmark summary data
            results_data: List of problem results data
            problem_visualizations: Optional dictionary mapping problem_id to visualization file paths
            title: Optional title for the visualization
        Returns:
            HTML string
        """
        results_norm = self._normalize_results(results_data if results_data is not None else (
            summary_data.get('results') if isinstance(summary_data, dict) else None))
        viz_map = problem_visualizations or {}
        stats = self._derive_summary_stats(summary_data if isinstance(
            summary_data, dict) else {}, results_norm)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        page_title = title or summary_data.get(
            'title') if isinstance(summary_data, dict) else None
        page_title = page_title or 'Benchmark Summary'

        # Build summary metrics HTML
        metrics_rows = []
        for k, v in stats.items():
            label = escape(str(k).replace('_', ' ').title())
            if isinstance(v, float) and 'rate' in str(k).lower():
                value = f"{v*100:.2f}%"
            else:
                value = self._format_number(v)
            metrics_rows.append(
                f'<div class="metric"><div class="label">{label}</div><div class="value">{escape(str(value))}</div></div>')
        metrics_html = '\n'.join(metrics_rows)

        # Build problems table
        table_rows = []
        for r in results_norm:
            pid = r.get('problem_id') or ''
            viz = r.get('visualization') or viz_map.get(
                pid) or self._match_viz(pid, viz_map) or ''
            status = r.get('status', '')
            score_val = r.get('score')
            score = '' if score_val is None else self._format_number(score_val)
            success = r.get('success')
            success_str = '' if success is None else (
                'Yes' if bool(success) else 'No')
            runtime = r.get('runtime_seconds')
            runtime_str = '' if runtime is None else self._format_number(
                runtime)
            steps = r.get('steps')
            steps_str = '' if steps is None else self._format_number(steps)
            agent = r.get('agent') or ''

            viz_cell = f'<a href="{escape(viz)}" target="_blank">Open</a>' if viz else ''
            table_rows.append(
                '<tr>'
                f'<td class="mono">{escape(str(pid))}</td>'
                f'<td>{escape(str(status))}</td>'
                f'<td class="num">{escape(str(score))}</td>'
                f'<td>{escape(success_str)}</td>'
                f'<td class="num">{escape(str(runtime_str))}</td>'
                f'<td class="num">{escape(str(steps_str))}</td>'
                f'<td class="mono">{escape(str(agent))}</td>'
                f'<td>{viz_cell}</td>'
                '</tr>'
            )
        table_body = '\n'.join(table_rows)

        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{escape(page_title)}</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
:root {{
  --bg: #0b0f14;
  --card: #121822;
  --text: #e6edf3;
  --muted: #9aa7b1;
  --accent: #4aa3ff;
  --ok: #16c98d;
  --bad: #ff6b6b;
  --table-alt: #0e141b;
  --border: #1c2530;
}}
html, body {{ margin:0; padding:0; background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, "Noto Sans", "Liberation Sans", sans-serif; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 24px; }}
h1 {{ margin: 0 0 16px 0; font-size: 28px; font-weight: 600; }}
.header {{ display: flex; justify-content: space-between; align-items: baseline; gap: 12px; flex-wrap: wrap; }}
.timestamp {{ color: var(--muted); font-size: 14px; }}
.card {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 16px; }}
.metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; }}
.metric {{ background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(0,0,0,0)); border: 1px solid var(--border); border-radius: 8px; padding: 12px; }}
.metric .label {{ font-size: 12px; color: var(--muted); margin-bottom: 6px; }}
.metric .value {{ font-size: 18px; font-weight: 600; }}
.table-wrap {{ margin-top: 20px; }}
table {{ width: 100%; border-collapse: collapse; overflow: hidden; border-radius: 10px; }}
thead th {{ text-align: left; font-size: 12px; color: var(--muted); background: var(--card); position: sticky; top: 0; padding: 10px 12px; border-bottom: 1px solid var(--border); }}
tbody td {{ padding: 10px 12px; border-bottom: 1px solid var(--border); }}
tbody tr:nth-child(odd) {{ background: var(--table-alt); }}
.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
.mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; }}
.status-success {{ color: var(--ok); }}
.status-failed {{ color: var(--bad); }}
.controls {{ display:flex; gap:10px; align-items:center; margin: 16px 0; }}
input[type="text"] {{ background: var(--bg); border: 1px solid var(--border); color: var(--text); border-radius: 8px; padding: 8px 10px; outline: none; min-width: 220px; }}
.small {{ color: var(--muted); font-size: 12px; }}
.link a {{ color: var(--accent); text-decoration: none; }}
.link a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>{escape(page_title)}</h1>
    <div class="timestamp">Generated: {escape(now)}</div>
  </div>
  <div class="card">
    <div class="metrics">
      {metrics_html}
    </div>
  </div>
  <div class="controls">
    <input id="search" type="text" placeholder="Filter by problem id, status, agent..." />
    <div class="small">Showing <span id="shownCount">0</span> of <span id="totalCount">{len(table_rows)}</span></div>
  </div>
  <div class="table-wrap">
    <table id="problems">
      <thead>
        <tr>
          <th>Problem ID</th>
          <th>Status</th>
          <th class="num">Score</th>
          <th>Success</th>
          <th class="num">Runtime (s)</th>
          <th class="num">Steps</th>
          <th>Agent</th>
          <th>Visualization</th>
        </tr>
      </thead>
      <tbody>
        {table_body}
      </tbody>
    </table>
  </div>
</div>
<script>
(function() {{
  const search = document.getElementById('search');
  const table = document.getElementById('problems').getElementsByTagName('tbody')[0];
  const shownCount = document.getElementById('shownCount');
  function filter() {{
    const q = (search.value || '').toLowerCase();
    let shown = 0;
    for (const row of table.rows) {{
      const text = row.innerText.toLowerCase();
      const show = !q || text.indexOf(q) !== -1;
      row.style.display = show ? '' : 'none';
      if (show) shown += 1;
    }}
    shownCount.textContent = shown;
  }}
  search.addEventListener('input', filter);
  filter();
}})();
</script>
</body>
</html>"""
        return html_doc

    def visualize_benchmark(self, summary_file, results_file=None, visualizations_dir=None, output_file=None):
        """
        Generate HTML visualization from benchmark summary file with links to problem visualizations.
        Args:
            summary_file: Path to the benchmark summary JSON file
            results_file: Optional path to the benchmark results JSON file
            visualizations_dir: Optional directory containing problem visualizations
            output_file: Optional path to save the HTML output
        Returns:
            Path to the generated HTML file
        """
        summary_path = Path(summary_file)
        if not summary_path.is_file():
            raise FileNotFoundError(f'Summary file not found: {summary_file}')
        with summary_path.open('r', encoding='utf-8') as f:
            summary_data = json.load(f)

        # Determine results_data
        results_data = None
        if results_file:
            rf = Path(results_file)
            if not rf.is_file():
                raise FileNotFoundError(
                    f'Results file not found: {results_file}')
            with rf.open('r', encoding='utf-8') as f:
                results_data = json.load(f)
        else:
            # Try to extract from summary_data
            if isinstance(summary_data, dict):
                if 'results' in summary_data:
                    results_data = summary_data['results']
                elif 'problems' in summary_data:
                    results_data = summary_data['problems']
                elif 'problem_results' in summary_data:
                    results_data = summary_data['problem_results']

        # Build visualization mapping from dir and possible mapping inside summary
        viz_map = {}
        if isinstance(summary_data, dict) and isinstance(summary_data.get('problem_visualizations'), dict):
            viz_map.update(summary_data['problem_visualizations'])
        viz_map = self._collect_visualizations(
            visualizations_dir, summary_mapping=viz_map)

        title = None
        if isinstance(summary_data, dict):
            title = summary_data.get('title')

        html_content = self.generate_summary_html(
            summary_data, results_data, problem_visualizations=viz_map, title=title)

        # Determine output path
        if output_file:
            out_path = Path(output_file)
        else:
            base_name = summary_path.stem + '.html'
            if self.output_dir:
                out_path = self.output_dir / base_name
            else:
                out_path = summary_path.with_suffix('.html')
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open('w', encoding='utf-8') as f:
            f.write(html_content)
        return str(out_path)
