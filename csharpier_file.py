import logging
import os
import shutil
import sys
import subprocess

import sublime  # type: ignore
import sublime_plugin  # type: ignore

STATUS_KEY = "csharpier"


def init_logger():
    global logger
    logger = logging.getLogger("csharpier")

    if not logger.hasHandlers():
        # Configure log level
        settings = sublime.load_settings("CSharpier.sublime-settings")
        log_level = settings.get("log_level", "WARNING").upper()
        logger.setLevel(getattr(logging, log_level, logging.WARNING))

        # Configure log format
        log_format = settings.get(
            "log_format", "%(name)s (%(levelname)s): %(message)s")
        formatter = logging.Formatter(log_format)

        # Add console handler with the specified format
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


logger = init_logger()


def is_csharp(view):
    return view.match_selector(0, "source.cs")


class CsharpierCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return is_csharp(self.view)

    is_visible = is_enabled

    def format(self, edit):
        filename = self.view.file_name()
        logger.info("Formatting: %s", filename)
        if not filename:
            logger.error("Cannot format unsaved file")
            self.view.set_status(STATUS_KEY, "Cannot format unsaved file")
            self.clear_status_with_delay()
            return

        settings = sublime.load_settings("CSharpier.sublime-settings")
        cmd = settings.get("csharpier_path", None)
        if cmd:
            cmd = os.path.expanduser(cmd)
            logger.info("Using csharpier_path setting: %s", cmd)

        if not cmd:
            cmd = shutil.which("dotnet-csharpier")
            if cmd is None:
                cmd = os.path.expanduser("~/.dotnet/tools/dotnet-csharpier")
                logger.warning(
                    "which dotnet-csharpier did not resolve a path, trying: %s", cmd)

        logger.info("Running '%s' on '%s'", cmd, filename)
        _, stderr = subprocess.Popen(
            [cmd, filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        stderr = stderr.decode(sys.getdefaultencoding())
        if stderr:
            # a typical error message:
            # Error path/to/File.cs - Failed to compile so was not formatted.
            # (165,13): error CS1002: ; expected
            logger.error("error from subprocess")
            logger.error("\n" + stderr)
            error = " ".join(stderr.splitlines())

            # compact the status bar output a bit
            error = error.replace(filename, os.path.basename(filename))
            if error.startswith("Error "):
                error = error[6:]

            self.view.set_status(STATUS_KEY, error)
            self.clear_status_with_delay()
        else:
            self.view.erase_status(STATUS_KEY)

    def clear_status_with_delay(self):
        sublime.set_timeout(lambda: self.view.erase_status(STATUS_KEY), 10000)

    def run(self, edit):
        self.format(edit)


class CsharpierOnSave(sublime_plugin.ViewEventListener):
    def on_post_save(self):
        settings = sublime.load_settings("CSharpier.sublime-settings")
        if settings.get("format_on_save", False):
            self.view.run_command("csharpier")
