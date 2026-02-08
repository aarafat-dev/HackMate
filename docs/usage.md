# Usage Guide

This guide covers the typical workflow and core operations within HackMate v2.0.

## 🏁 Engagement Workflow

### 1. Starting a New Engagement
1. Navigate to the **Engagements** page.
2. Click **New Engagement**.
3. Define your target (IP, Domain, or CIDR) and scope.
4. Once created, you will be redirected to the **Engagement Workspace**.

### 2. Following the PTES Methodology
The workspace is organized into 8 phases based on the Penetration Testing Execution Standard (PTES):
- **Phases 1-7**: Methodology guidance. Use the "MARK AS DONE" button to track progress. Completing a phase automatically moves you to the next one.
- **Phase 8**: Post-engagement record keeping.

### 3. Using the Terminal
1. Open the **Terminal** from the sidebar or engagement workspace.
2. Run standard security commands (e.g., `nmap -sV target.com`).
3. Only whitelisted commands are allowed for safety.
4. History is persisted per engagement.

### 4. Logging Findings
1. Go to the **Findings** page.
2. Select an engagement.
3. Add details for newly discovered vulnerabilities:
    - Title & Severity (Critical, High, Medium, Low, Info).
    - Description & Technical details.
    - Remediation steps & Evidence.
4. Findings are stored in the database for final reporting.

### 5. AI-Assisted Analysis
- Use the **AI Assistant** to get suggestions on exploits, methodology steps, or to explain complex tool outputs.
- Quick prompts are available to jump-start common tasks.

### 6. Generating Reports
1. Navigate to the **Reports** section.
2. Select an engagement and click **Generate Report**.
3. Choose the report type:
    - **Executive Summary**: High-level business risk focus.
    - **Technical Report**: Detailed findings, evidence, and remediation.
    - **Full Report**: Comprehensive analysis.
4. View generated reports in the **Markdown Viewer** or download them as **JSON** for external integration.
