# Analysis Notes - Nmap Scan

This document contains a **detailed breakdown of services**, **open ports**, and **security risks** identified during the Nmap scan executed on the subnet `192.168.XXX.XXX/24`.

Two hosts were discovered with significant open ports. Each entry below includes:

- Service explanation
- Why the service may be active
- Associated vulnerabilities
- Risk rating (Critical/High/Medium)
- Professional recommendations

---

# 🔵 Host 1:

## **Port 53/tcp — DNS (domain)**

### 📌 What This Service Does

Port 53 is used for **Domain Name System (DNS)** operations, converting domain names (e.g., google.com) into IP addresses.

### ⚙️ Why It Might Be Active

- Device is acting as a **local resolver**, DNS-forwarder, or internal router.

### 🔐 Security Risks

- **DNS amplification attacks** if the service responds to ANY external queries.
- **DNS cache poisoning** allowing redirection to malicious websites.
- **Information leakage** through zone transfers or verbose DNS responses.
- Misconfigurations may unintentionally expose internal infrastructure.

### 🛡️ Recommendations

- Restrict DNS responses to **internal trusted IPs only**.
- Disable zone transfers unless essential.
- Ensure DNSSEC or secure forwarding if supported.

### 🔥 Risk Level: **Medium**

---

# 🔵 Host 2:

This host exposes several high-risk Windows and virtualization-related services.

---

## **Port 135/tcp — Microsoft RPC (msrpc)**

### 📌 What This Service Does

MSRPC is responsible for **Windows service communications**, remote execution, COM/DCOM services, and networked management APIs.

### 🔐 Security Risks

- Historically targeted in major attacks (e.g., **MS03-026, Blaster worm**).
- Allows attackers to **enumerate Windows services**, domain info, and user accounts.
- May be exploited for remote code execution if outdated.

### 🛡️ Recommendations

- Restrict RPC to trusted internal machines only.
- Block externally via firewall.
- Ensure Windows updates are regularly applied.

### 🔥 Risk Level: **High**

---

## **Port 139/tcp — NetBIOS Session Service (netbios-ssn)**

### 📌 What This Service Does

Legacy file-sharing and name service protocol used in old Windows SMB implementations.

### 🔐 Security Risks

- Allows **share enumeration**, user listing, domain/workgroup discovery.
- Susceptible to **NTLM relay attacks**.
- Weak authentication in older implementations.

### 🛡️ Recommendations

- Disable NetBIOS if modern SMB is used.
- Block inbound NetBIOS traffic on public/untrusted networks.

### 🔥 Risk Level: **High**

---

## **Port 445/tcp — SMB (microsoft-ds)**

### 📌 What This Service Does

SMB is used for:

- File sharing
- Printer sharing
- Authentication and domain logins
- Inter-system communication

### 🔐 Security Risks

- Historically abused in major vulnerabilities like **EternalBlue (MS17-010)**.
- Primary attack vector for **WannaCry ransomware**.
- Allows enumeration of users, shares, and system policies.
- A common avenue for **lateral movement**.

### 🛡️ Recommendations

- Disable **SMBv1** entirely.
- Restrict SMB to internal LAN only.
- Apply latest Windows security patches.
- Monitor logs for suspicious SMB traffic.

### 🔥 Risk Level: **Critical**

---

## **Port 902/tcp — VMware Authentication Daemon (iss-realsecure)**

### 📌 What This Service Does

Used by **VMware Workstation / ESXi** for remote console access.

### 🔐 Security Risks

- Attackers can attempt unauthorized access to VM management.
- Outdated VMware versions may introduce vulnerabilities.
- Provides potential attacker insight into virtualization environment.

### 🛡️ Recommendations

- Allow access only from administrator systems.
- Keep VMware fully updated.

### 🔥 Risk Level: **Medium**

---

## **Port 912/tcp — VMware VIX / Apex-mesh**

### 📌 What This Service Does

Used by VMware tools for operations inside virtual machines (VIX API).

### 🔐 Security Risks

- May allow remote commands or manipulation of guest VMs.
- Attackers can query or interact with VM processes.

### 🛡️ Recommendations

- Restrict connectivity via firewall.
- Disable the service if unused.

### 🔥 Risk Level: **Medium**

---

## **Port 1064/tcp — JSTEL (Uncommon / Unknown Service)**

### 📌 What This Service Does

This port corresponds to a **non-standard or OEM application**. Unknown services often indicate:

- Vendor-specific tools
- Remote management programs
- Debug or admin interfaces
- Possible malicious implants (rare but possible)

### 🔐 Security Risks

- Unknown services = **attack surface you can't assess**.
- Could be abused as a covert channel if malicious.
- May reveal internal system information.

### 🛡️ Recommendations

- Investigate running process using:

```cmd
netstat -ano | find "1064"
```

- Disable the service if unnecessary.
- Conduct malware scan if service is suspicious.

### 🔥 Risk Level: **Medium–High**

---

## **Port 16992/tcp — Intel AMT (Active Management Technology)**

### 📌 What This Service Does

Part of Intel vPro remote management. AMT allows control of the machine even when:

- Powered off
- OS is not booted

### 🔐 Security Risks

- Known critical vulnerabilities (**INTEL-SA-00075**).
- If exposed, can allow **full system takeover**.
- Attackers may bypass OS-level security.

### 🛡️ Recommendations

- Disable Intel AMT in BIOS/UEFI if not required.
- If used, secure with strong credentials and latest firmware.
- Restrict access to AMT management ports.

### 🔥 Risk Level: **High**

---

# 🟪 Final Summary

| Port  | Service     | Risk Level   | Reason                       |
| ----- | ----------- | ------------ | ---------------------------- |
| 53    | DNS         | Medium       | Amplification, poisoning     |
| 135   | MSRPC       | High         | Remote enumeration, exploits |
| 139   | NetBIOS     | High         | NTLM relay, legacy weakness  |
| 445   | SMB         | **Critical** | EternalBlue, ransomware      |
| 902   | VMware Auth | Medium       | VM access exposure           |
| 912   | VMware VIX  | Medium       | Guest VM interaction         |
| 1064  | Unknown     | Medium–High  | Unknown service risk         |
| 16992 | Intel AMT   | High         | Remote takeover potential    |

---

# 🎯 Overall Security Recommendations

- Disable unnecessary services.
- Restrict access to management ports.
- Patch Windows and virtualization software.
- Investigate unknown ports and services.
- Harden or disable legacy protocols (NetBIOS, SMBv1).
- Implement network segmentation to limit exposure.
