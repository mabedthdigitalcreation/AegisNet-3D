# -*- coding: utf-8 -*-

MODALS = """
    <!-- Modals Container -->
    
    <!-- 1. AI Copilot Modal -->
    <div id="ai-copilot-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-950/80 backdrop-blur-md">
        <div class="hud-panel w-full max-w-2xl rounded-2xl p-4 sm:p-6 space-y-4 max-h-[90vh] flex flex-col border border-cyan-500/30 bg-slate-950">
            <div class="flex items-center justify-between border-b border-cyan-500/20 pb-3">
                <div class="flex items-center gap-2">
                    <svg class="svg-icon text-cyan-400 w-5 h-5"><use href="#ic-sparkle"></use></svg>
                    <h3 class="font-bold text-sm sm:text-base text-white">Gemini AI SOC Co-Pilot (Live Analyst)</h3>
                </div>
                <button onclick="closeModal('ai-copilot-modal')" class="text-slate-400 hover:text-white px-2 py-1">✕</button>
            </div>
            
            <div class="flex-1 overflow-y-auto space-y-3 pr-1 text-xs">
                <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-slate-300">
                    <span class="font-semibold text-cyan-300">Asisten Intelijen SOC:</span>
                    Menganalisis anomali jaringan, korelasi C2 penyerang, kerentanan CVE tereksploitasi, dan memberikan rekomendasi mitigasi taktis.
                </div>
                
                <div class="space-y-1.5">
                    <label class="text-[11px] font-mono text-slate-400">Pertanyaan / Instruksi Analisis:</label>
                    <textarea id="ai-user-query" rows="3" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-xs font-mono text-slate-200 focus:outline-none focus:border-cyan-400" placeholder="Contoh: Analisis IP C2 Cobalt Strike 162.243.103.246 dan berikan rekomendasi blokir di firewall enterprise."></textarea>
                </div>

                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2">
                        <span class="text-[11px] font-mono text-slate-400">Model:</span>
                        <span class="px-2 py-0.5 rounded bg-slate-800 text-purple-300 font-mono text-[10px]">gemini-2.5-flash-lite / Heuristic Engine</span>
                    </div>
                    <button onclick="askQuickGemini()" id="btn-ask-gemini" class="px-4 py-2 rounded-xl bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-400/50 text-cyan-200 font-semibold text-xs font-mono transition flex items-center gap-2">
                        <svg class="svg-icon text-cyan-300"><use href="#ic-sparkle"></use></svg>
                        <span>Jalankan Analisis</span>
                    </button>
                </div>

                <div class="space-y-1.5 pt-2">
                    <div class="flex items-center justify-between text-[11px] font-mono text-slate-400">
                        <span>Hasil Laporan Analisis:</span>
                        <button onclick="copyAiOutput()" class="text-cyan-400 hover:underline">Salin Laporan</button>
                    </div>
                    <div id="ai-response-output" class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 text-xs font-mono text-slate-200 min-h-[140px] max-h-[260px] overflow-y-auto whitespace-pre-wrap">
                        Klik 'Jalankan Analisis' atau 'AI Analisis' pada target penyerang untuk menghasilkan dossier investigasi otomatis.
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 2. Validity Lab Modal -->
    <div id="validity-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-950/80 backdrop-blur-md">
        <div class="hud-panel w-full max-w-2xl rounded-2xl p-4 sm:p-6 space-y-4 max-h-[90vh] flex flex-col border border-cyan-500/30 bg-slate-950">
            <div class="flex items-center justify-between border-b border-cyan-500/20 pb-3">
                <div class="flex items-center gap-2">
                    <svg class="svg-icon text-cyan-400 w-5 h-5"><use href="#ic-award"></use></svg>
                    <h3 class="font-bold text-sm sm:text-base text-white">Laboratorium Validitas Multi-Sensor (Zero-Simulation)</h3>
                </div>
                <button onclick="closeModal('validity-modal')" class="text-slate-400 hover:text-white px-2 py-1">✕</button>
            </div>
            
            <div class="flex-1 overflow-y-auto space-y-3 pr-1 text-xs">
                <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-slate-300 leading-relaxed">
                    Sistem ini menguji konsensus multi-sensor independen untuk memverifikasi akurasi data tanpa menggunakan mock data palsu:
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] font-mono">
                    <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 space-y-1">
                        <div class="text-cyan-300 font-bold">1. IP Quorum Consensus</div>
                        <div class="text-slate-400">Membandingkan egress IP dari ipwho.is, ipify.org, dan RIPE Stat secara paralel.</div>
                    </div>
                    <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 space-y-1">
                        <div class="text-amber-300 font-bold">2. WebRTC STUN Probe</div>
                        <div class="text-slate-400">Mengumpulkan kandidat ICE riil via Google &amp; Cloudflare STUN server.</div>
                    </div>
                    <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 space-y-1">
                        <div class="text-emerald-300 font-bold">3. DNS-over-HTTPS (DoH)</div>
                        <div class="text-slate-400">Mengukur latensi RTT riil ke Cloudflare (1.1.1.1) dan Google (8.8.8.8).</div>
                    </div>
                    <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 space-y-1">
                        <div class="text-purple-300 font-bold">4. Shodan InternetDB</div>
                        <div class="text-slate-400">Pengecekan port terbuka dan kerentanan CVE terverifikasi dari pemindaian Shodan.</div>
                    </div>
                </div>

                <div class="pt-2">
                    <button onclick="runLiveAccuracyBenchmark()" class="w-full py-2.5 rounded-xl bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-400/50 text-cyan-200 font-semibold font-mono text-xs transition">
                        Jalankan Benchmark Konsensus Sekarang
                    </button>
                </div>

                <div id="validity-benchmark-output" class="p-3 rounded-xl bg-slate-900 border border-slate-800 font-mono text-xs text-slate-300 space-y-1 min-h-[100px]">
                    <div class="text-slate-400">Klik tombol di atas untuk menjalankan pengujian kuorum live...</div>
                </div>
            </div>
        </div>
    </div>

    <!-- 3. Firewall Script Generator Modal -->
    <div id="firewall-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-950/80 backdrop-blur-md">
        <div class="hud-panel w-full max-w-2xl rounded-2xl p-4 sm:p-6 space-y-4 max-h-[90vh] flex flex-col border border-rose-500/30 bg-slate-950">
            <div class="flex items-center justify-between border-b border-rose-500/20 pb-3">
                <div class="flex items-center gap-2">
                    <svg class="svg-icon text-rose-400 w-5 h-5"><use href="#ic-firewall"></use></svg>
                    <h3 class="font-bold text-sm sm:text-base text-white">Generator Skrip Mitigasi Firewall (SOAR)</h3>
                </div>
                <button onclick="closeModal('firewall-modal')" class="text-slate-400 hover:text-white px-2 py-1">✕</button>
            </div>
            
            <div class="flex-1 overflow-y-auto space-y-3 pr-1 text-xs">
                <div class="flex items-center justify-between font-mono text-xs">
                    <span class="text-slate-400">IP Target Pemblokiran:</span>
                    <strong id="fw-target-ip" class="text-rose-400 font-bold select-all">127.0.0.1</strong>
                </div>

                <div class="flex flex-wrap gap-1.5 font-mono text-xs">
                    <button onclick="switchFirewallPlatform('ufw')" id="btn-fw-ufw" class="px-2.5 py-1 rounded-lg bg-rose-500/20 text-rose-200 border border-rose-500/40 font-semibold">Linux UFW</button>
                    <button onclick="switchFirewallPlatform('iptables')" id="btn-fw-iptables" class="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white">iptables</button>
                    <button onclick="switchFirewallPlatform('nftables')" id="btn-fw-nftables" class="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white">nftables</button>
                    <button onclick="switchFirewallPlatform('windows')" id="btn-fw-windows" class="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white">Windows PowerShell</button>
                    <button onclick="switchFirewallPlatform('cloudflare')" id="btn-fw-cloudflare" class="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white">Cloudflare WAF</button>
                </div>

                <div class="relative">
                    <pre id="firewall-script-output" class="p-3 rounded-xl bg-slate-900 border border-slate-800 font-mono text-[11px] text-rose-300 overflow-x-auto min-h-[140px] whitespace-pre-wrap"></pre>
                    <button onclick="copyFirewallScript()" class="absolute top-2.5 right-2.5 px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 font-mono text-[10px] border border-slate-700 flex items-center gap-1">
                        <svg class="svg-icon w-3 h-3"><use href="#ic-copy"></use></svg>
                        <span id="copy-fw-text">Salin Skrip</span>
                    </button>
                </div>

                <div class="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800 text-[11px] text-slate-400 leading-relaxed font-mono">
                    💡 <em>Skrip ini dapat dieksekusi langsung di server gateway, router, atau sistem operasi Anda untuk memblokir seluruh lalu lintas ingress/egress dari IP penyerang terkait.</em>
                </div>
            </div>
        </div>
    </div>

    <!-- 4. Defense Pillars Modal -->
    <div id="defense-pillars-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-950/80 backdrop-blur-md">
        <div class="hud-panel w-full max-w-2xl rounded-2xl p-4 sm:p-6 space-y-4 max-h-[90vh] flex flex-col border border-cyan-500/30 bg-slate-950">
            <div class="flex items-center justify-between border-b border-cyan-500/20 pb-3">
                <div class="flex items-center gap-2">
                    <svg class="svg-icon text-cyan-400 w-5 h-5"><use href="#ic-shield"></use></svg>
                    <h3 class="font-bold text-sm sm:text-base text-white">Arsitektur Pertahanan &amp; SOAR AegisNet 3D</h3>
                </div>
                <button onclick="closeModal('defense-pillars-modal')" class="text-slate-400 hover:text-white px-2 py-1">✕</button>
            </div>
            
            <div class="flex-1 overflow-y-auto space-y-3 pr-1 text-xs">
                <div class="space-y-2">
                    <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                        <strong class="text-cyan-300 font-semibold">1. Zero-Knowledge E2EE Vault (AES-256-GCM):</strong>
                        <p class="text-slate-400">Kunci enkripsi dihasilkan langsung menggunakan Web Cryptography API W3C di memori peramban klien. Tidak ada teks terbuka yang meninggalkan komputer Anda.</p>
                    </div>
                    <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                        <strong class="text-rose-400 font-semibold">2. SOAR In-Memory Runtime Firewall:</strong>
                        <p class="text-slate-400">Mengintersepsi fungsi fetch(), XMLHttpRequest, dan sendBeacon() secara real-time. Jika aplikasi mencoba berkomunikasi dengan IP yang terdaftar sebagai penyerang berbahaya, transmisi langsung di-DROP.</p>
                    </div>
                    <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                        <strong class="text-amber-300 font-semibold">3. Feed Attacker &amp; Hacker Dunia (Ransomwatch + C2 Tracker):</strong>
                        <p class="text-slate-400">Sinkronisasi langsung dengan feed OSINT terbuka (Ransomwatch, C2 tracker, CISA KEV) dengan header CORS terbuka, menyajikan data serangan aktual 24/7.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 5. Toast Notifications Container -->
    <div id="toast-box" class="fixed bottom-4 right-4 z-50 space-y-2 pointer-events-none"></div>
"""
