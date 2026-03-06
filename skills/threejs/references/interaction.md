# Three.js Interaction

## Raycaster

### Basic Setup
```typescript
const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();

function onPointerMove(event) {
  // Full window
  pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
  pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;

  // Canvas-specific
  const rect = canvas.getBoundingClientRect();
  pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
}

function checkIntersections() {
  raycaster.setFromCamera(pointer, camera);
  const intersects = raycaster.intersectObjects(scene.children, true);

  if (intersects.length > 0) {
    const hit = intersects[0];
    // hit.distance - distance from camera
    // hit.point - Vector3 world position
    // hit.face - Face3 (normal, materialIndex)
    // hit.object - intersected Object3D
    // hit.uv - texture coordinates
    // hit.instanceId - for InstancedMesh
  }
}
```

### Touch Support
```typescript
function onTouchMove(event) {
  event.preventDefault();
  const touch = event.touches[0];
  pointer.x = (touch.clientX / window.innerWidth) * 2 - 1;
  pointer.y = -(touch.clientY / window.innerHeight) * 2 + 1;
}
```

### Raycaster Options
```typescript
raycaster.near = 0.1;
raycaster.far = 1000;
raycaster.params.Line.threshold = 0.1; // Line detection sensitivity
raycaster.params.Points.threshold = 0.1; // Point cloud sensitivity
raycaster.layers.set(1); // Only intersect objects on layer 1
```

### Throttled Raycasting for Hover
```typescript
let lastRaycastTime = 0;
const raycastThrottle = 50; // ms

function animate(time) {
  if (time - lastRaycastTime > raycastThrottle) {
    checkIntersections();
    lastRaycastTime = time;
  }
  renderer.render(scene, camera);
}
```

## Camera Controls

### OrbitControls
```typescript
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 5;
controls.maxDistance = 50;
controls.maxPolarAngle = Math.PI / 2; // Prevent going below ground
controls.autoRotate = true;
controls.autoRotateSpeed = 2;

function animate() {
  controls.update(); // Required when damping or auto-rotate enabled
  renderer.render(scene, camera);
}
```

### FlyControls
```typescript
import { FlyControls } from 'three/examples/jsm/controls/FlyControls';

const controls = new FlyControls(camera, renderer.domElement);
controls.movementSpeed = 10;
controls.rollSpeed = Math.PI / 6;
controls.dragToLook = true;

const clock = new THREE.Clock();
function animate() {
  controls.update(clock.getDelta());
  renderer.render(scene, camera);
}
```

### FirstPersonControls
```typescript
import { FirstPersonControls } from 'three/examples/jsm/controls/FirstPersonControls';

const controls = new FirstPersonControls(camera, renderer.domElement);
controls.movementSpeed = 10;
controls.lookSpeed = 0.1;
controls.lookVertical = true;
controls.constrainVertical = true;
controls.verticalMin = 1.0;
controls.verticalMax = 2.0;

const clock = new THREE.Clock();
function animate() {
  controls.update(clock.getDelta());
  renderer.render(scene, camera);
}
```

### PointerLockControls with WASD
```typescript
import { PointerLockControls } from 'three/examples/jsm/controls/PointerLockControls';

const controls = new PointerLockControls(camera, document.body);

// Lock pointer on click
document.addEventListener('click', () => controls.lock());

const moveState = { forward: false, backward: false, left: false, right: false };
const velocity = new THREE.Vector3();
const direction = new THREE.Vector3();

document.addEventListener('keydown', (e) => {
  if (e.code === 'KeyW') moveState.forward = true;
  if (e.code === 'KeyS') moveState.backward = true;
  if (e.code === 'KeyA') moveState.left = true;
  if (e.code === 'KeyD') moveState.right = true;
});

document.addEventListener('keyup', (e) => {
  if (e.code === 'KeyW') moveState.forward = false;
  if (e.code === 'KeyS') moveState.backward = false;
  if (e.code === 'KeyA') moveState.left = false;
  if (e.code === 'KeyD') moveState.right = false;
});

const clock = new THREE.Clock();
function animate() {
  const delta = clock.getDelta();

  velocity.x -= velocity.x * 10.0 * delta;
  velocity.z -= velocity.z * 10.0 * delta;

  direction.z = Number(moveState.forward) - Number(moveState.backward);
  direction.x = Number(moveState.right) - Number(moveState.left);
  direction.normalize();

  if (moveState.forward || moveState.backward) velocity.z -= direction.z * 400.0 * delta;
  if (moveState.left || moveState.right) velocity.x -= direction.x * 400.0 * delta;

  controls.moveRight(-velocity.x * delta);
  controls.moveForward(-velocity.z * delta);

  renderer.render(scene, camera);
}
```

### TrackballControls
```typescript
import { TrackballControls } from 'three/examples/jsm/controls/TrackballControls';

const controls = new TrackballControls(camera, renderer.domElement);
controls.rotateSpeed = 1.0;
controls.zoomSpeed = 1.2;
controls.panSpeed = 0.8;
controls.staticMoving = true;
controls.dynamicDampingFactor = 0.3;

function animate() {
  controls.update();
  renderer.render(scene, camera);
}
```

### MapControls
```typescript
import { MapControls } from 'three/examples/jsm/controls/MapControls';

const controls = new MapControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.screenSpacePanning = false;
controls.minDistance = 10;
controls.maxDistance = 500;
controls.maxPolarAngle = Math.PI / 2;

function animate() {
  controls.update();
  renderer.render(scene, camera);
}
```

## TransformControls

```typescript
import { TransformControls } from 'three/examples/jsm/controls/TransformControls';

const transformControls = new TransformControls(camera, renderer.domElement);
scene.add(transformControls);

// Attach to object
transformControls.attach(selectedObject);

// Switch modes
transformControls.setMode('translate'); // or 'rotate', 'scale'
transformControls.setSpace('world'); // or 'local'

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
  if (e.key === 'g') transformControls.setMode('translate');
  if (e.key === 'r') transformControls.setMode('rotate');
  if (e.key === 's') transformControls.setMode('scale');
  if (e.key === 'Escape') transformControls.detach();
});

// Disable OrbitControls during drag
transformControls.addEventListener('dragging-changed', (event) => {
  orbitControls.enabled = !event.value;
});

// Object changed event
transformControls.addEventListener('objectChange', () => {
  console.log('Object transformed', selectedObject.position);
});
```

## DragControls

```typescript
import { DragControls } from 'three/examples/jsm/controls/DragControls';

const draggableObjects = [mesh1, mesh2, mesh3];
const dragControls = new DragControls(draggableObjects, camera, renderer.domElement);

// Events
dragControls.addEventListener('dragstart', (event) => {
  orbitControls.enabled = false;
  event.object.material.opacity = 0.5;
});

dragControls.addEventListener('drag', (event) => {
  // Constrain to ground plane
  event.object.position.y = 0;
});

dragControls.addEventListener('dragend', (event) => {
  orbitControls.enabled = true;
  event.object.material.opacity = 1.0;
});

// Disable/enable
dragControls.enabled = false;
```

## Selection System

### Click-to-Select with Visual Feedback
```typescript
let selectedObject = null;
const originalMaterials = new Map();

function onPointerClick(event) {
  pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
  pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(pointer, camera);
  const intersects = raycaster.intersectObjects(selectableObjects);

  // Deselect previous
  if (selectedObject) {
    selectedObject.material = originalMaterials.get(selectedObject);
    selectedObject = null;
  }

  // Select new
  if (intersects.length > 0) {
    selectedObject = intersects[0].object;
    originalMaterials.set(selectedObject, selectedObject.material);
    selectedObject.material = selectedObject.material.clone();
    selectedObject.material.emissive.setHex(0x555555);
  }
}
```

### Box Selection
```typescript
import { SelectionBox } from 'three/examples/jsm/interactive/SelectionBox';
import { SelectionHelper } from 'three/examples/jsm/interactive/SelectionHelper';

const selectionBox = new SelectionBox(camera, scene);
const helper = new SelectionHelper(renderer, 'selectBox');

let startPoint = new THREE.Vector2();
let isSelecting = false;

document.addEventListener('pointerdown', (e) => {
  if (e.shiftKey) {
    isSelecting = true;
    startPoint.set(e.clientX, e.clientY);
    selectionBox.startPoint.set(
      (e.clientX / window.innerWidth) * 2 - 1,
      -(e.clientY / window.innerHeight) * 2 + 1,
      0.5
    );
  }
});

document.addEventListener('pointermove', (e) => {
  if (isSelecting) {
    selectionBox.endPoint.set(
      (e.clientX / window.innerWidth) * 2 - 1,
      -(e.clientY / window.innerHeight) * 2 + 1,
      0.5
    );
    helper.onSelectMove(startPoint, new THREE.Vector2(e.clientX, e.clientY));
  }
});

document.addEventListener('pointerup', () => {
  if (isSelecting) {
    isSelecting = false;
    const selected = selectionBox.select();
    console.log('Selected objects:', selected);
    helper.onSelectOver();
  }
});
```

### Hover Effects with Cursor Change
```typescript
let hoveredObject = null;

function onPointerMove(event) {
  pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
  pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(pointer, camera);
  const intersects = raycaster.intersectObjects(hoverableObjects);

  // Remove previous hover
  if (hoveredObject && hoveredObject !== selectedObject) {
    hoveredObject.material.emissive.setHex(0x000000);
    hoveredObject = null;
    document.body.style.cursor = 'default';
  }

  // Apply new hover
  if (intersects.length > 0) {
    hoveredObject = intersects[0].object;
    if (hoveredObject !== selectedObject) {
      hoveredObject.material.emissive.setHex(0x222222);
    }
    document.body.style.cursor = 'pointer';
  }
}
```

## Keyboard Input

### Key State Tracking for WASD
```typescript
class KeyboardState {
  private keys: Map<string, boolean> = new Map();

  constructor() {
    document.addEventListener('keydown', (e) => this.keys.set(e.code, true));
    document.addEventListener('keyup', (e) => this.keys.set(e.code, false));
  }

  isPressed(code: string): boolean {
    return this.keys.get(code) || false;
  }

  isAnyPressed(...codes: string[]): boolean {
    return codes.some(code => this.isPressed(code));
  }
}

const keyboard = new KeyboardState();

function animate() {
  if (keyboard.isPressed('KeyW')) moveForward();
  if (keyboard.isPressed('KeyS')) moveBackward();
  if (keyboard.isPressed('KeyA')) moveLeft();
  if (keyboard.isPressed('KeyD')) moveRight();
  if (keyboard.isPressed('Space')) jump();
}
```

## World-Screen Coordinate Conversion

### worldToScreen (Position HTML over 3D)
```typescript
function worldToScreen(position: THREE.Vector3, camera: THREE.Camera): { x: number, y: number } {
  const vector = position.clone().project(camera);

  return {
    x: (vector.x * 0.5 + 0.5) * window.innerWidth,
    y: (-vector.y * 0.5 + 0.5) * window.innerHeight
  };
}

// Usage: Position HTML label
const screenPos = worldToScreen(mesh.position, camera);
labelElement.style.left = `${screenPos.x}px`;
labelElement.style.top = `${screenPos.y}px`;
```

### screenToWorld (Unproject)
```typescript
function screenToWorld(x: number, y: number, z: number, camera: THREE.Camera): THREE.Vector3 {
  const vector = new THREE.Vector3(
    (x / window.innerWidth) * 2 - 1,
    -(y / window.innerHeight) * 2 + 1,
    z
  );

  return vector.unproject(camera);
}

// Usage: Get ray direction
const near = screenToWorld(event.clientX, event.clientY, 0, camera);
const far = screenToWorld(event.clientX, event.clientY, 1, camera);
const direction = far.sub(near).normalize();
```

### Ray-Plane Intersection for Ground Positioning
```typescript
function getGroundPosition(event: MouseEvent, camera: THREE.Camera): THREE.Vector3 | null {
  const pointer = new THREE.Vector2(
    (event.clientX / window.innerWidth) * 2 - 1,
    -(event.clientY / window.innerHeight) * 2 + 1
  );

  raycaster.setFromCamera(pointer, camera);

  const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
  const intersection = new THREE.Vector3();

  return raycaster.ray.intersectPlane(plane, intersection);
}

// Usage: Place object on ground at mouse position
const groundPos = getGroundPosition(event, camera);
if (groundPos) {
  object.position.copy(groundPos);
}
```

## Event Handling Best Practices

### InteractionManager Class Pattern
```typescript
class InteractionManager {
  private raycaster = new THREE.Raycaster();
  private pointer = new THREE.Vector2();
  private selectedObject: THREE.Object3D | null = null;
  private hoveredObject: THREE.Object3D | null = null;

  constructor(
    private camera: THREE.Camera,
    private scene: THREE.Scene,
    private canvas: HTMLCanvasElement
  ) {
    this.setupEventListeners();
  }

  private setupEventListeners() {
    this.canvas.addEventListener('pointermove', this.onPointerMove.bind(this));
    this.canvas.addEventListener('click', this.onClick.bind(this));
  }

  private updatePointer(event: PointerEvent) {
    const rect = this.canvas.getBoundingClientRect();
    this.pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    this.pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
  }

  private onPointerMove(event: PointerEvent) {
    this.updatePointer(event);
    this.updateHover();
  }

  private onClick(event: PointerEvent) {
    this.updatePointer(event);
    this.updateSelection();
  }

  private getIntersections(): THREE.Intersection[] {
    this.raycaster.setFromCamera(this.pointer, this.camera);
    return this.raycaster.intersectObjects(this.scene.children, true);
  }

  private updateHover() {
    const intersects = this.getIntersections();

    if (this.hoveredObject) {
      this.hoveredObject.dispatchEvent({ type: 'hoverout' });
      this.hoveredObject = null;
    }

    if (intersects.length > 0) {
      this.hoveredObject = intersects[0].object;
      this.hoveredObject.dispatchEvent({ type: 'hoverover' });
    }
  }

  private updateSelection() {
    const intersects = this.getIntersections();

    if (this.selectedObject) {
      this.selectedObject.dispatchEvent({ type: 'deselect' });
      this.selectedObject = null;
    }

    if (intersects.length > 0) {
      this.selectedObject = intersects[0].object;
      this.selectedObject.dispatchEvent({ type: 'select' });
    }
  }

  dispose() {
    this.canvas.removeEventListener('pointermove', this.onPointerMove.bind(this));
    this.canvas.removeEventListener('click', this.onClick.bind(this));
  }
}

// Usage
const manager = new InteractionManager(camera, scene, renderer.domElement);

mesh.addEventListener('select', () => console.log('Selected!'));
mesh.addEventListener('hoverover', () => console.log('Hover!'));
```

## Performance Tips

### Throttle Raycasts
```typescript
// Use requestAnimationFrame for hover detection instead of raw mousemove
let rafId: number | null = null;

canvas.addEventListener('pointermove', (e) => {
  if (rafId !== null) return;

  rafId = requestAnimationFrame(() => {
    updatePointer(e);
    checkIntersections();
    rafId = null;
  });
});
```

### Use Layers
```typescript
// Interactive objects on layer 1
mesh.layers.set(1);

// Configure raycaster to only check layer 1
raycaster.layers.set(1);

// Camera must also see the layer
camera.layers.enable(1);
```

### Simple Collision Meshes
```typescript
// Use invisible simplified geometry for raycasting
const interactionMesh = new THREE.Mesh(
  new THREE.BoxGeometry(10, 10, 10),
  new THREE.MeshBasicMaterial({ visible: false })
);

const detailedMesh = new THREE.Mesh(
  complexGeometry,
  material
);

const group = new THREE.Group();
group.add(interactionMesh);
group.add(detailedMesh);

// Raycast only against interactionMesh
raycaster.intersectObject(interactionMesh);
```

### Disable Unused Controls
```typescript
// Disable controls when not needed
orbitControls.enabled = false;

// Or remove event listeners
orbitControls.dispose();

// Re-enable when needed
orbitControls.enabled = true;
```

### Limit Raycast Recursion
```typescript
// Don't recursively check all children
raycaster.intersectObjects(scene.children, false); // Only direct children

// Or maintain array of only interactive objects
const interactiveObjects: THREE.Object3D[] = [mesh1, mesh2, mesh3];
raycaster.intersectObjects(interactiveObjects);
```

## See Also

- [Fundamentals](fundamentals.md) - Coordinate systems and Object3D hierarchy
- [Animation](animation.md) - User-triggered animation playback
- [Geometry](geometry.md) - Raycasting targets and bounding boxes
- [Postprocessing](postprocessing.md) - Outline and selection visual effects
