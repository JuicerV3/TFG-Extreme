#!/usr/bin/env python3
"""Validate Thai localization invariants; never translate or rewrite prose."""

import argparse
import json
import re
import sys
from pathlib import Path


CONTROL_TOKEN = re.compile(
    r"%\d*\$?[sdif]|\$\([^)]*\)|\{[^{}]+\}|\\n|\n|[§&][0-9a-fk-or]"
)
PATCHOULI_LINK = re.compile(r"\$\(l:([^)]*)\)")


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def tokens(value: str):
    return sorted(CONTROL_TOKEN.findall(value))


def link_targets(value: str):
    return PATCHOULI_LINK.findall(value)


def occurrences(value: str, name: str):
    return len(re.findall(r"(?<!\w)" + re.escape(name) + r"(?!\w)", value))


def validate_pair(source: dict, translated: dict, canonical: list[str], allow_source_superset=False):
    errors = []
    if not allow_source_superset and set(source) != set(translated):
        missing = sorted(set(source) - set(translated))
        extra = sorted(set(translated) - set(source))
        if missing:
            errors.append(f"missing keys: {', '.join(missing[:8])}")
        if extra:
            errors.append(f"extra keys: {', '.join(extra[:8])}")

    for key in sorted(set(source) & set(translated)):
        source_value = source[key]
        translated_value = translated[key]
        if not isinstance(source_value, str) or not isinstance(translated_value, str):
            errors.append(f"{key}: values must be strings")
            continue
        if tokens(source_value) != tokens(translated_value):
            errors.append(
                f"{key}: control tokens differ: {tokens(source_value)} != {tokens(translated_value)}"
            )
        if link_targets(source_value) != link_targets(translated_value):
            errors.append(
                f"{key}: Patchouli link targets differ: "
                f"{link_targets(source_value)} != {link_targets(translated_value)}"
            )
        for name in canonical:
            source_count = occurrences(source_value, name)
            translated_count = occurrences(translated_value, name)
            if source_count and translated_count < source_count:
                errors.append(
                    f"{key}: canonical name was dropped: {name} "
                    f"({source_count} source occurrence(s), {translated_count} translated)"
                )
    return errors


def validate_manifest(manifest: dict):
    errors = []
    required = {
        "locale",
        "sources",
        "quest_keys",
        "field_guide_entries",
        "ftbquests_ui_keys",
        "canonical_names",
        "prefix_acceptance_cases",
    }
    errors.extend(f"manifest missing field: {field}" for field in sorted(required - set(manifest)))
    names = manifest.get("canonical_names", [])
    for index, name in enumerate(names):
        if not isinstance(name, str) or not name:
            errors.append(f"canonical_names[{index}] is not a non-empty string")
    if len(names) != len(set(names)):
        errors.append("canonical_names contains duplicates")
    return errors


def validate_tree(source, translated, canonical, path="$", errors=None):
    """Compare nested Patchouli JSON without judging translated prose."""
    errors = [] if errors is None else errors
    if type(source) is not type(translated):
        errors.append(f"{path}: JSON types differ")
        return errors
    if isinstance(source, dict):
        if set(source) != set(translated):
            errors.append(f"{path}: JSON keys differ")
            return errors
        for key in source:
            validate_tree(source[key], translated[key], canonical, f"{path}.{key}", errors)
    elif isinstance(source, list):
        if len(source) != len(translated):
            errors.append(f"{path}: array lengths differ")
            return errors
        for index, (source_item, translated_item) in enumerate(zip(source, translated)):
            validate_tree(source_item, translated_item, canonical, f"{path}[{index}]", errors)
    elif isinstance(source, str):
        if tokens(source) != tokens(translated):
            errors.append(f"{path}: control tokens differ")
        if link_targets(source) != link_targets(translated):
            errors.append(f"{path}: Patchouli link targets differ")
        for name in canonical:
            source_count = occurrences(source, name)
            if source_count and occurrences(translated, name) < source_count:
                errors.append(f"{path}: canonical name was dropped: {name}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--translated", type=Path)
    parser.add_argument("--expected-field", choices=("quest_keys", "ftbquests_ui_keys"))
    parser.add_argument(
        "--allow-source-superset",
        action="store_true",
        help="Allow a partial locale file while validating its translated keys",
    )
    parser.add_argument("--patchouli-source", type=Path, action="append")
    parser.add_argument("--patchouli-translated", type=Path, action="append")
    args = parser.parse_args()

    manifest = load_json(args.manifest)
    errors = validate_manifest(manifest)
    if bool(args.source) != bool(args.translated):
        errors.append("--source and --translated must be provided together")
    if args.source and args.translated:
        source = load_json(args.source)
        translated = load_json(args.translated)
        if args.expected_field:
            expected = set(manifest[args.expected_field])
            if set(translated) != expected:
                errors.append(f"translated keys do not match manifest field: {args.expected_field}")
        errors.extend(
            validate_pair(
                source,
                translated,
                manifest["canonical_names"],
                allow_source_superset=args.allow_source_superset,
            )
        )
    patchouli_sources = args.patchouli_source or []
    patchouli_translated = args.patchouli_translated or []
    if len(patchouli_sources) != len(patchouli_translated):
        errors.append("--patchouli-source and --patchouli-translated counts must match")
    else:
        for source_path, translated_path in zip(patchouli_sources, patchouli_translated):
            errors.extend(
                validate_tree(
                    load_json(source_path),
                    load_json(translated_path),
                    manifest["canonical_names"],
                    path=str(translated_path),
                )
            )

    if errors:
        print("Thai localization validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Thai localization structure is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
