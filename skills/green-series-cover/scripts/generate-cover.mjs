#!/usr/bin/env node

import { randomUUID } from 'node:crypto';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { dirname, extname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const API_ORIGIN = 'https://api.hiapi.ai';
const DEFAULT_MODEL = 'gpt-image-2/image-to-image';
const DEFAULT_REFERENCE = fileURLToPath(new URL('../assets/reference-cover.png', import.meta.url));

function usage(message) {
  if (message) console.error(`Error: ${message}`);
  console.error('Usage: node scripts/generate-cover.mjs --title "..." --issue 1 [--chapter 2] [--output cover.png] [--reference path] [--model id]');
  process.exitCode = 2;
}

function parseArgs(argv) {
  const options = { model: DEFAULT_MODEL, reference: DEFAULT_REFERENCE };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--title' || arg === '--issue' || arg === '--chapter' || arg === '--output' || arg === '--reference' || arg === '--model') {
      const value = argv[++i];
      if (!value) return usage(`${arg} requires a value`);
      options[arg.slice(2)] = value;
    } else if (arg === '--help' || arg === '-h') {
      usage();
      process.exitCode = 0;
      return null;
    } else {
      return usage(`unknown argument: ${arg}`);
    }
  }
  if (!options.title?.trim()) return usage('--title is required');
  if (!/^[1-9][0-9]*$/.test(String(options.issue ?? ''))) return usage('--issue must be a positive integer');
  if (options.chapter !== undefined && !/^[1-9][0-9]*$/.test(String(options.chapter))) return usage('--chapter must be a positive integer');
  options.issue = Number(options.issue);
  if (options.chapter !== undefined) options.chapter = Number(options.chapter);
  options.output = options.output ? resolve(options.output) : resolve(`wechat-cover-${options.issue}.png`);
  options.reference = resolve(options.reference);
  return options;
}

function requireApiKey() {
  const key = process.env.HIAPI_API_KEY?.trim();
  if (!key) throw new Error('HIAPI_API_KEY is not set in the current environment');
  return key;
}

async function imageDataUrl(filePath) {
  const data = await readFile(filePath);
  const extension = extname(filePath).toLowerCase();
  const mime = extension === '.jpg' || extension === '.jpeg' ? 'image/jpeg' : extension === '.webp' ? 'image/webp' : 'image/png';
  return `data:${mime};base64,${data.toString('base64')}`;
}

async function requestJson(url, init) {
  const response = await fetch(url, init);
  const text = await response.text();
  let body;
  try { body = text ? JSON.parse(text) : null; } catch { body = null; }
  if (!response.ok) {
    const message = (body?.error?.message ?? body?.message ?? text) || `HTTP ${response.status}`;
    throw new Error(`HiAPI request failed: ${message}`);
  }
  return body?.data ?? body;
}

function promptFor({ title, issue, chapter }) {
  const badgeText = chapter ? `第 ${chapter} 章 · 第 ${issue} 篇` : `系列第 ${issue} 篇`;
  return [
    'Use the supplied reference image as a locked visual composition for a Chinese WeChat public-account article cover.',
    'Preserve the right-side silver laptop, Windows blue screen, floating terminal/code panels, camera perspective, mint-white luminous background, teal line waves, soft shadows, and the clean 16:9 editorial technology style.',
    'Rebuild only the left 45 percent of the image for this article. Create a topic-relevant, simple editorial illustration or icon behind/around the left text without changing the right-side scene.',
    `Render the exact Chinese issue badge text: ${badgeText}.`,
    `Render the exact Chinese headline: ${title}.`,
    'Make the headline the largest left-side element with strong dark navy/black type and a restrained green/teal accent. Keep all text inside the left safe area and highly legible.',
    'Do not add any other words, logos, watermarks, QR codes, URLs, fake UI copy, or brand marks. Do not alter the chapter number, issue number, or title.',
  ].join(' ');
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (!options) return;
  const apiKey = requireApiKey();
  const reference = await imageDataUrl(options.reference);
  const payload = {
    model: options.model,
    input: {
      resolution: '1K',
      aspect_ratio: '16:9',
      prompt: promptFor(options),
      input_urls: [reference],
    },
  };
  const submitted = await requestJson(`${API_ORIGIN}/v1/tasks`, {
    method: 'POST',
    headers: { Accept: 'application/json', Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json', 'Idempotency-Key': randomUUID() },
    body: JSON.stringify(payload),
  });
  if (!submitted?.taskId) throw new Error('HiAPI response did not include data.taskId');
  process.stderr.write(`Submitted ${submitted.taskId}\n`);

  const deadline = Date.now() + 10 * 60 * 1000;
  let task;
  while (Date.now() < deadline) {
    task = await requestJson(`${API_ORIGIN}/v1/tasks/${encodeURIComponent(submitted.taskId)}`, {
      headers: { Accept: 'application/json', Authorization: `Bearer ${apiKey}` },
    });
    process.stderr.write(`Status: ${task.status}\n`);
    if (task.status === 'success' || task.status === 'fail') break;
    await new Promise((resolveDelay) => setTimeout(resolveDelay, 2000));
  }
  if (!task || task.status !== 'success') throw new Error(`HiAPI task failed or timed out: ${JSON.stringify(task?.error ?? task)}`);
  const output = task.output?.[0];
  if (!output?.url) throw new Error('HiAPI success response did not include output[0].url');
  const imageResponse = await fetch(output.url);
  if (!imageResponse.ok) throw new Error(`Failed to download generated cover: HTTP ${imageResponse.status}`);
  const bytes = Buffer.from(await imageResponse.arrayBuffer());
  await mkdir(dirname(options.output), { recursive: true });
  await writeFile(options.output, bytes);
  process.stdout.write(JSON.stringify({ output: options.output, taskId: submitted.taskId, bytes: bytes.length }) + '\n');
}

main().catch((error) => { console.error(error.message); process.exitCode = 1; });
