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
        for smell in smells:
            print("%s:%s %s (%s)" % (smell['lines'], smell['name'], smell['message'], smell['smell_type']))
