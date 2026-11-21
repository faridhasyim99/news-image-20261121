import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';

// Deterministic build verification: source bytes are copied unchanged on every run.
const source = join(process.cwd(), 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
const target = join(outDir, 'entry.png');
const bytes = readFileSync(source);
if (bytes.length > 1048576) throw new Error(`entry.png exceeds 1 MiB: ${bytes.length}`);
if (bytes.readUInt32BE(0) !== 0x89504e47 || bytes.readUInt32BE(16) !== 1024 || bytes.readUInt32BE(20) !== 1024) throw new Error('entry.png must be a 1024x1024 PNG');
mkdirSync(outDir, { recursive: true });
writeFileSync(target, bytes);
const written = readFileSync(target);
const digest = (b: Buffer) => createHash('sha256').update(b).digest('hex');
if (!written.equals(bytes) || digest(written) !== digest(bytes)) throw new Error('output read-back differs from entry.png');
