import sys
import mistletoe
from mistletoe.contrib.jira_renderer import JiraRenderer

class MarkdownToJira:

    def __init__(self):
        self.version = '1.0.2'
        self.options = {}
        self.options['output'] = '-'

    def run(self, optlist, args):
        for o, i in optlist:
            if o in ('-h', '--help'):
                sys.stderr.write(usageString + '\n')
                sys.stderr.write(helpString + '\n')
                sys.exit(1)
            elif o in ('-v', '--version'):
                sys.stdout.write('%s\n' % self.version)
                sys.exit(0)
            elif o in ('-o', '--output'):
                self.options['output'] = i
        if len(args) < 1:
            sys.stderr.write(usageString + '\n')
            sys.exit(1)
        with open(args[0], 'r', encoding='utf-8') if len(args) == 1 else sys.stdin as infile:
            rendered = mistletoe.markdown(infile, JiraRenderer)
        if self.options['output'] == '-':
            sys.stdout.write(rendered)
        else:
            with open(self.options['output'], 'w', encoding='utf-8') as outfile:
                outfile.write(rendered)