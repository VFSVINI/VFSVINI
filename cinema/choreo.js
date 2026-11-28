// Coreografia completa (120 s) e direcao de camera.
// Arena A (azul) em x=-6: Obi-Wan x Vader. Arena B (vermelha) em x=+6: Yoda x Imperador.
// Trechos de fundo usam autoFight (trocas de golpes geradas com semente); os de destaque sao escritos a mao.
import * as THREE from './three.module.min.js';
import { Fighter, Effects, Trails, Director, rng } from './world.js';

const PI = Math.PI;
const FACE_R = PI / 2;   // olhando para +X
const FACE_L = -PI / 2;  // olhando para -X
export const DURATION = 120;

export function buildShow(scene) {
  const obi = new Fighter('obi', -7.3, 0, FACE_R);
  const vader = new Fighter('vader', -4.7, 0, FACE_L);
  const yoda = new Fighter('yoda', 4.7, 0, FACE_R);
  const emp = new Fighter('emperor', 7.3, 0, FACE_L);
  const all = [obi, vader, yoda, emp];
  all.forEach((f) => {
    scene.add(f.ch);
    f.saberKeys[0].v = 0;
  });
  const fx = new Effects(scene);

  // ------------------------------------------------ utilitarios
  const mid = (a, b, t) => {
    a.update(t);
    b.update(t);
    const pa = a.saberPoints(), pb = b.saberPoints();
    return new THREE.Vector3().addVectors(pa.tip.clone().lerp(pa.base, 0.35), pb.tip.clone().lerp(pb.base, 0.35)).multiplyScalar(0.5);
  };
  const clash = (t, a, b, big = 1, slow = 1) => fx.add({ t, kind: 'clash', pos: mid(a, b, t), big, slow });
  const land = (t, f, slow = 1) => fx.add({ t, kind: 'land', pos: new THREE.Vector3(f.stateAt(t).x, 0, f.stateAt(t).z), slow });
  const handPos = (f, t, side = 'L') => {
    f.update(t);
    f.ch.updateMatrixWorld(true);
    return f.ch.userData.arms[side].hand.getWorldPosition(new THREE.Vector3());
  };
  const cur = (f) => f.rootKeys[f.rootKeys.length - 1].v;

  /** Salto acrobatico: agacha, voa em arco com giros (turns > 0 = para frente, < 0 = para tras) e pousa em toX. */
  function leap(f, t, toX, { h = 1.5, turns = 1, dur = 0.9, toYaw = null, ts = 1, endPose = 'guard' } = {}) {
    dur *= ts;
    f.pose(t - 0.3 * ts, 0.3 * ts, 'crouch');
    f.pose(t, 0.2 * ts, 'leap');
    const c = cur(f);
    const mx = (c.x + toX) / 2;
    f.move(t, dur / 2, { x: mx, y: h, flip: c.flip + turns * PI });
    const tgt = { x: toX, y: 0, flip: c.flip + turns * 2 * PI };
    if (toYaw !== null) tgt.yaw = toYaw;
    f.move(t + dur / 2, dur / 2, tgt);
    if (endPose) f.pose(t + dur - 0.12 * ts, 0.3 * ts, endPose);
    return t + dur;
  }

  /**
   * Troca de golpes gerada com semente entre L (esquerda) e R (direita), de t0 a t1.
   * ts > 1 deixa tudo mais lento (cena em camera lenta).
   */
  function autoFight(L, R, cx, t0, t1, seed, { ts = 1, slow = 1 } = {}) {
    const rr = rng(seed);
    let t = t0, turn = 0, n = 0;
    const kinds = ['strike', 'slash', 'thrust'];
    const parries = { strike: 'parryHigh', slash: 'parryLow', thrust: 'parryHigh' };
    const clampX = (x) => Math.max(cx - 3.0, Math.min(cx + 3.0, x));
    const sync = (f, tt, dur) => {
      const c = cur(f);
      f.move(tt, dur, { x: c.x });
    };
    while (t < t1 - 2.4 * ts) {
      const attLeft = turn % 2 === 0;
      const A = attLeft ? L : R, D = attLeft ? R : L;
      const dir = attLeft ? 1 : -1;
      const kind = kinds[Math.floor(rr() * 3)];
      const xa = cur(A).x, xd = cur(D).x;
      const gap = Math.abs(xd - xa);
      const step = Math.max(0, gap - 2.5);
      // aproximacao e preparacao
      A.pose(t, 0.45 * ts, 'windup').move(t, 0.45 * ts, { x: clampX(xa + dir * step) });
      D.pose(t + 0.15 * ts, 0.4 * ts, parries[kind]);
      A.pose(t + 0.45 * ts, 0.17 * ts, kind).move(t + 0.45 * ts, 0.2 * ts, { x: clampX(cur(A).x + dir * 0.25) });
      clash(t + 0.63 * ts, A, D, 1 + rr() * 0.3, slow);
      // recuo
      A.pose(t + 0.7 * ts, 0.4 * ts, 'guard').move(t + 0.7 * ts, 0.5 * ts, { x: clampX(cur(A).x - dir * 0.7) });
      D.pose(t + 0.75 * ts, 0.4 * ts, 'guard').move(t + 0.75 * ts, 0.5 * ts, { x: clampX(cur(D).x + dir * 0.35) });
      t += 1.45 * ts + rr() * 0.35 * ts;
      turn++;
      n++;
      if (n % 3 === 0 && t < t1 - 3.4 * ts) {
        // mortal para tras do defensor, atacante persegue
        const back = clampX(cur(D).x + dir * 2.0);
        const tEnd = leap(D, t + 0.3 * ts, back, { h: 1.3, turns: dir > 0 ? 1 : -1, dur: 0.85, ts });
        D.pose(tEnd, 0.3 * ts, 'guard');
        land(tEnd, D, slow);
        A.pose(t, 0.4 * ts, 'guard').move(t + 0.2 * ts, 0.9 * ts, { x: clampX(back - dir * 2.5) });
        t = tEnd + 0.3 * ts;
        turn++;
      }
    }
    // assentar no fim
    [L, R].forEach((f) => f.pose(t, 0.4 * ts, 'guard'));
    return t;
  }

  // ====================================================== DUELO A: Obi-Wan x Vader
  // 0-3: sabres acendem
  obi.saber(1.1, 0.35, true);
  vader.saber(1.5, 0.35, true);
  // 3.0-7.3: primeira troca
  vader.pose(3.0, 0.5, 'windup').move(3.0, 0.5, { x: -5.1 });
  vader.pose(3.5, 0.18, 'strike').move(3.5, 0.2, { x: -5.4 });
  obi.pose(3.0, 0.5, 'parryHigh').move(3.2, 0.4, { x: -7.1 });
  clash(3.62, vader, obi, 1.1);
  obi.move(3.7, 0.5, { x: -7.5 }).pose(3.7, 0.4, 'guard');
  vader.pose(3.8, 0.4, 'guard').move(3.8, 0.5, { x: -5.9 });
  obi.pose(4.3, 0.4, 'windup').move(4.3, 0.5, { x: -6.9 });
  obi.pose(4.75, 0.17, 'slash').move(4.75, 0.2, { x: -6.5 });
  vader.pose(4.3, 0.4, 'parryLow');
  clash(4.9, obi, vader, 1.0);
  vader.pose(4.95, 0.35, 'guard');
  obi.pose(5.1, 0.4, 'guard').move(5.1, 0.4, { x: -7.0 });
  vader.pose(5.6, 0.3, 'thrust').move(5.6, 0.4, { x: -5.7 });
  obi.pose(5.6, 0.3, 'thrust').move(5.6, 0.4, { x: -6.6 });
  clash(5.95, vader, obi, 1.2);
  vader.pose(6.2, 0.5, 'guard').move(6.4, 0.9, { x: -6.1 });
  const tl1 = leap(obi, 6.8, -8.6, { h: 1.3, turns: -1, dur: 0.8 });
  land(tl1, obi);
  // 7.5-29.5: troca automatica (camera foca no duelo B)
  autoFight(obi, vader, -6, 7.5, 29.5, 101);

  // 30-39: Vader usa a Forca; Obi-Wan e arremessado
  const vA = cur(vader), oA = cur(obi);
  vader.pose(30.4, 0.5, 'force').move(30.4, 0.5, { x: vA.x + 0.4 });
  fx.add({ t: 30.95, kind: 'push', pos: handPos(vader, 30.95, 'L'), slow: 0.8 });
  obi.pose(30.4, 0.4, 'parryHigh');
  obi.pose(31.0, 0.3, 'thrown');
  const fbO = cur(obi).flip;
  obi.move(31.0, 0.5, { x: oA.x - 1.8, y: 1.6, flip: fbO - 1.3 * PI });
  obi.move(31.5, 0.6, { x: oA.x - 3.0, y: 0.15, flip: fbO - 2 * PI });
  land(32.1, obi, 0.7);
  obi.pose(32.1, 0.6, 'crouch').move(32.1, 0.6, { y: 0 });
  obi.pose(32.9, 0.6, 'guard').move(32.9, 0.8, { x: oA.x - 2.0 });
  vader.pose(31.6, 0.5, 'guard').move(31.6, 1.6, { x: vA.x - 0.8 });
  // retomada, Vader pressiona
  vader.pose(34.0, 0.45, 'windup').move(34.0, 0.45, { x: cur(vader).x + 0.6 });
  vader.pose(34.45, 0.17, 'strike');
  obi.pose(34.1, 0.4, 'parryHigh');
  clash(34.68, vader, obi, 1.3, 0.7);
  vader.pose(34.8, 0.4, 'guard').move(34.8, 0.5, { x: cur(vader).x - 0.6 });
  obi.pose(34.9, 0.4, 'guard').move(34.9, 0.5, { x: cur(obi).x - 0.4 });
  // 36-55.5: automatico
  autoFight(obi, vader, -6, 36.0, 55.5, 202);

  // 56-69: Obi-Wan salta por cima do Vader e os lados se invertem
  {
    const vx = cur(vader).x, ox = cur(obi).x;
    const landX = vx + 2.4;
    const tEnd = leap(obi, 57.4, landX, { h: 2.1, turns: 1, dur: 1.5, toYaw: cur(obi).yaw + PI, ts: 1.2 });
    land(tEnd, obi, 0.8);
    vader.pose(57.4, 0.4, 'parryHigh');
    vader.move(58.6, 0.5, { yaw: cur(vader).yaw + PI });
    vader.pose(58.8, 0.5, 'guard');
    // troca no novo lado: Obi a direita (virado para -X), Vader a esquerda (virado para +X)
    vader.move(59.4, 0.5, { x: Math.max(-7.5, vx - 0.6) });
    clash(61.0, vader, obi, 1.1);
  }
  // 62-67: Vader ataca com mortal para frente
  {
    const ox = cur(obi).x;
    vader.pose(61.1, 0.5, 'guard');
    obi.pose(61.1, 0.5, 'guard');
    const tEnd = leap(vader, 63.0, ox - 2.6, { h: 1.7, turns: 1, dur: 1.0, endPose: null });
    vader.pose(tEnd - 0.1, 0.15, 'strike');
    obi.pose(63.3, 0.5, 'parryHigh');
    clash(tEnd + 0.05, vader, obi, 1.5, 0.6);
    land(tEnd, vader);
    vader.pose(tEnd + 0.2, 0.4, 'guard').move(tEnd + 0.2, 0.7, { x: cur(vader).x - 0.9 });
    obi.pose(tEnd + 0.3, 0.4, 'guard').move(tEnd + 0.3, 0.7, { x: cur(obi).x + 0.5 });
  }
  // 68-89.5: automatico (lados trocados: Vader a esquerda, Obi a direita)
  autoFight(vader, obi, -6, 68.0, 89.5, 303);

  // 90-105: final em camera lenta
  autoFight(vader, obi, -6, 90.0, 106.0, 404, { ts: 1.55, slow: 0.55 });
  // 106-120: afastam-se e apagam os sabres
  vader.pose(106.4, 0.8, 'guard').move(106.4, 1.5, { x: cur(vader).x - 0.8 });
  obi.pose(106.4, 0.8, 'guard').move(106.4, 1.5, { x: cur(obi).x + 0.8 });
  obi.saber(112.5, 0.5, false);
  vader.saber(113.2, 0.5, false);
  obi.pose(113.0, 1.2, 'guard');
  vader.pose(113.0, 1.2, 'guard');

  // ====================================================== DUELO B: Yoda x Imperador
  yoda.saber(1.3, 0.35, true);
  emp.saber(1.7, 0.35, true);
  autoFight(yoda, emp, 6, 4.0, 9.0, 505);
  // 9.4-16: Yoda salta com mortal; o Imperador gira por cima; raio da Forca
  yoda.pose(9.4, 0.3, 'guard');
  emp.pose(9.4, 0.3, 'guard');
  {
    const tEnd = leap(yoda, 9.9, 6.0, { h: 1.3, turns: 1, dur: 0.65, endPose: null });
    yoda.pose(tEnd - 0.2, 0.15, 'strike');
    emp.pose(10.0, 0.3, 'parryHigh').move(10.2, 0.35, { x: cur(emp).x + 0.4 });
    clash(10.5, yoda, emp, 1.3);
    land(tEnd, yoda);
    emp.pose(10.9, 0.4, 'guard').move(10.9, 0.5, { x: 7.3 });
    yoda.pose(10.9, 0.4, 'guard').move(10.9, 0.5, { x: 5.6 });
  }
  {
    const t2 = leap(emp, 11.9, 4.2, { h: 2.0, turns: -1, dur: 1.0, toYaw: cur(emp).yaw + PI });
    land(t2, emp);
    yoda.pose(11.5, 0.4, 'parryLow').move(12.2, 0.6, { yaw: cur(yoda).yaw + PI });
    // raio da Forca
    emp.saber(13.2, 0.2, false);
    emp.pose(13.2, 0.4, 'zap');
    yoda.pose(13.3, 0.4, 'parryHigh').move(13.3, 0.4, { x: 6.1 });
    fx.add({
      t: 13.6, t1: 15.7, kind: 'bolt',
      from: () => handPos(emp, 14.0, 'L').clone().setX(emp.ch.position.x + 0.4 * Math.sin(emp.ch.rotation.y)),
      to: () => yoda.saberPoints().tip,
    });
    emp.saber(15.8, 0.3, true);
    emp.pose(15.8, 0.5, 'guard');
    yoda.pose(15.7, 0.5, 'guard');
  }
  // 16-29.5: automatico (Yoda a direita agora, Imperador a esquerda)
  autoFight(emp, yoda, 6, 16.4, 29.5, 606);

  // 30-44: Yoda com giro duplo e Forca do Imperador
  {
    const tEnd = leap(yoda, 31.2, cur(emp).x + 2.2, { h: 2.2, turns: 2, dur: 1.5, ts: 1.0, endPose: null });
    yoda.pose(tEnd - 0.2, 0.15, 'strike');
    emp.pose(31.5, 0.5, 'parryHigh');
    clash(tEnd + 0.1, yoda, emp, 1.5, 0.6);
    land(tEnd, yoda, 0.8);
    emp.pose(tEnd + 0.3, 0.4, 'slash');
    yoda.pose(tEnd + 0.4, 0.3, 'parryLow');
    clash(tEnd + 0.7, emp, yoda, 1.2);
    // Imperador usa a Forca
    emp.pose(35.8, 0.5, 'force');
    fx.add({ t: 36.3, kind: 'push', pos: handPos(emp, 36.3, 'L'), slow: 0.8 });
    const yx = cur(yoda).x;
    yoda.pose(36.2, 0.3, 'thrown');
    const fbY = cur(yoda).flip;
    yoda.move(36.3, 0.5, { x: yx + 2.2, y: 1.4, flip: fbY + 1.2 * PI });
    yoda.move(36.8, 0.6, { x: yx + 3.0, y: 0, flip: fbY + 2 * PI });
    land(37.4, yoda, 0.7);
    yoda.pose(37.4, 0.6, 'crouch');
    yoda.pose(38.2, 0.5, 'guard');
    emp.pose(36.9, 0.5, 'guard');
  }
  autoFight(emp, yoda, 6, 39.0, 59.0, 707);

  // 60-76: Imperador salta girando por cima do Yoda; Yoda devolve com mortal
  {
    const yx = cur(yoda).x, ex = cur(emp).x;
    const t1 = leap(emp, 60.6, yx + 2.4, { h: 2.0, turns: -2, dur: 1.3, toYaw: cur(emp).yaw + PI });
    land(t1, emp, 0.8);
    yoda.pose(60.6, 0.4, 'parryHigh').move(61.6, 0.5, { yaw: cur(yoda).yaw + PI });
    yoda.pose(62.1, 0.5, 'guard');
    emp.pose(62.2, 0.5, 'guard');
    emp.pose(63.2, 0.45, 'windup');
    emp.pose(63.65, 0.17, 'strike');
    yoda.pose(63.2, 0.4, 'parryHigh');
    clash(63.88, emp, yoda, 1.3);
    emp.pose(64.0, 0.4, 'guard');
    yoda.pose(64.1, 0.4, 'guard');
    const t2 = leap(yoda, 65.6, cur(emp).x + 2.0, { h: 2.0, turns: 1, dur: 1.2, toYaw: cur(yoda).yaw + PI });
    land(t2, yoda, 0.8);
    emp.pose(65.8, 0.4, 'parryLow').move(66.8, 0.5, { yaw: cur(emp).yaw + PI });
    yoda.pose(t2 + 0.1, 0.4, 'guard');
    emp.pose(67.4, 0.4, 'guard');
  }
  autoFight(yoda, emp, 6, 68.0, 89.5, 808);

  // 90-105: final em camera lenta com raio grande
  {
    const t = autoFight(yoda, emp, 6, 90.0, 97.0, 909, { ts: 1.5, slow: 0.55 });
    emp.saber(97.2, 0.2, false);
    emp.pose(97.2, 0.4, 'zap');
    yoda.pose(97.3, 0.4, 'parryHigh');
    fx.add({
      t: 97.7, t1: 101.2, kind: 'bolt',
      from: () => handPos(emp, 99.0, 'L'),
      to: () => yoda.saberPoints().tip,
    });
    emp.saber(101.4, 0.3, true);
    emp.pose(101.4, 0.5, 'guard');
    yoda.pose(101.4, 0.5, 'guard');
    autoFight(yoda, emp, 6, 102.0, 107.0, 1010, { ts: 1.4, slow: 0.6 });
  }
  yoda.pose(107.2, 0.8, 'guard').move(107.2, 1.5, { x: cur(yoda).x - 0.8 });
  emp.pose(107.2, 0.8, 'guard').move(107.2, 1.5, { x: cur(emp).x + 0.8 });
  yoda.saber(112.8, 0.5, false);
  emp.saber(113.4, 0.5, false);
  yoda.pose(113.0, 1.2, 'guard');
  emp.pose(113.0, 1.2, 'guard');

  const trails = new Trails(scene, all);
  const dir = new Director(null);

  // ====================================================== CAMERA
  const hp = (f) => f.ch.userData.head.getWorldPosition(new THREE.Vector3());
  const orbit = (cx, t0, t1, r0, r1, h0, h1, a0, a1, fov0, fov1, ly = 1.25) =>
    dir.shot(t0, t1, (u) => {
      const a = a0 + (a1 - a0) * u, r = r0 + (r1 - r0) * u;
      return { pos: [cx + Math.sin(a) * r, h0 + (h1 - h0) * u, Math.cos(a) * r], look: [cx, ly, 0], fov: fov0 + (fov1 - fov0) * u };
    });
  const face = (f, t0, t1, dist, side, h = 0.05, fov = 24) =>
    dir.shot(t0, t1, (u) => {
      const p = hp(f);
      return { pos: [p.x + side * dist * 0.55, p.y + h, p.z + dist], look: [p.x, p.y - 0.05, p.z], fov };
    });
  const follow = (f, t0, t1, off, lookY = 1.2, fov = 30) =>
    dir.shot(t0, t1, () => {
      const p = f.ch.position;
      return { pos: [p.x + off[0], off[1], off[2]], look: [p.x, lookY + p.y * 0.6, 0], fov };
    });
  const between = (a, b, t0, t1, off, fov = 30, lookY = 1.3) =>
    dir.shot(t0, t1, (u) => {
      const pa = a.ch.position, pb = b.ch.position;
      const mx = (pa.x + pb.x) / 2;
      return { pos: [mx + off[0] + off[3] * u, off[1], off[2] - off[4] * u], look: [mx, lookY, 0], fov };
    });

  dir.shot(0, 3.0, (u) => ({ pos: [3 * u, 11 - 7.3 * u, 28 - 9 * u], look: [0, 1.3, 0], fov: 34 - 4 * u }));
  orbit(-6, 3.0, 5.4, 8.2, 5.6, 1.55, 1.45, -0.2, 0.15, 30, 27);
  between(obi, vader, 5.4, 7.0, [-1.6, 0.55, 4.2, 3.4, 0.6], 32, 1.3);
  orbit(-6, 7.0, 9.2, 6.4, 6.0, 2.4, 1.2, 0.5, 0.0, 34, 30);
  orbit(6, 9.2, 11.4, 6.3, 4.6, 1.35, 1.35, -0.1, 0.18, 28, 28, 1.0);
  orbit(6, 11.4, 13.2, 9.5, 5.8, 3.0, 1.6, 0.35, -0.2, 32, 32);
  dir.shot(13.2, 16.0, (u) => ({ pos: [7.8 - 1.6 * u, 1.1, 4.2 + 0.6 * u], look: [5.6, 1.35 + 0.2 * u, 0], fov: 30 - 3 * u }));
  dir.shot(16.0, 20.0, (u) => ({ pos: [-14 + 28 * u, 3.4, 20 - 3 * u], look: [0, 1.2, 0], fov: 38 }));
  face(vader, 20.0, 23.0, 1.7, -1, 0.1, 24);
  face(yoda, 23.0, 26.0, 1.4, 1, 0.0, 26);
  orbit(0, 26.0, 30.0, 17, 14, 0.6, 1.4, 0.55, -0.35, 40, 36, 1.4);
  between(vader, obi, 30.0, 32.2, [0.0, 1.7, 5.0, 0, 0], 28, 1.4);
  orbit(-6, 32.2, 34.0, 6.8, 5.6, 0.9, 1.5, 0.4, -0.7, 34, 30, 1.0);
  dir.shot(34.0, 36.0, (u) => ({ pos: [-6 + 0.4 * u, 9.5 - 2.5 * u, 3.5], look: [-6, 0.4, 0], fov: 34 }));
  follow(yoda, 36.0, 38.4, [-3.2, 1.5, 6.2], 1.2, 30);
  between(emp, yoda, 38.4, 42.0, [0, 1.2, 6.2, 0, 1.0], 28, 1.2);
  orbit(6, 42.0, 45.5, 8.5, 7.0, 1.6, 2.3, 0.1, 0.6, 32, 34);
  dir.shot(45.5, 50.0, (u) => ({ pos: [0, 5.5 - 3.6 * u, 25 - 6 * u], look: [0, 1.4, 0], fov: 36 }));
  face(obi, 50.0, 51.6, 1.6, -1, 0.05, 24);
  face(vader, 51.6, 53.2, 1.6, 1, 0.1, 24);
  face(yoda, 53.2, 54.8, 1.3, -1, 0.0, 26);
  face(emp, 54.8, 56.2, 1.5, 1, 0.05, 24);
  follow(obi, 56.2, 59.0, [3.0, 1.4, 6.6], 1.4, 30);
  orbit(-6, 59.0, 61.0, 5.8, 6.6, 1.3, 1.7, -0.5, 0.2, 30, 30);
  follow(emp, 61.0, 63.6, [-3.4, 1.5, 6.8], 1.4, 30);
  orbit(-6, 63.6, 66.8, 7.0, 4.6, 1.4, 1.2, 0.4, -0.1, 32, 26);
  orbit(6, 66.8, 70.0, 8.0, 6.4, 1.6, 1.9, 0.2, -0.5, 30, 30);
  dir.shot(70.0, 78.0, (u) => {
    const a = -0.9 + 1.8 * u;
    return { pos: [Math.sin(a) * 19, 2.6 + 1.2 * Math.sin(u * PI), Math.cos(a) * 19], look: [0, 1.2, 0], fov: 38 };
  });
  between(vader, obi, 78.0, 84.0, [0, 1.3, 6.4, 0, 0.4], 28, 1.3);
  between(emp, yoda, 84.0, 90.0, [0, 1.3, 6.4, 0, 0.4], 28, 1.2);
  orbit(-6, 90.0, 95.0, 5.2, 4.2, 1.1, 1.0, -0.7, 0.7, 30, 24);
  orbit(6, 95.0, 97.8, 6.2, 5.0, 1.2, 1.4, 0.5, 0.0, 30, 28, 1.3);
  face(yoda, 97.8, 100.2, 1.5, 1, 0.0, 28);
  dir.shot(100.2, 104.5, (u) => ({ pos: [4.5 + 3.5 * u, 1.0 + 0.5 * u, 5.2 - 0.6 * u], look: [5.6, 1.4, 0], fov: 28 }));
  dir.shot(104.5, 109.0, (u) => ({ pos: [0, 2.2 + 1.0 * u, 20 - 2 * u], look: [0, 1.3, 0], fov: 36 }));
  dir.shot(109.0, DURATION, (u) => ({ pos: [0, 3.2 + 9.0 * u, 18 + 10 * u], look: [0, 1.0, 0], fov: 36 - 3 * u }));

  return { fighters: all, fx, trails, dir, duration: DURATION };
}
