# Three.js Fundamentals Reference

## Scene

```javascript
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000000); // Color or null
scene.background = textureLoader.load('path/to/texture.jpg'); // Texture
scene.environment = hdrTexture; // For PBR materials (IBL)
scene.fog = new THREE.Fog(0xffffff, 1, 1000); // color, near, far
scene.fog = new THREE.FogExp2(0xffffff, 0.002); // color, density
```

**Key properties:**
- `scene.add(object)` / `scene.remove(object)`
- `scene.getObjectByName(name)` / `scene.getObjectById(id)`
- `scene.traverse(callback)` - recursively visit all descendants

## Cameras

### PerspectiveCamera
```javascript
const camera = new THREE.PerspectiveCamera(
  75,                                    // fov (degrees)
  window.innerWidth / window.innerHeight, // aspect ratio
  0.1,                                   // near clipping plane
  1000                                   // far clipping plane
);
camera.position.set(0, 5, 10);
camera.lookAt(0, 0, 0);
camera.updateProjectionMatrix(); // Call after changing fov, aspect, near, far
```

**Common gotchas:**
- Must call `updateProjectionMatrix()` after changing projection parameters
- Z-fighting occurs when near/far ratio is too large (keep near > 0.1, far reasonable)
- Default position is (0,0,0), default up is (0,1,0)

### OrthographicCamera
```javascript
const frustumSize = 10;
const aspect = window.innerWidth / window.innerHeight;
const camera = new THREE.OrthographicCamera(
  frustumSize * aspect / -2,  // left
  frustumSize * aspect / 2,   // right
  frustumSize / 2,            // top
  frustumSize / -2,           // bottom
  0.1,                        // near
  1000                        // far
);
camera.zoom = 1; // Increase to zoom in
camera.updateProjectionMatrix();
```

### ArrayCamera
```javascript
// For split-screen rendering
const camera1 = new THREE.PerspectiveCamera(50, 0.5, 1, 1000);
const camera2 = new THREE.PerspectiveCamera(50, 0.5, 1, 1000);
const arrayCamera = new THREE.ArrayCamera([camera1, camera2]);
```

### CubeCamera
```javascript
// For dynamic environment maps (reflections)
const cubeRenderTarget = new THREE.WebGLCubeRenderTarget(256);
const cubeCamera = new THREE.CubeCamera(0.1, 1000, cubeRenderTarget);
scene.add(cubeCamera);

// In render loop:
cubeCamera.update(renderer, scene);
reflectiveMesh.material.envMap = cubeRenderTarget.texture;
```

## WebGLRenderer

```javascript
const renderer = new THREE.WebGLRenderer({
  canvas: document.querySelector('#canvas'),
  antialias: true,
  alpha: true,           // Transparent background
  powerPreference: 'high-performance'
});

// Essential setup
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Cap at 2 for performance
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap; // or PCFShadowMap, VSMShadowMap

// Color management (Three.js r152+)
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;

// Other useful properties
renderer.physicallyCorrectLights = true; // Deprecated in r152, use useLegacyLights = false
renderer.useLegacyLights = false; // r152+
```

**Shadow types:**
- `THREE.BasicShadowMap` - fastest, lowest quality
- `THREE.PCFShadowMap` - default, filtered
- `THREE.PCFSoftShadowMap` - softer, slower
- `THREE.VSMShadowMap` - variance shadow maps, can have artifacts

## Object3D

Base class for most Three.js objects (Mesh, Light, Camera, Group, etc.)

```javascript
const obj = new THREE.Object3D();

// Transform properties (do NOT modify directly in most cases)
obj.position.set(x, y, z);
obj.rotation.set(x, y, z); // Euler angles in radians
obj.scale.set(x, y, z);
obj.quaternion.setFromEuler(new THREE.Euler(x, y, z)); // For rotation

// Hierarchy
obj.add(childObject);
obj.remove(childObject);
obj.parent // Reference to parent
obj.children // Array of children

// Visibility and rendering
obj.visible = true;
obj.layers.set(0); // Default layer is 0
obj.layers.enable(1); // Add to layer 1
obj.layers.toggle(2); // Toggle layer 2
obj.renderOrder = 0; // Higher values render last (for transparency)

// Traversal
obj.traverse((child) => {
  if (child.isMesh) {
    // Do something with meshes
  }
});

// World space transforms
obj.getWorldPosition(target); // Get world position into target Vector3
obj.getWorldQuaternion(target);
obj.getWorldScale(target);
obj.getWorldDirection(target);

// Update matrices (usually automatic)
obj.updateMatrix(); // Local transform
obj.updateMatrixWorld(); // World transform (includes parent)
obj.matrixAutoUpdate = false; // Disable auto-update for manual control
```

**Important:**
- Rotation uses Euler angles (gimbal lock possible), Quaternion for interpolation
- `matrixAutoUpdate` should stay `true` unless you're manually managing matrices
- World transforms require traversing parent chain

## Group

Convenience class for organizing objects.

```javascript
const group = new THREE.Group();
group.add(mesh1, mesh2, mesh3);
scene.add(group);

// Transform entire group
group.position.set(0, 5, 0);
group.rotation.y = Math.PI / 4;
```

## Mesh

```javascript
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0xff0000 });
const mesh = new THREE.Mesh(geometry, material);

// Shadows
mesh.castShadow = true;
mesh.receiveShadow = true;

// Raycasting
mesh.raycast(raycaster, intersects); // Usually called via scene.raycast

// Frustum culling
mesh.frustumCulled = true; // Default, disable if doing custom culling
```

## Coordinate System

Three.js uses a **right-handed** coordinate system:
- **+X** is right
- **+Y** is up
- **+Z** is out of the screen (toward camera in default view)
- Camera looks down **-Z** by default

```javascript
// Common camera setup (looking at origin from +Z)
camera.position.set(0, 0, 5);
camera.lookAt(0, 0, 0);
```

## Math Utilities

### Vector3
```javascript
const v = new THREE.Vector3(x, y, z);
v.set(x, y, z);
v.copy(otherVector);
v.add(otherVector); // v += other
v.sub(otherVector); // v -= other
v.multiplyScalar(scalar);
v.normalize(); // Make unit length
v.length(); // Magnitude
v.distanceTo(otherVector);
v.dot(otherVector);
v.cross(otherVector); // Cross product
v.lerp(targetVector, alpha); // Linear interpolation
v.applyMatrix4(matrix);
v.applyQuaternion(quaternion);
v.project(camera); // To NDC
v.unproject(camera); // From NDC
```

### Matrix4
```javascript
const m = new THREE.Matrix4();
m.identity();
m.makeTranslation(x, y, z);
m.makeRotationX(radians);
m.makeScale(x, y, z);
m.multiply(otherMatrix);
m.invert();
m.transpose();
m.decompose(position, quaternion, scale); // Extract TRS
m.compose(position, quaternion, scale); // Build from TRS
```

### Quaternion
```javascript
const q = new THREE.Quaternion();
q.setFromEuler(new THREE.Euler(x, y, z));
q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), Math.PI / 2);
q.multiply(otherQuaternion);
q.slerp(targetQuaternion, alpha); // Spherical interpolation
q.normalize();
```

### Euler
```javascript
const euler = new THREE.Euler(x, y, z, 'XYZ'); // Rotation order: XYZ, YXZ, ZXY, etc.
euler.setFromQuaternion(quaternion);
```

### Color
```javascript
const color = new THREE.Color(0xff0000);
const color2 = new THREE.Color('rgb(255, 0, 0)');
const color3 = new THREE.Color('hsl(0, 100%, 50%)');
color.set(0x00ff00);
color.setHex(0x0000ff);
color.setRGB(r, g, b); // 0-1 range
color.setHSL(h, s, l); // h: 0-1, s: 0-1, l: 0-1
color.lerp(targetColor, alpha);
color.getHex(); // Returns number
color.getHexString(); // Returns string without #
```

### MathUtils
```javascript
THREE.MathUtils.degToRad(degrees);
THREE.MathUtils.radToDeg(radians);
THREE.MathUtils.clamp(value, min, max);
THREE.MathUtils.lerp(start, end, alpha);
THREE.MathUtils.smoothstep(x, min, max);
THREE.MathUtils.mapLinear(x, a1, a2, b1, b2);
THREE.MathUtils.randFloat(low, high);
THREE.MathUtils.randInt(low, high);
THREE.MathUtils.seededRandom(seed); // Returns random function
THREE.MathUtils.isPowerOfTwo(value);
```

## Common Patterns

### Cleanup and Disposal
```javascript
// Dispose geometry and material
mesh.geometry.dispose();
mesh.material.dispose();

// Dispose textures
mesh.material.map?.dispose();
mesh.material.normalMap?.dispose();
mesh.material.envMap?.dispose();

// Dispose render targets
renderTarget.dispose();

// Remove from scene
scene.remove(mesh);

// Full cleanup function
function dispose(obj) {
  obj.traverse((child) => {
    if (child.geometry) child.geometry.dispose();
    if (child.material) {
      if (Array.isArray(child.material)) {
        child.material.forEach(m => m.dispose());
      } else {
        child.material.dispose();
      }
    }
  });
}
```

**Critical:** Always dispose when removing objects to prevent memory leaks.

### Clock for Animation
```javascript
const clock = new THREE.Clock();

function animate() {
  const deltaTime = clock.getDelta(); // Time since last call
  const elapsedTime = clock.getElapsedTime(); // Total time since start

  mesh.rotation.y += deltaTime; // Frame-rate independent rotation

  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}
animate();
```

### Responsive Canvas
```javascript
function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}
window.addEventListener('resize', onWindowResize);

// Or for specific container
function onWindowResize() {
  const container = renderer.domElement.parentElement;
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
}
```

### LoadingManager
```javascript
const manager = new THREE.LoadingManager();

manager.onStart = (url, loaded, total) => {
  console.log(`Started loading: ${url}`);
};

manager.onLoad = () => {
  console.log('All assets loaded');
};

manager.onProgress = (url, loaded, total) => {
  console.log(`Loading: ${loaded / total * 100}%`);
};

manager.onError = (url) => {
  console.error(`Error loading: ${url}`);
};

const textureLoader = new THREE.TextureLoader(manager);
const gltfLoader = new GLTFLoader(manager);
```

### Render Loop with Cleanup
```javascript
let animationId;

function animate() {
  animationId = requestAnimationFrame(animate);

  // Update logic
  controls?.update();

  renderer.render(scene, camera);
}

function cleanup() {
  cancelAnimationFrame(animationId);
  renderer.dispose();
  // Dispose all objects...
}
```

## Performance Tips

### Geometry
- Reuse geometries when possible (instancing)
- Use `BufferGeometry` (default in modern Three.js)
- Merge static geometries with `BufferGeometryUtils.mergeGeometries()`
- Use LOD (Level of Detail) for distant objects

### Materials
- Reuse materials when possible
- Use `MeshBasicMaterial` for unlit objects
- Limit `MeshStandardMaterial` / `MeshPhysicalMaterial` count
- Disable features you don't need (shadows, fog, etc.)

### Textures
- Use power-of-two dimensions (256, 512, 1024, 2048)
- Enable mipmaps for textures (default)
- Use compressed formats (KTX2, Basis)
- Set `texture.minFilter = THREE.NearestFilter` to disable mipmaps if not needed
- Dispose unused textures

### Rendering
- Cap `renderer.setPixelRatio()` at 2
- Use `renderer.info` to monitor draw calls, triangles
- Disable `shadowMap` if not needed
- Use `renderer.setAnimationLoop()` for VR/AR (better than requestAnimationFrame)
- Enable frustum culling (default)
- Use `renderer.compile(scene, camera)` to pre-compile shaders

### General
- Limit `traverse()` calls in render loop
- Use object pooling for frequently created/destroyed objects
- Batch updates (don't call `updateMatrixWorld()` multiple times per frame)
- Use `InstancedMesh` for many identical objects
- Use `Points` for particle systems (not individual meshes)

### Monitoring
```javascript
console.log(renderer.info.render); // Draw calls, triangles, etc.
console.log(renderer.info.memory); // Geometries, textures
console.log(renderer.info.programs.length); // Shader programs compiled
```

**Rule of thumb:** Keep draw calls < 100-200, triangles < 1M for 60fps on average hardware.

## See Also

- [Geometry](geometry.md) - Built-in shapes and custom BufferGeometry
- [Materials](materials.md) - Material types and PBR workflow
- [Lighting & Shadows](lighting-and-shadows.md) - Light types and shadow setup
- [Animation](animation.md) - Animation loop, mixer, and procedural motion
