# Three.js Materials

## Material Types Overview

| Material Type | Use Case | Lighting Support |
|--------------|----------|------------------|
| MeshBasicMaterial | Unlit surfaces, sprites, skybox | None |
| MeshLambertMaterial | Low-cost lit surfaces | Diffuse only |
| MeshPhongMaterial | Shiny surfaces, legacy PBR | Diffuse + Specular |
| MeshStandardMaterial | Modern PBR workflow | Full PBR |
| MeshPhysicalMaterial | Advanced materials (glass, car paint) | Full PBR + Extensions |
| MeshToonMaterial | Cel-shaded cartoon style | Custom gradient |
| MeshNormalMaterial | Debugging normals | None |
| MeshDepthMaterial | Debugging depth, shadows | None |
| PointsMaterial | Particle systems | None |
| LineBasicMaterial | Lines and wireframes | None |
| LineDashedMaterial | Dashed lines | None |
| ShaderMaterial | Custom GLSL with helpers | Custom |
| RawShaderMaterial | Full manual GLSL control | Custom |

## MeshBasicMaterial

Unlit material, ignores all lights. Best for performance or flat designs.

```typescript
const material = new THREE.MeshBasicMaterial({
  color: 0xff0000,
  transparent: true,
  opacity: 0.5,
  wireframe: true,
  map: texture,
  alphaMap: alphaTexture,
  envMap: cubeTexture, // Reflection without lighting
  combine: THREE.MultiplyOperation, // MixOperation, AddOperation
  reflectivity: 0.8,
  refractionRatio: 0.98
});
```

Common uses: Skyboxes, UI elements, debug wireframes, sprites.

## MeshLambertMaterial

Diffuse-only lighting model. Cheap but no specular highlights.

```typescript
const material = new THREE.MeshLambertMaterial({
  color: 0x00ff00,
  emissive: 0x222222, // Self-illumination
  emissiveIntensity: 0.5,
  map: texture,
  emissiveMap: emissiveTexture,
  envMap: cubeTexture
});
```

Use for matte surfaces where performance matters more than realism.

## MeshPhongMaterial

Adds specular highlights. Legacy but still useful for stylized looks.

```typescript
const material = new THREE.MeshPhongMaterial({
  color: 0x0000ff,
  specular: 0x555555, // Highlight color
  shininess: 30, // 0-100+, higher = tighter highlight
  emissive: 0x000000,
  map: texture,
  normalMap: normalTexture,
  normalScale: new THREE.Vector2(1, 1),
  bumpMap: bumpTexture,
  bumpScale: 1,
  displacementMap: dispTexture,
  displacementScale: 1,
  specularMap: specTexture,
  envMap: cubeTexture
});
```

Better than Lambert for shiny surfaces, cheaper than Standard.

## MeshStandardMaterial (PBR)

Modern physically-based rendering. Roughness/metalness workflow.

```typescript
const material = new THREE.MeshStandardMaterial({
  color: 0xffffff,
  roughness: 0.5, // 0 = mirror, 1 = diffuse
  metalness: 0.0, // 0 = dielectric, 1 = metal

  // Full texture set
  map: diffuseTexture,
  roughnessMap: roughnessTexture,
  metalnessMap: metalnessTexture,
  normalMap: normalTexture,
  normalScale: new THREE.Vector2(1, 1),

  aoMap: aoTexture, // Requires UV2
  aoMapIntensity: 1.0,

  displacementMap: dispTexture,
  displacementScale: 1,

  emissive: 0x000000,
  emissiveMap: emissiveTexture,
  emissiveIntensity: 1,

  envMap: cubeTexture,
  envMapIntensity: 1.0
});

// AO map requires UV2 attribute
geometry.setAttribute('uv2', geometry.attributes.uv);
```

### Roughness/Metalness Workflows

**Roughness**: Controls surface microsurface detail
- 0.0 = Perfect mirror (glass, polished metal)
- 0.3 = Glossy plastic, wet surfaces
- 0.7 = Wood, stone
- 1.0 = Chalk, fabric

**Metalness**: Separates metals from dielectrics
- 0.0 = Non-metal (plastic, wood, skin, stone)
- 1.0 = Metal (iron, gold, copper)
- Avoid in-between values (0-1) unless fading

### Environment Map Setup

```typescript
// Cube texture
const cubeLoader = new THREE.CubeTextureLoader();
const envMap = cubeLoader.load([
  'px.jpg', 'nx.jpg', 'py.jpg', 'ny.jpg', 'pz.jpg', 'nz.jpg'
]);
material.envMap = envMap;

// Scene-wide environment (recommended)
scene.environment = envMap; // Auto-applies to all PBR materials
```

## MeshPhysicalMaterial (Advanced PBR)

Extends StandardMaterial with advanced effects.

```typescript
const material = new THREE.MeshPhysicalMaterial({
  // All StandardMaterial properties +

  // Clearcoat (car paint, varnish)
  clearcoat: 1.0, // 0-1
  clearcoatRoughness: 0.1,
  clearcoatMap: clearcoatTexture,
  clearcoatRoughnessMap: clearcoatRoughTexture,
  clearcoatNormalMap: clearcoatNormalTexture,
  clearcoatNormalScale: new THREE.Vector2(1, 1),

  // Transmission (glass, transparent materials)
  transmission: 1.0, // 0-1, use instead of opacity for glass
  transmissionMap: transmissionTexture,
  thickness: 0.5, // Volume thickness for refraction
  thicknessMap: thicknessTexture,
  ior: 1.5, // Index of refraction (glass = 1.5, water = 1.33)

  // Sheen (fabric, velvet)
  sheen: 1.0,
  sheenRoughness: 0.5,
  sheenColor: new THREE.Color(0xffffff),

  // Iridescence (soap bubbles, oil slicks)
  iridescence: 1.0,
  iridescenceIOR: 1.3,
  iridescenceThicknessRange: [100, 400],

  // Anisotropy (brushed metal)
  anisotropy: 1.0,
  anisotropyRotation: 0, // Radians

  // Specular tint (colored reflections)
  specularIntensity: 1.0,
  specularColor: new THREE.Color(0xffffff)
});
```

### Glass Example

```typescript
const glass = new THREE.MeshPhysicalMaterial({
  color: 0xffffff,
  metalness: 0,
  roughness: 0,
  transmission: 1.0, // Fully transparent via refraction
  thickness: 0.5,
  ior: 1.5,
  envMapIntensity: 1.0,
  transparent: false // Use transmission instead
});
```

### Car Paint Example

```typescript
const carPaint = new THREE.MeshPhysicalMaterial({
  color: 0xff0000,
  metalness: 0.3,
  roughness: 0.2,
  clearcoat: 1.0,
  clearcoatRoughness: 0.1,
  envMapIntensity: 1.5
});
```

## MeshToonMaterial

Cel-shading with custom gradient control.

```typescript
// Create custom gradient for banding
const gradientData = new Uint8Array([0, 128, 255]); // 3-band gradient
const gradientTexture = new THREE.DataTexture(
  gradientData,
  gradientData.length,
  1,
  THREE.RedFormat
);
gradientTexture.minFilter = THREE.NearestFilter;
gradientTexture.magFilter = THREE.NearestFilter;
gradientTexture.needsUpdate = true;

const material = new THREE.MeshToonMaterial({
  color: 0xff6347,
  gradientMap: gradientTexture, // Controls shading bands
  map: texture,
  emissive: 0x000000,
  emissiveMap: emissiveTexture
});
```

Without gradientMap, defaults to 2-tone shading.

## MeshNormalMaterial / MeshDepthMaterial

Debug materials for visualizing geometry data.

```typescript
// Normals as RGB
const normalMat = new THREE.MeshNormalMaterial({
  flatShading: false
});

// Depth visualization
const depthMat = new THREE.MeshDepthMaterial({
  depthPacking: THREE.BasicDepthPacking // or RGBADepthPacking
});
```

Useful for debugging normal maps, depth sorting, and geometry issues.

## PointsMaterial

For particle systems and point clouds.

```typescript
const material = new THREE.PointsMaterial({
  color: 0xffffff,
  size: 0.1,
  sizeAttenuation: true, // Scale with distance
  map: texture, // Particle texture
  alphaMap: alphaTexture,
  transparent: true,
  opacity: 0.8,
  alphaTest: 0.5,
  depthWrite: false, // Prevent sorting issues
  blending: THREE.AdditiveBlending // For glowing effects
});

const points = new THREE.Points(geometry, material);
```

## LineBasicMaterial, LineDashedMaterial

```typescript
const basicLine = new THREE.LineBasicMaterial({
  color: 0x0000ff,
  linewidth: 1 // Note: Only works on some platforms
});

const dashedLine = new THREE.LineDashedMaterial({
  color: 0xff0000,
  dashSize: 3,
  gapSize: 1,
  linewidth: 1
});

// LineDashedMaterial requires computeLineDistances
const line = new THREE.Line(geometry, dashedLine);
line.computeLineDistances();
```

## ShaderMaterial

Custom GLSL with automatic uniform handling.

```typescript
const material = new THREE.ShaderMaterial({
  uniforms: {
    time: { value: 0 },
    color: { value: new THREE.Color(0xff0000) },
    texture1: { value: texture }
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform float time;
    uniform vec3 color;
    uniform sampler2D texture1;
    varying vec2 vUv;

    void main() {
      vec4 texColor = texture2D(texture1, vUv);
      gl_FragColor = vec4(color * texColor.rgb, 1.0);
    }
  `,
  transparent: true,
  side: THREE.DoubleSide
});

// Update uniforms in animation loop
material.uniforms.time.value = clock.getElapsedTime();
```

### Built-in Uniforms (Automatically Provided)

```glsl
// Matrices
uniform mat4 modelMatrix;
uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform mat3 normalMatrix;

// Camera
uniform vec3 cameraPosition;

// Fog
uniform vec3 fogColor;
uniform float fogNear;
uniform float fogFar;

// Time (if USE_TIME defined)
uniform float time;
```

### Built-in Attributes

```glsl
attribute vec3 position;
attribute vec3 normal;
attribute vec2 uv;
attribute vec2 uv2;
attribute vec4 color;
attribute vec3 tangent;
```

## RawShaderMaterial

Full manual control, no automatic uniforms or attributes.

```typescript
const material = new THREE.RawShaderMaterial({
  uniforms: {
    time: { value: 0 }
  },
  vertexShader: `
    precision mediump float;
    uniform mat4 modelViewMatrix;
    uniform mat4 projectionMatrix;
    attribute vec3 position;

    void main() {
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    precision mediump float;

    void main() {
      gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
    }
  `
});
```

Use when you need full control or are targeting WebGL2.

## Common Material Properties

```typescript
const material = new THREE.MeshStandardMaterial({
  // Visibility
  visible: true,

  // Transparency
  transparent: false,
  opacity: 1.0,
  alphaTest: 0.5, // Discard pixels below threshold (0-1)

  // Rendering
  side: THREE.FrontSide, // BackSide, DoubleSide
  depthTest: true,
  depthWrite: true,

  // Blending
  blending: THREE.NormalBlending,
  // NoBlending, AdditiveBlending, SubtractiveBlending, MultiplyBlending

  // Advanced
  flatShading: false,
  fog: true, // Affected by scene fog
  toneMapped: true,

  // Stencil buffer
  stencilWrite: false,
  stencilFunc: THREE.AlwaysStencilFunc,
  stencilRef: 0,
  stencilMask: 0xff,

  // Polygon offset (Z-fighting fix)
  polygonOffset: false,
  polygonOffsetFactor: 0,
  polygonOffsetUnits: 0
});
```

### Side Rendering

- `THREE.FrontSide`: Default, cull back faces
- `THREE.BackSide`: Render only back faces (interior views)
- `THREE.DoubleSide`: Render both sides (slower, avoid if possible)

### Alpha Blending Modes

```typescript
// Solid (default)
blending: THREE.NormalBlending

// Additive (glow effects)
blending: THREE.AdditiveBlending
depthWrite: false

// Multiply (shadows, tint)
blending: THREE.MultiplyBlending

// Custom
blending: THREE.CustomBlending
blendSrc: THREE.SrcAlphaFactor
blendDst: THREE.OneMinusSrcAlphaFactor
```

## Multiple Materials

Use geometry groups with material array.

```typescript
const geometry = new THREE.BoxGeometry(1, 1, 1);

// Define groups (start, count, materialIndex)
geometry.clearGroups();
geometry.addGroup(0, 6, 0);  // First 6 vertices use material[0]
geometry.addGroup(6, 6, 1);  // Next 6 use material[1]

const materials = [
  new THREE.MeshStandardMaterial({ color: 0xff0000 }),
  new THREE.MeshStandardMaterial({ color: 0x0000ff })
];

const mesh = new THREE.Mesh(geometry, materials);
```

Common use: Different materials per face or mesh section.

## Environment Maps

### Cube Texture Loader

```typescript
const loader = new THREE.CubeTextureLoader();
const envMap = loader.load([
  'px.jpg', 'nx.jpg', // positive/negative X
  'py.jpg', 'ny.jpg', // positive/negative Y
  'pz.jpg', 'nz.jpg'  // positive/negative Z
]);

material.envMap = envMap;
```

### HDR Environment Maps

```typescript
import { RGBELoader } from 'three/examples/jsm/loaders/RGBELoader.js';

const loader = new RGBELoader();
loader.load('environment.hdr', (texture) => {
  texture.mapping = THREE.EquirectangularReflectionMapping;

  // Apply to scene (recommended)
  scene.environment = texture;
  scene.background = texture; // Optional: use as skybox

  // Or apply to individual materials
  material.envMap = texture;
});
```

### Scene Environment (Recommended)

```typescript
// Auto-applies to all PBR materials
scene.environment = envMap;

// Control intensity per material
material.envMapIntensity = 1.5;
```

## Material Cloning and needsUpdate

```typescript
// Clone material (shares textures, copies properties)
const material2 = material.clone();

// Modify cloned material
material2.color.set(0x00ff00);

// Force shader recompilation when changing certain properties
material.needsUpdate = true; // Required after changing:
// - vertexShader/fragmentShader
// - uniforms structure
// - side, flatShading, fog
// - Adding/removing maps
```

### When needsUpdate is Required

Changes that need `material.needsUpdate = true`:
- Changing shader code
- Adding/removing texture maps
- Changing `side`, `flatShading`, `fog`
- Changing material type properties that affect shader compilation

Changes that don't need it:
- Uniform values (`material.uniforms.time.value`)
- Color values (`material.color.set()`)
- Numeric properties (`roughness`, `metalness`, `opacity`)

## Performance Tips

### Material Reuse for Batching

```typescript
// Share material across meshes for better batching
const sharedMat = new THREE.MeshStandardMaterial({ color: 0xff0000 });

for (let i = 0; i < 1000; i++) {
  const mesh = new THREE.Mesh(geometry, sharedMat); // Reuse
  scene.add(mesh);
}
```

### Alpha Test vs Transparency

```typescript
// Faster: Use alphaTest for cutout textures (leaves, grass)
const cutoutMat = new THREE.MeshStandardMaterial({
  map: texture,
  alphaTest: 0.5,
  transparent: false, // Not needed with alphaTest
  side: THREE.DoubleSide
});

// Slower: Full transparency requires sorting
const transparentMat = new THREE.MeshStandardMaterial({
  transparent: true,
  opacity: 0.5,
  depthWrite: false
});
```

### Use Simplest Material Possible

Performance hierarchy (fast to slow):
1. MeshBasicMaterial (no lighting)
2. MeshLambertMaterial (diffuse only)
3. MeshPhongMaterial (specular)
4. MeshStandardMaterial (PBR)
5. MeshPhysicalMaterial (advanced PBR)
6. ShaderMaterial (custom)

### Material Pooling Pattern

```typescript
class MaterialPool {
  private pool: Map<string, THREE.Material> = new Map();

  get(key: string, factory: () => THREE.Material): THREE.Material {
    if (!this.pool.has(key)) {
      this.pool.set(key, factory());
    }
    return this.pool.get(key)!;
  }

  dispose() {
    this.pool.forEach(mat => mat.dispose());
    this.pool.clear();
  }
}

// Usage
const pool = new MaterialPool();
const mat = pool.get('red-metal', () =>
  new THREE.MeshStandardMaterial({
    color: 0xff0000,
    metalness: 1,
    roughness: 0.2
  })
);
```

### Texture Optimization

```typescript
// Reuse textures across materials
const texture = textureLoader.load('diffuse.jpg');
texture.minFilter = THREE.LinearMipMapLinearFilter;
texture.magFilter = THREE.LinearFilter;
texture.anisotropy = renderer.capabilities.getMaxAnisotropy();

// Share across materials
const mat1 = new THREE.MeshStandardMaterial({ map: texture });
const mat2 = new THREE.MeshStandardMaterial({ map: texture });

// Dispose when done
material.dispose();
texture.dispose();
```

### Avoid DoubleSide When Possible

```typescript
// Slower: Renders twice
material.side = THREE.DoubleSide;

// Faster: Duplicate geometry with flipped normals if needed
geometry = geometry.clone();
geometry.scale(-1, 1, 1); // Flip inside-out
```

## See Also

- [Textures](textures.md) - Texture loading, UV mapping, and memory management
- [Lighting & Shadows](lighting-and-shadows.md) - How lights interact with materials
- [Shaders](shaders.md) - Custom ShaderMaterial and extending built-in materials
- [Geometry](geometry.md) - Geometry types that materials are applied to
