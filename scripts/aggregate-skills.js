/**
 * Aggregate skills from local skills/ directory
 * Reads SKILL.md files, extracts metadata, and collects all skill files
 *
 * Skills live in this repo under skills/. Set SKILLS_PATH env var to override.
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import matter from 'gray-matter';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const OUTPUT_FILE = path.join(ROOT, 'site', 'src', 'data', 'skills.json');

// Skills source: local skills/ directory or env override
const SKILLS_DIR = process.env.SKILLS_PATH || path.resolve(ROOT, 'skills');

const REPO_URL = 'https://github.com/vlabsai/skills-hub';
const REPO_NAME = 'vlabsai/skills-hub';
const DEFAULT_AUTHOR = 'vector-labs';
const DEFAULT_LICENSE = 'Apache-2.0';

// Category keywords for auto-categorization
const CATEGORY_KEYWORDS = {
  'observability': ['dashboard', 'metrics', 'monitor', 'datadog', 'alert', 'slo', 'sli', 'apm', 'trace', 'instrument'],
  'code-quality': ['review', 'lint', 'quality', 'refactor', 'clean', 'antipattern', 'anti-pattern', 'security'],
  'troubleshooting': ['diagnose', 'debug', 'logs', 'incident', 'troubleshoot', 'error', 'crash'],
  'devops-cicd': ['deploy', 'ci', 'cd', 'docker', 'kubernetes', 'terraform', 'pipeline', 'argocd'],
  'documentation': ['doc', 'readme', 'prd', 'contributing'],
  'testing': ['test', 'e2e', 'unit', 'integration', 'qa'],
  'general': []
};

/**
 * Determine category based on skill name and description
 */
function determineCategory(skillName, description = '') {
  const text = `${skillName} ${description}`.toLowerCase();

  for (const [category, keywords] of Object.entries(CATEGORY_KEYWORDS)) {
    if (category === 'general') continue;
    for (const keyword of keywords) {
      if (text.includes(keyword)) {
        return category;
      }
    }
  }
  return 'general';
}

/**
 * Recursively get all files in a directory
 */
function getFilesRecursive(dir, relativeTo = dir) {
  const files = [];
  if (!fs.existsSync(dir)) return files;

  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    const relativePath = path.relative(relativeTo, fullPath).replace(/\\/g, '/');

    if (entry.isDirectory()) {
      if (entry.name.startsWith('__') || entry.name.startsWith('.')) continue;
      files.push(...getFilesRecursive(fullPath, relativeTo));
    } else {
      if (entry.name.startsWith('.')) continue;
      const content = fs.readFileSync(fullPath, 'utf-8');
      files.push({ path: relativePath, name: entry.name, content });
    }
  }
  return files;
}

/**
 * Extract description from markdown content (fallback if no frontmatter description)
 */
function extractDescription(content) {
  const withoutFrontmatter = content.replace(/^---[\s\S]*?---\n*/m, '');
  const lines = withoutFrontmatter.split('\n');
  const descLines = [];

  for (const line of lines) {
    if (line.startsWith('#')) continue;
    if (descLines.length === 0 && line.trim() === '') continue;
    if (descLines.length > 0 && (line.trim() === '' || line.startsWith('#'))) break;
    descLines.push(line.trim());
  }
  return descLines.join(' ').slice(0, 300);
}

/**
 * Generate tags from skill name and description
 */
function generateTags(name, description) {
  const tags = new Set();
  const text = `${name} ${description}`.toLowerCase();

  const tagKeywords = [
    'datadog', 'dashboard', 'metrics', 'logs', 'review', 'dotnet', 'csharp',
    'kubernetes', 'terraform', 'security', 'performance', 'api', 'deploy'
  ];

  for (const keyword of tagKeywords) {
    if (text.includes(keyword)) tags.add(keyword);
  }

  name.split('-').filter(p => p.length > 2).forEach(p => tags.add(p));
  return Array.from(tags).slice(0, 5);
}

/**
 * Process a single skill folder
 */
function processSkill(skillPath, skillName) {
  const skillMdPath = path.join(skillPath, 'SKILL.md');
  if (!fs.existsSync(skillMdPath)) {
    console.warn(`  Skipping ${skillName}: No SKILL.md found`);
    return null;
  }

  const raw = fs.readFileSync(skillMdPath, 'utf-8');
  const { data: frontmatter, content } = matter(raw);
  const files = getFilesRecursive(skillPath);

  const skill = {
    id: skillName,
    name: frontmatter.name || skillName,
    description: frontmatter.description || extractDescription(content),
    shortDescription: (frontmatter.description || extractDescription(content)).slice(0, 100),
    category: determineCategory(skillName, frontmatter.description || content),
    author: frontmatter.metadata?.author || DEFAULT_AUTHOR,
    license: frontmatter.license || DEFAULT_LICENSE,
    licenseNotice: `Licensed under ${frontmatter.license || DEFAULT_LICENSE}`,
    source: {
      repo: REPO_URL,
      repoName: REPO_NAME,
      path: `skills/${skillName}`,
      branch: 'main'
    },
    files: files.map(f => ({ path: f.path, name: f.name, content: f.content })),
    skillMdContent: raw,
    tags: frontmatter.tags || generateTags(skillName, frontmatter.description || content),
    featured: frontmatter.featured || false,
    complexity: frontmatter.complexity || 'intermediate',
    compatibility: frontmatter.compatibility || null,
    platforms: frontmatter.platforms || ['windows', 'macos', 'linux'],
    links: frontmatter.links || []
  };

  return skill;
}

/**
 * Main aggregation
 */
async function aggregate() {
  console.log(`Aggregating skills from: ${SKILLS_DIR}\n`);

  if (!fs.existsSync(SKILLS_DIR)) {
    console.error(`Skills directory not found: ${SKILLS_DIR}`);
    console.error('Set SKILLS_PATH env var or ensure skills/ directory exists.');
    process.exit(1);
  }

  const skills = [];
  const categories = new Map();

  const skillFolders = fs.readdirSync(SKILLS_DIR, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name);

  console.log(`Found ${skillFolders.length} skill folder(s)`);

  for (const skillName of skillFolders) {
    const skillPath = path.join(SKILLS_DIR, skillName);
    const skill = processSkill(skillPath, skillName);

    if (skill) {
      skills.push(skill);
      categories.set(skill.category, (categories.get(skill.category) || 0) + 1);
      console.log(`  + ${skillName} [${skill.category}] (${skill.files.length} files)`);
    }
  }

  const output = {
    version: '2.0.0',
    lastUpdated: new Date().toISOString(),
    totalSkills: skills.length,
    categories: Array.from(categories.entries()).map(([id, count]) => ({ id, count })),
    skills
  };

  const outputDir = path.dirname(OUTPUT_FILE);
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(output, null, 2));

  console.log(`\nTotal: ${skills.length} skill(s) in ${categories.size} category(ies)`);
  console.log(`Output: ${OUTPUT_FILE}`);
}

aggregate().catch(console.error);
