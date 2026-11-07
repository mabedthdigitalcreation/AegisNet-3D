# -*- coding: utf-8 -*-

GLOBAL_VIEW = """
    <!-- Mode 2 Container: Global Threat Intelligence Radar -->
    <div id="view-global-mode" class="hidden w-full flex-1 min-h-0 grid grid-cols-1 md:grid-cols-2 xl:flex xl:flex-row justify-between items-stretch gap-3 xl:overflow-hidden">
        
        <!-- Left Panel: Live Attacker & Ransomware Stream -->
        <section class="hud-panel pointer-events-auto w-full xl:w-[410px] 2xl:w-[440px] rounded-2xl p-3 sm:p-3.5 flex flex-col gap-2.5 overflow-y-auto overflow-x-hidden shrink-0 xl:h-full order-2 md:order-2 xl:order-1">
            <div class="flex items-center justify-between border-b border-rose-500/20 pb-2">
                <div class="flex items-center gap-2">
                    <svg class="svg-icon text-rose-400"><use href="#ic-crosshair"></use></svg>
                    <h2 class="font-bold text-xs uppercase tracking-wider text-slate-200">Peristiwa Hacker &amp; Ransomware</h2>
                </div>
                <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40">
                    <span class="w-1.5 h-1.5 rounded-full bg-rose-500 animate-ping"></span>
                    LIVE FEED
                </span>
            </div>

            <!-- Feed Filter Bar -->
            <div class="cyber-card p-2.5 space-y-2">
                <div class="flex items-center justify-between text-[11px] font-mono text-slate-400">
                    <span>Filter Grup Ransomware:</span>
                    <button onclick="fetchGlobalThreatFeeds(true)" class="text-cyan-400 hover:underline flex items-center gap-1">
                        <svg class="svg-icon w-3 h-3"><use href="#ic-refresh"></use></svg>
                        <span>Sinkronkan Ulang</span>
                    </button>
                </div>
                <select id="ransom-group-filter" onchange="filterRansomwarePosts()" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs font-mono text-slate-200 focus:outline-none focus:border-rose-400">
                    <option value="all">Semua Kelompok Hacker / Geng Pemeras</option>
                    <option value="lockbit3">LockBit 3.0</option>
                    <option value="ransomhub">RansomHub</option>
                    <option value="play">Play Ransomware</option>
                    <option value="akira">Akira</option>
                    <option value="medusa">Medusa</option>
                    <option value="blacksuit">BlackSuit</option>
                    <option value="bianlian">BianLian</option>
                    <option value="rhysida">Rhysida</option>
                    <option value="handala">Handala Hack</option>
                    <option value="qilin">Qilin</option>
                </select>
                <div class="relative">
                    <input id="ransom-search-input" oninput="filterRansomwarePosts()" type="text" placeholder="Cari nama korban organisasi atau sektor industri..." class="w-full bg-slate-950 border border-slate-700 rounded-lg pl-8 pr-2.5 py-1.5 text-xs font-mono text-slate-200 focus:outline-none focus:border-rose-400">
                    <svg class="svg-icon text-slate-500 absolute left-2.5 top-2.5 w-3.5 h-3.5"><use href="#ic-search"></use></svg>
                </div>
            </div>

            <!-- Feed 1: Ransomware Live Extortion Feed -->
            <div class="space-y-1.5 flex-1 min-h-[220px] flex flex-col">
                <div class="flex items-center justify-between text-[10px] font-mono uppercase tracking-wider text-slate-400">
                    <span class="flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full bg-rose-500"></span>
                        <span>Korban Ransomware Terkini (Ransomwatch):</span>
                    </span>
                    <span id="ransom-feed-count" class="text-rose-400 font-bold">Memuat...</span>
                </div>
                <div id="ransom-posts-container" class="flex-1 min-h-[180px] max-h-[300px] overflow-y-auto space-y-1.5 pr-1 font-mono text-xs">
                    <div class="p-3 rounded-lg bg-slate-950/60 border border-slate-800 text-slate-400 animate-pulse text-center">
                        Mengambil feed langsung dari 100+ situs leak ransomware dunia...
                    </div>
                </div>
            </div>

            <!-- Feed 2: CISA Known Exploited Vulnerabilities (KEV) -->
            <div class="space-y-1.5 pt-2 border-t border-slate-800 flex-1 min-h-[160px] flex flex-col">
                <div class="flex items-center justify-between text-[10px] font-mono uppercase tracking-wider text-slate-400">
                    <span class="flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full bg-amber-400"></span>
                        <span>Eksploitasi Zero-Day Aktif (CISA KEV):</span>
                    </span>
                    <span id="cisa-kev-count" class="text-amber-300 font-bold">Memuat...</span>
                </div>
                <div id="cisa-kev-container" class="flex-1 min-h-[140px] max-h-[220px] overflow-y-auto space-y-1.5 pr-1 font-mono text-[11px]">
                    <div class="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800 text-slate-400 animate-pulse text-center">
                        Memuat katalog kerentanan aktif dieksploitasi penyerang...
                    </div>
                </div>
            </div>
        </section>

        <!-- Center Viewport: Global Threat Radar & 3D C2 Cloud -->
        <div class="col-span-1 md:col-span-2 xl:flex-1 min-h-[300px] sm:min-h-[380px] xl:min-h-0 relative pointer-events-none flex flex-col justify-between items-center p-1 sm:p-2 gap-3 order-1 md:order-1 xl:order-2 min-w-0">
            <!-- Global Telemetry Status Pill -->
            <div class="hud-panel pointer-events-auto rounded-2xl px-4 py-2 flex flex-wrap items-center justify-center gap-3 sm:gap-6 text-xs font-mono shadow-xl bg-slate-950/80 border border-rose-500/25">
                <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
                    <span class="text-slate-400">C2 Botnet Aktif:</span>
                    <strong id="pill-global-c2-count" class="text-rose-400 font-bold">Memuat...</strong>
                </div>
                <div class="hidden sm:flex items-center gap-2">
                    <span class="text-slate-400">Serangan Ransomware:</span>
                    <span id="pill-global-ransom-count" class="text-amber-400 font-bold">Memuat...</span>
                </div>
                <div class="hidden md:flex items-center gap-2">
                    <span class="text-slate-400">KEV Zero-Days:</span>
                    <span id="pill-global-kev-count" class="text-cyan-300 font-bold">Memuat...</span>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-slate-400">Feed Sync:</span>
                    <span id="pill-global-feed-status" class="text-emerald-400 font-bold">LIVE HTTP</span>
                </div>
            </div>

            <!-- Mode Notice Pill -->
            <div class="hud-panel pointer-events-auto rounded-xl px-3 py-1.5 text-[11px] font-mono text-rose-300 bg-slate-950/90 border border-rose-500/40 flex items-center gap-2 shadow-lg">
                <span class="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span>
                <span>Radar Ancaman Dunia: Menampilkan ratusan server C2 nyata &amp; vektor serangan cyber melintasi benua</span>
            </div>

            <!-- Global Camera & Threat Filter Controls -->
            <div class="hud-panel pointer-events-auto rounded-2xl p-1.5 flex items-center gap-1.5 shadow-xl bg-slate-950/80 border border-rose-500/25">
                <button onclick="filterC2Display('all')" id="btn-c2-all" class="px-2.5 py-1.5 rounded-xl bg-rose-500/20 border border-rose-500/50 text-rose-200 text-xs font-semibold font-mono transition">
                    Semua C2
                </button>
                <button onclick="filterC2Display('online')" id="btn-c2-online" class="px-2.5 py-1.5 rounded-xl bg-slate-900 border border-transparent hover:border-slate-700 text-slate-300 text-xs font-semibold font-mono transition">
                    Hanya Online
                </button>
                <button onclick="filterC2Display('cobalt')" id="btn-c2-cobalt" class="px-2.5 py-1.5 rounded-xl bg-slate-900 border border-transparent hover:border-slate-700 text-slate-300 text-xs font-semibold font-mono transition">
                    Cobalt Strike
                </button>
                <div class="w-px h-5 bg-slate-700 mx-1"></div>
                <button onclick="toggleThreatArcs()" id="btn-toggle-arcs" class="px-2.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white text-xs font-mono transition" title="Tampilkan / Sembunyikan Vektor Serangan">
                    Arc: <span id="arc-status-text" class="text-rose-400 font-bold">ON</span>
                </button>
                <button onclick="resetCameraView()" class="p-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white transition" title="Reset Sudut Kamera">
                    <svg class="svg-icon"><use href="#ic-crosshair"></use></svg>
                </button>
            </div>
        </div>

        <!-- Right Panel: Attacker Infrastructure & OSINT Forensic Scanner -->
        <section class="hud-panel pointer-events-auto w-full xl:w-[410px] 2xl:w-[440px] rounded-2xl p-3 sm:p-3.5 flex flex-col gap-2.5 overflow-y-auto overflow-x-hidden shrink-0 xl:h-full order-3 md:order-3 xl:order-3">
            <div class="flex items-center justify-between border-b border-rose-500/20 pb-2">
                <div class="flex items-center gap-2">
                    <svg class="svg-icon text-rose-400"><use href="#ic-terminal"></use></svg>
                    <h2 class="font-bold text-xs uppercase tracking-wider text-slate-200">Pelacak Attacker &amp; Forensik OSINT</h2>
                </div>
                <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40">
                    LIVE RECON
                </span>
            </div>

            <!-- Target IP / Domain Input Bar -->
            <div class="cyber-card p-3 space-y-2">
                <div class="flex items-center justify-between text-xs font-mono">
                    <span class="text-slate-400">Target Investigasi:</span>
                    <span class="text-cyan-300">Shodan • BGP • Quorum</span>
                </div>
                <div class="flex gap-1.5">
                    <input id="custom-ip-input" type="text" placeholder="IP v4/v6 atau domain penyerang..." class="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs font-mono text-slate-200 focus:outline-none focus:border-cyan-400">
                    <button onclick="trackCustomIP()" class="px-3 py-1.5 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-500/50 text-cyan-200 font-semibold text-xs font-mono transition flex items-center gap-1">
                        <svg class="svg-icon"><use href="#ic-search"></use></svg>
                        <span>Lacak</span>
                    </button>
                </div>
                <!-- Quick Suggestion Tags -->
                <div class="flex flex-wrap gap-1 text-[10px] font-mono pt-1">
                    <span class="text-slate-500">Preset C2:</span>
                    <button onclick="quickFillIP('162.243.103.246')" class="px-1.5 py-0.5 rounded bg-slate-800 text-rose-300 hover:bg-slate-700">Cobalt-US</button>
                    <button onclick="quickFillIP('185.220.101.5')" class="px-1.5 py-0.5 rounded bg-slate-800 text-amber-300 hover:bg-slate-700">Tor-Exit</button>
                    <button onclick="quickFillIP('45.33.32.156')" class="px-1.5 py-0.5 rounded bg-slate-800 text-cyan-300 hover:bg-slate-700">Shodan-Scan</button>
                    <button onclick="quickFillIP('1.1.1.1')" class="px-1.5 py-0.5 rounded bg-slate-800 text-emerald-300 hover:bg-slate-700">CF-DNS</button>
                </div>
            </div>

            <!-- Target Forensic Dossier Details -->
            <div class="cyber-card p-3 space-y-2 text-xs font-mono">
                <div class="flex items-center justify-between border-b border-slate-800 pb-1">
                    <span class="text-slate-400">Target Host / IP:</span>
                    <strong id="target-ip-display" class="text-rose-300 font-bold select-all tracking-wider">Menunggu Target...</strong>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-slate-400">Reverse DNS (PTR):</span>
                    <span id="target-ptr-display" class="text-slate-300 truncate max-w-[200px]">--</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-slate-400">Abuse Contact Email:</span>
                    <span id="target-abuse-display" class="text-cyan-300 truncate max-w-[200px]">--</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-slate-400">ISP / Organisasi:</span>
                    <span id="target-asn-display" class="text-slate-300 truncate max-w-[200px]">--</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-slate-400">Lokasi / Negara:</span>
                    <span id="target-geo-display" class="text-slate-300">--</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-slate-400">BGP Prefix (CIDR):</span>
                    <span id="target-bgp-display" class="text-slate-300">--</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-slate-400">Jarak Geodesik &amp; RTT:</span>
                    <span id="target-distance-display" class="text-amber-300">-- km (~-- ms)</span>
                </div>
                <!-- Shodan InternetDB Info -->
                <div class="pt-1 border-t border-slate-800 space-y-1">
                    <div class="flex items-center justify-between">
                        <span class="text-slate-400 font-bold">Port Terbuka (Shodan):</span>
                        <span id="target-ports-display" class="text-rose-400 font-bold">--</span>
                    </div>
                    <div class="flex items-center justify-between">
                        <span class="text-slate-400 font-bold">Kerentanan CVE Terdeteksi:</span>
                        <span id="target-cves-display" class="text-amber-300 font-bold">--</span>
                    </div>
                </div>
            </div>

            <!-- Forensic Action Buttons -->
            <div class="grid grid-cols-3 gap-1.5 pt-1">
                <button onclick="openFirewallModal()" class="py-2 px-1 rounded-xl bg-rose-500/20 hover:bg-rose-500/30 border border-rose-500/50 text-rose-200 font-semibold text-[11px] font-mono transition flex flex-col items-center justify-center gap-1">
                    <svg class="svg-icon text-rose-300"><use href="#ic-firewall"></use></svg>
                    <span>Skrip Firewall</span>
                </button>
                <button onclick="exportForensicReport()" class="py-2 px-1 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-600 text-slate-200 font-semibold text-[11px] font-mono transition flex flex-col items-center justify-center gap-1">
                    <svg class="svg-icon text-cyan-300"><use href="#ic-download"></use></svg>
                    <span>Unduh JSON</span>
                </button>
                <button onclick="analyzeTargetWithGemini()" class="py-2 px-1 rounded-xl bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-500/40 text-cyan-200 font-semibold text-[11px] font-mono transition flex flex-col items-center justify-center gap-1">
                    <svg class="svg-icon text-purple-300"><use href="#ic-sparkle"></use></svg>
                    <span>AI Analisis</span>
                </button>
            </div>

            <!-- Live C2 Infrastructure List -->
            <div class="space-y-1.5 pt-1 flex-1 min-h-[140px] flex flex-col">
                <div class="flex items-center justify-between text-[10px] font-mono uppercase tracking-wider text-slate-400">
                    <span>Server C2 Terdeteksi Terkini:</span>
                    <span id="c2-list-count" class="text-rose-400 font-bold">Memuat...</span>
                </div>
                <div id="c2-server-list-container" class="flex-1 min-h-[120px] max-h-[180px] overflow-y-auto space-y-1 pr-1 font-mono text-[11px]">
                    <div class="p-2 rounded bg-slate-950/60 border border-slate-800 text-slate-400 text-center animate-pulse">
                        Memuat data C2 tracker global...
                    </div>
                </div>
            </div>

            <!-- Global Threat SIEM Stream -->
            <div class="flex-1 min-h-[120px] flex flex-col gap-1 pt-1 border-t border-slate-800">
                <div class="flex items-center justify-between text-[10px] font-mono uppercase tracking-wider text-slate-400">
                    <span>Terminal Intelijen Serangan Global:</span>
                    <button onclick="clearGlobalLogs()" class="hover:text-white">Bersihkan</button>
                </div>
                <div id="packet-log-container-global" class="flex-1 min-h-[100px] max-h-[150px] overflow-y-auto bg-slate-950/90 rounded-lg p-2 border border-slate-800 font-mono text-[10px] space-y-1">
                    <div class="text-rose-400">[THREAT-SYNC] Menghubungkan ke jaringan feed ancaman global...</div>
                </div>
            </div>
        </section>
    </div>
"""
