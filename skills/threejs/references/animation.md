# Three.js Animation

## Animation System Overview

Three.js uses a three-part system for animations:
- **AnimationClip**: Contains keyframe data (tracks)
- **AnimationMixer**: Manages animation playback for an object
- **AnimationAction**: Controls individual clip playback (play, pause, blend, etc.)

```javascript
const mixer = new THREE.AnimationMixer(model);
const action = mixer.clipAction(animationClip);
action.play();

// In animation loop
mixer.update(deltaTime);
```

## AnimationClip

An AnimationClip contains keyframe tracks that animate object properties.

```javascript
// Create clip manually
const positionKF = new THREE.VectorKeyframeTrack(
  '.position',
  [0, 1, 2],           // times
  [0, 0, 0, 10, 0, 0, 0, 5, 0]  // values (x,y,z for each time)
);

const clip = new THREE.AnimationClip('move', 2, [positionKF]);
```

### KeyframeTrack Types

```javascript
// NumberKeyframeTrack - single values
new THREE.NumberKeyframeTrack('.material.opacity', [0, 1], [1, 0]);

// VectorKeyframeTrack - position, scale (x,y,z)
new THREE.VectorKeyframeTrack('.position', [0, 1], [0,0,0, 5,2,0]);

// QuaternionKeyframeTrack - rotation
new THREE.QuaternionKeyframeTrack('.quaternion', [0, 1], [0,0,0,1, 0,0.707,0,0.707]);

// ColorKeyframeTrack - colors
new THREE.ColorKeyframeTrack('.material.color', [0, 1], [1,0,0, 0,0,1]);

// BooleanKeyframeTrack - on/off
new THREE.BooleanKeyframeTrack('.visible', [0, 0.5, 1], [true, false, true]);

// StringKeyframeTrack - discrete values
new THREE.StringKeyframeTrack('.morphTargetInfluences[0]', [0, 1], ['smile', 'frown']);
```

### Property Path Syntax

```javascript
'.position'                    // Root object position
'.scale[0]'                    // X scale component
'.material.opacity'            // Material property
'.bones[2].position'           // Bone position
'.morphTargetInfluences[0]'    // Morph target
```

### Interpolation Modes

```javascript
import { InterpolateLinear, InterpolateSmooth, InterpolateDiscrete } from 'three';

track.setInterpolation(InterpolateLinear);   // Linear (default)
track.setInterpolation(InterpolateSmooth);   // Smooth/cubic
track.setInterpolation(InterpolateDiscrete); // Step/no interpolation
```

## AnimationMixer

Manages all animations for a single object or hierarchy.

```javascript
const mixer = new THREE.AnimationMixer(model);

// Update in animation loop
const clock = new THREE.Clock();
function animate() {
  const delta = clock.getDelta();
  mixer.update(delta);
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}
```

### Mixer Events

```javascript
mixer.addEventListener('finished', (e) => {
  console.log('Animation finished:', e.action.getClip().name);
});

mixer.addEventListener('loop', (e) => {
  console.log('Loop completed:', e.action.getClip().name);
});
```

### Mixer Methods

```javascript
mixer.stopAllAction();           // Stop all animations
mixer.update(deltaTime);         // Update animations
mixer.setTime(seconds);          // Set global time
mixer.uncacheClip(clip);         // Remove clip from cache
mixer.uncacheRoot(model);        // Remove all clips for object
```

## AnimationAction

Controls playback of a single AnimationClip.

```javascript
const action = mixer.clipAction(clip);

// Basic playback
action.play();
action.stop();
action.reset();
action.paused = true;
```

### Action Properties

```javascript
action.timeScale = 1.0;      // Speed (2.0 = 2x, 0.5 = half speed, -1 = reverse)
action.weight = 1.0;         // Blend weight (0-1)
action.time = 0;             // Current time
action.enabled = true;       // Enable/disable action
action.clampWhenFinished = true;  // Stay on last frame when finished
action.repetitions = 3;      // Number of times to play (with LoopRepeat)
```

### Loop Modes

```javascript
import { LoopOnce, LoopRepeat, LoopPingPong } from 'three';

action.setLoop(LoopOnce);      // Play once and stop
action.setLoop(LoopRepeat, 5); // Repeat 5 times (Infinity for endless)
action.setLoop(LoopPingPong);  // Forward then backward
```

### Fading and Crossfading

```javascript
// Fade in over 0.5 seconds
action.fadeIn(0.5);

// Fade out over 0.5 seconds
action.fadeOut(0.5);

// Crossfade between actions
const idleAction = mixer.clipAction(idleClip);
const walkAction = mixer.clipAction(walkClip);

idleAction.play();
walkAction.play();
idleAction.crossFadeTo(walkAction, 0.3);  // 0.3 second crossfade
```

## Loading GLTF Animations

```javascript
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const loader = new GLTFLoader();
loader.load('model.glb', (gltf) => {
  const model = gltf.scene;
  scene.add(model);

  const mixer = new THREE.AnimationMixer(model);

  // Play all animations
  gltf.animations.forEach((clip) => {
    mixer.clipAction(clip).play();
  });

  // Play specific animation
  const clip = THREE.AnimationClip.findByName(gltf.animations, 'Walk');
  const action = mixer.clipAction(clip);
  action.play();

  // Store mixer for update loop
  model.userData.mixer = mixer;
});

// In animation loop
scene.traverse((obj) => {
  if (obj.userData.mixer) {
    obj.userData.mixer.update(delta);
  }
});
```

## Skeletal Animation

### Accessing Skeleton and Bones

```javascript
const skinnedMesh = model.getObjectByName('Character');
const skeleton = skinnedMesh.skeleton;
const bones = skeleton.bones;

// Find specific bone
const handBone = bones.find(b => b.name === 'Hand_R');

// Visualize skeleton
const helper = new THREE.SkeletonHelper(skinnedMesh);
scene.add(helper);
```

### Programmatic Bone Animation

```javascript
// Rotate arm bone
const armBone = skeleton.getBoneByName('UpperArm_R');
armBone.rotation.z = Math.sin(time) * 0.5;

// Update skeleton
skeleton.update();
```

### Bone Attachments

Attach objects to bones (e.g., weapon to hand).

```javascript
const handBone = skeleton.getBoneByName('Hand_R');
const weapon = new THREE.Mesh(swordGeometry, swordMaterial);

// Position relative to bone
weapon.position.set(0, 0.5, 0);
weapon.rotation.x = Math.PI / 2;

handBone.add(weapon);
```

## Morph Targets

Morph targets (blend shapes) deform geometry between states.

```javascript
// Access morph targets
const mesh = model.getObjectByName('Face');
console.log(mesh.morphTargetDictionary); // { smile: 0, frown: 1, ... }

// Manually set influence (0-1)
mesh.morphTargetInfluences[0] = 0.5;  // 50% smile

// Animate with keyframes
const morphTrack = new THREE.NumberKeyframeTrack(
  '.morphTargetInfluences[0]',
  [0, 1, 2],
  [0, 1, 0]
);
const clip = new THREE.AnimationClip('smile', 2, [morphTrack]);
```

### Morph Animation from GLTF

```javascript
loader.load('face.glb', (gltf) => {
  const face = gltf.scene.getObjectByName('Face');

  // Morph targets included in animations
  const mixer = new THREE.AnimationMixer(face);
  const smileClip = THREE.AnimationClip.findByName(gltf.animations, 'Smile');
  mixer.clipAction(smileClip).play();
});
```

## Animation Blending

### Weight-based Blending

Blend between multiple animations (idle, walk, run).

```javascript
const idleAction = mixer.clipAction(idleClip);
const walkAction = mixer.clipAction(walkClip);
const runAction = mixer.clipAction(runClip);

// Start all actions
idleAction.play();
walkAction.play();
runAction.play();

// Blend based on speed
function updateBlending(speed) {
  if (speed < 0.5) {
    idleAction.weight = 1 - speed * 2;
    walkAction.weight = speed * 2;
    runAction.weight = 0;
  } else {
    idleAction.weight = 0;
    walkAction.weight = 1 - (speed - 0.5) * 2;
    runAction.weight = (speed - 0.5) * 2;
  }
}

updateBlending(0.7); // 70% speed = blend walk/run
```

### Additive Blending

Layer animations on top of base animation (e.g., waving while walking).

```javascript
import { AnimationUtils } from 'three';

// Make clip additive
const waveClip = AnimationUtils.makeClipAdditive(originalWaveClip);

const walkAction = mixer.clipAction(walkClip);
const waveAction = mixer.clipAction(waveClip);

walkAction.play();
waveAction.play();

// Additive weight controls blend amount
waveAction.weight = 0.8;
```

## Animation Utilities

```javascript
import { AnimationUtils } from 'three';

// Find clip by name
const clip = THREE.AnimationClip.findByName(clips, 'Walk');

// Create subclip (extract portion)
const subClip = AnimationUtils.subclip(clip, 'WalkFirstHalf', 0, 30);

// Make additive
const additiveClip = AnimationUtils.makeClipAdditive(clip);

// Optimize clip (remove redundant keyframes)
clip.optimize();

// Sort tracks
clip.resetDuration(); // Recalculate duration from tracks
```

## Procedural Animation Patterns

### Smooth Damping

Smooth movement toward target value.

```javascript
function smoothDamp(current, target, velocity, smoothTime, deltaTime) {
  const omega = 2 / smoothTime;
  const x = omega * deltaTime;
  const exp = 1 / (1 + x + 0.48 * x * x + 0.235 * x * x * x);
  const change = current - target;
  const temp = (velocity + omega * change) * deltaTime;

  velocity = (velocity - omega * temp) * exp;
  const result = target + (change + temp) * exp;

  return { value: result, velocity };
}

// Usage
let pos = 0;
let vel = 0;

function animate() {
  const result = smoothDamp(pos, targetPos, vel, 0.3, deltaTime);
  pos = result.value;
  vel = result.velocity;

  object.position.x = pos;
}
```

### Spring Physics

Simple spring-based animation.

```javascript
class Spring {
  constructor(stiffness = 100, damping = 10) {
    this.stiffness = stiffness;
    this.damping = damping;
    this.velocity = 0;
    this.value = 0;
  }

  update(target, deltaTime) {
    const force = (target - this.value) * this.stiffness;
    const dampingForce = this.velocity * this.damping;
    this.velocity += (force - dampingForce) * deltaTime;
    this.value += this.velocity * deltaTime;
    return this.value;
  }
}

// Usage
const spring = new Spring(150, 15);

function animate() {
  const pos = spring.update(targetPos, deltaTime);
  object.position.x = pos;
}
```

### Oscillation Patterns

```javascript
// Sine wave (bobbing)
object.position.y = Math.sin(time * 2) * amplitude;

// Bounce (elastic)
const bounce = Math.abs(Math.sin(time * Math.PI)) * amplitude;
object.position.y = bounce;

// Circular orbit
object.position.x = Math.cos(time) * radius;
object.position.z = Math.sin(time) * radius;

// Figure-8 (lissajous)
object.position.x = Math.sin(time) * radius;
object.position.y = Math.sin(time * 2) * radius;

// Damped oscillation
const decay = Math.exp(-time * 0.5);
object.position.y = Math.sin(time * 5) * amplitude * decay;
```

## Performance Tips

### Share Animation Clips

```javascript
// Don't create new clips for each instance
const clip = clips[0];

characters.forEach(char => {
  const mixer = new THREE.AnimationMixer(char);
  mixer.clipAction(clip).play(); // Reuse same clip
});
```

### Optimize Clips

```javascript
// Remove redundant keyframes
clip.optimize();

// Remove unused tracks
clip.tracks = clip.tracks.filter(track => track.times.length > 1);
```

### Disable Off-screen Animations

```javascript
function animate() {
  characters.forEach(char => {
    if (isVisible(char)) {
      char.userData.mixer.update(delta);
    }
  });
}
```

### Cache Clips

```javascript
const clipCache = new Map();

function getClip(name, animations) {
  if (!clipCache.has(name)) {
    const clip = THREE.AnimationClip.findByName(animations, name);
    clipCache.set(name, clip);
  }
  return clipCache.get(name);
}
```

### Limit Update Frequency

```javascript
let accumulatedTime = 0;
const updateInterval = 1/30; // 30 FPS for animations

function animate() {
  const delta = clock.getDelta();
  accumulatedTime += delta;

  while (accumulatedTime >= updateInterval) {
    mixer.update(updateInterval);
    accumulatedTime -= updateInterval;
  }

  renderer.render(scene, camera);
}
```

## See Also

- [Fundamentals](fundamentals.md) - Animation loop, Clock, and delta time
- [Shaders](shaders.md) - Animated shader uniforms and procedural effects
- [Loaders](loaders.md) - Loading animated GLTF/FBX models
- [Interaction](interaction.md) - User-triggered animations and controls
