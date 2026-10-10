'use strict';
/* When-hardening-helps viewers: canvas rendering of packing replays.
   A replay frame holds {ph, s, g, u, L, p} with p = flat [x0,y0,t0, ...].
   A piece is drawn from pieces.json: `parts` = convex polygons about the
   centroid; the morph is core scale s = g*(1-u) plus rounding radius g*u*rho,
   approximated by stroking the core path. Orange = soft (u > 0.02), blue = hard.
   Vanilla JS, no dependencies. */
const WHH = (() => {
  const SOFT = '#e8912d', HARD = '#2d6fe8';

  async function loadJSON(url) {
    const r = await fetch(url);
    if (!r.ok) throw new Error('fetch failed: ' + url);
    return r.json();
  }

  // ---------- geometry ----------
  // World-space vertices of one part under pose (x, y, theta) and core scale s.
  function partWorld(part, x, y, c, d, s) {
    const out = new Array(part.length);
    for (let i = 0; i < part.length; i += 2) {
      const vx = part[i] * s, vy = part[i + 1] * s;
      out[i] = x + vx * c - vy * d;
      out[i + 1] = y + vx * d + vy * c;
    }
    return out;
  }

  // Container outline in world coords (centred at origin), for size L.
  function containerPath(container, L) {
    if (container === 'circle') return { kind: 'circle', r: L };
    if (container === 'triangle') {
      const rc = L / Math.sqrt(3); // centroid -> vertex
      const pts = [];
      for (const a of [Math.PI / 2, Math.PI / 2 + 2 * Math.PI / 3, Math.PI / 2 + 4 * Math.PI / 3])
        pts.push([rc * Math.cos(a), rc * Math.sin(a)]);
      return { kind: 'poly', pts };
    }
    const h = L / 2; // square
    return { kind: 'poly', pts: [[-h, -h], [h, -h], [h, h], [-h, h]] };
  }

  // Half-extent of the container, for fitting the view.
  function containerExtent(container, L) {
    if (container === 'circle') return L;
    if (container === 'triangle') return L / Math.sqrt(3);
    return L / Math.SQRT2;
  }

  // ---------- renderer ----------
  function makeRenderer(canvas, piece, container) {
    const ctx = canvas.getContext('2d');
    let replay = null, frameIdx = 0;
    const cont = () => container;

    function resize() {
      const dpr = window.devicePixelRatio || 1;
      const w = canvas.clientWidth, h = canvas.clientHeight;
      const W = Math.max(1, Math.round(w * dpr)), H = Math.max(1, Math.round(h * dpr));
      if (canvas.width !== W || canvas.height !== H) { canvas.width = W; canvas.height = H; }
    }

    function draw() {
      resize();
      const W = canvas.width, H = canvas.height;
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, W, H);
      if (!replay) return;
      const f = replay.frames[frameIdx];
      const ext = containerExtent(cont(), f.L) || 1;
      const sc = Math.min(W, H) / 2 * 0.92 / ext; // px per world unit
      const cx = W / 2, cy = H / 2;
      const X = wx => cx + wx * sc, Y = wy => cy - wy * sc; // y-up

      // container
      const cp = containerPath(cont(), f.L);
      ctx.beginPath();
      if (cp.kind === 'circle') ctx.arc(cx, cy, cp.r * sc, 0, 2 * Math.PI);
      else { cp.pts.forEach(([px, py], i) => i ? ctx.lineTo(X(px), Y(py)) : ctx.moveTo(X(px), Y(py))); ctx.closePath(); }
      ctx.strokeStyle = 'rgba(0,0,0,0.35)'; ctx.lineWidth = Math.max(1, W / 300); ctx.stroke();

      // pieces
      const s = f.g * (1 - f.u), rw = f.g * f.u * (piece.rho || 0);
      const col = f.u > 0.02 ? SOFT : HARD;
      const n = f.p.length / 3;
      ctx.lineJoin = 'round';
      for (let i = 0; i < n; i++) {
        const x = f.p[3 * i], y = f.p[3 * i + 1], t = f.p[3 * i + 2];
        const c = Math.cos(t), d = Math.sin(t);
        if (!piece.parts || !piece.parts.length) { // disk piece
          ctx.beginPath(); ctx.arc(X(x), Y(y), Math.max(0.5, f.g * (piece.rho || 0.5) * sc), 0, 2 * Math.PI);
          ctx.fillStyle = col; ctx.globalAlpha = 0.8; ctx.fill(); ctx.globalAlpha = 1;
          continue;
        }
        for (const part of piece.parts) {
          const wv = partWorld(part, x, y, c, d, s);
          ctx.beginPath();
          for (let k = 0; k < wv.length; k += 2) k ? ctx.lineTo(X(wv[k]), Y(wv[k + 1])) : ctx.moveTo(X(wv[k]), Y(wv[k + 1]));
          ctx.closePath();
          ctx.strokeStyle = col; ctx.lineWidth = Math.max(0.5, 2 * rw * sc); ctx.stroke();
          ctx.fillStyle = col; ctx.globalAlpha = 0.8; ctx.fill(); ctx.globalAlpha = 1;
        }
      }
      // softness readout
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.fillStyle = 'rgba(0,0,0,0.55)';
      ctx.font = `${Math.max(10, W / 28)}px system-ui, sans-serif`;
      ctx.fillText(f.u > 0.02 ? 'soft' : 'hard', 8, 14 * (W / 200) + 4);
    }

    return {
      setReplay(r) { replay = r; frameIdx = 0; draw(); },
      get nFrames() { return replay ? replay.frames.length : 0; },
      get frame() { return frameIdx; },
      set frame(i) { if (replay) frameIdx = Math.max(0, Math.min(replay.frames.length - 1, i | 0)); draw(); },
      frameData() { return replay ? replay.frames[frameIdx] : null; },
      draw, resize,
    };
  }

  // ---------- synchronized replay wall ----------
  // tiles: [{file, caption, sub, href}]; all tiles share one clock.
  function wall(el, tiles, pieces, opts) {
    opts = opts || {};
    const seconds = opts.seconds || 12;
    const state = { playing: false, t: 0, raf: 0, last: 0 };
    const items = [];

    for (const t of tiles) {
      const div = document.createElement('div');
      div.className = 'tile';
      div.innerHTML = `<a class="tilelink" href="${t.href}"><canvas></canvas></a>
        <div class="tilecap"><b>${t.caption}</b><span>${t.sub}</span></div>
        <div class="tileload">loading…</div>`;
      el.appendChild(div);
      const canvas = div.querySelector('canvas');
      const item = { tile: t, div, canvas, rend: null, loaded: false, fps: 12 };
      items.push(item);
    }

    const io = new IntersectionObserver(entries => {
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        const item = items.find(i => i.div === e.target);
        io.unobserve(e.target);
        if (!item || item.loaded) continue;
        item.loaded = true; // fetch once
        loadJSON(item.tile.file).then(rep => {
          const piece = pieces[rep.piece];
          if (!piece) throw new Error('unknown piece ' + rep.piece);
          item.rend = makeRenderer(item.canvas, piece, rep.container);
          item.rend.setReplay(rep);
          item.fps = rep.frames.length / seconds;
          item.div.querySelector('.tileload').remove();
          item.div.classList.add('ready');
        }).catch(err => {
          const l = item.div.querySelector('.tileload');
          if (l) l.textContent = 'replay unavailable';
        });
      }
    }, { rootMargin: '400px' });
    items.forEach(i => io.observe(i.div));

    function tick(now) {
      if (!state.playing) return;
      const dt = (now - state.last) / 1000; state.last = now;
      state.t += dt;
      let done = true;
      for (const item of items) {
        if (!item.rend) { done = false; continue; }
        const fi = Math.min(item.rend.nFrames - 1, Math.floor(state.t * item.fps));
        item.rend.frame = fi;
        if (fi < item.rend.nFrames - 1) done = false;
      }
      if (done) { pause(); return; }
      state.raf = requestAnimationFrame(tick);
    }
    function play() { state.t = 0; state.last = performance.now(); state.playing = true; state.raf = requestAnimationFrame(tick); }
    function pause() { state.playing = false; cancelAnimationFrame(state.raf); }
    function toggle() { if (state.playing) { pause(); return false; } play(); return true; }

    return { play, pause, toggle, get paused() { return !state.playing; } };
  }

  // ---------- single replay viewer (families page) ----------
  function viewer(el, pieces) {
    el.innerHTML = `<div class="viewer">
      <canvas class="vcanvas"></canvas>
      <div class="vcontrols">
        <button class="vplay">Play</button>
        <input class="vscrub" type="range" min="0" max="100" value="0" step="1">
        <span class="vinfo mono"></span>
      </div></div>`;
    const canvas = el.querySelector('.vcanvas');
    const btn = el.querySelector('.vplay'), scrub = el.querySelector('.vscrub'), info = el.querySelector('.vinfo');
    let rend = null, raf = 0, last = 0, fps = 12;

    function showInfo() {
      const f = rend.frameData();
      if (!f) { info.textContent = ''; return; }
      info.textContent = `${f.ph} · step ${f.s} · L ${(+f.L).toFixed(4)} · γ ${(+f.g).toFixed(2)} τ ${(+f.u).toFixed(2)} · frame ${rend.frame + 1}/${rend.nFrames}`;
      scrub.value = Math.round(100 * rend.frame / Math.max(1, rend.nFrames - 1));
    }
    function stop() { cancelAnimationFrame(raf); raf = 0; btn.textContent = 'Play'; }
    function stepFn(now) {
      const dt = (now - last) / 1000; last = now;
      let fi = rend.frame + dt * fps;
      if (fi >= rend.nFrames - 1) { rend.frame = rend.nFrames - 1; showInfo(); stop(); return; }
      rend.frame = fi; showInfo();
      raf = requestAnimationFrame(stepFn);
    }
    btn.onclick = () => {
      if (!rend) return;
      if (raf) { stop(); return; }
      if (rend.frame >= rend.nFrames - 1) rend.frame = 0;
      btn.textContent = 'Pause'; last = performance.now();
      raf = requestAnimationFrame(stepFn);
    };
    scrub.oninput = () => { if (!rend) return; stop(); rend.frame = Math.round(scrub.value / 100 * (rend.nFrames - 1)); showInfo(); };
    new ResizeObserver(() => { if (rend) rend.draw(); }).observe(canvas);

    return {
      async load(file, seconds) {
        stop();
        const rep = await loadJSON(file);
        const piece = pieces[rep.piece];
        if (!piece) throw new Error('unknown piece ' + rep.piece);
        rend = makeRenderer(canvas, piece, rep.container);
        rend.setReplay(rep);
        fps = rep.frames.length / (seconds || 12);
        btn.textContent = 'Play'; showInfo();
      },
      get ready() { return !!rend; },
    };
  }

  return { loadJSON, makeRenderer, wall, viewer, SOFT, HARD };
})();
