import os
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from statistics import mean
from html import escape


class BenchmarkVisualizer:
    '''Utility for visualizing benchmark results and agent interactions across multiple problems'''

    def __init__(self, output_dir=None):
        '''
        Initialize the benchmark visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _format_seconds(self, seconds):
        try:
            if seconds is None:
                return ''
            seconds = float(seconds)
            if seconds < 1:
                return f'{seconds:.3f}s'
            return str(timedelta(seconds=int(seconds)))
        except Exception:
            return str(seconds)

    def _parse_datetime(self, value):
        if not value:
            return ''
        try:
            # Try common formats or epoch
            if isinstance(value, (int, float)):
                return datetime.fromtimestamp(value).isoformat(timespec='seconds')
            # If string datetime
            return str(datetime.fromisoformat(str(value)))
        except Exception:
            return str(value)

    def _get(self, dct, keys, default=None):
        for k in keys:
            if k in dct and dct[k] is not None:
                return dct[k]
        return default

    def _is_success(self, item):
        v = self._get(item, ['success', 'passed',
                      'solved', 'is_solved', 'ok', 'pass'])
        if isinstance(v, bool):
            return v
        if v is not None:
            try:
                if isinstance(v, (int, float)):
                    return v != 0
                s = str(v).strip().lower()
                return s in ('true', 'yes', 'y', '1', 'success', 'passed', 'solved', 'ok')
            except Exception:
                pass
        status = self._get(item, ['status', 'result', 'outcome'])
        if status:
            s = str(status).strip().lower()
            return s in ('success', 'passed', 'pass', 'ok', 'solved', 'complete')
        score = self._get(item, ['score'])
        try:
            if score is not None:
                return float(score) > 0
        except Exception:
            pass
        return False

    def _problem_id_from_result(self, item):
        for k in ('problem_id', 'id', 'problem', 'name', 'task_id', 'task', 'problem_name'):
            if k in item and item[k] is not None:
                return str(item[k])
        # Try nested fields
        meta = item.get('meta') or item.get('metadata') or {}
        for k in ('problem_id', 'id', 'name'):
            if k in meta and meta[k] is not None:
                return str(meta[k])
        return ''

    def _agent_from_result(self, item):
        for k in ('agent', 'model', 'policy', 'runner', 'solver'):
            if k in item and item[k]:
                return str(item[k])
        agent_cfg = item.get('agent') or item.get('config') or {}
        if isinstance(agent_cfg, dict):
            for k in ('name', 'id', 'model'):
                if k in agent_cfg and agent_cfg[k]:
                    return str(agent_cfg[k])
        return ''

    def _runtime_from_result(self, item):
        # Common keys
        for k in ('runtime_sec', 'runtime', 'time_sec', 'time', 'elapsed', 'duration'):
            v = item.get(k)
            if v is not None:
                try:
                    return float(v)
                except Exception:
                    pass
        # Nested metrics
        metrics = item.get('metrics') or {}
        for k in ('runtime_sec', 'runtime', 'time'):
            v = metrics.get(k)
            if v is not None:
                try:
                    return float(v)
                except Exception:
                    pass
        return None

    def _score_from_result(self, item):
        v = self._get(item, ['score', 'reward', 'accuracy'])
        try:
            return None if v is None else float(v)
        except Exception:
            return v

    def _attempts_from_result(self, item):
        v = self._get(item, ['attempts', 'num_attempts', 'trials', 'steps'])
        try:
            return None if v is None else int(v)
        except Exception:
            return v

    def _error_from_result(self, item):
        v = self._get(item, ['error', 'error_message',
                      'last_error', 'exception'])
        if v is None:
            logs = self._get(item, ['logs', 'stderr'])
            if isinstance(logs, str):
                return logs[-200:]
        return v

    def _sanitize_key(self, s):
        s = str(s).strip().lower()
        s = re.sub(r'\.(html?|htm)$', '', s)
        s = re.sub(r'[^a-z0-9]+', '-', s)
        return s.strip('-')

    def _find_link_for_problem(self, mapping, problem_id, problem_name=None):
        candidates = []
        if problem_id:
            candidates.append(str(problem_id))
        if problem_name:
            candidates.append(str(problem_name))
        # Also add sanitized versions
        candidates += [self._sanitize_key(c) for c in candidates if c]
        for c in candidates:
            if c in mapping:
                return mapping[c]
        # Try loose matching on mapping keys
        pid_san = self._sanitize_key(problem_id) if problem_id else ''
        pname_san = self._sanitize_key(problem_name) if problem_name else ''
        for k in mapping.keys():
            if k == pid_san or k == pname_san:
                return mapping[k]
        return None

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
        results = results_data or []
        pv = problem_visualizations or {}

        total_problems = (
            summary_data.get('num_problems')
            or summary_data.get('total_problems')
            or summary_data.get('total')
            or (len(results) if isinstance(results, list) else 0)
        )

        success_count = (
            summary_data.get('num_solved')
            or summary_data.get('success_count')
        )
        if success_count is None and isinstance(results, list):
            success_count = sum(1 for r in results if self._is_success(r))

        success_rate = summary_data.get('success_rate')
        if success_rate is None and total_problems:
            success_rate = (success_count or 0) / total_problems * 100

        runtimes = [self._runtime_from_result(r) for r in results]
        runtimes = [r for r in runtimes if r is not None]
        total_runtime = (
            summary_data.get('total_runtime_sec')
            or summary_data.get('total_runtime')
            or summary_data.get('wall_time')
            or (sum(runtimes) if runtimes else None)
        )
        avg_runtime = (
            summary_data.get('avg_runtime_sec')
            or (mean(runtimes) if runtimes else None)
        )

        scores = [self._score_from_result(r) for r in results]
        scores_num = [s for s in scores if isinstance(s, (int, float))]
        avg_score = mean(scores_num) if scores_num else None

        benchmark_name = summary_data.get(
            'benchmark_name') or summary_data.get('name') or 'Benchmark'
        created_at = self._parse_datetime(summary_data.get(
            'started_at') or summary_data.get('start_time') or summary_data.get('timestamp'))
        finished_at = self._parse_datetime(summary_data.get(
            'finished_at') or summary_data.get('end_time'))

        page_title = title or f'{benchmark_name} Results'

        # Build summary cards
        def metric_card(label, value, subtitle=None):
            val_str = '' if value is None else (f'{value:.2f}%' if label.lower().startswith(
                'success') and isinstance(value, (int, float)) else escape(str(value)))
            sub = f'<div class="metric-sub">{escape(str(subtitle))}</div>' if subtitle else ''
            return f'''
            <div class="metric">
              <div class="metric-label">{escape(label)}</div>
              <div class="metric-value">{val_str}</div>
              {sub}
            </div>
            '''

        summary_cards = []
        summary_cards.append(metric_card('Total Problems', total_problems))
        summary_cards.append(metric_card(
            'Solved', success_count, f'{(success_rate or 0):.2f}%'))
        summary_cards.append(metric_card('Avg Runtime', self._format_seconds(
            avg_runtime) if avg_runtime is not None else None))
        summary_cards.append(metric_card('Total Runtime', self._format_seconds(
            total_runtime) if total_runtime is not None else None))
        if avg_score is not None:
            summary_cards.append(metric_card('Avg Score', f'{avg_score:.3f}'))

        # Build table rows
        rows_html = []
        for r in results:
            pid = self._problem_id_from_result(r)
            pname = r.get('name') or r.get('problem_name') or ''
            display_id = pid or pname or ''
            status_ok = self._is_success(r)
            status_text = 'Success' if status_ok else 'Fail'
            score = self._score_from_result(r)
            runtime = self._runtime_from_result(r)
            attempts = self._attempts_from_result(r)
            agent = self._agent_from_result(r)
            err = self._error_from_result(r)
            err_str = ''
            if err:
                s = str(err).strip().replace('\n', ' ')
                if len(s) > 120:
                    s = s[:117] + '...'
                err_str = escape(s)

            link = self._find_link_for_problem(pv, pid, pname)
            link_html = f'<a class="plink" href="{escape(link)}" target="_blank">view</a>' if link else ''

            row_class = 'ok' if status_ok else 'fail'
            rows_html.append(f'''
            <tr class="{row_class}">
              <td class="cell-id">{escape(str(display_id))}</td>
              <td class="cell-status">{status_text}</td>
              <td class="cell-score">{"" if score is None else escape(f"{score:.4f}" if isinstance(score, (int, float)) else str(score))}</td>
              <td class="cell-runtime">{escape(self._format_seconds(runtime))}</td>
              <td class="cell-attempts">{"" if attempts is None else escape(str(attempts))}</td>
              <td class="cell-agent">{escape(agent)}</td>
              <td class="cell-link">{link_html}</td>
              <td class="cell-error">{err_str}</td>
            </tr>
            ''')

        # If results not provided, still allow summary_data-only page
        results_section = ''
        if rows_html:
            results_section = f'''
            <div class="controls">
              <input id="search" type="text" placeholder="Filter problems..." />
              <span class="legend">
                <span class="dot ok"></span> Success
                <span class="dot fail"></span> Fail
              </span>
            </div>
            <div class="table-wrap">
              <table id="results">
                <thead>
                  <tr>
                    <th>Problem</th>
                    <th>Status</th>
                    <th>Score</th>
                    <th>Runtime</th>
                    <th>Attempts</th>
                    <th>Agent</th>
                    <th>Link</th>
                    <th>Error</th>
                  </tr>
                </thead>
                <tbody>
                  {''.join(rows_html)}
                </tbody>
              </table>
            </div>
            '''

        # Additional details section from summary_data (generic key-value)
        extra_keys = []
        for k, v in summary_data.items():
            if k in ('num_problems', 'total_problems', 'total', 'num_solved', 'success_count', 'success_rate', 'total_runtime_sec', 'total_runtime', 'wall_time', 'avg_runtime_sec', 'benchmark_name', 'name', 'started_at', 'start_time', 'timestamp', 'finished_at', 'end_time', 'results', 'problems', 'cases'):
                continue
            extra_keys.append((k, v))
        extra_html = ''
        if extra_keys:
            items = ''.join(
                [f'<div class="kv"><span class="k">{escape(str(k))}</span><span class="v">{escape(str(v))}</span></div>' for k, v in extra_keys])
            extra_html = f'''
            <div class="extras">
              <div class="section-title">Details</div>
              <div class="kv-wrap">
                {items}
              </div>
            </div>
            '''

        html_doc = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{escape(page_title)}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root {{
      --bg: #0b0f14;
      --panel: #121821;
      --text: #e7edf5;
      --muted: #9fb0c8;
      --ok: #2fbf71;
      --fail: #ff6b6b;
      --accent: #5aa2ff;
      --border: #243244;
    }}
    html, body {{
      margin: 0; padding: 0; background: var(--bg); color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, "Helvetica Neue", Arial, "Noto Sans", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", sans-serif;
    }}
    .wrap {{ max-width: 1200px; margin: 24px auto 64px; padding: 0 16px; }}
    .title {{ font-size: 26px; font-weight: 700; margin-bottom: 6px; }}
    .subtitle {{ color: var(--muted); margin-bottom: 20px; }}
    .cards {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px; margin: 20px 0 8px;
    }}
    .metric {{
      background: var(--panel); border: 1px solid var(--border);
      padding: 14px; border-radius: 10px;
    }}
    .metric-label {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .06em; }}
    .metric-value {{ font-size: 22px; font-weight: 700; margin-top: 6px; }}
    .metric-sub {{ margin-top: 2px; color: var(--muted); font-size: 12px; }}
    .controls {{
      display: flex; align-items: center; justify-content: space-between;
      gap: 12px; margin: 18px 0 10px;
    }}
    #search {{
      flex: 1; max-width: 420px; background: var(--panel); color: var(--text);
      border: 1px solid var(--border); border-radius: 8px; padding: 10px 12px; outline: none;
    }}
    .legend {{ color: var(--muted); font-size: 13px; }}
    .dot {{
      display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin: 0 8px 0 0; vertical-align: middle;
    }}
    .dot.ok {{ background: var(--ok); }}
    .dot.fail {{ background: var(--fail); }}
    .table-wrap {{ overflow: auto; border-radius: 10px; border: 1px solid var(--border); }}
    table {{ width: 100%; border-collapse: collapse; background: var(--panel); }}
    thead th {{
      text-align: left; position: sticky; top: 0; background: #182131; color: var(--muted);
      font-weight: 600; font-size: 12px; letter-spacing: .05em; text-transform: uppercase;
      padding: 12px 10px; border-bottom: 1px solid var(--border);
    }}
    tbody td {{ padding: 10px; border-top: 1px solid var(--border); vertical-align: top; }}
    tbody tr.ok td .cell-status {{ color: var(--ok); }}
    tbody tr.fail td .cell-status {{ color: var(--fail); }}
    .cell-id {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; font-size: 13px; }}
    .cell-error {{ color: var(--muted); max-width: 420px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .plink {{ color: var(--accent); text-decoration: none; }}
    .plink:hover {{ text-decoration: underline; }}
    .extras {{ margin-top: 26px; }}
    .section-title {{ font-size: 18px; font-weight: 700; margin-bottom: 10px; }}
    .kv-wrap {{
      display: grid; grid-template-columns: 1fr 2fr; gap: 8px 16px;
      background: var(--panel); border: 1px solid var(--border); padding: 14px; border-radius: 10px;
    }}
    .kv .k {{ color: var(--muted); }}
    .kv .v {{ margin-left: 8px; word-break: break-word; }}
    .footer {{ color: var(--muted); font-size: 12px; margin-top: 22px; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="title">{escape(page_title)}</div>
    <div class="subtitle">
      {escape(benchmark_name)}
      {' • Started ' + escape(created_at) if created_at else ''}
      {' • Finished ' + escape(finished_at) if finished_at else ''}
    </div>
    <div class="cards">
      {''.join(summary_cards)}
    </div>
    {results_section}
    {extra_html}
    <div class="footer">Generated on {escape(datetime.now().isoformat(timespec='seconds'))}</div>
  </div>
  <script>
    const input = document.querySelector('#search');
    const rows = Array.from(document.querySelectorAll('#results tbody tr'));
    if (input && rows.length) {{
      input.addEventListener('input', () => {{
        const q = input.value.trim().toLowerCase();
        rows.forEach(r => {{
          const txt = r.innerText.toLowerCase();
          r.style.display = txt.includes(q) ? '' : 'none';
        }});
      }});
    }}
  </script>
</body>
</html>
'''
        return html_doc

    def visualize_benchmark(self, summary_file, results_file=None, visualizations_dir=None, output_file=None):
        '''
        Generate HTML visualization from benchmark summary file with links to problem visualizations.
        Args:
            summary_file: Path to the benchmark summary JSON file
            results_file: Optional path to the benchmark results JSON file
            visualizations_dir: Optional directory containing problem visualizations
            output_file: Optional path to save the HTML output
        Returns:
            Path to the generated HTML file
        '''
        summary_path = Path(summary_file)
        if not summary_path.exists():
            raise FileNotFoundError(f'Summary file not found: {summary_file}')

        with open(summary_path, 'r', encoding='utf-8') as f:
            summary_data = json.load(f)

        # Load results
        results_data = []
        if results_file:
            rf = Path(results_file)
            if not rf.exists():
                raise FileNotFoundError(
                    f'Results file not found: {results_file}')
            with open(rf, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
            if isinstance(loaded, list):
                results_data = loaded
            elif isinstance(loaded, dict):
                for key in ('results', 'problems', 'cases', 'items'):
                    if key in loaded and isinstance(loaded[key], list):
                        results_data = loaded[key]
                        break
        else:
            # Try to read embedded results in summary
            if isinstance(summary_data, dict):
                for key in ('results', 'problems', 'cases', 'items'):
                    if key in summary_data and isinstance(summary_data[key], list):
                        results_data = summary_data[key]
                        break

        # Determine output file path
        if output_file:
            out_path = Path(output_file)
        else:
            out_dir = self.output_dir if self.output_dir else summary_path.parent
            out_dir.mkdir(parents=True, exist_ok=True)
            out_name = f'{summary_path.stem}_summary.html'
            out_path = out_dir / out_name

        # Build mapping for problem visualizations
        mapping = {}
        if visualizations_dir:
            vdir = Path(visualizations_dir)
            if vdir.exists():
                html_files = list(vdir.rglob('*.html'))
                for p in html_files:
                    key_variants = set()
                    base = p.stem  # filename without extension
                    key_variants.add(base)
                    key_variants.add(self._sanitize_key(base))
                    # Also add common stripped prefixes
                    m = re.sub(
                        r'^(problem|prob|task|case)[-_]*', '', base, flags=re.IGNORECASE)
                    key_variants.add(m)
                    key_variants.add(self._sanitize_key(m))
                    # Relative path from out_path parent
                    rel = os.path.relpath(p, out_path.parent)
                    for k in key_variants:
                        mapping[k] = rel

        title = summary_data.get('title') or summary_data.get(
            'benchmark_name') or 'Benchmark Results'
        html_str = self.generate_summary_html(
            summary_data, results_data, mapping, title=title)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html_str)

        return str(out_path)
