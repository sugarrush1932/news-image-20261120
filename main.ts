// main.ts — entry program for news-image-20261120 (program/v1, Node 22).
//
// The picture ships in the repository as entry.png, drawn beforehand by
// render.py. This program reads it, checks it is a whole PNG inside the
// competition's limits, and writes it byte for byte to the harness output
// directory as entry.png, so both grading runs produce identical bytes.
//
// Paths are resolved from this file's own location, never from the working
// directory (the grader mounts the repository read-only at an arbitrary
// path). The output directory is $MAKEFUN_OUTPUT_DIR where the driver sets
// it, and /output inside the grader's container.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1048576; // 1 MiB
const MAX_SIDE = 1024;

// First eight bytes of every PNG file.
const SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
// A whole PNG ends with the IEND chunk: zero length, type IEND, fixed CRC.
const TRAILER = Buffer.from([
  0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82,
]);

function loadArtwork(): Buffer {
  const here = dirname(fileURLToPath(import.meta.url));
  const data = readFileSync(join(here, "entry.png"));
  if (data.length > MAX_BYTES) {
    throw new Error(`entry.png is ${data.length} bytes, over the 1 MiB limit`);
  }
  if (!data.subarray(0, SIGNATURE.length).equals(SIGNATURE)) {
    throw new Error("entry.png does not start with the PNG signature");
  }
  // IHDR is the first chunk: width and height are big-endian uint32s at
  // offsets 16 and 20 of the file.
  const width = data.readUInt32BE(16);
  const height = data.readUInt32BE(20);
  if (width > MAX_SIDE || height > MAX_SIDE) {
    throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
  }
  if (!data.subarray(data.length - TRAILER.length).equals(TRAILER)) {
    throw new Error("entry.png is truncated: it does not end with the IEND chunk");
  }
  return data;
}

function main(): void {
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  mkdirSync(outDir, { recursive: true });
  const data = loadArtwork();
  const target = join(outDir, "entry.png");
  writeFileSync(target, data);
  // The grader runs this program twice and requires identical bytes, so a
  // short or torn write must fail loudly here instead of scoring broken.
  const landed = readFileSync(target);
  if (!landed.equals(data)) {
    throw new Error(`write to ${target} did not land byte for byte`);
  }
}

main();
