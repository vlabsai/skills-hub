---
name: threejs
description: >-
  Guia completo de desenvolvimento Three.js com padroes obrigatorios:
  disposal de recursos, cap de pixel ratio em 2x, color spaces por tipo de
  textura e template scaffold aprovado. Cobre fundamentals, geometria,
  materiais, iluminacao, shaders, interacao e pos-processamento.
license: Apache-2.0
compatibility: claude-code
allowed-tools: Read Write Edit Glob Bash
metadata:
  author: vector-labs
  version: "1.0"
tags: [3d, webgl, graphics]
complexity: advanced
---

# Three.js Best Practices

## Quick Start

```typescript
import * as THREE from "three";

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
document.body.appendChild(renderer.domElement);

// Mesh
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

// Light
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 5, 5);
scene.add(light);
scene.add(new THREE.AmbientLight(0xffffff, 0.3));

camera.position.z = 5;

// Animation loop
const clock = new THREE.Clock();
function animate() {
  const delta = clock.getDelta();
  cube.rotation.x += delta;
  cube.rotation.y += delta;
  renderer.render(scene, camera);
}
renderer.setAnimationLoop(animate);

// Resize
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```

## Topic References

Read the relevant reference file based on the task at hand:

- [references/fundamentals.md](references/fundamentals.md) - Scene, camera, renderer, Object3D, math utilities, coordinate system, cleanup/disposal patterns
- [references/geometry.md](references/geometry.md) - Built-in shapes, custom BufferGeometry, InstancedMesh, points, lines, edges, geometry utilities
- [references/materials.md](references/materials.md) - All material types, PBR workflow (Standard/Physical), environment maps, material properties, multiple materials
- [references/lighting-and-shadows.md](references/lighting-and-shadows.md) - Light types (Ambient, Hemisphere, Directional, Point, Spot, RectArea), shadow setup, IBL/HDR, lighting setups
- [references/textures.md](references/textures.md) - Texture loading/config, color spaces, HDR, render targets, UV mapping, texture atlas, memory management
- [references/animation.md](references/animation.md) - AnimationMixer/Clip/Action, skeletal animation, morph targets, animation blending, procedural animation
- [references/shaders.md](references/shaders.md) - ShaderMaterial, GLSL uniforms/varyings, common shader patterns, extending built-in materials, instanced shaders
- [references/interaction.md](references/interaction.md) - Raycasting, camera controls (Orbit/Fly/PointerLock), TransformControls, DragControls, selection, coordinate conversion
- [references/postprocessing.md](references/postprocessing.md) - EffectComposer, bloom, DOF, SSAO, FXAA/SMAA, custom ShaderPass, selective bloom, multi-pass rendering
- [references/loaders.md](references/loaders.md) - GLTF/Draco loading, OBJ/FBX/STL formats, LoadingManager, async patterns, caching, error handling

## Essential Patterns

**Always dispose resources when done:**
```typescript
geometry.dispose();
material.dispose();
texture.dispose();
renderer.dispose();
```

**Frame-rate-independent animation:** Always use `clock.getDelta()` or `clock.getElapsedTime()`.

**Pixel ratio:** Always `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))` to cap at 2x.

**Color spaces:** Set `texture.colorSpace = THREE.SRGBColorSpace` for color/albedo maps. Leave data maps (normal, roughness, metalness) as default.
