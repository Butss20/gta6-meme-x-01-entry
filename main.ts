// gta6-meme-x-01 entry (Node 22, standard library only).
//
// The entry is the X post itself: this program only hands the grader the
// post's address. It reads POST.json from the repository next to this file
// and writes the same bytes to the output directory, where the gate reads
// them. The house then reads the post from X and judges its first picture
// and its text; nothing this program writes is judged.
//
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const postPath = join(botDir, "POST.json");

let postText: string;
try {
  postText = readFileSync(postPath, "utf8");
} catch (err) {
  console.error(`cannot read ${postPath}: ${(err as Error).message}`);
  process.exit(1);
}

try {
  JSON.parse(postText);
} catch (err) {
  console.error(`POST.json is not valid JSON: ${(err as Error).message}`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "POST.json"), postText);
