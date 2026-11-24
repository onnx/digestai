# Copyright (c) ONNX Project Contributors
# SPDX-License-Identifier: Apache-2.0

"""Bounded diagnostic logging for GUI launches, including windowed executables."""

import atexit
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
import threading

from platformdirs import user_log_dir


def log_path():
    return Path(user_log_dir("digest")) / "digest.log"


class DiagnosticFileHandler(RotatingFileHandler):
    def handleError(self, record):  # noqa: ARG002 -- logging's handler interface
        # Avoid recursively logging to redirected stderr if the disk fills up.
        if sys.__stderr__ is not None:
            sys.__stderr__.write("Could not write to the Digest diagnostic log.\n")


class LogStream:
    def __init__(self, original, level):
        self.original = original
        self.level = level
        self.pending = ""
        self.lock = threading.RLock()

    @property
    def encoding(self):
        return getattr(self.original, "encoding", "utf-8")

    def isatty(self):
        return bool(self.original and self.original.isatty())

    def write(self, text):
        with self.lock:
            if self.original is not None:
                self.original.write(text)
            self.pending += text
            while "\n" in self.pending:
                line, self.pending = self.pending.split("\n", 1)
                if line.strip():
                    logging.getLogger("digest.console").log(self.level, line)
            # Bound buffering even when a library writes progress without newlines.
            if len(self.pending) >= 8192:
                self.flush()
        return len(text)

    def flush(self):
        with self.lock:
            if self.original is not None:
                self.original.flush()
            if self.pending.strip():
                logging.getLogger("digest.console").log(self.level, self.pending)
            self.pending = ""


def configure_logging():
    logger = logging.getLogger("digest")
    if any(isinstance(handler, RotatingFileHandler) for handler in logger.handlers):
        return
    try:
        path = log_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        handler = DiagnosticFileHandler(path, maxBytes=2 * 1024 * 1024, backupCount=3, encoding="utf-8")
    except OSError as error:
        # A read-only profile should not prevent launching the GUI.
        if sys.stderr is not None:
            sys.stderr.write(f"Could not open Digest diagnostic log: {error}\n")
        return
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stdout = LogStream(sys.stdout, logging.INFO)
    stderr = LogStream(sys.stderr, logging.ERROR)
    sys.stdout, sys.stderr = stdout, stderr
    atexit.register(stdout.flush)
    atexit.register(stderr.flush)

    original_hook = sys.excepthook

    def exception_hook(exc_type, value, traceback):
        logger.error("Unhandled exception", exc_info=(exc_type, value, traceback))
        if stderr.original is not None:
            original_hook(exc_type, value, traceback)

    sys.excepthook = exception_hook

    def thread_exception_hook(args):
        exception_hook(args.exc_type, args.exc_value, args.exc_traceback)

    threading.excepthook = thread_exception_hook
    logger.info("Digest started; diagnostic log: %s", path)
