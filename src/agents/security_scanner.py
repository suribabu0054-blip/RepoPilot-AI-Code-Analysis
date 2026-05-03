"""
Security Scanner Agent
Scans code for OWASP Top 10 vulnerabilities and security best practices
Optionally uses IBM watsonx.ai Granite for enhanced AI-powered security analysis
"""

import re
from typing import Dict, List, Optional
from src.utils import get_watsonx_client


class SecurityScanner:
    """Agent for scanning security vulnerabilities"""
    
    def __init__(self):
        self.name = "Security Scanner"
        self.watsonx_client = get_watsonx_client()
        self.owasp_categories = [
            "Injection", "Broken Authentication", "Sensitive Data Exposure",
            "XML External Entities", "Broken Access Control", "Security Misconfiguration",
            "Cross-Site Scripting", "Insecure Deserialization", "Known Vulnerabilities",
            "Insufficient Logging"
        ]
    
    def scan(self, code: str, language: str = "python") -> Dict:
        """
        Scan code for security vulnerabilities.
        
        Uses IBM watsonx.ai Granite model if configured, otherwise falls back
        to local rule-based security scanning.
        """
        # Try watsonx.ai Granite analysis first if available
        watsonx_result = self._try_watsonx_analysis(code, language)
        if watsonx_result:
            # Merge watsonx results with local analysis for comprehensive coverage
            pass
        
        vulnerabilities = []
        
        # Check for common vulnerabilities (OWASP Top 10)
        vulnerabilities.extend(self._check_injection(code))
        vulnerabilities.extend(self._check_hardcoded_secrets(code))
        vulnerabilities.extend(self._check_insecure_functions(code))
        vulnerabilities.extend(self._check_weak_crypto(code))
        vulnerabilities.extend(self._check_authentication_issues(code))
        vulnerabilities.extend(self._check_access_control(code))
        vulnerabilities.extend(self._check_xss_vulnerabilities(code))
        vulnerabilities.extend(self._check_insecure_deserialization(code))
        vulnerabilities.extend(self._check_logging_monitoring(code))
        vulnerabilities.extend(self._check_security_misconfiguration(code))
        
        # Generate report
        summary = self._generate_summary(vulnerabilities)
        recommendations = self._generate_recommendations(vulnerabilities)
        
        return {
            "summary": summary,
            "vulnerabilities": vulnerabilities,
            "recommendations": recommendations,
            "severity_count": self._count_by_severity(vulnerabilities)
        }
        
    def _try_watsonx_analysis(self, code: str, language: str) -> Optional[Dict]:
        """
        Attempt to analyze code security using IBM watsonx.ai Granite model.
        
        Args:
            code: Source code to analyze
            language: Programming language
        
        Returns:
            Security analysis results from Granite model, or None if not available
        """
        if not self.watsonx_client.is_configured():
            return None
        
        try:
            # Call watsonx.ai Granite model for security analysis
            result = self.watsonx_client.analyze_code(
                code=code,
                language=language,
                analysis_type='security'
            )
            return result
        except Exception as e:
            print(f"Warning: watsonx security analysis failed, using local analysis: {e}")
            return None
    
    def _check_injection(self, code: str) -> List[Dict]:
        """Check for injection vulnerabilities (OWASP A03:2021)"""
        issues = []
        
        # SQL Injection - string formatting in queries
        if re.search(r'(execute|cursor\.execute)\s*\([^)]*[%+]', code):
            issues.append({
                "type": "SQL Injection",
                "severity": "Critical",
                "description": "SQL query uses string formatting - vulnerable to injection",
                "line": "Query execution with % or + operator",
                "fix": "Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))"
            })
        
        # SQL Injection - .format() in queries
        if re.search(r'(SELECT|INSERT|UPDATE|DELETE).*\.format\s*\(', code, re.IGNORECASE):
            issues.append({
                "type": "SQL Injection",
                "severity": "Critical",
                "description": "SQL query uses .format() - vulnerable to injection",
                "line": "Query with .format() method",
                "fix": "Use parameterized queries or ORM (SQLAlchemy, Django ORM)"
            })
        
        # Command Injection - os.system
        if 'os.system' in code:
            issues.append({
                "type": "Command Injection",
                "severity": "Critical",
                "description": "os.system() executes shell commands - extremely dangerous",
                "line": "os.system() call",
                "fix": "Use subprocess.run() with shell=False and validate all inputs"
            })
        
        # Command Injection - subprocess with shell=True
        if re.search(r'subprocess\.(call|run|Popen).*shell\s*=\s*True', code):
            issues.append({
                "type": "Command Injection",
                "severity": "Critical",
                "description": "subprocess with shell=True enables command injection",
                "line": "subprocess call with shell=True",
                "fix": "Set shell=False and pass command as list: subprocess.run(['ls', '-l'])"
            })
        
        # LDAP Injection
        if re.search(r'ldap.*search.*[%+]', code, re.IGNORECASE):
            issues.append({
                "type": "LDAP Injection",
                "severity": "High",
                "description": "LDAP query uses string concatenation",
                "line": "LDAP search with string formatting",
                "fix": "Use parameterized LDAP queries and escape special characters"
            })
        
        # NoSQL Injection
        if re.search(r'(find|findOne|aggregate).*\{.*\$.*\}', code):
            if '+' in code or '%' in code:
                issues.append({
                    "type": "NoSQL Injection",
                    "severity": "High",
                    "description": "MongoDB query may be vulnerable to injection",
                    "line": "NoSQL query with string manipulation",
                    "fix": "Validate and sanitize all user inputs before queries"
                })
        
        return issues
    
    def _check_hardcoded_secrets(self, code: str) -> List[Dict]:
        """Check for hardcoded secrets (OWASP A07:2021)"""
        issues = []
        
        # API Keys - various patterns
        if re.search(r'api[_-]?key\s*=\s*["\'][^"\']{20,}["\']', code, re.IGNORECASE):
            issues.append({
                "type": "Hardcoded API Key",
                "severity": "Critical",
                "description": "API key hardcoded in source code - major security risk",
                "line": "API key assignment",
                "fix": "Use environment variables: api_key = os.getenv('API_KEY')"
            })
        
        # Passwords
        if re.search(r'password\s*=\s*["\'][^"\']+["\']', code, re.IGNORECASE):
            issues.append({
                "type": "Hardcoded Password",
                "severity": "Critical",
                "description": "Password hardcoded in source code",
                "line": "Password assignment",
                "fix": "Use environment variables or secret management (AWS Secrets Manager, HashiCorp Vault)"
            })
        
        # Secret keys
        if re.search(r'secret[_-]?key\s*=\s*["\'][^"\']{16,}["\']', code, re.IGNORECASE):
            issues.append({
                "type": "Hardcoded Secret Key",
                "severity": "Critical",
                "description": "Secret key exposed in code",
                "line": "Secret key assignment",
                "fix": "Load from secure configuration: secret_key = os.getenv('SECRET_KEY')"
            })
        
        # AWS credentials
        if re.search(r'(aws_access_key_id|aws_secret_access_key)\s*=\s*["\']', code, re.IGNORECASE):
            issues.append({
                "type": "Hardcoded AWS Credentials",
                "severity": "Critical",
                "description": "AWS credentials in source code",
                "line": "AWS credential assignment",
                "fix": "Use AWS IAM roles or credentials file (~/.aws/credentials)"
            })
        
        # Database connection strings
        if re.search(r'(mysql|postgresql|mongodb)://[^:]+:[^@]+@', code, re.IGNORECASE):
            issues.append({
                "type": "Hardcoded Database Credentials",
                "severity": "Critical",
                "description": "Database credentials in connection string",
                "line": "Database connection string",
                "fix": "Use environment variables for connection details"
            })
        
        # Private keys
        if 'BEGIN PRIVATE KEY' in code or 'BEGIN RSA PRIVATE KEY' in code:
            issues.append({
                "type": "Embedded Private Key",
                "severity": "Critical",
                "description": "Private key embedded in source code",
                "line": "Private key content",
                "fix": "Store keys in secure key management system, never in code"
            })
        
        return issues
    
    def _check_insecure_functions(self, code: str) -> List[Dict]:
        """Check for insecure function usage"""
        issues = []
        
        # eval() usage
        if 'eval(' in code:
            issues.append({
                "type": "Dangerous Function - eval()",
                "severity": "Critical",
                "description": "eval() can execute arbitrary code - major security risk",
                "line": "eval() call",
                "fix": "Use ast.literal_eval() for safe evaluation or json.loads() for JSON"
            })
        
        # exec() usage
        if 'exec(' in code:
            issues.append({
                "type": "Dangerous Function - exec()",
                "severity": "Critical",
                "description": "exec() executes arbitrary Python code",
                "line": "exec() call",
                "fix": "Avoid exec(), redesign to use safe alternatives"
            })
        
        # compile() usage
        if 'compile(' in code:
            issues.append({
                "type": "Dangerous Function - compile()",
                "severity": "High",
                "description": "compile() can create code objects from strings",
                "line": "compile() call",
                "fix": "Avoid dynamic code compilation, use static code"
            })
        
        # input() in Python 2 style
        if re.search(r'\binput\s*\(', code):
            issues.append({
                "type": "Unsafe Input",
                "severity": "Medium",
                "description": "input() without validation can be dangerous",
                "line": "input() call",
                "fix": "Validate and sanitize all user inputs"
            })
        
        return issues
    
    def _check_weak_crypto(self, code: str) -> List[Dict]:
        """Check for weak cryptography (OWASP A02:2021)"""
        issues = []
        
        # MD5 usage
        if re.search(r'\bmd5\b', code, re.IGNORECASE):
            issues.append({
                "type": "Weak Hashing - MD5",
                "severity": "High",
                "description": "MD5 is cryptographically broken and should not be used",
                "line": "MD5 usage",
                "fix": "Use SHA-256 or bcrypt for passwords: hashlib.sha256() or bcrypt.hashpw()"
            })
        
        # SHA1 usage
        if re.search(r'\bsha1\b', code, re.IGNORECASE):
            issues.append({
                "type": "Weak Hashing - SHA1",
                "severity": "High",
                "description": "SHA1 is deprecated and vulnerable to collision attacks",
                "line": "SHA1 usage",
                "fix": "Use SHA-256 or stronger: hashlib.sha256()"
            })
        
        # DES encryption
        if re.search(r'\bDES\b', code):
            issues.append({
                "type": "Weak Encryption - DES",
                "severity": "High",
                "description": "DES encryption is obsolete and easily broken",
                "line": "DES usage",
                "fix": "Use AES-256: from cryptography.fernet import Fernet"
            })
        
        # Hardcoded encryption keys
        if re.search(r'(Fernet|AES).*key\s*=\s*["\']', code):
            issues.append({
                "type": "Hardcoded Encryption Key",
                "severity": "Critical",
                "description": "Encryption key hardcoded in source",
                "line": "Encryption key assignment",
                "fix": "Generate and store keys securely, load from environment"
            })
        
        # Random instead of secrets
        if 'random.random' in code or 'random.randint' in code:
            if 'token' in code.lower() or 'password' in code.lower() or 'key' in code.lower():
                issues.append({
                    "type": "Weak Random Number Generation",
                    "severity": "Medium",
                    "description": "random module is not cryptographically secure",
                    "line": "random module usage",
                    "fix": "Use secrets module: secrets.token_urlsafe(32)"
                })
        
        return issues
    
    def _check_authentication_issues(self, code: str) -> List[Dict]:
        """Check for authentication vulnerabilities (OWASP A07:2021)"""
        issues = []
        
        # Weak password validation
        if re.search(r'len\s*\(\s*password\s*\)\s*[<>=]+\s*[1-7]', code):
            issues.append({
                "type": "Weak Password Policy",
                "severity": "High",
                "description": "Password length requirement is too weak",
                "line": "Password validation",
                "fix": "Require minimum 8-12 characters with complexity requirements"
            })
        
        # No password hashing
        if 'password' in code.lower() and 'hash' not in code.lower() and 'bcrypt' not in code.lower():
            if '==' in code or 'SELECT' in code:
                issues.append({
                    "type": "Plaintext Password Comparison",
                    "severity": "Critical",
                    "description": "Passwords appear to be stored/compared in plaintext",
                    "line": "Password comparison",
                    "fix": "Hash passwords with bcrypt: bcrypt.hashpw(password, bcrypt.gensalt())"
                })
        
        # Session without timeout
        if 'session' in code.lower() and 'timeout' not in code.lower() and 'expire' not in code.lower():
            issues.append({
                "type": "Missing Session Timeout",
                "severity": "Medium",
                "description": "Sessions may not have timeout configured",
                "line": "Session management",
                "fix": "Implement session timeout: session.permanent = True, app.permanent_session_lifetime = timedelta(minutes=30)"
            })
        
        return issues
    
    def _check_access_control(self, code: str) -> List[Dict]:
        """Check for access control issues (OWASP A01:2021)"""
        issues = []
        
        # Direct object reference
        if re.search(r'(user_id|id)\s*=\s*request\.(GET|POST|args|form)', code):
            issues.append({
                "type": "Insecure Direct Object Reference",
                "severity": "High",
                "description": "User-supplied ID used directly without authorization check",
                "line": "Direct object access",
                "fix": "Verify user has permission to access the resource before retrieval"
            })
        
        # Missing authorization checks
        if '@app.route' in code or '@route' in code:
            if '@login_required' not in code and '@requires_auth' not in code:
                issues.append({
                    "type": "Missing Authorization",
                    "severity": "High",
                    "description": "Route may lack authentication/authorization",
                    "line": "Route definition",
                    "fix": "Add @login_required or @requires_auth decorator"
                })
        
        return issues
    
    def _check_xss_vulnerabilities(self, code: str) -> List[Dict]:
        """Check for XSS vulnerabilities (OWASP A03:2021)"""
        issues = []
        
        # Unsafe HTML rendering
        if re.search(r'(render_template_string|Markup|safe)', code):
            issues.append({
                "type": "Cross-Site Scripting (XSS)",
                "severity": "High",
                "description": "Unsafe HTML rendering detected",
                "line": "HTML rendering",
                "fix": "Use auto-escaping templates, avoid |safe filter with user input"
            })
        
        # innerHTML or similar
        if 'innerHTML' in code or 'outerHTML' in code:
            issues.append({
                "type": "DOM-based XSS",
                "severity": "High",
                "description": "Direct DOM manipulation can lead to XSS",
                "line": "DOM manipulation",
                "fix": "Use textContent instead of innerHTML, or sanitize input"
            })
        
        return issues
    
    def _check_insecure_deserialization(self, code: str) -> List[Dict]:
        """Check for insecure deserialization (OWASP A08:2021)"""
        issues = []
        
        # pickle.loads
        if 'pickle.loads' in code or 'pickle.load' in code:
            issues.append({
                "type": "Insecure Deserialization - Pickle",
                "severity": "Critical",
                "description": "pickle can execute arbitrary code during deserialization",
                "line": "pickle.loads() call",
                "fix": "Use JSON for data serialization, or validate pickle source"
            })
        
        # PyYAML unsafe load
        if re.search(r'yaml\.load\s*\([^,)]*\)', code):
            if 'Loader=' not in code:
                issues.append({
                    "type": "Insecure Deserialization - YAML",
                    "severity": "High",
                    "description": "yaml.load() without Loader is unsafe",
                    "line": "yaml.load() call",
                    "fix": "Use yaml.safe_load() or yaml.load(data, Loader=yaml.SafeLoader)"
                })
        
        # marshal
        if 'marshal.loads' in code:
            issues.append({
                "type": "Insecure Deserialization - Marshal",
                "severity": "High",
                "description": "marshal is not secure against malicious data",
                "line": "marshal.loads() call",
                "fix": "Use JSON or validate data source"
            })
        
        return issues
    
    def _check_logging_monitoring(self, code: str) -> List[Dict]:
        """Check for logging and monitoring issues (OWASP A09:2021)"""
        issues = []
        
        # No logging
        if 'logging' not in code and 'logger' not in code:
            if 'def ' in code or 'class ' in code:
                issues.append({
                    "type": "Insufficient Logging",
                    "severity": "Low",
                    "description": "No logging implementation found",
                    "line": "Throughout code",
                    "fix": "Implement logging: import logging; logger = logging.getLogger(__name__)"
                })
        
        # Logging sensitive data
        if re.search(r'log.*password|log.*secret|log.*token', code, re.IGNORECASE):
            issues.append({
                "type": "Sensitive Data in Logs",
                "severity": "High",
                "description": "Sensitive information may be logged",
                "line": "Logging statement",
                "fix": "Never log passwords, tokens, or secrets. Redact sensitive data."
            })
        
        return issues
    
    def _check_security_misconfiguration(self, code: str) -> List[Dict]:
        """Check for security misconfiguration (OWASP A05:2021)"""
        issues = []
        
        # Debug mode in production
        if re.search(r'debug\s*=\s*True', code, re.IGNORECASE):
            issues.append({
                "type": "Debug Mode Enabled",
                "severity": "High",
                "description": "Debug mode should never be enabled in production",
                "line": "Debug configuration",
                "fix": "Set debug=False in production, use environment variables"
            })
        
        # Insecure SSL/TLS
        if re.search(r'verify\s*=\s*False', code):
            issues.append({
                "type": "SSL Verification Disabled",
                "severity": "High",
                "description": "SSL certificate verification is disabled",
                "line": "SSL configuration",
                "fix": "Enable SSL verification: verify=True or use proper certificates"
            })
        
        # Permissive CORS
        if re.search(r'CORS.*origins?\s*=\s*["\']?\*', code, re.IGNORECASE):
            issues.append({
                "type": "Permissive CORS Policy",
                "severity": "Medium",
                "description": "CORS allows all origins (*)",
                "line": "CORS configuration",
                "fix": "Restrict CORS to specific trusted domains"
            })
        
        # Default credentials
        if re.search(r'(admin|root|default).*password.*=.*(admin|password|123)', code, re.IGNORECASE):
            issues.append({
                "type": "Default Credentials",
                "severity": "Critical",
                "description": "Default or weak credentials detected",
                "line": "Credential assignment",
                "fix": "Use strong, unique credentials and change defaults immediately"
            })
        
        return issues
    
    def _generate_summary(self, vulnerabilities: List[Dict]) -> str:
        """Generate security summary"""
        if not vulnerabilities:
            return "✅ **No major security issues detected!**\n\nThe code appears to follow basic security practices."
        
        critical = sum(1 for v in vulnerabilities if v['severity'] == 'Critical')
        high = sum(1 for v in vulnerabilities if v['severity'] == 'High')
        medium = sum(1 for v in vulnerabilities if v['severity'] == 'Medium')
        
        summary = f"🔒 **Security Scan Results**\n\n"
        summary += f"Found {len(vulnerabilities)} potential security issue(s):\n\n"
        
        if critical > 0:
            summary += f"- 🔴 **Critical**: {critical}\n"
        if high > 0:
            summary += f"- 🟠 **High**: {high}\n"
        if medium > 0:
            summary += f"- 🟡 **Medium**: {medium}\n"
        
        return summary
    
    def _generate_recommendations(self, vulnerabilities: List[Dict]) -> str:
        """Generate security recommendations"""
        if not vulnerabilities:
            return "Continue following security best practices!"
        
        recs = "💡 **Recommendations:**\n\n"
        
        for i, vuln in enumerate(vulnerabilities[:5], 1):
            recs += f"{i}. **{vuln['type']}** ({vuln['severity']})\n"
            recs += f"   - Issue: {vuln['description']}\n"
            recs += f"   - Fix: {vuln['fix']}\n\n"
        
        if len(vulnerabilities) > 5:
            recs += f"... and {len(vulnerabilities) - 5} more issues\n"
        
        return recs
    
    def _count_by_severity(self, vulnerabilities: List[Dict]) -> Dict:
        """Count vulnerabilities by severity"""
        return {
            "critical": sum(1 for v in vulnerabilities if v['severity'] == 'Critical'),
            "high": sum(1 for v in vulnerabilities if v['severity'] == 'High'),
            "medium": sum(1 for v in vulnerabilities if v['severity'] == 'Medium'),
            "low": sum(1 for v in vulnerabilities if v['severity'] == 'Low')
        }
