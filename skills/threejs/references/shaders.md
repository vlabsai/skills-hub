# Three.js Shaders

## ShaderMaterial vs RawShaderMaterial

**ShaderMaterial**: Auto-provides common uniforms and attributes, adds precision statements.

```javascript
const material = new THREE.ShaderMaterial({
  vertexShader: `
    // Auto-provided: position, normal, uv attributes
    // Auto-provided: modelMatrix, viewMatrix, projectionMatrix, etc.
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    varying vec2 vUv;
    void main() {
      gl_FragColor = vec4(vUv, 0.0, 1.0);
    }
  `
});
```

**RawShaderMaterial**: Requires manual declaration of everything.

```javascript
const material = new THREE.RawShaderMaterial({
  vertexShader: `
    precision mediump float;
    uniform mat4 modelViewMatrix;
    uniform mat4 projectionMatrix;
    attribute vec3 position;
    attribute vec2 uv;
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    precision mediump float;
    varying vec2 vUv;
    void main() {
      gl_FragColor = vec4(vUv, 0.0, 1.0);
    }
  `
});
```

## Uniforms

All uniform types supported:

```javascript
const material = new THREE.ShaderMaterial({
  uniforms: {
    uTime: { value: 0.0 },
    uSpeed: { value: 1.0 },
    uResolution: { value: new THREE.Vector2(800, 600) },
    uColor: { value: new THREE.Color(0xff0000) },
    uTexture: { value: texture },
    uMatrix: { value: new THREE.Matrix4() },
    uFloatArray: { value: [1.0, 2.0, 3.0] },
    uVec3Array: { value: [new THREE.Vector3(), new THREE.Vector3()] }
  },
  vertexShader: `...`,
  fragmentShader: `
    uniform float uTime;
    uniform vec2 uResolution;
    uniform vec3 uColor;
    uniform sampler2D uTexture;
    void main() {
      vec4 texColor = texture2D(uTexture, vUv);
      gl_FragColor = vec4(uColor * texColor.rgb, 1.0);
    }
  `
});

// Update at runtime
material.uniforms.uTime.value += deltaTime;
material.uniforms.uColor.value.set(0x00ff00);
```

## Varyings

Pass data from vertex to fragment shader:

```javascript
vertexShader: `
  varying vec2 vUv;
  varying vec3 vNormal;
  varying vec3 vPosition;
  varying vec3 vWorldPosition;

  void main() {
    vUv = uv;
    vNormal = normalize(normalMatrix * normal);
    vPosition = position;
    vWorldPosition = (modelMatrix * vec4(position, 1.0)).xyz;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`,
fragmentShader: `
  varying vec2 vUv;
  varying vec3 vNormal;
  varying vec3 vPosition;
  varying vec3 vWorldPosition;

  void main() {
    gl_FragColor = vec4(vNormal * 0.5 + 0.5, 1.0);
  }
`
```

## Common Shader Patterns

### Texture Sampling

```glsl
uniform sampler2D uTexture;
varying vec2 vUv;

void main() {
  vec4 texColor = texture2D(uTexture, vUv);
  gl_FragColor = texColor;
}
```

### Vertex Displacement (Wave)

```glsl
uniform float uTime;
varying vec2 vUv;

void main() {
  vUv = uv;
  vec3 pos = position;
  pos.z += sin(pos.x * 5.0 + uTime) * 0.1;
  pos.z += cos(pos.y * 5.0 + uTime) * 0.1;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
```

### Fresnel Effect

```glsl
varying vec3 vNormal;
varying vec3 vPosition;
uniform vec3 cameraPosition;

void main() {
  vec3 viewDirection = normalize(cameraPosition - vPosition);
  float fresnel = pow(1.0 - dot(vNormal, viewDirection), 3.0);
  gl_FragColor = vec4(vec3(fresnel), 1.0);
}
```

### Noise-Based Effects

```glsl
// Random function
float random(vec2 st) {
  return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}

// Value noise
float noise(vec2 st) {
  vec2 i = floor(st);
  vec2 f = fract(st);
  float a = random(i);
  float b = random(i + vec2(1.0, 0.0));
  float c = random(i + vec2(0.0, 1.0));
  float d = random(i + vec2(1.0, 1.0));
  vec2 u = smoothstep(0.0, 1.0, f);
  return mix(a, b, u.x) + (c - a) * u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
}

void main() {
  float n = noise(vUv * 10.0);
  gl_FragColor = vec4(vec3(n), 1.0);
}
```

### Gradients

```glsl
// Linear gradient
void main() {
  vec3 colorA = vec3(1.0, 0.0, 0.0);
  vec3 colorB = vec3(0.0, 0.0, 1.0);
  vec3 color = mix(colorA, colorB, vUv.x);
  gl_FragColor = vec4(color, 1.0);
}

// Radial gradient
void main() {
  float dist = distance(vUv, vec2(0.5));
  vec3 color = mix(vec3(1.0), vec3(0.0), smoothstep(0.0, 0.5, dist));
  gl_FragColor = vec4(color, 1.0);
}
```

### Rim Lighting

```glsl
varying vec3 vNormal;
varying vec3 vPosition;
uniform vec3 cameraPosition;

void main() {
  vec3 viewDirection = normalize(cameraPosition - vPosition);
  float rimPower = 2.0;
  float rim = 1.0 - max(0.0, dot(vNormal, viewDirection));
  rim = pow(rim, rimPower);
  vec3 rimColor = vec3(0.0, 1.0, 1.0);
  gl_FragColor = vec4(rimColor * rim, 1.0);
}
```

### Dissolve Effect with Edge Glow

```glsl
uniform float uProgress;
uniform sampler2D uNoiseTexture;
varying vec2 vUv;

void main() {
  float noise = texture2D(uNoiseTexture, vUv).r;
  float threshold = uProgress;
  float edge = 0.05;

  if (noise < threshold) discard;

  float edgeFactor = smoothstep(threshold, threshold + edge, noise);
  vec3 edgeColor = vec3(1.0, 0.5, 0.0);
  vec3 baseColor = vec3(1.0);
  vec3 color = mix(edgeColor, baseColor, edgeFactor);

  gl_FragColor = vec4(color, 1.0);
}
```

## Extending Built-in Materials

Use `onBeforeCompile` to modify existing materials:

```javascript
const material = new THREE.MeshStandardMaterial({ color: 0xff0000 });

material.onBeforeCompile = (shader) => {
  // Add custom uniforms
  shader.uniforms.uTime = { value: 0.0 };

  // Modify vertex shader
  shader.vertexShader = shader.vertexShader.replace(
    '#include <begin_vertex>',
    `
    #include <begin_vertex>
    transformed.z += sin(transformed.x * 5.0 + uTime) * 0.1;
    `
  );

  // Modify fragment shader
  shader.fragmentShader = shader.fragmentShader.replace(
    '#include <color_fragment>',
    `
    #include <color_fragment>
    diffuseColor.rgb *= vec3(vUv, 1.0);
    `
  );

  // Store reference for updates
  material.userData.shader = shader;
};

// Update in animation loop
material.userData.shader.uniforms.uTime.value += deltaTime;
```

Common injection points:
- `#include <begin_vertex>` - Modify vertex position
- `#include <beginnormal_vertex>` - Modify normals
- `#include <color_fragment>` - Modify diffuse color
- `#include <emissivemap_fragment>` - Add emissive effects
- `#include <roughnessmap_fragment>` - Modify roughness
- `#include <metalnessmap_fragment>` - Modify metalness

## GLSL Built-in Functions

### Math Functions

```glsl
abs(x)           // Absolute value
sign(x)          // -1, 0, or 1
floor(x)         // Round down
ceil(x)          // Round up
fract(x)         // Fractional part
mod(x, y)        // Modulo
min(x, y)        // Minimum
max(x, y)        // Maximum
clamp(x, min, max) // Constrain value
mix(a, b, t)     // Linear interpolation
step(edge, x)    // 0 if x < edge, else 1
smoothstep(e0, e1, x) // Smooth interpolation

// Trigonometry
sin(x), cos(x), tan(x)
asin(x), acos(x), atan(x, y)
radians(deg), degrees(rad)

// Exponential
pow(x, y)        // x^y
exp(x)           // e^x
log(x)           // Natural log
sqrt(x)          // Square root
```

### Vector Operations

```glsl
length(v)        // Vector length
distance(a, b)   // Distance between points
dot(a, b)        // Dot product
cross(a, b)      // Cross product (vec3)
normalize(v)     // Unit vector
reflect(I, N)    // Reflection vector
refract(I, N, eta) // Refraction vector
```

### Texture Functions

```glsl
// GLSL 1.0 (default)
texture2D(sampler2D, vec2)
textureCube(samplerCube, vec3)

// GLSL 3.0
texture(sampler2D, vec2)
texture(samplerCube, vec3)
```

## Material Properties

```javascript
const material = new THREE.ShaderMaterial({
  uniforms: { /* ... */ },
  vertexShader: `...`,
  fragmentShader: `...`,

  // Transparency
  transparent: true,
  opacity: 0.5,

  // Rendering
  side: THREE.DoubleSide, // FrontSide, BackSide, DoubleSide
  depthTest: true,
  depthWrite: true,

  // Blending
  blending: THREE.NormalBlending, // AdditiveBlending, SubtractiveBlending, MultiplyBlending

  // Extensions
  extensions: {
    derivatives: true,      // #extension GL_OES_standard_derivatives
    fragDepth: false,
    drawBuffers: false,
    shaderTextureLOD: false
  },

  // GLSL version
  glslVersion: THREE.GLSL3 // Use GLSL 3.0
});
```

## Shader Includes

### Using ShaderChunk

```javascript
import { ShaderChunk } from 'three';

const customChunk = `
  float customFunction(float x) {
    return sin(x) * 0.5 + 0.5;
  }
`;

ShaderChunk.customChunk = customChunk;

const shader = `
  #include <customChunk>

  void main() {
    float value = customFunction(vUv.x);
    gl_FragColor = vec4(vec3(value), 1.0);
  }
`;
```

### External .glsl Files (with bundlers)

```javascript
// With Vite or webpack
import vertexShader from './shaders/vertex.glsl';
import fragmentShader from './shaders/fragment.glsl';

const material = new THREE.ShaderMaterial({
  vertexShader,
  fragmentShader
});
```

## Instanced Shaders

```javascript
const geometry = new THREE.PlaneGeometry(1, 1);
const instanceCount = 100;

// Create instanced attributes
const offsets = new Float32Array(instanceCount * 3);
const colors = new Float32Array(instanceCount * 3);

for (let i = 0; i < instanceCount; i++) {
  offsets[i * 3] = Math.random() * 10 - 5;
  offsets[i * 3 + 1] = Math.random() * 10 - 5;
  offsets[i * 3 + 2] = Math.random() * 10 - 5;

  colors[i * 3] = Math.random();
  colors[i * 3 + 1] = Math.random();
  colors[i * 3 + 2] = Math.random();
}

geometry.setAttribute('aOffset', new THREE.InstancedBufferAttribute(offsets, 3));
geometry.setAttribute('aColor', new THREE.InstancedBufferAttribute(colors, 3));

const material = new THREE.ShaderMaterial({
  vertexShader: `
    attribute vec3 aOffset;
    attribute vec3 aColor;
    varying vec3 vColor;

    void main() {
      vColor = aColor;
      vec3 pos = position + aOffset;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
    }
  `,
  fragmentShader: `
    varying vec3 vColor;
    void main() {
      gl_FragColor = vec4(vColor, 1.0);
    }
  `
});

const mesh = new THREE.InstancedMesh(geometry, material, instanceCount);
```

## Debugging

### Log Shader Code

```javascript
material.onBeforeCompile = (shader) => {
  console.log('Vertex Shader:', shader.vertexShader);
  console.log('Fragment Shader:', shader.fragmentShader);
};
```

### Visual Debugging

```glsl
// Output coordinates as color
void main() {
  gl_FragColor = vec4(vUv, 0.0, 1.0); // See UV mapping
  // gl_FragColor = vec4(vNormal * 0.5 + 0.5, 1.0); // See normals
  // gl_FragColor = vec4(vPosition * 0.5 + 0.5, 1.0); // See positions
}
```

### Check Shader Errors

```javascript
renderer.checkShaderErrors = true; // Default is true in dev

// Catch compilation errors
material.onBeforeCompile = (shader) => {
  shader.fragmentShader = shader.fragmentShader.replace(
    'void main()',
    `
    void main() {
      #ifdef GL_ES
      precision mediump float;
      #endif
    `
  );
};
```

## Performance Tips

1. **Minimize uniforms**: Bundle related data into vectors/arrays
2. **Avoid conditionals**: Use `mix()` and `step()` instead of if/else
3. **Precalculate in JavaScript**: Move static calculations to CPU
4. **Lookup textures**: Use textures for complex functions (gradients, noise)
5. **Limit overdraw**: Use `depthTest` and `depthWrite` appropriately
6. **Reduce varying count**: Only pass necessary data to fragment shader

### Key Pattern: Replace Conditionals

```glsl
// BAD: Branching hurts performance
if (value > 0.5) {
  color = colorA;
} else {
  color = colorB;
}

// GOOD: Use step() and mix()
float threshold = step(0.5, value);
color = mix(colorB, colorA, threshold);

// BETTER: Use smoothstep() for smooth transitions
float threshold = smoothstep(0.4, 0.6, value);
color = mix(colorB, colorA, threshold);
```

### Optimize Texture Lookups

```glsl
// BAD: Multiple lookups
vec4 tex1 = texture2D(uTexture, vUv);
vec4 tex2 = texture2D(uTexture, vUv);
float value = tex1.r + tex2.g;

// GOOD: Single lookup
vec4 tex = texture2D(uTexture, vUv);
float value = tex.r + tex.g;
```

### Precalculate Constants

```glsl
// BAD: Calculated every fragment
float pi = 3.14159;
float angle = pi * 2.0 * vUv.x;

// GOOD: Define as constant
const float TWO_PI = 6.28318;
float angle = TWO_PI * vUv.x;
```

## See Also

- [Materials](materials.md) - Built-in materials that shaders can extend
- [Postprocessing](postprocessing.md) - Custom ShaderPass for post-processing effects
- [Textures](textures.md) - Texture sampling and data textures in shaders
- [Animation](animation.md) - Animating shader uniforms over time
