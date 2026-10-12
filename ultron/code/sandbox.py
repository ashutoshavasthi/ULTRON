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


def _plain(v, depth=0):
    """A value as a scientist would write it down, or None if it isn't plain data."""
    if isinstance(v, (bool, int, float, str)) or v is None:
        return v
    if depth < 3 and isinstance(v, (list, tuple)) and len(v) <= 200:
        out = [_plain(x, depth + 1) for x in v]
        return None if any(x is None and y is not None for x, y in zip(out, v)) else out
    return None


def trace(source, seconds=5, max_steps=20000):
    """Run one Engc program and film it: before each line of the Engc program runs,
    which line it is, how deep in routine calls, the plain values of every name, and
    how many lines have been printed so far; and the names' values when it ends.
    Returns run()'s result plus "steps" and "final"."""
    import sys
    try:
        from engc.compiler import CompileError, compile_source
    except ImportError as e:
        raise Unavailable(f"Engc is not installed ({INSTALL})") from e
    try:
        python = compile_source(source)
    except CompileError:
        return {"ok": False, "printed": [], "error": "does not compile", "steps": []}
    out = io.StringIO()
    env = {"__name__": "__main__", "__builtins__": __builtins__}
    steps = []
    final = {}

    class _TooLong(Exception):
        pass

    def tracer(frame, event, arg):
        if frame.f_code.co_filename != "<engc>" or frame.f_code.co_name == "<module>":
            return None
        if event == "return" and frame.f_code.co_name == "main":
            final.update({k: _plain(v) for k, v in frame.f_locals.items()
                          if not k.startswith("_") and (_plain(v) is not None or v is None)})
        if event == "line":
            line = env.get("_ENG_LINE_MAP", {}).get(frame.f_lineno)
            if line is not None:
                if len(steps) >= max_steps:
                    raise _TooLong()
                depth, f = 0, frame.f_back
                while f is not None:
                    depth += f.f_code.co_filename == "<engc>" and f.f_code.co_name != "<module>"
                    f = f.f_back
                memory = {}
                for k, v in frame.f_locals.items():
                    if not k.startswith("_"):
                        p = _plain(v)
                        if p is not None or v is None:
                            memory[k] = p
                steps.append({"line": line, "depth": depth, "memory": memory,
                              "printed": out.getvalue().count("\n")})
        return tracer

    old = None
    try:
        old = signal.signal(signal.SIGALRM, _alarm)
        signal.setitimer(signal.ITIMER_REAL, seconds)
    except (ValueError, AttributeError):
        old = None
    before = sys.gettrace()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            sys.settrace(tracer)
            try:
                exec(compile(python, "<engc>", "exec"), env)
            finally:
                sys.settrace(before)
        ok, error = True, None
    except (_Timeout, _TooLong):
        ok, error = False, "ran too long"
    except SystemExit:
        ok, error = False, "failed"
    except Exception:  # noqa: BLE001
        ok, error = False, "failed"
    finally:
        if old is not None:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, old)
    printed = out.getvalue().splitlines()
    return {"ok": ok, "printed": printed if ok else [], "error": error, "steps": steps,
            "final": final if ok else None}
