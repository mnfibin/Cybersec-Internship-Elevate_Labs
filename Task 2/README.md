# 🔎🛡️ Phishing Email Analysis

This repository contains a detailed analysis report of a phishing email designed to impersonate Microsoft Security Notifications. The purpose of this task is to study phishing indicators, recognize common social-engineering techniques, and build awareness for detecting fraudulent emails.

## 📚 Contents

- **Phishing_Mail_Report.docx** — A comprehensive report analyzing a phishing email claiming "Unusual Sign-In Activity" on a Microsoft account.

- **microsoft_phishing_template_sample.eml** — The email template used for the task.

## ✨ Overview

An email claiming "Unusual Sign‑In Activity" for a Microsoft account was analyzed. The message attempted to trick recipients into clicking a malicious link and handing over credentials. This README summarizes the findings, indicators, methodology, and recommended actions.

## 🛠️ Methodology

1. **📧 Sender Validation** — compared displayed sender address with official Microsoft senders.

2. **🧾 Email Header Inspection** — analyzed raw headers for SPF, DKIM, DMARC, return-path, IP and hops.

3. **🔗 Link & URL Analysis** — hovered links, followed redirect chains, captured destination URLs.

4. **🧐 Content Analysis** — looked for urgency, grammar errors, spoofed formatting, and misleading instructions.

5. **📸 Evidence Collection** — screenshots of header analyzer output and hovered-link previews.

6. **🧾 Consolidation** — compiled indicators into the final verdict.

## 🚩 Key Phishing Indicators

### 1. ✉️ Spoofed Sender Address

- **Displayed:** `noreply@account.microsoft.com` (looks legitimate but is forged).

### 2. 🔐 Authentication Failures (Headers)

- **SPF** = none (sending IP not authorized)
- **DKIM** = none (no cryptographic signature)
- **DMARC** = fail
- **Return‑Path** = `bounce@nonkfrgr.co.uk` (unrelated/suspicious)

→ Strong evidence email didn't originate from Microsoft.

### 3. 🔗 Malicious Redirect Links

- **Visible CTA:** "Report The User"
- **Actual redirect:** `https://microsoft-security-alert.com/verify` (fraudulent credential harvest site).

### 4. ⏳ Urgency & Fear Tactics

- Claims of login from "Russia/Moscow" to force quick action.

### 5. 🔀 Mismatched URLs / Link Text

- Displayed link text imitates Microsoft branding but href points to a different domain.

### 6. ✍️ Grammar & Formatting Errors

- **Examples:** "sign.in" instead of "sign‑in", awkward sentence structure, inconsistent capitalization.
- Large providers rarely leave such errors in security alerts.

## ✅ Final Verdict

Because of sender spoofing, failed SPF/DKIM/DMARC checks, malicious redirect links, and fear-driven social engineering — **this email is conclusively a phishing attempt**.

**Action:** DO NOT click links, DO NOT enter credentials, and REPORT the email. 🚫🔗🛑

## 🛡️ Practical Tips to Avoid Phishing

- **🔍 Verify Sender Address** — check full domain spelling and legitimacy.
- **🖱️ Hover Before You Click** — inspect the actual href; on mobile, long‑press to preview.
- **🧾 Check SPF / DKIM / DMARC** — header results reveal spoofing.
- **✍️ Look for Typos** — grammar/formatting errors are red flags.
- **🔒 Never Share Credentials via Email** — legitimate providers will never ask for your password.
- **🚨 Be Skeptical of Urgent Messages** — attackers weaponize urgency.
- **🌐 Cross‑Verify on Official Sites** — manually type account.microsoft.com instead of following an email link.
- **🔐 Enable MFA** — protects accounts even if passwords leak.

## 🛠️ Additional Cybersecurity Recommendations

- Keep antivirus/antimalware updated. 🧯
- Use browser phishing protection and link scanners. 🧩
- Regularly review account activity logs for unknown sign‑ins. 📊
- Report suspicious emails to your provider and organization. 📣
- Learn to read raw email headers for deeper investigations. 🧠

## 📢 Reporting & Next Steps (If you received this email)

1. **❌ Do not click links or open attachments.**
2. **📨 Report the email** using your mail provider's "Report phishing" option and notify your security team.
3. **🔐 If you used the link or suspect compromise** — change your password from a trusted device and enable MFA.
4. **🗂️ Preserve the original email and headers** for investigation or law enforcement if required.

## 🎯 Learning Outcomes

This exercise helps you become proficient at:

- Spotting spoofed sender identities 🕵️
- Interpreting SPF/DKIM/DMARC results 📜
- Tracing malicious URLs and redirect chains 🔗
- Recognizing social engineering patterns (urgency, fear) 🧠
- Performing structured phishing investigations 🧾

---

## 📝 License

This project is for educational purposes only. Use this analysis to improve your cybersecurity awareness and help others identify phishing attempts.
