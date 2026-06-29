"""Dependency-free TOML read/write for the configuration subset we use.

Reading prefers the standard-library ``tomllib`` (Python 3.11+), then ``tomli``
if installed, and finally a small fallback parser that understands the constrained
subset this project emits (tables, strings, integers, floats, booleans, and
single-line arrays of scalars). Writing always uses the local serializer, so the
package needs no third-party TOML dependency.

The fallback parser is intentionally small. On Python 3.11+ the robust standard
library handles arbitrary user-edited files; the fallback only has to round-trip
what :func:`dumps` produces.
"""

from __future__ import annotations

from typing import Any

__all__ = ["loads", "dumps", "load", "save"]


# --------------------------------------------------------------------------- #
# Reading
# --------------------------------------------------------------------------- #
def loads(text: str) -> dict[str, Any]:
    """Parse a TOML string into a nested dict."""
    try:
        import tomllib  # Python 3.11+

        return tomllib.loads(text)
    except ModuleNotFoundError:
        pass
    try:
        import tomli  # backport for < 3.11

        return tomli.loads(text)
    except ModuleNotFoundError:
        return _fallback_loads(text)


def load(path: str) -> dict[str, Any]:
    """Read and parse a TOML file at ``path``."""
    with open(path, encoding="utf-8") as handle:
        return loads(handle.read())


def _fallback_loads(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    current = root
    for raw_line in text.splitlines():
        line = _strip_comment(raw_line).strip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            current = _descend(root, line[1:-1].strip())
            continue
        if "=" not in line:
            raise ValueError(f"Malformed TOML line: {raw_line!r}")
        key, _, value = line.partition("=")
        current[key.strip()] = _parse_value(value.strip())
    return root


def _descend(root: dict[str, Any], dotted: str) -> dict[str, Any]:
    node = root
    for part in (p.strip() for p in dotted.split(".")):
        node = node.setdefault(part, {})
        if not isinstance(node, dict):
            raise ValueError(f"Table path collides with a value: {dotted!r}")
    return node


def _strip_comment(line: str) -> str:
    out: list[str] = []
    in_string = False
    quote = ""
    for char in line:
        if in_string:
            out.append(char)
            if char == quote:
                in_string = False
        elif char in ('"', "'"):
            in_string = True
            quote = char
            out.append(char)
        elif char == "#":
            break
        else:
            out.append(char)
    return "".join(out)


def _parse_value(token: str) -> Any:
    if token.startswith("[") and token.endswith("]"):
        inner = token[1:-1].strip()
        if not inner:
            return []
        return [_parse_value(item.strip()) for item in _split_array(inner)]
    if (token.startswith('"') and token.endswith('"')) or (
        token.startswith("'") and token.endswith("'")
    ):
        return token[1:-1]
    if token in ("true", "false"):
        return token == "true"
    try:
        return int(token)
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        pass
    raise ValueError(f"Unsupported TOML value: {token!r}")


def _split_array(inner: str) -> list[str]:
    items: list[str] = []
    buf: list[str] = []
    depth = 0
    in_string = False
    quote = ""
    for char in inner:
        if in_string:
            buf.append(char)
            if char == quote:
                in_string = False
        elif char in ('"', "'"):
            in_string = True
            quote = char
            buf.append(char)
        elif char in "[":
            depth += 1
            buf.append(char)
        elif char in "]":
            depth -= 1
            buf.append(char)
        elif char == "," and depth == 0:
            items.append("".join(buf))
            buf = []
        else:
            buf.append(char)
    if buf:
        items.append("".join(buf))
    return items


# --------------------------------------------------------------------------- #
# Writing
# --------------------------------------------------------------------------- #
def dumps(data: dict[str, Any], *, header: str | None = None) -> str:
    """Serialize a nested dict to TOML.

    Top-level scalars are emitted first, then one table per nested dict. Values
    may be ``str``, ``bool``, ``int``, ``float``, or a list of those scalars.
    """
    lines: list[str] = []
    if header:
        lines.extend(f"# {h}" for h in header.splitlines())
        lines.append("")

    scalars = {k: v for k, v in data.items() if not isinstance(v, dict)}
    tables = {k: v for k, v in data.items() if isinstance(v, dict)}

    for key, value in scalars.items():
        lines.append(f"{key} = {_format(value)}")
    if scalars and tables:
        lines.append("")

    for index, (name, table) in enumerate(tables.items()):
        if index:
            lines.append("")
        lines.append(f"[{name}]")
        for key, value in table.items():
            lines.append(f"{key} = {_format(value)}")

    return "\n".join(lines) + "\n"


def save(path: str, data: dict[str, Any], *, header: str | None = None) -> None:
    """Serialize ``data`` and write it to ``path``."""
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(dumps(data, header=header))


def _format(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return _format_string(value)
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(_format(item) for item in value) + "]"
    raise TypeError(f"Cannot serialize value of type {type(value).__name__}: {value!r}")


def _format_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'
