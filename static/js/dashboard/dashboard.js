// FE-03 — Patrimônio chart + period switching
// FE-05 — Month navigation (to be added)
(function () {
  'use strict';

  // ── Chart constants ────────────────────────────────────────────────
  const W = 1000, H = 300;
  const PAD_L = 60, PAD_R = 28, PAD_T = 22, PAD_B = 36;
  const CW = W - PAD_L - PAD_R;
  const CH = H - PAD_T - PAD_B;

  // ── Format helpers ─────────────────────────────────────────────────
  function fmtBR(v, decimals = 2) {
    return 'R$ ' + Number(v).toLocaleString('pt-BR', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    });
  }

  function fmtBRInt(v) {
    return 'R$ ' + Number(v).toLocaleString('pt-BR', {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    });
  }

  // ── Catmull-Rom spline ─────────────────────────────────────────────
  function smoothPath(pts, tension) {
    tension = tension === undefined ? 0.22 : tension;
    if (pts.length === 0) return '';
    if (pts.length === 1) return 'M ' + pts[0].x + ',' + pts[0].y;
    var d = 'M ' + pts[0].x.toFixed(2) + ',' + pts[0].y.toFixed(2);
    for (var i = 0; i < pts.length - 1; i++) {
      var p0 = pts[Math.max(i - 1, 0)];
      var p1 = pts[i];
      var p2 = pts[i + 1];
      var p3 = pts[Math.min(i + 2, pts.length - 1)];
      var c1x = p1.x + (p2.x - p0.x) * tension;
      var c1y = p1.y + (p2.y - p0.y) * tension;
      var c2x = p2.x - (p3.x - p1.x) * tension;
      var c2y = p2.y - (p3.y - p1.y) * tension;
      d += ' C ' + c1x.toFixed(2) + ',' + c1y.toFixed(2) +
           ' ' + c2x.toFixed(2) + ',' + c2y.toFixed(2) +
           ' ' + p2.x.toFixed(2) + ',' + p2.y.toFixed(2);
    }
    return d;
  }

  // ── Build SVG coordinate points from series data ───────────────────
  function buildPoints(series) {
    if (series.length === 0) return [];
    var values = series.map(function (d) { return d.value; });
    var minV = Math.min.apply(null, values);
    var maxV = Math.max.apply(null, values);
    var range = maxV - minV || 1;
    var yMin = Math.floor((minV - range * 0.35) / 100) * 100;
    var yMax = Math.ceil((maxV + range * 0.35) / 100) * 100;
    var n = series.length;
    return series.map(function (d, i) {
      return {
        x: PAD_L + (n === 1 ? CW / 2 : (i / (n - 1)) * CW),
        y: PAD_T + (1 - (d.value - yMin) / (yMax - yMin)) * CH,
        date: d.date,
        value: d.value,
        yMin: yMin,
        yMax: yMax,
      };
    });
  }

  // ── Draw the SVG chart ─────────────────────────────────────────────
  function drawChart(svgEl, series) {
    if (!svgEl || series.length === 0) return [];

    var pts = buildPoints(series);
    var yMin = pts[0].yMin;
    var yMax = pts[0].yMax;
    var linePath = smoothPath(pts);
    var baseY = PAD_T + CH;
    var areaPath = linePath +
      ' L ' + pts[pts.length - 1].x.toFixed(2) + ',' + baseY +
      ' L ' + pts[0].x.toFixed(2) + ',' + baseY + ' Z';

    var gridSvg = '', labelsSvg = '', xLabelsSvg = '';
    var gridSteps = 4;
    for (var i = 0; i <= gridSteps; i++) {
      var gy = PAD_T + (i / gridSteps) * CH;
      var gv = yMax - (i / gridSteps) * (yMax - yMin);
      gridSvg += '<line class="pat-grid-line" x1="' + PAD_L + '" y1="' + gy.toFixed(1) +
                 '" x2="' + (W - PAD_R) + '" y2="' + gy.toFixed(1) + '"/>';
      labelsSvg += '<text class="pat-axis-text" x="' + (PAD_L - 12) + '" y="' + (gy + 4).toFixed(1) +
                   '" text-anchor="end">' + fmtBRInt(gv) + '</text>';
    }

    // Limit x-axis labels to avoid crowding
    var labelStep = Math.max(1, Math.ceil(pts.length / 8));
    pts.forEach(function (p, idx) {
      if (idx % labelStep === 0 || idx === pts.length - 1) {
        xLabelsSvg += '<text class="pat-axis-text" x="' + p.x.toFixed(1) +
                      '" y="' + (baseY + 22).toFixed(1) + '" text-anchor="middle">' + p.date + '</text>';
      }
    });

    var last = pts[pts.length - 1];

    svgEl.innerHTML =
      '<defs>' +
        '<linearGradient id="patAreaGrad" x1="0" y1="0" x2="0" y2="1">' +
          '<stop offset="0" stop-color="var(--color-primary)" stop-opacity=".4"/>' +
          '<stop offset=".5" stop-color="var(--color-primary)" stop-opacity=".1"/>' +
          '<stop offset="1" stop-color="var(--color-primary)" stop-opacity="0"/>' +
        '</linearGradient>' +
        '<linearGradient id="patLineGrad" x1="0" y1="0" x2="1" y2="0">' +
          '<stop offset="0" stop-color="#caa033"/>' +
          '<stop offset=".5" stop-color="var(--color-primary)"/>' +
          '<stop offset="1" stop-color="#fde47a"/>' +
        '</linearGradient>' +
      '</defs>' +
      gridSvg + labelsSvg + xLabelsSvg +
      '<path class="pat-area" d="' + areaPath + '" fill="url(#patAreaGrad)"/>' +
      '<path class="pat-line-glow" d="' + linePath + '"/>' +
      '<path class="pat-line" id="patLineMain" d="' + linePath + '"/>' +
      '<circle class="pat-dot-pulse" cx="' + last.x.toFixed(2) + '" cy="' + last.y.toFixed(2) + '" r="5"/>' +
      '<circle class="pat-dot" cx="' + last.x.toFixed(2) + '" cy="' + last.y.toFixed(2) + '" r="4.5"/>';

    // Set stroke-dasharray length for draw animation
    requestAnimationFrame(function () {
      var path = document.getElementById('patLineMain');
      if (path && path.getTotalLength) {
        path.style.setProperty('--pat-len', path.getTotalLength());
      }
    });

    return pts;
  }

  // ── Update the stats display (value, badge, period label) ──────────
  function updatePatStats(data) {
    var currentValue = parseFloat(data.current_value);
    var changeAbs    = parseFloat(data.change_absolute);
    var changePct    = parseFloat(data.change_percent);
    var period       = data.period;

    var periodLabels = { '1M': 'em 1M', '6M': 'em 6M', '1A': 'em 1A', 'ALL': 'desde o início' };

    var valueEl       = document.getElementById('patrimonio-value');
    var badgeEl       = document.getElementById('patrimonio-badge');
    var badgeAbsEl    = document.getElementById('patrimonio-badge-abs');
    var badgePctEl    = document.getElementById('patrimonio-badge-pct');
    var periodLabelEl = document.getElementById('patrimonio-period-label');
    var insightEl     = document.getElementById('patrimonio-insight-text');

    if (valueEl) {
      valueEl.innerHTML = '<span class="pat-currency">R$</span>' +
        Number(currentValue).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }

    var arrowUp = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M3 17l6-6 4 4 8-8M14 7h7v7"/></svg>';
    var arrowDn = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M3 7l6 6 4-4 8 8M14 17h7v-7"/></svg>';

    if (badgeEl) {
      badgeEl.className = 'pat-chip ' + (changeAbs >= 0 ? 'pat-chip-up' : 'pat-chip-down');
      badgeEl.innerHTML = (changeAbs >= 0 ? arrowUp : arrowDn) +
        '<span class="num" id="patrimonio-badge-abs"></span>';
    }

    var newAbsEl = document.getElementById('patrimonio-badge-abs');
    if (newAbsEl) {
      var sign = changeAbs >= 0 ? '+' : '';
      newAbsEl.textContent = sign + fmtBR(changeAbs);
    }

    if (badgePctEl) {
      var pctSign = changePct >= 0 ? '+' : '';
      badgePctEl.textContent = pctSign +
        Number(changePct).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '%';
    }

    if (periodLabelEl) {
      periodLabelEl.textContent = ' ' + (periodLabels[period] || '');
    }

    if (insightEl) {
      var direction = changeAbs >= 0 ? 'cresceu' : 'caiu';
      var absPctStr = Number(Math.abs(changePct)).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      insightEl.innerHTML = 'Seu patrimônio <b>' + direction + ' ' + absPctStr + '%</b>' +
        ' ' + (periodLabels[period] || '') +
        ' — variação de <b>' + (changeAbs >= 0 ? '+' : '') + fmtBR(changeAbs) + '</b>.';
    }
  }

  // ── Crosshair interaction ──────────────────────────────────────────
  function initCrosshair(getPoints) {
    var wrap      = document.getElementById('patChartWrap');
    var crosshair = document.getElementById('patCrosshair');
    var hoverDot  = document.getElementById('patHoverDot');
    var tooltip   = document.getElementById('patTooltip');
    if (!wrap || !crosshair || !hoverDot || !tooltip) return;

    var ttDate  = tooltip.querySelector('.pat-tt-date');
    var ttValue = tooltip.querySelector('.pat-tt-value');

    function onMove(clientX) {
      var pts = getPoints();
      if (pts.length === 0) return;
      var rect = wrap.getBoundingClientRect();
      var xPx  = clientX - rect.left;
      var vbX  = (xPx / rect.width) * W;

      var nearest = pts[0], minD = Infinity;
      pts.forEach(function (p) {
        var d = Math.abs(p.x - vbX);
        if (d < minD) { minD = d; nearest = p; }
      });

      var pxX = (nearest.x / W) * rect.width;
      var pxY = (nearest.y / H) * rect.height;

      crosshair.style.left = pxX + 'px';
      hoverDot.style.left  = pxX + 'px';
      hoverDot.style.top   = pxY + 'px';
      tooltip.style.left   = pxX + 'px';
      tooltip.style.top    = pxY + 'px';

      if (ttDate)  ttDate.textContent  = nearest.date;
      if (ttValue) ttValue.textContent = fmtBR(nearest.value);
      wrap.classList.add('active');
    }

    wrap.addEventListener('mousemove', function (e) { onMove(e.clientX); });
    wrap.addEventListener('mouseleave', function () { wrap.classList.remove('active'); });
    wrap.addEventListener('touchmove', function (e) {
      e.preventDefault();
      onMove(e.touches[0].clientX);
    }, { passive: false });
    wrap.addEventListener('touchend', function () { wrap.classList.remove('active'); });
  }

  // ── Period pills ───────────────────────────────────────────────────
  function initPeriodPills(onPeriodChange) {
    var pills = document.querySelectorAll('.pat-period-btn');
    pills.forEach(function (btn) {
      btn.addEventListener('click', function () {
        pills.forEach(function (b) {
          b.classList.remove('active');
          b.setAttribute('aria-selected', 'false');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');
        onPeriodChange(btn.dataset.period);
      });
    });
  }

  // ── Bootstrap ─────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    var svgEl   = document.getElementById('patrimonio-chart');
    var dataEl  = document.getElementById('patrimonio-data');
    var wrap    = document.getElementById('patChartWrap');
    if (!svgEl || !dataEl) return;

    var initialData  = JSON.parse(dataEl.textContent);
    var currentPts   = [];

    updatePatStats(initialData);
    currentPts = drawChart(svgEl, initialData.series);

    initCrosshair(function () { return currentPts; });

    initPeriodPills(function (period) {
      if (wrap) wrap.classList.add('pat-loading');

      fetch('/dashboard/api/patrimonio/?period=' + period)
        .then(function (resp) {
          if (resp.redirected) { window.location = resp.url; return null; }
          if (!resp.ok) throw new Error('HTTP ' + resp.status);
          return resp.json();
        })
        .then(function (data) {
          if (!data) return;
          updatePatStats(data);
          currentPts = drawChart(svgEl, data.series);
        })
        .catch(function () {
          // keep existing chart on error — no silent failure for debugging
          console.warn('[patrimonio] falha ao buscar período');
        })
        .finally(function () {
          if (wrap) wrap.classList.remove('pat-loading');
        });
    });
  });

})();
