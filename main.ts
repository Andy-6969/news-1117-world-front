// Entry for make.fun's news-image-20261117: copies the front page that render.py drew
// (entry.png, 1024x1024 PNG, under 1 MiB) to /output/entry.png.
// Locally: MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
