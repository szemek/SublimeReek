import os
import sublime
import sublime_plugin
import subprocess
import string
import re
import json

class SublimeReek(sublime_plugin.EventListener):
    """The main ST3 plugin class."""

    def __init__(self, *args, **kwargs):
        """Initialize a new instance."""
        super().__init__(*args, **kwargs)

    def on_post_save_async(self, view):
        """Called after view is saved."""

        filename = view.file_name()
        if re.match(r".*(\.rb)$", filename) == None:
            return

        command = string.Template('reek --format json $filename').substitute(filename=filename)

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ)
        output, errors = process.communicate()
        smells = json.loads(output.decode('ascii'))

        self.clear_regions(view)

        print('Reek:')
        for smell in smells:
            lines = smell['lines']
            context = smell['context']
            message = smell['message']
            smell_type = smell['smell_type']
            print("%s:%s %s (%s)" % (lines, context, message, smell_type))

            for line in lines:
                self.mark_line(view, line)

    def mark_line(self, view, line):
        scope = 'variable.parameter'
        point = view.text_point(int(line) - 1, 0)
        region = view.full_line(point)
        view.add_regions('line_%s' % line, [region], scope, 'dot', sublime.HIDDEN | sublime.PERSISTENT)

    def clear_regions(self, view):
        lines, _ = view.rowcol(view.size())
        for line in range(lines):
            view.erase_regions('line_%s' % (line + 1))
