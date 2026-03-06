# Three.js Lighting & Shadows

## Light Types Overview

| Type | Description | Shadow Support | Performance Cost |
|------|-------------|----------------|------------------|
| AmbientLight | Uniform illumination, no direction | No | Very Low |
| HemisphereLight | Sky/ground gradient | No | Low |
| DirectionalLight | Parallel rays (sun-like) | Yes | Medium |
| PointLight | Omnidirectional (bulb-like) | Yes | Medium-High |
| SpotLight | Cone-shaped beam | Yes | Medium-High |
| RectAreaLight | Rectangular area light | No (native) | High |

## AmbientLight

Provides uniform lighting to all objects equally. No direction or shadows.

```typescript
const ambient = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambient);
```

**Use case:** Base illumination, fill shadows, prevent pure black areas.

## HemisphereLight

Creates gradient lighting from sky color to ground color. Ideal for outdoor scenes.

```typescript
const hemiLight = new THREE.HemisphereLight(
  0x87ceeb, // sky color (light blue)
  0x8b4513, // ground color (brown)
  0.6       // intensity
);
hemiLight.position.set(0, 50, 0);
scene.add(hemiLight);
```

**Use case:** Natural outdoor ambient lighting, sky/ground color bounce.

## DirectionalLight

Emits parallel rays like sunlight. Uses orthographic shadow camera.

```typescript
const dirLight = new THREE.DirectionalLight(0xffffff, 1);
dirLight.position.set(5, 10, 7);
dirLight.castShadow = true;

// Shadow camera setup
dirLight.shadow.camera.left = -10;
dirLight.shadow.camera.right = 10;
dirLight.shadow.camera.top = 10;
dirLight.shadow.camera.bottom = -10;
dirLight.shadow.camera.near = 0.1;
dirLight.shadow.camera.far = 50;

// Shadow quality
dirLight.shadow.mapSize.width = 2048;
dirLight.shadow.mapSize.height = 2048;
dirLight.shadow.bias = -0.0001;
dirLight.shadow.normalBias = 0.02;

scene.add(dirLight);

// Visualize shadow camera
const helper = new THREE.CameraHelper(dirLight.shadow.camera);
scene.add(helper);
```

**Key points:**
- Position determines light direction
- Tight shadow frustum improves quality
- Adjust bias to fix shadow acne

## PointLight

Omnidirectional light like a light bulb. Uses cube shadow map (6 renders).

```typescript
const pointLight = new THREE.PointLight(0xffffff, 1, 100, 2);
pointLight.position.set(0, 5, 0);
pointLight.castShadow = true;

// Shadow setup
pointLight.shadow.mapSize.width = 1024;
pointLight.shadow.mapSize.height = 1024;
pointLight.shadow.camera.near = 0.5;
pointLight.shadow.camera.far = 100;
pointLight.shadow.bias = -0.001;

// Distance and decay
pointLight.distance = 100; // 0 = infinite
pointLight.decay = 2;      // physically correct

scene.add(pointLight);
```

**Parameters:**
- `distance`: Maximum range (0 = infinite)
- `decay`: Light falloff (2 = physically accurate)

## SpotLight

Cone-shaped light with falloff. Uses perspective shadow camera.

```typescript
const spotLight = new THREE.SpotLight(0xffffff, 1);
spotLight.position.set(10, 10, 10);
spotLight.target.position.set(0, 0, 0);
spotLight.castShadow = true;

// Cone shape
spotLight.angle = Math.PI / 6;      // 30 degrees
spotLight.penumbra = 0.2;           // soft edge
spotLight.distance = 50;
spotLight.decay = 2;

// Shadow setup
spotLight.shadow.mapSize.width = 1024;
spotLight.shadow.mapSize.height = 1024;
spotLight.shadow.camera.near = 1;
spotLight.shadow.camera.far = 50;
spotLight.shadow.bias = -0.0001;

scene.add(spotLight);
scene.add(spotLight.target);
```

**Parameters:**
- `angle`: Cone angle in radians
- `penumbra`: Edge softness (0-1)
- `target`: Point the light aims at

## RectAreaLight

Rectangular area light for soft realistic lighting. Only works with MeshStandardMaterial and MeshPhysicalMaterial.

```typescript
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';
import { RectAreaLightHelper } from 'three/addons/helpers/RectAreaLightHelper.js';

// Required initialization
RectAreaLightUniformsLib.init();

const rectLight = new THREE.RectAreaLight(0xffffff, 5, 4, 2);
rectLight.position.set(0, 5, 0);
rectLight.lookAt(0, 0, 0);
scene.add(rectLight);

// Helper
const helper = new RectAreaLightHelper(rectLight);
rectLight.add(helper);
```

**Limitations:**
- No native shadow support (use contact shadows workaround)
- Only Standard/Physical materials
- Requires UniformsLib initialization

## Shadow Setup

### Enable Shadows

```typescript
// 1. Enable on renderer
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// 2. Enable on light
light.castShadow = true;

// 3. Enable on objects
mesh.castShadow = true;
mesh.receiveShadow = true;
```

### Shadow Map Types

```typescript
THREE.BasicShadowMap      // Fast, hard edges
THREE.PCFShadowMap        // Default, filtered
THREE.PCFSoftShadowMap    // Softer shadows
THREE.VSMShadowMap        // Variance Shadow Maps, can blur
```

### Tight Frustum Optimization

```typescript
// Fit shadow camera tightly around scene
const box = new THREE.Box3().setFromObject(sceneGroup);
const size = box.getSize(new THREE.Vector3());

dirLight.shadow.camera.left = -size.x / 2;
dirLight.shadow.camera.right = size.x / 2;
dirLight.shadow.camera.top = size.y / 2;
dirLight.shadow.camera.bottom = -size.y / 2;
dirLight.shadow.camera.updateProjectionMatrix();
```

### Shadow Acne Fixes

```typescript
// Adjust bias values to fix artifacts
light.shadow.bias = -0.0001;        // Offset shadow depth
light.shadow.normalBias = 0.02;     // Offset along normal
```

### Contact Shadows (Fake/Fast)

```typescript
import { ContactShadows } from 'three/addons/objects/ContactShadows.js';

const contactShadows = new ContactShadows({
  opacity: 0.5,
  scale: 10,
  blur: 1,
  far: 10
});
contactShadows.position.y = 0;
scene.add(contactShadows);
```

## Light Helpers

```typescript
// All light types have helpers
const ambientHelper = new THREE.HemisphereLightHelper(hemiLight, 5);
const dirHelper = new THREE.DirectionalLightHelper(dirLight, 5);
const pointHelper = new THREE.PointLightHelper(pointLight, 1);
const spotHelper = new THREE.SpotLightHelper(spotLight);
const rectHelper = new RectAreaLightHelper(rectLight);

scene.add(ambientHelper);
scene.add(dirHelper);
scene.add(pointHelper);
scene.add(spotHelper);

// Update spot helper after changes
spotHelper.update();
```

## Environment Lighting (IBL)

### HDR Environment Maps

```typescript
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';

const rgbeLoader = new RGBELoader();
rgbeLoader.load('/path/to/env.hdr', (texture) => {
  texture.mapping = THREE.EquirectangularReflectionMapping;

  scene.background = texture;
  scene.environment = texture; // PBR reflections

  // Optional blur
  scene.backgroundBlurriness = 0.5;
  scene.backgroundIntensity = 1.0;
  scene.environmentIntensity = 1.0;
});
```

### PMREM Generator (Prefiltered Mipmaps)

```typescript
import { PMREMGenerator } from 'three';

const pmremGenerator = new PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();

rgbeLoader.load('/env.hdr', (texture) => {
  const envMap = pmremGenerator.fromEquirectangular(texture).texture;

  scene.environment = envMap;

  texture.dispose();
  pmremGenerator.dispose();
});
```

### Cube Texture Environment

```typescript
const cubeLoader = new THREE.CubeTextureLoader();
const envMap = cubeLoader.load([
  'px.jpg', 'nx.jpg',
  'py.jpg', 'ny.jpg',
  'pz.jpg', 'nz.jpg'
]);

scene.background = envMap;
scene.environment = envMap;
```

## Light Probes

Baked ambient lighting from environment map.

```typescript
import { LightProbeGenerator } from 'three/addons/lights/LightProbeGenerator.js';

// From cube texture
const cubeTexture = cubeLoader.load([...]);
const lightProbe = LightProbeGenerator.fromCubeTexture(cubeTexture);
scene.add(lightProbe);

// From equirectangular
const probe = LightProbeGenerator.fromCubeRenderTarget(
  renderer,
  cubeRenderTarget
);
scene.add(probe);
```

## Common Lighting Setups

### Three-Point Lighting

```typescript
// Key light (main)
const keyLight = new THREE.DirectionalLight(0xffffff, 1);
keyLight.position.set(5, 5, 5);
keyLight.castShadow = true;

// Fill light (soften shadows)
const fillLight = new THREE.DirectionalLight(0xffffff, 0.3);
fillLight.position.set(-5, 0, 0);

// Back light (rim/separation)
const backLight = new THREE.DirectionalLight(0xffffff, 0.5);
backLight.position.set(0, 3, -5);

scene.add(keyLight, fillLight, backLight);
```

### Outdoor Daylight

```typescript
// Sky gradient
const hemiLight = new THREE.HemisphereLight(0x87ceeb, 0x8b7355, 0.6);
scene.add(hemiLight);

// Sun
const sunLight = new THREE.DirectionalLight(0xfff4e6, 1);
sunLight.position.set(10, 20, 5);
sunLight.castShadow = true;
sunLight.shadow.camera.left = -20;
sunLight.shadow.camera.right = 20;
sunLight.shadow.camera.top = 20;
sunLight.shadow.camera.bottom = -20;
scene.add(sunLight);
```

### Indoor Studio

```typescript
// Multiple soft area lights
const light1 = new THREE.RectAreaLight(0xffffff, 5, 4, 2);
light1.position.set(-3, 3, 0);
light1.lookAt(0, 0, 0);

const light2 = new THREE.RectAreaLight(0xffffff, 3, 4, 2);
light2.position.set(3, 3, 0);
light2.lookAt(0, 0, 0);

const fillAmbient = new THREE.AmbientLight(0xffffff, 0.2);

scene.add(light1, light2, fillAmbient);
```

## Light Animation

### Orbit Animation

```typescript
function animate(time) {
  const radius = 10;
  pointLight.position.x = Math.cos(time) * radius;
  pointLight.position.z = Math.sin(time) * radius;
}
```

### Pulse Intensity

```typescript
function animate(time) {
  light.intensity = 0.5 + Math.sin(time * 2) * 0.5;
}
```

### Color Cycle

```typescript
function animate(time) {
  const hue = (time * 0.1) % 1;
  light.color.setHSL(hue, 1, 0.5);
}
```

### Animated Target

```typescript
function animate(time) {
  spotLight.target.position.x = Math.cos(time) * 5;
  spotLight.target.position.z = Math.sin(time) * 5;
  spotLight.target.updateMatrixWorld();
}
```

## Performance Tips

1. **Limit light count**: Aim for 3-5 real-time lights maximum
2. **Bake static lighting**: Use lightmaps for non-moving lights
3. **Smaller shadow maps**: 1024x1024 often sufficient, use 2048+ only for hero lights
4. **Tight shadow frustums**: Minimize shadow camera bounds for better quality
5. **Disable shadows on distant objects**: Use layers or distance checks
6. **Use light layers**: Selective lighting with Object3D.layers
7. **Environment maps over lights**: IBL cheaper than multiple lights
8. **Ambient + single shadow**: Often sufficient for mobile
9. **Shadow map type**: PCFShadowMap good balance, avoid PCFSoft on mobile
10. **Disable unnecessary shadows**: Not all objects need to cast/receive

### Light Layers Example

```typescript
// Setup layers
camera.layers.enable(0);
camera.layers.enable(1);

light.layers.set(1); // Only affects layer 1

object1.layers.set(0); // Not affected by light
object2.layers.set(1); // Affected by light
```

### Conditional Shadows

```typescript
function updateShadows(camera) {
  scene.traverse((obj) => {
    if (obj.isMesh) {
      const distance = obj.position.distanceTo(camera.position);
      obj.castShadow = distance < 20;
    }
  });
}
```

## See Also

- [Materials](materials.md) - PBR materials that respond to lighting
- [Textures](textures.md) - HDR environment maps and IBL textures
- [Postprocessing](postprocessing.md) - Bloom, SSAO, and other light-related effects
- [Fundamentals](fundamentals.md) - Scene setup and renderer configuration
