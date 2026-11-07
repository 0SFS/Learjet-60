import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

// Rebuild from the user's unmodified Sketchfab archive. Keep its geometry,
// transforms and embedded JPEGs; apply white paint to the exterior assemblies.
const archive = process.argv[2];
if (!archive) throw new Error('Usage: node scripts/prepare-hd.mjs /path/to/bombardier-learjet-60.zip');
const source = execFileSync('unzip', ['-p', archive, 'source/Bombardier Learjet 60.glb'], { maxBuffer: 10 * 1024 * 1024 });
const sourceSha256 = createHash('sha256').update(source).digest('hex');
if (sourceSha256 !== '628b40536e7af862e9e47f85e3517e47cd6cf14e796f014cbd20a7e0f5bd0fde') {
  throw new Error('The source GLB differs from the inspected archive; inspect the new source before importing it.');
}
if (source.readUInt32LE(0) !== 0x46546c67 || source.readUInt32LE(4) !== 2 || source.readUInt32LE(8) !== source.length) {
  throw new Error('Expected a complete GLB 2 file.');
}
const chunks = [];
for (let offset = 12; offset < source.length;) {
  const length = source.readUInt32LE(offset), type = source.readUInt32LE(offset + 4);
  chunks.push({ type, bytes: source.subarray(offset + 8, offset + 8 + length) });
  offset += 8 + length;
}
const jsonChunk = chunks.find(chunk => chunk.type === 0x4e4f534a);
const gltf = JSON.parse(jsonChunk.bytes.toString('utf8'));
if (gltf.images.length !== 12 || gltf.images.some(image => image.bufferView === undefined || image.uri !== undefined)) {
  throw new Error('Expected all twelve source textures to be embedded.');
}

// Paint only the exterior shells. The source materials are also used by lights
// and engine internals, so keep them and assign a separate paint material to
// these mesh primitives. Glazing, chrome, fans, lights and the cabin retain
// their authored materials. No texture processing or runtime shader is needed.
const paintAssemblies = {
  node_10: 'material22', // fuselage shell
  node_15: 'material14', // horizontal tail
  node_16: 'material39', // wing surfaces
  node_17: 'material40',
  node_19: 'material25',
  node_22: 'material24',
  node_23: 'material16', // nacelle shells; fan meshes remain unchanged
  node_25: 'material13', // horizontal tail
  node_26: 'material17', // fuselage fairings and vertical tail
};
const whitePaint = gltf.materials.length;
gltf.materials.push({
  name: 'Learjet60_WhitePaint',
  pbrMetallicRoughness: {
    baseColorFactor: [1, 1, 1, 1],
    metallicFactor: 0,
    roughnessFactor: 0.3,
  },
});
for (const [nodeName, expectedMaterial] of Object.entries(paintAssemblies)) {
  const node = gltf.nodes.find(node => node.name === nodeName);
  const primitives = gltf.meshes[node?.mesh]?.primitives;
  if (!primitives?.length || primitives.some(primitive => gltf.materials[primitive.material]?.name !== expectedMaterial)) {
    throw new Error(`Expected exterior assembly ${nodeName} to use ${expectedMaterial}.`);
  }
  for (const primitive of primitives) primitive.material = whitePaint;
}
gltf.asset.copyright = 'Bombardier Learjet 60 by OUTPISTON (https://sketchfab.com/outpiston), CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/).';
gltf.asset.extras = {
  ...gltf.asset.extras,
  sourceUrl: 'https://sketchfab.com/3d-models/bombardier-learjet-60-7573f836dd3a46bdbce8b90b5a40f104',
  sourceSha256,
  changes: 'Added attribution and provenance metadata. Replaced black exterior paint with a white paint material on the fuselage, wings, tail and nacelle shells. Source geometry, coordinate frame, embedded textures and other material assignments preserved.',
  defaultPaint: 'white',
  metresPerSourceUnit: 1,
};
const json = Buffer.from(JSON.stringify(gltf));
jsonChunk.bytes = Buffer.concat([json, Buffer.alloc((4 - json.length % 4) % 4, 0x20)]);
const header = Buffer.from(source.subarray(0, 12));
header.writeUInt32LE(12 + chunks.reduce((sum, chunk) => sum + 8 + chunk.bytes.length, 0), 8);
const result = [header];
for (const chunk of chunks) {
  const chunkHeader = Buffer.alloc(8);
  chunkHeader.writeUInt32LE(chunk.bytes.length, 0); chunkHeader.writeUInt32LE(chunk.type, 4);
  result.push(chunkHeader, chunk.bytes);
}
const output = fileURLToPath(new URL('../public/aircraft/learjet-60/Learjet_60_HD.glb', import.meta.url));
await mkdir(fileURLToPath(new URL('../public/aircraft/learjet-60/', import.meta.url)), { recursive: true });
await writeFile(output, Buffer.concat(result));
console.log(JSON.stringify({ output, sourceSha256, triangles: 25176, embeddedTextures: 12, metresPerSourceUnit: 1, defaultPaint: 'white' }));
