#!/bin/bash
# Claude Code statusline — uses pre-calculated fields for accuracy
# Docs: https://code.claude.com/docs/en/statusline
export LC_ALL=C

input=$(cat)

# Extract pre-calculated fields (accurate, no manual math needed)
MODEL=$(echo "$input" | jq -r '.model.display_name // "Unknown"')
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
DURATION_MS=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
IN_TOK=$(echo "$input" | jq -r '.context_window.total_input_tokens // 0')
OUT_TOK=$(echo "$input" | jq -r '.context_window.total_output_tokens // 0')

# Format token counts with k suffix for readability
format_tokens() {
  local n=$1
  if [ "$n" -ge 1000 ]; then
    printf "%.1fk" "$(awk -v n="$n" 'BEGIN { printf "%.1f", n / 1000 }')"
  else
    printf "%d" "$n"
  fi
}
IN_TOK_FMT=$(format_tokens "$IN_TOK")
OUT_TOK_FMT=$(format_tokens "$OUT_TOK")

# Format cost
COST_FMT=$(printf '$%.2f' "$COST")

# Format duration
DURATION_SEC=$((DURATION_MS / 1000))
MINS=$((DURATION_SEC / 60))
SECS=$((DURATION_SEC % 60))
if [ "$MINS" -gt 59 ]; then
  HOURS=$((MINS / 60))
  MINS=$((MINS % 60))
  TIME_FMT="${HOURS}h ${MINS}m"
else
  TIME_FMT="${MINS}m ${SECS}s"
fi

# Color context by usage threshold
GREEN='\033[32m'; YELLOW='\033[33m'; RED='\033[31m'
DIM='\033[2m'; RESET='\033[0m'

if [ "$PCT" -ge 75 ]; then CTX_COLOR="$RED"
elif [ "$PCT" -ge 50 ]; then CTX_COLOR="$YELLOW"
else CTX_COLOR="$GREEN"; fi

printf "${DIM}%s${RESET} | ${DIM}%s${RESET} | ${DIM}%s${RESET} | ${DIM}in %s / out %s${RESET} | ${CTX_COLOR}%s%% ctx${RESET}\n" \
  "$MODEL" "$COST_FMT" "$TIME_FMT" "$IN_TOK_FMT" "$OUT_TOK_FMT" "$PCT"
