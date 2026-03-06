#!/usr/bin/env node

/**
 * Vector Labs Skills CLI
 *
 * Install skills from vlabsai/skills-hub into your project.
 * Auto-detects your AI tool and installs to the correct location.
 *
 * Usage:
 *   npx @vlabsai/skills add <skill-name>       Install a skill (auto-detect tool)
 *   npx @vlabsai/skills list                    List available skills
 *   npx @vlabsai/skills info <skill-name>       Show skill details
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, appendFileSync } from 'fs';
import { join, dirname, relative } from 'path';
import { argv, exit, cwd, env, stdin, stdout } from 'process';
import { createInterface } from 'readline';
import { execSync } from 'child_process';
import { homedir } from 'os';

const REPO_OWNER = env.VECTOR_LABS_SKILLS_OWNER || 'vlabsai';
const REPO_NAME = env.VECTOR_LABS_SKILLS_REPO || 'skills-hub';
let BRANCH = env.VECTOR_LABS_SKILLS_BRANCH || 'main';
const SKILLS_DIR = 'skills';
const API_BASE = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}`;

// ── Tool detection ───────────────────────────────────────────────────────────

const TOOLS = [
  {
    id: 'claude-code',
    name: 'Claude Code',
    dest: '.claude/skills',
    detect: () => existsSync(join(cwd(), '.claude')),
  },
  {
    id: 'cursor',
    name: 'Cursor',
    dest: '.cursor/skills',
    detect: () => existsSync(join(cwd(), '.cursor')) || existsSync(join(cwd(), '.cursorrules')),
  },
  {
    id: 'copilot',
    name: 'GitHub Copilot',
    dest: '.github/skills',
    detect: () => existsSync(join(cwd(), '.github', 'copilot-instructions.md')) || existsSync(join(cwd(), '.github', 'skills')),
  },
  {
    id: 'gemini',
    name: 'Gemini CLI',
    dest: '.gemini/skills',
    detect: () => existsSync(join(cwd(), '.gemini')),
  },
];

function detectTools() {
  return TOOLS.filter(t => t.detect());
}

// ── Parse global flags ───────────────────────────────────────────────────────

const args = argv.slice(2);

function extractFlag(name) {
  const idx = args.indexOf(name);
  if (idx === -1) return null;
  const val = args[idx + 1];
  args.splice(idx, 2);
  return val;
}

const LOCAL_SOURCE = extractFlag('--source') || env.VECTOR_LABS_SKILLS_SOURCE || null;
const FORCE_DEST = extractFlag('--dest');
const FORCE_TOOL = extractFlag('--tool');
const FORCE_BRANCH = extractFlag('--branch');
if (FORCE_BRANCH) BRANCH = FORCE_BRANCH;
const YES_FLAG = args.includes('-y') || args.includes('--yes');
if (YES_FLAG) {
  const yIdx = args.indexOf('-y') !== -1 ? args.indexOf('-y') : args.indexOf('--yes');
  if (yIdx !== -1) args.splice(yIdx, 1);
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function error(msg) {
  console.error(`\x1b[31merror:\x1b[0m ${msg}`);
  exit(1);
}

function success(msg) {
  console.log(`\x1b[32m✓\x1b[0m ${msg}`);
}

function info(msg) {
  console.log(`\x1b[36mℹ\x1b[0m ${msg}`);
}

function dim(msg) {
  return `\x1b[2m${msg}\x1b[0m`;
}

function bold(msg) {
  return `\x1b[1m${msg}\x1b[0m`;
}

async function prompt(question) {
  const rl = createInterface({ input: stdin, output: stdout });
  return new Promise(resolve => {
    rl.question(question, answer => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

// ── GitHub token resolution ─────────────────────────────────────────────────

function tryGhAuthToken() {
  try {
    return execSync('gh auth token', { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] }).trim();
  } catch {
    return null;
  }
}

function readNpmrcToken() {
  const npmrcPath = join(homedir(), '.npmrc');
  if (!existsSync(npmrcPath)) return null;
  const content = readFileSync(npmrcPath, 'utf-8');
  // Match a literal token (not env var reference)
  const match = content.match(/\/\/npm\.pkg\.github\.com\/:_authToken=(?!\$\{)(.+)/);
  return match ? match[1].trim() : null;
}

function resolveGitHubToken() {
  // 1. Env vars (highest priority)
  if (env.GITHUB_TOKEN) return env.GITHUB_TOKEN;
  if (env.GH_TOKEN) return env.GH_TOKEN;
  // 2. gh CLI
  const ghToken = tryGhAuthToken();
  if (ghToken) return ghToken;
  // 3. .npmrc (literal token only)
  const npmrcToken = readNpmrcToken();
  if (npmrcToken) return npmrcToken;
  return null;
}

function checkNpmrcSetup() {
  const npmrcPath = join(homedir(), '.npmrc');
  if (!existsSync(npmrcPath)) return { hasRegistry: false, hasAuth: false };
  const content = readFileSync(npmrcPath, 'utf-8');
  return {
    hasRegistry: content.includes('@vlabsai:registry=https://npm.pkg.github.com'),
    hasAuth: /\/\/npm\.pkg\.github\.com\/:_authToken=/.test(content),
  };
}

function ensureAuth() {
  const token = resolveGitHubToken();
  if (!token) {
    console.error(`\n  ${bold('Authentication required')}\n`);
    console.error(`  The skills repo (${REPO_OWNER}/${REPO_NAME}) requires a GitHub token.\n`);
    console.error(`  Run ${bold('npx @vlabsai/skills setup')} to configure authentication.\n`);
    console.error(`  Or set GITHUB_TOKEN in your environment:\n`);
    console.error(`    export GITHUB_TOKEN=$(gh auth token)\n`);
    exit(1);
  }
  return token;
}

async function setupAuth() {
  console.log(`\n  ${bold('Vector Labs Skills — Setup')}\n`);

  const { hasRegistry, hasAuth } = checkNpmrcSetup();
  const npmrcPath = join(homedir(), '.npmrc');

  // Step 1: Check npm registry config
  if (hasRegistry && hasAuth) {
    success('.npmrc already configured for @vlabsai packages');
  } else {
    info('Configuring ~/.npmrc for GitHub Packages...\n');

    // Try to get a token
    let token = tryGhAuthToken();

    if (token) {
      info(`Found token from ${bold('gh auth token')}`);
    } else {
      console.log(`  No GitHub CLI token found. You need a GitHub Personal Access Token`);
      console.log(`  with ${bold('read:packages')} and ${bold('repo')} scopes.\n`);
      console.log(`  Create one at: ${dim('https://github.com/settings/tokens/new')}\n`);
      token = await prompt('  Paste your token: ');
      if (!token) error('No token provided.');
    }

    // Validate token
    info('Validating token...');
    const res = await fetch('https://api.github.com/user', {
      headers: { 'Authorization': `token ${token}`, 'User-Agent': 'vector-labs-skills-cli' }
    });

    if (!res.ok) {
      error('Token is invalid or expired. Please check and try again.');
    }

    const user = await res.json();
    success(`Authenticated as ${bold(user.login)}`);

    // Write .npmrc entries
    const lines = [];
    if (!hasRegistry) lines.push('@vlabsai:registry=https://npm.pkg.github.com');
    if (!hasAuth) lines.push(`//npm.pkg.github.com/:_authToken=${token}`);

    if (lines.length > 0) {
      const existing = existsSync(npmrcPath) ? readFileSync(npmrcPath, 'utf-8') : '';
      const separator = existing && !existing.endsWith('\n') ? '\n' : '';
      appendFileSync(npmrcPath, separator + lines.join('\n') + '\n');
      success(`Updated ${dim(npmrcPath)}`);
    }
  }

  // Step 2: Verify access to the skills repo
  console.log('');
  info('Verifying access to skills repo...');

  const token = resolveGitHubToken();
  const res = await fetch(`${API_BASE}/contents/${SKILLS_DIR}?ref=${BRANCH}`, {
    headers: {
      'Authorization': `token ${token}`,
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'vector-labs-skills-cli'
    }
  });

  if (res.ok) {
    const data = await res.json();
    const skillCount = data.filter(e => e.type === 'dir').length;
    success(`Access confirmed — ${skillCount} skill(s) available`);
  } else if (res.status === 404) {
    info(`Skills directory not found on branch ${bold(BRANCH)}. This is OK if skills aren't on main yet.`);
  } else {
    console.error(`  ${dim(`Status: ${res.status}`)}`);
    error('Could not access the skills repo. Check that your token has repo access.');
  }

  console.log(`\n  ${bold('Setup complete!')} You can now run:\n`);
  console.log(`    npx @vlabsai/skills list`);
  console.log(`    npx @vlabsai/skills add <skill-name>\n`);
}

// ── Resolve install destination ──────────────────────────────────────────────

async function resolveDestination() {
  // Explicit --dest always wins
  if (FORCE_DEST) return FORCE_DEST;

  // Explicit --tool
  if (FORCE_TOOL) {
    const tool = TOOLS.find(t => t.id === FORCE_TOOL);
    if (!tool) error(`Unknown tool: ${FORCE_TOOL}. Available: ${TOOLS.map(t => t.id).join(', ')}`);
    return tool.dest;
  }

  // Auto-detect
  const detected = detectTools();

  if (detected.length === 1) {
    info(`Detected ${bold(detected[0].name)} → installing to ${bold(detected[0].dest)}`);
    return detected[0].dest;
  }

  if (detected.length > 1) {
    console.log(`\n  Detected multiple AI tools:\n`);
    detected.forEach((t, i) => {
      console.log(`    ${bold(String(i + 1))}. ${t.name} → ${dim(t.dest)}`);
    });
    console.log(`    ${bold(String(detected.length + 1))}. All of the above`);
    console.log('');

    if (YES_FLAG) {
      // With -y, install to all detected
      return detected.map(t => t.dest);
    }

    const answer = await prompt(`  Which tool? [1-${detected.length + 1}]: `);
    const choice = parseInt(answer);

    if (choice === detected.length + 1) {
      return detected.map(t => t.dest);
    }

    if (choice >= 1 && choice <= detected.length) {
      return detected[choice - 1].dest;
    }

    error('Invalid choice.');
  }

  // Nothing detected — ask
  console.log(`\n  No AI tool detected. Where should skills be installed?\n`);
  TOOLS.forEach((t, i) => {
    console.log(`    ${bold(String(i + 1))}. ${t.name} ${dim(`→ ${t.dest}`)}`);
  });
  console.log(`    ${bold(String(TOOLS.length + 1))}. Custom path`);
  console.log('');

  if (YES_FLAG) {
    // Default to copilot (.github/skills) with -y flag
    info('No tool detected, using default: .github/skills');
    return '.github/skills';
  }

  const answer = await prompt(`  Which tool? [1-${TOOLS.length + 1}]: `);
  const choice = parseInt(answer);

  if (choice >= 1 && choice <= TOOLS.length) {
    return TOOLS[choice - 1].dest;
  }

  if (choice === TOOLS.length + 1) {
    const customPath = await prompt('  Enter path: ');
    if (!customPath) error('No path provided.');
    return customPath;
  }

  error('Invalid choice.');
}

// ── Local filesystem provider ────────────────────────────────────────────────

function localListSkills(sourcePath) {
  const skillsPath = join(sourcePath, SKILLS_DIR);
  if (!existsSync(skillsPath)) error(`Skills directory not found: ${skillsPath}`);

  return readdirSync(skillsPath, { withFileTypes: true })
    .filter(d => d.isDirectory() && !d.name.startsWith('.'))
    .map(d => d.name);
}

function localReadFile(sourcePath, filePath) {
  const fullPath = join(sourcePath, filePath);
  if (!existsSync(fullPath)) return null;
  return readFileSync(fullPath, 'utf-8');
}

function localCollectFiles(dir) {
  const files = [];
  const entries = readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = join(dir, entry.name);
    if (entry.name.startsWith('.')) continue;

    if (entry.isDirectory()) {
      files.push(...localCollectFiles(fullPath));
    } else {
      files.push(fullPath);
    }
  }
  return files;
}

// ── GitHub API provider ──────────────────────────────────────────────────────

async function githubFetch(path) {
  const url = `${API_BASE}${path}`;
  const headers = { 'Accept': 'application/vnd.github.v3+json', 'User-Agent': 'vector-labs-skills-cli' };

  const token = resolveGitHubToken();
  if (token) headers['Authorization'] = `token ${token}`;

  const res = await fetch(url, { headers });

  if (res.status === 401 || res.status === 403) {
    console.error('');
    console.error(`  ${bold('API rate limit or access error')} (${res.status})`);
    console.error(`  Try setting a GitHub token to increase rate limits:\n`);
    console.error(`    export GITHUB_TOKEN=$(gh auth token)\n`);
    console.error(`  Or run ${bold('npx @vlabsai/skills setup')} for guided setup.\n`);
    exit(1);
  }
  if (res.status === 404) return null;
  if (!res.ok) error(`GitHub API error: ${res.status} ${res.statusText}`);

  return res.json();
}

async function githubCollectFiles(entries, basePath) {
  const files = [];

  for (const entry of entries) {
    if (entry.type === 'file') {
      const data = await githubFetch(`/contents/${entry.path}?ref=${BRANCH}`);
      if (data?.content) {
        const relativePath = entry.path.replace(`${basePath}/`, '');
        const content = Buffer.from(data.content, 'base64').toString('utf-8');
        files.push({ path: relativePath, content });
      }
    } else if (entry.type === 'dir') {
      const subEntries = await githubFetch(`/contents/${entry.path}?ref=${BRANCH}`);
      if (subEntries) {
        files.push(...await githubCollectFiles(subEntries, basePath));
      }
    }
  }

  return files;
}

// ── Fetch skill files ────────────────────────────────────────────────────────

async function fetchSkillFiles(skillName) {
  if (LOCAL_SOURCE) {
    const skillDir = join(LOCAL_SOURCE, SKILLS_DIR, skillName);
    if (!existsSync(skillDir)) {
      error(`Skill "${skillName}" not found. Run ${bold('npx @vlabsai/skills list')} to see available skills.`);
    }

    const allPaths = localCollectFiles(skillDir);
    return allPaths.map(fullPath => ({
      path: relative(skillDir, fullPath),
      content: readFileSync(fullPath, 'utf-8')
    }));
  }

  info(`Fetching ${skillName} from ${REPO_OWNER}/${REPO_NAME}...`);
  const tree = await githubFetch(`/contents/${SKILLS_DIR}/${skillName}?ref=${BRANCH}`);
  if (!tree) {
    error(`Skill "${skillName}" not found. Run ${bold('npx @vlabsai/skills list')} to see available skills.`);
  }
  return githubCollectFiles(tree, `${SKILLS_DIR}/${skillName}`);
}

// ── Commands ─────────────────────────────────────────────────────────────────

async function listSkills() {
  let skillNames;

  if (LOCAL_SOURCE) {
    info(`Reading skills from ${LOCAL_SOURCE}...`);
    skillNames = localListSkills(LOCAL_SOURCE);
  } else {
    info(`Fetching skills from ${REPO_OWNER}/${REPO_NAME}...`);
    const tree = await githubFetch(`/contents/${SKILLS_DIR}?ref=${BRANCH}`);
    if (!tree) error('Could not fetch skills directory.');
    skillNames = tree.filter(e => e.type === 'dir').map(e => e.name);
  }

  if (skillNames.length === 0) {
    info('No skills found.');
    return;
  }

  console.log(`\n  Available skills (${skillNames.length}):\n`);
  for (const name of skillNames.sort()) {
    let desc = '';
    if (LOCAL_SOURCE) {
      const content = localReadFile(LOCAL_SOURCE, `${SKILLS_DIR}/${name}/SKILL.md`);
      if (content) {
        const match = content.match(/description:\s*['"]?(.+?)['"]?\s*$/m);
        if (match) desc = match[1].slice(0, 60);
      }
    }
    console.log(`    ${name}${desc ? dim(`  ${desc}`) : ''}`);
  }
  console.log(`\n  Run ${bold('npx @vlabsai/skills add <name>')} to install.\n`);
}

async function showInfo(skillName) {
  info(`Fetching ${skillName}...`);

  let content;
  let fileList;

  if (LOCAL_SOURCE) {
    content = localReadFile(LOCAL_SOURCE, `${SKILLS_DIR}/${skillName}/SKILL.md`);
    if (!content) error(`Skill "${skillName}" not found.`);

    const skillDir = join(LOCAL_SOURCE, SKILLS_DIR, skillName);
    const allFiles = localCollectFiles(skillDir);
    fileList = allFiles.map(f => relative(skillDir, f));
  } else {
    const data = await githubFetch(`/contents/${SKILLS_DIR}/${skillName}/SKILL.md?ref=${BRANCH}`);
    if (!data?.content) error(`Skill "${skillName}" not found.`);
    content = Buffer.from(data.content, 'base64').toString('utf-8');

    const tree = await githubFetch(`/contents/${SKILLS_DIR}/${skillName}?ref=${BRANCH}`);
    if (tree) {
      const files = await githubCollectFiles(tree, `${SKILLS_DIR}/${skillName}`);
      fileList = files.map(f => f.path);
    }
  }

  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (fmMatch) {
    console.log(`\n  Skill: ${bold(skillName)}`);
    const lines = fmMatch[1].split('\n');
    for (const line of lines) {
      if (line.trim()) console.log(`  ${line.trim()}`);
    }
  }

  if (fileList) {
    console.log(`\n  Files (${fileList.length}):`);
    for (const f of fileList) {
      console.log(`    ${f}`);
    }
  }
  console.log('');
}

async function addSkill(skillName) {
  const files = await fetchSkillFiles(skillName);
  if (files.length === 0) error('No files found in skill.');

  const destinations = await resolveDestination();
  const destList = Array.isArray(destinations) ? destinations : [destinations];

  for (const dest of destList) {
    const targetDir = join(cwd(), dest, skillName);

    if (existsSync(targetDir)) {
      info(`Overwriting existing skill at ${dest}/${skillName}/`);
    }

    for (const file of files) {
      const filePath = join(targetDir, file.path);
      mkdirSync(dirname(filePath), { recursive: true });
      writeFileSync(filePath, file.content);
      console.log(`  ${dim('+')} ${dest}/${skillName}/${file.path}`);
    }

    success(`Installed ${skillName} (${files.length} files) → ${bold(dest + '/' + skillName + '/')}`);
  }

  console.log('');
}

// ── CLI Router ───────────────────────────────────────────────────────────────

const command = args[0];

if (!command || command === '--help' || command === '-h') {
  console.log(`
  ${bold('Vector Labs Skills CLI')}

  \x1b[4mUsage:\x1b[0m
    npx @vlabsai/skills list                      List available skills
    npx @vlabsai/skills add <skill-name>          Auto-detect tool and install
    npx @vlabsai/skills add <name> --tool cursor  Install for specific tool
    npx @vlabsai/skills add <name> --dest <path>  Install to custom path
    npx @vlabsai/skills info <skill-name>         Show skill details
    npx @vlabsai/skills setup                     Configure auth (optional)

  \x1b[4mCommands:\x1b[0m
    list          List all available skills
    add <name>    Install a skill into your project
    info <name>   Show skill metadata and files
    setup         Configure GitHub token (optional — increases API rate limits)

  \x1b[4mOptions:\x1b[0m
    --tool <id>       Target tool: claude-code, cursor, copilot, gemini
    --dest <path>     Custom install path (overrides tool detection)
    --branch <name>   GitHub branch to fetch from (default: main)
    --source <path>   Read skills from local directory instead of GitHub
    -y, --yes         Skip prompts (auto-select or use defaults)

  \x1b[4mTool detection:\x1b[0m
    The CLI auto-detects your AI tool and installs to the right place:
      .claude/          → Claude Code  → .claude/skills/
      .cursor/          → Cursor       → .cursor/skills/
      .github/copilot-* → Copilot      → .github/skills/
      .gemini/          → Gemini CLI   → .gemini/skills/

  \x1b[4mEnvironment (optional):\x1b[0m
    GITHUB_TOKEN          GitHub token (increases API rate limits)
    GH_TOKEN              Alternative token variable (used by gh CLI)
    VECTOR_LABS_SKILLS_SOURCE    Local path to skills repo (same as --source)

  \x1b[4mExamples:\x1b[0m
    npx @vlabsai/skills list
    npx @vlabsai/skills add generate-dashboard
    npx @vlabsai/skills add review-pr --tool cursor
    npx @vlabsai/skills add diagnose-logs -y
`);
  exit(0);
}

switch (command) {
  case 'setup':
  case 'init':
  case 'auth':
    await setupAuth();
    break;

  case 'list':
  case 'ls':
    await listSkills();
    break;

  case 'add':
  case 'install':
  case 'i': {
    const skillName = args[1];
    if (!skillName) error('Missing skill name. Usage: npx @vlabsai/skills add <skill-name>');
    await addSkill(skillName);
    break;
  }

  case 'info':
  case 'show': {
    const skillName = args[1];
    if (!skillName) error('Missing skill name. Usage: npx @vlabsai/skills info <skill-name>');
    await showInfo(skillName);
    break;
  }

  default:
    error(`Unknown command: ${command}. Run npx @vlabsai/skills --help`);
}
