import os
import subprocess
import shutil

import sublime
import sublime_plugin

DEFAULT_FORMAT_ON_SAVE = False


def is_csharp(view):
    return view.match_selector(0, "source.cs")


class CsharpierCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return is_csharp(self.view)

    is_visible = is_enabled

    def format(self, edit):
        cmd = shutil.which("dotnet-csharpier")
        if cmd is None:
            cmd = os.path.expanduser("~/.dotnet/tools/dotnet-csharpier")
            print("dotnet-csharpier not found on PATH, trying " + cmd)

        print("running " + cmd + " " + self.view.file_name())
        subprocess.check_call([cmd, self.view.file_name()])

    def run(self, edit):
        self.format(edit)


class CsharpierOnSave(sublime_plugin.ViewEventListener):
    def on_post_save(self):
        settings = self.view.settings() or {}
        format_on_save = settings.get("csharpier.format_on_save")
        if format_on_save is None:
            format_on_save = DEFAULT_FORMAT_ON_SAVE
        if format_on_save:
            self.view.run_command("csharpier")
