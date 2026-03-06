# Three.js Loaders

## LoadingManager

Coordinates multiple loaders with unified callbacks:

```javascript
const manager = new THREE.LoadingManager();

manager.onStart = (url, itemsLoaded, itemsTotal) => {
  console.log(`Started loading: ${url}`);
};

manager.onLoad = () => {
  console.log('All assets loaded');
};

manager.onProgress = (url, itemsLoaded, itemsTotal) => {
  console.log(`Loading: ${itemsLoaded}/${itemsTotal}`);
};

manager.onError = (url) => {
  console.error(`Error loading: ${url}`);
};

// Use with any loader
const textureLoader = new THREE.TextureLoader(manager);
const gltfLoader = new THREE.GLTFLoader(manager);
```

## Texture Loading

### TextureLoader

```javascript
// Callback style
const loader = new THREE.TextureLoader();
loader.load(
  'texture.jpg',
  (texture) => {
    material.map = texture;
    material.needsUpdate = true;
  },
  undefined,
  (error) => console.error(error)
);

// Synchronous style (starts loading immediately)
const texture = loader.load('texture.jpg');
material.map = texture;
```

### Texture Configuration

```javascript
const texture = loader.load('texture.jpg');

// Color space (important for correct rendering)
texture.colorSpace = THREE.SRGBColorSpace; // For color textures
texture.colorSpace = THREE.LinearSRGBColorSpace; // For data textures (normal, roughness, etc.)

// Wrapping
texture.wrapS = THREE.RepeatWrapping;
texture.wrapT = THREE.RepeatWrapping;
texture.repeat.set(4, 4);

// Filtering
texture.minFilter = THREE.LinearMipmapLinearFilter;
texture.magFilter = THREE.LinearFilter;

// Anisotropic filtering (better quality at angles)
const maxAnisotropy = renderer.capabilities.getMaxAnisotropy();
texture.anisotropy = maxAnisotropy;

// Flip Y (some formats need this)
texture.flipY = false;
```

### CubeTextureLoader

```javascript
const cubeLoader = new THREE.CubeTextureLoader();
const envMap = cubeLoader.load([
  'px.jpg', 'nx.jpg',
  'py.jpg', 'ny.jpg',
  'pz.jpg', 'nz.jpg'
]);

scene.background = envMap;
material.envMap = envMap;
```

### HDR/EXR Loading

```javascript
import { RGBELoader } from 'three/examples/jsm/loaders/RGBELoader.js';
import { EXRLoader } from 'three/examples/jsm/loaders/EXRLoader.js';

// HDR
const rgbeLoader = new RGBELoader();
rgbeLoader.load('environment.hdr', (texture) => {
  texture.mapping = THREE.EquirectangularReflectionMapping;
  scene.background = texture;
  scene.environment = texture;
});

// EXR
const exrLoader = new EXRLoader();
exrLoader.load('environment.exr', (texture) => {
  texture.mapping = THREE.EquirectangularReflectionMapping;
  scene.environment = texture;
});
```

### PMREMGenerator for PBR

```javascript
import { PMREMGenerator } from 'three';

const pmremGenerator = new PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();

rgbeLoader.load('environment.hdr', (texture) => {
  const envMap = pmremGenerator.fromEquirectangular(texture).texture;
  scene.environment = envMap;
  texture.dispose();
  pmremGenerator.dispose();
});
```

## GLTF/GLB Loading

### Basic GLTFLoader

```javascript
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const loader = new GLTFLoader();
loader.load('model.glb', (gltf) => {
  const model = gltf.scene;
  scene.add(model);

  // Access animations
  const mixer = new THREE.AnimationMixer(model);
  gltf.animations.forEach((clip) => {
    mixer.clipAction(clip).play();
  });

  // Access cameras
  const camera = gltf.cameras[0];

  // Asset info
  console.log(gltf.asset);
});
```

### GLTF with Draco Compression

```javascript
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';

const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('/draco/'); // Path to decoder files
dracoLoader.setDecoderConfig({ type: 'js' }); // or 'wasm'

const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(dracoLoader);

gltfLoader.load('compressed.glb', (gltf) => {
  scene.add(gltf.scene);
});

// Cleanup when done
dracoLoader.dispose();
```

### GLTF with KTX2 Textures

```javascript
import { KTX2Loader } from 'three/examples/jsm/loaders/KTX2Loader.js';

const ktx2Loader = new KTX2Loader();
ktx2Loader.setTranscoderPath('/basis/');
ktx2Loader.detectSupport(renderer);

const gltfLoader = new GLTFLoader();
gltfLoader.setKTX2Loader(ktx2Loader);

gltfLoader.load('model.glb', (gltf) => {
  scene.add(gltf.scene);
});

// Cleanup
ktx2Loader.dispose();
```

### Processing GLTF Content

```javascript
loader.load('model.glb', (gltf) => {
  const model = gltf.scene;

  // Enable shadows via traverse
  model.traverse((node) => {
    if (node.isMesh) {
      node.castShadow = true;
      node.receiveShadow = true;
    }
  });

  // Find by name
  const specificMesh = model.getObjectByName('MeshName');

  // Adjust materials
  model.traverse((node) => {
    if (node.isMesh && node.material) {
      node.material.roughness = 0.5;
      node.material.metalness = 1.0;
    }
  });

  // Center and scale
  const box = new THREE.Box3().setFromObject(model);
  const center = box.getCenter(new THREE.Vector3());
  const size = box.getSize(new THREE.Vector3());

  model.position.sub(center); // Center
  const maxDim = Math.max(size.x, size.y, size.z);
  model.scale.setScalar(2 / maxDim); // Scale to fit

  scene.add(model);
});
```

## Other Model Formats

### OBJ+MTL

```javascript
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';
import { MTLLoader } from 'three/examples/jsm/loaders/MTLLoader.js';

const mtlLoader = new MTLLoader();
mtlLoader.load('model.mtl', (materials) => {
  materials.preload();

  const objLoader = new OBJLoader();
  objLoader.setMaterials(materials);
  objLoader.load('model.obj', (object) => {
    scene.add(object);
  });
});
```

### FBX

```javascript
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader.js';

const loader = new FBXLoader();
loader.load('model.fbx', (object) => {
  // FBX often needs scaling
  object.scale.setScalar(0.01);

  // Access animations
  if (object.animations.length > 0) {
    const mixer = new THREE.AnimationMixer(object);
    object.animations.forEach((clip) => {
      mixer.clipAction(clip).play();
    });
  }

  scene.add(object);
});
```

### STL

```javascript
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader.js';

const loader = new STLLoader();
loader.load('model.stl', (geometry) => {
  const material = new THREE.MeshPhongMaterial({ color: 0x888888 });
  const mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);
});
```

### PLY

```javascript
import { PLYLoader } from 'three/examples/jsm/loaders/PLYLoader.js';

const loader = new PLYLoader();
loader.load('model.ply', (geometry) => {
  geometry.computeVertexNormals();

  // PLY can contain vertex colors
  const material = new THREE.MeshStandardMaterial({
    vertexColors: geometry.hasAttribute('color')
  });

  const mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);
});
```

## Async/Promise Loading

### Promisified Loader Pattern

```javascript
function loadGLTF(url) {
  return new Promise((resolve, reject) => {
    const loader = new GLTFLoader();
    loader.load(url, resolve, undefined, reject);
  });
}

// Usage
async function init() {
  try {
    const gltf = await loadGLTF('model.glb');
    scene.add(gltf.scene);
  } catch (error) {
    console.error('Failed to load model:', error);
  }
}

// Or with loadAsync (available in newer versions)
const gltf = await loader.loadAsync('model.glb');
```

### Loading Multiple Assets

```javascript
async function loadAssets() {
  const textureLoader = new THREE.TextureLoader();
  const gltfLoader = new GLTFLoader();

  const [texture, model, envMap] = await Promise.all([
    textureLoader.loadAsync('texture.jpg'),
    gltfLoader.loadAsync('model.glb'),
    new RGBELoader().loadAsync('env.hdr')
  ]);

  return { texture, model, envMap };
}
```

## Caching

### Built-in Cache

```javascript
// Enable global cache
THREE.Cache.enabled = true;

// Same URL will be loaded only once
loader.load('texture.jpg'); // Loads from network
loader.load('texture.jpg'); // Returns from cache

// Clear cache
THREE.Cache.clear();

// Remove specific file
THREE.Cache.remove('texture.jpg');
```

### Custom AssetManager

```javascript
class AssetManager {
  constructor() {
    this.textures = new Map();
    this.models = new Map();
    this.textureLoader = new THREE.TextureLoader();
    this.gltfLoader = new GLTFLoader();
  }

  async loadTexture(url, clone = false) {
    if (this.textures.has(url)) {
      const cached = this.textures.get(url);
      return clone ? cached.clone() : cached;
    }

    const texture = await this.textureLoader.loadAsync(url);
    this.textures.set(url, texture);
    return texture;
  }

  async loadModel(url, clone = false) {
    if (this.models.has(url)) {
      const cached = this.models.get(url);
      return clone ? cached.scene.clone() : cached.scene;
    }

    const gltf = await this.gltfLoader.loadAsync(url);
    this.models.set(url, gltf);
    return gltf.scene;
  }

  dispose() {
    this.textures.forEach(texture => texture.dispose());
    this.models.forEach(gltf => {
      gltf.scene.traverse(node => {
        if (node.geometry) node.geometry.dispose();
        if (node.material) {
          if (Array.isArray(node.material)) {
            node.material.forEach(mat => mat.dispose());
          } else {
            node.material.dispose();
          }
        }
      });
    });
    this.textures.clear();
    this.models.clear();
  }
}

// Usage
const assets = new AssetManager();
const texture = await assets.loadTexture('texture.jpg');
const model = await assets.loadModel('model.glb', true); // Clone for instancing
```

## Loading from Different Sources

### Data URL/Base64

```javascript
const dataUrl = 'data:image/png;base64,iVBORw0KGgoAAAANS...';
const texture = textureLoader.load(dataUrl);
```

### Blob URL

```javascript
const response = await fetch('texture.jpg');
const blob = await response.blob();
const blobUrl = URL.createObjectURL(blob);

const texture = textureLoader.load(blobUrl);

// Cleanup when done
URL.revokeObjectURL(blobUrl);
```

### ArrayBuffer

```javascript
const response = await fetch('model.glb');
const buffer = await response.arrayBuffer();

const loader = new GLTFLoader();
loader.parse(buffer, '', (gltf) => {
  scene.add(gltf.scene);
}, (error) => {
  console.error(error);
});
```

### Custom Paths

```javascript
// Set base path for all loads
loader.setPath('assets/models/');
loader.load('model.glb'); // Loads from assets/models/model.glb

// Set resource path (for referenced assets like textures)
loader.setResourcePath('assets/textures/');

// Custom URL modification
loader.setURLModifier((url) => {
  // Add CDN prefix, authentication tokens, etc.
  return `https://cdn.example.com/${url}?token=abc123`;
});
```

## Error Handling

### Graceful Fallback

```javascript
async function loadWithFallback(primary, fallback) {
  const loader = new GLTFLoader();

  try {
    return await loader.loadAsync(primary);
  } catch (error) {
    console.warn(`Failed to load ${primary}, trying fallback`);
    try {
      return await loader.loadAsync(fallback);
    } catch (fallbackError) {
      console.error('Both primary and fallback failed');
      // Return default/placeholder model
      const geometry = new THREE.BoxGeometry();
      const material = new THREE.MeshBasicMaterial({ color: 0xff0000 });
      const placeholder = new THREE.Mesh(geometry, material);
      return { scene: placeholder };
    }
  }
}
```

### Retry Logic with Exponential Backoff

```javascript
async function loadWithRetry(url, maxRetries = 3) {
  const loader = new GLTFLoader();

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await loader.loadAsync(url);
    } catch (error) {
      if (i === maxRetries - 1) throw error;

      const delay = Math.pow(2, i) * 1000; // 1s, 2s, 4s
      console.warn(`Retry ${i + 1}/${maxRetries} after ${delay}ms`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

### Timeout with AbortController

```javascript
async function loadWithTimeout(url, timeoutMs = 10000) {
  const loader = new GLTFLoader();

  const timeoutPromise = new Promise((_, reject) => {
    setTimeout(() => reject(new Error('Load timeout')), timeoutMs);
  });

  const loadPromise = loader.loadAsync(url);

  return Promise.race([loadPromise, timeoutPromise]);
}
```

## Performance Tips

### Use Draco Compression

Reduces GLTF file size by 60-90% for geometry-heavy models. Requires DRACOLoader setup.

### Use KTX2/Basis Textures

GPU-compressed textures reduce memory usage and loading time. Requires KTX2Loader setup.

### Progressive Loading with Placeholders

```javascript
// Show low-res placeholder immediately
const placeholder = textureLoader.load('thumbnail.jpg');
material.map = placeholder;

// Load high-res in background
textureLoader.load('full-res.jpg', (texture) => {
  material.map = texture;
  material.needsUpdate = true;
  placeholder.dispose();
});
```

### Lazy Loading

Only load assets when needed:

```javascript
class LazyLoader {
  constructor() {
    this.loader = new GLTFLoader();
    this.loaded = new Map();
  }

  async getModel(name) {
    if (!this.loaded.has(name)) {
      const gltf = await this.loader.loadAsync(`models/${name}.glb`);
      this.loaded.set(name, gltf);
    }
    return this.loaded.get(name).scene.clone();
  }
}
```

### Enable Cache

```javascript
THREE.Cache.enabled = true;
```

Prevents re-downloading the same asset multiple times across your application.

## See Also

- [Geometry](geometry.md) - Geometry processing after loading models
- [Materials](materials.md) - Material setup for loaded models
- [Animation](animation.md) - Playing animations from loaded GLTF/FBX
- [Textures](textures.md) - Texture loading and compression formats
