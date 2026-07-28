#!/usr/bin/env bash
set -euo pipefail

MODE="dry-run"
if [[ "${1:-}" == "--apply" ]]; then
  MODE="apply"
elif [[ "${1:-}" == "--dry-run" || "${1:-}" == "" ]]; then
  MODE="dry-run"
elif [[ "${1:-}" == "--help" ]]; then
  echo "Usage: cleanup_orphan_summaries.sh [--dry-run|--apply]"
  echo "Detect summaries whose Original file no longer exists."
  exit 0
else
  echo "Unknown option: ${1}" >&2
  echo "Usage: cleanup_orphan_summaries.sh [--dry-run|--apply]" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SUMMARY_DIR="${VAULT_ROOT}/02_SUMMARY"

if [[ ! -d "${SUMMARY_DIR}" ]]; then
  echo "Summary directory not found: ${SUMMARY_DIR}" >&2
  exit 1
fi

total=0
checked=0
orphans=0
removed=0
missing_source_line=0

for summary in "${SUMMARY_DIR}"/*.summary.md; do
  [[ -e "${summary}" ]] || continue
  total=$((total + 1))

  original_rel="$(sed -n 's/^- Original: \(.*\)$/\1/p' "${summary}" | head -n 1)"
  if [[ -z "${original_rel}" ]]; then
    missing_source_line=$((missing_source_line + 1))
    echo "[WARN] Missing 'Original' line: ${summary}"
    continue
  fi

  checked=$((checked + 1))
  original_abs="${VAULT_ROOT}/${original_rel#/}"

  if [[ ! -f "${original_abs}" ]]; then
    orphans=$((orphans + 1))
    echo "[ORPHAN] ${summary}"
    echo "         missing source: ${original_rel}"
    if [[ "${MODE}" == "apply" ]]; then
      rm -f "${summary}"
      removed=$((removed + 1))
      echo "         removed"
    fi
  fi
done

echo
echo "Mode: ${MODE}"
echo "Summary files total: ${total}"
echo "Checked with Original path: ${checked}"
echo "Orphan summaries found: ${orphans}"
echo "Summaries removed: ${removed}"
echo "Missing Original metadata: ${missing_source_line}"
