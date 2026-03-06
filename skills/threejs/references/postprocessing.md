# Three.js Post-Processing

## EffectComposer Setup

```javascript
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass';

// Create composer
const composer = new EffectComposer(renderer);

// ALWAYS add RenderPass first
const renderPass = new RenderPass(scene, camera);
composer.addPass(renderPass);

// Add other passes...

// In animation loop: use composer.render() instead of renderer.render()
function animate() {
  requestAnimationFrame(animate);
  composer.render(); // NOT renderer.render(scene, camera)
}

// Handle resize
window.addEventListener('resize', () => {
  renderer.setSize(window.innerWidth, window.innerHeight);
  composer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
});
```

## Common Effects

### Bloom (UnrealBloomPass)

```javascript
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass';

const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  1.5,    // strength
  0.4,    // radius
  0.85    // threshold (0-1, higher = less bloom)
);
composer.addPass(bloomPass);

// Adjustable properties
bloomPass.strength = 1.5;
bloomPass.radius = 0.4;
bloomPass.threshold = 0.85;
```

### Selective Bloom (Layer-based)

```javascript
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass';

// Setup layers
const BLOOM_LAYER = 1;
const bloomLayer = new THREE.Layers();
bloomLayer.set(BLOOM_LAYER);

// Mark objects for bloom
glowingMesh.layers.enable(BLOOM_LAYER);

// Create two composers
const finalComposer = new EffectComposer(renderer);
const bloomComposer = new EffectComposer(renderer);

// Bloom composer setup
bloomComposer.addPass(new RenderPass(scene, camera));
const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  1.5, 0.4, 0.85
);
bloomComposer.addPass(bloomPass);

// Final composer setup
finalComposer.addPass(new RenderPass(scene, camera));
const mixPass = new ShaderPass(
  new THREE.ShaderMaterial({
    uniforms: {
      baseTexture: { value: null },
      bloomTexture: { value: bloomComposer.renderTarget2.texture }
    },
    vertexShader: `
      varying vec2 vUv;
      void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      uniform sampler2D baseTexture;
      uniform sampler2D bloomTexture;
      varying vec2 vUv;
      void main() {
        gl_FragColor = texture2D(baseTexture, vUv) + vec4(1.0) * texture2D(bloomTexture, vUv);
      }
    `
  }), 'baseTexture'
);
mixPass.needsSwap = true;
finalComposer.addPass(mixPass);

// Render function with darken/restore pattern
function render() {
  // Render bloom
  camera.layers.set(BLOOM_LAYER);
  bloomComposer.render();

  // Render final scene
  camera.layers.set(0);
  finalComposer.render();
}
```

### FXAA (Fast Approximate Anti-Aliasing)

```javascript
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass';
import { FXAAShader } from 'three/examples/jsm/shaders/FXAAShader';

const fxaaPass = new ShaderPass(FXAAShader);
const pixelRatio = renderer.getPixelRatio();

fxaaPass.material.uniforms['resolution'].value.x = 1 / (window.innerWidth * pixelRatio);
fxaaPass.material.uniforms['resolution'].value.y = 1 / (window.innerHeight * pixelRatio);

composer.addPass(fxaaPass);

// Update on resize
function onResize() {
  const pixelRatio = renderer.getPixelRatio();
  fxaaPass.material.uniforms['resolution'].value.x = 1 / (window.innerWidth * pixelRatio);
  fxaaPass.material.uniforms['resolution'].value.y = 1 / (window.innerHeight * pixelRatio);
}
```

### SMAA (Subpixel Morphological Anti-Aliasing)

```javascript
import { SMAAPass } from 'three/examples/jsm/postprocessing/SMAAPass';

const smaaPass = new SMAAPass(
  window.innerWidth * renderer.getPixelRatio(),
  window.innerHeight * renderer.getPixelRatio()
);
composer.addPass(smaaPass);

// Update on resize
function onResize() {
  smaaPass.setSize(
    window.innerWidth * renderer.getPixelRatio(),
    window.innerHeight * renderer.getPixelRatio()
  );
}
```

### SSAO (Screen Space Ambient Occlusion)

```javascript
import { SSAOPass } from 'three/examples/jsm/postprocessing/SSAOPass';

const ssaoPass = new SSAOPass(scene, camera, window.innerWidth, window.innerHeight);
ssaoPass.kernelRadius = 16;
ssaoPass.minDistance = 0.005;
ssaoPass.maxDistance = 0.1;
ssaoPass.output = SSAOPass.OUTPUT.Default; // Default, SSAO, Blur, Beauty, Depth, Normal

composer.addPass(ssaoPass);
```

### Depth of Field (BokehPass)

```javascript
import { BokehPass } from 'three/examples/jsm/postprocessing/BokehPass';

const bokehPass = new BokehPass(scene, camera, {
  focus: 1.0,       // focus distance
  aperture: 0.025,  // aperture size (lower = more blur)
  maxblur: 0.01     // max blur amount
});

composer.addPass(bokehPass);

// Adjustable
bokehPass.uniforms['focus'].value = 1.0;
bokehPass.uniforms['aperture'].value = 0.025;
bokehPass.uniforms['maxblur'].value = 0.01;
```

### Film Grain

```javascript
import { FilmPass } from 'three/examples/jsm/postprocessing/FilmPass';

const filmPass = new FilmPass(
  0.35,   // noise intensity
  0.025,  // scanline intensity
  648,    // scanline count
  false   // grayscale
);

composer.addPass(filmPass);
```

### Vignette

```javascript
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass';
import { VignetteShader } from 'three/examples/jsm/shaders/VignetteShader';

const vignettePass = new ShaderPass(VignetteShader);
vignettePass.uniforms['offset'].value = 1.0;   // vignette offset
vignettePass.uniforms['darkness'].value = 1.0; // vignette darkness

composer.addPass(vignettePass);
```

### Color Correction

```javascript
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass';
import { ColorCorrectionShader } from 'three/examples/jsm/shaders/ColorCorrectionShader';

const colorCorrectionPass = new ShaderPass(ColorCorrectionShader);
colorCorrectionPass.uniforms['powRGB'].value = new THREE.Vector3(2.0, 2.0, 2.0);
colorCorrectionPass.uniforms['mulRGB'].value = new THREE.Vector3(1.0, 1.0, 1.0);
colorCorrectionPass.uniforms['addRGB'].value = new THREE.Vector3(0.0, 0.0, 0.0);

composer.addPass(colorCorrectionPass);
```

### Gamma Correction

```javascript
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass';
import { GammaCorrectionShader } from 'three/examples/jsm/shaders/GammaCorrectionShader';

const gammaCorrectionPass = new ShaderPass(GammaCorrectionShader);
composer.addPass(gammaCorrectionPass);
```

### Pixelation

```javascript
import { RenderPixelatedPass } from 'three/examples/jsm/postprocessing/RenderPixelatedPass';

const pixelPass = new RenderPixelatedPass(6, scene, camera); // 6 = pixel size
composer.addPass(pixelPass);
```

### Glitch Effect

```javascript
import { GlitchPass } from 'three/examples/jsm/postprocessing/GlitchPass';

const glitchPass = new GlitchPass();
glitchPass.goWild = false; // enable for constant glitching

composer.addPass(glitchPass);
```

### Halftone Effect

```javascript
import { HalftonePass } from 'three/examples/jsm/postprocessing/HalftonePass';

const halftonePass = new HalftonePass(window.innerWidth, window.innerHeight, {
  shape: 1,           // 1 = dot, 2 = ellipse, 3 = line, 4 = square
  radius: 4,          // dot radius
  rotateR: Math.PI / 12,  // rotation angles for CMYK
  rotateG: Math.PI / 12 * 2,
  rotateB: Math.PI / 12 * 3,
  scatter: 0          // scatter amount
});

composer.addPass(halftonePass);
```

### Outline Effect

```javascript
import { OutlinePass } from 'three/examples/jsm/postprocessing/OutlinePass';

const outlinePass = new OutlinePass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  scene,
  camera
);

outlinePass.edgeStrength = 3.0;
outlinePass.edgeGlow = 0.0;
outlinePass.edgeThickness = 1.0;
outlinePass.pulsePeriod = 0;
outlinePass.visibleEdgeColor.set('#ffffff');
outlinePass.hiddenEdgeColor.set('#190a05');

// Add objects to outline
outlinePass.selectedObjects = [mesh1, mesh2];

composer.addPass(outlinePass);
```

## Custom ShaderPass

### Basic Custom Effect Structure

```javascript
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass';

const customShader = {
  uniforms: {
    tDiffuse: { value: null },  // REQUIRED: input texture from previous pass
    amount: { value: 1.0 }      // custom uniforms
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform sampler2D tDiffuse;
    uniform float amount;
    varying vec2 vUv;

    void main() {
      vec4 color = texture2D(tDiffuse, vUv);
      // Apply effect...
      gl_FragColor = color;
    }
  `
};

const customPass = new ShaderPass(customShader);
composer.addPass(customPass);
```

### Invert Colors Example

```javascript
const invertShader = {
  uniforms: {
    tDiffuse: { value: null }
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform sampler2D tDiffuse;
    varying vec2 vUv;

    void main() {
      vec4 color = texture2D(tDiffuse, vUv);
      gl_FragColor = vec4(1.0 - color.rgb, color.a);
    }
  `
};

const invertPass = new ShaderPass(invertShader);
composer.addPass(invertPass);
```

### Chromatic Aberration Example

```javascript
const chromaticAberrationShader = {
  uniforms: {
    tDiffuse: { value: null },
    amount: { value: 0.005 }
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform sampler2D tDiffuse;
    uniform float amount;
    varying vec2 vUv;

    void main() {
      vec2 offset = vec2(amount, 0.0);
      vec4 cr = texture2D(tDiffuse, vUv + offset);
      vec4 cga = texture2D(tDiffuse, vUv);
      vec4 cb = texture2D(tDiffuse, vUv - offset);

      gl_FragColor = vec4(cr.r, cga.g, cb.b, cga.a);
    }
  `
};

const chromaticPass = new ShaderPass(chromaticAberrationShader);
composer.addPass(chromaticPass);
```

## Combining Multiple Effects

```javascript
// Example pipeline: RenderPass > Bloom > Vignette > Gamma > FXAA
// ALWAYS add anti-aliasing (FXAA/SMAA) LAST

const composer = new EffectComposer(renderer);

// 1. RenderPass (always first)
const renderPass = new RenderPass(scene, camera);
composer.addPass(renderPass);

// 2. Bloom
const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  1.5, 0.4, 0.85
);
composer.addPass(bloomPass);

// 3. Vignette
const vignettePass = new ShaderPass(VignetteShader);
vignettePass.uniforms['offset'].value = 1.0;
vignettePass.uniforms['darkness'].value = 1.0;
composer.addPass(vignettePass);

// 4. Gamma correction
const gammaCorrectionPass = new ShaderPass(GammaCorrectionShader);
composer.addPass(gammaCorrectionPass);

// 5. FXAA (always last for anti-aliasing)
const fxaaPass = new ShaderPass(FXAAShader);
const pixelRatio = renderer.getPixelRatio();
fxaaPass.material.uniforms['resolution'].value.x = 1 / (window.innerWidth * pixelRatio);
fxaaPass.material.uniforms['resolution'].value.y = 1 / (window.innerHeight * pixelRatio);
composer.addPass(fxaaPass);
```

## Render to Texture (WebGLRenderTarget)

```javascript
// Create render target
const renderTarget = new THREE.WebGLRenderTarget(
  window.innerWidth,
  window.innerHeight,
  {
    minFilter: THREE.LinearFilter,
    magFilter: THREE.LinearFilter,
    format: THREE.RGBAFormat,
    stencilBuffer: false
  }
);

// Use with composer
const composer = new EffectComposer(renderer, renderTarget);

// Manual render to texture
renderer.setRenderTarget(renderTarget);
renderer.render(scene, camera);
renderer.setRenderTarget(null);

// Use texture in material
const material = new THREE.MeshBasicMaterial({
  map: renderTarget.texture
});
```

## Multi-Pass Rendering (Multiple Composers)

```javascript
// Different scenes/layers
const mainComposer = new EffectComposer(renderer);
mainComposer.addPass(new RenderPass(mainScene, camera));

const uiComposer = new EffectComposer(renderer);
uiComposer.addPass(new RenderPass(uiScene, camera));

// Render in order
function animate() {
  requestAnimationFrame(animate);

  // Render main scene with effects
  mainComposer.render();

  // Render UI on top without clearing
  renderer.autoClear = false;
  uiComposer.render();
  renderer.autoClear = true;
}
```

## WebGPU Post-Processing (Node-based, r150+)

```javascript
import { pass, bloom, fxaa, output } from 'three/nodes';

// Create post-processing chain using nodes
const scenePass = pass(scene, camera);
const bloomPass = bloom(scenePass, 1.5, 0.4, 0.85);
const fxaaPass = fxaa(bloomPass);

// Use in render loop
renderer.compute(fxaaPass);
renderer.render(scene, camera);

// Or use postProcessing chain
const postProcessing = scenePass.bloom(1.5, 0.4, 0.85).fxaa();
renderer.compute(postProcessing);
```

## Performance Tips

1. **Limit passes**: Each pass = full-screen render. Combine shaders when possible.

2. **Lower resolution for blur effects**:
```javascript
const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth / 2, window.innerHeight / 2), // half resolution
  1.5, 0.4, 0.85
);
```

3. **Toggle effects conditionally**:
```javascript
bloomPass.enabled = highQualityMode;
```

4. **FXAA over MSAA**: FXAA is cheaper than multi-sample anti-aliasing.

5. **Profile and disable**: Use Chrome DevTools Performance to identify bottlenecks.

6. **Reuse render targets**:
```javascript
const renderTarget = new THREE.WebGLRenderTarget(width, height);
composer1.renderTarget1 = renderTarget;
composer2.renderTarget1 = renderTarget;
```

7. **Adaptive quality**:
```javascript
function updateQuality(fps) {
  if (fps < 30) {
    bloomPass.enabled = false;
    ssaoPass.enabled = false;
  }
}
```

## Handle Resize

```javascript
function onWindowResize() {
  const width = window.innerWidth;
  const height = window.innerHeight;

  // Update camera
  camera.aspect = width / height;
  camera.updateProjectionMatrix();

  // Update renderer
  renderer.setSize(width, height);

  // Update composer
  composer.setSize(width, height);

  // Update FXAA resolution
  const pixelRatio = renderer.getPixelRatio();
  fxaaPass.material.uniforms['resolution'].value.x = 1 / (width * pixelRatio);
  fxaaPass.material.uniforms['resolution'].value.y = 1 / (height * pixelRatio);

  // Update bloom resolution (if using lower res)
  bloomPass.resolution.set(width / 2, height / 2);

  // Update SMAA
  smaaPass.setSize(width * pixelRatio, height * pixelRatio);

  // Update SSAO
  ssaoPass.setSize(width, height);

  // Update render targets
  renderTarget.setSize(width, height);
}

window.addEventListener('resize', onWindowResize);
```

## See Also

- [Shaders](shaders.md) - Writing custom GLSL for ShaderPass
- [Lighting & Shadows](lighting-and-shadows.md) - Light sources that drive bloom/SSAO
- [Textures](textures.md) - Render targets and framebuffer textures
- [Fundamentals](fundamentals.md) - Renderer setup and pixel ratio
