# AegisNet 3D — Enterprise Cyber Defense Operations & Global Threat Intelligence

[![Deployment](https://img.shields.io/badge/Cloudflare_Pages-Auto_Deploy-F38020?style=for-the-badge&logo=cloudflare&logoColor=white)](https://pages.cloudflare.com)
[![Architecture](https://img.shields.io/badge/Architecture-Zero_Simulation-00F0FF?style=for-the-badge)](https://mabedthdigitalcreation.my.id)
[![Engine](https://img.shields.io/badge/Three.js-r128_WebGL-10B981?style=for-the-badge&logo=threedotjs&logoColor=white)](https://threejs.org)
[![Author](https://img.shields.io/badge/Developed_by-Mabedth_Digital_Creation-8B5CF6?style=for-the-badge)](https://mabedthdigitalcreation.my.id)

AegisNet 3D adalah platform intelijen keamanan siber dan visualisasi 3D real-time berstandar Enterprise Security Operations Center (SOC). Seluruh fitur beroperasi **100% menggunakan data telemetri nyata, sensor langsung, dan feed ancaman global tanpa manipulasi simulasi atau mock dummy**.

---

## 🛡️ Arsitektur Dual-Workspace UI/UX

AegisNet 3D dirancang dengan pemisahan kerja yang intuitif dan tegas antara keamanan perangkat personal dan pemantauan ancaman global:

### 1. Mode Keamanan Pribadi (Personal Security Posture)
Fokus pada audit postur keamanan perangkat lokal pengguna, kerahasiaan data, dan pencegahan kebocoran identitas jaringan:
- **Egress IP Quorum Sensor**: Konsensus multi-source real-time (`ipify`, `ipwho.is`) untuk mendeteksi alamat IP publik, ISP, ASN, dan geolokasi akurat.
- **Deteksi Kebocoran WebRTC STUN**: Pengujian kandidat ICE (`srflx` & `host`) via STUN Google (`stun.l.google.com:19302`) untuk memverifikasi apakah VPN mengalami kebocoran IP lokal/publik.
- **Audit Pembajakan DNS DoH**: Pengujian resolusi DNS-over-HTTPS Cloudflare (1.1.1.1) dan Google (8.8.8.8) secara paralel dengan metrik latensi ms riil.
- **Hardware & WebGL Fingerprint Entropy**: Deteksi GPU Renderer, CPU Core concurrency, dan kalkulasi SHA-256 canvas fingerprinting.
- **Client-Side WebCrypto AES-256-GCM Vault**: Enkripsi dan dekripsi payload data/teks terisolasi di sisi browser dengan IV 12-byte acak dan rotasi kunci kriptografis instan.
- **k-Anonymity Credential Breach Checker**: Pemeriksaan kata sandi via SHA-1 prefix Have I Been Pwned (HIBP) API tanpa pernah mengirimkan kata sandi asli pengguna.
- **Domain & Email Hygiene**: Pemeriksaan rekam otoritatif MX, SPF, dan DMARC anti-spoofing via DoH.

### 2. Mode Radar Peristiwa Dunia (Global Threat Intelligence Radar)
Fokus pada pemantauan hacker, kelompok penyerang siber, dan infrastruktur malware aktif di seluruh dunia:
- **Ransomwatch Live Attacker Feed**: Feed live 21.000+ catatan insiden ransomware (LockBit, RansomHub, Play, BlackCat, Akira) dengan filter kelompok hacker dan pencarian entitas korban.
- **CISA KEV Exploited Vulnerabilities**: Kerentanan zero-day dan CVE yang telah dikonfirmasi dieksploitasi di dunia nyata secara aktif oleh aktor ancaman.
- **Pelacak Infrastruktur Botnet C2**: Pemetaan server Command & Control (Cobalt Strike, Mirai, AsyncRAT) dengan status online/offline dan koordinat geografis nyata.
- **Three.js 3D Interactive Cyber Globe**: Visualisasi bola dunia 3D berbasis WebGL dengan simpul C2 yang dapat diklik (*raycasting popover*), rotasi dinamis, dan garis lengkung serangan (*attack arcs*) antar wilayah.

---

## ⚡ SOAR & Skrip Mitigasi Firewall

Dilengkapi generator mitigasi satu klik untuk mengisolasi penyerang atau IP mencurigakan ke berbagai infrastruktur keamanan:
- **Linux UFW**: `sudo ufw insert 1 deny from <IP> to any`
- **Linux iptables**: `sudo iptables -I INPUT -s <IP> -j DROP`
- **Linux nftables**: `sudo nft add rule inet filter input ip saddr <IP> drop`
- **Windows Defender Firewall**: PowerShell cmdlets `New-NetFirewallRule`
- **Cloudflare WAF**: Ekspresi filter rule blocking edge

---

## 🚀 Integrasi & Deployment

- **Hosting**: Auto-deploy ke **Cloudflare Pages** setiap ada commit baru pada branch `main`.
- **Zero Build Step**: Monolitik HTML5, Tailwind CSS, Three.js, dan Web APIs murni tanpa kompilasi server yang rumit.
- **Modular Build Engine**: Source code tersusun modular di direktori `parts/` dan dirakit menggunakan `build.py`.

---

## 🏢 Tentang Pengembang

Dikembangkan dengan dedikasi tinggi oleh **Mabedth Digital Creation** ([mabedthdigitalcreation.my.id](https://mabedthdigitalcreation.my.id)).
