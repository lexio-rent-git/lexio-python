"""Génère src/lexio_rent/_resources.py à partir de spec/openapi.json.

Usage : python scripts/generate.py
Chaque opération OpenAPI devient une méthode, rangée par ressource (premier
segment du chemin) : GET /vehicles -> client.vehicles.list(),
POST /rentals/{rentalId}/cancel -> client.rentals.cancel(rental_id, ...).
"""
from __future__ import annotations

import json
import keyword
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEC = json.loads((ROOT / "spec" / "openapi.json").read_text(encoding="utf-8"))
OUT = ROOT / "src" / "lexio_rent" / "_resources.py"
METHODS = ("get", "post", "put", "patch", "delete")


def snake(name: str) -> str:
    s = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", name).replace("-", "_")
    s = s.lower()
    return s + "_" if keyword.iskeyword(s) else s


def deref(obj):
    if isinstance(obj, dict) and "$ref" in obj:
        node = SPEC
        for part in obj["$ref"].lstrip("#/").split("/"):
            node = node[part]
        return node
    return obj


def singular(tok: str) -> str:
    if tok.endswith("ies"):
        return tok[:-3] + "y"
    return tok[:-1] if tok.endswith("s") and not tok.endswith("ss") else tok


def method_name(op_id: str, resource: str) -> str:
    toks = snake(op_id).split("_")
    res = resource.split("-")
    variants = [res, [singular(t) for t in res], res[:-1] + [singular(res[-1])]]
    for v in variants:
        n = len(v)
        for i in range(1, len(toks) - n + 1):
            if toks[i : i + n] == v:
                return _safe("_".join(toks[:i] + toks[i + n :]))
    return _safe("_".join(toks))


def _safe(name: str) -> str:
    return name + "_" if keyword.iskeyword(name) else name


def class_name(resource: str) -> str:
    return "".join(p.capitalize() for p in resource.split("-")) + "Resource"


def one_line(text: str | None) -> str:
    return " ".join((text or "").split()).replace('"""', "'''")


resources: dict[str, list[str]] = {}
seen: dict[str, set[str]] = {}

for path, ops in SPEC["paths"].items():
    resource = path.strip("/").split("/")[0]
    path_level = [deref(p) for p in ops.get("parameters", [])]
    for http, op in ops.items():
        if http not in METHODS:
            continue
        name = method_name(op["operationId"], resource)
        if name in seen.setdefault(resource, set()):
            raise SystemExit(f"collision {resource}.{name}")
        seen[resource].add(name)

        params = path_level + [deref(p) for p in op.get("parameters", [])]
        path_params = [p for p in params if p["in"] == "path"]
        query_params = [p for p in params if p["in"] == "query"]
        idem = next((p for p in params if p["in"] == "header" and p["name"] == "Idempotency-Key"), None)
        has_body = "requestBody" in op
        body_required = has_body and op["requestBody"].get("required", False)

        sig = ["self"]
        for p in path_params:
            sig.append(f"{snake(p['name'])}: str")
        if has_body and body_required:
            sig.append("body: Mapping[str, Any]")
        kw = []
        if has_body and not body_required:
            kw.append("body: Mapping[str, Any] | None = None")
        for p in query_params:
            kw.append(f"{snake(p['name'])}: Any = None")
        if idem is not None:
            kw.append("idempotency_key: str | None = None")
        if kw:
            sig.append("*")
            sig.extend(kw)

        fmt_path = re.sub(r"\{(\w+)\}", lambda m: "{" + snake(m.group(1)) + "}", path)
        query_map = ", ".join(f'"{p["name"]}": {snake(p["name"])}' for p in query_params)
        summary = one_line(op.get("summary")) or op["operationId"]
        desc = one_line(op.get("description"))
        doc = f'"""{summary}.\n\n        ``{http.upper()} {path}`` (operationId ``{op["operationId"]}``).'
        if desc:
            doc += f"\n\n        {desc[:600]}"
        if query_params:
            doc += "\n\n        Paramètres de requête : " + ", ".join(
                f"``{snake(p['name'])}`` → ``{p['name']}``" for p in query_params
            ) + "."
        if idem is not None:
            req = "obligatoire côté API, générée automatiquement si absente" if idem.get("required") else "facultative"
            doc += f"\n\n        ``Idempotency-Key`` : {req}."
        doc += '\n        """'

        lines = [f"    def {name}({', '.join(sig)}) -> Any:", f"        {doc}"]
        call = [f'"{http.upper()}"', f'f"{fmt_path}"' if "{" in fmt_path else f'"{fmt_path}"']
        if query_params:
            call.append(f"params={{{query_map}}}")
        if has_body:
            call.append("json=body")
        if idem is not None:
            call.append("idempotency_key=idempotency_key")
            call.append(f"idempotency_required={bool(idem.get('required'))}")
        lines.append(f"        return self._client.request({', '.join(call)})")
        resources.setdefault(resource, []).append("\n".join(lines))

out = [
    '"""Ressources de l\'API Lexio Rent — FICHIER GÉNÉRÉ par scripts/generate.py, ne pas éditer."""',
    "from __future__ import annotations",
    "",
    "from typing import TYPE_CHECKING, Any, Mapping",
    "",
    "if TYPE_CHECKING:",
    "    from ._client import Lexio",
    "",
    f'SPEC_VERSION = "{SPEC["info"]["version"]}"',
    "",
]
attrs = []
for resource, methods in resources.items():
    cls = class_name(resource)
    out.append("")
    out.append(f"class {cls}:")
    out.append(f'    """Opérations sur ``/{resource}``."""')
    out.append("")
    out.append('    def __init__(self, client: "Lexio") -> None:')
    out.append("        self._client = client")
    for m in methods:
        out.append("")
        out.append(m)
    out.append("")
    attrs.append((snake(resource), cls))

out.append("")
out.append("RESOURCES = {")
for attr, cls in attrs:
    out.append(f'    "{attr}": {cls},')
out.append("}")
OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"{OUT.relative_to(ROOT)} : {sum(len(v) for v in resources.values())} opérations, {len(resources)} ressources")
for attr, cls in attrs:
    print(" ", attr, sorted(seen[attr.replace('_', '-')] if attr.replace('_', '-') in seen else seen[attr]))
