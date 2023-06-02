import logging
import os
import shutil
import sys
import subprocess

import sublime
import sublime_plugin

STATUS_KEY = "charpier"

log = logging.getLogger("csharpier")


def is_csharp(view):
    return view.match_selector(0, "source.cs")


class CsharpierCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return is_csharp(self.view)

    is_visible = is_enabled

    def format(self, edit):
        filename = self.view.file_name()
        cmd = shutil.which("dotnet-csharpier")
        if cmd is None:
            cmd = os.path.expanduser("~/.dotnet/tools/dotnet-csharpier")
            log.warning("CSharpier: dotnet-csharpier not found on PATH, trying %s", cmd)

        log.info("CSharpier: running %s %s", cmd, filename)
        _, stderr = subprocess.Popen(
            [cmd, filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).communicate()
        stderr = stderr.decode(sys.getdefaultencoding())
        if stderr:
            # a typical error message:
            # Error path/to/File.cs - Failed to compile so was not formatted.
            # (165,13): error CS1002: ; expected
            log.error("CSharpier: error from subprocess")
            log.error("\n" + stderr)
            error = " ".join(stderr.splitlines())

            # compactify the status bar output a bit
            error = error.replace(filename, os.path.basename(filename))
            if error.startswith("Error "):
                error = error[6:]

            self.view.set_status(STATUS_KEY, "CSharpier: " + error)
            sublime.set_timeout(lambda: self.view.erase_status(STATUS_KEY), 10000)
        else:
            self.view.erase_status(STATUS_KEY)

    def run(self, edit):
        self.format(edit)


class CsharpierOnSave(sublime_plugin.ViewEventListener):
    def on_post_save(self):
        settings = sublime.load_settings("CSharpier.sublime-settings")
        if settings.get("format_on_save", False):
            self.view.run_command("csharpier")
