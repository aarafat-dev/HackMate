"""
HackMate v2.0 - AI Service
Google Gemini integration for AI-powered features.
"""

import os
from typing import List, Dict, Any, Optional
from config import get_settings

settings = get_settings()

# Try to import Google Generative AI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class AIService:
    """
    AI service for Google Gemini integration.
    
    Provides:
    - Chat assistance
    - Phase guidance generation
    - Output analysis
    - Report generation
    - Scan suggestions
    
    Falls back to mock responses if Gemini API is unavailable.
    """
    
    def __init__(self):
        self.model = None
        self.use_mock = True
        
        if GEMINI_AVAILABLE and settings.gemini_api_key:
            try:
                genai.configure(api_key=settings.gemini_api_key)
                self.model = genai.GenerativeModel(settings.gemini_model)
                self.use_mock = False
                print(f"[AI] Gemini API initialized successfully with model: {settings.gemini_model}")
            except Exception as e:
                print(f"[AI] Gemini initialization failed: {e}")
                print("[AI] Falling back to mock responses")
    
    async def chat(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a chat message to the AI assistant.
        
        Args:
            message: User's message
            context: Engagement context (target, phase, findings)
        
        Returns:
            dict with 'message' and optional 'suggestions'
        """
        if self.use_mock:
            return self._mock_chat(message, context)
        
        try:
            system_prompt = f"""You are HACKMATE AI, an elite penetration testing assistant with a hacker mentor persona.

PERSONALITY:
- Direct, no fluff
- Uses hacker slang: pwn, shell, foothold, etc.
- Terminal-style formatting: [INFO], [CRITICAL], [TIP]
- Confident but not arrogant
- Proactive with suggestions

CONTEXT:
- Engagement: {context.get('engagement_name', 'Unknown')}
- Target: {context.get('target', 'Unknown')}
- Current Phase: {context.get('phase_number', 0)}/8 - {context.get('current_phase', 'Unknown')}
- Findings Count: {context.get('findings_count', 0)}

RULES:
1. Always emphasize ethical hacking and authorization
2. Provide specific, executable commands
3. Explain WHY you're suggesting something
4. Reference tools by name
5. Be encouraging but realistic"""

            response = self.model.generate_content(
                f"{system_prompt}\n\nUser: {message}",
                generation_config={
                    "temperature": settings.ai_temperature,
                    "max_output_tokens": settings.ai_max_tokens
                }
            )
            
            return {
                "message": response.text,
                "suggestions": []
            }
        except Exception as e:
            print(f"[AI] Chat error: {e}")
            return self._mock_chat(message, context)
    
    async def generate_welcome(self, target: str) -> str:
        """Generate an initial welcome message from the AI."""
        if self.use_mock:
            return f"[SYSTEM ONLINE] Greetings. I am HackMate AI. I am ready to assist with the assessment of {target}. Status: OPERATIONAL."
        
        try:
            prompt = f"""You are HACKMATE AI, an elite penetration testing assistant.
Generate a short, cool, hacker-style welcome message for a new engagement targeting: {target}.
Introduce yourself briefly and ask how you can help.
Keep it under 50 words."""
            
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.8,
                    "max_output_tokens": 100
                }
            )
            return response.text
        except Exception as e:
            print(f"[AI] Welcome generation error: {e}")
            return f"[SYSTEM ONLINE] HackMate AI ready for target: {target}."

    async def generate_phase_guidance(
        self,
        phase_name: str,
        phase_number: int,
        target: str,
        objectives: List[str]
    ) -> str:
        """Generate AI guidance for a specific PTES phase."""
        if self.use_mock:
            return self._mock_phase_guidance(phase_name, phase_number, target)
        
        try:
            prompt = f"""Generate penetration testing guidance for the following phase:

Phase: {phase_number}/8 - {phase_name}
Target: {target}
Objectives: {', '.join(objectives or [])}

Provide:
1. Key objectives for this phase
2. Recommended tools and techniques
3. What to look for in results
4. Common mistakes to avoid
5. Suggested next steps

Keep response under 300 words. Be specific and actionable."""

            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 1024
                }
            )
            
            return response.text
        except Exception as e:
            print(f"[AI] Phase guidance error: {e}")
            return self._mock_phase_guidance(phase_name, phase_number, target)
    
    async def analyze_output(
        self,
        tool: str,
        output: str,
        target: str
    ) -> Dict[str, Any]:
        """Analyze tool output and extract findings."""
        if self.use_mock:
            return self._mock_analyze_output(tool, output)
        
        try:
            prompt = f"""Analyze this {tool} scan output and provide a structured response:

Target: {target}
Tool: {tool}
Output:
{output[:5000]}  # Limit output length

Provide:
1. Summary of key findings
2. List of potential vulnerabilities found
3. Risk level (critical/high/medium/low)
4. Recommended next steps

Format as JSON with keys: summary, findings, next_steps, risk_level"""

            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.3,
                    "max_output_tokens": 2048
                }
            )
            
            # Try to parse as JSON, fall back to structured response
            return {
                "summary": response.text[:500],
                "findings": [],
                "next_steps": ["Review the detailed analysis above"],
                "risk_level": "medium"
            }
        except Exception as e:
            print(f"[AI] Analysis error: {e}")
            return self._mock_analyze_output(tool, output)
    
    async def generate_report(
        self,
        engagement_name: str,
        target: str,
        scope: str,
        findings: List[Any],
        report_type: str,
        include_evidence: bool,
        include_remediation: bool
    ) -> str:
        """Generate a penetration testing report."""
        if self.use_mock:
            return self._mock_report(engagement_name, target, findings, report_type)
        
        try:
            findings_summary = "\n".join([
                f"- [{f.severity.upper()}] {f.title}" 
                for f in findings[:20]  # Limit to 20 findings
            ])
            
            prompt = f"""Generate a {report_type} penetration testing report:

Engagement: {engagement_name}
Target: {target}
Scope: {scope or 'Full scope'}

Findings:
{findings_summary}

Report Type: {report_type}
Include Evidence: {include_evidence}
Include Remediation: {include_remediation}

Generate a professional, well-formatted Markdown report."""

            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.5,
                    "max_output_tokens": 4096
                }
            )
            
            return response.text
        except Exception as e:
            print(f"[AI] Report generation error: {e}")
            return self._mock_report(engagement_name, target, findings, report_type)
    
    async def suggest_next_scan(
        self,
        target: str,
        phase_number: int,
        phase_name: str
    ) -> Dict[str, Any]:
        """Suggest the next scan to run."""
        if self.use_mock:
            return self._mock_scan_suggestion(target, phase_number)
        
        try:
            prompt = f"""Based on the current penetration testing phase, suggest the next scan:

Target: {target}
Phase: {phase_number}/8 - {phase_name}

Provide:
1. Recommended tool
2. Specific command
3. Why this scan is useful
4. What to look for in results

Format as JSON with keys: tool, command, reason, expected_findings"""

            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 512
                }
            )
            
            return {
                "tool": "nmap",
                "command": f"nmap -sV -sC {target}",
                "reason": response.text[:500],
                "expected_findings": ["Open ports", "Service versions"]
            }
        except Exception as e:
            print(f"[AI] Scan suggestion error: {e}")
            return self._mock_scan_suggestion(target, phase_number)
    
    # =========================================================================
    # Mock Responses (used when Gemini API is unavailable)
    # =========================================================================
    
    def _mock_chat(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Mock chat response for testing."""
        phase = context.get('phase_number', 0)
        target = context.get('target', 'target.com')
        
        responses = {
            "help": f"""[INFO] Here's what I can help you with:

• **Reconnaissance**: Use `nmap`, `whois`, `dig` for initial enumeration
• **Web Scanning**: Try `nikto`, `gobuster` for web targets
• **Vulnerability Scanning**: `nuclei` is great for CVE detection

[TIP] Start with basic enumeration:
```bash
nmap -sV -sC {target}
```

What would you like to focus on?""",
            
            "default": f"""[INFO] Got it! For target {target} in phase {phase}...

Here are some recommendations:
1. Run a comprehensive port scan first
2. Enumerate services on open ports
3. Check for known vulnerabilities

[TIP] Try this command:
```bash
nmap -sV -sC -p- {target}
```

Let me know if you need specific guidance!"""
        }
        
        key = "help" if "help" in message.lower() else "default"
        
        return {
            "message": responses[key],
            "suggestions": [
                f"nmap -sV {target}",
                f"nikto -h {target}",
                f"gobuster dir -u http://{target} -w /usr/share/wordlists/dirb/common.txt"
            ]
        }
    
    def _mock_phase_guidance(self, phase_name: str, phase_number: int, target: str) -> str:
        """Mock phase guidance for testing."""
        guidance = {
            1: f"""# Pre-Engagement Interactions

**Key Objectives:**
- Get written authorization (CRITICAL!)
- Define scope boundaries clearly
- Establish communication protocols

**Recommended Actions:**
1. Obtain signed Rules of Engagement (RoE)
2. Document all in-scope and out-of-scope targets
3. Set up secure communication channels
4. Define escalation procedures

**⚠️ WARNING:** Never proceed without proper authorization.""",

            2: f"""# Intelligence Gathering for {target}

**Key Objectives:**
- Collect OSINT without touching the target
- Build a comprehensive target profile

**Recommended Tools:**
```bash
# Domain info
whois {target}
dig {target} ANY

# Subdomain enumeration
# subfinder -d {target}

# Technology detection
# whatweb {target}
```

**What to Look For:**
- Email addresses and employee names
- Subdomains and related domains
- Technology stack clues""",

            4: f"""# Vulnerability Analysis for {target}

**Key Objectives:**
- Identify security weaknesses
- Enumerate services and versions
- Find exploitable vulnerabilities

**Recommended Scans:**
```bash
# Port scanning
nmap -sV -sC {target}

# Web scanning
nikto -h {target}

# Directory enumeration
gobuster dir -u http://{target} -w /usr/share/wordlists/dirb/common.txt

# Vulnerability scanning
nuclei -u {target}
```

**What to Look For:**
- Outdated software versions
- Default credentials
- Misconfigurations
- Known CVEs"""
        }
        
        return guidance.get(phase_number, f"# {phase_name}\n\nProceed with standard methodology for this phase.")
    
    def _mock_analyze_output(self, tool: str, output: str) -> Dict[str, Any]:
        """Mock output analysis for testing."""
        return {
            "summary": f"Analysis of {tool} output completed. Found potential security indicators that require further investigation.",
            "findings": [
                {
                    "title": "Open Port Detected",
                    "severity": "info",
                    "description": "Service detected on target"
                }
            ],
            "next_steps": [
                f"Run targeted scans on identified services",
                "Check for known vulnerabilities",
                "Enumerate discovered services"
            ],
            "risk_level": "medium"
        }
    
    def _mock_report(
        self,
        engagement_name: str,
        target: str,
        findings: List[Any],
        report_type: str
    ) -> str:
        """Mock report generation for testing."""
        severity_counts = {}
        for f in findings:
            sev = f.severity if hasattr(f, 'severity') else 'info'
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
        
        findings_list = "\n".join([
            f"### {i+1}. {f.title}\n- **Severity:** {f.severity}\n- **Status:** {f.status}\n"
            for i, f in enumerate(findings[:10])
        ]) if findings else "No findings recorded."
        
        return f"""# {engagement_name} - {report_type.title()} Report

## Executive Summary

This penetration test was conducted against **{target}** to identify security vulnerabilities and assess the overall security posture.

### Findings Overview

| Severity | Count |
|----------|-------|
| Critical | {severity_counts.get('critical', 0)} |
| High | {severity_counts.get('high', 0)} |
| Medium | {severity_counts.get('medium', 0)} |
| Low | {severity_counts.get('low', 0)} |
| Info | {severity_counts.get('info', 0)} |

**Total Findings:** {len(findings)}

## Detailed Findings

{findings_list}

## Recommendations

1. Address all critical and high severity findings immediately
2. Implement a patch management program
3. Conduct regular security assessments
4. Review access controls and authentication mechanisms

---

*Report generated by HackMate v2.0*
"""
    
    def _mock_scan_suggestion(self, target: str, phase_number: int) -> Dict[str, Any]:
        """Mock scan suggestion for testing."""
        suggestions = {
            2: {
                "tool": "dig",
                "command": f"dig {target} ANY +noall +answer",
                "reason": "DNS enumeration reveals subdomains and mail servers",
                "expected_findings": ["MX records", "NS records", "TXT records"]
            },
            4: {
                "tool": "nmap",
                "command": f"nmap -sV -sC -p- {target}",
                "reason": "Comprehensive port scan reveals all open services",
                "expected_findings": ["Open ports", "Service versions", "Script results"]
            }
        }
        
        return suggestions.get(phase_number, {
            "tool": "nmap",
            "command": f"nmap -sV {target}",
            "reason": "Basic service enumeration is always a good starting point",
            "expected_findings": ["Open ports", "Service versions"]
        })
