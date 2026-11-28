// Personagens 3D com tracos reconheciveis (Obi-Wan, Vader, Yoda, Imperador) e sabres de luz.
// Convencoes: frente = +Z local; o braco do sabre fica em -X; membros pendem para -Y.
// Rotacao X negativa no ombro = braco para frente/cima; no cotovelo, negativa = dobra para frente.
import * as THREE from './three.module.min.js';

const M = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.72, metalness: 0.05, ...o });
const SHINY = (color, o = {}) => M(color, { roughness: 0.2, metalness: 0.7, ...o });
const CLOTH = (color, o = {}) => M(color, { roughness: 0.96, metalness: 0, side: THREE.DoubleSide, ...o });

function put(parent, mesh, x = 0, y = 0, z = 0, shadow = true) {
  mesh.position.set(x, y, z);
  mesh.castShadow = shadow;
  parent.add(mesh);
  return mesh;
}
const caps = (r, len, m, seg = 10) => new THREE.Mesh(new THREE.CapsuleGeometry(r, len, 4, seg), m);
const sph = (r, m, ws = 18, hs = 14) => new THREE.Mesh(new THREE.SphereGeometry(r, ws, hs), m);
const bx = (w, h, d, m) => new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m);
const cyl = (rt, rb, h, m, seg = 14) => new THREE.Mesh(new THREE.CylinderGeometry(rt, rb, h, seg), m);
const cn = (r, h, m, seg = 12) => new THREE.Mesh(new THREE.ConeGeometry(r, h, seg), m);
const lathe = (pts, m, seg = 28, phi0 = 0, phiLen = Math.PI * 2) => new THREE.Mesh(new THREE.LatheGeometry(pts.map(([r, y]) => new THREE.Vector2(r, y)), seg, phi0, phiLen), m);

export const GLOW_TEX = (() => {
  const c = document.createElement('canvas');
  c.width = c.height = 64;
  const g = c.getContext('2d');
  const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, 'rgba(255,255,255,1)');
  gr.addColorStop(0.35, 'rgba(255,255,255,0.45)');
  gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr;
  g.fillRect(0, 0, 64, 64);
  return new THREE.CanvasTexture(c);
})();

function makeSaber(color, length = 1.15) {
  const g = new THREE.Group();
  const hilt = cyl(0.024, 0.028, 0.27, SHINY(0xa8b0bd), 12);
  g.add(hilt);
  for (const y of [-0.08, 0.0, 0.08]) {
    const ring = cyl(0.03, 0.03, 0.018, M(0x2a2f39), 12);
    ring.position.y = y;
    g.add(ring);
  }
  const emitter = cyl(0.03, 0.022, 0.04, SHINY(0xc7ced9), 12);
  emitter.position.y = 0.15;
  g.add(emitter);
  const bladeGroup = new THREE.Group();
  bladeGroup.position.y = 0.17;
  const core = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, length, 10), new THREE.MeshBasicMaterial({ color: 0xffffff }));
  core.position.y = length / 2;
  const halo = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, length + 0.06, 12), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.55, blending: THREE.AdditiveBlending, depthWrite: false }));
  halo.position.y = length / 2;
  const halo2 = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, length + 0.1, 12), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.2, blending: THREE.AdditiveBlending, depthWrite: false }));
  halo2.position.y = length / 2;
  bladeGroup.add(core, halo, halo2);
  const light = new THREE.PointLight(color, 4, 5, 2);
  light.position.y = length * 0.55;
  bladeGroup.add(light);
  g.add(bladeGroup);
  g.userData = { blade: bladeGroup, light, length, color };
  return g;
}

const SPEC = {
  obi: { scale: 1.0, saber: 0x5ab8ff, hipH: 0.95, legK: 1.0, torsoW: 0.42, armR: 0.052 },
  vader: { scale: 1.12, saber: 0xff2a2a, hipH: 0.95, legK: 1.0, torsoW: 0.5, armR: 0.062 },
  yoda: { scale: 0.5, saber: 0x4cff4c, hipH: 0.62, legK: 0.62, torsoW: 0.4, armR: 0.05 },
  emperor: { scale: 0.98, saber: 0xff2a2a, hipH: 0.95, legK: 1.0, torsoW: 0.4, armR: 0.05 },
};

export function buildCharacter(kind) {
  const spec = SPEC[kind];
  const s = spec.scale;
  const root = new THREE.Group();
  const flip = new THREE.Group();
  flip.position.y = spec.hipH * s;
  root.add(flip);
  const hips = new THREE.Group();
  flip.add(hips);

  // ---------- materiais por personagem
  const skin = kind === 'yoda' ? M(0x93bd6b, { roughness: 0.8 }) : kind === 'emperor' ? M(0xb9b496, { roughness: 0.85 }) : M(0xe9c3a0, { roughness: 0.8 });
  const C = {
    obi: { top: CLOTH(0xdccfae), sleeve: CLOTH(0xb89d6c), pants: CLOTH(0x7b6642), boots: M(0x3b2a1a, { roughness: 0.6 }), cloak: CLOTH(0x6b4a2b), belt: M(0x4a3320, { roughness: 0.6 }) },
    vader: { top: SHINY(0x0e0e14), sleeve: SHINY(0x101018), pants: M(0x0c0c12), boots: SHINY(0x0b0b10), cloak: CLOTH(0x07070b), belt: M(0x2a2a35, { metalness: 0.5 }) },
    yoda: { top: CLOTH(0xc9b27e), sleeve: CLOTH(0x8d6b45), pants: CLOTH(0xc9b27e), boots: M(0x93bd6b), cloak: CLOTH(0x8d6b45), belt: M(0x6a4a2a) },
    emperor: { top: CLOTH(0x0c0c13), sleeve: CLOTH(0x0b0b12), pants: CLOTH(0x0b0b12), boots: M(0x08080c), cloak: CLOTH(0x090910), belt: M(0x15151d) },
  }[kind];

  // ---------- pernas
  const legs = {};
  const lk = spec.legK;
  for (const side of [-1, 1]) {
    const thigh = new THREE.Group();
    thigh.position.set(side * 0.1 * s, -0.02 * s, 0);
    put(thigh, caps(0.078 * s, 0.34 * s * lk, C.pants), 0, -0.21 * s * lk);
    const shin = new THREE.Group();
    shin.position.y = -0.42 * s * lk;
    put(shin, caps(0.066 * s, 0.34 * s * lk, C.boots), 0, -0.2 * s * lk);
    if (kind === 'obi' || kind === 'vader') put(shin, cyl(0.082 * s, 0.07 * s, 0.1 * s, C.boots, 12), 0, -0.04 * s * lk); // cano da bota
    if (kind !== 'yoda') {
      const foot = bx(0.11 * s, 0.075 * s, 0.26 * s, C.boots);
      put(shin, foot, 0, -0.395 * s * lk, 0.05 * s);
    } else {
      for (const tx of [-1, 0, 1]) put(shin, cn(0.022, 0.1, skin, 6), tx * 0.035, -0.38 * lk, 0.1).rotation.x = Math.PI / 2;
    }
    thigh.add(shin);
    hips.add(thigh);
    legs[side < 0 ? 'R' : 'L'] = { thigh, shin };
  }
  put(hips, bx(0.3 * s, 0.14 * s, 0.2 * s, C.pants));

  // ---------- tronco
  const spine = new THREE.Group();
  spine.position.y = 0.08 * s;
  hips.add(spine);
  const tw = spec.torsoW;
  let torso;
  if (kind === 'vader') {
    torso = put(spine, bx(tw * s, 0.56 * s, 0.3 * s, C.top), 0, 0.3 * s);
  } else {
    torso = put(spine, cyl(tw * 0.5 * s, tw * 0.42 * s, 0.58 * s, C.top, 18), 0, 0.3 * s);
    torso.scale.z = 0.62;
  }
  const belt = put(spine, cyl(tw * 0.47 * s, tw * 0.47 * s, 0.08 * s, C.belt, 18), 0, 0.05 * s);
  belt.scale.z = 0.68;

  // ---------- cabeca
  const head = new THREE.Group();
  head.position.y = 0.67 * s;
  spine.add(head);
  put(spine, cyl(0.07 * s, 0.085 * s, 0.1 * s, kind === 'vader' ? C.top : skin, 12), 0, 0.6 * s); // pescoco

  if (kind === 'obi') {
    put(head, sph(0.118 * s, skin), 0, 0.0, 0);
    put(head, cn(0.022 * s, 0.05 * s, skin, 8), 0, -0.01 * s, 0.115 * s).rotation.x = Math.PI / 2; // nariz
    for (const sx of [-1, 1]) {
      put(head, sph(0.016 * s, M(0x24303c), 8, 6), sx * 0.045 * s, 0.02 * s, 0.105 * s);
      const brow = put(head, bx(0.05 * s, 0.012 * s, 0.02 * s, M(0x7a4a22)), sx * 0.045 * s, 0.05 * s, 0.108 * s);
      brow.rotation.z = sx * -0.12;
      put(head, sph(0.03 * s, skin, 8, 6), sx * 0.115 * s, 0, 0).scale.set(0.5, 1, 0.8); // orelha
    }
    const hair = put(head, sph(0.128 * s, M(0x8a5a2b, { roughness: 0.9 })), 0, 0.035 * s, -0.012 * s);
    hair.scale.set(1, 0.78, 1.08);
    put(head, sph(0.1 * s, M(0x8a5a2b, { roughness: 0.9 }), 12, 8), 0, -0.01 * s, -0.07 * s).scale.set(1.1, 1.05, 0.7); // nuca
    const beard = put(head, sph(0.105 * s, M(0xa4713f, { roughness: 0.95 })), 0, -0.09 * s, 0.05 * s);
    beard.scale.set(1.0, 1.0, 0.8);
    put(head, bx(0.085 * s, 0.022 * s, 0.03 * s, M(0xa4713f)), 0, -0.04 * s, 0.108 * s); // bigode
  } else if (kind === 'vader') {
    const helm = lathe([[0.001, 0.19], [0.07, 0.185], [0.125, 0.16], [0.152, 0.1], [0.158, 0.03], [0.15, -0.04], [0.152, -0.095], [0.19, -0.165], [0.16, -0.175]], SHINY(0x0b0b11, { roughness: 0.22 }));
    helm.scale.set(1, 1, 1.1);
    helm.position.y = 0.02 * s;
    helm.castShadow = true;
    helm.scale.multiplyScalar(s);
    head.add(helm);
    // mascara frontal
    const faceplate = new THREE.Group();
    faceplate.position.set(0, 0.0, 0.158 * s);
    head.add(faceplate);
    for (const sx of [-1, 1]) {
      const lens = put(faceplate, sph(0.048 * s, SHINY(0x14141c, { emissive: 0x1a0000 })), sx * 0.062 * s, 0.045 * s, 0);
      lens.scale.set(1.25, 0.8, 0.3);
      lens.rotation.z = sx * -0.35;
      put(faceplate, bx(0.07 * s, 0.014 * s, 0.03 * s, SHINY(0x0a0a10)), sx * 0.062 * s, 0.092 * s, -0.005 * s).rotation.z = sx * -0.35;
      put(faceplate, bx(0.014 * s, 0.07 * s, 0.025 * s, SHINY(0x181820)), sx * 0.1 * s, -0.04 * s, -0.01 * s).rotation.z = sx * 0.3;
    }
    put(faceplate, cn(0.024 * s, 0.085 * s, SHINY(0x1b1b24), 4), 0, -0.01 * s, 0.005 * s).rotation.x = Math.PI;
    put(faceplate, bx(0.13 * s, 0.075 * s, 0.03 * s, M(0x2a2a35, { metalness: 0.5 })), 0, -0.095 * s, 0);
    for (let i = -2; i <= 2; i++) put(faceplate, bx(0.01 * s, 0.06 * s, 0.014 * s, SHINY(0x6b6b78)), i * 0.024 * s, -0.095 * s, 0.018 * s);
    put(faceplate, bx(0.1 * s, 0.02 * s, 0.03 * s, SHINY(0x1b1b24)), 0, -0.145 * s, -0.01 * s); // queixo/tubo
  } else if (kind === 'yoda') {
    // yoda: cabecao enrugado, orelhas longas e caidas
    const h = put(head, sph(0.24, skin, 20, 16), 0, 0.02, 0);
    h.scale.set(1, 0.95, 0.95);
    for (const sx of [-1, 1]) {
      const ear = put(head, cn(0.1, 0.5, skin, 12), sx * 0.34, 0.06, -0.02);
      ear.rotation.z = sx * -1.45;
      ear.rotation.x = 0.0;
      ear.scale.z = 0.35;
      const inner = put(head, cn(0.06, 0.36, M(0xc99a82, { roughness: 0.9 }), 10), sx * 0.34, 0.06, 0.012);
      inner.rotation.z = sx * -1.45;
      inner.scale.z = 0.25;
      const ew = put(head, sph(0.05, M(0xf6f0dc, { roughness: 0.4 }), 14, 10), sx * 0.1, 0.05, 0.215);
      put(head, sph(0.024, M(0x6a4412, { roughness: 0.3 }), 10, 8), sx * 0.1, 0.05, 0.258);
      put(head, sph(0.01, M(0x0a0a0a), 6, 5), sx * 0.1, 0.05, 0.279);
      const lid = put(head, sph(0.056, skin, 12, 8), sx * 0.1, 0.092, 0.2);
      lid.scale.set(1.1, 0.5, 0.9);
      // rugas na testa
      for (let i = 0; i < 3; i++) put(head, bx(0.16, 0.01, 0.02, M(0x6e9a4c)), sx * 0.0, 0.14 + i * 0.03, 0.21 - i * 0.012).rotation.z = 0;
    }
    put(head, cn(0.025, 0.06, skin, 8), 0, -0.02, 0.23).rotation.x = Math.PI / 2; // nariz
    put(head, bx(0.1, 0.012, 0.03, M(0x5f8a42)), 0, -0.1, 0.205); // boca
    for (const dx of [-0.05, 0, 0.05]) put(head, cn(0.006, 0.07, M(0xeeeee6), 4), dx, 0.25, -0.02).rotation.z = dx * 3; // fios brancos
  } else {
    // imperador: capuz fundo, rosto palido e enrugado
    put(head, sph(0.092 * s, skin, 16, 12), 0, 0, 0.012 * s).scale.set(0.92, 1.12, 0.95);
    put(head, cn(0.03 * s, 0.07 * s, skin, 6), 0, -0.012 * s, 0.1 * s).rotation.x = Math.PI / 2;
    for (const sx of [-1, 1]) {
      put(head, sph(0.03 * s, M(0x1a1812, { roughness: 1 }), 10, 8), sx * 0.04 * s, 0.025 * s, 0.085 * s).scale.set(1.2, 0.8, 0.6); // orbita
      put(head, new THREE.Mesh(new THREE.SphereGeometry(0.013 * s, 8, 6), new THREE.MeshBasicMaterial({ color: 0xffd23f })), sx * 0.04 * s, 0.025 * s, 0.098 * s);
      put(head, bx(0.05 * s, 0.01 * s, 0.02 * s, M(0x8d8868)), sx * 0.05 * s, -0.045 * s, 0.07 * s).rotation.z = sx * 0.35; // ruga
    }
    put(head, bx(0.06 * s, 0.01 * s, 0.02 * s, M(0x4a4636)), 0, -0.07 * s, 0.083 * s);
    const hood = lathe([[0.001, 0.2], [0.08, 0.205], [0.15, 0.17], [0.2, 0.08], [0.215, -0.02], [0.2, -0.1], [0.15, -0.16], [0.17, -0.2]], CLOTH(0x07070c), 28, 0.85, Math.PI * 2 - 1.7);
    hood.scale.set(s, s, s * 1.15);
    hood.position.set(0, 0.01 * s, -0.045 * s);
    hood.rotation.x = -0.2;
    hood.castShadow = true;
    head.add(hood);
    const shadow = put(head, sph(0.1 * s, M(0x050508, { roughness: 1 }), 12, 8), 0, 0.105 * s, 0.02 * s); // sombra da testa
    shadow.scale.set(1.05, 0.55, 0.9);
  }

  // ---------- bracos (R = lado do sabre, em -X)
  const arms = {};
  const ar = spec.armR;
  for (const side of [-1, 1]) {
    const sh = new THREE.Group();
    sh.position.set(side * (tw / 2 + 0.04) * s, 0.5 * s, 0);
    spine.add(sh);
    put(sh, sph(ar * 1.15 * s, C.sleeve), 0, 0, 0);
    put(sh, caps(ar * s, 0.24 * s, C.sleeve), 0, -0.16 * s);
    const el = new THREE.Group();
    el.position.y = -0.32 * s;
    sh.add(el);
    put(el, caps(ar * 0.92 * s, 0.22 * s, kind === 'vader' ? SHINY(0x101018) : C.sleeve), 0, -0.15 * s);
    if (kind === 'emperor') {
      put(sh, cn(0.11 * s, 0.34 * s, C.sleeve, 12), 0, -0.2 * s).rotation.x = Math.PI; // manga larga
      put(el, cn(0.1 * s, 0.3 * s, C.sleeve, 12), 0, -0.17 * s).rotation.x = Math.PI;
    }
    if (kind === 'vader') put(el, cyl(0.062 * s, 0.07 * s, 0.1 * s, SHINY(0x14141c), 12), 0, -0.26 * s); // luva/punho
    const hand = put(el, sph(0.05 * s, kind === 'vader' ? SHINY(0x0b0b10) : skin, 12, 10), 0, -0.3 * s);
    if (kind === 'emperor') {
      for (let f = -1; f <= 1; f++) {
        const fin = put(el, cyl(0.007 * s, 0.006 * s, 0.075 * s, skin, 5), f * 0.018 * s, -0.36 * s, 0.01 * s);
        fin.rotation.x = 0.15;
      }
    }
    arms[side < 0 ? 'R' : 'L'] = { sh, el, hand };
    if (kind === 'vader') {
      const pad = put(sh, sph(0.1 * s, SHINY(0x101018), 14, 10), side * 0.015 * s, 0.035 * s, 0);
      pad.scale.set(1.2, 0.75, 1.05);
    }
  }

  // ---------- sabre na mao R
  const saber = makeSaber(spec.saber, kind === 'yoda' ? 0.9 : 1.15);
  saber.position.y = -0.3 * s;
  saber.rotation.x = Math.PI - 0.2;
  arms.R.el.add(saber);
  saber.scale.setScalar(kind === 'yoda' ? 1.5 : 1.0);

  // ---------- detalhes por personagem
  let cape = null;
  const makeCape = (w, h, mat, z = -0.16, segX = 6, segY = 12) => {
    const geo = new THREE.PlaneGeometry(w * s, h * s, segX, segY);
    geo.translate(0, -h * s * 0.5 + 0.58 * s, 0);
    const c = new THREE.Mesh(geo, mat);
    c.position.set(0, 0.0, z * s);
    c.castShadow = true;
    spine.add(c);
    c.userData.base = Float32Array.from(geo.attributes.position.array);
    return c;
  };
  if (kind === 'obi') {
    cape = makeCape(0.82, 1.35, C.cloak, -0.17);
    const cowl = put(spine, sph(0.16 * s, C.cloak, 14, 10), 0, 0.6 * s, -0.12 * s); // capuz caido nas costas
    cowl.scale.set(1.1, 0.7, 0.8);
    // sobretunica e bolsas no cinto
    put(spine, bx(0.16 * s, 0.5 * s, 0.03 * s, C.sleeve), -0.1 * s, 0.28 * s, 0.135 * s);
    put(spine, bx(0.16 * s, 0.5 * s, 0.03 * s, C.sleeve), 0.1 * s, 0.28 * s, 0.135 * s);
    for (const bxp of [-0.17, 0.17]) put(spine, bx(0.07 * s, 0.07 * s, 0.05 * s, C.belt), bxp * s, 0.02 * s, 0.1 * s);
    put(spine, bx(0.05 * s, 0.05 * s, 0.03 * s, SHINY(0xc9a24a)), 0, 0.05 * s, 0.15 * s);
  } else if (kind === 'vader') {
    cape = makeCape(1.0, 1.55, C.cloak, -0.18);
    const plate = put(spine, bx(0.32 * s, 0.26 * s, 0.05 * s, M(0x1a1a22, { metalness: 0.5, roughness: 0.35 })), 0, 0.38 * s, 0.16 * s);
    put(spine, bx(0.26 * s, 0.17 * s, 0.03 * s, M(0x242430, { metalness: 0.4 })), 0, 0.37 * s, 0.19 * s);
    [0xff3b3b, 0x4bd5ee, 0x4cff4c].forEach((c, i) => put(spine, new THREE.Mesh(new THREE.SphereGeometry(0.015 * s, 8, 6), new THREE.MeshBasicMaterial({ color: c })), (i - 1) * 0.06 * s, 0.41 * s, 0.21 * s, false));
    for (let i = -1; i <= 1; i++) put(spine, bx(0.04 * s, 0.015 * s, 0.02 * s, SHINY(0x8a8a98)), i * 0.06 * s, 0.335 * s, 0.21 * s);
    put(spine, bx(0.36 * s, 0.2 * s, 0.26 * s, SHINY(0x0b0b11)), 0, 0.16 * s, 0, true); // abdomen
    put(spine, bx(0.07 * s, 0.07 * s, 0.03 * s, SHINY(0xb6bcc8)), 0, 0.05 * s, 0.16 * s); // fivela
    put(spine, cyl(0.13 * s, 0.16 * s, 0.09 * s, SHINY(0x101018), 14), 0, 0.6 * s); // gola
  } else if (kind === 'yoda') {
    cape = makeCape(0.7, 0.9, C.cloak, -0.12, 4, 6);
    cape.position.y = -0.1 * s;
    const robe = put(hips, cyl(0.2 * s * 1.0, 0.34 * s, 0.62 * s * 1.0, C.top, 16), 0, -0.1 * s * 0.0);
    robe.position.y = -0.18;
    put(spine, cyl(tw * 0.45 * s, tw * 0.5 * s, 0.34 * s, C.cloak, 16), 0, 0.26 * s);
    put(spine, bx(0.1 * s, 0.4 * s, 0.03 * s, C.belt), 0, 0.25 * s, 0.14 * s);
  } else {
    cape = makeCape(1.0, 1.5, C.cloak, -0.17);
    const skirt = new THREE.Mesh(lathe([[0.2 * s, 0.1 * s], [0.26 * s, -0.2 * s], [0.38 * s, -0.6 * s], [0.5 * s, -0.95 * s]], CLOTH(0x090910), 20).geometry, CLOTH(0x090910));
    skirt.castShadow = true;
    hips.add(skirt);
    put(spine, cyl(tw * 0.55 * s, tw * 0.5 * s, 0.56 * s, C.top, 18), 0, 0.3 * s).scale.z = 0.7;
    put(spine, cyl(0.12 * s, 0.2 * s, 0.16 * s, C.top, 14), 0, 0.58 * s); // ombros/gola
  }

  root.userData = { kind, s, flip, hips, spine, head, legs, arms, saber, cape };
  return root;
}

export const DEF_POSE = {
  hipsRx: 0, hipsRy: 0, spRx: 0, spRy: 0, spRz: 0, headRx: 0, headRy: 0,
  rsx: -0.9, rsy: 0, rsz: 0.1, rel: -1.0,
  lsx: -0.3, lsy: 0, lsz: -0.2, lel: -0.6,
  ltx: 0, ltz: 0.05, lkn: 0, rtx: 0, rtz: -0.05, rkn: 0,
  hipY: 0,
};

export function applyPose(ch, p, t = 0) {
  const u = ch.userData;
  u.hips.rotation.set(p.hipsRx, p.hipsRy, 0);
  u.hips.position.y = p.hipY * u.s;
  u.spine.rotation.set(p.spRx, p.spRy, p.spRz);
  u.head.rotation.set(p.headRx, p.headRy, 0);
  u.arms.R.sh.rotation.set(p.rsx, p.rsy, p.rsz);
  u.arms.R.el.rotation.set(p.rel, 0, 0);
  u.arms.L.sh.rotation.set(p.lsx, p.lsy, p.lsz);
  u.arms.L.el.rotation.set(p.lel, 0, 0);
  u.legs.L.thigh.rotation.set(p.ltx, 0, p.ltz);
  u.legs.L.shin.rotation.set(p.lkn, 0, 0);
  u.legs.R.thigh.rotation.set(p.rtx, 0, p.rtz);
  u.legs.R.shin.rotation.set(p.rkn, 0, 0);
  if (u.cape) {
    const pos = u.cape.geometry.attributes.position;
    const base = u.cape.userData.base;
    for (let i = 0; i < pos.count; i++) {
      const y = base[i * 3 + 1];
      const k = Math.min(1, Math.max(0, (0.58 * u.s - y) / (1.3 * u.s)));
      pos.array[i * 3 + 2] = base[i * 3 + 2] + Math.sin(t * 3.0 + y * 4 + base[i * 3] * 3) * 0.05 * k * u.s - 0.14 * k * u.s;
    }
    pos.needsUpdate = true;
    u.cape.geometry.computeVertexNormals();
  }
}
