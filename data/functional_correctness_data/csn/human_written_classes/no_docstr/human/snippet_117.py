import yaml
import sys
import codecs

class YAMLHighlight:

    def __init__(self, options):
        config = yaml.full_load(file(options.config, 'rb').read())
        self.style = config[options.style]
        if options.input:
            self.input = file(options.input, 'rb')
        else:
            self.input = sys.stdin
        if options.output:
            self.output = file(options.output, 'wb')
        else:
            self.output = sys.stdout

    def highlight(self):
        input = self.input.read()
        if input.startswith(codecs.BOM_UTF16_LE):
            input = unicode(input, 'utf-16-le')
        elif input.startswith(codecs.BOM_UTF16_BE):
            input = unicode(input, 'utf-16-be')
        else:
            input = unicode(input, 'utf-8')
        substitutions = self.style.substitutions
        tokens = yaml.scan(input)
        events = yaml.parse(input)
        markers = []
        number = 0
        for token in tokens:
            number += 1
            if token.start_mark.index != token.end_mark.index:
                cls = token.__class__
                if (cls, -1) in substitutions:
                    markers.append([token.start_mark.index, +2, number, substitutions[cls, -1]])
                if (cls, +1) in substitutions:
                    markers.append([token.end_mark.index, -2, number, substitutions[cls, +1]])
        number = 0
        for event in events:
            number += 1
            cls = event.__class__
            if (cls, -1) in substitutions:
                markers.append([event.start_mark.index, +1, number, substitutions[cls, -1]])
            if (cls, +1) in substitutions:
                markers.append([event.end_mark.index, -1, number, substitutions[cls, +1]])
        markers.sort()
        markers.reverse()
        chunks = []
        position = len(input)
        for index, weight1, weight2, substitution in markers:
            if index < position:
                chunk = input[index:position]
                for substring, replacement in self.style.replaces:
                    chunk = chunk.replace(substring, replacement)
                chunks.append(chunk)
                position = index
            chunks.append(substitution)
        chunks.reverse()
        result = u''.join(chunks)
        if self.style.header:
            self.output.write(self.style.header)
        self.output.write(result.encode('utf-8'))
        if self.style.footer:
            self.output.write(self.style.footer)