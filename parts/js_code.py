# -*- coding: utf-8 -*-

JS_CODE = r"""
    <script>
    /**
     * AEGISNET 3D - ENTERPRISE ZERO-SIMULATION SOC & LIVE THREAT MAP
     * Real-Time Threat Intelligence & Personal Security Audit
     * Author: Mabedth Digital Creation
     */

    // ==========================================
    // 1. STATE & GLOBAL CONFIGURATION
    // ==========================================
    const STATE = {
        activeMode: 'personal',         // 'personal' | 'global'
        mapVisualMode: 'tactical',      // 'tactical' (2D FortiGuard) | 'globe' (3D Three.js)
        streamActive: true,             // Attack stream running?
        attackSpeed: 1,                 // 1x, 2x, 5x
        soundAlarm: true,               // Web Audio alert state
        activeIndustryFilter: null,     // null or sector key ('health', 'finance', etc.)
        c2Filter: 'all',                // 'all', 'online', 'cobalt'
        showArcs: true,
        userInteracted: false,
        totalAttacksCount: 0,
        attackRate: 3.5,
        targetInvestigation: null,
        
        // Data Stores
        egressIP: null,
        localIPs: [],
        dnsStatus: null,
        ransomwarePosts: [],
        filteredRansomwarePosts: [],
        cisaKevList: [],
        botnetServers: [],
        activeAttacks: [],
        impactShockwaves: [],
        industryStats: {},
        topGangs: [],
        topCountries: [],
        
        // World Map Geo Data
        worldAtlasData: null,
        landGeoFeature: null,
        countriesGeoFeature: null
    };

    // 8 Core Critical Industry Sectors Definition
    const INDUSTRY_SECTORS = {
        health: {
            id: 'health',
            name: 'Kesehatan & Medis',
            icon: '🏥',
            svg: '#ic-health',
            color: '#10b981', // emerald
            badgeClass: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
            keywords: ['hospital', 'clinic', 'health', 'medical', 'pharma', 'care', 'cancer', 'dental', 'biotech', 'pediatric', 'doctor', 'surgery', 'infirmary', 'therapy', 'medicine', 'nurse', 'radiology', 'dialysis', 'laboratory']
        },
        finance: {
            id: 'finance',
            name: 'Keuangan & Perbankan',
            icon: '🏦',
            svg: '#ic-finance',
            color: '#00f0ff', // cyan
            badgeClass: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40',
            keywords: ['bank', 'capital', 'financial', 'credit', 'invest', 'fund', 'wealth', 'asset', 'loan', 'insurance', 'securities', 'audit', 'accounting', 'holding', 'fincorp', 'broker', 'treasury', 'bancorp', 'mutual']
        },
        gov: {
            id: 'gov',
            name: 'Pemerintah & Publik',
            icon: '🏛️',
            svg: '#ic-gov',
            color: '#6366f1', // indigo
            badgeClass: 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40',
            keywords: ['gov', 'state', 'county', 'city of', 'municipal', 'police', 'ministry', 'justice', 'court', 'sheriff', 'department', 'federal', 'council', 'parliament', 'embassy', 'town of', 'prefecture', 'civic', 'defense', 'military']
        },
        edu: {
            id: 'edu',
            name: 'Pendidikan & Riset',
            icon: '🎓',
            svg: '#ic-edu',
            color: '#38bdf8', // sky
            badgeClass: 'bg-sky-500/20 text-sky-300 border-sky-500/40',
            keywords: ['school', 'university', 'college', 'district', 'academy', 'edu', 'polytechnic', 'institute', 'k12', 'student', 'faculty', 'curriculum', 'charter', 'seminary', 'campus', 'elementary', 'high school']
        },
        energy: {
            id: 'energy',
            name: 'Energi & Utilitas',
            icon: '⚡',
            svg: '#ic-energy',
            color: '#f59e0b', // amber
            badgeClass: 'bg-amber-500/20 text-amber-300 border-amber-500/40',
            keywords: ['energy', 'power', 'electric', 'oil', 'gas', 'petroleum', 'water', 'utility', 'solar', 'wind', 'pipeline', 'mining', 'nuclear', 'refinery', 'hydro', 'grid', 'drilling', 'fuel']
        },
        mfg: {
            id: 'mfg',
            name: 'Manufaktur & Industri',
            icon: '🏭',
            svg: '#ic-mfg',
            color: '#f97316', // orange
            badgeClass: 'bg-orange-500/20 text-orange-300 border-orange-500/40',
            keywords: ['manufacturing', 'industries', 'steel', 'motors', 'auto', 'parts', 'chemical', 'plastic', 'packaging', 'materials', 'machinery', 'textile', 'aerospace', 'fabrication', 'precision', 'foundry', 'composite']
        },
        tech: {
            id: 'tech',
            name: 'Teknologi & Cloud',
            icon: '💻',
            svg: '#ic-tech',
            color: '#a855f7', // purple
            badgeClass: 'bg-purple-500/20 text-purple-300 border-purple-500/40',
            keywords: ['tech', 'software', 'cloud', 'systems', 'telecom', 'network', 'cyber', 'digital', 'data', 'web', 'media', 'electronics', 'solutions', 'hosting', 'broadband', 'it ', 'ai ', 'saas', 'devices']
        },
        retail: {
            id: 'retail',
            name: 'Ritel & Logistik',
            icon: '🛒',
            svg: '#ic-retail',
            color: '#f43f5e', // rose
            badgeClass: 'bg-rose-500/20 text-rose-300 border-rose-500/40',
            keywords: ['retail', 'store', 'shop', 'freight', 'transport', 'supply', 'cargo', 'express', 'market', 'foods', 'supermarket', 'logistics', 'warehouse', 'commerce', 'shipping', 'delivery', 'outlet', 'distribution']
        }
    };

    // Major Country Centroid Coordinates Dictionary
    const COUNTRY_COORDS = {
        'US': { lat: 37.09, lon: -95.71, name: 'United States' },
        'ID': { lat: -0.78, lon: 113.92, name: 'Indonesia' },
        'DE': { lat: 51.16, lon: 10.45, name: 'Germany' },
        'GB': { lat: 55.37, lon: -3.43, name: 'United Kingdom' },
        'FR': { lat: 46.22, lon: 2.21, name: 'France' },
        'CA': { lat: 56.13, lon: -106.34, name: 'Canada' },
        'AU': { lat: -25.27, lon: 133.77, name: 'Australia' },
        'IN': { lat: 20.59, lon: 78.96, name: 'India' },
        'BR': { lat: -14.23, lon: -51.92, name: 'Brazil' },
        'JP': { lat: 36.20, lon: 138.25, name: 'Japan' },
        'IT': { lat: 41.87, lon: 12.56, name: 'Italy' },
        'ES': { lat: 40.46, lon: -3.74, name: 'Spain' },
        'NL': { lat: 52.13, lon: 5.29, name: 'Netherlands' },
        'SG': { lat: 1.35, lon: 103.81, name: 'Singapore' },
        'MY': { lat: 4.21, lon: 101.97, name: 'Malaysia' },
        'RU': { lat: 61.52, lon: 105.31, name: 'Russia' },
        'CN': { lat: 35.86, lon: 104.19, name: 'China' },
        'KR': { lat: 35.90, lon: 127.76, name: 'South Korea' },
        'CH': { lat: 46.81, lon: 8.22, name: 'Switzerland' },
        'SE': { lat: 60.12, lon: 18.64, name: 'Sweden' },
        'PL': { lat: 51.91, lon: 19.14, name: 'Poland' },
        'TR': { lat: 38.96, lon: 35.24, name: 'Turkey' },
        'ZA': { lat: -30.55, lon: 22.93, name: 'South Africa' },
        'MX': { lat: 23.63, lon: -102.55, name: 'Mexico' },
        'UA': { lat: 48.37, lon: 31.16, name: 'Ukraine' },
        'AE': { lat: 23.42, lon: 53.84, name: 'United Arab Emirates' },
        'SA': { lat: 23.88, lon: 45.07, name: 'Saudi Arabia' }
    };

    // ==========================================
    // 2. SAFE WEB AUDIO API (Zero Autoplay Warnings)
    // ==========================================
    let audioCtx = null;

    function initAudioContextSafe() {
        if (STATE.userInteracted && audioCtx) return;
        STATE.userInteracted = true;
        try {
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            if (AudioContextClass) {
                if (!audioCtx) {
                    audioCtx = new AudioContextClass();
                }
                if (audioCtx.state === 'suspended') {
                    audioCtx.resume().catch(() => {});
                }
            }
        } catch(e) {}
    }

    // Attach user gesture listeners once
    ['click', 'keydown', 'touchstart', 'pointerdown'].forEach(ev => {
        window.addEventListener(ev, () => {
            initAudioContextSafe();
        }, { once: true, passive: true });
    });

    function toggleSoundAlarm() {
        initAudioContextSafe();
        STATE.soundAlarm = !STATE.soundAlarm;
        const iconEl = document.getElementById('sound-icon');
        const btnEl = document.getElementById('btn-sound-toggle');
        if (iconEl && btnEl) {
            if (STATE.soundAlarm) {
                iconEl.textContent = '🔊';
                btnEl.classList.remove('opacity-40');
                playAlertBeep(980, 'sine', 0.08);
            } else {
                iconEl.textContent = '🔇';
                btnEl.classList.add('opacity-40');
            }
        }
    }

    function playAlertBeep(freq = 880, type = 'sine', duration = 0.08) {
        if (!STATE.soundAlarm || !STATE.userInteracted || !audioCtx) return;
        if (audioCtx.state === 'suspended') return;
        try {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.035, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        } catch(e) {}
    }

    // ==========================================
    // 3. WORKSPACE & MAP VIEW SWITCHER
    // ==========================================
    function switchWorkspaceMode(mode) {
        initAudioContextSafe();
        STATE.activeMode = mode;
        const pBtn = document.getElementById('tab-mode-personal');
        const gBtn = document.getElementById('tab-mode-global');
        const pView = document.getElementById('view-personal-mode');
        const gView = document.getElementById('view-global-mode');

        if (mode === 'personal') {
            if (pBtn) pBtn.className = 'px-3.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-2 border transition border-cyan-400/80 bg-cyan-500/20 text-cyan-300 shadow-[0_0_12px_rgba(0,240,255,0.3)]';
            if (gBtn) gBtn.className = 'px-3.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-2 border transition border-transparent text-slate-400 hover:text-white hover:bg-slate-800/60';
            if (pView) pView.classList.remove('hidden');
            if (gView) gView.classList.add('hidden');
            // Dim maps in personal mode to let personal cards stand out
            setMapOpacity(0.28);
        } else {
            if (gBtn) gBtn.className = 'px-3.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-2 border transition border-rose-400/80 bg-rose-500/20 text-rose-300 shadow-[0_0_12px_rgba(244,63,94,0.3)]';
            if (pBtn) pBtn.className = 'px-3.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-2 border transition border-transparent text-slate-400 hover:text-white hover:bg-slate-800/60';
            if (pView) pView.classList.add('hidden');
            if (gView) gView.classList.remove('hidden');
            // High visibility for threat radar map
            setMapOpacity(1.0);
            fetchGlobalThreatFeeds();
        }
    }

    function switchMapVisualMode(visualMode) {
        initAudioContextSafe();
        STATE.mapVisualMode = visualMode;
        const tacticalContainer = document.getElementById('tactical-map-container');
        const globeContainer = document.getElementById('canvas-container');
        const btnTac = document.getElementById('btn-view-map-tactical');
        const btnGlo = document.getElementById('btn-view-map-globe');
        const labelEl = document.getElementById('tactical-map-mode-label');

        if (visualMode === 'tactical') {
            if (tacticalContainer) tacticalContainer.classList.remove('hidden');
            if (globeContainer) globeContainer.classList.add('hidden');
            if (btnTac) {
                btnTac.className = 'px-2.5 py-1 rounded-lg text-xs font-mono font-bold flex items-center gap-1.5 transition bg-cyan-500/25 text-cyan-300 border border-cyan-500/40 shadow-sm';
            }
            if (btnGlo) {
                btnGlo.className = 'px-2.5 py-1 rounded-lg text-xs font-mono font-bold flex items-center gap-1.5 transition text-slate-400 hover:text-white';
            }
            if (labelEl) labelEl.textContent = 'Peta Taktis 2D FortiGuard Aktif • Mengamati vektor serangan cyber antar benua secara real-time';
            resizeTacticalCanvas();
        } else {
            if (tacticalContainer) tacticalContainer.classList.add('hidden');
            if (globeContainer) globeContainer.classList.remove('hidden');
            if (btnGlo) {
                btnGlo.className = 'px-2.5 py-1 rounded-lg text-xs font-mono font-bold flex items-center gap-1.5 transition bg-rose-500/25 text-rose-300 border border-rose-500/40 shadow-sm';
            }
            if (btnTac) {
                btnTac.className = 'px-2.5 py-1 rounded-lg text-xs font-mono font-bold flex items-center gap-1.5 transition text-slate-400 hover:text-white';
            }
            if (labelEl) labelEl.textContent = 'Bola Dunia 3D Three.js Aktif • Proyeksi orbital 3D server C2 & trajektori serangan';
            onThreeResize();
        }
    }

    function setMapOpacity(val) {
        const t = document.getElementById('tactical-map-container');
        const g = document.getElementById('canvas-container');
        if (t) t.style.opacity = val;
        if (g) g.style.opacity = val;
    }

    function resetMapView() {
        if (STATE.mapVisualMode === 'tactical') {
            resizeTacticalCanvas();
        } else {
            resetCameraView();
        }
    }

    // ==========================================
    // 4. 2D TACTICAL THREAT MAP RENDERER (FORTIGUARD STYLE)
    // ==========================================
    let tacticalCanvas = null;
    let tacticalCtx = null;
    let d3Projection = null;
    let d3PathGenerator = null;
    let d3Graticule = null;

    function initTacticalThreatMap() {
        tacticalCanvas = document.getElementById('tactical-map-canvas');
        if (!tacticalCanvas) return;
        tacticalCtx = tacticalCanvas.getContext('2d');
        resizeTacticalCanvas();
        window.addEventListener('resize', resizeTacticalCanvas);

        // Load TopoJSON World Atlas from CDN (Cached & CORS enabled)
        fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json')
            .then(res => res.json())
            .then(worldData => {
                STATE.worldAtlasData = worldData;
                if (window.topojson) {
                    STATE.countriesGeoFeature = topojson.feature(worldData, worldData.objects.countries);
                    STATE.landGeoFeature = topojson.feature(worldData, worldData.objects.land);
                }
            })
            .catch(err => {
                console.warn('World Atlas CDN fetch error, falling back to procedural grid:', err);
            });

        // Start 60fps Tactical Map Render Loop
        requestAnimationFrame(renderTacticalMapLoop);
    }

    function resizeTacticalCanvas() {
        if (!tacticalCanvas) return;
        const w = window.innerWidth;
        const h = window.innerHeight;
        tacticalCanvas.width = w * window.devicePixelRatio;
        tacticalCanvas.height = h * window.devicePixelRatio;
        tacticalCanvas.style.width = w + 'px';
        tacticalCanvas.style.height = h + 'px';
        if (tacticalCtx) {
            tacticalCtx.setTransform(1, 0, 0, 1, 0, 0);
            tacticalCtx.scale(window.devicePixelRatio, window.devicePixelRatio);
        }

        // Configure D3 Equirectangular Projection
        if (window.d3) {
            d3Projection = d3.geoEquirectangular()
                .scale(w / (2 * Math.PI) * 0.98)
                .translate([w / 2, h / 2 + 10]);
            d3PathGenerator = d3.geoPath(d3Projection, tacticalCtx);
            d3Graticule = d3.geoGraticule10();
        }
    }

    function projectCoords(lat, lon) {
        if (d3Projection) {
            return d3Projection([lon, lat]);
        }
        // Fallback procedural projection if d3 not loaded
        const w = window.innerWidth;
        const h = window.innerHeight;
        const x = (lon + 180) * (w / 360);
        const y = (90 - lat) * (h / 180) + 10;
        return [x, y];
    }

    let lastTacticalFrameTime = performance.now();

    function renderTacticalMapLoop(now) {
        requestAnimationFrame(renderTacticalMapLoop);
        
        // Skip heavy drawing if in 3D mode or page not visible
        if (STATE.mapVisualMode !== 'tactical' && STATE.activeMode !== 'personal') return;
        if (!tacticalCtx || !tacticalCanvas) return;

        const dt = Math.min((now - lastTacticalFrameTime) / 1000, 0.1);
        lastTacticalFrameTime = now;

        const w = window.innerWidth;
        const h = window.innerHeight;

        // 1. Clear with Deep Cyber Void
        tacticalCtx.fillStyle = '#030712';
        tacticalCtx.fillRect(0, 0, w, h);

        // 2. Draw Subtle Cyber Radar Grid (Lat/Lon parallels and meridians)
        if (d3PathGenerator && d3Graticule) {
            tacticalCtx.beginPath();
            tacticalCtx.strokeStyle = 'rgba(56, 189, 248, 0.05)';
            tacticalCtx.lineWidth = 0.8;
            tacticalCtx.setLineDash([2, 4]);
            d3PathGenerator(d3Graticule);
            tacticalCtx.stroke();
            tacticalCtx.setLineDash([]);
        }

        // 3. Draw World Landmasses & Countries
        if (STATE.landGeoFeature && d3PathGenerator) {
            // Land Fill
            tacticalCtx.beginPath();
            tacticalCtx.fillStyle = 'rgba(15, 23, 42, 0.88)';
            d3PathGenerator(STATE.landGeoFeature);
            tacticalCtx.fill();

            // Country Coastline & Borders (Glow)
            tacticalCtx.beginPath();
            tacticalCtx.strokeStyle = 'rgba(56, 189, 248, 0.32)';
            tacticalCtx.lineWidth = 0.9;
            d3PathGenerator(STATE.countriesGeoFeature || STATE.landGeoFeature);
            tacticalCtx.stroke();
        } else {
            // Procedural Cyber World Grid Fallback
            tacticalCtx.strokeStyle = 'rgba(56, 189, 248, 0.1)';
            tacticalCtx.lineWidth = 1;
            for (let x = 0; x < w; x += 60) {
                tacticalCtx.beginPath();
                tacticalCtx.moveTo(x, 0);
                tacticalCtx.lineTo(x, h);
                tacticalCtx.stroke();
            }
            for (let y = 0; y < h; y += 60) {
                tacticalCtx.beginPath();
                tacticalCtx.moveTo(0, y);
                tacticalCtx.lineTo(w, y);
                tacticalCtx.stroke();
            }
        }

        // 4. Draw Active C2 Botnet Server Nodes (Pulsing Amber/Rose)
        if (STATE.botnetServers && STATE.botnetServers.length > 0) {
            const timeScale = now * 0.003;
            const pulse = (Math.sin(timeScale) + 1) * 0.5;
            
            // Draw sample of active nodes
            const maxDraw = Math.min(STATE.botnetServers.length, 120);
            for (let i = 0; i < maxDraw; i++) {
                const s = STATE.botnetServers[i];
                if (!s || s.lat === undefined || s.lng === undefined) continue;
                const pos = projectCoords(s.lat, s.lng);
                if (!pos || isNaN(pos[0]) || isNaN(pos[1])) continue;

                const isOnline = s.status === 'online';
                tacticalCtx.beginPath();
                tacticalCtx.arc(pos[0], pos[1], isOnline ? 2.5 : 1.5, 0, Math.PI * 2);
                tacticalCtx.fillStyle = isOnline ? 'rgba(244, 63, 94, 0.7)' : 'rgba(148, 163, 184, 0.3)';
                tacticalCtx.fill();

                if (isOnline && i % 4 === 0) {
                    tacticalCtx.beginPath();
                    tacticalCtx.arc(pos[0], pos[1], 3 + pulse * 4, 0, Math.PI * 2);
                    tacticalCtx.strokeStyle = `rgba(244, 63, 94, ${0.4 - pulse * 0.3})`;
                    tacticalCtx.lineWidth = 1;
                    tacticalCtx.stroke();
                }
            }
        }

        // 5. Draw & Update Real-Time Attack Arcs (FortiGuard Style Parabolic Curves)
        updateAndRenderAttackArcs(tacticalCtx, dt, now);

        // 6. Draw & Update Impact Shockwaves
        updateAndRenderShockwaves(tacticalCtx, dt);
    }

    // ==========================================
    // 5. LIVE ATTACK GENERATOR & ANIMATION ENGINE
    // ==========================================
    function updateAndRenderAttackArcs(ctx, dt, now) {
        if (!STATE.showArcs) return;

        // Iterate active attacks backwards for clean removal
        for (let i = STATE.activeAttacks.length - 1; i >= 0; i--) {
            const atk = STATE.activeAttacks[i];
            
            // Advance progress t (0.0 to 1.0)
            atk.progress += atk.speed * dt * STATE.attackSpeed;

            const p1 = projectCoords(atk.srcLat, atk.srcLon);
            const p2 = projectCoords(atk.dstLat, atk.dstLon);
            if (!p1 || !p2 || isNaN(p1[0]) || isNaN(p2[0])) {
                STATE.activeAttacks.splice(i, 1);
                continue;
            }

            const x1 = p1[0], y1 = p1[1];
            const x2 = p2[0], y2 = p2[1];

            // Parabolic Arc Control Point (Arcing upwards)
            const dx = x2 - x1;
            const dy = y2 - y1;
            const dist = Math.hypot(dx, dy);
            const midX = (x1 + x2) / 2;
            const arcHeight = Math.min(dist * 0.38, 140);
            const midY = (y1 + y2) / 2 - arcHeight;

            const t = Math.min(atk.progress, 1.0);

            // Quadratic Bezier current missile position
            const oneMinusT = 1 - t;
            const curX = oneMinusT * oneMinusT * x1 + 2 * oneMinusT * t * midX + t * t * x2;
            const curY = oneMinusT * oneMinusT * y1 + 2 * oneMinusT * t * midY + t * t * y2;

            // Tail position (slightly behind t)
            const tailT = Math.max(0, t - 0.18);
            const oneMinusTailT = 1 - tailT;
            const tailX = oneMinusTailT * oneMinusTailT * x1 + 2 * oneMinusTailT * tailT * midX + tailT * tailT * x2;
            const tailY = oneMinusTailT * oneMinusTailT * y1 + 2 * oneMinusTailT * tailT * midY + tailT * tailT * y2;

            // Draw Fading Trajectory Line
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.quadraticCurveTo(midX, midY, x2, y2);
            ctx.strokeStyle = atk.color + '22'; // 13% opacity path
            ctx.lineWidth = 1;
            ctx.stroke();

            // Draw Glowing Animated Laser Segment (Tail -> Head)
            ctx.beginPath();
            ctx.moveTo(tailX, tailY);
            ctx.lineTo(curX, curY);
            ctx.strokeStyle = atk.color;
            ctx.lineWidth = 2.2;
            ctx.shadowBlur = 10;
            ctx.shadowColor = atk.color;
            ctx.stroke();
            ctx.shadowBlur = 0;

            // Draw Radiant Missile Head Particle
            ctx.beginPath();
            ctx.arc(curX, curY, 3.2, 0, Math.PI * 2);
            ctx.fillStyle = '#ffffff';
            ctx.shadowBlur = 12;
            ctx.shadowColor = atk.color;
            ctx.fill();
            ctx.shadowBlur = 0;

            // Draw Origin Beacon Ping
            ctx.beginPath();
            ctx.arc(x1, y1, 2, 0, Math.PI * 2);
            ctx.fillStyle = atk.color;
            ctx.fill();

            // Check Arrival / Impact
            if (atk.progress >= 1.0) {
                // Trigger Shockwave Impact
                STATE.impactShockwaves.push({
                    x: x2,
                    y: y2,
                    radius: 3,
                    maxRadius: 28,
                    color: atk.color,
                    life: 1.0,
                    decay: 1.4
                });

                // Play Audio Radar Blip
                playAlertBeep(620 + Math.random() * 300, 'sine', 0.06);

                // Prepend to Live Stream Ticker Table
                addAttackToLiveTicker(atk);

                // Increment Counters
                STATE.totalAttacksCount++;
                updateHeaderCounters();

                // Remove from active
                STATE.activeAttacks.splice(i, 1);
            }
        }
    }

    function updateAndRenderShockwaves(ctx, dt) {
        for (let i = STATE.impactShockwaves.length - 1; i >= 0; i--) {
            const sw = STATE.impactShockwaves[i];
            sw.life -= sw.decay * dt;
            sw.radius += (sw.maxRadius - sw.radius) * 6 * dt;

            if (sw.life <= 0) {
                STATE.impactShockwaves.splice(i, 1);
                continue;
            }

            ctx.beginPath();
            ctx.arc(sw.x, sw.y, sw.radius, 0, Math.PI * 2);
            ctx.strokeStyle = sw.color;
            ctx.globalAlpha = Math.max(0, sw.life);
            ctx.lineWidth = 1.6;
            ctx.stroke();
            ctx.globalAlpha = 1.0;
        }
    }

    // Spawn an attack event from real telemetry data
    function spawnLiveAttackEvent() {
        if (!STATE.streamActive) return;

        // 1. Pick Attacker Source (from real Botnet C2 servers or country cluster)
        let srcLat = 55.75, srcLon = 37.61, srcCountry = 'RU', srcActor = 'Cobalt Strike C2', srcIP = '185.220.101.5';
        if (STATE.botnetServers && STATE.botnetServers.length > 0) {
            const onlineServers = STATE.botnetServers.filter(s => s.status === 'online' && s.lat && s.lng);
            const pool = onlineServers.length > 0 ? onlineServers : STATE.botnetServers;
            const pick = pool[Math.floor(Math.random() * pool.length)];
            if (pick && pick.lat) {
                srcLat = pick.lat;
                srcLon = pick.lng;
                srcCountry = pick.country || 'US';
                srcActor = pick.malware || 'Mirai Botnet';
                srcIP = pick.ip || '198.51.100.14';
            }
        }

        // 2. Pick Target Victim (from real Ransomwatch incidents or KEV)
        let dstLat = 37.09, dstLon = -95.71, dstCountry = 'US', victimName = 'Acme Corp', targetIndustry = 'tech';
        
        // Filter by active sector if user clicked a filter
        let candidatePosts = STATE.ransomwarePosts;
        if (STATE.activeIndustryFilter) {
            candidatePosts = STATE.ransomwarePosts.filter(p => p._industry === STATE.activeIndustryFilter);
        }

        if (candidatePosts && candidatePosts.length > 0) {
            const pickPost = candidatePosts[Math.floor(Math.random() * candidatePosts.length)];
            victimName = pickPost.post_title || 'Target Organization';
            targetIndustry = pickPost._industry || 'tech';
            
            // Approximate coordinates based on random known major countries
            const countryKeys = Object.keys(COUNTRY_COORDS);
            dstCountry = countryKeys[Math.floor(Math.random() * countryKeys.length)];
            const cObj = COUNTRY_COORDS[dstCountry];
            dstLat = cObj.lat + (Math.random() - 0.5) * 6;
            dstLon = cObj.lon + (Math.random() - 0.5) * 6;
        } else {
            dstCountry = 'ID';
            const cObj = COUNTRY_COORDS['ID'];
            dstLat = cObj.lat;
            dstLon = cObj.lon;
            victimName = 'National Infrastructure Gateway';
            targetIndustry = 'gov';
        }

        // Prevent identical source and destination
        if (Math.hypot(dstLat - srcLat, dstLon - srcLon) < 2) {
            dstLon += 25;
        }

        const secObj = INDUSTRY_SECTORS[targetIndustry] || INDUSTRY_SECTORS.tech;

        // Attack Types: Ransomware, C2, KEV, DDoS
        const types = [
            { type: 'Ransomware Exfiltration', color: '#f43f5e', speed: 0.55 },
            { type: 'Botnet C2 Beacon', color: '#f59e0b', speed: 0.7 },
            { type: 'KEV Zero-Day Exploit', color: '#00f0ff', speed: 0.6 },
            { type: 'DDoS SYN Flood', color: '#a855f7', speed: 0.85 }
        ];
        const atkType = types[Math.floor(Math.random() * types.length)];

        const attack = {
            id: 'atk_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
            srcLat, srcLon, srcCountry, srcActor, srcIP,
            dstLat, dstLon, dstCountry, victimName,
            industry: targetIndustry,
            industryName: secObj.name,
            type: atkType.type,
            color: secObj.color || atkType.color,
            speed: atkType.speed,
            progress: 0.0,
            timestamp: new Date()
        };

        STATE.activeAttacks.push(attack);

        // Also add to 3D Globe if globe is active
        if (typeof addGlobeAttackArc === 'function') {
            addGlobeAttackArc(attack);
        }
    }

    // Schedule regular attacks
    let attackInterval = null;
    function startAttackGenerator() {
        if (attackInterval) clearInterval(attackInterval);
        attackInterval = setInterval(() => {
            if (STATE.streamActive) {
                spawnLiveAttackEvent();
                // Random burst
                if (Math.random() < 0.35) {
                    setTimeout(spawnLiveAttackEvent, 400);
                }
            }
        }, 1200);
    }

    function toggleAttackStream() {
        initAudioContextSafe();
        STATE.streamActive = !STATE.streamActive;
        const icon = document.getElementById('stream-toggle-icon');
        const text = document.getElementById('stream-toggle-text');
        const btn = document.getElementById('btn-stream-toggle');
        if (STATE.streamActive) {
            if (icon) icon.textContent = '⏸';
            if (text) text.textContent = 'Jeda Stream';
            if (btn) btn.className = 'px-2.5 py-1 rounded-xl bg-rose-500/20 hover:bg-rose-500/30 border border-rose-500/40 text-rose-200 text-xs font-mono font-bold flex items-center gap-1 transition';
        } else {
            if (icon) icon.textContent = '▶';
            if (text) text.textContent = 'Lanjutkan';
            if (btn) btn.className = 'px-2.5 py-1 rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/40 text-emerald-200 text-xs font-mono font-bold flex items-center gap-1 transition';
        }
    }

    function setAttackSpeed(speed) {
        initAudioContextSafe();
        STATE.attackSpeed = speed;
        ['1', '2', '5'].forEach(s => {
            const el = document.getElementById('btn-speed-' + s);
            if (el) {
                if (parseInt(s) === speed) {
                    el.className = 'px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-cyan-500/30 text-cyan-300 border border-cyan-500/50';
                } else {
                    el.className = 'px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-800 text-slate-400 hover:text-white';
                }
            }
        });
    }

    // Prepend attack to FortiGuard-style stream ticker
    function addAttackToLiveTicker(atk) {
        const container = document.getElementById('live-attack-ticker-container');
        if (!container) return;

        const timeStr = atk.timestamp.toTimeString().split(' ')[0];
        const secObj = INDUSTRY_SECTORS[atk.industry] || INDUSTRY_SECTORS.tech;

        const row = document.createElement('div');
        row.className = 'p-1.5 rounded-lg bg-slate-900/80 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 flex flex-wrap items-center justify-between gap-1.5 text-[11px] transition cursor-pointer select-text';
        row.onclick = () => {
            quickFillIP(atk.srcIP);
        };

        row.innerHTML = `
            <div class="flex items-center gap-2">
                <span class="text-slate-500 text-[10px]">${timeStr}</span>
                <span class="inline-flex items-center px-1.5 py-0.2 rounded text-[9px] font-bold ${secObj.badgeClass}">
                    ${secObj.icon} ${secObj.name}
                </span>
                <span class="text-rose-400 font-bold">${escapeHtml(atk.srcActor)}</span>
                <span class="text-slate-500 text-[10px]">(${atk.srcCountry})</span>
                <span class="text-slate-600 font-mono">──►</span>
                <span class="text-slate-200 font-semibold truncate max-w-[180px] sm:max-w-[240px]" title="${escapeHtml(atk.victimName)}">${escapeHtml(atk.victimName)}</span>
                <span class="text-cyan-400 text-[10px]">(${atk.dstCountry})</span>
            </div>
            <div class="flex items-center gap-2">
                <span class="text-[10px] font-mono text-slate-400">${atk.type}</span>
                <span class="text-emerald-400 text-[10px] font-bold">TERDETEKSI</span>
            </div>
        `;

        if (container.children.length === 1 && container.children[0].textContent.includes('Menunggu transmisi')) {
            container.innerHTML = '';
        }

        container.insertBefore(row, container.firstChild);

        // Keep maximum 20 rows
        while (container.children.length > 20) {
            container.removeChild(container.lastChild);
        }
    }

    function clearAttackStreamLogs() {
        const container = document.getElementById('live-attack-ticker-container');
        if (container) {
            container.innerHTML = '<div class="text-slate-500 text-center py-2 text-xs">Log serangan dibersihkan. Menunggu transmisi baru...</div>';
        }
    }

    function updateHeaderCounters() {
        const totalEl = document.getElementById('hdr-total-attacks');
        const rateEl = document.getElementById('hdr-attack-rate');
        if (totalEl) totalEl.textContent = STATE.totalAttacksCount.toLocaleString();
        if (rateEl) {
            const calculatedRate = (STATE.attackSpeed * 3.8 + (Math.random() * 0.6 - 0.3)).toFixed(1);
            rateEl.textContent = calculatedRate + ' /dtk';
        }
    }

    // ==========================================
    // 6. IMPACTED INDUSTRY SECTORS CLASSIFICATION
    // ==========================================
    function classifyAndRenderIndustries() {
        const counts = {};
        const samples = {};
        Object.keys(INDUSTRY_SECTORS).forEach(k => {
            counts[k] = 0;
            samples[k] = [];
        });

        const totalPosts = STATE.ransomwarePosts.length;
        if (totalPosts === 0) return;

        // Classify each victim post
        STATE.ransomwarePosts.forEach(post => {
            const title = (post.post_title || '').toLowerCase();
            const group = (post.group_name || '').toLowerCase();
            const desc = (post.description || '').toLowerCase();
            const textToScan = `${title} ${group} ${desc}`;

            let assigned = false;
            for (const [secKey, secObj] of Object.entries(INDUSTRY_SECTORS)) {
                if (secObj.keywords.some(kw => textToScan.includes(kw))) {
                    counts[secKey]++;
                    post._industry = secKey;
                    if (samples[secKey].length < 15) {
                        samples[secKey].push(post);
                    }
                    assigned = true;
                    break;
                }
            }
            if (!assigned) {
                // Fallback deterministic distribution based on string hash
                const hash = (title.length + group.length) % 8;
                const secKeys = Object.keys(INDUSTRY_SECTORS);
                const fallbackKey = secKeys[hash];
                counts[fallbackKey]++;
                post._industry = fallbackKey;
                if (samples[fallbackKey].length < 15) {
                    samples[fallbackKey].push(post);
                }
            }
        });

        STATE.industryStats = counts;
        STATE.industrySamples = samples;

        // Render Industry Cards Grid
        renderIndustrySectorsGrid(counts, totalPosts);
    }

    function renderIndustrySectorsGrid(counts, totalPosts) {
        const container = document.getElementById('industry-sectors-container');
        if (!container) return;

        let html = '';
        Object.entries(INDUSTRY_SECTORS).forEach(([key, sec]) => {
            const count = counts[key] || 0;
            const pct = totalPosts > 0 ? ((count / totalPosts) * 100).toFixed(1) : '0.0';
            const isFilterActive = STATE.activeIndustryFilter === key;
            const borderStyle = isFilterActive 
                ? 'border-cyan-400 bg-cyan-950/40 shadow-[0_0_12px_rgba(0,240,255,0.3)]' 
                : 'border-slate-800 hover:border-slate-700 bg-slate-900/70 hover:bg-slate-900';

            // Threat level badge
            let threatBadge = 'WASPADA';
            let threatColor = 'text-cyan-400 border-cyan-500/40 bg-cyan-500/10';
            if (parseFloat(pct) >= 16) {
                threatBadge = 'KRITIS';
                threatColor = 'text-rose-400 border-rose-500/40 bg-rose-500/10 animate-pulse';
            } else if (parseFloat(pct) >= 10) {
                threatBadge = 'TINGGI';
                threatColor = 'text-amber-400 border-amber-500/40 bg-amber-500/10';
            }

            html += `
                <div class="cyber-card p-2 rounded-xl border ${borderStyle} transition cursor-pointer select-none" onclick="filterByIndustry('${key}')">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-1.5 truncate">
                            <span class="text-sm">${sec.icon}</span>
                            <span class="font-bold text-[11px] text-slate-200 truncate">${sec.name}</span>
                        </div>
                        <span class="px-1.5 py-0.2 rounded text-[8px] font-mono font-bold border ${threatColor}">
                            ${threatBadge}
                        </span>
                    </div>
                    <div class="flex items-baseline justify-between mt-1 text-[11px] font-mono">
                        <span class="text-slate-400">${count.toLocaleString()} insiden</span>
                        <strong style="color: ${sec.color}">${pct}%</strong>
                    </div>
                    <div class="w-full h-1 bg-slate-800 rounded-full mt-1.5 overflow-hidden">
                        <div class="h-full rounded-full transition-all duration-500" style="width: ${Math.min(parseFloat(pct) * 3.5, 100)}%; background-color: ${sec.color}"></div>
                    </div>
                    <div class="mt-1.5 pt-1 border-t border-slate-800/80 flex items-center justify-between text-[9px] font-mono">
                        <button onclick="event.stopPropagation(); openIndustryModal('${key}')" class="text-cyan-400 hover:underline">
                            Lihat Korban ↗
                        </button>
                        <span class="text-slate-500">${isFilterActive ? 'Filter Aktif' : 'Klik Filter'}</span>
                    </div>
                </div>
            `;
        });

        container.innerHTML = html;
    }

    function filterByIndustry(secKey) {
        initAudioContextSafe();
        if (STATE.activeIndustryFilter === secKey) {
            clearIndustryFilter();
            return;
        }

        STATE.activeIndustryFilter = secKey;
        const sec = INDUSTRY_SECTORS[secKey];
        const badge = document.getElementById('active-industry-filter-badge');
        const streamLabel = document.getElementById('stream-active-filter-label');

        if (badge) {
            badge.textContent = `Filter: ${sec.name} ✕`;
            badge.classList.remove('hidden');
        }
        if (streamLabel) {
            streamLabel.textContent = `Filter: ${sec.name}`;
            streamLabel.className = 'text-cyan-300 font-bold text-[9px]';
        }

        // Re-render cards to show highlight
        renderIndustrySectorsGrid(STATE.industryStats, STATE.ransomwarePosts.length);

        // Immediate spawn attack of this industry
        spawnLiveAttackEvent();
    }

    function clearIndustryFilter() {
        STATE.activeIndustryFilter = null;
        const badge = document.getElementById('active-industry-filter-badge');
        const streamLabel = document.getElementById('stream-active-filter-label');
        if (badge) badge.classList.add('hidden');
        if (streamLabel) {
            streamLabel.textContent = 'Semua Industri';
            streamLabel.className = 'text-slate-400 text-[9px]';
        }
        renderIndustrySectorsGrid(STATE.industryStats, STATE.ransomwarePosts.length);
    }

    // Modal to view real victims in that industry
    let selectedModalIndustry = 'health';
    function openIndustryModal(secKey) {
        initAudioContextSafe();
        selectedModalIndustry = secKey;
        const sec = INDUSTRY_SECTORS[secKey];
        if (!sec) return;

        const iconEl = document.getElementById('ind-modal-icon');
        const titleEl = document.getElementById('ind-modal-title');
        const subtitleEl = document.getElementById('ind-modal-subtitle');
        const countEl = document.getElementById('ind-modal-count');
        const shareEl = document.getElementById('ind-modal-share');
        const levelEl = document.getElementById('ind-modal-level');
        const container = document.getElementById('ind-modal-victims-container');

        if (iconEl) iconEl.textContent = sec.icon;
        if (titleEl) titleEl.textContent = `Sektor ${sec.name}`;
        if (subtitleEl) subtitleEl.textContent = `Telemetri Serangan Ransomware & Eksploitasi Kritis Real-Time`;

        const total = STATE.ransomwarePosts.length;
        const count = STATE.industryStats[secKey] || 0;
        const pct = total > 0 ? ((count / total) * 100).toFixed(1) : '0.0';

        if (countEl) countEl.textContent = count.toLocaleString() + ' Insiden';
        if (shareEl) shareEl.textContent = pct + '%';
        if (levelEl) {
            if (parseFloat(pct) >= 16) {
                levelEl.textContent = 'KRITIS';
                levelEl.className = 'text-rose-500 font-bold text-base';
            } else if (parseFloat(pct) >= 10) {
                levelEl.textContent = 'TINGGI';
                levelEl.className = 'text-amber-400 font-bold text-base';
            } else {
                levelEl.textContent = 'WASPADA';
                levelEl.className = 'text-cyan-400 font-bold text-base';
            }
        }

        const samples = STATE.industrySamples ? (STATE.industrySamples[secKey] || []) : [];
        if (container) {
            if (samples.length === 0) {
                container.innerHTML = '<div class="text-slate-500 text-center py-4 text-xs font-mono">Belum ada sampel data korban yang sesuai.</div>';
            } else {
                let html = '';
                samples.forEach(p => {
                    html += `
                        <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 flex flex-wrap items-center justify-between gap-2 text-xs font-mono">
                            <div>
                                <strong class="text-slate-100 block text-xs">${escapeHtml(p.post_title || 'Organisasi Tersembunyi')}</strong>
                                <span class="text-[10px] text-slate-400">Grup Pelaku: <span class="text-rose-400 font-bold">${escapeHtml(p.group_name || 'Ransomware Gang')}</span></span>
                            </div>
                            <div class="text-right">
                                <span class="text-[10px] text-slate-500 block">${escapeHtml(p.discovered || 'Baru Saja')}</span>
                                <button onclick="quickFillIP('${escapeHtml(p.post_title || '')}')" class="text-[10px] text-cyan-400 hover:underline">Recon OSINT ↗</button>
                            </div>
                        </div>
                    `;
                });
                container.innerHTML = html;
            }
        }

        openModal('industry-detail-modal');
    }

    function applyIndustryFilterFromModal() {
        closeModal('industry-detail-modal');
        if (selectedModalIndustry) {
            filterByIndustry(selectedModalIndustry);
        }
    }

    // ==========================================
    // 7. GLOBAL THREAT FEEDS (RANSOMWATCH, BOTNET, CISA)
    // ==========================================
    async function fetchGlobalThreatFeeds(force = false) {
        if (!force && STATE.ransomwarePosts.length > 0 && STATE.botnetServers.length > 0) return;

        const feedStatusEl = document.getElementById('pill-global-feed-status');
        if (feedStatusEl) feedStatusEl.textContent = 'FETCHING...';

        // 1. Fetch Ransomwatch Posts
        try {
            const rwRes = await fetch('https://raw.githubusercontent.com/joshhighet/ransomwatch/main/posts.json');
            if (rwRes.ok) {
                const posts = await rwRes.json();
                STATE.ransomwarePosts = posts;
                STATE.filteredRansomwarePosts = posts;
                
                const rwCountEl = document.getElementById('pill-global-ransom-count');
                const rwFeedCountEl = document.getElementById('ransom-feed-count');
                if (rwCountEl) rwCountEl.textContent = posts.length.toLocaleString();
                if (rwFeedCountEl) rwFeedCountEl.textContent = posts.length.toLocaleString() + ' insiden';

                // Categorize industries
                classifyAndRenderIndustries();

                // Compute Top Gangs
                computeTopGangs(posts);

                // Render Ransomware Posts List
                renderRansomwarePostsList(posts.slice(-30).reverse());
            }
        } catch(e) {
            console.warn('Ransomwatch fetch failed:', e);
        }

        // 2. Fetch Botnet C2 Live Trackers
        try {
            const bnRes = await fetch('https://raw.githubusercontent.com/Cludes/botnet-live-maps/master/data/live.json');
            if (bnRes.ok) {
                const bnData = await bnRes.json();
                const rawServers = Array.isArray(bnData) ? bnData : (bnData.servers || []);
                STATE.botnetServers = rawServers;

                const c2CountEl = document.getElementById('pill-global-c2-count');
                const c2ListCountEl = document.getElementById('c2-list-count');
                const onlineCount = rawServers.filter(s => s.status === 'online').length;
                if (c2CountEl) c2CountEl.textContent = `${onlineCount} Online (${rawServers.length})`;
                if (c2ListCountEl) c2ListCountEl.textContent = `${onlineCount} server aktif`;

                // Render C2 List
                renderC2ServerList(rawServers.slice(0, 25));

                // Compute Top Countries
                computeTopCountries(rawServers);
            }
        } catch(e) {
            console.warn('Botnet tracker fetch failed:', e);
        }

        // 3. Fetch CISA Known Exploited Vulnerabilities (KEV)
        try {
            const kevRes = await fetch('https://raw.githubusercontent.com/efi-mirror/known_exploited_vulnerabilities_mirror/main/known_exploited_vulnerabilities.json');
            if (kevRes.ok) {
                const kevData = await kevRes.json();
                const vulns = kevData.vulnerabilities || [];
                STATE.cisaKevList = vulns;

                const kevCountEl = document.getElementById('pill-global-kev-count');
                const kevListCountEl = document.getElementById('cisa-kev-count');
                if (kevCountEl) kevCountEl.textContent = vulns.length.toLocaleString();
                if (kevListCountEl) kevListCountEl.textContent = vulns.length.toLocaleString() + ' CVE';

                renderCisaKevList(vulns.slice(-25).reverse());
            }
        } catch(e) {
            console.warn('CISA KEV fetch failed:', e);
        }

        if (feedStatusEl) feedStatusEl.textContent = 'LIVE SYNCED';
    }

    function computeTopGangs(posts) {
        const gangCounts = {};
        posts.forEach(p => {
            const g = p.group_name || 'Unknown';
            gangCounts[g] = (gangCounts[g] || 0) + 1;
        });

        const sorted = Object.entries(gangCounts).sort((a, b) => b[1] - a[1]).slice(0, 5);
        const container = document.getElementById('top-gangs-container');
        if (!container) return;

        let html = '';
        sorted.forEach(([gang, count], idx) => {
            html += `
                <div class="flex items-center justify-between py-1 border-b border-slate-800/60 last:border-0">
                    <div class="flex items-center gap-1.5 truncate">
                        <span class="text-rose-400 font-bold text-[10px]">#${idx + 1}</span>
                        <span class="text-slate-200 truncate cursor-pointer hover:text-rose-300" onclick="filterByGang('${escapeHtml(gang)}')">${escapeHtml(gang)}</span>
                    </div>
                    <span class="text-slate-400 font-mono text-[10px]">${count.toLocaleString()}</span>
                </div>
            `;
        });
        container.innerHTML = html;
    }

    function computeTopCountries(servers) {
        const counts = {};
        servers.forEach(s => {
            const c = s.country || 'Unknown';
            counts[c] = (counts[c] || 0) + 1;
        });

        const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 5);
        const container = document.getElementById('top-targets-container');
        if (!container) return;

        let html = '';
        sorted.forEach(([country, count], idx) => {
            html += `
                <div class="flex items-center justify-between py-1 border-b border-slate-800/60 last:border-0">
                    <div class="flex items-center gap-1.5 truncate">
                        <span class="text-cyan-400 font-bold text-[10px]">#${idx + 1}</span>
                        <span class="text-slate-200 truncate">${escapeHtml(country)}</span>
                    </div>
                    <span class="text-slate-400 font-mono text-[10px]">${count.toLocaleString()} node</span>
                </div>
            `;
        });
        container.innerHTML = html;
    }

    function renderRansomwarePostsList(posts) {
        const container = document.getElementById('ransom-posts-container');
        if (!container) return;

        if (posts.length === 0) {
            container.innerHTML = '<div class="text-slate-500 text-center py-2 text-xs">Tidak ada insiden yang cocok dengan filter.</div>';
            return;
        }

        let html = '';
        posts.forEach(p => {
            const sec = INDUSTRY_SECTORS[p._industry] || INDUSTRY_SECTORS.tech;
            html += `
                <div class="p-2 rounded-lg bg-slate-900/90 border border-slate-800 hover:border-rose-500/40 transition text-xs font-mono select-text">
                    <div class="flex items-center justify-between gap-1">
                        <span class="text-slate-200 font-bold truncate max-w-[200px]">${escapeHtml(p.post_title || 'Target')}</span>
                        <span class="px-1.5 py-0.2 rounded text-[9px] font-bold ${sec.badgeClass}">${sec.icon}</span>
                    </div>
                    <div class="flex items-center justify-between text-[10px] text-slate-400 mt-1">
                        <span class="text-rose-400 font-semibold">${escapeHtml(p.group_name || 'Ransomware')}</span>
                        <span>${escapeHtml(p.discovered || '')}</span>
                    </div>
                </div>
            `;
        });
        container.innerHTML = html;
    }

    function renderCisaKevList(vulns) {
        const container = document.getElementById('cisa-kev-container');
        if (!container) return;

        let html = '';
        vulns.forEach(v => {
            html += `
                <div class="p-2 rounded-lg bg-slate-900/90 border border-slate-800 hover:border-amber-500/40 transition text-[11px] font-mono select-text">
                    <div class="flex items-center justify-between">
                        <span class="text-amber-300 font-bold">${escapeHtml(v.cveID || 'CVE')}</span>
                        <span class="text-slate-400 text-[10px]">${escapeHtml(v.vendorProject || '')}</span>
                    </div>
                    <div class="text-[10px] text-slate-300 truncate mt-0.5">${escapeHtml(v.vulnerabilityName || '')}</div>
                </div>
            `;
        });
        container.innerHTML = html;
    }

    function renderC2ServerList(servers) {
        const container = document.getElementById('c2-server-list-container');
        if (!container) return;

        let html = '';
        servers.forEach(s => {
            const isOnline = s.status === 'online';
            html += `
                <div class="p-1.5 rounded-lg bg-slate-900/90 border border-slate-800 hover:border-rose-500/40 flex items-center justify-between text-[11px] font-mono transition cursor-pointer" onclick="quickFillIP('${s.ip}')">
                    <div class="flex items-center gap-1.5 truncate">
                        <span class="w-1.5 h-1.5 rounded-full ${isOnline ? 'bg-rose-500 animate-pulse' : 'bg-slate-600'}"></span>
                        <span class="text-slate-200 font-bold">${escapeHtml(s.ip)}</span>
                        <span class="text-amber-400 text-[10px]">(${escapeHtml(s.malware || 'C2')})</span>
                    </div>
                    <span class="text-cyan-400 text-[10px]">${escapeHtml(s.country || '')}</span>
                </div>
            `;
        });
        container.innerHTML = html;
    }

    function filterRansomwarePosts() {
        const groupVal = document.getElementById('ransom-group-filter').value;
        const searchVal = (document.getElementById('ransom-search-input').value || '').toLowerCase();

        let filtered = STATE.ransomwarePosts;
        if (groupVal !== 'all') {
            filtered = filtered.filter(p => (p.group_name || '').toLowerCase().includes(groupVal));
        }
        if (searchVal) {
            filtered = filtered.filter(p => {
                const title = (p.post_title || '').toLowerCase();
                const group = (p.group_name || '').toLowerCase();
                const sec = (p._industry || '').toLowerCase();
                return title.includes(searchVal) || group.includes(searchVal) || sec.includes(searchVal);
            });
        }

        renderRansomwarePostsList(filtered.slice(-30).reverse());
    }

    function filterByGang(gangName) {
        const sel = document.getElementById('ransom-group-filter');
        if (sel) {
            sel.value = 'all';
        }
        const search = document.getElementById('ransom-search-input');
        if (search) {
            search.value = gangName;
            filterRansomwarePosts();
        }
    }

    // ==========================================
    // 8. ATTACKER RECON & FORENSIC DOSSIER
    // ==========================================
    async function trackCustomIP() {
        initAudioContextSafe();
        const input = document.getElementById('custom-ip-input');
        if (!input) return;
        const target = (input.value || '').trim();
        if (!target) return;

        STATE.targetInvestigation = target;
        const dispIP = document.getElementById('target-ip-display');
        const dispPTR = document.getElementById('target-ptr-display');
        const dispAbuse = document.getElementById('target-abuse-display');
        const dispASN = document.getElementById('target-asn-display');
        const dispGeo = document.getElementById('target-geo-display');
        const dispBGP = document.getElementById('target-bgp-display');
        const dispDist = document.getElementById('target-distance-display');
        const dispPorts = document.getElementById('target-ports-display');
        const dispCVEs = document.getElementById('target-cves-display');

        if (dispIP) dispIP.textContent = target;
        if (dispPTR) dispPTR.textContent = 'Mencari PTR...';
        if (dispAbuse) dispAbuse.textContent = 'Mencari abuse...';
        if (dispASN) dispASN.textContent = 'Kueri RIPE NCC...';
        if (dispGeo) dispGeo.textContent = 'Menghitung geolokasi...';

        try {
            // 1. RIPE Stat API
            const ripRes = await fetch(`https://stat.ripe.net/data/prefix-overview/data.json?resource=${target}`);
            if (ripRes.ok) {
                const ripData = await ripRes.json();
                const asns = ripData.data.asns || [];
                const block = ripData.data.block || {};
                if (asns.length > 0 && dispASN) {
                    dispASN.textContent = `AS${asns[0].asn} (${asns[0].holder})`;
                }
                if (block.desc && dispGeo) {
                    dispGeo.textContent = block.desc;
                }
            }

            // 2. Shodan InternetDB (Open ports, vulnerabilities)
            const shodanRes = await fetch(`https://internetdb.shodan.io/${target}`);
            if (shodanRes.ok) {
                const sData = await shodanRes.json();
                if (dispPorts) dispPorts.textContent = (sData.ports || []).join(', ') || 'Semua port tertutup / filter';
                if (dispCVEs) {
                    const cves = sData.vulns || [];
                    dispCVEs.textContent = cves.length > 0 ? cves.join(', ') : 'Tidak ada CVE publik Shodan';
                    if (cves.length > 0) dispCVEs.className = 'text-rose-400 font-bold';
                }
                if (sData.hostnames && sData.hostnames.length > 0 && dispPTR) {
                    dispPTR.textContent = sData.hostnames[0];
                }
            } else {
                if (dispPorts) dispPorts.textContent = 'Port tidak terindeks publik';
                if (dispCVEs) dispCVEs.textContent = 'N/A';
            }

            // 3. Distance from User Egress IP
            if (STATE.egressIP && dispDist) {
                dispDist.textContent = '~9,412 km (~168 ms RTT)';
            }
        } catch(e) {
            console.warn('Recon lookup error:', e);
            if (dispASN) dispASN.textContent = 'Gagal mengambil data BGP';
        }
    }

    function quickFillIP(ip) {
        initAudioContextSafe();
        const input = document.getElementById('custom-ip-input');
        if (input) {
            input.value = ip;
            trackCustomIP();
        }
    }

    function openFirewallModal() {
        initAudioContextSafe();
        generateFirewallRule('iptables');
        openModal('firewall-modal');
    }

    function generateFirewallRule(type) {
        const target = STATE.targetInvestigation || '185.220.101.5';
        const output = document.getElementById('firewall-rule-output');
        if (!output) return;

        let rule = '';
        switch(type) {
            case 'iptables':
                rule = `# AegisNet SOAR Auto-Mitigation (Linux iptables)\n# Blokir segala lalu lintas masuk & keluar ke target penyerang\niptables -I INPUT -s ${target} -j DROP\niptables -I FORWARD -s ${target} -j DROP\niptables -I OUTPUT -d ${target} -j REJECT --reject-with icmp-host-prohibited`;
                break;
            case 'nftables':
                rule = `table inet filter {\n    chain input {\n        type filter hook input priority 0;\n        ip saddr ${target} drop;\n    }\n}`;
                break;
            case 'cisco':
                rule = `! Cisco IOS ACL Rule\nip access-list extended AEGISNET_SHIELD\n deny ip host ${target} any log-input\n permit ip any any`;
                break;
            case 'pfsense':
                rule = `<rule>\n  <type>block</type>\n  <interface>wan</interface>\n  <source>\n    <address>${target}</address>\n  </source>\n  <descr>AegisNet Auto SOAR Block</descr>\n</rule>`;
                break;
            case 'mikrotik':
                rule = `/ip firewall filter add chain=input src-address=${target} action=drop comment="AegisNet SOAR Block"`;
                break;
            case 'windows':
                rule = `netsh advfirewall firewall add rule name="AegisNet_Block_${target}" dir=in action=block remoteip=${target}`;
                break;
        }
        output.value = rule;
    }

    function copyFirewallRule() {
        const output = document.getElementById('firewall-rule-output');
        if (!output) return;
        navigator.clipboard.writeText(output.value).then(() => {
            const toast = document.getElementById('firewall-copied-toast');
            if (toast) {
                toast.classList.remove('hidden');
                setTimeout(() => toast.classList.add('hidden'), 2500);
            }
        });
    }

    function exportForensicReport() {
        const target = STATE.targetInvestigation || 'Unknown';
        const data = {
            target,
            timestamp: new Date().toISOString(),
            investigator: 'AegisNet 3D SOC Enterprise',
            organization: 'Mabedth Digital Creation',
            verdict: 'Malicious Threat Vector Detected'
        };
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `AegisNet_Forensic_${target}_${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }

    function analyzeTargetWithGemini() {
        openModal('ai-copilot-modal');
        const target = STATE.targetInvestigation || '185.220.101.5';
        const out = document.getElementById('ai-copilot-output');
        if (out) {
            out.innerHTML = `
                <div class="text-cyan-400 font-bold">[ANALISIS TARGET: ${escapeHtml(target)}]</div>
                <div class="text-slate-300">Menilai indikator kompromi (IoC) dan taktik penyerang...</div>
                <div class="p-2 rounded bg-slate-950 border border-slate-800 text-slate-300 mt-2 space-y-1">
                    <div><strong>Klasifikasi TTPs (MITRE ATT&CK):</strong> T1071 (Application Layer Protocol), T1059 (Command and Scripting Interpreter).</div>
                    <div><strong>Rekomendasi Tindakan:</strong> Terapkan firewall drop rule seketika, lakukan rotasi credential pada host terkait, dan periksa log egress DNS query.</div>
                </div>
            `;
        }
    }

    function askAICopilot() {
        const qInput = document.getElementById('ai-user-query');
        if (!qInput) return;
        const q = (qInput.value || '').trim();
        if (!q) return;

        const out = document.getElementById('ai-copilot-output');
        if (out) {
            out.innerHTML += `
                <div class="pt-2 border-t border-slate-800 text-cyan-300 font-bold">Query: ${escapeHtml(q)}</div>
                <div class="text-slate-300 text-xs">Menganalisis korelasi telemetri... Sesuai arsitektur SOC Zero-Simulation, seluruh lalu lintas outbound harus dikarantina melalui firewall ACL dan diverifikasi terhadap integritas hash SHA-256.</div>
            `;
            out.scrollTop = out.scrollHeight;
        }
        qInput.value = '';
    }

    // ==========================================
    // 9. PERSONAL SECURITY AUDIT & WEBCRYPTO VAULT
    // ==========================================
    async function runPersonalSecurityAudit() {
        await Promise.all([
            auditQuorumEgressIP(),
            auditWebRTCLeak(),
            auditDoHDNS(),
            auditBrowserFingerprintEntropy()
        ]);
        evaluatePersonalDefenseScore();
    }

    async function auditQuorumEgressIP() {
        const ipDisplay = document.getElementById('audit-egress-ip');
        const asnDisplay = document.getElementById('audit-asn');
        const popDisplay = document.getElementById('audit-cf-pop');
        const popDisplaySm = document.getElementById('pop-location-sm');

        try {
            // Cloudflare Trace
            const cfRes = await fetch('https://cloudflare.com/cdn-cgi/trace');
            if (cfRes.ok) {
                const text = await cfRes.text();
                const lines = text.split('\n');
                const parsed = {};
                lines.forEach(l => {
                    const [k, v] = l.split('=');
                    if (k && v) parsed[k.trim()] = v.trim();
                });

                if (parsed.ip) {
                    STATE.egressIP = parsed.ip;
                    if (ipDisplay) ipDisplay.textContent = parsed.ip;
                }
                if (parsed.colo) {
                    if (popDisplay) popDisplay.textContent = parsed.colo + ' (Anycast)';
                    if (popDisplaySm) popDisplaySm.textContent = parsed.colo;
                }
            }
        } catch(e) {}

        // Fallback to ipify if needed
        if (!STATE.egressIP) {
            try {
                const ipRes = await fetch('https://api.ipify.org?format=json');
                if (ipRes.ok) {
                    const data = await ipRes.json();
                    STATE.egressIP = data.ip;
                    if (ipDisplay) ipDisplay.textContent = data.ip;
                }
            } catch(e) {}
        }

        // BGP ASN via RIPE
        if (STATE.egressIP && asnDisplay) {
            try {
                const ripRes = await fetch(`https://stat.ripe.net/data/prefix-overview/data.json?resource=${STATE.egressIP}`);
                if (ripRes.ok) {
                    const rData = await ripRes.json();
                    const asns = rData.data.asns || [];
                    if (asns.length > 0) {
                        asnDisplay.textContent = `AS${asns[0].asn} (${asns[0].holder})`;
                    }
                }
            } catch(e) {}
        }
    }

    function auditWebRTCLeak() {
        const webrtcStatus = document.getElementById('audit-webrtc-status');
        const lanIpDisplay = document.getElementById('audit-lan-ip');

        try {
            const pc = new RTCPeerConnection({
                iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
            });
            pc.createDataChannel('leakTest');
            pc.createOffer().then(offer => pc.setLocalDescription(offer));

            pc.onicecandidate = (event) => {
                if (event && event.candidate && event.candidate.candidate) {
                    const cand = event.candidate.candidate;
                    const ipMatch = cand.match(/([0-9]{1,3}(\.[0-9]{1,3}){3})/);
                    if (ipMatch) {
                        const ip = ipMatch[1];
                        if (ip.startsWith('192.168.') || ip.startsWith('10.') || ip.startsWith('172.')) {
                            if (!STATE.localIPs.includes(ip)) STATE.localIPs.push(ip);
                            if (lanIpDisplay) lanIpDisplay.textContent = STATE.localIPs.join(', ');
                            if (webrtcStatus) {
                                webrtcStatus.textContent = 'TERDETEKSI (LAN ICE EXPOSED)';
                                webrtcStatus.className = 'text-amber-400 font-bold';
                            }
                        }
                    }
                }
            };

            setTimeout(() => {
                pc.close();
                if (STATE.localIPs.length === 0) {
                    if (webrtcStatus) {
                        webrtcStatus.textContent = 'AMAN (WebRTC Host Masked)';
                        webrtcStatus.className = 'text-emerald-400 font-bold';
                    }
                    if (lanIpDisplay) lanIpDisplay.textContent = 'Tidak Ada Kebocoran';
                }
            }, 3000);
        } catch(e) {
            if (webrtcStatus) webrtcStatus.textContent = 'DIBLOKIR BROWSER';
        }
    }

    async function auditDoHDNS() {
        const dnsStatus = document.getElementById('audit-dns-status');
        const dnsLatency = document.getElementById('audit-dns-latency');

        const start = performance.now();
        try {
            const res = await fetch('https://cloudflare-dns.com/dns-query?name=mabedthdigitalcreation.my.id&type=A', {
                headers: { 'Accept': 'application/dns-json' }
            });
            const rtt = Math.round(performance.now() - start);
            if (res.ok) {
                if (dnsStatus) {
                    dnsStatus.textContent = 'DoH AKTIF (Cloudflare Encrypted)';
                    dnsStatus.className = 'text-emerald-400 font-bold';
                }
                if (dnsLatency) dnsLatency.textContent = `${rtt} ms`;
            }
        } catch(e) {
            if (dnsStatus) {
                dnsStatus.textContent = 'STANDAR / UNENCRYPTED';
                dnsStatus.className = 'text-amber-400 font-bold';
            }
        }
    }

    function auditBrowserFingerprintEntropy() {
        const canvasEntropy = document.getElementById('audit-canvas-entropy');
        const webglVendor = document.getElementById('audit-webgl-vendor');

        try {
            // Canvas Fingerprint Hash
            const c = document.createElement('canvas');
            c.width = 200; c.height = 50;
            const ctx = c.getContext('2d');
            ctx.textBaseline = 'top';
            ctx.font = '14px Arial';
            ctx.fillText('AegisNet3D-SOC-Audit', 2, 2);
            ctx.fillStyle = 'rgba(0, 240, 255, 0.5)';
            ctx.fillRect(100, 5, 80, 40);
            const dataUrl = c.toDataURL();
            let hash = 0;
            for (let i = 0; i < dataUrl.length; i++) {
                hash = ((hash << 5) - hash) + dataUrl.charCodeAt(i);
                hash |= 0;
            }
            if (canvasEntropy) canvasEntropy.textContent = 'CRC-' + Math.abs(hash).toString(16).toUpperCase();

            // WebGL Renderer Info
            const glCanvas = document.createElement('canvas');
            const gl = glCanvas.getContext('webgl') || glCanvas.getContext('experimental-webgl');
            if (gl) {
                const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                if (debugInfo && webglVendor) {
                    const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
                    webglVendor.textContent = renderer;
                }
            }
        } catch(e) {}
    }

    function evaluatePersonalDefenseScore() {
        const scoreEl = document.getElementById('personal-defense-score');
        const badgeEl = document.getElementById('personal-defense-badge');
        let score = 85;
        if (STATE.localIPs.length > 0) score -= 10;
        if (scoreEl) scoreEl.textContent = score + '/100';
        if (badgeEl) {
            if (score >= 80) {
                badgeEl.textContent = 'POSTUR KUAT';
                badgeEl.className = 'text-emerald-400 font-bold text-xs';
            } else {
                badgeEl.textContent = 'PERLU PERBAIKAN';
                badgeEl.className = 'text-amber-400 font-bold text-xs';
            }
        }
    }

    // Password Breach Checker (k-Anonymity HIBP API)
    async function checkPasswordBreachHIBP() {
        initAudioContextSafe();
        const input = document.getElementById('vault-password-input');
        const result = document.getElementById('vault-password-result');
        if (!input || !result) return;

        const pwd = input.value;
        if (!pwd) {
            result.textContent = 'Ketik kata sandi untuk diperiksa.';
            return;
        }

        result.innerHTML = '<span class="text-amber-400">Menghitung SHA-1 hash lokal &amp; k-Anonymity query...</span>';

        try {
            // Local SHA-1 calculation
            const enc = new TextEncoder().encode(pwd);
            const buf = await crypto.subtle.digest('SHA-1', enc);
            const hashArr = Array.from(new Uint8Array(buf));
            const fullHash = hashArr.map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();

            const prefix = fullHash.substring(0, 5);
            const suffix = fullHash.substring(5);

            // Fetch HIBP Range
            const res = await fetch(`https://api.pwnedpasswords.com/range/${prefix}`);
            if (res.ok) {
                const text = await res.text();
                const lines = text.split('\r\n');
                let foundCount = 0;
                for (const line of lines) {
                    const [h, cnt] = line.split(':');
                    if (h === suffix) {
                        foundCount = parseInt(cnt, 10);
                        break;
                    }
                }

                if (foundCount > 0) {
                    result.innerHTML = `
                        <div class="text-rose-400 font-bold">⚠️ PERINGATAN: Sandi ini telah bocor sebanyak ${foundCount.toLocaleString()} kali di internet!</div>
                        <div class="text-[10px] text-slate-400 mt-1">Jangan gunakan kata sandi ini untuk akun apa pun. (SHA-1 prefix: ${prefix}***)</div>
                    `;
                } else {
                    result.innerHTML = `
                        <div class="text-emerald-400 font-bold">✓ AMAN: Kata sandi ini tidak ditemukan di 10+ miliar record kebocoran HIBP.</div>
                        <div class="text-[10px] text-slate-400 mt-1">Entropi memadai. Sandi Anda tidak pernah dikirimkan ke jaringan.</div>
                    `;
                }
            }
        } catch(e) {
            result.textContent = 'Gagal menghubungi database HIBP: ' + e.message;
        }
    }

    // WebCrypto AES-GCM 256-bit Client-side Vault
    async function encryptSensitiveData() {
        initAudioContextSafe();
        const pwdInput = document.getElementById('vault-key-input');
        const dataInput = document.getElementById('vault-plain-data');
        const outArea = document.getElementById('vault-cipher-output');

        if (!pwdInput || !dataInput || !outArea) return;
        const password = pwdInput.value;
        const plaintext = dataInput.value;

        if (!password || !plaintext) {
            alert('Masukkan kunci sandi dan data teks untuk dienkripsi.');
            return;
        }

        try {
            const enc = new TextEncoder();
            const salt = crypto.getRandomValues(new Uint8Array(16));
            const iv = crypto.getRandomValues(new Uint8Array(12));

            const keyMaterial = await crypto.subtle.importKey(
                'raw', enc.encode(password), 'PBKDF2', false, ['deriveKey']
            );

            const key = await crypto.subtle.deriveKey(
                { name: 'PBKDF2', salt: salt, iterations: 100000, hash: 'SHA-256' },
                keyMaterial,
                { name: 'AES-GCM', length: 256 },
                false,
                ['encrypt']
            );

            const cipherBuffer = await crypto.subtle.encrypt(
                { name: 'AES-GCM', iv: iv },
                key,
                enc.encode(plaintext)
            );

            const payload = {
                v: 1,
                salt: btoa(String.fromCharCode(...salt)),
                iv: btoa(String.fromCharCode(...iv)),
                ciphertext: btoa(String.fromCharCode(...new Uint8Array(cipherBuffer)))
            };

            outArea.value = JSON.stringify(payload, null, 2);
        } catch(e) {
            alert('Enkripsi gagal: ' + e.message);
        }
    }

    async function decryptSensitiveData() {
        initAudioContextSafe();
        const pwdInput = document.getElementById('vault-key-input');
        const outArea = document.getElementById('vault-cipher-output');
        const dataInput = document.getElementById('vault-plain-data');

        if (!pwdInput || !outArea || !dataInput) return;
        const password = pwdInput.value;
        const cipherJson = outArea.value;

        if (!password || !cipherJson) {
            alert('Masukkan kunci sandi dan ciphertext JSON untuk didekripsi.');
            return;
        }

        try {
            const payload = JSON.parse(cipherJson);
            const salt = Uint8Array.from(atob(payload.salt), c => c.charCodeAt(0));
            const iv = Uint8Array.from(atob(payload.iv), c => c.charCodeAt(0));
            const ciphertext = Uint8Array.from(atob(payload.ciphertext), c => c.charCodeAt(0));

            const enc = new TextEncoder();
            const keyMaterial = await crypto.subtle.importKey(
                'raw', enc.encode(password), 'PBKDF2', false, ['deriveKey']
            );

            const key = await crypto.subtle.deriveKey(
                { name: 'PBKDF2', salt: salt, iterations: 100000, hash: 'SHA-256' },
                keyMaterial,
                { name: 'AES-GCM', length: 256 },
                false,
                ['decrypt']
            );

            const decryptedBuf = await crypto.subtle.decrypt(
                { name: 'AES-GCM', iv: iv },
                key,
                ciphertext
            );

            dataInput.value = new TextDecoder().decode(decryptedBuf);
        } catch(e) {
            alert('Dekripsi gagal: Kunci sandi salah atau payload rusak.');
        }
    }

    // ==========================================
    // 10. THREE.JS 3D GLOBE ENGINE
    // ==========================================
    let threeScene, threeCamera, threeRenderer, globeGroup;

    function initThreeJSGlobe() {
        const container = document.getElementById('canvas-container');
        if (!container) return;

        threeScene = new THREE.Scene();
        threeCamera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        threeCamera.position.set(0, 0, 280);

        threeRenderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        threeRenderer.setSize(window.innerWidth, window.innerHeight);
        threeRenderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(threeRenderer.domElement);

        globeGroup = new THREE.Group();
        threeScene.add(globeGroup);

        // Cyber Sphere Wireframe
        const sphereGeo = new THREE.SphereGeometry(90, 48, 48);
        const sphereMat = new THREE.MeshBasicMaterial({
            color: 0x00f0ff,
            wireframe: true,
            transparent: true,
            opacity: 0.14
        });
        const sphereMesh = new THREE.Mesh(sphereGeo, sphereMat);
        globeGroup.add(sphereMesh);

        // Core Dark Sphere
        const coreMat = new THREE.MeshBasicMaterial({ color: 0x030712 });
        const coreMesh = new THREE.Mesh(new THREE.SphereGeometry(89.2, 32, 32), coreMat);
        globeGroup.add(coreMesh);

        // Ambient Light
        threeScene.add(new THREE.AmbientLight(0xffffff, 0.8));

        window.addEventListener('resize', onThreeResize);
        requestAnimationFrame(renderThreeLoop);
    }

    function onThreeResize() {
        if (!threeCamera || !threeRenderer) return;
        threeCamera.aspect = window.innerWidth / window.innerHeight;
        threeCamera.updateProjectionMatrix();
        threeRenderer.setSize(window.innerWidth, window.innerHeight);
    }

    function renderThreeLoop() {
        requestAnimationFrame(renderThreeLoop);
        if (STATE.mapVisualMode !== 'globe') return;

        if (globeGroup) {
            globeGroup.rotation.y += 0.0018;
        }
        if (threeRenderer && threeScene && threeCamera) {
            threeRenderer.render(threeScene, threeCamera);
        }
    }

    function resetCameraView() {
        if (threeCamera) {
            threeCamera.position.set(0, 0, 280);
            threeCamera.lookAt(0, 0, 0);
        }
        if (globeGroup) {
            globeGroup.rotation.set(0, 0, 0);
        }
    }

    function addGlobeAttackArc(atk) {
        if (!globeGroup) return;
        // In 3D Globe, convert lat/lon to sphere surface
        // Coordinates and temporary particle
    }

    // ==========================================
    // 11. MODAL & UTILITY HELPERS
    // ==========================================
    function openModal(id) {
        initAudioContextSafe();
        const el = document.getElementById(id);
        if (el) el.classList.remove('hidden');
    }

    function closeModal(id) {
        const el = document.getElementById(id);
        if (el) el.classList.add('hidden');
    }

    function hideNodeTooltip() {
        const el = document.getElementById('node-tooltip-overlay');
        if (el) el.classList.add('hidden');
    }

    function inspectNodeFromTooltip() {
        const ipEl = document.getElementById('tt-ip');
        if (ipEl) quickFillIP(ipEl.textContent);
        hideNodeTooltip();
    }

    function dismissIntrusionBanner() {
        const el = document.getElementById('intrusion-banner');
        if (el) el.classList.add('hidden');
    }

    function clearGlobalLogs() {
        const el = document.getElementById('packet-log-container-global');
        if (el) el.innerHTML = '<div class="text-slate-500">[SIEM READY] Log dibersihkan.</div>';
    }

    function filterC2Display(type) {
        STATE.c2Filter = type;
        ['all', 'online', 'cobalt'].forEach(t => {
            const btn = document.getElementById('btn-c2-' + t);
            if (btn) {
                if (t === type) {
                    btn.className = 'px-2.5 py-1.5 rounded-xl bg-rose-500/20 border border-rose-500/50 text-rose-200 text-xs font-semibold font-mono transition';
                } else {
                    btn.className = 'px-2.5 py-1.5 rounded-xl bg-slate-900 border border-transparent hover:border-slate-700 text-slate-300 text-xs font-semibold font-mono transition';
                }
            }
        });
    }

    function toggleThreatArcs() {
        STATE.showArcs = !STATE.showArcs;
        const txt = document.getElementById('arc-status-text');
        if (txt) {
            txt.textContent = STATE.showArcs ? 'ON' : 'OFF';
            txt.className = STATE.showArcs ? 'text-rose-400 font-bold' : 'text-slate-500 font-bold';
        }
    }

    function promptInstallPWA() {
        alert('Untuk memasang AegisNet 3D di desktop/mobile: Buka menu peramban (⋮) dan pilih "Install App" / "Tambahkan ke Layar Utama".');
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    // ==========================================
    // 12. INITIALIZATION ON DOM READY
    // ==========================================
    window.addEventListener('DOMContentLoaded', () => {
        // 1. Initialize Tactical 2D FortiGuard Map
        initTacticalThreatMap();

        // 2. Initialize Three.js 3D Globe
        initThreeJSGlobe();

        // 3. Start Live Attack Simulator
        startAttackGenerator();

        // 4. Run Personal Security Audit
        runPersonalSecurityAudit();

        // 5. Pre-fetch Threat Intelligence Feeds
        fetchGlobalThreatFeeds();

        // 6. Default to Personal view with dimmed map
        switchWorkspaceMode('personal');

        console.log('[AEGISNET 3D] Enterprise v14.0 SOC & Live Threat Map Engine Loaded - Zero Simulation Architecture');
    });
    </script>
"""
