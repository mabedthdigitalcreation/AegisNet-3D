# -*- coding: utf-8 -*-

HEADER_NAV = """
<body class="bg-cyber-bg text-slate-100 min-h-screen flex flex-col justify-between selection:bg-cyan-500 selection:text-black relative antialiased">
    <!-- Scanline Texture -->
    <div class="fixed inset-0 scanline-overlay z-10 pointer-events-none"></div>

    <!-- 3D Three.js WebGL Canvas -->
    <div id="canvas-container" class="fixed inset-0 z-0 pointer-events-auto"></div>

    <!-- Floating 3D Node Tooltip Popover -->
    <div id="node-tooltip-overlay" class="hidden hud-panel rounded-xl p-3 min-w-[260px] max-w-[320px] text-xs space-y-1.5 shadow-2xl border border-rose-500/50 bg-slate-950/95">
        <div class="flex items-center justify-between border-b border-rose-500/30 pb-1.5">
            <span class="inline-flex items-center gap-1.5 font-bold text-rose-400 text-[11px] uppercase tracking-wider">
                <span class="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
                Infrastruktur Penyerang (C2)
            </span>
            <button onclick="hideNodeTooltip()" class="text-slate-400 hover:text-white px-1">✕</button>
        </div>
        <div class="space-y-1 pt-1 font-mono text-[11px]">
            <div class="flex justify-between"><span class="text-slate-400">Target IP:</span><span id="tt-ip" class="text-rose-300 font-bold">127.0.0.1:8080</span></div>
            <div class="flex justify-between"><span class="text-slate-400">Malware Family:</span><span id="tt-malware" class="text-amber-300 font-bold">Cobalt Strike</span></div>
            <div class="flex justify-between"><span class="text-slate-400">Negara:</span><span id="tt-country" class="text-cyan-300">United States</span></div>
            <div class="flex justify-between"><span class="text-slate-400">ASN:</span><span id="tt-asn" class="text-slate-300 truncate max-w-[150px]">AS14061 DigitalOcean</span></div>
            <div class="flex justify-between"><span class="text-slate-400">Status:</span><span id="tt-status" class="text-emerald-400 font-bold">ONLINE</span></div>
        </div>
        <div class="pt-2">
            <button id="tt-inspect-btn" onclick="inspectNodeFromTooltip()" class="w-full py-1.5 rounded-lg bg-rose-500/20 hover:bg-rose-500/35 border border-rose-500/50 text-rose-200 font-semibold text-[11px] transition flex items-center justify-center gap-1.5">
                <svg class="svg-icon"><use href="#ic-search"></use></svg>
                <span>Investigasi Forensik OSINT</span>
            </button>
        </div>
    </div>

    <!-- Intrusion / SOAR Banner -->
    <div id="intrusion-banner" class="hidden fixed top-0 inset-x-0 z-50 bg-rose-950/95 border-b border-rose-500/80 px-4 py-2 text-center text-xs sm:text-sm text-rose-200 backdrop-blur-md transition-all shadow-[0_4px_24px_rgba(244,63,94,0.35)]">
        <div class="max-w-7xl mx-auto flex items-center justify-between gap-3">
            <div class="flex items-center gap-2 font-mono">
                <span class="inline-block w-2.5 h-2.5 rounded-full bg-rose-400 animate-ping"></span>
                <strong class="text-rose-300">DETEKSI ANOMALI SOAR:</strong>
                <span id="intrusion-banner-text">Mencegah lalu lintas berbahaya keluar dari peramban.</span>
            </div>
            <button onclick="dismissIntrusionBanner()" class="text-xs px-2.5 py-1 rounded bg-rose-900/60 hover:bg-rose-800 text-rose-100 border border-rose-500/40">Tutup</button>
        </div>
    </div>

    <!-- Header Navigation -->
    <header class="relative z-30 px-3 sm:px-6 py-2.5 max-w-[1780px] mx-auto w-full flex flex-wrap items-center justify-between gap-2.5 border-b border-cyan-500/15 bg-slate-950/60 backdrop-blur-md">
        <!-- Logo & Brand -->
        <div class="flex items-center gap-3">
            <div class="relative flex items-center justify-center w-9 h-9 rounded-xl bg-cyan-500/10 border border-cyan-400/40 shadow-[0_0_15px_rgba(0,240,255,0.25)]">
                <svg class="svg-icon text-cyan-400 w-5 h-5"><use href="#ic-shield"></use></svg>
                <span class="absolute -bottom-0.5 -right-0.5 w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            </div>
            <div>
                <div class="flex items-center gap-2">
                    <span class="font-extrabold text-base sm:text-lg tracking-wider text-white">AEGIS<span class="text-cyan-400">NET</span> 3D</span>
                    <span class="hidden sm:inline-block px-1.5 py-0.2 rounded text-[10px] font-mono font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40">v14.0 SOC</span>
                </div>
                <div class="text-[10px] text-slate-400 font-mono tracking-tight hidden sm:block">
                    REAL-TIME ANOMALY GUARD • ZERO-SIMULATION ARCHITECTURE
                </div>
            </div>
        </div>

        <!-- Center: Dual-Mode Workspace Switcher Tabs -->
        <div class="hud-panel rounded-2xl p-1 flex items-center gap-1 shadow-lg bg-slate-900/80 border border-cyan-500/30">
            <button id="tab-mode-personal" onclick="switchWorkspaceMode('personal')" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-2 border transition border-cyan-400/80 bg-cyan-500/20 text-cyan-300 shadow-[0_0_12px_rgba(0,240,255,0.3)]">
                <svg class="svg-icon text-cyan-400"><use href="#ic-shield"></use></svg>
                <span>Keamanan Pribadi</span>
            </button>
            <button id="tab-mode-global" onclick="switchWorkspaceMode('global')" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-2 border transition border-transparent text-slate-400 hover:text-white hover:bg-slate-800/60">
                <svg class="svg-icon text-rose-400"><use href="#ic-crosshair"></use></svg>
                <span>Peristiwa Dunia (Attacker Radar)</span>
                <span class="inline-flex items-center px-1.5 py-0.2 rounded-full text-[9px] font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40 animate-pulse">LIVE</span>
            </button>
        </div>

        <!-- Right: Utility Controls & Modals -->
        <div class="flex items-center gap-1.5 sm:gap-2">
            <!-- PoP Badge -->
            <div id="cf-pop-badge-sm" class="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-slate-900/80 border border-slate-700/60 text-[11px] font-mono text-slate-300" title="Cloudflare Edge Anycast PoP">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                <span>PoP:</span>
                <span id="pop-location-sm" class="text-cyan-300 font-bold">MDC-EDGE</span>
            </div>

            <!-- Sound Alarm Toggle -->
            <button id="btn-sound-toggle" onclick="toggleSoundAlarm()" class="px-2.5 py-1.5 rounded-xl bg-slate-900/80 border border-slate-700/60 hover:border-cyan-500/50 text-slate-300 hover:text-cyan-300 text-xs font-mono transition" title="Alarm Audio">
                <span id="sound-icon">🔊</span>
            </button>

            <!-- Quick Modal Triggers -->
            <button onclick="openModal('validity-modal')" class="px-2.5 py-1.5 rounded-xl bg-slate-900/80 border border-slate-700/60 hover:border-cyan-500/50 text-slate-300 hover:text-cyan-300 text-xs font-mono transition flex items-center gap-1" title="Laboratorium Validitas Multi-Sensor">
                <svg class="svg-icon text-cyan-400"><use href="#ic-award"></use></svg>
                <span class="hidden lg:inline">Validitas</span>
            </button>

            <button onclick="openModal('firewall-modal')" class="px-2.5 py-1.5 rounded-xl bg-slate-900/80 border border-slate-700/60 hover:border-rose-500/50 text-slate-300 hover:text-rose-300 text-xs font-mono transition flex items-center gap-1" title="Generator Skrip Firewall & SOAR">
                <svg class="svg-icon text-rose-400"><use href="#ic-firewall"></use></svg>
                <span class="hidden lg:inline">Firewall</span>
            </button>

            <button onclick="openModal('ai-copilot-modal')" class="px-2.5 py-1.5 rounded-xl bg-cyan-500/15 border border-cyan-400/50 hover:bg-cyan-500/25 text-cyan-200 text-xs font-semibold font-mono transition flex items-center gap-1.5 shadow-[0_0_12px_rgba(0,240,255,0.2)]">
                <svg class="svg-icon text-cyan-300"><use href="#ic-sparkle"></use></svg>
                <span>AI SOC</span>
            </button>

            <!-- PWA Install -->
            <button id="btn-install-pwa" onclick="promptInstallPWA()" class="hidden px-2 py-1.5 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-xs font-mono transition" title="Pasang Aplikasi PWA">
                <svg class="svg-icon"><use href="#ic-download"></use></svg>
            </button>
        </div>
    </header>
"""
