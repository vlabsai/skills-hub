#!/bin/bash
# Deploy a directory to Vercel production
# Handles the non-interactive CLI quirks (scope, project linking)
#
# Usage: deploy.sh <source-dir> <project-name> [--preview]
#
# Arguments:
#   source-dir    Directory to deploy (must contain index.html or package.json)
#   project-name  Vercel project name (lowercase, hyphens only)
#   --preview     Deploy as preview instead of production (optional)

set -euo pipefail

SOURCE_DIR="${1:?Usage: deploy.sh <source-dir> <project-name> [--preview]}"
PROJECT_NAME="${2:?Usage: deploy.sh <source-dir> <project-name> [--preview]}"
PROD_FLAG="--prod"

if [[ "${3:-}" == "--preview" ]]; then
  PROD_FLAG=""
fi

# Validate source directory
if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "ERROR: Directory '$SOURCE_DIR' does not exist" >&2
  exit 1
fi

if [[ ! -f "$SOURCE_DIR/index.html" && ! -f "$SOURCE_DIR/package.json" ]]; then
  echo "ERROR: Directory must contain index.html or package.json" >&2
  exit 1
fi

# Check vercel CLI
if ! command -v vercel &> /dev/null; then
  echo "ERROR: vercel CLI not found. Install with: npm i -g vercel" >&2
  exit 1
fi

# Check authentication
if ! vercel whoami &> /dev/null 2>&1; then
  echo "ERROR: Not authenticated. Run: vercel login" >&2
  exit 1
fi

echo "==> Resolving Vercel org..."

# Method 1: Extract team ID from vercel link error (most reliable in non-interactive mode)
ORG_ID=$(vercel link --yes 2>&1 | python3 -c "
import sys, re
text = sys.stdin.read()
match = re.search(r'team_[A-Za-z0-9]+', text)
if match:
    print(match.group())
" 2>/dev/null || echo "")

# Method 2: Find org ID from any existing .vercel/project.json on disk
if [[ -z "$ORG_ID" ]]; then
  ORG_ID=$(find "$HOME" -maxdepth 4 -path '*/.vercel/project.json' -print -quit 2>/dev/null | xargs python3 -c "
import json, sys
d = json.load(open(sys.argv[1]))
print(d.get('orgId', ''))
" 2>/dev/null || echo "")
fi

if [[ -z "$ORG_ID" ]]; then
  echo "ERROR: Could not determine Vercel org ID" >&2
  echo "Try running 'vercel link' manually in any project first" >&2
  exit 1
fi

echo "    Org ID: $ORG_ID"

# Check if project exists, create if not
echo "==> Checking project '$PROJECT_NAME'..."
PROJECT_ID=$(vercel project ls --json 2>&1 | python3 -c "
import sys, json
lines = sys.stdin.read()
start = lines.index('{')
data = json.loads(lines[start:])
projects = data.get('projects', [])
for p in projects:
    if p.get('name') == '${PROJECT_NAME}':
        print(p['id'])
        break
" 2>/dev/null || echo "")

if [[ -z "$PROJECT_ID" ]]; then
  echo "    Project not found, creating..."
  vercel project add "$PROJECT_NAME" 2>&1
  sleep 1
  PROJECT_ID=$(vercel project ls --json 2>&1 | python3 -c "
import sys, json
lines = sys.stdin.read()
start = lines.index('{')
data = json.loads(lines[start:])
projects = data.get('projects', [])
for p in projects:
    if p.get('name') == '${PROJECT_NAME}':
        print(p['id'])
        break
" 2>/dev/null || echo "")
  if [[ -z "$PROJECT_ID" ]]; then
    echo "ERROR: Failed to create project or retrieve project ID" >&2
    exit 1
  fi
  echo "    Created project: $PROJECT_NAME ($PROJECT_ID)"
else
  echo "    Found project: $PROJECT_NAME ($PROJECT_ID)"
fi

# Write .vercel/project.json in source directory
echo "==> Linking project..."
mkdir -p "$SOURCE_DIR/.vercel"
cat > "$SOURCE_DIR/.vercel/project.json" << EJSON
{
  "orgId": "$ORG_ID",
  "projectId": "$PROJECT_ID"
}
EJSON

# Deploy
echo "==> Deploying${PROD_FLAG:+ to production}..."
DEPLOY_OUTPUT=$(cd "$SOURCE_DIR" && vercel deploy $PROD_FLAG --yes 2>&1)
echo "$DEPLOY_OUTPUT"

# Extract URLs
PRODUCTION_URL=$(echo "$DEPLOY_OUTPUT" | grep -oE 'https://[a-zA-Z0-9._-]+\.vercel\.app' | tail -1)

echo ""
echo "==> Deploy complete!"
if [[ -n "$PRODUCTION_URL" ]]; then
  echo "    URL: $PRODUCTION_URL"
fi

# Output JSON for programmatic use
echo ""
echo "JSON_OUTPUT:{\"url\":\"$PRODUCTION_URL\",\"project\":\"$PROJECT_NAME\",\"projectId\":\"$PROJECT_ID\"}"
