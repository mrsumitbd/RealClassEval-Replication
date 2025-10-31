import json
import os
from pathlib import Path
from html import escape as _escape
from datetime import datetime
from statistics import mean
from typing import Dict, List, Optional, Any


class BenchmarkVisualizer:
    '''Utility for visualizing benchmark results and agent interactions across multiple problems'''

    def __init__(self, output_dir=None):
        '''
        Initialize the benchmark visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = Path(
            output_dir) if output_dir else Path.cwd() / 'benchmark_reports'
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _slug(self, s: str) -> str:
        out = []
        prev_dash = False
        for ch in s.lower():
            if ch.isalnum():
                out.append(ch)
                prev_dash = False
            else:
                if not prev_dash:
                    out.append('-')
                    prev_dash = True
        res = ''.join(out).strip('-')
        return res or s.lower()

    def _human_time(self, seconds: Optional[float]) -> str:
        if seconds is None:
            return '-'
        try:
            seconds = float(seconds)
        except Exception:
            return str(seconds)
        if seconds < 1:
            return f'{seconds*1000:.0f} ms'
        mins, secs = divmod(int(seconds), 60)
        hrs, mins = divmod(mins, 60)
        if hrs:
            return f'{hrs}h {mins}m {secs}s'
        if mins:
            return f'{mins}m {secs}s'
        return f'{seconds:.2f} s'

    def _status_info(self, status_raw: Any) -> (str, str):
        s = str(status_raw).strip().lower() if status_raw is not None else ''
        if s in ('pass', 'passed', 'success', 'succeeded', 'ok', 'true', '1', 'complete', 'completed'):
            return 'Passed', '#2ea043'
        if s in ('skip', 'skipped'):
            return 'Skipped', '#bf8700'
        if s in ('running', 'in_progress', 'in-progress', 'pending'):
            return 'Running', '#0366d6'
        if s in ('', 'none', 'unknown'):
            return 'Unknown', '#57606a'
        return 'Failed', '#d1242f'

    def _infer_results_list(self, summary_data: dict, results_data: Optional[Any]) -> List[dict]:
        if isinstance(results_data, list):
            return results_data
        # Try common keys within summary data
        for key in ('results', 'problems', 'problem_results', 'items', 'cases'):
            val = summary_data.get(key)
            if isinstance(val, list):
                return val
        return []

    def _compute_overall_stats(self, summary_data: dict, results: List[dict]) -> dict:
        # If summary already has totals, prefer them; else compute.
        total = summary_data.get('total_problems') or summary_data.get(
            'total') or len(results)
        passed = summary_data.get('passed')
        failed = summary_data.get('failed')
        skipped = summary_data.get('skipped')

        if passed is None or failed is None or skipped is None:
            p = f_ = sk = 0
            scores = []
            times = []
            for r in results:
                status_label, _ = self._status_info(
                    r.get('status', r.get('outcome', r.get('result'))))
                if status_label == 'Passed':
                    p += 1
                elif status_label == 'Failed':
                    f_ += 1
                elif status_label == 'Skipped':
                    sk += 1
                sc = r.get('score') if 'score' in r else (
                    r.get('reward') if 'reward' in r else r.get('accuracy'))
                if isinstance(sc, (int, float)):
                    scores.append(float(sc))
                tm = r.get('time', r.get('duration', r.get('elapsed')))
                try:
                    if tm is not None:
                        times.append(float(tm))
                except Exception:
                    pass
            if total == 0:
                total = p + f_ + sk
            passed = p if passed is None else passed
            failed = f_ if failed is None else failed
            skipped = sk if skipped is None else skipped
            avg_score = summary_data.get('avg_score')
            avg_time = summary_data.get('avg_time')
            if avg_score is None:
                avg_score = (mean(scores) if scores else None)
            if avg_time is None:
                avg_time = (mean(times) if times else None)
        else:
            avg_score = summary_data.get('avg_score')
            avg_time = summary_data.get('avg_time')

        success_rate = summary_data.get('success_rate')
        if success_rate is None:
            denom = (total - skipped) if (total - skipped) > 0 else total
            success_rate = (passed / denom * 100.0) if denom else 0.0

        started = summary_data.get(
            'start_time') or summary_data.get('started_at')
        finished = summary_data.get('end_time') or summary_data.get(
            'ended_at') or summary_data.get('finished_at')
        duration = summary_data.get('duration')
        if duration is None:
            try:
                if started and finished:
                    st = datetime.fromisoformat(
                        str(started).replace('Z', '+00:00'))
                    ft = datetime.fromisoformat(
                        str(finished).replace('Z', '+00:00'))
                    duration = (ft - st).total_seconds()
            except Exception:
                duration = None

        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'success_rate': success_rate,
            'avg_score': avg_score,
            'avg_time': avg_time,
            'start_time': started,
            'end_time': finished,
            'duration': duration,
        }

    def _rel_link(self, target_path: Path, base_dir: Path) -> str:
        try:
            return os.path.relpath(str(target_path), start=str(base_dir))
        except Exception:
            return str(target_path)

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
        problem_visualizations = problem_visualizations or {}
        results = self._infer_results_list(summary_data or {}, results_data)
        stats = self._compute_overall_stats(summary_data or {}, results)

        page_title = title or summary_data.get('title') or 'Benchmark Summary'
        esc = _escape

        def badge_html(status):
            label, color = self._status_info(status)
            return f'<span class="badge" style="background:{color}1A;color:{color};border:1px solid {color};">{esc(label)}</span>'

        def val_or_dash(v, fmt='{:.3f}'):
            if v is None or v == '':
                return '-'
            if isinstance(v, float) and fmt:
                try:
                    return fmt.format(v)
                except Exception:
                    return str(v)
            return str(v)

        styles = '''
        body { font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; margin: 0; color: #24292f; }
        .container { max-width: 1200px; margin: 0 auto; padding: 24px; }
        h1 { font-size: 24px; margin: 0 0 16px 0; }
        .sub { color: #57606a; margin-bottom: 24px; }
        .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 20px; }
        .card { border: 1px solid #d0d7de; border-radius: 8px; padding: 12px; background: #fff; }
        .card .label { color: #57606a; font-size: 12px; }
        .card .value { font-size: 20px; font-weight: 600; }
        .badge { font-size: 12px; border-radius: 999px; padding: 2px 8px; display: inline-block; }
        table { width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #d0d7de; border-radius: 8px; overflow: hidden; }
        thead { background: #f6f8fa; }
        th, td { padding: 10px 12px; border-bottom: 1px solid #d0d7de; text-align: left; font-size: 14px; }
        tr:hover { background: #f6f8fa; }
        .muted { color: #57606a; }
        .nowrap { white-space: nowrap; }
        .link { color: #0969da; text-decoration: none; }
        .link:hover { text-decoration: underline; }
        .toolbar { display: flex; gap: 8px; align-items: center; margin: 12px 0 16px 0; }
        input[type="search"] { padding: 8px 10px; border: 1px solid #d0d7de; border-radius: 6px; width: 280px; }
        details { margin-top: 16px; }
        code, pre { font-family: ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace; }
        .right { text-align: right; }
        '''

        # Build table rows
        rows_html = []
        for r in results:
            pid = r.get('problem_id') or r.get('id') or r.get(
                'problem') or r.get('task_id') or r.get('task')
            name = r.get('problem_name') or r.get(
                'name') or r.get('title') or ''
            display_id = str(pid) if pid is not None else (name or '-')
            status_raw = r.get('status', r.get('outcome', r.get('result')))
            score = r.get('score') if 'score' in r else (
                r.get('reward') if 'reward' in r else r.get('accuracy'))
            tm = r.get('time', r.get('duration', r.get('elapsed')))
            steps = r.get('num_steps', r.get('steps'))
            agent = r.get('agent') or r.get(
                'model') or r.get('agent_name') or ''
            link = None
            if pid is not None and pid in problem_visualizations:
                link = problem_visualizations[pid]
            elif name:
                slug = self._slug(str(name))
                if slug in problem_visualizations:
                    link = problem_visualizations[slug]
            elif pid is not None:
                slug = self._slug(str(pid))
                if slug in problem_visualizations:
                    link = problem_visualizations[slug]

            name_cell = esc(
                str(name)) if name else '<span class="muted">-</span>'
            id_cell = esc(str(display_id))

            if link:
                name_cell = f'<a class="link" href="{esc(str(link))}" target="_blank" rel="noopener">{name_cell or id_cell}</a>'

            rows_html.append(
                f'<tr data-search="{esc((str(pid) or "") + " " + (str(name) or ""))}">'
                f'<td class="nowrap">{name_cell}</td>'
                f'<td class="muted">{id_cell}</td>'
                f'<td>{badge_html(status_raw)}</td>'
                f'<td class="right">{esc(val_or_dash(score, fmt="{:.3f}"))}</td>'
                f'<td class="right">{esc(self._human_time(tm))}</td>'
                f'<td class="right">{esc(str(steps) if steps is not None else "-")}</td>'
                f'<td class="nowrap">{esc(str(agent)) if agent else "-"}</td>'
                f'</tr>'
            )

        # Summary cards
        cards_html = f'''
        <div class="cards">
          <div class="card">
            <div class="label">Total</div>
            <div class="value">{stats["total"]}</div>
          </div>
          <div class="card">
            <div class="label">Passed</div>
            <div class="value">{stats["passed"]}</div>
          </div>
          <div class="card">
            <div class="label">Failed</div>
            <div class="value">{stats["failed"]}</div>
          </div>
          <div class="card">
            <div class="label">Skipped</div>
            <div class="value">{stats["skipped"]}</div>
          </div>
          <div class="card">
            <div class="label">Success rate</div>
            <div class="value">{stats["success_rate"]:.1f}%</div>
          </div>
          <div class="card">
            <div class="label">Avg. score</div>
            <div class="value">{val_or_dash(stats["avg_score"], fmt="{:.3f}")}</div>
          </div>
          <div class="card">
            <div class="label">Avg. time</div>
            <div class="value">{self._human_time(stats["avg_time"])}</div>
          </div>
          <div class="card">
            <div class="label">Duration</div>
            <div class="value">{self._human_time(stats["duration"])}</div>
          </div>
        </div>
        '''

        toolbar_html = '''
        <div class="toolbar">
          <input id="searchBox" type="search" placeholder="Filter problems..." />
        </div>
        '''

        table_html = f'''
        <table id="problems">
          <thead>
            <tr>
              <th>Problem</th>
              <th>ID</th>
              <th>Status</th>
              <th class="right">Score</th>
              <th class="right">Time</th>
              <th class="right">Steps</th>
              <th>Agent</th>
            </tr>
          </thead>
          <tbody>
            {''.join(rows_html) if rows_html else '<tr><td colspan="7" class="muted">No problem results found.</td></tr>'}
          </tbody>
        </table>
        '''

        raw_data_html = f'''
        <details>
          <summary>Show raw data</summary>
          <h3>Summary</h3>
          <pre>{_escape(json.dumps(summary_data, indent=2, default=str))}</pre>
          <h3>Results</h3>
          <pre>{_escape(json.dumps(results, indent=2, default=str))}</pre>
        </details>
        '''

        script = '''
        <script>
        (function(){
          const q = document.getElementById('searchBox');
          if (!q) return;
          q.addEventListener('input', function() {
            const term = q.value.toLowerCase();
            document.querySelectorAll('#problems tbody tr').forEach(function(tr){
              const hay = tr.getAttribute('data-search') || '';
              tr.style.display = hay.toLowerCase().indexOf(term) !== -1 ? '' : 'none';
            });
          });
        })();
        </script>
        '''

        header_sub = []
        if stats.get('start_time'):
            header_sub.append(f'Start: {esc(str(stats["start_time"]))}')
        if stats.get('end_time'):
            header_sub.append(f'End: {esc(str(stats["end_time"]))}')
        header_html = f'''
        <h1>{esc(page_title)}</h1>
        <div class="sub">{' • '.join(header_sub)}</div>
        '''

        html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{esc(page_title)}</title>
<style>{styles}</style>
</head>
<body>
  <div class="container">
    {header_html}
    {cards_html}
    {toolbar_html}
    {table_html}
    {raw_data_html}
  </div>
  {script}
</body>
</html>'''
        return html

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
        with summary_path.open('r', encoding='utf-8') as f:
            summary_data = json.load(f)

        results_data = None
        if results_file:
            rf = Path(results_file)
            if not rf.exists():
                raise FileNotFoundError(
                    f'Results file not found: {results_file}')
            with rf.open('r', encoding='utf-8') as f:
                results_data = json.load(f)

        results_list = self._infer_results_list(summary_data, results_data)

        viz_map: Dict[str, str] = {}
        if visualizations_dir:
            vdir = Path(visualizations_dir)
            if vdir.exists() and vdir.is_dir():
                all_html = []
                try:
                    all_html = list(vdir.rglob('*.html'))
                except Exception:
                    pass
                stem_map: Dict[str, Path] = {}
                for p in all_html:
                    key = p.stem.lower()
                    stem_map[key] = p
                    if p.name.lower() == 'index.html' and p.parent != vdir:
                        stem_map[p.parent.name.lower()] = p
                # Build IDs for mapping
                for r in results_list:
                    candidates = []
                    pid = r.get('problem_id') or r.get('id') or r.get(
                        'problem') or r.get('task_id') or r.get('task')
                    name = r.get('problem_name') or r.get(
                        'name') or r.get('title')
                    if pid is not None:
                        s_pid = str(pid).lower()
                        candidates.extend([s_pid, self._slug(s_pid)])
                    if name:
                        s_name = str(name).lower()
                        candidates.extend([s_name, self._slug(s_name)])
                    link_path: Optional[Path] = None
                    for cand in candidates:
                        if cand in stem_map:
                            link_path = stem_map[cand]
                            break
                    if link_path:
                        viz_map[str(pid) if pid is not None else (self._slug(name) if name else link_path.stem)] = self._rel_link(
                            link_path, base_dir=(Path(output_file).parent if output_file else self.output_dir))
            else:
                pass  # silently ignore missing dir

        title = summary_data.get('title') or summary_data.get(
            'benchmark_name') or 'Benchmark Summary'
        html = self.generate_summary_html(
            summary_data, results_list, viz_map, title=title)

        if output_file:
            out_path = Path(output_file)
            out_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_title = self._slug(str(title)) or 'benchmark'
            out_path = self.output_dir / f'{safe_title}_{ts}.html'
        out_path.write_text(html, encoding='utf-8')
        return str(out_path)
