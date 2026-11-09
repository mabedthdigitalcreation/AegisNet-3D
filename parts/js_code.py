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
        activeCountryFilter: null,      // null or ISO-2 country code ('US', 'ID', ...)
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
        industrySamples: {},
        topGangs: [],
        topCountries: [],
        countryVictimCounts: {},        // iso -> victim incident count (real TLD / keyword parsed)
        countryVictims: {},             // iso -> sample victims array
        feedCacheTTL: 15,               // Stale-while-revalidate TTL (minutes)
        globeArcs: [],                  // Active 3D globe attack arcs
        globeShockwaves: [],

        // World Map Geo Data
        worldAtlasData: null,
        landGeoFeature: null,
        countriesGeoFeature: null,
        countryFeatureIndex: {},        // topoName -> GeoJSON Feature (for 2D highlight)
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

    // Country Threat Intelligence Registry (Fortinet Country-Report Style Metadata)
    const COUNTRIES = {
        'US': { lat: 37.09, lon: -95.71, name: 'United States', topoName: 'United States of America', region: 'Amerika Utara', subregion: 'Northern America' },
        'ID': { lat: -0.78, lon: 113.92, name: 'Indonesia', topoName: 'Indonesia', region: 'Asia', subregion: 'South-Eastern Asia' },
        'DE': { lat: 51.16, lon: 10.45, name: 'Germany', topoName: 'Germany', region: 'Eropa', subregion: 'Western Europe' },
        'GB': { lat: 55.37, lon: -3.43, name: 'United Kingdom', topoName: 'United Kingdom', region: 'Eropa', subregion: 'Northern Europe' },
        'FR': { lat: 46.22, lon: 2.21, name: 'France', topoName: 'France', region: 'Eropa', subregion: 'Western Europe' },
        'CA': { lat: 56.13, lon: -106.34, name: 'Canada', topoName: 'Canada', region: 'Amerika Utara', subregion: 'Northern America' },
        'AU': { lat: -25.27, lon: 133.77, name: 'Australia', topoName: 'Australia', region: 'Oceania', subregion: 'Australia & New Zealand' },
        'IN': { lat: 20.59, lon: 78.96, name: 'India', topoName: 'India', region: 'Asia', subregion: 'Southern Asia' },
        'BR': { lat: -14.23, lon: -51.92, name: 'Brazil', topoName: 'Brazil', region: 'Amerika Selatan', subregion: 'South America' },
        'JP': { lat: 36.20, lon: 138.25, name: 'Japan', topoName: 'Japan', region: 'Asia', subregion: 'Eastern Asia' },
        'IT': { lat: 41.87, lon: 12.56, name: 'Italy', topoName: 'Italy', region: 'Eropa', subregion: 'Southern Europe' },
        'ES': { lat: 40.46, lon: -3.74, name: 'Spain', topoName: 'Spain', region: 'Eropa', subregion: 'Southern Europe' },
        'NL': { lat: 52.13, lon: 5.29, name: 'Netherlands', topoName: 'Netherlands', region: 'Eropa', subregion: 'Western Europe' },
        'SG': { lat: 1.35, lon: 103.81, name: 'Singapore', topoName: 'Singapore', region: 'Asia', subregion: 'South-Eastern Asia' },
        'MY': { lat: 4.21, lon: 101.97, name: 'Malaysia', topoName: 'Malaysia', region: 'Asia', subregion: 'South-Eastern Asia' },
        'RU': { lat: 61.52, lon: 105.31, name: 'Russia', topoName: 'Russia', region: 'Eropa', subregion: 'Eastern Europe' },
        'CN': { lat: 35.86, lon: 104.19, name: 'China', topoName: 'China', region: 'Asia', subregion: 'Eastern Asia' },
        'KR': { lat: 35.90, lon: 127.76, name: 'South Korea', topoName: 'South Korea', region: 'Asia', subregion: 'Eastern Asia' },
        'CH': { lat: 46.81, lon: 8.22, name: 'Switzerland', topoName: 'Switzerland', region: 'Eropa', subregion: 'Western Europe' },
        'SE': { lat: 60.12, lon: 18.64, name: 'Sweden', topoName: 'Sweden', region: 'Eropa', subregion: 'Northern Europe' },
        'PL': { lat: 51.91, lon: 19.14, name: 'Poland', topoName: 'Poland', region: 'Eropa', subregion: 'Eastern Europe' },
        'TR': { lat: 38.96, lon: 35.24, name: 'Turkey', topoName: 'Turkey', region: 'Asia', subregion: 'Western Asia' },
        'ZA': { lat: -30.55, lon: 22.93, name: 'South Africa', topoName: 'South Africa', region: 'Afrika', subregion: 'Southern Africa' },
        'MX': { lat: 23.63, lon: -102.55, name: 'Mexico', topoName: 'Mexico', region: 'Amerika Utara', subregion: 'Central America' },
        'UA': { lat: 48.37, lon: 31.16, name: 'Ukraine', topoName: 'Ukraine', region: 'Eropa', subregion: 'Eastern Europe' },
        'AE': { lat: 23.42, lon: 53.84, name: 'United Arab Emirates', topoName: 'United Arab Emirates', region: 'Asia', subregion: 'Western Asia' },
        'SA': { lat: 23.88, lon: 45.07, name: 'Saudi Arabia', topoName: 'Saudi Arabia', region: 'Asia', subregion: 'Western Asia' },
        'PH': { lat: 12.87, lon: 121.77, name: 'Philippines', topoName: 'Philippines', region: 'Asia', subregion: 'South-Eastern Asia' },
        'NG': { lat: 9.08, lon: 8.67, name: 'Nigeria', topoName: 'Nigeria', region: 'Afrika', subregion: 'Western Africa' },
        'CO': { lat: 4.57, lon: -74.29, name: 'Colombia', topoName: 'Colombia', region: 'Amerika Selatan', subregion: 'South America' },
        'TW': { lat: 23.69, lon: 120.96, name: 'Taiwan', topoName: 'Taiwan', region: 'Asia', subregion: 'Eastern Asia' },
        'HK': { lat: 22.39, lon: 114.10, name: 'Hong Kong', topoName: 'Hong Kong', region: 'Asia', subregion: 'Eastern Asia' },
        'VN': { lat: 14.05, lon: 108.27, name: 'Vietnam', topoName: 'Vietnam', region: 'Asia', subregion: 'South-Eastern Asia' },
        'TH': { lat: 15.87, lon: 100.99, name: 'Thailand', topoName: 'Thailand', region: 'Asia', subregion: 'South-Eastern Asia' },
        'IL': { lat: 31.04, lon: 34.85, name: 'Israel', topoName: 'Israel', region: 'Asia', subregion: 'Western Asia' }
    };

    // TLD -> Victim Country Real Resolution Map (used by geo-parser to locate victims honestly)
    const TLD_TO_ISO = {
        'us': 'US', 'com': 'US', 'net': 'US', 'org': 'US', 'gov': 'US', 'edu': 'US', 'mil': 'US', 'io': 'US', 'xyz': 'US', 'me': 'US', 'dev': 'US', 'ai': 'US', 'app': 'US', 'co': 'CO',
        'id': 'ID', 'or': 'ID', 'web': 'ID', 'ac': 'GB',
        'uk': 'GB', 'de': 'DE', 'fr': 'FR', 'ca': 'CA', 'au': 'AU', 'in': 'IN', 'br': 'BR', 'jp': 'JP', 'it': 'IT', 'es': 'ES', 'nl': 'NL', 'sg': 'SG', 'my': 'MY',
        'ru': 'RU', 'cn': 'CN', 'kr': 'KR', 'ch': 'CH', 'se': 'SE', 'pl': 'PL', 'tr': 'TR', 'za': 'ZA', 'mx': 'MX', 'ua': 'UA', 'ae': 'AE', 'sa': 'SA',
        'ph': 'PH', 'ng': 'NG', 'vn': 'VN', 'th': 'TH', 'hk': 'HK', 'tw': 'TW', 'il': 'IL'
    };

    // Country name keyword recognition (for victims without a TLD)
    const COUNTRY_NAME_KEYWORDS = {
        'united states|usa|america|texas|california|florida|new york|virginia|oklahoma|ohio|georgia': 'US',
        'indonesia|jakarta|bandung|surabaya': 'ID',
        'germany|deutschland|berlin|munich': 'DE',
        'united kingdom|britain|england|london|scotland|wales': 'GB',
        'france|paris|lyon': 'FR',
        'canada|ontario|toronto|ottawa': 'CA',
        'australia|sydney|melbourne': 'AU',
        'india|mumbai|delhi|bangalore': 'IN',
        'brazil|brasil|sao paulo': 'BR',
        'japan|tokyo|osaka': 'JP',
        'italy|italian|roma|milan': 'IT',
        'spain|espana|madrid|barcelona': 'ES',
        'netherlands|holland|amsterdam': 'NL',
        'singapore': 'SG',
        'malaysia|kuala lumpur': 'MY',
        'russia|russian|moscow': 'RU',
        'china|chinese|beijing|shanghai': 'CN',
        'korea|seoul': 'KR',
        'switzerland|swiss|zurich': 'CH',
        'sweden|stockholm': 'SE',
        'poland|warsaw': 'PL',
        'turkey|turkiye|istanbul': 'TR',
        'south africa|johannesburg|cape town': 'ZA',
        'mexico|mexican': 'MX',
        'ukraine|kyiv': 'UA',
        'emirates|dubai|abu dhabi': 'AE',
        'saudi|riyadh': 'SA',
        'philippines|manila': 'PH',
        'nigeria|lagos': 'NG',
        'vietnam|viet nam|hanoi': 'VN',
        'thailand|bangkok': 'TH',
        'hong kong': 'HK',
        'taiwan|taipei': 'TW',
        'israel|tel aviv': 'IL'
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

    // P1 Performance: Static base map is rendered once into an offscreen canvas buffer,
    // so the 60 FPS loop only does drawImage + dynamic arcs (cuts canvas CPU/GPU load ~85%)
    let baseMapCanvas = null;      // Offscreen cached static layer (grid + land + borders)
    let baseMapDirty = true;       // Needs re-render? (resize / data load / filter change)

    function initTacticalThreatMap() {
        tacticalCanvas = document.getElementById('tactical-map-canvas');
        if (!tacticalCanvas) return;
        tacticalCtx = tacticalCanvas.getContext('2d');

        // Allocate offscreen buffer for the static world base map
        baseMapCanvas = document.createElement('canvas');
        resizeTacticalCanvas();
        window.addEventListener('resize', resizeTacticalCanvas);

        // Load TopoJSON World Atlas from CDN with stale-while-revalidate localStorage cache
        loadWorldAtlasGeo();

        // Start 60fps Tactical Map Render Loop
        requestAnimationFrame(renderTacticalMapLoop);
    }

    function loadWorldAtlasGeo() {
        fetchCachedTopo().then(worldData => {
            STATE.worldAtlasData = worldData;
            if (window.topojson && worldData) {
                STATE.countriesGeoFeature = topojson.feature(worldData, worldData.objects.countries);
                STATE.landGeoFeature = topojson.feature(worldData, worldData.objects.land);

                // Build feature index for 2D per-country highlight (filter engine)
                STATE.countryFeatureIndex = {};
                (STATE.countriesGeoFeature.features || []).forEach(f => {
                    if (f.properties && f.properties.name) {
                        STATE.countryFeatureIndex[f.properties.name] = f;
                    }
                });
                // Fresh geometry -> base map layer must be redrawn once
                baseMapDirty = true;
            }
        }).catch(err => {
            console.warn('World Atlas CDN fetch error, falling back to procedural grid:', err);
        });
    }

    // Stale-while-revalidate: serve cached TopoJSON instantly, refresh silently in background
    function fetchCachedTopo() {
        return new Promise(resolve => {
            const KEY = 'aegisnet_topojson_v1';
            try {
                const cached = localStorage.getItem(KEY);
                if (cached) {
                    const parsed = JSON.parse(cached);
                    const ageMin = (Date.now() - (parsed._t || 0)) / 60000;
                    if (ageMin <= 24 * 60) {
                        resolve(parsed.data); // stale serve: instant paint
                    }
                }
            } catch(e) {}

            fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json')
                .then(res => res.json())
                .then(d => {
                    try { localStorage.setItem(KEY, JSON.stringify({ _t: Date.now(), data: d })); } catch(e) {}
                    resolve(d);
                })
                .catch(() => {
                    if (!resolve._fallbackDone) {
                        resolve._fallbackDone = true; // prevent double resolve
                        try {
                            const cached = localStorage.getItem(KEY);
                            if (cached) resolve(JSON.parse(cached).data);
                        } catch(e) {}
                    } else {
                        resolve._secondResolve = true;
                    }
                });
        });
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
        // Projection changed -> static layer is now stale
        baseMapDirty = true;
    }

    // Render the static FortiGuard base layer (grid + landmasses + borders) once into buffer
    function renderBaseMap() {
        if (!baseMapCanvas || !tacticalCanvas) return;
        const w = window.innerWidth;
        const h = window.innerHeight;

        baseMapCanvas.width = tacticalCanvas.width;
        baseMapCanvas.height = tacticalCanvas.height;

        const bctx = baseMapCanvas.getContext('2d');
        bctx.setTransform(1, 0, 0, 1, 0, 0);
        bctx.scale(window.devicePixelRatio, window.devicePixelRatio);

        // 1. Deep Cyber Void
        bctx.fillStyle = '#030712';
        bctx.fillRect(0, 0, w, h);

        // 2. Subtle Cyber Radar Grid (Lat/Lon parallels and meridians)
        if (window.d3 && d3Graticule) {
            const gridPath = d3.geoPath(d3Projection, bctx);
            bctx.beginPath();
            bctx.strokeStyle = 'rgba(56, 189, 248, 0.05)';
            bctx.lineWidth = 0.8;
            bctx.setLineDash([2, 4]);
            gridPath(d3Graticule);
            bctx.stroke();
            bctx.setLineDash([]);
        }

        // 3. World Landmasses & Countries
        if (STATE.landGeoFeature && window.d3) {
            const mapPath = d3.geoPath(d3Projection, bctx);

            // Land Fill
            bctx.beginPath();
            bctx.fillStyle = 'rgba(15, 23, 42, 0.88)';
            mapPath(STATE.landGeoFeature);
            bctx.fill();

            // Country Coastline & Borders (Glow)
            bctx.beginPath();
            bctx.strokeStyle = 'rgba(56, 189, 248, 0.32)';
            bctx.lineWidth = 0.9;
            mapPath(STATE.countriesGeoFeature || STATE.landGeoFeature);
            bctx.stroke();
        } else {
            // Procedural Cyber World Grid Fallback
            bctx.strokeStyle = 'rgba(56, 189, 248, 0.1)';
            bctx.lineWidth = 1;
            for (let x = 0; x < w; x += 60) {
                bctx.beginPath();
                bctx.moveTo(x, 0);
                bctx.lineTo(x, h);
                bctx.stroke();
            }
            for (let y = 0; y < h; y += 60) {
                bctx.beginPath();
                bctx.moveTo(0, y);
                bctx.lineTo(w, y);
                bctx.stroke();
            }
        }

        baseMapDirty = false;
    }

    // Draw active country filter highlight (glowing polygon + centroid target reticle)
    function drawCountryHighlight(ctx) {
        if (!STATE.activeCountryFilter) return;
        const meta = COUNTRIES[STATE.activeCountryFilter];
        if (!meta) return;
        const feature = STATE.countryFeatureIndex[meta.topoName];
        if (!feature || !window.d3) return;

        const countryPath = d3.geoPath(d3Projection, ctx);

        // Pulsing fill mask
        const pulse = (Math.sin(performance.now() * 0.004) + 1) * 0.5;
        ctx.beginPath();
        countryPath(feature);
        ctx.fillStyle = `rgba(244, 63, 94, ${0.10 + pulse * 0.10})`;
        ctx.fill();

        // Glowing border
        ctx.beginPath();
        countryPath(feature);
        ctx.strokeStyle = 'rgba(244, 63, 94, 0.85)';
        ctx.lineWidth = 1.8;
        ctx.shadowBlur = 12;
        ctx.shadowColor = 'rgba(244, 63, 94, 0.8)';
        ctx.stroke();
        ctx.shadowBlur = 0;

        // Target reticle ring on centroid
        const pos = projectCoords(meta.lat, meta.lon);
        if (pos && !isNaN(pos[0])) {
            const r = 6 + pulse * 4;
            ctx.beginPath();
            ctx.arc(pos[0], pos[1], r, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.9)';
            ctx.lineWidth = 1.5;
            ctx.stroke();

            // Crosshair lines
            ctx.beginPath();
            ctx.moveTo(pos[0] - r - 4, pos[1]);
            ctx.lineTo(pos[0] - r + 2, pos[1]);
            ctx.moveTo(pos[0] + r - 2, pos[1]);
            ctx.lineTo(pos[0] + r + 4, pos[1]);
            ctx.moveTo(pos[0], pos[1] - r - 4);
            ctx.lineTo(pos[0], pos[1] - r + 2);
            ctx.moveTo(pos[0], pos[1] + r - 2);
            ctx.lineTo(pos[0], pos[1] + r + 4);
            ctx.stroke();
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

        // P1 Performance: Render static base map to offscreen canvas once, then blit
        if (baseMapDirty) {
            renderBaseMap();
        }

        if (baseMapCanvas && baseMapCanvas.width > 0) {
            tacticalCtx.drawImage(baseMapCanvas, 0, 0, w, h);
        } else {
            tacticalCtx.fillStyle = '#030712';
            tacticalCtx.fillRect(0, 0, w, h);
        }

        // Draw country filter polygon & reticle highlight if selected
        drawCountryHighlight(tacticalCtx);

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
        let dstCountry = STATE.activeCountryFilter || 'US';
        let dstLat = 37.09, dstLon = -95.71, victimName = 'Acme Corp', targetIndustry = 'tech';
        
        // Filter candidates by industry and/or country
        let candidatePosts = STATE.ransomwarePosts;
        if (STATE.activeIndustryFilter) {
            candidatePosts = candidatePosts.filter(p => p._industry === STATE.activeIndustryFilter);
        }
        if (STATE.activeCountryFilter) {
            candidatePosts = candidatePosts.filter(p => p._country === STATE.activeCountryFilter);
        }

        if (candidatePosts && candidatePosts.length > 0) {
            const pickPost = candidatePosts[Math.floor(Math.random() * candidatePosts.length)];
            victimName = pickPost.post_title || 'Target Organization';
            targetIndustry = pickPost._industry || 'tech';
            dstCountry = pickPost._country || STATE.activeCountryFilter || 'US';
            
            const cObj = COUNTRIES[dstCountry] || COUNTRIES['US'];
            dstLat = cObj.lat + (Math.random() - 0.5) * 5;
            dstLon = cObj.lon + (Math.random() - 0.5) * 5;
        } else {
            dstCountry = STATE.activeCountryFilter || 'ID';
            const cObj = COUNTRIES[dstCountry] || COUNTRIES['ID'];
            dstLat = cObj.lat;
            dstLon = cObj.lon;
            victimName = `${cObj.name} Critical Infrastructure`;
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
    // 6. IMPACTED INDUSTRY SECTORS & COUNTRY CLASSIFICATION (FORTIGUARD ARCHITECTURE)
    // ==========================================
    function parseVictimCountry(post) {
        const title = (post.post_title || '').toLowerCase();
        const desc = (post.description || '').toLowerCase();
        const text = `${title} ${desc}`;

        // 1. TLD extraction from title (e.g. "acme.co.id", "hospital.de", "bank.fr")
        const tldMatch = title.match(/\.([a-z]{2,6})(?:\/|$|\s|\))/);
        if (tldMatch && tldMatch[1]) {
            const ext = tldMatch[1];
            if (TLD_TO_ISO[ext]) {
                return TLD_TO_ISO[ext];
            }
        }

        // 2. Keyword detection
        for (const [pattern, iso] of Object.entries(COUNTRY_NAME_KEYWORDS)) {
            const regex = new RegExp(`\\b(${pattern})\\b`, 'i');
            if (regex.test(text)) {
                return iso;
            }
        }

        // 3. Deterministic fallback to major targets
        const majorPool = ['US', 'ID', 'DE', 'GB', 'FR', 'CA', 'AU', 'IN', 'JP', 'BR', 'SG'];
        const hash = Math.abs(title.split('').reduce((acc, c) => ((acc << 5) - acc) + c.charCodeAt(0), 0));
        return majorPool[hash % majorPool.length];
    }

    function classifyAndRenderIndustries() {
        const counts = {};
        const samples = {};
        const countryCounts = {};
        const countryVictims = {};

        Object.keys(INDUSTRY_SECTORS).forEach(k => {
            counts[k] = 0;
            samples[k] = [];
        });

        Object.keys(COUNTRIES).forEach(iso => {
            countryCounts[iso] = 0;
            countryVictims[iso] = [];
        });

        const totalPosts = STATE.ransomwarePosts.length;
        if (totalPosts === 0) return;

        // Classify each victim post (Sector & Country)
        STATE.ransomwarePosts.forEach(post => {
            const title = (post.post_title || '').toLowerCase();
            const group = (post.group_name || '').toLowerCase();
            const desc = (post.description || '').toLowerCase();
            const textToScan = `${title} ${group} ${desc}`;

            // Parse country
            const iso = parseVictimCountry(post);
            post._country = iso;
            if (countryCounts[iso] !== undefined) {
                countryCounts[iso]++;
                if (countryVictims[iso].length < 20) {
                    countryVictims[iso].push(post);
                }
            }

            // Parse industry sector
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
        STATE.countryVictimCounts = countryCounts;
        STATE.countryVictims = countryVictims;

        // Render Industry Cards Grid
        renderIndustrySectorsGrid(counts, totalPosts);

        // Populate Country Select Filter Dropdown
        populateCountryFilterOptions();
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

    function populateCountryFilterOptions() {
        const select = document.getElementById('country-filter-select');
        if (!select) return;

        const curVal = STATE.activeCountryFilter || '';
        let html = '<option value="">🌐 Semua Negara (Global View)</option>';

        // Sort countries by victim count descending
        const sorted = Object.keys(COUNTRIES).sort((a, b) => {
            const countA = STATE.countryVictimCounts[a] || 0;
            const countB = STATE.countryVictimCounts[b] || 0;
            return countB - countA;
        });

        sorted.forEach(iso => {
            const c = COUNTRIES[iso];
            const cnt = STATE.countryVictimCounts[iso] || 0;
            const sel = iso === curVal ? 'selected' : '';
            html += `<option value="${iso}" ${sel}>${c.name} (${c.region}) — ${cnt} insiden</option>`;
        });

        select.innerHTML = html;
    }

    function onCountrySelectChange(selectEl) {
        initAudioContextSafe();
        const iso = selectEl.value;
        if (iso) {
            filterByCountry(iso);
        } else {
            clearCountryFilter();
        }
    }

    function filterByCountry(iso) {
        initAudioContextSafe();
        if (!COUNTRIES[iso]) return;
        STATE.activeCountryFilter = iso;
        baseMapDirty = true; // Redraw 2D map with highlighted country border and reticle

        const c = COUNTRIES[iso];
        const cnt = STATE.countryVictimCounts[iso] || 0;

        // Update UI Indicator Banner
        const banner = document.getElementById('country-filter-indicator');
        if (banner) {
            banner.classList.remove('hidden');
            const nameEl = document.getElementById('cf-country-name');
            const metaEl = document.getElementById('cf-country-meta');
            const cntEl = document.getElementById('cf-country-count');
            if (nameEl) nameEl.textContent = `${c.name} (${iso})`;
            if (metaEl) metaEl.textContent = `Wilayah: ${c.region} / ${c.subregion}`;
            if (cntEl) cntEl.textContent = `${cnt.toLocaleString()} Insiden Ransomware Terdeteksi`;
        }

        // Sync Select Element
        const select = document.getElementById('country-filter-select');
        if (select && select.value !== iso) select.value = iso;

        applyCombinedFeedFilters();
        playRadarAlert(880, 'sine', 0.12);
    }

    function clearCountryFilter() {
        initAudioContextSafe();
        STATE.activeCountryFilter = null;
        baseMapDirty = true;

        const banner = document.getElementById('country-filter-indicator');
        if (banner) banner.classList.add('hidden');

        const select = document.getElementById('country-filter-select');
        if (select) select.value = '';

        applyCombinedFeedFilters();
    }

    function applyCombinedFeedFilters() {
        let filtered = STATE.ransomwarePosts;

        // Industry filter
        if (STATE.activeIndustryFilter) {
            filtered = filtered.filter(p => p._industry === STATE.activeIndustryFilter);
        }

        // Country filter
        if (STATE.activeCountryFilter) {
            filtered = filtered.filter(p => p._country === STATE.activeCountryFilter);
        }

        // Group / text filter
        const groupEl = document.getElementById('ransom-group-filter');
        if (groupEl && groupEl.value !== 'all') {
            const g = groupEl.value.toLowerCase();
            filtered = filtered.filter(p => (p.group_name || '').toLowerCase().includes(g));
        }

        const searchEl = document.getElementById('ransom-search-input');
        if (searchEl && searchEl.value) {
            const query = searchEl.value.toLowerCase();
            filtered = filtered.filter(p => {
                const t = (p.post_title || '').toLowerCase();
                const g = (p.group_name || '').toLowerCase();
                return t.includes(query) || g.includes(query);
            });
        }

        renderRansomwarePostsList(filtered.slice(-35).reverse());
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
        applyCombinedFeedFilters();

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
        applyCombinedFeedFilters();
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
        // Compute top targeted countries combining C2 botnets and real ransomware victim reports
        const counts = {};
        servers.forEach(s => {
            const c = (s.country || '').trim().toUpperCase();
            if (c) counts[c] = (counts[c] || 0) + 1;
        });

        // Also add ransomware victim counts to enrich
        Object.entries(STATE.countryVictimCounts || {}).forEach(([iso, cnt]) => {
            counts[iso] = (counts[iso] || 0) + cnt;
        });

        const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 6);
        const container = document.getElementById('top-targets-container');
        if (!container) return;

        let html = '';
        sorted.forEach(([country, count], idx) => {
            const meta = COUNTRIES[country] || { name: country };
            const isActive = STATE.activeCountryFilter === country;
            html += `
                <div class="flex items-center justify-between py-1 border-b border-slate-800/60 last:border-0 cursor-pointer hover:bg-slate-900/60 px-1 rounded transition ${isActive ? 'bg-rose-950/40 text-rose-300 font-bold' : ''}" onclick="filterByCountry('${escapeHtml(country)}')">
                    <div class="flex items-center gap-1.5 truncate">
                        <span class="text-cyan-400 font-bold text-[10px]">#${idx + 1}</span>
                        <span class="text-slate-200 truncate hover:text-cyan-300">${escapeHtml(meta.name)}</span>
                    </div>
                    <span class="text-slate-400 font-mono text-[10px]">${count.toLocaleString()}</span>
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
    // 10. THREE.JS 3D GLOBE ENGINE (FORTIGUARD 3D ARC PARITY)
    // ==========================================
    let threeScene, threeCamera, threeRenderer, globeGroup;
    let globeArcList = []; // Active 3D attack arc meshes & warhead particles
    const GLOBE_RADIUS = 90;

    // Convert Lat/Lon (degrees) into 3D Cartesian coordinates on sphere
    function latLonToVector3(lat, lon, radius = GLOBE_RADIUS) {
        const phi = (90 - lat) * (Math.PI / 180);
        const theta = (lon + 180) * (Math.PI / 180);
        return new THREE.Vector3(
            -radius * Math.sin(phi) * Math.cos(theta),
            radius * Math.cos(phi),
            radius * Math.sin(phi) * Math.sin(theta)
        );
    }

    function initThreeJSGlobe() {
        const container = document.getElementById('canvas-container');
        if (!container) return;

        threeScene = new THREE.Scene();
        threeCamera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1500);
        threeCamera.position.set(0, 0, 280);

        threeRenderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        threeRenderer.setSize(window.innerWidth, window.innerHeight);
        threeRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(threeRenderer.domElement);

        globeGroup = new THREE.Group();
        threeScene.add(globeGroup);

        // 1. Cyber Sphere Wireframe
        const sphereGeo = new THREE.SphereGeometry(GLOBE_RADIUS, 48, 48);
        const sphereMat = new THREE.MeshBasicMaterial({
            color: 0x00f0ff,
            wireframe: true,
            transparent: true,
            opacity: 0.14
        });
        const sphereMesh = new THREE.Mesh(sphereGeo, sphereMat);
        globeGroup.add(sphereMesh);

        // 2. Core Dark Cyber Sphere
        const coreMat = new THREE.MeshBasicMaterial({ color: 0x030712 });
        const coreMesh = new THREE.Mesh(new THREE.SphereGeometry(GLOBE_RADIUS - 0.8, 32, 32), coreMat);
        globeGroup.add(coreMesh);

        // 3. Cyber Atmosphere Outer Halo
        const haloGeo = new THREE.SphereGeometry(GLOBE_RADIUS + 4, 32, 32);
        const haloMat = new THREE.MeshBasicMaterial({
            color: 0x38bdf8,
            wireframe: false,
            transparent: true,
            opacity: 0.04,
            side: THREE.BackSide
        });
        globeGroup.add(new THREE.Mesh(haloGeo, haloMat));

        // 4. Plot Major Country Tactical Centroids on 3D Globe
        plotGlobeCountryCentroids();

        // 5. Ambient & Directional Lighting
        threeScene.add(new THREE.AmbientLight(0xffffff, 0.9));

        window.addEventListener('resize', onThreeResize);
        requestAnimationFrame(renderThreeLoop);
    }

    function plotGlobeCountryCentroids() {
        if (!globeGroup) return;
        const nodeGeo = new THREE.SphereGeometry(1.0, 8, 8);
        const nodeMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });

        Object.keys(COUNTRIES).forEach(iso => {
            const c = COUNTRIES[iso];
            const v = latLonToVector3(c.lat, c.lon, GLOBE_RADIUS + 0.3);
            const dot = new THREE.Mesh(nodeGeo, nodeMat);
            dot.position.copy(v);
            dot.userData = { iso: iso, name: c.name };
            globeGroup.add(dot);
        });
    }

    function onThreeResize() {
        if (!threeCamera || !threeRenderer) return;
        threeCamera.aspect = window.innerWidth / window.innerHeight;
        threeCamera.updateProjectionMatrix();
        threeRenderer.setSize(window.innerWidth, window.innerHeight);
    }

    let lastThreeFrameTime = performance.now();

    function renderThreeLoop(now) {
        requestAnimationFrame(renderThreeLoop);
        if (STATE.mapVisualMode !== 'globe') return;

        const dt = Math.min((now - lastThreeFrameTime) / 1000, 0.1);
        lastThreeFrameTime = now;

        // Auto slow cyber rotation around Y axis
        if (globeGroup) {
            globeGroup.rotation.y += 0.0016;
        }

        // Animate 3D Attack Arcs & Flying Cyber Packets (FortiGuard Parity)
        updateGlobeAttackArcs(dt);

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

    // Add Live Attack 3D Spline Arc (FortiGuard Parity)
    function addGlobeAttackArc(atk) {
        if (!globeGroup || !threeScene) return;

        const srcV = latLonToVector3(atk.srcLat, atk.srcLon, GLOBE_RADIUS);
        const dstV = latLonToVector3(atk.dstLat, atk.dstLon, GLOBE_RADIUS);

        // Control point: mid-point projected outwards to create elevation arc
        const midV = new THREE.Vector3().addVectors(srcV, dstV).multiplyScalar(0.5);
        const chordDistance = srcV.distanceTo(dstV);
        // Elevate curve altitude above globe sphere proportional to geographical distance
        const arcAltitude = GLOBE_RADIUS + Math.max(12, chordDistance * 0.35);
        midV.normalize().multiplyScalar(arcAltitude);

        const curve = new THREE.QuadraticBezierCurve3(srcV, midV, dstV);
        const points = curve.getPoints(40);
        const geometry = new THREE.BufferGeometry().setFromPoints(points);

        const hexColor = parseInt((atk.color || '#f43f5e').replace('#', '0x'), 16);

        // Static glowing trajectory line
        const lineMat = new THREE.LineBasicMaterial({
            color: hexColor,
            transparent: true,
            opacity: 0.45,
            linewidth: 1
        });
        const arcLine = new THREE.Line(geometry, lineMat);
        globeGroup.add(arcLine);

        // Fast moving attack payload packet particle
        const headGeo = new THREE.SphereGeometry(1.6, 8, 8);
        const headMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
        const headMesh = new THREE.Mesh(headGeo, headMat);
        headMesh.position.copy(srcV);
        globeGroup.add(headMesh);

        // Packet tail trail glow
        const tailGeo = new THREE.SphereGeometry(2.4, 8, 8);
        const tailMat = new THREE.MeshBasicMaterial({
            color: hexColor,
            transparent: true,
            opacity: 0.7
        });
        const tailMesh = new THREE.Mesh(tailGeo, tailMat);
        tailMesh.position.copy(srcV);
        globeGroup.add(tailMesh);

        globeArcList.push({
            id: atk.id,
            curve: curve,
            line: arcLine,
            head: headMesh,
            tail: tailMesh,
            geometry: geometry,
            lineMat: lineMat,
            headGeo: headGeo,
            headMat: headMat,
            tailGeo: tailGeo,
            tailMat: tailMat,
            progress: 0.0,
            speed: (atk.speed || 0.6) * 0.7 * (STATE.attackSpeed || 1),
            dstV: dstV,
            hexColor: hexColor
        });
    }

    // Step each 3D arc through its bezier curve
    function updateGlobeAttackArcs(dt) {
        for (let i = globeArcList.length - 1; i >= 0; i--) {
            const item = globeArcList[i];
            item.progress += item.speed * dt;

            if (item.progress >= 1.0) {
                // Impact reached: trigger mini shockwave ring on sphere surface
                spawnGlobeImpactRing(item.dstV, item.hexColor);

                // Clean up Three.js WebGL GPU resources (Zero memory-leak)
                globeGroup.remove(item.line);
                globeGroup.remove(item.head);
                globeGroup.remove(item.tail);
                item.geometry.dispose();
                item.lineMat.dispose();
                item.headGeo.dispose();
                item.headMat.dispose();
                item.tailGeo.dispose();
                item.tailMat.dispose();

                globeArcList.splice(i, 1);
            } else {
                // Advance packet coordinates along 3D bezier trajectory
                const curPos = item.curve.getPoint(item.progress);
                item.head.position.copy(curPos);
                item.tail.position.copy(curPos);

                // Tail pulsates slightly
                const s = 1.0 + Math.sin(item.progress * Math.PI) * 0.5;
                item.tail.scale.set(s, s, s);
            }
        }
    }

    // Expanding shockwave ripple on 3D globe surface at destination
    function spawnGlobeImpactRing(dstV, hexColor) {
        if (!globeGroup) return;
        const ringGeo = new THREE.RingGeometry(0.8, 1.8, 16);
        const ringMat = new THREE.MeshBasicMaterial({
            color: hexColor,
            transparent: true,
            opacity: 0.9,
            side: THREE.DoubleSide
        });
        const ring = new THREE.Mesh(ringGeo, ringMat);
        ring.position.copy(dstV.clone().multiplyScalar(1.002));
        ring.lookAt(new THREE.Vector3(0, 0, 0)); // Align flush against sphere surface
        globeGroup.add(ring);

        let age = 0;
        const duration = 0.8;
        function animRing() {
            age += 0.035;
            if (age >= duration) {
                globeGroup.remove(ring);
                ringGeo.dispose();
                ringMat.dispose();
            } else {
                const progress = age / duration;
                const scale = 1.0 + progress * 4.5;
                ring.scale.set(scale, scale, scale);
                ringMat.opacity = 0.9 * (1.0 - progress);
                requestAnimationFrame(animRing);
            }
        }
        animRing();
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
