# Attack Surface Framework
version 1 of the surface mitigation effort


## Overview
The Attack Surface Framework discovers assets, detects vulnerabilities, and provides detailed reports. It integrates with multiple tools and platforms for comprehensive analysis and reporting.

---

## Features
1. **Asset Discovery**:
   - Network assets (Nmap)
   - Cloud resources (AWS)
   - API endpoints (Swagger/OpenAPI)

2. **Plug-ins**:
   - Port scanning
   - Vulnerability detection

3. **Reporting**:
   - CSV, JSON, and PDF reports
   - Integration with Splunk and Elasticsearch

4. **Dashboard**:
   - Interactive web interface using Flask and Chart.js.

---

## Reporting Configuration

### 1. CSV and JSON Reports
Reports are automatically saved to the `reports/output/` directory.

### 2. PDF Report
Requires `fpdf`:
```bash
pip install fpdf
