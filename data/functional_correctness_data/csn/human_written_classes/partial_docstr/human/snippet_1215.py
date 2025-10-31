class SphinxDocstring:
    """
    Helper to parse and modify sphinx docstrings
    """

    def __init__(docstr, lines):
        docstr.lines = lines
        import re
        tag_pat = re.compile('^:(\\w*):')
        directive_pat = re.compile('^.. (\\w*)::\\s*(\\w*)')
        sphinx_parts = []
        for idx, line in enumerate(lines):
            tag_match = tag_pat.search(line)
            directive_match = directive_pat.search(line)
            if tag_match:
                tag = tag_match.groups()[0]
                sphinx_parts.append({'tag': tag, 'start_offset': idx, 'type': 'tag'})
            elif directive_match:
                tag = directive_match.groups()[0]
                sphinx_parts.append({'tag': tag, 'start_offset': idx, 'type': 'directive'})
        prev_offset = len(lines)
        for part in sphinx_parts[::-1]:
            part['end_offset'] = prev_offset
            prev_offset = part['start_offset']
        docstr.sphinx_parts = sphinx_parts
        if 0:
            for line in lines:
                print(line)

    def find_tagged_lines(docstr, tag):
        for part in docstr.sphinx_parts[::-1]:
            if part['tag'] == tag:
                edit_slice = slice(part['start_offset'], part['end_offset'])
                return_section = docstr.lines[edit_slice]
                text = '\n'.join(return_section)
                found = {'edit_slice': edit_slice, 'text': text}
                yield found