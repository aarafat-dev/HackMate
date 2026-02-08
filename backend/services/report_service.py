"""
HackMate v2.0 - Report Service
Report generation utilities.
"""

from typing import List, Dict, Any
from datetime import datetime


class ReportService:
    """
    Report generation service.
    
    Provides utilities for generating different report types.
    Most heavy lifting is done by AIService, this handles formatting.
    """
    
    @staticmethod
    def format_executive_summary(
        engagement_name: str,
        target: str,
        findings: List[Any],
        start_date: datetime = None,
        end_date: datetime = None
    ) -> str:
        """Generate executive summary section."""
        # Count findings by severity
        severity_counts = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        }
        
        for f in findings:
            sev = f.severity if hasattr(f, 'severity') else 'info'
            if sev in severity_counts:
                severity_counts[sev] += 1
        
        total = len(findings)
        risk_score = (
            severity_counts["critical"] * 10 +
            severity_counts["high"] * 7 +
            severity_counts["medium"] * 4 +
            severity_counts["low"] * 1
        )
        
        if risk_score == 0:
            risk_level = "Low"
            risk_color = "🟢"
        elif risk_score < 20:
            risk_level = "Medium"
            risk_color = "🟡"
        elif risk_score < 50:
            risk_level = "High"
            risk_color = "🟠"
        else:
            risk_level = "Critical"
            risk_color = "🔴"
        
        return f"""## Executive Summary

### Engagement Overview

| Attribute | Value |
|-----------|-------|
| **Engagement Name** | {engagement_name} |
| **Target** | {target} |
| **Assessment Date** | {start_date or datetime.now().strftime('%Y-%m-%d')} |
| **Overall Risk** | {risk_color} {risk_level} (Score: {risk_score}) |

### Findings Summary

| Severity | Count | Percentage |
|----------|-------|------------|
| 🔴 Critical | {severity_counts['critical']} | {(severity_counts['critical']/max(1,total)*100):.1f}% |
| 🟠 High | {severity_counts['high']} | {(severity_counts['high']/max(1,total)*100):.1f}% |
| 🟡 Medium | {severity_counts['medium']} | {(severity_counts['medium']/max(1,total)*100):.1f}% |
| 🟢 Low | {severity_counts['low']} | {(severity_counts['low']/max(1,total)*100):.1f}% |
| ⚪ Info | {severity_counts['info']} | {(severity_counts['info']/max(1,total)*100):.1f}% |
| **Total** | **{total}** | **100%** |

### Key Recommendations

1. Address all critical and high severity findings immediately
2. Implement patches for identified vulnerabilities
3. Review and strengthen access controls
4. Conduct follow-up assessment after remediation
"""
    
    @staticmethod
    def format_finding(finding: Any, index: int) -> str:
        """Format a single finding for the report."""
        severity_emoji = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢",
            "info": "⚪"
        }
        
        sev = finding.severity if hasattr(finding, 'severity') else 'info'
        emoji = severity_emoji.get(sev, "⚪")
        
        result = f"""### {index}. {emoji} {finding.title}

| Attribute | Value |
|-----------|-------|
| **Severity** | {finding.severity.upper() if hasattr(finding, 'severity') else 'INFO'} |
| **Status** | {finding.status if hasattr(finding, 'status') else 'Open'} |
| **Affected Component** | {finding.affected_component if hasattr(finding, 'affected_component') and finding.affected_component else 'N/A'} |
| **CVSS Score** | {finding.cvss_score if hasattr(finding, 'cvss_score') and finding.cvss_score else 'N/A'} |
| **CVE ID** | {finding.cve_id if hasattr(finding, 'cve_id') and finding.cve_id else 'N/A'} |

**Description:**
{finding.description if hasattr(finding, 'description') and finding.description else 'No description provided.'}
"""
        
        if hasattr(finding, 'evidence') and finding.evidence:
            result += f"""
**Evidence:**
```
{finding.evidence[:1000]}{'...' if len(finding.evidence) > 1000 else ''}
```
"""
        
        if hasattr(finding, 'remediation') and finding.remediation:
            result += f"""
**Remediation:**
{finding.remediation}
"""
        
        return result + "\n---\n"
    
    @staticmethod
    def format_methodology_section() -> str:
        """Format PTES methodology section."""
        return """## Methodology

This assessment followed the Penetration Testing Execution Standard (PTES) methodology:

1. **Pre-Engagement Interactions** - Scope definition and authorization
2. **Intelligence Gathering** - OSINT and passive reconnaissance
3. **Threat Modeling** - Attack surface mapping and prioritization
4. **Vulnerability Analysis** - Scanning and enumeration
5. **Exploitation** - Controlled exploitation of vulnerabilities
6. **Post-Exploitation** - Impact demonstration
7. **Reporting** - Documentation and recommendations
8. **Cleanup** - Artifact removal and system restoration
"""
    
    @staticmethod
    def format_tools_section(tools_used: List[str] = None) -> str:
        """Format tools used section."""
        default_tools = [
            "Nmap - Network scanning and enumeration",
            "Nikto - Web server vulnerability scanning",
            "Gobuster - Directory and file brute-forcing",
            "Nuclei - CVE and vulnerability detection",
            "Custom scripts and manual testing"
        ]
        
        tools = tools_used or default_tools
        tools_list = "\n".join([f"- {tool}" for tool in tools])
        
        return f"""## Tools Used

The following tools were used during this assessment:

{tools_list}
"""
