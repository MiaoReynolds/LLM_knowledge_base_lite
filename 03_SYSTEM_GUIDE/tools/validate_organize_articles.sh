#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-.}"
VAULT="$ROOT_DIR"

README_HUMAN="$VAULT/README_HUMAN.md"
MASTER_INDEX="$VAULT/01_INDEX/master_index.md"

fail=0

if [[ ! -f "$README_HUMAN" || ! -f "$MASTER_INDEX" ]]; then
  echo "[ERROR] Missing README_HUMAN.md or 01_INDEX/master_index.md"
  exit 2
fi

echo "== Validate organize-articles integrity =="

echo
echo "[1/3] Root-note residue check"
root_notes=$(find "$VAULT" -maxdepth 1 -type f \( -name "*.md" -o -name "*.canvas" \) \
  ! -name "README.md" ! -name "README_HUMAN.md" | sort || true)
if [[ -n "$root_notes" ]]; then
  echo "[WARN] Note files still in vault root:"
  echo "$root_notes"
  fail=1
else
  echo "[OK] No root-level note residue"
fi

echo
echo "[2/3] Master-index path existence check"
tmp_master=$(mktemp)
tmp_readme=$(mktemp)
trap 'rm -f "$tmp_master" "$tmp_readme"' EXIT

awk -F'|' '
  /^\|/ && $0 ~ /processed \+ summarized/ {
    loc=$3
    gsub(/^[ \t]+|[ \t]+$/, "", loc)
    if (loc != "") print loc
  }
' "$MASTER_INDEX" | sort -u > "$tmp_master"

while IFS= read -r p; do
  [[ -z "$p" ]] && continue
  fs="$VAULT$p"
  if [[ ! -e "$fs" ]]; then
    echo "[WARN] Missing file referenced by master_index: $p"
    fail=1
  fi
done < "$tmp_master"

if [[ $fail -eq 0 ]]; then
  echo "[OK] All master_index processed paths exist"
fi

echo
echo "[3/3] README_HUMAN coverage check"
grep -o '\[\[[^]]\+\]\]' "$README_HUMAN" \
  | sed -E 's/^\[\[|\]\]$//g' \
  | sed -E 's#^#/#' \
  | sort -u > "$tmp_readme"

while IFS= read -r p; do
  [[ -z "$p" ]] && continue
  if ! grep -Fxq "$p" "$tmp_readme"; then
    echo "[WARN] Processed note missing from README_HUMAN: $p"
    fail=1
  fi
done < "$tmp_master"

if [[ $fail -eq 0 ]]; then
  echo "[OK] README_HUMAN covers all processed source paths"
fi

echo
if [[ $fail -ne 0 ]]; then
  echo "[RESULT] FAILED (see warnings above)"
  exit 1
fi

echo "[RESULT] PASSED"
