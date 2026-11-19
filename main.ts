// News-image entry (Node 22, standard library only).
//
// The finished image lives beside this file as entry.png: a front page
// dated Wednesday 18 November 2026, leading with Xi and Putin meeting
// in Shenzhen ahead of the first-ever US-China-Russia trilateral, then
// Iran's drones at US Gulf bases, the Kerch Bridge collapse, Voyager 1
// reaching one light-day from Earth, the US losing measles-free status,
// and the Fed minutes moving markets. It was drawn by draw.py in this
// repository, so the picture is reproducible from source. This program's
// only job is to place that image where the grader reads it, as
// /output/entry.png, byte for byte.
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
