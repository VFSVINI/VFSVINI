// Motor da cena 3D: mundo, lutadores com trilhas de animacao, efeitos e diretor de camera.
// Tudo e funcao do tempo t (renderizacao deterministica, quadro a quadro).
import * as THREE from './three.module.min.js';
import { buildCharacter, applyPose, DEF_POSE, GLOW_TEX } from './chars.js';

export const W = 900;
export const H = 344;

export const smooth = (x) => x * x * (3 - 2 * x);
export const lerp = (a, b, k) => a + (b - a) * k;
export function rng(seed) {
  let s = seed >>> 0;
  return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296;
}

// ---------------------------------------------------------------- trilhas
function sampleKeys(keys, t) {
  if (t <= keys[0].t) return keys[0].v;
  const last = keys[keys.length - 1];
  if (t >= last.t) return last.v;
  let i = 0;
  while (keys[i + 1].t < t) i++;
  const a = keys[i], b = keys[i + 1];
  const k = smooth((t - a.t) / (b.t - a.t));
  if (typeof a.v === 'number') return lerp(a.v, b.v, k);
  const out = {};
  for (const key in a.v) out[key] = lerp(a.v[key], b.v[key], k);
  return out;
}

export const POSES = {
  guard: { rsx: -1.2, rel: -1.45, rsz: -0.05, lsx: -0.75, lel: -1.1, lsz: -0.15, spRy: 0.3, ltx: -0.4, lkn: 0.6, rtx: 0.3, rkn: 0.5, hipY: -0.12, hipsRy: 0.2 },
  guardLow: { rsx: -0.8, rel: -1.2, rsz: -0.1, lsx: -0.5, lel: -0.9, spRy: 0.4, ltx: -0.5, lkn: 0.8, rtx: 0.4, rkn: 0.7, hipY: -0.25, spRx: 0.15 },
  windup: { rsx: -2.7, rel: -0.7, rsz: -0.2, lsx: -0.9, lel: -1.0, spRx: -0.18, spRy: -0.55, ltx: -0.2, lkn: 0.4, rtx: 0.1, rkn: 0.3, hipY: -0.08, hipsRy: -0.3 },
  strike: { rsx: -1.55, rel: -0.25, rsz: -0.1, lsx: -0.4, lel: -0.8, spRx: 0.32, spRy: 0.7, ltx: -0.95, lkn: 1.0, rtx: 0.5, rkn: 0.25, hipY: -0.22, hipsRy: 0.45 },
  slash: { rsx: -1.35, rel: -0.3, rsz: -1.25, lsx: -0.2, lsz: 0.7, lel: -0.4, spRy: -0.95, spRz: 0.15, ltx: -0.7, lkn: 0.9, rtx: 0.55, rkn: 0.3, hipY: -0.2, hipsRy: -0.4 },
  thrust: { rsx: -1.5, rel: -0.15, rsz: -0.05, lsx: -0.6, lel: -0.7, spRx: 0.12, spRy: 0.5, ltx: -1.1, lkn: 1.0, rtx: 0.55, rkn: 0.1, hipY: -0.2 },
  parryHigh: { rsx: -2.15, rel: -1.15, rsz: -0.1, lsx: -1.3, lel: -0.9, spRx: -0.1, spRy: 0.2, ltx: -0.3, lkn: 0.5, rtx: 0.2, rkn: 0.4, hipY: -0.1 },
  parryLow: { rsx: -0.7, rel: -1.3, rsz: -0.15, lsx: -0.4, lel: -0.7, spRx: 0.2, ltx: -0.6, lkn: 0.9, rtx: 0.4, rkn: 0.8, hipY: -0.28 },
  crouch: { rsx: -1.0, rel: -1.3, lsx: -0.6, lel: -0.9, ltx: -0.9, lkn: 1.5, rtx: -0.7, rkn: 1.4, hipY: -0.42, spRx: 0.25 },
  leap: { rsx: -1.6, rel: -1.3, rsz: -0.4, lsx: -1.2, lel: -1.0, lsz: 0.4, ltx: -1.5, lkn: 1.9, rtx: -1.3, rkn: 1.7, hipY: 0.0, spRx: 0.2 },
  air: { rsx: -1.9, rel: -0.6, rsz: -0.9, lsx: -0.2, lsz: 1.0, lel: -0.5, ltx: -0.4, lkn: 0.5, rtx: 0.2, rkn: 0.3, hipY: 0 },
  force: { rsx: -1.1, rel: -1.2, lsx: -1.55, lel: -0.1, lsz: -0.05, spRy: -0.2, ltx: -0.5, lkn: 0.7, rtx: 0.3, rkn: 0.5, hipY: -0.15 },
  zap: { rsx: -1.5, rel: -0.2, rsz: -0.45, lsx: -1.5, lel: -0.2, lsz: 0.45, spRx: 0.05, ltx: -0.4, lkn: 0.5, rtx: 0.2, rkn: 0.4, hipY: -0.1 },
  thrown: { rsx: -0.5, rel: -0.5, rsz: -0.8, lsx: -0.5, lsz: 0.8, lel: -0.4, spRx: -0.35, ltx: 0.3, lkn: 0.3, rtx: 0.1, rkn: 0.3, hipY: 0 },
};
const fullPose = (name) => ({ ...DEF_POSE, ...(POSES[name] || {}) });

export class Fighter {
  constructor(kind, x, z, yaw) {
    this.kind = kind;
    this.ch = buildCharacter(kind);
    this.rootKeys = [{ t: 0, v: { x, y: 0, z, yaw, flip: 0 } }];
    this.poseKeys = [{ t: 0, v: fullPose('guard') }];
    this.saberKeys = [{ t: 0, v: 1 }];
    this.trail = [];
  }
  _push(keys, t, v) {
    const last = keys[keys.length - 1];
    if (t < last.t) throw new Error(`chave fora de ordem em ${this.kind}: ${t} < ${last.t}`);
    keys.push({ t, v });
  }
  /** Mover/girar: segura o valor atual ate t0 e vai para o alvo em t0+dur. */
  move(t0, dur, target) {
    const cur = this.rootKeys[this.rootKeys.length - 1];
    if (cur.t < t0) this._push(this.rootKeys, t0, cur.v);
    this._push(this.rootKeys, t0 + dur, { ...cur.v, ...target });
    return this;
  }
  pose(t0, dur, name) {
    const cur = this.poseKeys[this.poseKeys.length - 1];
    if (cur.t < t0) this._push(this.poseKeys, t0, cur.v);
    this._push(this.poseKeys, t0 + dur, fullPose(name));
    return this;
  }
  saber(t0, dur, on) {
    const cur = this.saberKeys[this.saberKeys.length - 1];
    if (cur.t < t0) this._push(this.saberKeys, t0, cur.v);
    this._push(this.saberKeys, t0 + dur, on ? 1 : 0);
    return this;
  }
  stateAt(t) {
    return sampleKeys(this.rootKeys, t);
  }
  update(t) {
    const r = sampleKeys(this.rootKeys, t);
    const p = sampleKeys(this.poseKeys, t);
    const sb = sampleKeys(this.saberKeys, t);
    const ch = this.ch;
    ch.position.set(r.x, r.y, r.z);
    ch.rotation.y = r.yaw;
    ch.userData.flip.rotation.x = r.flip;
    // respiracao
    const breath = Math.sin(t * 2.2 + r.x) * 0.012;
    applyPose(ch, { ...p, spRx: p.spRx + breath, hipY: p.hipY }, t);
    const sab = ch.userData.saber;
    sab.userData.blade.scale.y = Math.max(0.001, sb);
    sab.userData.blade.visible = sb > 0.01;
    sab.userData.light.intensity = 4 * sb * (0.92 + 0.08 * Math.sin(t * 40 + r.x));
  }
  /** Posicoes mundiais da base e da ponta do sabre (apos update). */
  saberPoints() {
    const sab = this.ch.userData.saber;
    this.ch.updateMatrixWorld(true);
    const len = sab.userData.length * sab.scale.x * sab.userData.blade.scale.y;
    const base = new THREE.Vector3(0, 0.13, 0);
    const tip = new THREE.Vector3(0, 0.13 + sab.userData.length * sab.userData.blade.scale.y, 0);
    return { base: sab.localToWorld(base), tip: sab.localToWorld(tip) };
  }
}

// ---------------------------------------------------------------- mundo
export function createWorld() {
  const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('c'), antialias: true, preserveDrawingBuffer: true });
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.setSize(W, H, false);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.15;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x04060f);
  scene.fog = new THREE.FogExp2(0x070b18, 0.018);
  const camera = new THREE.PerspectiveCamera(32, W / H, 0.1, 200);

  scene.add(new THREE.HemisphereLight(0x7f9ed8, 0x1a1020, 1.15));
  const key = new THREE.DirectionalLight(0xcfdcff, 2.6);
  key.position.set(-6, 11, 9);
  key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  Object.assign(key.shadow.camera, { left: -16, right: 16, top: 10, bottom: -8, near: 1, far: 40 });
  key.shadow.bias = -0.0005;
  scene.add(key);
  const rim = new THREE.DirectionalLight(0xff6a5a, 1.1);
  rim.position.set(8, 5, -9);
  scene.add(rim);

  // chao
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(120, 120), new THREE.MeshStandardMaterial({ color: 0x141c34, roughness: 0.42, metalness: 0.45 }));
  floor.rotation.x = -Math.PI / 2;
  floor.receiveShadow = true;
  scene.add(floor);
  const grid = new THREE.GridHelper(120, 120, 0x2a3a6b, 0x1a2444);
  grid.position.y = 0.01;
  grid.material.transparent = true;
  grid.material.opacity = 0.35;
  scene.add(grid);

  // arenas
  const arenas = [
    { x: -6, color: 0x4bd5ee },
    { x: 6, color: 0xff3a3a },
  ];
  for (const a of arenas) {
    const ring = new THREE.Mesh(new THREE.RingGeometry(3.3, 3.45, 64), new THREE.MeshBasicMaterial({ color: a.color, transparent: true, opacity: 0.9, side: THREE.DoubleSide }));
    ring.rotation.x = -Math.PI / 2;
    ring.position.set(a.x, 0.02, 0);
    scene.add(ring);
    const halo = new THREE.Mesh(new THREE.RingGeometry(3.45, 4.4, 64), new THREE.MeshBasicMaterial({ color: a.color, transparent: true, opacity: 0.12, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false }));
    halo.rotation.x = -Math.PI / 2;
    halo.position.set(a.x, 0.03, 0);
    scene.add(halo);
    const disc = new THREE.Mesh(new THREE.CircleGeometry(3.3, 64), new THREE.MeshStandardMaterial({ color: 0x0c1226, roughness: 0.3, metalness: 0.7 }));
    disc.rotation.x = -Math.PI / 2;
    disc.position.set(a.x, 0.015, 0);
    disc.receiveShadow = true;
    scene.add(disc);
    const l = new THREE.PointLight(a.color, 6, 14, 2);
    l.position.set(a.x, 3.5, 0);
    scene.add(l);
  }

  // colunas ao fundo
  const colMat = new THREE.MeshStandardMaterial({ color: 0x1b2442, roughness: 0.7, metalness: 0.2, flatShading: true });
  for (let i = -6; i <= 6; i++) {
    const c = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.65, 14, 8), colMat);
    c.position.set(i * 4.4, 7, -10 - (i % 2 === 0 ? 0 : 1.5));
    c.castShadow = true;
    scene.add(c);
  }
  // estrelas e planeta
  const R = rng(5);
  const sp = new Float32Array(600 * 3);
  for (let i = 0; i < 600; i++) {
    const th = R() * Math.PI * 2, ph = Math.acos(R() * 0.8 + 0.1);
    sp[i * 3] = 90 * Math.sin(ph) * Math.cos(th);
    sp[i * 3 + 1] = 90 * Math.cos(ph) * 0.8 + 6;
    sp[i * 3 + 2] = -90 * Math.abs(Math.sin(ph) * Math.sin(th)) - 10;
  }
  const sg = new THREE.BufferGeometry();
  sg.setAttribute('position', new THREE.BufferAttribute(sp, 3));
  scene.add(new THREE.Points(sg, new THREE.PointsMaterial({ color: 0xffffff, size: 0.5, sizeAttenuation: true, fog: false })));
  const planet = new THREE.Mesh(new THREE.SphereGeometry(14, 24, 16), new THREE.MeshBasicMaterial({ color: 0x1a2a55, fog: false }));
  planet.position.set(-22, 26, -80);
  scene.add(planet);
  const planetGlow = new THREE.Sprite(new THREE.SpriteMaterial({ map: GLOW_TEX, color: 0x4a6fd0, transparent: true, opacity: 0.55, blending: THREE.AdditiveBlending, fog: false }));
  planetGlow.scale.set(60, 60, 1);
  planetGlow.position.copy(planet.position);
  scene.add(planetGlow);

  return { renderer, scene, camera, key };
}

// ---------------------------------------------------------------- efeitos
export class Effects {
  constructor(scene) {
    this.scene = scene;
    this.events = []; // {t, kind, pos, big, seed}
    this.sparkGroup = new THREE.Group();
    scene.add(this.sparkGroup);
    this.flashSprites = [];
    this.rings = [];
    this.dusts = [];
    this.bolts = [];
    this.pointsMat = new THREE.PointsMaterial({ size: 0.11, vertexColors: true, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, map: GLOW_TEX, sizeAttenuation: true });
    this.sparks = new THREE.Points(new THREE.BufferGeometry(), this.pointsMat);
    this.sparks.frustumCulled = false;
    scene.add(this.sparks);
    this.boltLines = new THREE.LineSegments(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({ color: 0xcfeeff, transparent: true, opacity: 0.95, blending: THREE.AdditiveBlending }));
    this.boltLines.frustumCulled = false;
    scene.add(this.boltLines);
    this.boltGlow = new THREE.LineSegments(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({ color: 0x3f8cff, transparent: true, opacity: 0.55, blending: THREE.AdditiveBlending }));
    this.boltGlow.frustumCulled = false;
    scene.add(this.boltGlow);
    this.flashLight = new THREE.PointLight(0xffe9b0, 0, 12, 2);
    scene.add(this.flashLight);
    this.sprites = [];
    for (let i = 0; i < 24; i++) {
      const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: GLOW_TEX, transparent: true, depthWrite: false }));
      sp.visible = false;
      scene.add(sp);
      this.sprites.push(sp);
    }
    this.ringMeshes = [];
    for (let i = 0; i < 8; i++) {
      const m = new THREE.Mesh(new THREE.RingGeometry(0.96, 1.0, 48), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false }));
      m.rotation.x = -Math.PI / 2;
      m.visible = false;
      scene.add(m);
      this.ringMeshes.push(m);
    }
  }
  add(ev) {
    ev.seed = ev.seed || this.events.length * 977 + 13;
    this.events.push(ev);
  }
  update(t, camera) {
    // faiscas
    const pos = [], col = [];
    let flash = 0;
    const flashPos = new THREE.Vector3();
    let si = 0, ri = 0;
    this.sprites.forEach((s) => (s.visible = false));
    this.ringMeshes.forEach((m) => (m.visible = false));
    const boltPts = [], boltPts2 = [];
    for (const ev of this.events) {
      const tau = (t - ev.t) * (ev.slow || 1);
      if (ev.kind === 'clash') {
        if (tau >= 0 && tau < 1.3) {
          const R = rng(ev.seed);
          const n = Math.round(46 * ev.big);
          for (let i = 0; i < n; i++) {
            const th = R() * Math.PI * 2, ph = (R() - 0.35) * 2.2, sp = (2 + R() * 6) * (0.8 + ev.big * 0.3);
            const vx = Math.cos(th) * Math.cos(ph) * sp, vy = Math.sin(ph) * sp + 2.5, vz = Math.sin(th) * Math.cos(ph) * sp;
            const life = 0.5 + R() * 0.8;
            if (tau > life) continue;
            const x = ev.pos.x + vx * tau, z = ev.pos.z + vz * tau;
            let y = ev.pos.y + vy * tau - 5.5 * tau * tau;
            if (y < 0.02) y = 0.02;
            pos.push(x, y, z);
            const k = 1 - tau / life;
            col.push(1.0 * k + 0.2, (0.85 * k) * k + 0.1 * k, 0.45 * k * k);
          }
        }
        if (tau >= -0.02 && tau < 0.32 && si < this.sprites.length) {
          const s = this.sprites[si++];
          const k = Math.max(0, 1 - Math.max(0, tau) / 0.32);
          s.visible = true;
          s.position.copy(ev.pos);
          s.scale.setScalar(1.2 + 3.2 * ev.big * (1 - k * 0.6));
          s.material.color.setRGB(1, 0.92, 0.65);
          s.material.opacity = k;
          s.material.blending = THREE.AdditiveBlending;
        }
        if (tau >= 0 && tau < 0.55 && ri < this.ringMeshes.length && ev.big >= 1.2) {
          const m = this.ringMeshes[ri++];
          m.visible = true;
          m.position.set(ev.pos.x, 0.04, ev.pos.z);
          m.scale.setScalar(0.4 + (3.5 * ev.big * tau) / 0.55);
          m.material.opacity = 0.6 * (1 - tau / 0.55);
          m.material.color.setRGB(1, 0.9, 0.7);
        }
        if (tau >= -0.02 && tau < 0.35) {
          const k = 1 - Math.max(0, tau) / 0.35;
          if (k * ev.big > flash) {
            flash = k * ev.big;
            flashPos.copy(ev.pos);
          }
        }
      } else if (ev.kind === 'push') {
        if (tau >= 0 && tau < 0.9) {
          for (let k = 0; k < 3 && ri < this.ringMeshes.length; k++) {
            const tt = tau - k * 0.12;
            if (tt < 0 || tt > 0.6) continue;
            const m = this.ringMeshes[ri++];
            m.visible = true;
            m.position.set(ev.pos.x, 0.05 + k * 0.01, ev.pos.z);
            m.scale.setScalar(0.5 + 6.5 * (tt / 0.6));
            m.material.opacity = 0.75 * (1 - tt / 0.6);
            m.material.color.setRGB(0.55, 0.8, 1);
          }
          if (tau < 0.3) {
            flash = Math.max(flash, 1 - tau / 0.3);
            flashPos.copy(ev.pos);
          }
        }
      } else if (ev.kind === 'land') {
        if (tau >= 0 && tau < 0.8) {
          for (let k = 0; k < 3 && si < this.sprites.length; k++) {
            const s = this.sprites[si++];
            const dirx = k === 0 ? -1 : k === 1 ? 1 : 0, dirz = k === 2 ? 1 : 0.3 * (k - 0.5);
            s.visible = true;
            s.position.set(ev.pos.x + dirx * tau * 1.5, 0.1 + tau * 0.5, ev.pos.z + dirz * tau * 1.5);
            s.scale.setScalar(0.5 + tau * 2.4);
            s.material.color.setRGB(0.55, 0.5, 0.42);
            s.material.opacity = 0.55 * (1 - tau / 0.8);
            s.material.blending = THREE.NormalBlending;
          }
        }
      } else if (ev.kind === 'bolt') {
        if (t >= ev.t && t < ev.t1) {
          const fi = Math.floor(t * 18);
          const R = rng(fi * 31 + ev.seed);
          const segs = (a, b, amp) => {
            const n = 12;
            let prev = a.clone();
            for (let i = 1; i <= n; i++) {
              const u = i / n;
              const p = a.clone().lerp(b, u);
              if (i < n) p.add(new THREE.Vector3((R() - 0.5) * amp, (R() - 0.5) * amp, (R() - 0.5) * amp));
              boltPts.push(prev.x, prev.y, prev.z, p.x, p.y, p.z);
              prev = p;
            }
          };
          const a = ev.from(t), b = ev.to(t);
          for (let k = 0; k < 3; k++) segs(a, b, 0.5);
          for (let k = 0; k < 4; k++) segs(a, b, 0.9);
          boltPts2.push(...boltPts);
          if (si < this.sprites.length) {
            const s = this.sprites[si++];
            s.visible = true;
            s.position.copy(b);
            s.scale.setScalar(1.6 + R() * 0.8);
            s.material.color.setRGB(0.6, 0.85, 1);
            s.material.opacity = 0.9;
            s.material.blending = THREE.AdditiveBlending;
          }
          flash = Math.max(flash, 0.35);
          flashPos.copy(b);
        }
      }
    }
    const g = this.sparks.geometry;
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    const bg = this.boltLines.geometry;
    bg.setAttribute('position', new THREE.Float32BufferAttribute(boltPts, 3));
    const bg2 = this.boltGlow.geometry;
    bg2.setAttribute('position', new THREE.Float32BufferAttribute(boltPts2, 3));
    this.flashLight.intensity = flash * 28;
    this.flashLight.position.copy(flashPos);
    return flash;
  }
}

// ---------------------------------------------------------------- rastro dos sabres
export class Trails {
  constructor(scene, fighters) {
    this.fighters = fighters;
    this.meshes = fighters.map((f) => {
      const geo = new THREE.BufferGeometry();
      const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: f.ch.userData.saber.userData.color, transparent: true, opacity: 0.22, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false, vertexColors: true }));
      m.frustumCulled = false;
      scene.add(m);
      return m;
    });
  }
  update(t) {
    const N = 5, dt = 0.02;
    this.fighters.forEach((f, idx) => {
      const pts = [];
      for (let k = 0; k <= N; k++) {
        f.update(Math.max(0, t - k * dt));
        const { base, tip } = f.saberPoints();
        pts.push({ base, tip });
      }
      f.update(t);
      const pos = [], col = [];
      for (let k = 0; k < N; k++) {
        const a = pts[k], b = pts[k + 1];
        const ka = 1 - k / N, kb = 1 - (k + 1) / N;
        const push = (p, c) => {
          pos.push(p.x, p.y, p.z);
          col.push(c, c, c);
        };
        // dois triangulos entre os segmentos (base->ponta)
        push(a.base, ka * 0.0); push(a.tip, ka); push(b.tip, kb);
        push(a.base, ka * 0.0); push(b.tip, kb); push(b.base, kb * 0.0);
      }
      const g = this.meshes[idx].geometry;
      g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
      g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    });
  }
}

// ---------------------------------------------------------------- camera
export class Director {
  constructor(camera) {
    this.camera = camera;
    this.shots = []; // {t0,t1, fn(u, t) -> {pos, look, fov}}
  }
  shot(t0, t1, fn) {
    this.shots.push({ t0, t1, fn });
    return this;
  }
  apply(t, shake = 0) {
    let s = this.shots.find((x) => t >= x.t0 && t < x.t1) || this.shots[this.shots.length - 1];
    const u = Math.min(1, Math.max(0, (t - s.t0) / (s.t1 - s.t0)));
    const r = s.fn(smooth(u), t, u);
    const cam = this.camera;
    const hh = 0.012; // handheld leve
    cam.position.set(r.pos[0] + Math.sin(t * 1.3) * hh, r.pos[1] + Math.sin(t * 1.7 + 1) * hh, r.pos[2] + Math.sin(t * 1.1 + 2) * hh);
    if (shake > 0) {
      cam.position.x += (Math.sin(t * 91) + Math.sin(t * 57)) * 0.04 * shake;
      cam.position.y += (Math.sin(t * 83) + Math.sin(t * 61)) * 0.04 * shake;
    }
    cam.lookAt(r.look[0], r.look[1], r.look[2]);
    cam.fov = r.fov;
    cam.updateProjectionMatrix();
  }
}
