# Three.js Textures

## Texture Loading

### TextureLoader with callbacks
```typescript
const loader = new THREE.TextureLoader();
loader.load(
  'texture.jpg',
  (texture) => { /* success */ },
  (progress) => { /* loading */ },
  (error) => { /* error */ }
);
```

### Promise wrapper for async/await
```typescript
function loadTexture(url: string): Promise<THREE.Texture> {
  return new Promise((resolve, reject) => {
    new THREE.TextureLoader().load(url, resolve, undefined, reject);
  });
}

// Usage
const texture = await loadTexture('texture.jpg');
```

### LoadingManager for multiple textures
```typescript
const manager = new THREE.LoadingManager();
manager.onLoad = () => console.log('All loaded');
manager.onProgress = (url, loaded, total) => console.log(`${loaded}/${total}`);

const loader = new THREE.TextureLoader(manager);
const tex1 = loader.load('tex1.jpg');
const tex2 = loader.load('tex2.jpg');
```

## Texture Configuration

### Color space - CRITICAL
```typescript
// Color maps (albedo, emissive) - ALWAYS use SRGBColorSpace
texture.colorSpace = THREE.SRGBColorSpace;

// Data maps (normal, roughness, metalness, ao, displacement) - NO color space
normalMap.colorSpace = THREE.NoColorSpace; // default
```

### Wrapping modes
```typescript
texture.wrapS = THREE.RepeatWrapping;
texture.wrapT = THREE.RepeatWrapping;
// Options: ClampToEdgeWrapping (default), RepeatWrapping, MirroredRepeatWrapping

texture.repeat.set(4, 4);
texture.offset.set(0.5, 0.5);
texture.rotation = Math.PI / 4; // radians
texture.center.set(0.5, 0.5); // rotation pivot
```

### Filtering
```typescript
// Minification (texture smaller than surface)
texture.minFilter = THREE.LinearMipmapLinearFilter; // default, best quality
// Options: NearestFilter, LinearFilter, NearestMipmapNearestFilter, etc.

// Magnification (texture larger than surface)
texture.magFilter = THREE.LinearFilter; // default
// Options: NearestFilter, LinearFilter

// Anisotropic filtering (better quality at angles)
const maxAnisotropy = renderer.capabilities.getMaxAnisotropy();
texture.anisotropy = maxAnisotropy; // typically 16
```

### Mipmaps
```typescript
texture.generateMipmaps = true; // default
texture.minFilter = THREE.LinearMipmapLinearFilter;

// Disable for non-power-of-2 or custom mipmaps
texture.generateMipmaps = false;
texture.minFilter = THREE.LinearFilter;
```

## Texture Types

### Regular Texture
```typescript
const texture = new THREE.TextureLoader().load('image.jpg');
```

### DataTexture (raw pixel data)
```typescript
const width = 256, height = 256;
const size = width * height;
const data = new Uint8Array(4 * size); // RGBA

for (let i = 0; i < size; i++) {
  const stride = i * 4;
  data[stride] = 255;     // R
  data[stride + 1] = 0;   // G
  data[stride + 2] = 0;   // B
  data[stride + 3] = 255; // A
}

const texture = new THREE.DataTexture(data, width, height);
texture.colorSpace = THREE.SRGBColorSpace;
texture.needsUpdate = true;
```

### CanvasTexture (2D canvas)
```typescript
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
ctx.fillStyle = '#ff0000';
ctx.fillRect(0, 0, 256, 256);

const texture = new THREE.CanvasTexture(canvas);
texture.colorSpace = THREE.SRGBColorSpace;
texture.needsUpdate = true; // call when canvas updates
```

### VideoTexture (auto-updates)
```typescript
const video = document.createElement('video');
video.src = 'video.mp4';
video.loop = true;
video.muted = true;
video.play();

const texture = new THREE.VideoTexture(video);
texture.colorSpace = THREE.SRGBColorSpace;
// Auto-updates each frame while video plays
```

### Compressed textures (KTX2/Basis)
```typescript
import { KTX2Loader } from 'three/examples/jsm/loaders/KTX2Loader';

const ktx2Loader = new KTX2Loader();
ktx2Loader.setTranscoderPath('basis/');
ktx2Loader.detectSupport(renderer);

const texture = await ktx2Loader.loadAsync('texture.ktx2');
```

## Cube Textures

### CubeTextureLoader for skyboxes/envmaps
```typescript
const loader = new THREE.CubeTextureLoader();
const cubeTexture = loader.load([
  'px.jpg', 'nx.jpg', // +X, -X
  'py.jpg', 'ny.jpg', // +Y, -Y
  'pz.jpg', 'nz.jpg'  // +Z, -Z
]);

scene.background = cubeTexture;
material.envMap = cubeTexture;
```

### Equirectangular to cubemap with PMREMGenerator
```typescript
import { RGBELoader } from 'three/examples/jsm/loaders/RGBELoader';

const rgbeLoader = new RGBELoader();
const hdrTexture = await rgbeLoader.loadAsync('env.hdr');

const pmremGenerator = new THREE.PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();
const envMap = pmremGenerator.fromEquirectangular(hdrTexture).texture;

scene.environment = envMap;
scene.background = envMap;

hdrTexture.dispose();
pmremGenerator.dispose();
```

## HDR Textures

### RGBELoader (.hdr files)
```typescript
import { RGBELoader } from 'three/examples/jsm/loaders/RGBELoader';

const loader = new RGBELoader();
const texture = await loader.loadAsync('environment.hdr');
texture.mapping = THREE.EquirectangularReflectionMapping;
```

### EXRLoader (.exr files)
```typescript
import { EXRLoader } from 'three/examples/jsm/loaders/EXRLoader';

const loader = new EXRLoader();
const texture = await loader.loadAsync('environment.exr');
texture.mapping = THREE.EquirectangularReflectionMapping;
```

### Background options
```typescript
scene.background = texture; // Direct background
scene.environment = texture; // Environment lighting for all PBR materials
scene.backgroundBlurriness = 0.5; // 0-1, blurs background
scene.backgroundIntensity = 1.0; // Brightness multiplier
```

## Render Targets

### WebGLRenderTarget
```typescript
const renderTarget = new THREE.WebGLRenderTarget(512, 512, {
  minFilter: THREE.LinearFilter,
  magFilter: THREE.LinearFilter,
  format: THREE.RGBAFormat,
  type: THREE.UnsignedByteType
});

// Render to target
renderer.setRenderTarget(renderTarget);
renderer.render(scene, camera);
renderer.setRenderTarget(null);

// Use as texture
material.map = renderTarget.texture;
```

### Depth texture
```typescript
const renderTarget = new THREE.WebGLRenderTarget(512, 512);
renderTarget.depthTexture = new THREE.DepthTexture(512, 512);
renderTarget.depthTexture.type = THREE.FloatType;

// Access depth in material
material.map = renderTarget.depthTexture;
```

### Multi-sample anti-aliasing (MSAA)
```typescript
const renderTarget = new THREE.WebGLRenderTarget(512, 512, {
  samples: 4 // MSAA samples (0 = off, 4 or 8 recommended)
});
```

## CubeCamera

### Dynamic environment maps
```typescript
const cubeRenderTarget = new THREE.WebGLCubeRenderTarget(256);
const cubeCamera = new THREE.CubeCamera(0.1, 1000, cubeRenderTarget);

// Update environment map
function updateEnvMap(reflectiveObject) {
  reflectiveObject.visible = false; // Hide to avoid self-reflection
  cubeCamera.update(renderer, scene);
  reflectiveObject.visible = true;
}

material.envMap = cubeRenderTarget.texture;

// In animation loop
updateEnvMap(sphereMesh);
```

## UV Mapping

### Accessing/modifying UVs
```typescript
const geometry = new THREE.PlaneGeometry(1, 1);
const uvAttribute = geometry.attributes.uv;

for (let i = 0; i < uvAttribute.count; i++) {
  const u = uvAttribute.getX(i);
  const v = uvAttribute.getY(i);

  // Modify UVs
  uvAttribute.setXY(i, u * 2, v * 2);
}

uvAttribute.needsUpdate = true;
```

### Second UV channel for aoMap
```typescript
// Clone UV to UV2 for ambient occlusion
geometry.attributes.uv2 = geometry.attributes.uv.clone();

material.aoMap = aoTexture;
material.aoMapIntensity = 1.0;
```

### UV transform in shaders
```typescript
const material = new THREE.ShaderMaterial({
  uniforms: {
    map: { value: texture },
    uvTransform: { value: new THREE.Matrix3() }
  },
  vertexShader: `
    varying vec2 vUv;
    uniform mat3 uvTransform;
    void main() {
      vUv = (uvTransform * vec3(uv, 1.0)).xy;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform sampler2D map;
    varying vec2 vUv;
    void main() {
      gl_FragColor = texture2D(map, vUv);
    }
  `
});
```

## Texture Atlas

### Multiple images in one texture
```typescript
// Atlas with 4 sprites in 2x2 grid
const atlas = new THREE.TextureLoader().load('atlas.png');

// Select sprite at (0, 1) in 2x2 grid
const spriteSize = 0.5;
atlas.repeat.set(spriteSize, spriteSize);
atlas.offset.set(0 * spriteSize, 1 * spriteSize);

material.map = atlas;
```

## Material Texture Maps

### Complete PBR material setup
```typescript
const material = new THREE.MeshStandardMaterial({
  // Color maps - SRGBColorSpace
  map: colorTexture,                 // Albedo/diffuse
  emissiveMap: emissiveTexture,

  // Data maps - NoColorSpace (default)
  normalMap: normalTexture,
  normalScale: new THREE.Vector2(1, 1),

  roughnessMap: roughnessTexture,
  roughness: 1.0,

  metalnessMap: metalnessTexture,
  metalness: 1.0,

  aoMap: aoTexture,
  aoMapIntensity: 1.0,

  displacementMap: displacementTexture,
  displacementScale: 0.1,
  displacementBias: 0,

  alphaMap: alphaTexture,
  transparent: true,

  envMap: envMapTexture
});

// Set color space correctly
colorTexture.colorSpace = THREE.SRGBColorSpace;
emissiveTexture.colorSpace = THREE.SRGBColorSpace;
```

## Normal Map Types

### TangentSpace (default, most common)
```typescript
material.normalMap = normalTexture;
material.normalMapType = THREE.TangentSpaceNormalMap; // default
material.normalScale.set(1, 1); // Adjust strength
```

### ObjectSpace (rare, world-aligned)
```typescript
material.normalMap = normalTexture;
material.normalMapType = THREE.ObjectSpaceNormalMap;
```

## Procedural Textures

### Noise generation with DataTexture
```typescript
function generateNoiseTexture(width: number, height: number): THREE.DataTexture {
  const size = width * height;
  const data = new Uint8Array(4 * size);

  for (let i = 0; i < size; i++) {
    const stride = i * 4;
    const value = Math.random() * 255;
    data[stride] = value;
    data[stride + 1] = value;
    data[stride + 2] = value;
    data[stride + 3] = 255;
  }

  const texture = new THREE.DataTexture(data, width, height);
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.needsUpdate = true;
  return texture;
}
```

### Gradient generation
```typescript
function generateGradientTexture(width: number, height: number): THREE.DataTexture {
  const size = width * height;
  const data = new Uint8Array(4 * size);

  for (let i = 0; i < size; i++) {
    const x = i % width;
    const y = Math.floor(i / width);
    const stride = i * 4;

    const gradient = x / width * 255;
    data[stride] = gradient;
    data[stride + 1] = gradient;
    data[stride + 2] = gradient;
    data[stride + 3] = 255;
  }

  const texture = new THREE.DataTexture(data, width, height);
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.needsUpdate = true;
  return texture;
}
```

## Texture Memory Management

### Dispose patterns
```typescript
// Dispose single texture
texture.dispose();

// Dispose material textures
function disposeMaterialTextures(material: THREE.Material) {
  const textures = [
    'map', 'normalMap', 'roughnessMap', 'metalnessMap',
    'aoMap', 'emissiveMap', 'displacementMap', 'alphaMap',
    'envMap', 'lightMap', 'bumpMap', 'specularMap'
  ];

  textures.forEach(key => {
    if (material[key]) {
      material[key].dispose();
    }
  });
}

// Dispose mesh
function disposeMesh(mesh: THREE.Mesh) {
  mesh.geometry.dispose();
  if (Array.isArray(mesh.material)) {
    mesh.material.forEach(mat => {
      disposeMaterialTextures(mat);
      mat.dispose();
    });
  } else {
    disposeMaterialTextures(mesh.material);
    mesh.material.dispose();
  }
}
```

### TexturePool class for reuse
```typescript
class TexturePool {
  private cache = new Map<string, THREE.Texture>();
  private loader = new THREE.TextureLoader();

  load(url: string): THREE.Texture {
    if (this.cache.has(url)) {
      return this.cache.get(url)!;
    }

    const texture = this.loader.load(url);
    this.cache.set(url, texture);
    return texture;
  }

  dispose() {
    this.cache.forEach(texture => texture.dispose());
    this.cache.clear();
  }
}

const texturePool = new TexturePool();
const texture1 = texturePool.load('texture.jpg');
const texture2 = texturePool.load('texture.jpg'); // Reuses same texture
```

## Performance Tips

### Power-of-2 textures
```typescript
// Optimal: 256, 512, 1024, 2048, 4096
// Non-power-of-2 textures have limitations:
// - Cannot use mipmaps
// - Must use ClampToEdgeWrapping
// - Slower on some GPUs

const texture = loader.load('npot-texture.jpg');
texture.wrapS = THREE.ClampToEdgeWrapping;
texture.wrapT = THREE.ClampToEdgeWrapping;
texture.minFilter = THREE.LinearFilter;
texture.generateMipmaps = false;
```

### KTX2/Basis compression (massive savings)
```typescript
// 50-75% smaller file size + GPU compressed format
// Use basis_universal to convert: PNG/JPG -> KTX2
import { KTX2Loader } from 'three/examples/jsm/loaders/KTX2Loader';

const ktx2Loader = new KTX2Loader();
ktx2Loader.setTranscoderPath('basis/');
ktx2Loader.detectSupport(renderer);

const texture = await ktx2Loader.loadAsync('texture.ktx2');
```

### Texture atlases reduce draw calls
```typescript
// Instead of 100 textures, use 1 atlas with 100 sprites
```

### Mipmaps reduce aliasing and improve performance
```typescript
texture.generateMipmaps = true; // Always enable for power-of-2 textures
```

### Reasonable size limits
```typescript
// Mobile: 1024px max
// Desktop: 2048px typical, 4096px high-end
// Avoid 8192px unless absolutely necessary
```

### Reuse textures across materials
```typescript
const sharedTexture = loader.load('shared.jpg');
material1.map = sharedTexture;
material2.map = sharedTexture;
material3.map = sharedTexture;
```

## See Also

- [Materials](materials.md) - Applying textures to material properties
- [Lighting & Shadows](lighting-and-shadows.md) - HDR/IBL environment lighting
- [Loaders](loaders.md) - Asset loading patterns and caching
- [Shaders](shaders.md) - Custom texture sampling in GLSL
