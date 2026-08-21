#!/usr/bin/env node

import { randomUUID } from 'node:crypto';
import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';

const API_ORIGIN = 'https://api.hiapi.ai';
const MODEL = 'gpt-image-2/text-to-image';

function usage(message) {
  if (message) console.error(`Error: ${message}`);
  console.error('Usage: node generate.mjs --name figure-01 --ratio 1:1 --prompt "..." [--outdir .]');
  process.exitCode = 2;
}

function parseArgs(argv) {
  const options = { outdir: '.', ratio: '1:1' };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--name' || arg === '--ratio' || arg === '--prompt' || arg === '--outdir') {
      const value = argv[++i];
      if (!value) return usage(`${arg} requires a value`);
      options[arg.slice(2)] = value;
    } else {
      return usage(`unknown argument: ${arg}`);
    }
  }
  if (!options.name?.trim()) return usage('--name is required');
  if (!options.prompt?.trim()) return usage('--prompt is required');
  return options;
}

function requireApiKey() {
  const key = process.env.HIAPI_API_KEY?.trim();
  if (!key) throw new Error('HIAPI_API_KEY is not set in the current environment');
  return key;
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

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (!options) return;
  const apiKey = requireApiKey();
  const payload = {
    model: MODEL,
    input: {
      resolution: '1K',
      aspect_ratio: options.ratio,
      prompt: options.prompt,
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
    await new Promise((r) => setTimeout(r, 2000));
  }
  if (!task || task.status !== 'success') throw new Error(`HiAPI task failed or timed out: ${JSON.stringify(task?.error ?? task)}`);
  const output = task.output?.[0];
  if (!output?.url) throw new Error('HiAPI success response did not include output[0].url');
  const imageResponse = await fetch(output.url);
  if (!imageResponse.ok) throw new Error(`Failed to download image: HTTP ${imageResponse.status}`);
  const bytes = Buffer.from(await imageResponse.arrayBuffer());
  const outPath = resolve(options.outdir, `${options.name}.png`);
  await mkdir(dirname(outPath), { recursive: true });
  await writeFile(outPath, bytes);
  process.stdout.write(JSON.stringify({ output: outPath, taskId: submitted.taskId, bytes: bytes.length }) + '\n');
}

main().catch((error) => { console.error(error.message); process.exitCode = 1; });
