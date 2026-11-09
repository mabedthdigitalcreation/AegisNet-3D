# -*- coding: utf-8 -*-

GLOBAL_VIEW = """
    <!-- Mode 2 Container: Global Threat Intelligence Radar (FortiGuard Style Threat Map) -->
    <div id="view-global-mode" class="hidden w-full flex-1 min-h-0 flex flex-col xl:flex-row justify-between items-stretch gap-2.5 p-1 sm:p-2 overflow-y-auto xl:overflow-hidden relative z-20">
        
        <!-- Left Panel: Impacted Industry Sectors & Top Attacker Syndicates -->
        <section class="hud-panel pointer-events-auto w-full xl:w-[390px] 2xl:w-[420px] rounded-2xl p-3 flex flex-col gap-2.5 overflow-y-auto shrink-0 xl:h-full order-2 xl:order-1 bg-slate-950/85">
            <!-- Header -->
            <div class="flex items-center justify-between border-b border-rose-500/20 pb-2">
                <div class="flex items-center gap-2">
                    <svg class="svg-icon text-rose-400"><use href="#ic-crosshair"></use></svg>
                    <h2 class="font-bold text-xs uppercase tracking-wider text-slate-200">Intelijen Ancaman Global</h2>
                </div>
                <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40">
                    <span class="w-1.5 h-1.5 rounded-full bg-rose-500 animate-ping"></span>
                    FORTIGUARD RADAR
                </span>
            </div>

            <!-- SECTION 1: SEKTOR INDUSTRI TERDAMPAK (Impacted Industry Sectors Breakdown) -->
            <div class="cyber-card p-3 space-y-2 border-rose-500/30">
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-1.5">
                        <svg class="svg-icon text-amber-400 w-4 h-4"><use href="#ic-topology"></use></svg>
                        <h3 class="font-bold text-xs text-slate-200 tracking-wide">Sektor Industri Terdampak</h3>
                    </div>
                    <span id="active-industry-filter-badge" class="hidden px-2 py-0.5 rounded text-[9px] font-mono font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 cursor-pointer" onclick="clearIndustryFilter()" title="Klik untuk menghapus filter">
                        Filter Aktif ✕
                    </span>
                </div>
                <p class="text-[10px] text-slate-400 font-mono">
                    Klasifikasi telemetri real-time 8 sektor ekonomi &amp; infrastruktur kritis dari 16.000+ insiden ransomwatch &amp; CISA KEV:
                </p>

                <!-- Industry Grid (8 Core Sectors) -->
                <div id="industry-sectors-container" class="grid grid-cols-2 gap-1.5 pt-1">
                    <!-- Populated dynamically via JS -->
                    <div class="col-span-2 text-center text-xs text-slate-400 py-3 animate-pulse font-mono">
                        Mengklasifikasikan sektor industri terdampak...
                    </div>
                </div>

                <div class="pt-1 flex items-center justify-between text-[10px] font-mono text-slate-400 border-t border-slate-800">
                    <span>Klik sektor untuk memfilter peta</span>
                    <button onclick="clearIndustryFilter()" class="text-cyan-400 hover:underline">Tampilkan Semua</button>
                </div>
            </div>

            <!-- SECTION 2: TOP HACKER GANGS & TARGET COUNTRIES -->
            <div class="grid grid-cols-2 gap-2">
                <!-- Top Gangs -->
                <div class="cyber-card p-2.5 space-y-1.5">
                    <div class="flex items-center justify-between text-[10px] font-mono uppercase text-slate-300 font-bold border-b border-slate-800 pb-1">
                        <span class="text-rose-400">Grup Hacker Teraktif</span>
                    </div>
                    <div id="top-gangs-container" class="space-y-1 text-[11px] font-mono max-h-[140px] overflow-y-auto pr-1">
                        <div class="text-slate-500 text-center py-2 text-[10px]">Memuat data sindikat...</div>
                    </div>
                </div>

                <!-- Top Target Countries -->
                <div class="cyber-card p-2.5 space-y-1.5">
                    <div class="flex items-center justify-between text-[10px] font-mono uppercase text-slate-300 font-bold border-b border-slate-800 pb-1">
                        <span class="text-cyan-400">Negara Target Utama</span>
                    </div>
                    <div id="top-targets-container" class="space-y-1 text-[11px] font-mono max-h-[140px] overflow-y-auto pr-1">
                        <div class="text-slate-500 text-center py-2 text-[10px]">Memetakan negara target...</div>
                    </div>
                </div>
            </div>

            <!-- SECTION 3: RANSOMWARE FEED FILTER & SEARCH -->
            <div class="cyber-card p-2.5 space-y-2">
                <div class="flex items-center justify-between text-[11px] font-mono text-slate-400">
                    <span>Telusuri Korban &amp; Pelaku:</span>
                    <button onclick="fetchGlobalThreatFeeds(true)" class="text-cyan-400 hover:underline flex items-center gap-1">
                        <svg class="svg-icon w-3 h-3"><use href="#ic-refresh"></use></svg>
                        <span>Sync Feed</span>
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
                    <input id="ransom-search-input" oninput="filterRansomwarePosts()" type="text" placeholder="Cari nama organisasi, domain, atau industri..." class="w-full bg-slate-950 border border-slate-700 rounded-lg pl-8 pr-2.5 py-1.5 text-xs font-mono text-slate-200 focus:outline-none focus:border-rose-400">
                    <svg class="svg-icon text-slate-500 absolute left-2.5 top-2.5 w-3.5 h-3.5"><use href="#ic-search"></use></svg>
                </div>
            </div>

            <!-- Feed 1: Ransomware Live Extortion Feed -->
            <div class="space-y-1.5 flex-1 min-h-[160px] flex flex-col">
                <div class="flex items-center justify-between text-[10px] font-mono uppercase tracking-wider text-slate-400">
                    <span class="flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full bg-rose-500"></span>
                        <span>Korban Ransomware Terkini:</span>
                    </span>
                    <span id="ransom-feed-count" class="text-rose-400 font-bold">Memuat...</span>
                </div>
                <div id="ransom-posts-container" class="flex-1 min-h-[140px] max-h-[220px] overflow-y-auto space-y-1.5 pr-1 font-mono text-xs">
                    <div class="p-3 rounded-lg bg-slate-950/60 border border-slate-800 text-slate-400 animate-pulse text-center text-[11px]">
                        Mengambil feed langsung dari 100+ situs leak ransomware dunia...
                    </div>
                </div>
            </div>

            <!-- Feed 2: CISA Known Exploited Vulnerabilities (KEV) -->
            <div class="space-y-1.5 pt-2 border-t border-slate-800 flex-1 min-h-[140px] flex flex-col">
                <div class="flex items-center justify-between text-[10px] font-mono uppercase tracking-wider text-slate-400">
                    <span class="flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full bg-amber-400"></span>
                        <span>Eksploitasi Zero-Day Aktif (CISA KEV):</span>
                    </span>
                    <span id="cisa-kev-count" class="text-amber-300 font-bold">Memuat...</span>
                </div>
                <div id="cisa-kev-container" class="flex-1 min-h-[120px] max-h-[180px] overflow-y-auto space-y-1.5 pr-1 font-mono text-[11px]">
                    <div class="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800 text-slate-400 animate-pulse text-center">
                        Memuat katalog kerentanan aktif dieksploitasi penyerang...
                    </div>
                </div>
            </div>
        </section>

        <!-- Center Viewport: Threat Map HUD Overlay & Live Stream Ticker -->
        <div class="flex-1 min-h-[460px] xl:min-h-0 relative pointer-events-none flex flex-col justify-between items-center p-1 sm:p-2 gap-2.5 order-1 xl:order-2 min-w-0">
            <!-- Top Floating HUD: Real-time Telemetry Status Bar & Country Filter -->
            <div class="hud-panel pointer-events-auto rounded-2xl px-3 py-2 flex flex-wrap items-center justify-between gap-2.5 text-xs font-mono shadow-2xl bg-slate-950/90 border border-rose-500/30 w-full max-w-5xl">
                <div class="flex flex-wrap items-center gap-2 sm:gap-4 md:gap-5">
                    <div class="flex items-center gap-1.5">
                        <span class="w-2.5 h-2.5 rounded-full bg-rose-500 animate-ping"></span>
                        <span class="text-slate-400">Laju:</span>
                        <strong id="hdr-attack-rate" class="text-rose-400 font-bold tracking-wider">3.8 /dtk</strong>
                    </div>
                    <div class="flex items-center gap-1.5">
                        <span class="text-slate-400">Total:</span>
                        <strong id="hdr-total-attacks" class="text-amber-300 font-bold">0</strong>
                    </div>
                    <div class="hidden sm:flex items-center gap-1.5">
                        <span class="text-slate-400">C2 Server:</span>
                        <strong id="pill-global-c2-count" class="text-rose-400 font-bold">176</strong>
                    </div>
                    <div class="hidden md:flex items-center gap-1.5">
                        <span class="text-slate-400">Ransomware:</span>
                        <span id="pill-global-ransom-count" class="text-amber-400 font-bold">16,072</span>
                    </div>
                    <div class="hidden lg:flex items-center gap-1.5">
                        <span class="text-slate-400">KEV:</span>
                        <span id="pill-global-kev-count" class="text-cyan-300 font-bold">1,210</span>
                    </div>
                    <div class="flex items-center gap-1.5">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                        <span id="pill-global-feed-status" class="text-emerald-400 font-bold text-[11px]">FEED SYNCED</span>
                    </div>
                </div>

                <!-- FortiGuard Country Filter Dropdown -->
                <div class="flex items-center gap-1.5 ml-auto">
                    <span class="text-rose-300 font-bold text-[11px] flex items-center gap-1">
                        <svg class="svg-icon w-3.5 h-3.5 text-rose-400"><use href="#ic-crosshair"></use></svg>
                        <span>Filter Negara:</span>
                    </span>
                    <select id="country-filter-select" onchange="onCountrySelectChange(this)" class="bg-slate-900 border border-rose-500/40 rounded-lg px-2.5 py-1 text-xs font-mono text-slate-100 focus:outline-none focus:border-rose-400 max-w-[210px] cursor-pointer">
                        <option value="">🌐 Semua Negara (Global View)</option>
                        <option value="US">United States (Amerika Utara)</option>
                        <option value="ID">Indonesia (Asia)</option>
                        <option value="DE">Germany (Eropa)</option>
                        <option value="GB">United Kingdom (Eropa)</option>
                        <option value="FR">France (Eropa)</option>
                        <option value="CA">Canada (Amerika Utara)</option>
                        <option value="AU">Australia (Oceania)</option>
                        <option value="IN">India (Asia)</option>
                        <option value="BR">Brazil (Amerika Selatan)</option>
                        <option value="JP">Japan (Asia)</option>
                        <option value="SG">Singapore (Asia)</option>
                    </select>
                </div>
            </div>

            <!-- Country Filter Active Indicator Banner (FortiGuard Telemetry HUD) -->
            <div id="country-filter-indicator" class="hidden hud-panel pointer-events-auto rounded-xl px-4 py-2 text-xs font-mono bg-rose-950/80 border border-rose-500/60 shadow-[0_0_20px_rgba(244,63,94,0.3)] backdrop-blur-md flex flex-wrap items-center justify-between gap-3 w-full max-w-3xl transition">
                <div class="flex items-center gap-2.5">
                    <span class="w-3 h-3 rounded-full bg-rose-500 animate-ping"></span>
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="text-white font-bold tracking-wide" id="cf-country-name">Indonesia (ID)</span>
                            <span class="px-1.5 py-0.2 rounded text-[9px] bg-rose-500/30 text-rose-200 border border-rose-500/50 uppercase font-bold">RADAR TERKUNCI</span>
                        </div>
                        <div class="text-[11px] text-rose-200/80 flex items-center gap-3 mt-0.5">
                            <span id="cf-country-meta">Wilayah: Asia / South-Eastern Asia</span>
                            <span>&bull;</span>
                            <span id="cf-country-count" class="text-amber-300 font-bold">Memetakan insiden...</span>
                        </div>
                    </div>
                </div>
                <button onclick="clearCountryFilter()" class="px-2.5 py-1 rounded-lg bg-rose-500/20 hover:bg-rose-500/40 border border-rose-500/50 text-rose-100 text-xs font-mono font-bold transition flex items-center gap-1">
                    <span>Hapus Filter</span>
                    <span>✕</span>
                </button>
            </div>

            <!-- Center Reticle / Notice Badge -->
            <div class="hud-panel pointer-events-auto rounded-xl px-3 py-1.5 text-[11px] font-mono text-cyan-200 bg-slate-950/85 border border-cyan-500/30 flex items-center gap-2 shadow-lg backdrop-blur-md">
                <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
                <span id="tactical-map-mode-label">Peta Taktis 2D FortiGuard Aktif &bull; Mengamati vektor serangan cyber antar benua secara real-time</span>
            </div>

            <!-- Bottom Floating HUD: Map Controls & Live Cyber Attack Stream (FortiGuard Style Ticker) -->
            <div class="w-full max-w-5xl space-y-2 pointer-events-auto">
                <!-- Tactical Map Control Bar -->
                <div class="hud-panel rounded-2xl p-1.5 px-3 flex flex-wrap items-center justify-between gap-2 shadow-2xl bg-slate-950/90 border border-slate-700/60">
                    <div class="flex items-center gap-1.5">
                        <button onclick="toggleAttackStream()" id="btn-stream-toggle" class="px-2.5 py-1 rounded-xl bg-rose-500/20 hover:bg-rose-500/30 border border-rose-500/40 text-rose-200 text-xs font-mono font-bold flex items-center gap-1 transition">
                            <span id="stream-toggle-icon">⏸</span>
                            <span id="stream-toggle-text">Jeda Stream</span>
                        </button>
                        <div class="w-px h-4 bg-slate-700 mx-1"></div>
                        <span class="text-[11px] font-mono text-slate-400 hidden sm:inline">Kecepatan:</span>
                        <button onclick="setAttackSpeed(1)" id="btn-speed-1" class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-cyan-500/30 text-cyan-300 border border-cyan-500/50">1x</button>
                        <button onclick="setAttackSpeed(2)" id="btn-speed-2" class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-800 text-slate-400 hover:text-white">2x</button>
                        <button onclick="setAttackSpeed(5)" id="btn-speed-5" class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-800 text-slate-400 hover:text-white">5x</button>
                    </div>

                    <!-- Attack Legend -->
                    <div class="flex items-center gap-2 sm:gap-3 text-[10px] font-mono">
                        <div class="flex items-center gap-1">
                            <span class="w-2 h-2 rounded-full bg-rose-500 shadow-[0_0_6px_rgba(244,63,94,0.8)]"></span>
                            <span class="text-rose-300">Ransomware</span>
                        </div>
                        <div class="flex items-center gap-1">
                            <span class="w-2 h-2 rounded-full bg-amber-400 shadow-[0_0_6px_rgba(245,158,11,0.8)]"></span>
                            <span class="text-amber-300">Botnet C2</span>
                        </div>
                        <div class="flex items-center gap-1">
                            <span class="w-2 h-2 rounded-full bg-cyan-400 shadow-[0_0_6px_rgba(0,240,255,0.8)]"></span>
                            <span class="text-cyan-300">KEV Zero-Day</span>
                        </div>
                        <div class="flex items-center gap-1">
                            <span class="w-2 h-2 rounded-full bg-purple-400 shadow-[0_0_6px_rgba(168,85,247,0.8)]"></span>
                            <span class="text-purple-300">DDoS / Port</span>
                        </div>
                    </div>

                    <!-- Reset View -->
                    <button onclick="resetMapView()" class="p-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-mono transition" title="Pusatkan Kembali Tampilan Peta">
                        <svg class="svg-icon w-3.5 h-3.5"><use href="#ic-crosshair"></use></svg>
                    </button>
                </div>

                <!-- Live Cyber Attack Stream (FortiGuard Ticker Table) -->
                <div class="hud-panel rounded-2xl p-2.5 shadow-2xl bg-slate-950/95 border border-rose-500/25">
                    <div class="flex items-center justify-between pb-1.5 border-b border-slate-800 text-[10px] font-mono uppercase tracking-wider">
                        <span class="flex items-center gap-1.5 text-rose-300 font-bold">
                            <span class="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
                            Live Cyber Attack Stream (Real-Time Telemetry):
                        </span>
                        <div class="flex items-center gap-2">
                            <span id="stream-active-filter-label" class="text-slate-400 text-[9px]">Semua Industri</span>
                            <button onclick="clearAttackStreamLogs()" class="text-slate-500 hover:text-slate-300">Hapus</button>
                        </div>
                    </div>
                    <div id="live-attack-ticker-container" class="space-y-1 font-mono text-[11px] max-h-[105px] overflow-y-auto pr-1">
                        <div class="text-slate-500 text-center py-2 text-xs">Menunggu transmisi vektor serangan live...</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Right Panel: Attacker Infrastructure & OSINT Forensic Scanner -->
        <section class="hud-panel pointer-events-auto w-full xl:w-[390px] 2xl:w-[420px] rounded-2xl p-3 flex flex-col gap-2.5 overflow-y-auto shrink-0 xl:h-full order-3 xl:order-3 bg-slate-950/85">
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
                <form onsubmit="event.preventDefault(); trackCustomIP(); return false;" autocomplete="off" class="flex gap-1.5 w-full">
                    <input id="custom-ip-input" type="text" placeholder="IP v4/v6 atau domain penyerang..." class="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs font-mono text-slate-200 focus:outline-none focus:border-cyan-400">
                    <button type="submit" class="px-3 py-1.5 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-500/50 text-cyan-200 font-semibold text-xs font-mono transition flex items-center gap-1">
                        <svg class="svg-icon"><use href="#ic-search"></use></svg>
                        <span>Lacak</span>
                    </button>
                </form>
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
            <div class="space-y-1.5 pt-1 flex-1 min-h-[120px] flex flex-col">
                <div class="flex items-center justify-between text-[10px] font-mono uppercase tracking-wider text-slate-400">
                    <span>Server C2 Terdeteksi Terkini:</span>
                    <span id="c2-list-count" class="text-rose-400 font-bold">Memuat...</span>
                </div>
                <div id="c2-server-list-container" class="flex-1 min-h-[100px] max-h-[160px] overflow-y-auto space-y-1 pr-1 font-mono text-[11px]">
                    <div class="p-2 rounded bg-slate-950/60 border border-slate-800 text-slate-400 text-center animate-pulse">
                        Memuat data C2 tracker global...
                    </div>
                </div>
            </div>

            <!-- Global Threat SIEM Stream -->
            <div class="flex-1 min-h-[100px] flex flex-col gap-1 pt-1 border-t border-slate-800">
                <div class="flex items-center justify-between text-[10px] font-mono uppercase tracking-wider text-slate-400">
                    <span>Terminal Intelijen Serangan Global:</span>
                    <button onclick="clearGlobalLogs()" class="hover:text-white">Bersihkan</button>
                </div>
                <div id="packet-log-container-global" class="flex-1 min-h-[90px] max-h-[130px] overflow-y-auto bg-slate-950/90 rounded-lg p-2 border border-slate-800 font-mono text-[10px] space-y-1">
                    <div class="text-rose-400">[THREAT-SYNC] Menghubungkan ke jaringan feed ancaman global...</div>
                </div>
            </div>
        </section>
    </div>
"""
