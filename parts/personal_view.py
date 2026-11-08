# -*- coding: utf-8 -*-

PERSONAL_VIEW = """
    <!-- Mode 1 Container: Personal Security Posture -->
    <div id="view-personal-mode" class="w-full flex-1 min-h-0 grid grid-cols-1 md:grid-cols-2 xl:flex xl:flex-row justify-between items-stretch gap-3 xl:overflow-hidden">
        
        <!-- Left Panel: Personal Defense & Hardware Audit -->
        <section class="hud-panel pointer-events-auto w-full xl:w-[410px] 2xl:w-[440px] rounded-2xl p-3 sm:p-3.5 flex flex-col gap-2.5 overflow-y-auto overflow-x-hidden shrink-0 xl:h-full order-2 md:order-2 xl:order-1">
            <div class="flex items-center justify-between border-b border-cyan-500/20 pb-2">
                <div class="flex items-center gap-2">
                    <svg class="svg-icon text-cyan-400"><use href="#ic-shield"></use></svg>
                    <h2 class="font-bold text-xs uppercase tracking-wider text-slate-200">Perimeter Keamanan Perangkat</h2>
                </div>
                <span id="user-defense-badge" class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                    REAL-TIME EDR
                </span>
            </div>

            <!-- Egress IP Card -->
            <div class="cyber-card p-3 space-y-2">
                <div class="flex items-center justify-between text-xs font-mono">
                    <span class="text-slate-400">IP Publik Egress:</span>
                    <span id="user-ip" class="text-cyan-300 font-bold tracking-wider">Memeriksa Quorum...</span>
                </div>
                <div class="flex items-center justify-between text-xs font-mono">
                    <span class="text-slate-400">Tipe Jaringan:</span>
                    <span id="user-ip-status" class="text-emerald-400 font-semibold">Residensial / Non-Proxy</span>
                </div>
                <div class="flex items-center justify-between text-xs font-mono">
                    <span class="text-slate-400">ISP / ASN:</span>
                    <span id="user-isp" class="text-slate-300 truncate max-w-[210px]">Mendeteksi Otoritas...</span>
                </div>
                <div class="flex items-center justify-between text-xs font-mono">
                    <span class="text-slate-400">Lokasi / Quorum:</span>
                    <span id="user-loc" class="text-slate-300">Indonesia (Presisi Tinggi)</span>
                </div>
            </div>

            <!-- WebRTC Deep Leak Detector Card -->
            <div class="cyber-card p-3 space-y-1.5">
                <div class="flex items-center justify-between text-xs">
                    <div class="flex items-center gap-1.5 font-semibold text-slate-200">
                        <svg class="svg-icon text-amber-400"><use href="#ic-wifi"></use></svg>
                        <span>Detektor Kebocoran WebRTC</span>
                    </div>
                    <span id="webrtc-badge" class="px-1.5 py-0.2 rounded text-[10px] font-mono bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">AMAN</span>
                </div>
                <div id="webrtc-leak-summary" class="text-[11px] font-mono text-slate-300 space-y-1 pt-1">
                    <div class="flex justify-between"><span class="text-slate-400">Kandidat Host (LAN):</span><span id="webrtc-lan-ip" class="text-slate-300">Menunggu STUN...</span></div>
                    <div class="flex justify-between"><span class="text-slate-400">Kandidat STUN Refleksif:</span><span id="webrtc-stun-ip" class="text-cyan-300">Memeriksa...</span></div>
                    <div id="webrtc-leak-verdict" class="text-[10px] text-slate-400 pt-0.5 border-t border-slate-800">Tidak ada kebocoran alamat IP lokal atau VPN bypass terdeteksi.</div>
                </div>
            </div>

            <!-- DNS Resolver & DoH Hijack Card -->
            <div class="cyber-card p-3 space-y-1.5">
                <div class="flex items-center justify-between text-xs">
                    <div class="flex items-center gap-1.5 font-semibold text-slate-200">
                        <svg class="svg-icon text-cyan-400"><use href="#ic-globe"></use></svg>
                        <span>DNS Resolver &amp; Uji Pembajakan DoH</span>
                    </div>
                    <span id="dns-badge" class="px-1.5 py-0.2 rounded text-[10px] font-mono bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">SECURE</span>
                </div>
                <div id="dns-leak-summary" class="text-[11px] font-mono text-slate-300 space-y-1 pt-1">
                    <div class="flex justify-between"><span class="text-slate-400">Cloudflare DoH (1.1.1.1):</span><span id="dns-cf-latency" class="text-emerald-400">-- ms</span></div>
                    <div class="flex justify-between"><span class="text-slate-400">Google DoH (8.8.8.8):</span><span id="dns-google-latency" class="text-emerald-400">-- ms</span></div>
                    <div class="flex justify-between"><span class="text-slate-400">Integritas DNSSEC:</span><span id="dns-sec-status" class="text-cyan-300 font-bold">TERVERIFIKASI</span></div>
                </div>
            </div>

            <!-- Device Hardware & Canvas Fingerprinting -->
            <div class="cyber-card p-3 space-y-1.5">
                <div class="flex items-center justify-between text-xs">
                    <div class="flex items-center gap-1.5 font-semibold text-slate-200">
                        <svg class="svg-icon text-purple-400"><use href="#ic-cpu"></use></svg>
                        <span>Sidik Jari Perangkat &amp; Entropi WebGL</span>
                    </div>
                    <span id="device-fp-badge" class="px-1.5 py-0.2 rounded text-[10px] font-mono bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">ENTROPY OK</span>
                </div>
                <div id="user-device-summary" class="text-[11px] font-mono text-slate-300 space-y-1 pt-1">
                    <div class="flex justify-between"><span class="text-slate-400">GPU Chipset:</span><span id="device-gpu" class="text-cyan-300 truncate max-w-[200px]">Mendeteksi GPU...</span></div>
                    <div class="flex justify-between"><span class="text-slate-400">CPU Thread / Memori:</span><span id="device-cpu" class="text-slate-300">-- Cores</span></div>
                    <div class="flex justify-between"><span class="text-slate-400">Canvas SHA-256 Hash:</span><span id="device-canvas-hash" class="text-purple-300 font-bold truncate max-w-[170px]">Menghitung...</span></div>
                </div>
            </div>

            <!-- Quick Action Toolbar -->
            <div class="grid grid-cols-3 gap-1.5 pt-1">
                <button onclick="runLiveSecurityAudit()" class="py-2 px-1 rounded-xl bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-500/40 text-cyan-200 font-semibold text-[11px] transition flex flex-col items-center justify-center gap-1">
                    <svg class="svg-icon text-cyan-300"><use href="#ic-shield"></use></svg>
                    <span>Audit Penuh</span>
                </button>
                <button onclick="testWebRtcAndDnsLeaks()" class="py-2 px-1 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700/60 text-slate-200 font-semibold text-[11px] transition flex flex-col items-center justify-center gap-1">
                    <svg class="svg-icon text-amber-300"><use href="#ic-refresh"></use></svg>
                    <span>Uji Ulang Leak</span>
                </button>
                <button onclick="fetchRealUserTelemetry(true)" class="py-2 px-1 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700/60 text-slate-200 font-semibold text-[11px] transition flex flex-col items-center justify-center gap-1">
                    <svg class="svg-icon text-emerald-300"><use href="#ic-wifi"></use></svg>
                    <span>Kalibrasi</span>
                </button>
            </div>

            <!-- Real-time Defense Status & Recommendation List -->
            <div class="space-y-1 pt-1">
                <div class="text-[10px] font-mono uppercase text-slate-400 tracking-wider">Status Sensor &amp; Rekomendasi:</div>
                <div id="heuristic-list" class="space-y-1 text-xs">
                    <!-- Dynamic findings -->
                    <div class="p-2 rounded-lg bg-emerald-950/30 border border-emerald-500/30 text-[11px] text-emerald-300 flex items-start gap-1.5">
                        <span class="text-emerald-400 font-bold">✓</span>
                        <span>Enkripsi Klien WebCrypto AES-256-GCM aktif dengan session key unik.</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- Center Viewport: Personal Telemetry & 3D Globe -->
        <div class="col-span-1 md:col-span-2 xl:flex-1 min-h-[300px] sm:min-h-[380px] xl:min-h-0 relative pointer-events-none flex flex-col justify-between items-center p-1 sm:p-2 gap-3 order-1 md:order-1 xl:order-2 min-w-0">
            <!-- Telemetry Status Pill -->
            <div class="hud-panel pointer-events-auto rounded-2xl px-4 py-2 flex flex-wrap items-center justify-center gap-3 sm:gap-6 text-xs font-mono shadow-xl bg-slate-950/80 border border-cyan-500/25">
                <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span class="text-slate-400">Node Anda:</span>
                    <strong id="pill-user-city" class="text-white">Memuat...</strong>
                </div>
                <div class="hidden sm:flex items-center gap-2">
                    <span class="text-slate-400">Perimeter:</span>
                    <span id="pill-target-info" class="text-cyan-300 font-bold">Lokal Aman</span>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-slate-400">Konsensus:</span>
                    <span id="kpi-accuracy-score" class="text-emerald-400 font-bold">100%</span>
                </div>
                <div class="hidden sm:flex items-center gap-2">
                    <span class="text-slate-400">E2EE:</span>
                    <span id="kpi-e2ee-badge" class="text-cyan-300 font-bold">AES-GCM</span>
                </div>
                <div class="hidden md:flex items-center gap-2">
                    <span class="text-slate-400">SOAR Blocked:</span>
                    <span id="kpi-blocked-count" class="text-rose-400 font-bold">0 Drop</span>
                </div>
                <div class="hidden lg:flex items-center gap-2">
                    <span class="text-slate-400">AI Model:</span>
                    <span id="kpi-ai-model-badge" class="text-purple-300 font-bold">Flash-Lite</span>
                </div>
            </div>

            <!-- Mode Notice Pill -->
            <div class="hud-panel pointer-events-auto rounded-xl px-3 py-1.5 text-[11px] font-mono text-cyan-300 bg-slate-900/80 border border-cyan-500/30 flex items-center gap-2 shadow-lg">
                <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
                <span>Mode Keamanan Pribadi: Fokus Pemantauan Integritas Perangkat &amp; Enkripsi Sesi Anda</span>
            </div>

            <!-- Camera & View Controls -->
            <div class="hud-panel pointer-events-auto rounded-2xl p-1.5 flex items-center gap-1.5 shadow-xl bg-slate-950/80 border border-cyan-500/25">
                <button id="btn-view-globe" onclick="switchViewMode('globe')" class="px-3 py-1.5 rounded-xl bg-cyan-500/20 border border-cyan-400/50 text-cyan-200 text-xs font-semibold font-mono transition flex items-center gap-1.5 shadow-[0_0_10px_rgba(0,240,255,0.25)]">
                    <svg class="svg-icon"><use href="#ic-globe"></use></svg>
                    <span>Globe 3D</span>
                </button>
                <button id="btn-view-topology" onclick="switchViewMode('topology')" class="px-3 py-1.5 rounded-xl bg-slate-900/80 border border-transparent hover:border-slate-700 text-slate-300 hover:text-white text-xs font-semibold font-mono transition flex items-center gap-1.5">
                    <svg class="svg-icon"><use href="#ic-topology"></use></svg>
                    <span>Topologi Jaringan</span>
                </button>
                <div class="w-px h-5 bg-slate-700 mx-1"></div>
                <button onclick="toggleGlobeAutoRotate()" id="btn-toggle-rotate" class="p-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white transition" title="Rotasi Otomatis">
                    <svg class="svg-icon"><use href="#ic-refresh"></use></svg>
                </button>
                <button onclick="resetCameraView()" class="p-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white transition" title="Reset Sudut Kamera">
                    <svg class="svg-icon"><use href="#ic-crosshair"></use></svg>
                </button>
            </div>
        </div>

        <!-- Right Panel: Personal Cryptography & Identity Hygiene -->
        <section class="hud-panel pointer-events-auto w-full xl:w-[410px] 2xl:w-[440px] rounded-2xl p-3 sm:p-3.5 flex flex-col gap-2.5 overflow-y-auto overflow-x-hidden shrink-0 xl:h-full order-3 md:order-3 xl:order-3">
            <div class="flex items-center justify-between border-b border-cyan-500/20 pb-2">
                <div class="flex items-center gap-2">
                    <svg class="svg-icon text-cyan-400"><use href="#ic-key"></use></svg>
                    <h2 class="font-bold text-xs uppercase tracking-wider text-slate-200">Kriptografi &amp; Higienitas Akun</h2>
                </div>
                <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40">
                    ZERO-KNOWLEDGE
                </span>
            </div>

            <!-- Zero-Knowledge WebCrypto Vault -->
            <div class="cyber-card p-3 space-y-2">
                <div class="flex items-center justify-between text-xs">
                    <div class="flex items-center gap-1.5 font-semibold text-slate-200">
                        <svg class="svg-icon text-cyan-400"><use href="#ic-lock"></use></svg>
                        <span>Brankas Enkripsi WebCrypto (AES-256-GCM)</span>
                    </div>
                    <span class="text-[10px] font-mono text-cyan-300">W3C Subtly Sealed</span>
                </div>
                <textarea id="vault-plaintext-input" rows="2" class="w-full bg-slate-950/80 border border-slate-700 rounded-lg p-2 text-xs font-mono text-slate-200 focus:outline-none focus:border-cyan-400" placeholder="Ketik teks rahasia / payload untuk dienkripsi lokal..."></textarea>
                <div class="grid grid-cols-3 gap-1.5">
                    <button onclick="encryptRealE2eePayload()" class="py-1.5 px-2 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-400/50 text-cyan-200 font-semibold text-[11px] transition">
                        Enkripsi
                    </button>
                    <button onclick="decryptRealE2eePayload()" class="py-1.5 px-2 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-600 text-slate-200 font-semibold text-[11px] transition">
                        Dekripsi
                    </button>
                    <button onclick="rotateSessionCipherKey()" class="py-1.5 px-2 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-600 text-slate-300 text-[11px] transition">
                        Rotasi Kunci
                    </button>
                </div>
                <div id="vault-cipher-output" class="text-[10px] font-mono text-slate-400 bg-slate-950 p-2 rounded border border-slate-800 break-all select-all">
                    Ciphertext terautentikasi (IV 12-byte + AES-GCM Tag) akan muncul di sini.
                </div>
            </div>

            <!-- Password Breach & Entropy Audit (HIBP k-Anonymity) -->
            <div class="cyber-card p-3 space-y-2">
                <div class="flex items-center justify-between text-xs">
                    <div class="flex items-center gap-1.5 font-semibold text-slate-200">
                        <svg class="svg-icon text-amber-400"><use href="#ic-key"></use></svg>
                        <span>Audit Kebocoran Password (HIBP k-Anonymity)</span>
                    </div>
                    <span class="text-[10px] font-mono text-amber-300">SHA-1 Prefix</span>
                </div>
                <form onsubmit="event.preventDefault(); checkPasswordBreachHIBP(); return false;" autocomplete="off" class="flex gap-1.5 w-full">
                    <input id="vault-password-input" type="password" class="flex-1 bg-slate-950/80 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs font-mono text-slate-200 focus:outline-none focus:border-amber-400" placeholder="Ketik kata sandi untuk diuji...">
                    <button type="submit" class="px-3 py-1.5 rounded-lg bg-amber-500/20 hover:bg-amber-500/30 border border-amber-500/50 text-amber-200 font-semibold text-xs transition">
                        Audit Sandi
                    </button>
                </form>
                <div id="vault-password-result" class="text-[11px] font-mono text-slate-400 bg-slate-950 p-2 rounded border border-slate-800">
                    Ketik kata sandi untuk menghitung entropi Shannon dan memeriksa apakah telah bocor di 10+ miliar record HIBP tanpa mengirim sandi ke jaringan.
                </div>
            </div>

            <!-- Email & Domain Hygiene Audit -->
            <div class="cyber-card p-3 space-y-2">
                <div class="flex items-center justify-between text-xs">
                    <div class="flex items-center gap-1.5 font-semibold text-slate-200">
                        <svg class="svg-icon text-cyan-400"><use href="#ic-globe"></use></svg>
                        <span>Audit Email &amp; Keamanan Domain (XposedOrNot)</span>
                    </div>
                </div>
                <div class="flex gap-1.5">
                    <input id="vault-email-input" type="text" class="flex-1 bg-slate-950/80 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs font-mono text-slate-200 focus:outline-none focus:border-cyan-400" placeholder="nama@email.com atau domain.com">
                    <button onclick="checkEmailAndDomainHygiene()" class="px-3 py-1.5 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-500/50 text-cyan-200 font-semibold text-xs transition">
                        Audit
                    </button>
                </div>
                <div id="vault-email-result" class="text-[11px] font-mono text-slate-400 bg-slate-950 p-2 rounded border border-slate-800">
                    Memeriksa kebocoran email publik dan rekam DNS (MX, SPF, DMARC) via Cloudflare DoH.
                </div>
            </div>

            <!-- Browser Sandbox & Privacy Audit -->
            <div class="cyber-card p-3 space-y-1.5">
                <div class="flex items-center justify-between text-xs">
                    <div class="flex items-center gap-1.5 font-semibold text-slate-200">
                        <svg class="svg-icon text-emerald-400"><use href="#ic-shield"></use></svg>
                        <span>Audit Penyimpanan Peramban &amp; Sandbox</span>
                    </div>
                    <button onclick="auditBrowserStorageAndPrivacy()" class="text-[10px] font-mono text-cyan-400 hover:underline">
                        Periksa Ulang
                    </button>
                </div>
                <div id="vault-storage-result" class="text-[11px] font-mono text-slate-300 space-y-1">
                    <div class="flex justify-between"><span class="text-slate-400">LocalStorage:</span><span id="st-local" class="text-slate-300">Tersedia (Terisolasi)</span></div>
                    <div class="flex justify-between"><span class="text-slate-400">IndexedDB:</span><span id="st-idb" class="text-slate-300">Tersedia</span></div>
                    <div class="flex justify-between"><span class="text-slate-400">Cookie Third-Party:</span><span id="st-cookie" class="text-emerald-400 font-bold">Terblokir / Terisolasi</span></div>
                </div>
            </div>

            <!-- Personal SIEM Stream -->
            <div class="flex-1 min-h-[140px] flex flex-col gap-1 pt-1">
                <div class="flex items-center justify-between text-[10px] font-mono uppercase tracking-wider text-slate-400">
                    <span>Log Aktivitas Keamanan Pribadi:</span>
                    <button onclick="clearPersonalLogs()" class="hover:text-white">Bersihkan</button>
                </div>
                <div id="packet-log-container-personal" class="flex-1 min-h-[120px] max-h-[180px] overflow-y-auto bg-slate-950/90 rounded-lg p-2 border border-slate-800 font-mono text-[10px] space-y-1">
                    <div class="text-cyan-400">[EDR-INIT] Memulai pemantauan integritas perangkat klien...</div>
                </div>
            </div>
        </section>
    </div>
"""
