# Scan Your Local Network for Open Ports

This repository documents the execution of **Task 1** from the Cybersecurity Internship Program of Elevate Labs. The objective of this task is to perform **network reconnaissance**, identify **open ports** on devices in the local network, analyze the **services** behind those ports, and evaluate associated **security risks**.

---

## 📌 **Objective**

- Discover live hosts in your local network.
- Identify open ports and services running on each host.
- Capture network traffic using Wireshark.
- Research the purpose and risks of each service.
- Document findings and generate professional reports.

---

## 🛠️ **Tools Used**

- **Nmap** – Network scanning and port enumeration.
- **Wireshark** – Packet capture and traffic analysis.
- **Terminal** – Executing scans and commands.

---

## 📝 **Steps Performed**

### 1. Identified Local Network Range

Used the command:

```powershell
ipconfig #for Linux use ip -a
```

Determined the subnet to scan: `192.168.XXX.0/24`.

### 2. Started Wireshark Capture

- Launched Wireshark.
- Selected the active interface (Wi‑Fi/Ethernet).
- Started packet capture during the Nmap scan.
- Saved capture as `wireshark_packet_capture.pcap`.

### 3. Performed the TCP SYN Scan

```bash
nmap -sS 192.168.XXX.0/24 -oN nmap_scan_report.txt
```

### 4. Analyzed Results

- Identified open ports on two active hosts.
- Researched the purpose of each port/service.
- Identified associated vulnerabilities and risk levels.

### 6. Documented Final Findings

Created:

- `nmap_scan_summary.md` – Detailed research & risk analysis.
- `wireshark_packet_capture.md` – Packet capture explanation.

---

## 📂 **Repository Structure**

```
Task 1/
├── nmap/
│   ├── nmap_scan_report_anonymized.txt
│   └── nmap_scan_summary.md
│
├── wireshark/
│   ├── wireshark_packet_capture_anonymized.pcap
│   ├── wireshark_packet_capture.md
│   ├── wireshark_screenshot_1.png
│   └── wireshark_screenshot_2.png
│
└── README.md

```

---

## 🔍 **Key Insights**

- Only **2 hosts** were active in the subnet.
- Multiple high-risk and critical ports were open (SMB, MSRPC, AMT).
- One host appeared to run **VMware-related services**, suggesting virtualization.
- Intel AMT exposed (`16992`) indicates potentially risky remote management access.
- DNS service running on another host requires validation of intent.

---

## 🛡️ **Security Takeaways**

- Exposed SMB and RPC services should be **restricted** and **patched**.
- Legacy protocols like NetBIOS remain **high-risk**.
- Unknown services (e.g., port `1064`) require **immediate investigation**.
- Intel AMT must be **secured**, disabled, or restricted if not required.
- Unnecessary services should be disabled to minimize the attack surface.

---

## ✔️ **Executed**

- Successfully scanned local network using Nmap.
- Captured and analyzed traffic using Wireshark.
- Identified open ports and mapped them to known services.
- Evaluated security risks and documented findings professionally.
- Saved and organized all results into structured files.

---

## 🏁 **Outcome**

- Built foundational skills in scanning local networks and identifying active hosts.
- Gained the ability to detect open ports and map them to running services.
- Understood how exposed ports reveal system behavior and potential vulnerabilities.
- Learned to assess which services are necessary and which increase the attack surface.
- Improved awareness of how attackers leverage exposed services for reconnaissance or exploitation.
- Strengthened ability to interpret scan results and translate them into actionable security recommendations.

---
