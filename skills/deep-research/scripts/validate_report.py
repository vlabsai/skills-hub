#!/usr/bin/env python3
"""
Report Validation Script
Validates research reports for quality standards.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List


class ReportValidator:
    """Validates research report quality"""

    def __init__(self, report_path: Path):
        self.report_path = report_path
        self.content = self._read_report()
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def _read_report(self) -> str:
        try:
            with open(self.report_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"ERROR: Cannot read report: {e}")
            sys.exit(1)

    def validate(self) -> bool:
        print(f"\n{'='*60}")
        print(f"VALIDATING: {self.report_path.name}")
        print(f"{'='*60}\n")

        checks = [
            ("Has sections", self._check_has_sections),
            ("Citations present", self._check_citations),
            ("Bibliography", self._check_bibliography),
            ("No placeholders", self._check_placeholders),
            ("No truncation", self._check_content_truncation),
            ("Word count", self._check_word_count),
        ]

        for check_name, check_func in checks:
            print(f"  Checking: {check_name}...", end=" ")
            passed = check_func()
            print("PASS" if passed else "FAIL")

        self._print_summary()
        return len(self.errors) == 0

    def _check_has_sections(self) -> bool:
        """Check report has meaningful structure (at least 3 ## headings)"""
        sections = re.findall(r'^## .+$', self.content, re.MULTILINE)
        if len(sections) < 3:
            self.errors.append(f"Too few sections: {len(sections)} (need at least 3)")
            return False

        # Warn if missing common sections
        content_lower = self.content.lower()
        if 'bibliography' not in content_lower:
            self.warnings.append("No Bibliography section found")
        if 'executive summary' not in content_lower and 'summary' not in content_lower:
            self.warnings.append("No Executive Summary section found")

        return True

    def _check_citations(self) -> bool:
        """Check citations exist and are reasonably numbered"""
        citations = re.findall(r'\[(\d+)\]', self.content)
        if not citations:
            self.errors.append("No citations [N] found in report")
            return False

        unique = set(citations)
        if len(unique) < 5:
            self.warnings.append(f"Only {len(unique)} unique sources (consider expanding)")

        return True

    def _check_bibliography(self) -> bool:
        """Check bibliography exists and has entries matching citations"""
        pattern = r'## Bibliography(.*?)(?=##|\Z)'
        match = re.search(pattern, self.content, re.DOTALL | re.IGNORECASE)

        if not match:
            self.warnings.append("Missing Bibliography section")
            return True  # Warning, not error

        bib_section = match.group(1)

        # Check for truncation placeholders
        truncation_patterns = [
            (r'\[\d+-\d+\]', 'Citation range (e.g., [8-75])'),
            (r'Additional.*citations', '"Additional citations"'),
            (r'\[Continue with', '"[Continue with"'),
        ]
        for pattern_re, description in truncation_patterns:
            if re.search(pattern_re, bib_section, re.IGNORECASE):
                self.errors.append(f"Bibliography truncated: {description}")
                return False

        # Check entries exist
        bib_entries = re.findall(r'^\[(\d+)\]', bib_section, re.MULTILINE)
        if not bib_entries:
            self.errors.append("Bibliography has no entries")
            return False

        # Check citations in text have bib entries
        text_citations = set(re.findall(r'\[(\d+)\]', self.content))
        bib_citations = set(bib_entries)
        missing = text_citations - bib_citations
        if missing:
            self.warnings.append(f"Citations missing from bibliography: {sorted(missing)}")

        return True

    def _check_placeholders(self) -> bool:
        placeholders = ['TBD', 'TODO', 'FIXME', '[citation needed]', '[placeholder]']
        found = [p for p in placeholders if p in self.content]
        if found:
            self.errors.append(f"Placeholder text found: {', '.join(found)}")
            return False
        return True

    def _check_content_truncation(self) -> bool:
        patterns = [
            (r'Content continues', '"Content continues"'),
            (r'Due to length', '"Due to length"'),
            (r'\[Sections \d+-\d+', '"[Sections X-Y"'),
        ]
        for pattern_re, description in patterns:
            if re.search(pattern_re, self.content, re.IGNORECASE):
                self.errors.append(f"Content truncation: {description}")
                return False
        return True

    def _check_word_count(self) -> bool:
        word_count = len(self.content.split())
        if word_count < 500:
            self.warnings.append(f"Short report: {word_count} words")
        return True

    def _print_summary(self):
        print(f"\n{'='*60}")
        if self.errors:
            print(f"ERRORS ({len(self.errors)}):")
            for e in self.errors:
                print(f"  - {e}")
        if self.warnings:
            print(f"WARNINGS ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"  - {w}")
        if not self.errors and not self.warnings:
            print("ALL CHECKS PASSED")
        elif not self.errors:
            print("PASSED (with warnings)")
        else:
            print("FAILED — fix errors before delivery")
        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Validate research report")
    parser.add_argument('--report', '-r', type=str, required=True, help='Path to report')
    args = parser.parse_args()

    report_path = Path(args.report)
    if not report_path.exists():
        print(f"ERROR: Not found: {report_path}")
        sys.exit(1)

    validator = ReportValidator(report_path)
    passed = validator.validate()
    sys.exit(0 if passed else 1)


if __name__ == '__main__':
    main()
