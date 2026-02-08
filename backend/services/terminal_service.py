"""
HackMate v2.0 - Terminal Service
Safe command execution with whitelisting.
"""

import asyncio
import time
import shlex
import os
from typing import Dict, Any, List, Set
from config import get_settings

settings = get_settings()


class TerminalService:
    """
    Terminal service for safe command execution.
    
    Features:
    - Command whitelisting
    - Input sanitization
    - Timeout protection
    - Dangerous flag blocking
    """
    
    # Whitelisted command prefixes
    ALLOWED_COMMANDS: Set[str] = {
        # Network tools
        "nmap", "ping", "traceroute", "tracepath",
        "dig", "whois", "host", "nslookup",
        
        # Web tools
        "nikto", "gobuster", "dirb", "wfuzz",
        "curl", "wget", "httpie",
        
        # Vulnerability scanners
        "nuclei", "sqlmap",
        
        # Utilities
        "grep", "awk", "sed", "cat", "head", "tail", "less", "more",
        "wc", "sort", "uniq", "cut", "tr",
        "ls", "find", "file", "strings",
        
        # Built-in commands
        "echo", "help", "clear", "history"
    }
    
    # Dangerous flags/patterns to block
    BLOCKED_PATTERNS: List[str] = [
        "--script=exploit",
        "-oX",  # XML output to files
        "-oN",  # Normal output to files (allow stderr)
        "-oG",  # Grepable output to files
        ">/",   # Output redirection
        ">>/",  # Append redirection
        "|bash",
        "|sh",
        ";rm",
        "&&rm",
        "`",    # Command substitution
        "$(",   # Command substitution
        "eval",
        "exec",
    ]
    
    # Targets that should be blocked (security)
    BLOCKED_TARGETS: List[str] = [
        "127.0.0.1",
        "localhost",
        "0.0.0.0",
        "::1",
        "10.0.0.",
        "172.16.",
        "172.17.",
        "172.18.",
        "172.19.",
        "172.20.",
        "172.21.",
        "172.22.",
        "172.23.",
        "172.24.",
        "172.25.",
        "172.26.",
        "172.27.",
        "172.28.",
        "172.29.",
        "172.30.",
        "172.31.",
        "192.168.",
    ]
    
    def __init__(self):
        self.timeout = settings.command_timeout
    
    def _validate_command(self, command: str) -> bool:
        """
        Validate command against whitelist and blocklist.
        
        Raises ValueError if command is not allowed.
        """
        # Parse command
        try:
            parts = shlex.split(command)
        except ValueError:
            raise ValueError("Invalid command syntax")
        
        if not parts:
            raise ValueError("Empty command")
        
        # Get base command (without path)
        base_command = parts[0].split("/")[-1]
        
        # Check if command is whitelisted
        if base_command not in self.ALLOWED_COMMANDS:
            raise ValueError(f"Command '{base_command}' is not allowed. Use 'help' to see available commands.")
        
        # Check for blocked patterns
        command_lower = command.lower()
        for pattern in self.BLOCKED_PATTERNS:
            if pattern.lower() in command_lower:
                raise ValueError(f"Command contains blocked pattern: {pattern}")
        
        # Note: We're not blocking private IPs in this scaffold
        # to allow testing in local environments
        
        return True
    
    async def execute_command(
        self,
        command: str,
        engagement_id: str = None
    ) -> Dict[str, Any]:
        """
        Execute a command safely.
        
        Args:
            command: The command to execute
            engagement_id: Optional engagement ID for logging
        
        Returns:
            dict with stdout, stderr, exit_code, execution_time
        """
        # Handle built-in commands
        if command.strip() == "help":
            return {
                "stdout": self._get_help_text(),
                "stderr": "",
                "exit_code": 0,
                "execution_time": 0.0
            }
        
        if command.strip() == "clear":
            return {
                "stdout": "\033[2J\033[H",  # ANSI clear screen
                "stderr": "",
                "exit_code": 0,
                "execution_time": 0.0
            }
        
        if command.strip() == "whoami":
            return {
                "stdout": "pentester\n",
                "stderr": "",
                "exit_code": 0,
                "execution_time": 0.0
            }

        # Validate command
        self._validate_command(command)
        
        # Execute command
        start_time = time.time()
        
        # Determine working directory
        cwd = None
        if engagement_id:
            workspace_dir = os.path.join(os.getcwd(), "workspaces", engagement_id)
            os.makedirs(workspace_dir, exist_ok=True)
            cwd = workspace_dir

        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                raise TimeoutError(f"Command timed out after {self.timeout} seconds")
            
            execution_time = time.time() - start_time
            
            return {
                "stdout": stdout.decode("utf-8", errors="replace"),
                "stderr": stderr.decode("utf-8", errors="replace"),
                "exit_code": process.returncode,
                "execution_time": execution_time
            }
            
        except asyncio.TimeoutError:
            raise TimeoutError(f"Command timed out after {self.timeout} seconds")
        except Exception as e:
            raise Exception(f"Command execution failed: {str(e)}")
    
    def _get_help_text(self) -> str:
        """Generate help text for available commands."""
        return """
╔══════════════════════════════════════════════════════════════════╗
║                    HACKMATE TERMINAL v2.0                         ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  NETWORK TOOLS:                                                   ║
║    nmap      - Network scanner and port mapper                    ║
║    ping      - Test network connectivity                          ║
║    dig       - DNS lookup utility                                 ║
║    whois     - Domain registration lookup                         ║
║    host      - DNS lookup                                         ║
║    nslookup  - Query DNS servers                                  ║
║                                                                    ║
║  WEB TOOLS:                                                       ║
║    nikto     - Web server scanner                                 ║
║    gobuster  - Directory/file brute-forcer                        ║
║    curl      - Transfer data from URLs                            ║
║    wget      - Download files from web                            ║
║                                                                    ║
║  VULNERABILITY SCANNERS:                                          ║
║    nuclei    - Fast vulnerability scanner                         ║
║    sqlmap    - SQL injection detection                            ║
║                                                                    ║
║  UTILITIES:                                                       ║
║    grep      - Search text patterns                               ║
║    cat       - Display file contents                              ║
║    ls        - List directory contents                            ║
║    find      - Search for files                                   ║
║                                                                    ║
║  BUILT-IN:                                                        ║
║    help      - Show this help message                             ║
║    clear     - Clear terminal screen                              ║
║    history   - Show command history                               ║
║    whoami    - Show current user identity                         ║
║                                                                    ║
╠══════════════════════════════════════════════════════════════════╣
║  [!] Only authorized testing is permitted.                        ║
║  [!] Commands timeout after 5 minutes.                            ║
╚══════════════════════════════════════════════════════════════════╝
"""
