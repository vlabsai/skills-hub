# Three.js Geometry

## Built-in Geometries

### Basic Shapes
```javascript
// Box: width, height, depth, widthSegments, heightSegments, depthSegments
new THREE.BoxGeometry(1, 1, 1, 1, 1, 1);

// Sphere: radius, widthSegments, heightSegments, phiStart, phiLength, thetaStart, thetaLength
new THREE.SphereGeometry(1, 32, 16, 0, Math.PI * 2, 0, Math.PI);

// Plane: width, height, widthSegments, heightSegments
new THREE.PlaneGeometry(1, 1, 1, 1);

// Circle: radius, segments, thetaStart, thetaLength
new THREE.CircleGeometry(1, 32, 0, Math.PI * 2);

// Cylinder: radiusTop, radiusBottom, height, radialSegments, heightSegments, openEnded, thetaStart, thetaLength
new THREE.CylinderGeometry(1, 1, 2, 32, 1, false, 0, Math.PI * 2);

// Cone: radius, height, radialSegments, heightSegments, openEnded, thetaStart, thetaLength
new THREE.ConeGeometry(1, 2, 32, 1, false, 0, Math.PI * 2);

// Torus: radius, tube, radialSegments, tubularSegments, arc
new THREE.TorusGeometry(1, 0.4, 16, 100, Math.PI * 2);

// TorusKnot: radius, tube, tubularSegments, radialSegments, p, q
new THREE.TorusKnotGeometry(1, 0.4, 100, 16, 2, 3);

// Ring: innerRadius, outerRadius, thetaSegments, phiSegments, thetaStart, thetaLength
new THREE.RingGeometry(0.5, 1, 32, 1, 0, Math.PI * 2);
```

### Advanced Shapes
```javascript
// Capsule: radius, length, capSegments, radialSegments
new THREE.CapsuleGeometry(1, 1, 4, 8);

// Dodecahedron: radius, detail
new THREE.DodecahedronGeometry(1, 0);

// Icosahedron: radius, detail
new THREE.IcosahedronGeometry(1, 0);

// Octahedron: radius, detail
new THREE.OctahedronGeometry(1, 0);

// Tetrahedron: radius, detail
new THREE.TetrahedronGeometry(1, 0);

// Polyhedron: vertices, indices, radius, detail
new THREE.PolyhedronGeometry(vertices, indices, 1, 0);
```

### Path-based Geometries
```javascript
// Lathe: points, segments, phiStart, phiLength
const points = [new THREE.Vector2(0, 0), new THREE.Vector2(1, 0.5), new THREE.Vector2(0, 1)];
new THREE.LatheGeometry(points, 32, 0, Math.PI * 2);

// Extrude with bevel: shapes, options
const shape = new THREE.Shape();
shape.moveTo(0, 0);
shape.lineTo(0, 1);
shape.lineTo(1, 1);
shape.lineTo(1, 0);
shape.lineTo(0, 0);
const extrudeSettings = {
  depth: 2,
  bevelEnabled: true,
  bevelThickness: 0.1,
  bevelSize: 0.1,
  bevelSegments: 3,
  steps: 1
};
new THREE.ExtrudeGeometry(shape, extrudeSettings);

// Tube from curve: path, tubularSegments, radius, radialSegments, closed
const path = new THREE.CatmullRomCurve3([
  new THREE.Vector3(-1, 0, 0),
  new THREE.Vector3(0, 1, 0),
  new THREE.Vector3(1, 0, 0)
]);
new THREE.TubeGeometry(path, 64, 0.2, 8, false);
```

### TextGeometry
```javascript
const loader = new THREE.FontLoader();
loader.load('fonts/helvetiker_regular.typeface.json', (font) => {
  const geometry = new THREE.TextGeometry('Hello', {
    font: font,
    size: 1,
    height: 0.2,
    curveSegments: 12,
    bevelEnabled: true,
    bevelThickness: 0.03,
    bevelSize: 0.02,
    bevelSegments: 5
  });
  const mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);
});
```

## BufferGeometry

### Custom Geometry from Arrays
```javascript
const geometry = new THREE.BufferGeometry();

// Positions (3 values per vertex: x, y, z)
const positions = new Float32Array([
  -1, -1, 0,
   1, -1, 0,
   1,  1, 0,
  -1,  1, 0
]);
geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

// Indices (triangle vertex order)
const indices = new Uint16Array([0, 1, 2, 0, 2, 3]);
geometry.setIndex(new THREE.BufferAttribute(indices, 1));

// Normals (3 values per vertex)
const normals = new Float32Array([
  0, 0, 1,
  0, 0, 1,
  0, 0, 1,
  0, 0, 1
]);
geometry.setAttribute('normal', new THREE.BufferAttribute(normals, 3));

// UVs (2 values per vertex)
const uvs = new Float32Array([
  0, 0,
  1, 0,
  1, 1,
  0, 1
]);
geometry.setAttribute('uv', new THREE.BufferAttribute(uvs, 2));

// Vertex colors (3 values per vertex: r, g, b)
const colors = new Float32Array([
  1, 0, 0,
  0, 1, 0,
  0, 0, 1,
  1, 1, 0
]);
geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
```

### BufferAttribute Types
```javascript
// Float32Array: positions, normals, uvs, colors
new THREE.BufferAttribute(new Float32Array([...]), itemSize);

// Uint16Array: indices (up to 65535 vertices)
new THREE.BufferAttribute(new Uint16Array([...]), 1);

// Uint32Array: indices (larger meshes)
new THREE.BufferAttribute(new Uint32Array([...]), 1);

// Item sizes: position=3, normal=3, uv=2, color=3 or 4, index=1
```

### Modifying Geometry at Runtime
```javascript
const positionAttribute = geometry.getAttribute('position');

// Modify individual vertex
positionAttribute.setXYZ(vertexIndex, x, y, z);

// Mark for GPU update
positionAttribute.needsUpdate = true;

// Recompute normals after position changes
geometry.computeVertexNormals();

// Recompute bounding sphere for culling
geometry.computeBoundingSphere();

// Direct array access
const positions = positionAttribute.array;
positions[vertexIndex * 3] = x;
positions[vertexIndex * 3 + 1] = y;
positions[vertexIndex * 3 + 2] = z;
positionAttribute.needsUpdate = true;
```

### Interleaved Buffers
```javascript
// Combine multiple attributes in single array
const interleavedData = new Float32Array([
  // x, y, z, nx, ny, nz, u, v
  -1, -1, 0, 0, 0, 1, 0, 0,
   1, -1, 0, 0, 0, 1, 1, 0,
   1,  1, 0, 0, 0, 1, 1, 1
]);

const interleavedBuffer = new THREE.InterleavedBuffer(interleavedData, 8);
geometry.setAttribute('position', new THREE.InterleavedBufferAttribute(interleavedBuffer, 3, 0));
geometry.setAttribute('normal', new THREE.InterleavedBufferAttribute(interleavedBuffer, 3, 3));
geometry.setAttribute('uv', new THREE.InterleavedBufferAttribute(interleavedBuffer, 2, 6));
```

## EdgesGeometry & WireframeGeometry

```javascript
// EdgesGeometry: only edges where angle exceeds threshold
const edges = new THREE.EdgesGeometry(geometry, 30); // 30 degree threshold
const line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({ color: 0x000000 }));

// WireframeGeometry: all triangle edges
const wireframe = new THREE.WireframeGeometry(geometry);
const line = new THREE.LineSegments(wireframe, new THREE.LineBasicMaterial({ color: 0x000000 }));
```

## Points (Point Clouds)

```javascript
const geometry = new THREE.BufferGeometry();
const positions = new Float32Array(count * 3);
const colors = new Float32Array(count * 3);

for (let i = 0; i < count; i++) {
  positions[i * 3] = Math.random() * 10 - 5;
  positions[i * 3 + 1] = Math.random() * 10 - 5;
  positions[i * 3 + 2] = Math.random() * 10 - 5;

  colors[i * 3] = Math.random();
  colors[i * 3 + 1] = Math.random();
  colors[i * 3 + 2] = Math.random();
}

geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

const material = new THREE.PointsMaterial({
  size: 0.1,
  vertexColors: true,
  transparent: true,
  opacity: 0.8,
  sizeAttenuation: true // scale with distance
});

const points = new THREE.Points(geometry, material);
scene.add(points);
```

## Lines

```javascript
// Line: continuous line through points
const points = [
  new THREE.Vector3(-1, 0, 0),
  new THREE.Vector3(0, 1, 0),
  new THREE.Vector3(1, 0, 0)
];
const geometry = new THREE.BufferGeometry().setFromPoints(points);
const line = new THREE.Line(geometry, new THREE.LineBasicMaterial({ color: 0xff0000 }));

// LineLoop: closed loop
const loop = new THREE.LineLoop(geometry, new THREE.LineBasicMaterial({ color: 0x00ff00 }));

// LineSegments: disconnected segments (pairs of points)
const segments = new THREE.LineSegments(geometry, new THREE.LineBasicMaterial({ color: 0x0000ff }));
```

## InstancedMesh

```javascript
// Setup: geometry, material, instance count
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const count = 1000;
const instancedMesh = new THREE.InstancedMesh(geometry, material, count);

// Set transforms per instance
const dummy = new THREE.Object3D();
for (let i = 0; i < count; i++) {
  dummy.position.set(
    Math.random() * 100 - 50,
    Math.random() * 100 - 50,
    Math.random() * 100 - 50
  );
  dummy.rotation.set(
    Math.random() * Math.PI,
    Math.random() * Math.PI,
    Math.random() * Math.PI
  );
  dummy.scale.setScalar(Math.random() * 2 + 0.5);
  dummy.updateMatrix();
  instancedMesh.setMatrixAt(i, dummy.matrix);
}

// Per-instance colors
instancedMesh.instanceColor = new THREE.InstancedBufferAttribute(
  new Float32Array(count * 3),
  3
);
for (let i = 0; i < count; i++) {
  instancedMesh.setColorAt(i, new THREE.Color(Math.random(), Math.random(), Math.random()));
}

scene.add(instancedMesh);

// Runtime updates
dummy.position.y += 0.1;
dummy.updateMatrix();
instancedMesh.setMatrixAt(instanceId, dummy.matrix);
instancedMesh.instanceMatrix.needsUpdate = true;

// Raycasting
raycaster.intersectObject(instancedMesh); // returns array with instanceId property
```

## InstancedBufferGeometry

```javascript
// Custom per-instance attributes
const geometry = new THREE.InstancedBufferGeometry();

// Base geometry (shared)
const baseGeometry = new THREE.BoxGeometry(1, 1, 1);
geometry.index = baseGeometry.index;
geometry.attributes.position = baseGeometry.attributes.position;
geometry.attributes.normal = baseGeometry.attributes.normal;
geometry.attributes.uv = baseGeometry.attributes.uv;

// Per-instance offsets
const offsets = new Float32Array(count * 3);
for (let i = 0; i < count; i++) {
  offsets[i * 3] = Math.random() * 100 - 50;
  offsets[i * 3 + 1] = Math.random() * 100 - 50;
  offsets[i * 3 + 2] = Math.random() * 100 - 50;
}
geometry.setAttribute('offset', new THREE.InstancedBufferAttribute(offsets, 3));

// Per-instance colors
const colors = new Float32Array(count * 3);
for (let i = 0; i < count; i++) {
  colors[i * 3] = Math.random();
  colors[i * 3 + 1] = Math.random();
  colors[i * 3 + 2] = Math.random();
}
geometry.setAttribute('instanceColor', new THREE.InstancedBufferAttribute(colors, 3));

// Custom shader to use instance attributes
const material = new THREE.ShaderMaterial({
  vertexShader: `
    attribute vec3 offset;
    attribute vec3 instanceColor;
    varying vec3 vColor;
    void main() {
      vColor = instanceColor;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position + offset, 1.0);
    }
  `,
  fragmentShader: `
    varying vec3 vColor;
    void main() {
      gl_FragColor = vec4(vColor, 1.0);
    }
  `
});

const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);
```

## Geometry Utilities

```javascript
import { mergeGeometries } from 'three/examples/jsm/utils/BufferGeometryUtils.js';

// Merge multiple geometries into one
const geometries = [geometry1, geometry2, geometry3];
const merged = mergeGeometries(geometries);

// Merge with materials (creates groups for multi-material)
const merged = mergeGeometries(geometries, true);

// Compute tangents for normal mapping
import { computeTangents } from 'three/examples/jsm/utils/BufferGeometryUtils.js';
computeTangents(geometry);
```

## Common Patterns

### Center Geometry
```javascript
geometry.center(); // center around origin
geometry.computeBoundingBox();
const center = geometry.boundingBox.getCenter(new THREE.Vector3());
geometry.translate(-center.x, -center.y, -center.z);
```

### Scale to Fit
```javascript
geometry.computeBoundingBox();
const size = geometry.boundingBox.getSize(new THREE.Vector3());
const maxDim = Math.max(size.x, size.y, size.z);
const scale = desiredSize / maxDim;
geometry.scale(scale, scale, scale);
```

### Clone and Transform
```javascript
const clone = geometry.clone();
clone.translate(x, y, z);
clone.rotateX(angle);
clone.scale(sx, sy, sz);
```

### Morph Targets
```javascript
// Create base geometry
const geometry = new THREE.BoxGeometry(1, 1, 1);

// Create morph target (same vertex count)
const morphTarget = geometry.attributes.position.array.slice();
// Modify morphTarget array...
geometry.morphAttributes.position = [
  new THREE.BufferAttribute(morphTarget, 3)
];

// Animate in material
const material = new THREE.MeshStandardMaterial({ morphTargets: true });
const mesh = new THREE.Mesh(geometry, material);

// Control influence (0 to 1)
mesh.morphTargetInfluences[0] = 0.5;
```

## Performance Tips

1. **Use indexed geometry**: Reuse vertices with index buffer
2. **Merge static geometry**: Combine objects that don't move
3. **Use InstancedMesh**: For many copies of same geometry
4. **Reduce segment counts**: Lower poly counts for distant objects
5. **Dispose unused geometry**: Call `geometry.dispose()` when done
6. **Avoid frequent attribute updates**: Batch changes, update once per frame
7. **Use interleaved buffers**: Better cache performance for GPU
8. **Frustum culling**: Three.js automatic, ensure bounding spheres are correct
9. **LOD (Level of Detail)**: Use THREE.LOD for distance-based geometry switching
10. **Reuse geometries**: Share geometry instances across multiple meshes

```javascript
// Dispose pattern
geometry.dispose();
material.dispose();
texture.dispose();

// LOD example
const lod = new THREE.LOD();
lod.addLevel(highPolyMesh, 0);
lod.addLevel(mediumPolyMesh, 50);
lod.addLevel(lowPolyMesh, 100);
scene.add(lod);
```

## See Also

- [Fundamentals](fundamentals.md) - Scene setup, Object3D hierarchy, coordinate system
- [Materials](materials.md) - Material types to apply to geometries
- [Shaders](shaders.md) - Custom vertex/fragment shaders for geometry effects
- [Loaders](loaders.md) - Loading external 3D model geometry
