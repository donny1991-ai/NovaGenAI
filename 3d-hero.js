/**
 * NovaGenAI — 3D Particle Constellation Hero
 * Three.js particle field with mouse parallax, constellation lines,
 * scroll animations, and custom cursor glow.
 */
(function () {
  'use strict';

  const isMobile = window.innerWidth < 768;

  // ─── CUSTOM CURSOR ───────────────────────────────────
  if (!isMobile) {
    const cursor = document.createElement('div');
    cursor.className = 'nova-cursor';
    const cursorDot = document.createElement('div');
    cursorDot.className = 'nova-cursor__dot';
    document.body.appendChild(cursor);
    document.body.appendChild(cursorDot);

    let mx = -100, my = -100, cx = -100, cy = -100, dx = -100, dy = -100;

    document.addEventListener('mousemove', function (e) {
      mx = e.clientX;
      my = e.clientY;
    });

    (function animateCursor() {
      cx += (mx - cx) * 0.08;
      cy += (my - cy) * 0.08;
      dx += (mx - dx) * 0.25;
      dy += (my - dy) * 0.25;
      cursor.style.transform = 'translate(' + cx + 'px,' + cy + 'px)';
      cursorDot.style.transform = 'translate(' + dx + 'px,' + dy + 'px)';
      requestAnimationFrame(animateCursor);
    })();

    // Cursor hover state on interactive elements
    document.addEventListener('mouseover', function (e) {
      if (e.target.closest('a, button, [onclick], input, textarea, select, .nav__dropdown')) {
        cursor.classList.add('nova-cursor--hover');
      }
    });
    document.addEventListener('mouseout', function (e) {
      if (e.target.closest('a, button, [onclick], input, textarea, select, .nav__dropdown')) {
        cursor.classList.remove('nova-cursor--hover');
      }
    });
  }

  // ─── SCROLL ANIMATIONS (IntersectionObserver) ────────
  function initScrollAnimations() {
    var els = document.querySelectorAll('.fade-up, .eco, .ag-section, .solutions, .testimonials, .contact, .faq, .team-built-card, .team-eng-featured');
    if (!els.length) return;

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('nova-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    els.forEach(function (el) {
      el.classList.add('nova-animate');
      observer.observe(el);
    });
  }

  // ─── HERO TEXT ENTRANCE ──────────────────────────────
  function initHeroEntrance() {
    var headline = document.querySelector('.hero__headline');
    var subcopy = document.querySelector('.hero__subcopy');
    var status = document.querySelector('.hero__status');

    if (headline) headline.classList.add('nova-hero-enter');
    if (subcopy) subcopy.classList.add('nova-hero-enter', 'nova-hero-enter--delay');
    if (status) status.classList.add('nova-hero-enter', 'nova-hero-enter--delay2');

    requestAnimationFrame(function () {
      setTimeout(function () {
        if (headline) headline.classList.add('nova-hero-enter--active');
        if (subcopy) subcopy.classList.add('nova-hero-enter--active');
        if (status) status.classList.add('nova-hero-enter--active');
      }, 100);
    });
  }

  // ─── THREE.JS PARTICLE CONSTELLATION ─────────────────
  function initParticles() {
    if (isMobile) return;
    if (typeof THREE === 'undefined') return;

    var container = document.getElementById('nova-3d-canvas');
    if (!container) return;

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 50;

    var renderer = new THREE.WebGLRenderer({ alpha: true, antialias: false });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x000000, 0);
    container.appendChild(renderer.domElement);

    // Particle system
    var PARTICLE_COUNT = 400;
    var positions = new Float32Array(PARTICLE_COUNT * 3);
    var colors = new Float32Array(PARTICLE_COUNT * 3);
    var sizes = new Float32Array(PARTICLE_COUNT);
    var velocities = [];

    var cyanR = 0 / 255, cyanG = 212 / 255, cyanB = 255 / 255;
    var goldR = 212 / 255, goldG = 160 / 255, goldB = 23 / 255;

    for (var i = 0; i < PARTICLE_COUNT; i++) {
      var i3 = i * 3;
      positions[i3] = (Math.random() - 0.5) * 120;
      positions[i3 + 1] = (Math.random() - 0.5) * 80;
      positions[i3 + 2] = (Math.random() - 0.5) * 60;

      // 75% cyan, 25% gold
      if (Math.random() > 0.25) {
        colors[i3] = cyanR;
        colors[i3 + 1] = cyanG;
        colors[i3 + 2] = cyanB;
      } else {
        colors[i3] = goldR;
        colors[i3 + 1] = goldG;
        colors[i3 + 2] = goldB;
      }

      sizes[i] = Math.random() * 2.5 + 0.5;
      velocities.push({
        x: (Math.random() - 0.5) * 0.02,
        y: (Math.random() - 0.5) * 0.02,
        z: (Math.random() - 0.5) * 0.01
      });
    }

    var particleGeometry = new THREE.BufferGeometry();
    particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particleGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    particleGeometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

    // Custom shader material for glow particles
    var particleMaterial = new THREE.ShaderMaterial({
      uniforms: {
        uPixelRatio: { value: Math.min(window.devicePixelRatio, 2) }
      },
      vertexShader: [
        'attribute float size;',
        'varying vec3 vColor;',
        'uniform float uPixelRatio;',
        'void main() {',
        '  vColor = color;',
        '  vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);',
        '  gl_PointSize = size * uPixelRatio * (80.0 / -mvPosition.z);',
        '  gl_Position = projectionMatrix * mvPosition;',
        '}'
      ].join('\n'),
      fragmentShader: [
        'varying vec3 vColor;',
        'void main() {',
        '  float d = length(gl_PointCoord - vec2(0.5));',
        '  if (d > 0.5) discard;',
        '  float alpha = 1.0 - smoothstep(0.0, 0.5, d);',
        '  alpha *= 0.7;',
        '  gl_FragColor = vec4(vColor, alpha);',
        '}'
      ].join('\n'),
      transparent: true,
      vertexColors: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending
    });

    var particles = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particles);

    // Constellation lines
    var LINE_DISTANCE = 12;
    var MAX_LINES = 150;
    var linePositions = new Float32Array(MAX_LINES * 6);
    var lineColors = new Float32Array(MAX_LINES * 6);
    var lineGeometry = new THREE.BufferGeometry();
    lineGeometry.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
    lineGeometry.setAttribute('color', new THREE.BufferAttribute(lineColors, 3));
    lineGeometry.setDrawRange(0, 0);

    var lineMaterial = new THREE.LineBasicMaterial({
      vertexColors: true,
      transparent: true,
      opacity: 0.15,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });
    var lines = new THREE.LineSegments(lineGeometry, lineMaterial);
    scene.add(lines);

    // Mouse tracking
    var mouse = { x: 0, y: 0, targetX: 0, targetY: 0 };
    document.addEventListener('mousemove', function (e) {
      mouse.targetX = (e.clientX / window.innerWidth - 0.5) * 2;
      mouse.targetY = -(e.clientY / window.innerHeight - 0.5) * 2;
    });

    // Scroll offset for parallax
    var scrollY = 0;
    window.addEventListener('scroll', function () {
      scrollY = window.pageYOffset;
    });

    // Resize handler
    window.addEventListener('resize', function () {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // ─── RENDER LOOP ──────
    var clock = new THREE.Clock();

    function animate() {
      requestAnimationFrame(animate);

      var delta = clock.getDelta();
      var elapsed = clock.getElapsedTime();

      // Smooth mouse lerp
      mouse.x += (mouse.targetX - mouse.x) * 0.05;
      mouse.y += (mouse.targetY - mouse.y) * 0.05;

      // Update particle positions
      var pos = particleGeometry.attributes.position.array;
      for (var i = 0; i < PARTICLE_COUNT; i++) {
        var i3 = i * 3;
        pos[i3] += velocities[i].x;
        pos[i3 + 1] += velocities[i].y;
        pos[i3 + 2] += velocities[i].z;

        // Wrap around
        if (pos[i3] > 60) pos[i3] = -60;
        if (pos[i3] < -60) pos[i3] = 60;
        if (pos[i3 + 1] > 40) pos[i3 + 1] = -40;
        if (pos[i3 + 1] < -40) pos[i3 + 1] = 40;
      }
      particleGeometry.attributes.position.needsUpdate = true;

      // Mouse parallax on camera
      camera.position.x += (mouse.x * 8 - camera.position.x) * 0.03;
      camera.position.y += (mouse.y * 5 + scrollY * -0.01 - camera.position.y) * 0.03;
      camera.lookAt(0, 0, 0);

      // Subtle rotation
      particles.rotation.y = elapsed * 0.02;
      particles.rotation.x = Math.sin(elapsed * 0.01) * 0.1;

      // Update constellation lines (check nearby pairs)
      var lineCount = 0;
      var lp = lineGeometry.attributes.position.array;
      var lc = lineGeometry.attributes.color.array;

      for (var a = 0; a < PARTICLE_COUNT && lineCount < MAX_LINES; a++) {
        var a3 = a * 3;
        for (var b = a + 1; b < PARTICLE_COUNT && lineCount < MAX_LINES; b++) {
          var b3 = b * 3;
          var dx = pos[a3] - pos[b3];
          var dy = pos[a3 + 1] - pos[b3 + 1];
          var dz = pos[a3 + 2] - pos[b3 + 2];
          var dist = dx * dx + dy * dy + dz * dz;
          if (dist < LINE_DISTANCE * LINE_DISTANCE) {
            var idx = lineCount * 6;
            lp[idx] = pos[a3]; lp[idx + 1] = pos[a3 + 1]; lp[idx + 2] = pos[a3 + 2];
            lp[idx + 3] = pos[b3]; lp[idx + 4] = pos[b3 + 1]; lp[idx + 5] = pos[b3 + 2];
            // Use color of first particle
            var ca3 = a * 3;
            lc[idx] = colors[ca3]; lc[idx + 1] = colors[ca3 + 1]; lc[idx + 2] = colors[ca3 + 2];
            lc[idx + 3] = colors[ca3]; lc[idx + 4] = colors[ca3 + 1]; lc[idx + 5] = colors[ca3 + 2];
            lineCount++;
          }
        }
      }
      lineGeometry.setDrawRange(0, lineCount * 2);
      lineGeometry.attributes.position.needsUpdate = true;
      lineGeometry.attributes.color.needsUpdate = true;

      renderer.render(scene, camera);
    }

    animate();

    // Cleanup on reduced motion
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      renderer.dispose();
      container.innerHTML = '';
    }
  }

  // ─── INIT ────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    initHeroEntrance();
    initScrollAnimations();
    initParticles();
  });
})();
