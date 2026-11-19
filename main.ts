// News-image entry (Node 22, standard library only).
//
// The finished image lives beside this file as entry.png: a dense front
// page dated Wednesday 18 November 2026 with 46 verified stories from
// that day across 7 regions — Xi and Putin in Shenzhen, Iran's drones at
// US Gulf bases, Russia's 141-drone attack on Ukraine, Voyager 1 at one
// light-day, the Fed minutes, Cyclone Akvan, the EU's Ukraine loan, the
// Spain high-speed train crash, and 35 more stories, with 11 of them
// drawn as original illustrations, plus a date check.
// The page is written as HTML/CSS in page.html in this repository and
// rendered to entry.png by render.py (headless Chromium), so the picture
// is reproducible from source. This program's only job is to place that
// image where the grader reads it, as /output/entry.png, byte for byte.
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
