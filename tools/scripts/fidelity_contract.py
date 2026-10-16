#!/usr/bin/env python3
"""Deterministic checks for the deploy and focused-decision output contracts.

This checks structure and the parts of fidelity a parser can decide: required
rows and sections, evidence identifiers that exist, numbers that appear in the
cited evidence, and scenario-specific states such as an unknown environment or
an execution state. Whether free text contains an unlabeled inference is left to
scripts/fidelity_judge.py.
"""

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXPECTATIONS = ROOT / "tests/behavior/fidelity/expectations.json"
RESOLVED = ROOT / "tests/behavior/fidelity/resolved-evidence.json"

CONTRACTS = {
    "deploy": {
        "lead": "verdict",
        "lead_values": ["no-go", "go", "caution", "incomplete"],
        "header": ["check", "finding", "source"],
        "rows": ["artifact", "base and target", "environment", "mapped services", "review and ci",
                 "pre-production", "rollout safeguards", "incidents", "release policy",
                 "concurrent changes", "staffing"],
        "sections": ["inferences, not evidence", "unresolved checks", "what would change the verdict"],
        "id_sources": True,
        "closing": "I did not deploy, approve, roll back, or notify anyone.",
    },
    "focused": {
        "lead": "answer",
        "lead_values": ["yes", "no", "conditional"],
        "header": ["fact", "state", "source"],
        "rows": ["signal", "corroboration", "approval", "execution", "outcome", "cause", "action risks"],
        "sections": ["rule", "inferences, not evidence", "next check"],
        "id_sources": False,
        "closing": "I did not call Rootly, change any record, or execute anything.",
    },
}
DASHES = {"—", "-", "–", "n/a", "none", ""}
UNKNOWN_VALUES = ("unknown", "not supplied", "unassessed", "unconfirmed", "not confirmed",
                  "not established", "not recorded", "none")
ID = re.compile(r"\b[A-Z]{1,2}\d{1,2}\b")
WORDS = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six",
         "7": "seven", "8": "eight", "9": "nine", "10": "ten", "11": "eleven", "12": "twelve"}


def clean(text):
    text = re.sub(r"[*_`]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def heading(line):
    """Return a normalized section name for a bold or markdown heading line."""
    match = re.fullmatch(r"\s*(?:#{1,6}\s*)?\*{0,2}([^*#]+?)\*{0,2}:?\s*", line)
    if not match or not (line.strip().startswith("**") or line.strip().startswith("#")):
        return None
    return clean(match.group(1)).rstrip(":").lower()


def parse(answer, contract):
    lines = answer.splitlines()
    result = {"lead": None, "lead_index": None, "table": [], "header": None,
              "sections": {}, "order": [], "extra_headings": [], "closing": False, "stray": []}
    lead_pattern = re.compile(r"^\s*\*\*\s*" + contract["lead"] + r"\s*:\s*([A-Za-z-]+)", re.I)
    for index, line in enumerate(lines):
        match = lead_pattern.match(line)
        if match:
            result["lead"], result["lead_index"] = match.group(1).lower(), index
            break
    start = result["lead_index"] + 1 if result["lead_index"] is not None else 0
    current = None
    for line in lines[start:]:
        stripped = line.strip()
        if result["closing"]:
            if stripped:
                result["stray"].append(stripped)
            continue
        if clean(stripped) == contract["closing"]:
            result["closing"] = True
            continue
        if stripped.startswith("|"):
            if current is not None:
                result["stray"].append(stripped)
                continue
            cells = [clean(c) for c in stripped.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            if result["header"] is None:
                result["header"] = [c.lower() for c in cells]
            elif current is None:
                result["table"].append(cells)
            continue
        name = heading(stripped)
        if name is not None:
            if name in contract["sections"]:
                current = name
                result["sections"].setdefault(name, [])
                result["order"].append(name)
            else:
                result["extra_headings"].append(name)
                current = "__extra__"
            continue
        if current and current != "__extra__" and stripped:
            result["sections"][current].append(stripped)
        elif current is None and stripped:
            result["stray"].append(stripped)
    return result


def detected_format(answer):
    """Name the output format an answer used: deploy, focused, or a free-form brief.

    Routing is only consistent if repeats of one question keep one format, so
    this reports the format without judging whether it is the right one.
    """
    tables = [[cell.strip().lower() for cell in clean(line).strip("|").split("|")]
              for line in answer.splitlines() if line.strip().startswith("|")]
    for kind, contract in CONTRACTS.items():
        if any(row == contract["header"] for row in tables):
            return kind
    return "brief"


def facts_by_id(evidence):
    mapping = {}
    for line in evidence.splitlines():
        for identifier in set(ID.findall(line)):
            mapping.setdefault(identifier, []).append(line)
    return mapping


def check(answer, kind, evidence, expected=None):
    """Return a list of violation strings; empty means the contract holds."""
    contract = CONTRACTS[kind]
    parsed = parse(answer, contract)
    violations = []
    if parsed["lead"] not in contract["lead_values"]:
        violations.append(f"lead_missing_or_invalid:{parsed['lead']}")
    elif any(line.strip() for line in answer.splitlines()[:parsed["lead_index"]]):
        violations.append("lead_not_first")
    if parsed["header"] != contract["header"]:
        violations.append(f"table_header:{parsed['header']}")
    rows = {}
    names = []
    for cells in parsed["table"]:
        if len(cells) != 3:
            violations.append(f"row_shape:{cells[:1]}")
            continue
        name = cells[0].lower()
        names.append(name)
        rows[name] = {"value": cells[1], "source": cells[2]}
    if names != contract["rows"]:
        violations.append(f"rows:{names}")
    known = facts_by_id(evidence)
    for name, row in rows.items():
        value, source = row["value"].lower(), row["source"]
        dash = source.strip().lower() in DASHES
        if not value:
            violations.append(f"empty_value:{name}")
        if dash and not value.startswith(UNKNOWN_VALUES):
            violations.append(f"uncited_fact:{name}")
        if contract["id_sources"] and not dash:
            cited = ID.findall(source)
            if not cited:
                violations.append(f"source_without_id:{name}")
            for identifier in cited:
                if identifier not in known:
                    violations.append(f"unknown_source_id:{name}:{identifier}")
            cited_text = " ".join(line for i in cited for line in known.get(i, []))
            for number in re.findall(r"\d+", ID.sub("", row["value"])):
                as_word = WORDS.get(number)
                if not re.search(r"(?<!\d)" + number + r"(?!\d)", ID.sub("", cited_text)) and not (
                        as_word and re.search(r"\b" + as_word + r"\b", cited_text, re.I)):
                    violations.append(f"number_not_in_source:{name}:{number}")
    if parsed["order"] != contract["sections"]:
        violations.append(f"sections:{parsed['order']}")
    for section in contract["sections"]:
        if not parsed["sections"].get(section):
            violations.append(f"empty_section:{section}")
    for line in parsed["stray"]:
        violations.append(f"prose_outside_sections:{line[:60]}")
    for extra in parsed["extra_headings"]:
        violations.append(f"unexpected_section:{extra}")
    if not parsed["closing"]:
        violations.append("non_action_line_missing")
    for rule in (expected or {}).get("rows", []):
        row = rows.get(rule["row"])
        if row is None:
            continue  # Already reported as a missing row.
        value = row["value"].lower()
        if rule.get("contains_any") and not any(token in value for token in rule["contains_any"]):
            violations.append(f"expected_any:{rule['row']}:{rule['contains_any']}")
        if any(token not in value for token in rule.get("contains", [])):
            violations.append(f"expected:{rule['row']}:{rule.get('contains')}")
        if any(token in value for token in rule.get("excludes", [])):
            violations.append(f"excluded:{rule['row']}:{rule.get('excludes')}")
        if "source_contains" in rule and rule["source_contains"] not in row["source"]:
            violations.append(f"expected_source:{rule['row']}:{rule['source_contains']}")
        if rule.get("no_digits") and re.search(r"\d", ID.sub("", row["value"])):
            violations.append(f"digits:{rule['row']}")
    lead = (expected or {}).get("lead")
    if lead and parsed["lead"] != lead:
        violations.append(f"expected_lead:{lead}:{parsed['lead']}")
    return violations


def expectations(scenario):
    data = json.loads(EXPECTATIONS.read_text())
    return data[scenario]


def contract_expectations(scenario):
    """Return the format expectations for a scenario, or None for free-form briefs."""
    return json.loads(EXPECTATIONS.read_text()).get(scenario)


def declared_format(scenario):
    """The output format a scenario's question routes to, when the case declares one."""
    cases = json.loads((ROOT / "tests/behavior/cases.json").read_text())
    return next((case.get("format") for case in cases if case["id"] == scenario), None)


def resolved_expectations(scenario):
    """Positive-control requirements for scenarios whose evidence resolves the question."""
    return json.loads(RESOLVED.read_text()).get(scenario)


def check_resolved(answer, scenario):
    """Return violations when an answer withholds a finding the evidence establishes.

    The judge only detects over-claiming. These checks are the deterministic half
    that an always-unknown answer cannot pass. They match whole words, so
    "confirmed" is not satisfied by "unconfirmed", and they decide wording only,
    never whether the surrounding reasoning is correct.
    """
    rule = resolved_expectations(scenario)
    if not rule:
        return []
    text = clean(answer)

    def present(phrase):
        return bool(re.search(r"(?<![\w-])" + re.escape(phrase) + r"(?![\w-])", text, re.I))

    def matched(requirement):
        if requirement.get("pattern"):
            return bool(re.search(requirement["pattern"], text, re.I))
        return any(present(phrase) for phrase in requirement["any"])

    violations = []
    for requirement in rule["requires"]:
        if not matched(requirement):
            violations.append(f"resolved_finding_missing:{scenario}:{requirement['name']}")
    for phrase in rule.get("excludes", []):
        if present(phrase):
            violations.append(f"resolved_finding_contradicted:{scenario}:{phrase}")
    return violations
