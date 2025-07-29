# Web Application Vulnerability Scanner

A simple **Web Vulnerability Scanner** built with **Python** and **Flask**.  
This tool scans target websites for common security issues and provides a user-friendly web interface for viewing results.

---

## **Features**
The scanner checks for common web vulnerabilities, including:

- **Cross-Site Scripting (XSS)**
- **SQL Injection (SQLi)**
- **Cross-Site Request Forgery (CSRF)**
- **Open Redirect**
- **Command Injection** (basic detection)

---

## **What This Project Does**
- Crawls the target website.
- Identifies forms, links, and parameters.
- Tests them using common attack payloads.
- Detects vulnerabilities by analyzing response content, reflected payloads, or error messages.

The **results** are displayed on a web dashboard with:
- Vulnerability **type**
- **URL** where the vulnerability was found
- **Severity** (High, Medium, Low)
- **Evidence** (payload used or error message)
- **Description** of the risk

---

## **How to Use This Project**

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/Paidimarrysumanjali/webapplicationscanner.git
cd webapplicationscanner
