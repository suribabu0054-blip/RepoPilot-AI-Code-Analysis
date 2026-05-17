# 🔐 Security Scan Report

## 📌 Summary
The analysis identified **3 security issues** categorized by severity:
- 🔴 Critical: 1
- 🟡 Medium: 1
- 🟢 Low: 1

---

## 🔴 Command Injection (Critical)

**Description:**  
The use of `os.system()` executes shell commands directly using user input.

**Risk:**  
An attacker can inject malicious commands, leading to full system compromise.

**Example Issue:**
```python
command = "ping -c 1 " + address
os.system(command)