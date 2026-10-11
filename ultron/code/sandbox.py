"""The code world: a sandbox that runs Engc programs.

Engc (github.com/ashutoshavasthi/Engc-V1, pinned to ENGC_COMMIT) compiles structured
English to Python. The sandbox compiles a program, runs it with no files and no
network, and reports only what a scientist would see: what it printed, or that it
failed. Ultron never sees the compiler, its grammar tables or the Python it makes.
"""

import contextlib
import io
import signal

ENGC_COMMIT = "eec6e27dded90304cfcbd155b2e572fbd21e9482"
INSTALL = ("pip install 'engc @ git+https://github.com/ashutoshavasthi/Engc-V1@"
           + ENGC_COMMIT + "'")


class Unavailable(Exception):
    """Engc is not installed here."""


def available():
    try:
        import engc.compiler  # noqa: F401
    except ImportError:
        return False
    return True


class _Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise _Timeout()


def run(source, seconds=5):
    """Run one Engc program. Returns {"ok": bool, "printed": [lines], "error": str|None}."""
    try:
        from engc.compiler import CompileError, compile_source
    except ImportError as e:
        raise Unavailable(f"Engc is not installed ({INSTALL})") from e
    try:
        python = compile_source(source)
    except CompileError:
        return {"ok": False, "printed": [], "error": "does not compile"}
    out = io.StringIO()
    env = {"__name__": "__main__", "__builtins__": __builtins__}
    old = None
    try:
        old = signal.signal(signal.SIGALRM, _alarm)
        signal.setitimer(signal.ITIMER_REAL, seconds)
    except (ValueError, AttributeError):     # not the main thread, or no alarms here
        old = None
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            exec(compile(python, "<engc>", "exec"), env)
        ok, error = True, None
    except _Timeout:
        ok, error = False, "ran too long"
    except SystemExit:
        ok, error = False, "failed"
    except Exception:  # noqa: BLE001 - whatever the program did, it failed
        ok, error = False, "failed"
    finally:
        if old is not None:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, old)
    printed = out.getvalue().splitlines()
    if not ok:
        printed = []
    return {"ok": ok, "printed": printed, "error": error}

