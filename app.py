"""A fixed, top-to-bottom visual story about warehouse labor standards."""

import streamlit as st


st.set_page_config(
    page_title="From PPH to a Digital Twin",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


_LEGACY_WAREHOUSE_ANIMATION = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    html, body { margin: 0; background: #0C1C31; overflow: hidden; }
    .stage {
      position: relative;
      height: 510px;
      border-radius: 22px;
      overflow: hidden;
      background: radial-gradient(circle at 50% 25%, #23486E 0%, #10233E 50%, #081523 100%);
      box-shadow: 0 22px 48px rgba(23, 40, 70, 0.22);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    canvas { width: 100%; height: 100%; display: block; }
    .badge {
      position: absolute; top: 18px; left: 20px;
      color: #C9DDFF; background: rgba(8, 25, 44, 0.68);
      border: 1px solid rgba(148, 190, 255, 0.28);
      border-radius: 999px; padding: 8px 12px;
      font-size: 10px; font-weight: 800; letter-spacing: 0.11em; text-transform: uppercase;
    }
    .live {
      position: absolute; top: 24px; right: 22px; color: #B9D6CA;
      font-size: 10px; font-weight: 750; letter-spacing: 0.08em; text-transform: uppercase;
    }
    .live::before {
      content: ""; display: inline-block; width: 7px; height: 7px; border-radius: 50%;
      margin-right: 7px; background: #46D6A6; box-shadow: 0 0 0 4px rgba(70,214,166,.14);
      animation: pulse 1.8s ease-in-out infinite;
    }
    .caption {
      position: absolute; left: 20px; bottom: 18px; max-width: 285px; color: #DCE9F8;
      font-size: 12px; line-height: 1.45; text-shadow: 0 1px 6px rgba(0,0,0,.35);
    }
    .caption b { color: #FFFFFF; }
    @keyframes pulse { 50% { transform: scale(.75); opacity: .55; } }
  </style>
</head>
<body>
  <div class="stage">
    <canvas id="warehouse"></canvas>
    <div class="badge">Illustrative digital twin</div>
    <div class="live">Active flow</div>
    <div class="caption"><b>Work is moving.</b><br>Without task-level standards, the labor behind each movement remains invisible.</div>
  </div>
  <script>
    const canvas = document.getElementById("warehouse");
    const ctx = canvas.getContext("2d");
    let W = 0, H = 0, dpr = 1;

    function resize() {
      const rect = canvas.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = rect.width; H = rect.height;
      canvas.width = W * dpr; canvas.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    window.addEventListener("resize", resize);
    resize();

    function iso(x, y, z = 0) {
      const sx = Math.min(W * 0.0072, 6.0);
      const sy = sx * 0.47;
      return { x: W * 0.51 + (x - y) * sx, y: H * 0.21 + (x + y) * sy - z * sy * 1.62 };
    }
    function line(a, b, color, width = 1, dash = []) {
      ctx.save(); ctx.strokeStyle = color; ctx.lineWidth = width; ctx.setLineDash(dash);
      ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); ctx.restore();
    }
    function polygon(points, fill, stroke = null) {
      ctx.beginPath(); ctx.moveTo(points[0].x, points[0].y);
      for (let i = 1; i < points.length; i++) ctx.lineTo(points[i].x, points[i].y);
      ctx.closePath();
      if (fill) { ctx.fillStyle = fill; ctx.fill(); }
      if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = 1; ctx.stroke(); }
    }
    function rack(x, y, w, h, height, color) {
      const base = [iso(x,y), iso(x+w,y), iso(x+w,y+h), iso(x,y+h)];
      const top = [iso(x,y,height), iso(x+w,y,height), iso(x+w,y+h,height), iso(x,y+h,height)];
      polygon([base[1], base[2], top[2], top[1]], "#284866");
      polygon([base[2], base[3], top[3], top[2]], "#1D3853");
      polygon(top, color, "rgba(213,231,249,.25)");
      for (let u = 0.18; u < 1; u += 0.18) {
        line(iso(x + w * u, y, height + .1), iso(x + w * u, y + h, height + .1), "rgba(233,243,252,.16)");
      }
    }
    function tabletop(x, y, w, h) {
      const p = [iso(x,y,2.2), iso(x+w,y,2.2), iso(x+w,y+h,2.2), iso(x,y+h,2.2)];
      polygon(p, "#8E663E", "rgba(255,224,180,.28)");
      for (const c of [iso(x+.5,y+.5), iso(x+w-.5,y+.5), iso(x+w-.5,y+h-.5), iso(x+.5,y+h-.5)]) {
        line(c, {x:c.x, y:c.y + 17}, "#31506D", 2);
      }
    }
    function conveyor(points) {
      for (let i = 1; i < points.length; i++) {
        const a = iso(points[i-1][0], points[i-1][1], 1.6);
        const b = iso(points[i][0], points[i][1], 1.6);
        line(a, b, "#527A9E", 12);
        line(a, b, "#A9C4DA", 3);
      }
    }
    function pointOnPath(points, t) {
      const segments = [];
      let total = 0;
      for (let i = 1; i < points.length; i++) {
        const dx = points[i][0] - points[i-1][0], dy = points[i][1] - points[i-1][1];
        const len = Math.hypot(dx, dy); segments.push(len); total += len;
      }
      let target = (t % 1) * total;
      for (let i = 0; i < segments.length; i++) {
        if (target <= segments[i]) {
          const f = target / segments[i];
          return [points[i][0] + (points[i+1][0]-points[i][0])*f, points[i][1] + (points[i+1][1]-points[i][1])*f];
        }
        target -= segments[i];
      }
      return points[points.length - 1];
    }
    function pallet(x, y, color = "#D8914B") {
      const a = iso(x,y,1.5), b = iso(x+3,y,1.5), c = iso(x+3,y+2,1.5), d = iso(x,y+2,1.5);
      const up = 8;
      polygon([{x:a.x,y:a.y-up},{x:b.x,y:b.y-up},{x:c.x,y:c.y-up},{x:d.x,y:d.y-up}], color, "rgba(255,230,190,.35)");
      polygon([{x:c.x,y:c.y-up},{x:d.x,y:d.y-up},d,c], "#9D5C2B");
      polygon([{x:b.x,y:b.y-up},{x:c.x,y:c.y-up},c,b], "#B86E35");
    }
    function worker(x, y, phase) {
      const p = iso(x,y,0), bob = Math.sin(phase) * 1.2;
      ctx.save();
      ctx.fillStyle = "rgba(4,14,25,.25)"; ctx.beginPath(); ctx.ellipse(p.x, p.y+7, 6, 2.4, 0, 0, Math.PI*2); ctx.fill();
      ctx.fillStyle = "#F5D1B5"; ctx.beginPath(); ctx.arc(p.x, p.y-18+bob, 4, 0, Math.PI*2); ctx.fill();
      ctx.fillStyle = "#45D7A6"; ctx.fillRect(p.x-4, p.y-14+bob, 8, 11);
      ctx.strokeStyle = "#CDE7F5"; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.moveTo(p.x-2, p.y-2+bob); ctx.lineTo(p.x-4, p.y+5); ctx.moveTo(p.x+2, p.y-2+bob); ctx.lineTo(p.x+4, p.y+5); ctx.stroke();
      ctx.restore();
    }
    function forklift(x, y, phase) {
      const p = iso(x,y,0), sway = Math.sin(phase) * 0.7;
      ctx.save();
      ctx.translate(p.x, p.y+sway);
      ctx.fillStyle = "rgba(3,13,24,.25)"; ctx.beginPath(); ctx.ellipse(0,8,13,4,0,0,Math.PI*2); ctx.fill();
      ctx.fillStyle = "#F3C84E"; ctx.fillRect(-11,-7,17,10);
      ctx.fillStyle = "#162E47"; ctx.fillRect(-1,-16,7,10); ctx.fillRect(7,-19,2,22);
      ctx.fillStyle = "#27394C"; ctx.beginPath(); ctx.arc(-7,5,4,0,Math.PI*2); ctx.arc(5,5,4,0,Math.PI*2); ctx.fill();
      ctx.strokeStyle = "#BDD2E5"; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(9,1); ctx.lineTo(18,1); ctx.moveTo(9,4); ctx.lineTo(18,4); ctx.stroke();
      ctx.restore();
    }
    function draw(time) {
      // Keep this loop active even when the browser reports a reduced-motion
      // preference. This is a short, explanatory product animation, and an
      // inactive first frame makes the digital-twin idea read as a screenshot.
      const motionTime = time * 2.75;
      ctx.clearRect(0,0,W,H);
      const gradient = ctx.createLinearGradient(0,0,0,H);
      gradient.addColorStop(0,"#1C4165"); gradient.addColorStop(.58,"#102A45"); gradient.addColorStop(1,"#0A1828");
      ctx.fillStyle = gradient; ctx.fillRect(0,0,W,H);

      const floor = [iso(0,0), iso(100,0), iso(100,60), iso(0,60)];
      polygon(floor, "#163852", "rgba(173,207,240,.32)");
      for (let x = 0; x <= 100; x += 10) line(iso(x,0), iso(x,60), "rgba(171,209,241,.11)");
      for (let y = 0; y <= 60; y += 10) line(iso(0,y), iso(100,y), "rgba(171,209,241,.11)");

      polygon([iso(6,8), iso(36,8), iso(36,29), iso(6,29)], "rgba(68,214,166,.10)");
      polygon([iso(45,5), iso(90,5), iso(90,27), iso(45,27)], "rgba(77,124,254,.10)");
      for (let x = 48; x <= 82; x += 9) rack(x, 9, 5.5, 28, 9, "#466E92");
      for (let x = 11; x <= 32; x += 7) rack(x, 36, 4.5, 17, 7, "#567C9B");
      tabletop(21,18,18,7); tabletop(43,37,18,7);
      conveyor([[9,12],[27,12],[27,22],[45,22],[45,32],[70,32]]);
      conveyor([[17,47],[35,47],[35,39],[49,39]]);

      const cartPaths = [
        [[9,12],[27,12],[27,22],[45,22],[45,32],[70,32]],
        [[17,47],[35,47],[35,39],[49,39]],
        [[10,29],[24,29],[34,34],[46,34]]
      ];
      cartPaths.forEach((path, i) => {
        const p = pointOnPath(path, motionTime*.00007 + i*.34);
        pallet(p[0],p[1], i === 1 ? "#D59A53" : "#C98142");
      });
      const forkPath = [[7,31],[23,31],[40,27],[64,20],[85,14]];
      const fp = pointOnPath(forkPath, motionTime*.00004);
      forklift(fp[0], fp[1], motionTime*.005);

      const workerPaths = [
        [[22,17],[38,17],[38,25],[22,25]],
        [[42,43],[62,43],[62,49],[42,49]],
        [[83,38],[91,38],[91,51],[83,51]]
      ];
      workerPaths.forEach((path, i) => {
        const p = pointOnPath(path, motionTime*.000026 + i*.27);
        worker(p[0],p[1], motionTime*.008+i);
      });
      ctx.save();
      ctx.fillStyle = "#A9C7E3"; ctx.font = "600 11px Inter, Arial";
      ctx.fillText("Inbound", iso(5,7).x, iso(5,7).y-14);
      ctx.fillText("Workstations", iso(28,19).x, iso(28,19).y-19);
      ctx.fillText("Storage", iso(72,10).x, iso(72,10).y-22);
      ctx.fillText("Outbound", iso(57,38).x, iso(57,38).y-20);
      ctx.restore();
      requestAnimationFrame(draw);
    }
    requestAnimationFrame(draw);
  </script>
</body>
</html>
"""

WAREHOUSE_ANIMATION = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    html, body { margin: 0; background: #091829; overflow: hidden; }
    .stage {
      position: relative;
      height: 510px;
      overflow: hidden;
      border-radius: 22px;
      background: radial-gradient(circle at 50% 20%, #254a70 0%, #102b46 48%, #081624 100%);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      box-shadow: 0 22px 48px rgba(19, 40, 68, .24);
    }
    canvas { display: block; width: 100%; height: 100%; }
    .eyebrow {
      position: absolute; top: 18px; left: 20px;
      padding: 8px 12px; border: 1px solid rgba(167, 207, 245, .23);
      border-radius: 999px; background: rgba(6, 21, 37, .68);
      color: #cce2fa; font-size: 10px; font-weight: 800;
      letter-spacing: .11em; text-transform: uppercase;
    }
    .legend {
      position: absolute; top: 21px; right: 22px; display: flex; gap: 14px;
      color: #b9d3e8; font-size: 10px; font-weight: 750; letter-spacing: .07em;
      text-transform: uppercase;
    }
    .legend span { display: flex; align-items: center; gap: 6px; }
    .legend i { width: 7px; height: 7px; display: inline-block; border-radius: 50%; }
    .legend .high { background: #63d6b7; box-shadow: 0 0 0 4px rgba(99,214,183,.14); }
    .legend .ground { background: #f1c255; box-shadow: 0 0 0 4px rgba(241,194,85,.14); }
    .caption {
      position: absolute; left: 20px; bottom: 17px; max-width: 350px;
      color: #c9dced; font-size: 12px; line-height: 1.45;
      text-shadow: 0 1px 6px rgba(0,0,0,.35);
    }
    .caption b { color: #fff; }
  </style>
</head>
<body>
  <div class="stage">
    <canvas id="warehouse-cycle"></canvas>
    <div class="eyebrow">Animated warehouse cycle</div>
    <div class="legend">
      <span><i class="high"></i>High-bay putaway</span>
      <span><i class="ground"></i>Ground-level drop</span>
    </div>
    <div class="caption"><b>One pallet count. Two very different cycles.</b><br>Equipment, elevation, travel, and handling change the labor required.</div>
  </div>
  <script>
    const canvas = document.getElementById("warehouse-cycle");
    const ctx = canvas.getContext("2d");
    const BASE_W = 960;
    const BASE_H = 510;
    let W = 0, H = 0, dpr = 1;

    function resize() {
      const box = canvas.getBoundingClientRect();
      W = Math.max(1, box.width);
      H = Math.max(1, box.height);
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(W * dpr);
      canvas.height = Math.round(H * dpr);
    }
    window.addEventListener("resize", resize);
    if (window.ResizeObserver) new ResizeObserver(resize).observe(document.body);
    resize();

    const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
    const ramp = (t, a, b) => clamp((t - a) / (b - a));
    const lerp = (a, b, t) => a + (b - a) * t;
    const smooth = (t) => {
      t = clamp(t);
      return t * t * (3 - 2 * t);
    };
    const ease = (t) => {
      t = clamp(t);
      return t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    };

    function poly(points, fill, stroke, width = 1) {
      ctx.beginPath();
      ctx.moveTo(points[0][0], points[0][1]);
      for (let i = 1; i < points.length; i++) ctx.lineTo(points[i][0], points[i][1]);
      ctx.closePath();
      if (fill) { ctx.fillStyle = fill; ctx.fill(); }
      if (stroke) { ctx.lineWidth = width; ctx.strokeStyle = stroke; ctx.stroke(); }
    }
    function line(x1, y1, x2, y2, color, width = 1, dash = []) {
      ctx.save();
      ctx.beginPath();
      ctx.setLineDash(dash);
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.lineWidth = width;
      ctx.strokeStyle = color;
      ctx.stroke();
      ctx.restore();
    }
    function rr(x, y, w, h, r, fill, stroke) {
      const q = Math.min(r, w / 2, h / 2);
      ctx.beginPath();
      ctx.moveTo(x + q, y);
      ctx.arcTo(x + w, y, x + w, y + h, q);
      ctx.arcTo(x + w, y + h, x, y + h, q);
      ctx.arcTo(x, y + h, x, y, q);
      ctx.arcTo(x, y, x + w, y, q);
      ctx.closePath();
      if (fill) { ctx.fillStyle = fill; ctx.fill(); }
      if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = 1; ctx.stroke(); }
    }
    function text(value, x, y, size, color, weight = 600, align = "left") {
      ctx.save();
      ctx.fillStyle = color;
      ctx.font = weight + " " + size + "px Inter, Arial, sans-serif";
      ctx.textAlign = align;
      ctx.fillText(value, x, y);
      ctx.restore();
    }
    function pallet(cx, bottom, width = 58, color = "#d88940", alpha = 1) {
      const h = width * .53;
      const x = cx - width / 2;
      ctx.save();
      ctx.globalAlpha = alpha;
      ctx.fillStyle = "rgba(2, 12, 23, .27)";
      ctx.beginPath();
      ctx.ellipse(cx, bottom + 5, width * .45, 5, 0, 0, Math.PI * 2);
      ctx.fill();
      rr(x, bottom - h + 4, width, h - 10, 2, color, "rgba(255,234,205,.25)");
      poly([[x, bottom - h + 4], [x + width, bottom - h + 4], [x + width - 6, bottom - h - 3], [x + 6, bottom - h - 3]], "#edb36a", "rgba(255,238,210,.35)");
      ctx.fillStyle = "rgba(95,47,24,.28)";
      ctx.fillRect(x + width * .48, bottom - h + 7, 2, h - 15);
      ctx.fillStyle = "#8a542b";
      ctx.fillRect(x - 3, bottom - 7, width + 6, 7);
      ctx.fillStyle = "#bd7a3e";
      ctx.fillRect(x + 3, bottom, width - 6, 5);
      for (let k = 0; k < 3; k++) {
        ctx.fillStyle = "#5e3925";
        ctx.fillRect(x + 7 + k * ((width - 14) / 2), bottom + 4, 6, 3);
      }
      ctx.restore();
    }
    function rack(x, y, w, h, code, target, targetFilled) {
      const levels = 3;
      const bays = 2;
      const innerX = x + 13;
      const innerY = y + 14;
      const innerW = w - 26;
      const bayW = innerW / bays;
      const levelH = 94;
      const depth = 18;

      poly([[x + 7, y], [x + w + 7, y], [x + w + depth, y - depth], [x + depth, y - depth]], "#28455e", "rgba(184,216,243,.18)");
      rr(x + 7, y, w, h, 2, "#173149", "rgba(188,219,243,.18)");
      poly([[x + w + 7, y], [x + w + 7, y + h], [x + w + depth, y + h - depth], [x + w + depth, y - depth]], "#10273d", "rgba(169,209,242,.14)");

      for (let level = 0; level < levels; level++) {
        const top = innerY + level * levelH;
        const base = top + 80;
        for (let bay = 0; bay < bays; bay++) {
          const sx = innerX + bay * bayW;
          const isTarget = target.level === level && target.bay === bay;
          rr(sx + 3, top + 3, bayW - 6, 76, 2, isTarget ? "rgba(42,120,111,.28)" : "rgba(11,33,52,.57)", isTarget ? "rgba(99,214,183,.54)" : "rgba(164,207,238,.10)");
          if (isTarget && !targetFilled) {
            line(sx + 12, top + 14, sx + bayW - 12, top + 14, "rgba(99,214,183,.54)", 1, [4, 4]);
            text(level === 0 ? "LEVEL 3" : "GROUND", sx + bayW / 2, top + 39, 9, "rgba(168,220,208,.78)", 800, "center");
          }
          const staticLoad = !isTarget && ((bay + level * 2) % 3 !== 1 || level === 2);
          if (staticLoad) {
            const pColor = level === 1 ? "#bf7b40" : (bay === 0 ? "#d5964f" : "#c57c3a");
            pallet(sx + bayW / 2, base - 7, Math.min(58, bayW * .58), pColor, .94);
          }
        }
        ctx.fillStyle = "#63829b";
        ctx.fillRect(x + 4, base, w + 6, 7);
        ctx.fillStyle = "#a5c1d5";
        ctx.fillRect(x + 8, base, w - 2, 2);
      }

      const uprights = [x + 4, x + w / 2 + 4, x + w + 4];
      uprights.forEach((ux) => {
        ctx.fillStyle = "#537c9a";
        ctx.fillRect(ux, y - 6, 8, h + 13);
        ctx.fillStyle = "#87aac2";
        ctx.fillRect(ux + 1, y - 4, 2, h + 8);
      });
      ctx.fillStyle = "#6a91ad";
      ctx.fillRect(x + 2, y - 7, w + 11, 9);
      text(code, x + 14, y - 17, 10, "#a9c8df", 800);
    }
    function reachTruck(bodyX, forkY, forkExtension) {
      const ground = 385;
      const mastX = bodyX + 100;
      ctx.save();
      ctx.fillStyle = "rgba(0,10,21,.30)";
      ctx.beginPath();
      ctx.ellipse(bodyX + 52, ground + 8, 63, 10, 0, 0, Math.PI * 2);
      ctx.fill();
      rr(bodyX + 7, ground - 42, 82, 33, 4, "#f4c848", "rgba(255,238,169,.42)");
      rr(bodyX + 30, ground - 72, 38, 31, 3, "#25445a", "rgba(206,231,244,.42)");
      rr(bodyX + 35, ground - 68, 28, 21, 2, "#9ccde1", "rgba(224,246,255,.35)");
      ctx.fillStyle = "#1d3448";
      ctx.fillRect(bodyX + 7, ground - 14, 82, 10);
      ctx.fillStyle = "#26394d";
      [bodyX + 25, bodyX + 74].forEach((wx) => {
        ctx.beginPath(); ctx.arc(wx, ground - 4, 11, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = "#99b5c8"; ctx.beginPath(); ctx.arc(wx, ground - 4, 4, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = "#26394d";
      });
      ctx.fillStyle = "#34516a";
      ctx.fillRect(mastX - 6, 99, 7, ground - 99);
      ctx.fillRect(mastX + 9, 99, 7, ground - 99);
      line(mastX - 2, 102, mastX + 14, 102, "#bdd8e8", 2);
      rr(mastX - 12, forkY - 10, 34, 18, 2, "#355972", "#bad8e8");
      line(mastX + 15, forkY + 2, mastX + 96 + forkExtension, forkY + 2, "#c3ddea", 3);
      line(mastX + 15, forkY + 7, mastX + 96 + forkExtension, forkY + 7, "#82a8c0", 2);
      ctx.fillStyle = "#61d6b7";
      ctx.fillRect(bodyX + 48, ground - 64, 7, 13);
      ctx.fillStyle = "#f0c8ab";
      ctx.beginPath(); ctx.arc(bodyX + 51, ground - 71, 4, 0, Math.PI * 2); ctx.fill();
      ctx.restore();
      return { mastX, palletX: mastX + 78 + forkExtension };
    }
    function counterbalanceTruck(mastX, forkY, forkExtension) {
      const ground = 385;
      ctx.save();
      ctx.fillStyle = "rgba(0,10,21,.30)";
      ctx.beginPath();
      ctx.ellipse(mastX + 44, ground + 8, 64, 10, 0, 0, Math.PI * 2);
      ctx.fill();
      rr(mastX + 2, ground - 43, 86, 34, 5, "#eeae3c", "rgba(255,231,178,.4)");
      rr(mastX + 26, ground - 74, 37, 31, 3, "#28495e", "rgba(201,229,245,.42)");
      rr(mastX + 30, ground - 70, 27, 20, 2, "#a3d0e4", "rgba(224,246,255,.38)");
      ctx.fillStyle = "#1e3448";
      ctx.fillRect(mastX + 2, ground - 15, 86, 11);
      ctx.fillStyle = "#283a4c";
      [mastX + 20, mastX + 72].forEach((wx) => {
        ctx.beginPath(); ctx.arc(wx, ground - 4, 11, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = "#a4bccb"; ctx.beginPath(); ctx.arc(wx, ground - 4, 4, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = "#283a4c";
      });
      ctx.fillStyle = "#365a73";
      ctx.fillRect(mastX - 7, 218, 7, ground - 218);
      ctx.fillRect(mastX + 9, 218, 7, ground - 218);
      rr(mastX - 13, forkY - 10, 31, 18, 2, "#365a73", "#c3ddea");
      line(mastX - 12, forkY + 2, mastX - 84 - forkExtension, forkY + 2, "#c3ddea", 3);
      line(mastX - 12, forkY + 7, mastX - 84 - forkExtension, forkY + 7, "#87abc2", 2);
      ctx.fillStyle = "#f0c8ab";
      ctx.beginPath(); ctx.arc(mastX + 45, ground - 71, 4, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = "#f7d862";
      ctx.fillRect(mastX + 42, ground - 64, 7, 13);
      ctx.restore();
      return { palletX: mastX - 52 - forkExtension };
    }
    function floor() {
      const g = ctx.createLinearGradient(0, 335, 0, 510);
      g.addColorStop(0, "#163c55");
      g.addColorStop(1, "#0b2034");
      ctx.fillStyle = g;
      ctx.fillRect(0, 335, BASE_W, 175);
      for (let x = -100; x < BASE_W + 110; x += 72) line(x, 510, x + 210, 335, "rgba(170,211,237,.08)");
      for (let y = 355; y < 510; y += 34) line(0, y, BASE_W, y, "rgba(170,211,237,.07)");
      line(24, 397, 935, 397, "rgba(242,193,82,.38)", 2, [9, 9]);
      line(24, 405, 935, 405, "rgba(242,193,82,.16)", 1, [9, 9]);
    }
    function routeArrow(x, y, dir, color) {
      ctx.save();
      ctx.globalAlpha = .5;
      ctx.fillStyle = color;
      if (dir === "right") poly([[x, y], [x + 20, y], [x + 20, y - 7], [x + 33, y + 4], [x + 20, y + 15], [x + 20, y + 8], [x, y + 8]], color);
      else poly([[x, y], [x - 20, y], [x - 20, y - 7], [x - 33, y + 4], [x - 20, y + 15], [x - 20, y + 8], [x, y + 8]], color);
      ctx.restore();
    }
    function draw(time) {
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);
      const bg = ctx.createLinearGradient(0, 0, 0, H);
      bg.addColorStop(0, "#1b4166");
      bg.addColorStop(.65, "#0d263f");
      bg.addColorStop(1, "#081827");
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, W, H);

      const scale = Math.min(W / BASE_W, H / BASE_H);
      const ox = (W - BASE_W * scale) / 2;
      const oy = (H - BASE_H * scale) / 2;
      ctx.setTransform(dpr * scale, 0, 0, dpr * scale, dpr * ox, dpr * oy);

      const seconds = (time % 11500) / 1000;
      const leftArrive = ease(ramp(seconds, .15, 1.8));
      const leftLeave = ease(ramp(seconds, 7.35, 8.9));
      let leftBodyX = -145;
      if (seconds < 1.8) leftBodyX = lerp(-145, 160, leftArrive);
      else if (seconds < 7.35) leftBodyX = 160;
      else leftBodyX = lerp(160, -145, leftLeave);
      const leftLiftUp = ease(ramp(seconds, 1.8, 4.0));
      const leftLiftDown = ease(ramp(seconds, 5.45, 7.15));
      let leftForkY = 367;
      if (seconds < 4.0) leftForkY = lerp(367, 174, leftLiftUp);
      else if (seconds < 5.45) leftForkY = 174;
      else leftForkY = lerp(174, 367, leftLiftDown);
      const leftExtension = 16 * smooth(ramp(seconds, 4.0, 4.8)) * (1 - smooth(ramp(seconds, 4.95, 5.45)));
      const leftStored = seconds >= 5.05;

      const rightArrive = ease(ramp(seconds, .85, 2.55));
      const rightLeave = ease(ramp(seconds, 4.45, 5.95));
      let rightMastX = 1050;
      if (seconds < 2.55) rightMastX = lerp(1050, 835, rightArrive);
      else if (seconds < 4.45) rightMastX = 835;
      else rightMastX = lerp(835, 1050, rightLeave);
      const rightDrop = ease(ramp(seconds, 2.55, 3.65));
      const rightForkY = lerp(338, 362, rightDrop);
      const rightExtension = 8 * smooth(ramp(seconds, 3.1, 3.65));
      const rightStored = seconds >= 3.78;

      floor();
      routeArrow(44, 418, "right", "#69d8ba");
      routeArrow(520, 418, "left", "#f4c44d");
      rack(120, 80, 320, 300, "A-04  •  HIGH BAY", { level: 0, bay: 1 }, leftStored);
      rack(560, 80, 300, 300, "B-01  •  GROUND", { level: 2, bay: 1 }, rightStored);

      if (leftStored) pallet(354, 174, 61, "#d99045");
      if (rightStored) pallet(778, 362, 60, "#cc833c");

      if (seconds < 7.35 || seconds > 8.9) {
        const reach = reachTruck(leftBodyX, leftForkY, leftExtension);
        if (!leftStored && leftBodyX > -70) pallet(reach.palletX, leftForkY - 7, 60, "#d99045");
      }
      if (seconds < 4.45 || seconds > 5.95) {
        const counter = counterbalanceTruck(rightMastX, rightForkY, rightExtension);
        if (!rightStored && rightMastX < 1010) pallet(counter.palletX, rightForkY - 7, 60, "#cc833c");
      }

      ctx.save();
      ctx.globalAlpha = .66;
      rr(126, 451, 171, 23, 11, "rgba(8,24,40,.76)", "rgba(130,184,221,.21)");
      text("REACH TRUCK  •  LEVEL 3", 211, 466, 10, "#b9dcef", 800, "center");
      rr(611, 451, 179, 23, 11, "rgba(8,24,40,.76)", "rgba(130,184,221,.21)");
      text("COUNTERBALANCE  •  LEVEL 1", 700, 466, 10, "#b9dcef", 800, "center");
      ctx.restore();

      requestAnimationFrame(draw);
    }
    requestAnimationFrame(draw);
  </script>
</body>
</html>
"""


st.markdown(
    """
    <style>
      :root {
        --ink: #07111F;
        --paper: #F6F8FB;
        --card: #FFFFFF;
        --muted: #5D6B7E;
        --line: #DDE4ED;
        --navy: #10233E;
        --blue: #4D7CFE;
        --mint: #34C99A;
        --orange: #FF9A5D;
        --red: #EE6A63;
      }
      .stApp { background: var(--paper); }
      [data-testid="stSidebar"],
      [data-testid="stSidebarCollapsedControl"] { display: none !important; }
      [data-testid="stHeader"] { background: rgba(0,0,0,0); }
      .block-container {
        max-width: 1180px;
        padding: 3.2rem 2rem 5rem 2rem;
      }
      .eyebrow {
        color: #3B67E5;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
      }
      .hero-title {
        color: var(--ink);
        font-size: clamp(2.45rem, 5vw, 4.8rem);
        font-weight: 780;
        line-height: 1.02;
        letter-spacing: -0.06em;
        margin: 0 0 1.2rem 0;
      }
      .hero-copy {
        color: var(--muted);
        font-size: 1.16rem;
        line-height: 1.58;
        max-width: 510px;
        margin: 0;
      }
      .label {
        color: #3B67E5;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.10em;
        text-transform: uppercase;
      }
      .section-title {
        color: var(--ink);
        font-size: clamp(1.7rem, 3vw, 2.55rem);
        font-weight: 750;
        line-height: 1.08;
        letter-spacing: -0.045em;
        margin: 0.35rem 0 0.8rem 0;
      }
      .section-copy {
        color: var(--muted);
        font-size: 1.04rem;
        line-height: 1.55;
        max-width: 740px;
      }
      [data-testid="stImage"] img {
        border-radius: 20px;
        box-shadow: 0 22px 48px rgba(23, 40, 70, 0.18);
      }
      .story-rule {
        height: 1px;
        background: var(--line);
        margin: 5.0rem 0;
      }
      .task-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 8px 26px rgba(24, 43, 70, 0.06);
      }
      .task-card-head {
        display: flex;
        gap: 0.65rem;
        align-items: center;
        padding: 1rem 1.15rem 0.25rem 1.15rem;
      }
      .task-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        flex: none;
      }
      .task-name {
        color: var(--ink);
        font-weight: 780;
        font-size: 1.05rem;
      }
      .task-copy {
        color: var(--muted);
        line-height: 1.48;
        padding: 0.35rem 1.15rem 1.1rem 1.15rem;
        min-height: 70px;
      }
      .pph-strip {
        background: #EEF2F7;
        color: #3D4E64;
        font-size: 0.8rem;
        font-weight: 750;
        padding: 0.7rem 1.15rem;
        border-top: 1px solid var(--line);
      }
      .center-message {
        background: var(--navy);
        color: #FFFFFF;
        border-radius: 18px;
        padding: 1.35rem 1.15rem;
        margin: 1.25rem 0 0 0;
        text-align: center;
      }
      .center-message .small {
        color: #9CC3FF;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.10em;
        text-transform: uppercase;
      }
      .center-message .main {
        font-size: 1.28rem;
        line-height: 1.25;
        font-weight: 720;
        margin-top: 0.35rem;
      }
      .flow {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.9rem;
        margin-top: 2rem;
      }
      .flow-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 1.1rem;
        min-height: 180px;
        position: relative;
      }
      .flow-card:not(:last-child)::after {
        content: "→";
        position: absolute;
        right: -0.83rem;
        top: 43%;
        z-index: 2;
        width: 1.5rem;
        height: 1.5rem;
        border-radius: 50%;
        background: var(--blue);
        color: #FFF;
        display: grid;
        place-items: center;
        font-weight: 800;
      }
      .flow-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: grid;
        place-items: center;
        font-size: 1.05rem;
        margin-bottom: 1rem;
      }
      .flow-card h3 {
        color: var(--ink);
        font-size: 1rem;
        margin: 0 0 0.45rem 0;
      }
      .flow-card p {
        color: var(--muted);
        font-size: 0.87rem;
        line-height: 1.45;
        margin: 0;
      }
      .motion-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.42rem;
        margin-top: 0.8rem;
      }
      .motion {
        color: #254670;
        background: #ECF3FF;
        border: 1px solid #D6E5FF;
        border-radius: 100px;
        padding: 0.24rem 0.52rem;
        font-size: 0.72rem;
        font-weight: 700;
      }
      .twin-board {
        background: linear-gradient(135deg, #0E203A 0%, #142C4E 100%);
        border-radius: 22px;
        padding: 1.6rem;
        box-shadow: 0 22px 44px rgba(23, 40, 70, 0.16);
      }
      .twin-label {
        color: #92B9FF;
        font-size: 0.74rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
      }
      .twin-title {
        color: #FFFFFF;
        font-size: clamp(1.45rem, 3vw, 2.2rem);
        letter-spacing: -0.04em;
        line-height: 1.1;
        margin: 0.45rem 0 0.7rem 0;
      }
      .twin-copy {
        color: #C3D4EC;
        font-size: 0.98rem;
        line-height: 1.5;
        max-width: 610px;
      }
      .test-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.8rem;
        margin-top: 1.35rem;
      }
      .test-card {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(169, 197, 239, 0.20);
        border-radius: 14px;
        padding: 1rem;
      }
      .test-card h3 {
        color: #FFFFFF;
        font-size: 0.96rem;
        margin: 0 0 0.35rem 0;
      }
      .test-card p {
        color: #BFD0E8;
        font-size: 0.82rem;
        line-height: 1.42;
        margin: 0;
      }
      .closing {
        color: var(--ink);
        font-size: clamp(1.8rem, 4vw, 3.3rem);
        font-weight: 760;
        line-height: 1.08;
        letter-spacing: -0.05em;
        max-width: 900px;
        margin-top: 1rem;
      }
      @media (max-width: 800px) {
        .block-container { padding: 2rem 1rem 4rem 1rem; }
        .flow { grid-template-columns: 1fr 1fr; }
        .flow-card:not(:last-child)::after { display: none; }
        .test-grid { grid-template-columns: 1fr; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="eyebrow">Labor standards • workload forecasting • digital twin</div>', unsafe_allow_html=True)
hero_copy, hero_visual = st.columns([0.92, 1.08], gap="large")
with hero_copy:
    st.markdown(
        '<h1 class="hero-title">A warehouse can have the right volume and still schedule the wrong labor.</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="hero-copy">When every pallet is treated as the same unit of work, the plan cannot see the travel, equipment, elevation, handling, or congestion that actually determines labor. Without standards, a workload-driven forecast, or a digital twin, teams are left to react on the floor.</p>',
        unsafe_allow_html=True,
    )
with hero_visual:
    st.iframe(WAREHOUSE_ANIMATION, height=510, width="stretch", alt="Animated warehouse digital twin")
    st.caption("Illustrative animated digital-twin environment")


st.markdown('<div class="story-rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="label">The PPH problem</div>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Two pallet moves can share one PPH metric but require completely different work.</h2>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-copy">PPH is useful as a high-level output. It becomes misleading when it is used as the labor standard itself. The same count conceals the operational conditions behind each movement.</p>',
    unsafe_allow_html=True,
)

short_html = """
<div class="task-card">
  <div class="task-card-head"><span class="task-dot" style="background:#34C99A"></span><span class="task-name">Pallet A: a simple move</span></div>
  <div style="padding:0.45rem 1.0rem 0.3rem 1.0rem">
    <svg viewBox="0 0 520 185" width="100%" role="img" aria-label="Short ground-level pallet route">
      <rect x="8" y="10" width="504" height="162" rx="14" fill="#F3F8F7"/>
      <rect x="310" y="31" width="118" height="98" rx="4" fill="#7891A5"/>
      <g stroke="#F3F8F7" stroke-width="4"><line x1="310" y1="63" x2="428" y2="63"/><line x1="310" y1="96" x2="428" y2="96"/><line x1="349" y1="31" x2="349" y2="129"/><line x1="389" y1="31" x2="389" y2="129"/></g>
      <rect x="347" y="101" width="37" height="20" fill="#F2C84A"/><rect x="351" y="94" width="29" height="10" fill="#D59B45"/>
      <path d="M100,122 C170,122 220,122 329,122" fill="none" stroke="#34C99A" stroke-width="8" stroke-linecap="round"/>
      <polygon points="329,122 313,113 313,131" fill="#34C99A"/>
      <rect x="67" y="102" width="44" height="26" rx="3" fill="#F7C84C"/><rect x="106" y="92" width="13" height="42" fill="#22344B"/><circle cx="78" cy="135" r="8" fill="#22344B"/><circle cx="108" cy="135" r="8" fill="#22344B"/>
      <text x="55" y="157" fill="#4E657A" font-size="16" font-family="Arial">Forklift</text>
      <text x="305" y="157" fill="#4E657A" font-size="16" font-family="Arial">Ground-level slot</text>
    </svg>
  </div>
  <div class="task-copy">Short travel, ground-level access, familiar equipment, and a direct route.</div>
  <div class="pph-strip">Reported as: one pallet movement</div>
</div>
"""

complex_html = """
<div class="task-card">
  <div class="task-card-head"><span class="task-dot" style="background:#EE6A63"></span><span class="task-name">Pallet B: a complex move</span></div>
  <div style="padding:0.45rem 1.0rem 0.3rem 1.0rem">
    <svg viewBox="0 0 520 185" width="100%" role="img" aria-label="Long high-rack pallet route">
      <rect x="8" y="10" width="504" height="162" rx="14" fill="#FFF5F1"/>
      <rect x="344" y="22" width="118" height="124" rx="4" fill="#7891A5"/>
      <g stroke="#F3F8F7" stroke-width="4"><line x1="344" y1="53" x2="462" y2="53"/><line x1="344" y1="84" x2="462" y2="84"/><line x1="344" y1="115" x2="462" y2="115"/><line x1="383" y1="22" x2="383" y2="146"/><line x1="423" y1="22" x2="423" y2="146"/></g>
      <rect x="420" y="26" width="36" height="19" fill="#F2C84A"/><rect x="424" y="19" width="28" height="10" fill="#D59B45"/>
      <path d="M90,130 C155,152 242,150 278,122 S325,59 410,39" fill="none" stroke="#EE6A63" stroke-width="8" stroke-linecap="round" stroke-dasharray="12 9"/>
      <polygon points="410,39 393,36 400,52" fill="#EE6A63"/>
      <rect x="58" y="109" width="40" height="22" rx="3" fill="#F7C84C"/><rect x="93" y="68" width="12" height="68" fill="#22344B"/><rect x="103" y="67" width="18" height="5" fill="#22344B"/><circle cx="69" cy="137" r="8" fill="#22344B"/><circle cx="97" cy="137" r="8" fill="#22344B"/>
      <text x="43" y="158" fill="#4E657A" font-size="16" font-family="Arial">Reach truck</text>
      <text x="330" y="163" fill="#4E657A" font-size="16" font-family="Arial">High-rack placement</text>
    </svg>
  </div>
  <div class="task-copy">Longer travel, higher placement, specialized equipment, and more potential interference.</div>
  <div class="pph-strip">Reported as: one pallet movement</div>
</div>
"""

task_a, task_b = st.columns(2, gap="large")
with task_a:
    st.markdown(short_html, unsafe_allow_html=True)
with task_b:
    st.markdown(complex_html, unsafe_allow_html=True)

st.markdown(
    '<div class="center-message"><div class="small">The hidden mismatch</div><div class="main">One output metric. Two different labor requirements.</div></div>',
    unsafe_allow_html=True,
)


st.markdown('<div class="story-rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="label">Make the work visible</div>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Create a labor standard for the work actually being performed.</h2>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-copy">MOST gives each movement a structured, defensible time. Those standards turn operational variation into a usable system for planning, forecasting, and execution.</p>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="flow">
      <div class="flow-card">
        <div class="flow-icon" style="background:#EAF1FF">▣</div>
        <h3>Identify task types</h3>
        <p>Separate the simple move from the high-rack, long-travel, or special-equipment move.</p>
      </div>
      <div class="flow-card">
        <div class="flow-icon" style="background:#E7FAF4">◫</div>
        <h3>Build MOST standards</h3>
        <p>Break each task into the motions and conditions that determine its expected time.</p>
        <div class="motion-row"><span class="motion">travel</span><span class="motion">access</span><span class="motion">lift</span><span class="motion">place</span></div>
      </div>
      <div class="flow-card">
        <div class="flow-icon" style="background:#FFF0E8">▤</div>
        <h3>Create the standard library</h3>
        <p>Store standards by task, zone, equipment, position, and handling condition.</p>
      </div>
      <div class="flow-card">
        <div class="flow-icon" style="background:#F3EDFF">⌁</div>
        <h3>Forecast the work mix</h3>
        <p>Predict the expected mix of task types, then translate it into labor by hour, shift, and zone.</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="story-rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="label">Test the future safely</div>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Turn the warehouse into a digital twin before changing the real operation.</h2>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-copy">Once the work is measured and forecasted, a digital twin lets the operation test alternatives without relying on rough estimates or expensive trial-and-error on the floor.</p>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="twin-board">
      <div class="twin-label">Digital twin scenario environment</div>
      <div class="twin-title">Test the operating design before the operation has to live with it.</div>
      <div class="twin-copy">Use the model to compare choices, observe the flow they create, and select an operating plan with clearer tradeoffs.</div>
      <div class="test-grid">
        <div class="test-card"><h3>Labor</h3><p>Test staffing levels, shift coverage, skills, and work allocation.</p></div>
        <div class="test-card"><h3>Work</h3><p>Test task release, routing, congestion, replenishment, and dock priorities.</p></div>
        <div class="test-card"><h3>Layout</h3><p>Test slotting, storage locations, travel paths, equipment, and material flow.</p></div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="story-rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="label">The outcome</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="closing">From a generic productivity rate to a testable operating plan built around the work itself.</div>',
    unsafe_allow_html=True,
)
