from pathlib import Path
from khive.core import TimePolicy
from typing import Any
import re

class DiaryWritingAssistant:
    """Assistant for manual diary writing process"""

    def __init__(self, dry_run: bool=False, target_date: str | None=None):
        self.dry_run = dry_run
        self.target_date = target_date
        self.summaries_dir = Path('.khive/notes/summaries')
        self.diaries_dir = Path('.khive/notes/diaries')
        self.diaries_dir.mkdir(parents=True, exist_ok=True)

    def find_unprocessed_summaries(self) -> dict[str, list[Path]]:
        """Find summaries that haven't been processed into diaries, grouped by date"""
        summaries_by_date = {}
        if not self.summaries_dir.exists():
            return summaries_by_date
        for summary_file in self.summaries_dir.glob('summary_*.md'):
            try:
                content = summary_file.read_text()
                if 'processed: true' in content and (not self.dry_run):
                    continue
                match = re.search('summary_(\\d{8})_\\d{6}\\.md', summary_file.name)
                if match:
                    date_str = match.group(1)
                    formatted_date = f'{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}'
                    if self.target_date and formatted_date != self.target_date:
                        continue
                    if formatted_date not in summaries_by_date:
                        summaries_by_date[formatted_date] = []
                    summaries_by_date[formatted_date].append(summary_file)
            except Exception as e:
                print(f'{RED}Error reading {summary_file}: {e}{RESET}')
        for date in summaries_by_date:
            summaries_by_date[date].sort(key=lambda p: p.stat().st_mtime)
        return summaries_by_date

    def extract_summary_overview(self, summary_path: Path) -> dict[str, Any]:
        """Extract basic overview from a conversation summary for context"""
        content = summary_path.read_text()
        overview = {'main_topic': 'Unknown', 'duration': 'Unknown', 'key_points': [], 'file_path': str(summary_path)}
        match = re.search('main_topic:\\s*(.+)', content)
        if match:
            overview['main_topic'] = match.group(1).strip()
        match = re.search('duration:\\s*(.+)', content)
        if match:
            overview['duration'] = match.group(1).strip()
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(('- ', '* ')) and len(line) > 10:
                point = line[2:].strip()
                if len(point) < 100:
                    overview['key_points'].append(point)
                    if len(overview['key_points']) >= 3:
                        break
        return overview

    def prompt_diary_writing(self, date: str, summaries: list[Path], existing_diary: Path | None=None) -> str:
        """Streamlined diary writing prompt"""
        diary_file = self.diaries_dir / f"diary_{date.replace('-', '')}.md"
        action_type = 'Appending to' if existing_diary else 'Writing New'
        print(f'\n📔 {action_type} Diary Entry for {date}')
        print(f'Sessions: {len(summaries)} to process')
        print()
        print('Session Context:')
        for i, summary_path in enumerate(summaries, 1):
            overview = self.extract_summary_overview(summary_path)
            topic = overview['main_topic'][:50] + '...' if len(overview['main_topic']) > 50 else overview['main_topic']
            print(f"  {i}. {topic} ({overview['duration']})")
        print()
        print('🎯 Diary Writing Task:')
        if existing_diary:
            print(f'1. Read existing diary: {existing_diary}')
            print('2. Use Edit tool to append reflections on new sessions above')
        else:
            print(f'1. Write new diary: {diary_file}')
        print("2. Focus on: orchestration learnings, Ocean's guidance, technical insights")
        print('3. Target: 100-200 lines of honest reflection')
        print('4. Run this command again to mark summaries as processed')
        return f"diary_{date.replace('-', '')}.md"

    def check_diary_exists(self, date: str) -> Path | None:
        """Check if diary already exists for this date, return path if exists"""
        diary_file = self.diaries_dir / f"diary_{date.replace('-', '')}.md"
        return diary_file if diary_file.exists() else None

    def mark_summaries_processed(self, summaries: list[Path]) -> None:
        """Mark summaries as processed by adding processed: true flag"""
        for summary_path in summaries:
            try:
                content = summary_path.read_text()
                if 'processed: true' not in content:
                    content += f'\n\n---\nprocessed: true\nprocessed_date: {TimePolicy.now_utc().isoformat()}\n'
                    if not self.dry_run:
                        summary_path.write_text(content)
                        print(f'  {GREEN}✓ Marked {summary_path.name} as processed{RESET}')
                    else:
                        print(f'  {YELLOW}[DRY RUN] Would mark {summary_path.name} as processed{RESET}')
            except Exception as e:
                print(f'  {RED}✗ Error marking {summary_path.name}: {e}{RESET}')

    def process_diaries(self):
        """Main process for diary writing assistance"""
        print(f'{BOLD}📔 Diary Writing Assistant{RESET}')
        print(f'{CYAN}Helping you write thoughtful diary entries...{RESET}')
        print()
        summaries_by_date = self.find_unprocessed_summaries()
        if not summaries_by_date:
            print(f'{GREEN}✓ No unprocessed summaries found.{RESET}')
            return
        print(f'{BOLD}{YELLOW}Found {sum((len(s) for s in summaries_by_date.values()))} unprocessed summaries across {len(summaries_by_date)} dates{RESET}')
        for date in sorted(summaries_by_date.keys()):
            summaries = summaries_by_date[date]
            existing_diary = self.check_diary_exists(date)
            if existing_diary and (not summaries):
                print(f'\n{GREEN}✓ Diary for {date} already complete{RESET}')
                continue
            if existing_diary:
                print(f'\n{YELLOW}📔 Diary for {date} exists, but {len(summaries)} new summaries need to be added{RESET}')
                self.prompt_diary_writing(date, summaries, existing_diary)
            else:
                self.prompt_diary_writing(date, summaries)
            if self.check_diary_exists(date):
                print(f'\n{GREEN}✓ Diary for {date} found!{RESET}')
                print(f'  Marking {len(summaries)} summaries as processed...')
                self.mark_summaries_processed(summaries)
            else:
                print(f'\n{YELLOW}⏸  Waiting for diary to be written for {date}{RESET}')
                print('  Summaries remain unprocessed until diary is created.')
                break
        print(f'\n{GREEN}✓ Diary processing session complete!{RESET}')