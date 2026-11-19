// News-image entry (Node 22, standard library only).
//
// The finished image lives beside this file as entry.png: a front page
// summing up the world's news of Wednesday 18 November 2026, drawn
// by draw.py. This program's only job is to place that image where the
// grader reads it, as /output/entry.png, byte for byte.
//
// Run it locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, 'entry.png'), join(outDir, 'entry.png'));
