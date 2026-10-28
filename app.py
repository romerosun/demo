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

PEOPLE_PALLET_ANIMATION = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    html, body { margin: 0; background: #0C1C31; overflow: hidden; }
    .stage {
      height: 510px; position: relative; overflow: hidden; border-radius: 22px;
      background: radial-gradient(circle at 46% 17%, #365979 0%, #162C47 52%, #0A1727 100%);
      font-family: Inter, ui-sans-serif, system-ui, sans-serif;
    }
    svg { width: 100%; height: 100%; display: block; }
    .badge {
      position:absolute; top:18px; left:20px; color:#C9DDFF; background:rgba(8,25,44,.68);
      border:1px solid rgba(148,190,255,.28); border-radius:999px; padding:8px 12px;
      font-size:10px; font-weight:800; letter-spacing:.11em; text-transform:uppercase;
    }
    .caption {
      position:absolute; left:20px; bottom:18px; max-width:285px; color:#DCE9F8;
      font-size:12px; line-height:1.45; text-shadow:0 1px 6px rgba(0,0,0,.35);
    }
    .caption b { color:#FFFFFF; }
    .mover { animation: carry 5.5s ease-in-out infinite; }
    .pulse { animation: fade 5.5s ease-in-out infinite; }
    @keyframes carry {
      0%, 8% { transform: translate(0px, 0px); opacity: 1; }
      62%, 78% { transform: translate(255px, -108px); opacity: 1; }
      100% { transform: translate(255px, -108px); opacity: 0; }
    }
    @keyframes fade {
      0%, 58% { opacity:.18; } 70%, 86% { opacity:1; } 100% { opacity:.18; }
    }
  </style>
</head>
<body>
  <div class="stage">
    <svg viewBox="0 0 780 510" aria-label="Workers moving pallets through a staging area">
      <defs>
        <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
          <path d="M24 0H0V24" fill="none" stroke="rgba(177,208,235,.16)" stroke-width="1"/>
        </pattern>
        <filter id="glow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      </defs>
      <polygon points="76,375 431,186 709,331 342,491" fill="#243D59" stroke="#7195B7" stroke-width="2"/>
      <polygon points="76,375 431,186 709,331 342,491" fill="url(#grid)" opacity=".72"/>
      <g opacity=".93">
        <polygon points="477,197 635,280 615,291 457,208" fill="#7C9BB7"/>
        <polygon points="457,208 615,291 615,356 457,273" fill="#426783"/>
        <g stroke="#DDEAF5" stroke-width="3" opacity=".72">
          <path d="M477 207L477 283M508 223L508 299M539 239L539 315M570 255L570 331M601 271L601 347"/>
          <path d="M466 234L624 317M466 259L624 342"/>
        </g>
      </g>
      <path d="M176 394 C273 366 357 326 459 264" fill="none" stroke="#4DD3A2" stroke-width="8" stroke-linecap="round" stroke-dasharray="10 11" filter="url(#glow)"/>
      <g class="mover">
        <ellipse cx="188" cy="399" rx="24" ry="9" fill="rgba(0,0,0,.30)"/>
        <circle cx="183" cy="352" r="12" fill="#F2C7A7"/>
        <path d="M172 348H194" stroke="#EFF5F8" stroke-width="6"/>
        <rect x="171" y="365" width="24" height="35" rx="5" fill="#42B883"/>
        <path d="M178 399L174 417M189 399L194 415" stroke="#203544" stroke-width="5" stroke-linecap="round"/>
        <rect x="204" y="378" width="43" height="27" rx="3" fill="#D9A064" stroke="#8F5B34" stroke-width="2"/>
        <path d="M218 378V405M232 378V405M204 391H247" stroke="#B87846" stroke-width="1.5"/>
      </g>
      <g>
        <ellipse cx="491" cy="259" rx="21" ry="8" fill="rgba(0,0,0,.28)"/>
        <circle cx="489" cy="216" r="11" fill="#F2C7A7"/>
        <path d="M479 211H499" stroke="#EFF5F8" stroke-width="5"/>
        <rect x="478" y="228" width="22" height="32" rx="5" fill="#E4D833"/>
        <path d="M484 260L480 276M494 260L499 275" stroke="#203544" stroke-width="5" stroke-linecap="round"/>
      </g>
      <g>
        <ellipse cx="305" cy="336" rx="21" ry="8" fill="rgba(0,0,0,.28)"/>
        <circle cx="303" cy="293" r="11" fill="#F2C7A7"/>
        <path d="M293 288H313" stroke="#EFF5F8" stroke-width="5"/>
        <rect x="292" y="305" width="22" height="32" rx="5" fill="#D9655A"/>
        <path d="M298 337L294 352M308 337L313 351" stroke="#203544" stroke-width="5" stroke-linecap="round"/>
      </g>
      <g class="pulse">
        <circle cx="468" cy="269" r="21" fill="none" stroke="#4DD3A2" stroke-width="3"/>
        <circle cx="468" cy="269" r="32" fill="none" stroke="rgba(77,211,162,.45)" stroke-width="2"/>
      </g>
    </svg>
    <div class="badge">Illustrative manual flow</div>
    <div class="caption"><b>People move work too.</b><br>Every handoff, walk, scan, and placement becomes a measurable part of the work.</div>
  </div>
</body>
</html>
"""


COVER_FLOOR = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    html, body { margin: 0; background: #e9edf2; overflow: hidden; }
    .stage {
      position: relative;
      height: 580px;
      overflow: hidden;
      border-radius: 22px;
      background: linear-gradient(135deg, #f6f8fb 0%, #e5eaf0 100%);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      box-shadow: 0 20px 50px rgba(20, 43, 70, .15);
    }
    canvas { display: block; width: 100%; height: 100%; }
    .chip {
      position: absolute; top: 18px; left: 20px;
      padding: 8px 12px; border: 1px solid rgba(32, 61, 91, .18);
      border-radius: 999px; color: #274462; background: rgba(255,255,255,.78);
      font-size: 10px; font-weight: 800; letter-spacing: .11em; text-transform: uppercase;
    }
    .note {
      position: absolute; right: 20px; bottom: 17px; color: #536d85;
      font-size: 11px; font-weight: 700; letter-spacing: .04em;
    }
  </style>
</head>
<body>
  <div class="stage">
    <canvas id="cover-floor"></canvas>
    <div class="chip">Grid-based facility foundation</div>
    <div class="note">90 m × 52 m • 1 m planning grid</div>
  </div>
  <script>
    const canvas = document.getElementById("cover-floor");
    const ctx = canvas.getContext("2d");
    const BASE_W = 960;
    const BASE_H = 580;
    const FACILITY_W = 90;
    const FACILITY_D = 52;
    let width = 0, height = 0, dpr = 1;

    function resize() {
      const box = canvas.getBoundingClientRect();
      width = Math.max(1, box.width);
      height = Math.max(1, box.height);
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      draw();
    }
    window.addEventListener("resize", resize);
    if (window.ResizeObserver) new ResizeObserver(resize).observe(document.body);

    function poly(points, fill, stroke, lineWidth = 1) {
      ctx.beginPath();
      ctx.moveTo(points[0].x, points[0].y);
      for (let i = 1; i < points.length; i++) ctx.lineTo(points[i].x, points[i].y);
      ctx.closePath();
      if (fill) { ctx.fillStyle = fill; ctx.fill(); }
      if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = lineWidth; ctx.stroke(); }
    }
    function line(a, b, color, lineWidth = 1, dash = []) {
      ctx.save();
      ctx.beginPath();
      ctx.setLineDash(dash);
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.strokeStyle = color;
      ctx.lineWidth = lineWidth;
      ctx.stroke();
      ctx.restore();
    }
    function text(value, x, y, size, color, weight = 700, align = "left") {
      ctx.save();
      ctx.fillStyle = color;
      ctx.font = weight + " " + size + "px Inter, Arial, sans-serif";
      ctx.textAlign = align;
      ctx.fillText(value, x, y);
      ctx.restore();
    }
    function draw() {
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, width, height);
      const scale = Math.min(width / BASE_W, height / BASE_H);
      const ox = (width - BASE_W * scale) / 2;
      const oy = (height - BASE_H * scale) / 2;
      ctx.setTransform(dpr * scale, 0, 0, dpr * scale, dpr * ox, dpr * oy);

      const bg = ctx.createLinearGradient(0, 0, 0, BASE_H);
      bg.addColorStop(0, "#f7f9fc");
      bg.addColorStop(1, "#e4eaf1");
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, BASE_W, BASE_H);

      const sx = 5.55;
      const sy = 2.72;
      const origin = { x: 484, y: 76 };
      const iso = (x, y, z = 0) => ({
        x: origin.x + (x - y) * sx,
        y: origin.y + (x + y) * sy - z * 12,
      });
      const hash = (a, b, c) => {
        const n = Math.sin(a * 12.9898 + b * 78.233 + c * 37.719) * 43758.5453;
        return n - Math.floor(n);
      };
      function cuboid(x, y, w, depth, z, h, top, front, side, stroke = null) {
        const a = iso(x, y, z), b = iso(x + w, y, z), c = iso(x + w, y + depth, z), d = iso(x, y + depth, z);
        const ta = iso(x, y, z + h), tb = iso(x + w, y, z + h), tc = iso(x + w, y + depth, z + h), td = iso(x, y + depth, z + h);
        poly([b, c, tc, tb], side, stroke);
        poly([c, d, td, tc], front, stroke);
        poly([ta, tb, tc, td], top, stroke);
      }
      function pallet(x, y, w, depth, z, tint = "#c98a48") {
        cuboid(x, y, w, depth, z, .14, "#c8955a", "#8d5a30", "#a56f3d", "rgba(83,57,32,.35)");
        cuboid(x + .10, y + .10, w - .20, depth - .20, z + .14, .96, tint, "#9f6433", "#b8773e", "rgba(255,242,212,.32)");
        const split = iso(x + w / 2, y + .10, z + 1.10);
        const splitEnd = iso(x + w / 2, y + depth - .10, z + 1.10);
        const cross = iso(x + .10, y + depth / 2, z + 1.10);
        const crossEnd = iso(x + w - .10, y + depth / 2, z + 1.10);
        line(split, splitEnd, "rgba(91,52,29,.32)", .7);
        line(cross, crossEnd, "rgba(91,52,29,.24)", .7);
      }
      function rackRow(x, y, length, depth, rowIndex) {
        const bay = 4;
        const bays = Math.floor(length / bay);
        const levels = [.14, 2.65, 5.16];
        const beams = [1.48, 3.99, 6.50];
        const occupancy = [.56, .73, .47, .64, .36, .68][rowIndex % 6];

        levels.forEach((z, level) => {
          for (let i = 0; i < bays; i++) {
            if (hash(i, level, rowIndex) < occupancy) {
              const tint = hash(i + 2, level, rowIndex) > .32 ? "#cd914c" : "#d9dce1";
              pallet(x + i * bay + .28, y + .34, 2.34, depth - .68, z, tint);
            }
          }
        });
        beams.forEach((z) => {
          cuboid(x, y + .10, length, .18, z, .17, "#f4a33e", "#b95f1f", "#d87f2c");
          cuboid(x, y + depth - .28, length, .18, z, .17, "#f4a33e", "#b95f1f", "#d87f2c");
        });
        for (let i = 0; i <= bays; i++) {
          const px = x + i * bay - .08;
          cuboid(px, y + .04, .18, .18, 0, 7.55, "#7199ba", "#1d4f78", "#3a77a7");
          cuboid(px, y + depth - .22, .18, .18, 0, 7.55, "#7199ba", "#1d4f78", "#3a77a7");
        }
      }
      function conveyor(x, y, length, depth = 1.25) {
        cuboid(x, y, length, depth, .30, .22, "#5e8bb0", "#245578", "#3d7099");
        for (let u = .4; u < length; u += .8) {
          line(iso(x + u, y + .08, .54), iso(x + u, y + depth - .08, .54), "rgba(230,242,251,.72)", .7);
        }
        [x + .45, x + length - .55].forEach((px) => {
          cuboid(px, y + .18, .14, .14, 0, .34, "#547287", "#294a62", "#3b5c74");
          cuboid(px, y + depth - .32, .14, .14, 0, .34, "#547287", "#294a62", "#3b5c74");
        });
      }
      function worker(x, y) {
        const feet = iso(x, y, .06);
        const torso = iso(x, y, 1.02);
        const head = iso(x, y, 1.60);
        ctx.save();
        ctx.strokeStyle = "#263847";
        ctx.lineWidth = 1.3;
        ctx.beginPath();
        ctx.moveTo(feet.x - 2.5, feet.y); ctx.lineTo(torso.x - 1.5, torso.y + 7);
        ctx.moveTo(feet.x + 2.5, feet.y); ctx.lineTo(torso.x + 1.5, torso.y + 7);
        ctx.stroke();
        ctx.fillStyle = "#42b883";
        ctx.fillRect(torso.x - 3.2, torso.y + 1, 6.4, 8.4);
        ctx.fillStyle = "#f0caab";
        ctx.beginPath(); ctx.arc(head.x, head.y + 2.7, 3.1, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = "#f7f4e8";
        ctx.fillRect(head.x - 3.4, head.y, 6.8, 2.0);
        ctx.restore();
      }
      function forklift(x, y, kind = "counterbalance") {
        const reach = kind === "reach";
        const body = reach ? "#efbb3d" : "#f3c84e";
        const shadow = iso(x + 1.05, y + .58, .01);
        ctx.save();
        ctx.fillStyle = "rgba(29, 42, 53, .18)";
        ctx.beginPath(); ctx.ellipse(shadow.x, shadow.y + 4, 12, 4.4, 0, 0, Math.PI * 2); ctx.fill();
        ctx.restore();
        cuboid(x, y, 2.15, 1.16, .13, .55, body, "#ad761f", "#cf992b");
        cuboid(x + .42, y + .16, .96, .82, .68, .88, "#39566c", "#173348", "#26465d");
        cuboid(x + .62, y + .28, .55, .52, 1.56, .10, "#ecf3f7", "#9bb2c0", "#c9d9e1");
        cuboid(x + 1.80, y + .43, .15, .24, .48, reach ? 3.70 : 2.75, "#29465a", "#142a3b", "#1f3d51");
        cuboid(x + 1.92, y + .48, .95, .10, .50, .08, "#cbdce6", "#849ba9", "#aebfca");
        const w1 = iso(x + .40, y + .16, .11);
        const w2 = iso(x + 1.75, y + .96, .11);
        ctx.save();
        ctx.fillStyle = "#263543";
        [w1, w2].forEach((p) => { ctx.beginPath(); ctx.arc(p.x, p.y + 2, 3.7, 0, Math.PI * 2); ctx.fill(); });
        ctx.restore();
      }
      function palletJack(x, y) {
        cuboid(x, y, 1.30, .68, .10, .18, "#f1b844", "#a97323", "#d29431");
        cuboid(x + 1.10, y + .26, .13, .14, .18, 1.10, "#516a7b", "#263e50", "#3c586b");
      }
      function dock(x) {
        // Trailer, dock portal, and yellow bollards are kept square to the dock grid.
        cuboid(x + .27, 2.02, 2.10, 2.16, .14, 1.28, "#f8fbfd", "#aebec9", "#d9e3e9", "rgba(74, 98, 116, .22)");
        cuboid(x + .42, 3.94, 1.78, .16, .10, .28, "#586a78", "#283d4d", "#425a6c");
        cuboid(x, .75, 2.65, .28, 0, 3.10, "#81909d", "#596875", "#6e7e8b");
        cuboid(x + .20, 1.06, 2.25, .22, .20, 2.35, "#263e54", "#15273a", "#1f3448");
        [.08, 2.40].forEach((offset) => cuboid(x + offset, 1.48, .13, .13, 0, .72, "#ffd22e", "#c69d08", "#e0b512"));
      }
      const floor = [iso(0, 0), iso(FACILITY_W, 0), iso(FACILITY_W, FACILITY_D), iso(0, FACILITY_D)];

      ctx.save();
      ctx.shadowColor = "rgba(33, 56, 79, .18)";
      ctx.shadowBlur = 22;
      ctx.shadowOffsetY = 14;
      poly(floor, "#dfe5eb", "#8ba0b1", 1.5);
      ctx.restore();

      for (let x = 0; x <= FACILITY_W; x++) {
        const strong = x % 10 === 0;
        line(iso(x, 0), iso(x, FACILITY_D), strong ? "rgba(92,119,141,.32)" : "rgba(111,136,156,.13)", strong ? 1.15 : .55);
      }
      for (let y = 0; y <= FACILITY_D; y++) {
        const strong = y % 10 === 0;
        line(iso(0, y), iso(FACILITY_W, y), strong ? "rgba(92,119,141,.32)" : "rgba(111,136,156,.13)", strong ? 1.15 : .55);
      }

      const outline = [iso(0, 0), iso(FACILITY_W, 0), iso(FACILITY_W, FACILITY_D), iso(0, FACILITY_D)];
      poly(outline, null, "#516f86", 1.8);

      // A clean dock-wall datum gives the top edge the same warehouse context as the reference view.
      cuboid(1.4, .20, 28.2, .38, 0, 6.2, "#8c98a4", "#596774", "#73818e");

      function zone(x, y, w, d, fill, border) {
        poly([iso(x,y), iso(x+w,y), iso(x+w,y+d), iso(x,y+d)], fill, border, 1.3);
      }
      function footprint(x, y, w, d) {
        const p = [iso(x,y), iso(x+w,y), iso(x+w,y+d), iso(x,y+d)];
        poly(p, "rgba(79, 116, 149, .10)", "rgba(64, 100, 133, .64)", 1.25);
        const midA = iso(x, y + d / 2);
        const midB = iso(x + w, y + d / 2);
        line(midA, midB, "rgba(64, 100, 133, .26)", 1, [4, 4]);
      }

      zone(4, 31, 27, 16, "rgba(59, 130, 246, .035)", "rgba(59, 130, 246, .25)");
      zone(35, 7, 50, 41, "rgba(15, 118, 110, .018)", "rgba(15, 118, 110, .23)");
      zone(2, 5, 26, 18, "rgba(245, 158, 11, .025)", "rgba(245, 158, 11, .25)");

      // Seven long, parallel selective-rack rows: 2.2 m rack depth and 3.7 m working aisles.
      const rackStartX = 36;
      const rackLength = 48;
      const rackDepth = 2.2;
      const rowY = [7.5, 13.4, 19.3, 25.2, 31.1, 37.0, 42.9];
      rowY.forEach((y) => footprint(rackStartX, y, rackLength, rackDepth));

      // Cross aisle and dock-facing staging alignment.
      line(iso(32, 5), iso(32, 48), "rgba(245, 158, 11, .84)", 2.4, [8, 6]);
      line(iso(35, 5), iso(85, 5), "rgba(245, 158, 11, .84)", 2.4, [8, 6]);
      line(iso(35, 48), iso(85, 48), "rgba(245, 158, 11, .84)", 2.4, [8, 6]);

      // Yellow travel and safety demarcation, visible in every clear aisle.
      [5.7, 11.6, 17.5, 23.4, 29.3, 35.2, 41.1, 46.2].forEach((y) => {
        line(iso(34, y), iso(85, y), "rgba(250, 202, 21, .92)", 1.55, [7, 5]);
      });
      line(iso(4, 30), iso(31, 30), "rgba(250, 202, 21, .92)", 1.55);
      line(iso(4, 47.6), iso(31, 47.6), "rgba(250, 202, 21, .92)", 1.55);

      // Every operational object is positioned from the exact same metre grid.
      // This makes the view read like a digital-twin viewport rather than a painted illustration.
      for (let x = 4; x <= 24; x += 4) dock(x);

      // Seven straight selective-rack runs with a deliberately mixed pallet occupancy.
      rowY.forEach((y, index) => rackRow(rackStartX, y, rackLength, rackDepth, index));

      // Receiving and consolidation conveyors in the blue staging zone.
      conveyor(4.6, 32.7, 19.2);
      conveyor(4.6, 36.6, 19.2);
      conveyor(4.6, 40.5, 19.2);
      conveyor(5.8, 44.5, 15.3);
      conveyor(21.7, 33.5, 1.2, 10.2);
      conveyor(8.5, 29.9, 13.7);

      // Work in progress at the consolidation benches.
      pallet(5.6, 34.0, 2.2, 1.1, .14);
      pallet(10.5, 35.0, 2.2, 1.1, .14, "#d9dce1");
      pallet(13.3, 38.0, 2.2, 1.1, .14, "#d9dce1");
      pallet(18, 41.1, 2.2, 1.1, .14);
      pallet(24, 45.1, 2.2, 1.1, .14, "#d9dce1");
      pallet(27.2, 19.5, 2.2, 1.1, .14, "#d9dce1");

      // Associates are deliberately clustered at the manual touch points, not inside traffic lanes.
      [
        [7, 34], [10, 35], [13, 33.7], [17, 35.4], [20, 34],
        [8, 39], [12, 38], [16, 39.4], [20, 40],
        [9, 43], [14, 44], [19, 43.5], [23, 45]
      ].forEach(([x, y]) => worker(x, y));

      // A mix of counterbalance and reach trucks makes the equipment strategy legible at a glance.
      forklift(29.5, 15.5, "counterbalance");
      forklift(52, 11.0, "reach");
      forklift(61.5, 22.8, "reach");
      forklift(68, 34.6, "reach");
      forklift(77, 46.0, "counterbalance");
      palletJack(23, 42.5);
    }
    resize();
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


st.markdown(
    """
    <style>
      .cover-kicker {
        color: #3B67E5; font-size: .74rem; font-weight: 800; letter-spacing: .13em;
        text-transform: uppercase; margin: 0 0 .9rem 0;
      }
      .cover-title {
        max-width: 910px; color: #07111F; font-size: clamp(2.55rem, 5.2vw, 5.25rem);
        font-weight: 780; letter-spacing: -.065em; line-height: .98; margin: 0 0 1.15rem 0;
      }
      .cover-copy {
        max-width: 710px; color: #5D6B7E; font-size: 1.08rem; line-height: 1.58; margin: 0 0 1.35rem 0;
      }
      [data-testid="stImage"] img {
        border: 1px solid #DCE5EE; border-radius: 22px; box-shadow: 0 22px 52px rgba(20, 43, 70, .17);
      }
      .cover-pills { display:flex; flex-wrap:wrap; gap:.55rem; margin: 1.15rem 0 4.7rem 0; }
      .cover-pill {
        border: 1px solid #D8E4F1; border-radius: 999px; color: #274462; background: #FFF;
        font-size: .79rem; font-weight: 760; padding: .45rem .78rem;
      }
      .story-step { margin-top: 5.4rem; }
      .step-line { display:flex; align-items:center; gap:.8rem; color:#3B67E5; font-size:.74rem; font-weight:800; letter-spacing:.12em; text-transform:uppercase; }
      .step-number {
        display:grid; place-items:center; width:1.85rem; height:1.85rem; border-radius:50%;
        color:#FFF; background:#3B67E5; font-size:.72rem;
      }
      .step-title {
        max-width:870px; color:#07111F; font-size:clamp(1.85rem, 3.5vw, 3.25rem); font-weight:770;
        letter-spacing:-.055em; line-height:1.05; margin:.85rem 0 .7rem;
      }
      .step-copy { max-width:735px; color:#5D6B7E; font-size:1rem; line-height:1.58; margin:0 0 1.55rem; }
      .visual-label { color:#536D85; font-size:.73rem; font-weight:800; letter-spacing:.1em; text-transform:uppercase; margin:.85rem 0 0; }
      .motion-canvas {
        position:relative; overflow:hidden; min-height:405px; padding:1.55rem; border:1px solid #DCE5EE;
        border-radius:22px; background:linear-gradient(140deg,#F8FAFD 0%,#EAF1F8 100%);
      }
      .motion-caption { color:#26445F; font-weight:800; font-size:.78rem; letter-spacing:.1em; text-transform:uppercase; }
      .motion-figure { display:grid; grid-template-columns: 1.18fr .82fr; gap:1.6rem; align-items:center; margin-top:1.1rem; }
      .motion-traces { display:grid; gap:.75rem; }
      .motion-trace { position:relative; height:2.65rem; border-radius:10px; background:#FFF; border:1px solid #DCE6EE; overflow:hidden; }
      .motion-trace::after {
        content:""; position:absolute; left:9%; right:7%; top:50%; border-top:4px solid #4D7CFE;
        transform:translateY(-50%); border-radius:999px;
      }
      .motion-trace:nth-child(2)::after { left:18%; right:18%; border-top-color:#34C99A; border-top-style:dashed; }
      .motion-trace:nth-child(3)::after { left:4%; right:28%; border-top-color:#FF9A5D; }
      .motion-trace:nth-child(4)::after { left:31%; right:5%; border-top-color:#9A78EE; border-top-style:dashed; }
      .motion-name { position:absolute; z-index:1; top:50%; left:.72rem; transform:translateY(-50%); color:#4D6579; font-size:.73rem; font-weight:760; background:#FFF; padding-right:.35rem; }
      .motion-arrow { color:#4D7CFE; font-size:2rem; font-weight:700; text-align:center; }
      .time-bucket {
        min-height:220px; padding:1.15rem; border-radius:16px; color:#FFF;
        background:linear-gradient(145deg,#122C4B,#214E78); box-shadow:0 16px 28px rgba(20,53,83,.18);
        display:flex; flex-direction:column; justify-content:center; text-align:center;
      }
      .bucket-kicker { color:#9CC4FF; font-size:.68rem; letter-spacing:.1em; font-weight:800; text-transform:uppercase; }
      .bucket-expression { display:flex; align-items:center; justify-content:center; gap:.55rem; margin:.85rem 0 .65rem; color:#FFF; font-size:1.15rem; font-weight:760; }
      .bucket-cell { min-width:78px; padding:.8rem .35rem; border:1px solid rgba(205,226,255,.32); border-radius:10px; background:rgba(255,255,255,.09); }
      .bucket-note { color:#C1D7EE; font-size:.78rem; line-height:1.45; }
      .forecast-map {
        display:grid; grid-template-columns: 1.05fr .18fr 1.55fr; gap:1rem; align-items:center; padding:1.55rem;
        border:1px solid #DCE5EE; border-radius:22px; background:#FFF;
      }
      .variable-stack { display:grid; grid-template-columns:1fr 1fr; gap:.5rem; }
      .variable { color:#4A637A; background:#F4F7FB; border:1px solid #DCE5EE; border-radius:10px; padding:.7rem; font-size:.77rem; font-weight:740; text-align:center; }
      .forecast-arrow { color:#4D7CFE; font-size:2.5rem; text-align:center; font-weight:700; }
      .activity-grid { display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:.65rem; }
      .activity-box { min-height:75px; display:flex; align-items:flex-end; padding:.85rem; border-radius:12px; background:linear-gradient(145deg,#5C88FF,#3B67E5); color:#FFF; font-size:.85rem; font-weight:780; box-shadow:0 8px 16px rgba(59,103,229,.18); }
      .activity-box:nth-child(2) { background:linear-gradient(145deg,#609FE6,#3771B9); }
      .activity-box:nth-child(3) { background:linear-gradient(145deg,#56BCA3,#269174); }
      .activity-box:nth-child(4) { background:linear-gradient(145deg,#9A8FE5,#7468C8); }
      .schedule-board { overflow:hidden; padding:1.55rem; border:1px solid #DCE5EE; border-radius:22px; background:#F8FAFD; }
      .schedule-head { display:flex; align-items:center; justify-content:space-between; gap:1rem; margin-bottom:1rem; }
      .schedule-title { color:#26445F; font-size:.78rem; font-weight:800; letter-spacing:.1em; text-transform:uppercase; }
      .schedule-key { color:#698197; font-size:.75rem; font-weight:700; }
      .schedule-grid { display:grid; grid-template-columns:116px repeat(16,1fr); gap:3px; min-width:720px; }
      .schedule-grid > div { min-height:30px; border-radius:4px; }
      .schedule-row-label { display:flex; align-items:center; color:#4E657A; font-size:.77rem; font-weight:760; }
      .slot { background:#E6ECF2; }
      .slot.active { background:#4D7CFE; }
      .slot.mint { background:#34C99A; }
      .slot.orange { background:#FF9A5D; }
      .slot.purple { background:#9A78EE; }
      .schedule-times { display:grid; grid-template-columns:116px repeat(4,1fr); color:#7D91A3; font-size:.67rem; font-weight:760; margin-top:.55rem; min-width:720px; }
      .dashboard-shell { padding:1.55rem; border-radius:22px; background:linear-gradient(145deg,#0B1930,#152F52); box-shadow:0 22px 48px rgba(20,43,70,.18); }
      .dashboard-top { display:flex; justify-content:space-between; gap:1rem; align-items:flex-start; }
      .dashboard-label { color:#9CC4FF; font-size:.73rem; font-weight:800; letter-spacing:.1em; text-transform:uppercase; }
      .dashboard-title { color:#FFF; font-size:clamp(1.45rem,3vw,2.35rem); line-height:1.08; letter-spacing:-.045em; font-weight:740; margin:.5rem 0 0; }
      .status-pill { color:#BFECD9; border:1px solid rgba(112,220,178,.32); border-radius:999px; padding:.45rem .65rem; font-size:.68rem; font-weight:800; white-space:nowrap; }
      .dashboard-grid { display:grid; grid-template-columns:1.25fr .75fr; gap:1rem; margin-top:1.25rem; }
      .simulation-pane { min-height:230px; border:1px solid rgba(174,207,248,.22); border-radius:14px; background:linear-gradient(145deg,rgba(84,129,173,.28),rgba(10,27,49,.3)); position:relative; overflow:hidden; }
      .simulation-pane::before { content:""; position:absolute; inset:20px; background-image:linear-gradient(rgba(166,203,240,.13) 1px,transparent 1px),linear-gradient(90deg,rgba(166,203,240,.13) 1px,transparent 1px); background-size:23px 23px; transform:skewY(-10deg); opacity:.75; }
      .sim-flow { position:absolute; border-top:4px solid #4D7CFE; border-radius:999px; }
      .sim-flow.one { width:53%; top:47%; left:16%; transform:rotate(-13deg); }
      .sim-flow.two { width:36%; top:62%; left:43%; border-color:#34C99A; transform:rotate(18deg); }
      .sim-node { position:absolute; width:13px; height:13px; border-radius:50%; background:#FFF; box-shadow:0 0 0 5px rgba(77,124,254,.18); }
      .sim-node.a { top:39%; left:16%; } .sim-node.b { top:31%; left:65%; } .sim-node.c { top:68%; left:74%; background:#34C99A; box-shadow:0 0 0 5px rgba(52,201,154,.18); }
      .dashboard-metrics { display:grid; grid-template-columns:1fr 1fr; gap:.75rem; }
      .dashboard-metric { min-height:104px; padding:.85rem; border:1px solid rgba(174,207,248,.20); border-radius:12px; background:rgba(255,255,255,.06); }
      .metric-label { color:#AFC7E3; font-size:.68rem; font-weight:780; letter-spacing:.08em; text-transform:uppercase; }
      .metric-value { color:#FFF; font-size:1.02rem; font-weight:780; margin-top:.75rem; }
      .metric-sub { color:#9FC0D9; font-size:.73rem; margin-top:.25rem; }
      @media (max-width: 800px) {
        .motion-figure, .forecast-map, .dashboard-grid { grid-template-columns:1fr; }
        .forecast-arrow { transform:rotate(90deg); }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="cover-kicker">Labor standards • workload forecasting • simulation</div>', unsafe_allow_html=True)
st.markdown('<h1 class="cover-title">A digital twin for better labor, throughput, and flexibility.</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="cover-copy">Model the work, translate movement into time, forecast it at the right level of detail, and test the operating plan before it reaches the floor.</p>',
    unsafe_allow_html=True,
)
st.image("assets/warehouse_hero_3d.png", use_container_width=True)
st.markdown(
    '<div class="cover-pills"><span class="cover-pill">Labor</span><span class="cover-pill">Throughput</span><span class="cover-pill">Flexibility</span></div>',
    unsafe_allow_html=True,
)


st.markdown('<section class="story-step"><div class="step-line"><span class="step-number">01</span> Model the operation</div><h2 class="step-title">Start with the work as it actually happens.</h2><p class="step-copy">The twin begins with the physical movements of people, equipment, pallets, and locations.</p></section>', unsafe_allow_html=True)
model_left, model_right = st.columns(2, gap="large")
with model_left:
    st.iframe(WAREHOUSE_ANIMATION, height=510, width="stretch", alt="Forklift task animation")
    st.markdown('<p class="visual-label">Equipment movement</p>', unsafe_allow_html=True)
with model_right:
    st.iframe(PEOPLE_PALLET_ANIMATION, height=510, width="stretch", alt="People moving pallets animation")
    st.markdown('<p class="visual-label">Manual pallet movement</p>', unsafe_allow_html=True)


st.markdown('<section class="story-step"><div class="step-line"><span class="step-number">02</span> Translate motion into time</div><h2 class="step-title">Each movement becomes a measurable element of work.</h2><p class="step-copy">Motion traces stack into a standard activity time, creating a common language for labor content.</p></section>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="motion-canvas">
      <div class="motion-caption">Motion sequence → standard time</div>
      <div class="motion-figure">
        <div class="motion-traces">
          <div class="motion-trace"><span class="motion-name">Travel</span></div>
          <div class="motion-trace"><span class="motion-name">Access</span></div>
          <div class="motion-trace"><span class="motion-name">Handle</span></div>
          <div class="motion-trace"><span class="motion-name">Place</span></div>
        </div>
        <div>
          <div class="motion-arrow">→</div>
          <div class="time-bucket">
            <div class="bucket-kicker">Standard activity</div>
            <div class="bucket-expression"><span class="bucket-cell">Activity</span><span>×</span><span class="bucket-cell">Time</span></div>
            <div class="bucket-note">A repeatable unit of labor content, ready to be forecasted and scheduled.</div>
          </div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown('<section class="story-step"><div class="step-line"><span class="step-number">03</span> Forecast the work mix</div><h2 class="step-title">Forecast the variables that actually create the workload.</h2><p class="step-copy">Instead of sending a generic volume number to labor planning, translate granular operating drivers into activity demand.</p></section>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="forecast-map">
      <div class="variable-stack">
        <div class="variable">Order profile</div><div class="variable">SKU family</div>
        <div class="variable">Zone</div><div class="variable">Location level</div>
        <div class="variable">Equipment</div><div class="variable">Handling type</div>
      </div>
      <div class="forecast-arrow">→</div>
      <div class="activity-grid">
        <div class="activity-box">Putaway</div><div class="activity-box">Replenishment</div>
        <div class="activity-box">Picking</div><div class="activity-box">Shipping</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown('<section class="story-step"><div class="step-line"><span class="step-number">04</span> Build the operating schedule</div><h2 class="step-title">Turn forecasted activities into a granular labor plan.</h2><p class="step-copy">Workload is staged into 15-minute intervals so staffing and task release can respond to the shape of demand.</p></section>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="schedule-board">
      <div class="schedule-head"><div class="schedule-title">Activity demand by 15-minute interval</div><div class="schedule-key">Template view • no data loaded</div></div>
      <div class="schedule-grid">
        <div class="schedule-row-label">Receiving</div><div class="slot"></div><div class="slot active"></div><div class="slot active"></div><div class="slot active"></div><div class="slot active"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div>
        <div class="schedule-row-label">Putaway</div><div class="slot"></div><div class="slot"></div><div class="slot mint"></div><div class="slot mint"></div><div class="slot mint"></div><div class="slot mint"></div><div class="slot mint"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div>
        <div class="schedule-row-label">Picking</div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot orange"></div><div class="slot orange"></div><div class="slot orange"></div><div class="slot orange"></div><div class="slot orange"></div><div class="slot orange"></div><div class="slot orange"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div>
        <div class="schedule-row-label">Shipping</div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot purple"></div><div class="slot purple"></div><div class="slot purple"></div><div class="slot purple"></div><div class="slot purple"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div>
      </div>
      <div class="schedule-times"><span></span><span>Start of shift</span><span>Mid-shift</span><span>Peak</span><span>Close</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown('<section class="story-step"><div class="step-line"><span class="step-number">05</span> Test the operating system</div><h2 class="step-title">Run the digital twin as an operating decision dashboard.</h2><p class="step-copy">Compare staffing, throughput, layout, and service scenarios before changing the real operation.</p></section>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="dashboard-shell">
      <div class="dashboard-top">
        <div><div class="dashboard-label">Digital twin scenario workspace</div><div class="dashboard-title">Test the plan before the floor has to live with it.</div></div>
        <div class="status-pill">READY FOR SCENARIOS</div>
      </div>
      <div class="dashboard-grid">
        <div class="simulation-pane"><span class="sim-flow one"></span><span class="sim-flow two"></span><span class="sim-node a"></span><span class="sim-node b"></span><span class="sim-node c"></span></div>
        <div class="dashboard-metrics">
          <div class="dashboard-metric"><div class="metric-label">Labor</div><div class="metric-value">Staffing plan</div><div class="metric-sub">By interval and zone</div></div>
          <div class="dashboard-metric"><div class="metric-label">Throughput</div><div class="metric-value">Flow capacity</div><div class="metric-sub">By task and route</div></div>
          <div class="dashboard-metric"><div class="metric-label">Flexibility</div><div class="metric-value">Scenario range</div><div class="metric-sub">Test alternative rules</div></div>
          <div class="dashboard-metric"><div class="metric-label">Layout</div><div class="metric-value">Operating design</div><div class="metric-sub">Evaluate change safely</div></div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.stop()


st.iframe(COVER_FLOOR, height=580, width="stretch", alt="Grid-based warehouse cover foundation")
st.caption("Grid-based facility foundation. The existing animated warehouse story remains below.")
st.markdown('<div class="story-rule"></div>', unsafe_allow_html=True)

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
