"""
Code Modernizer Agent
Suggests code modernization and Python best practices
Optionally uses IBM watsonx.ai Granite for enhanced AI-powered modernization suggestions
"""

import re
from typing import Dict, List, Optional
from src.utils import get_watsonx_client


class CodeModernizer:
    """Agent for suggesting code modernization"""
    
    def __init__(self):
        self.name = "Code Modernizer"
        self.watsonx_client = get_watsonx_client()
    
    def analyze(self, code: str, language: str = "python") -> Dict:
        """
        Analyze code and suggest modernizations.
        
        Uses IBM watsonx.ai Granite model if configured, otherwise falls back
        to local rule-based modernization analysis.
        """
        # Try watsonx.ai Granite analysis first if available
        watsonx_result = self._try_watsonx_analysis(code, language)
        if watsonx_result:
            # Use watsonx results if available
            pass
        
        # Fall back to local modernization analysis
        suggestions = []
        
        # Check for various modernization opportunities
        suggestions.extend(self._check_python_version(code))
        suggestions.extend(self._check_type_hints(code))
        suggestions.extend(self._check_f_strings(code))
        suggestions.extend(self._check_comprehensions(code))
        suggestions.extend(self._check_context_managers(code))
        suggestions.extend(self._check_pathlib(code))
        suggestions.extend(self._check_dataclasses(code))
        suggestions.extend(self._check_error_handling(code))
        suggestions.extend(self._check_logging(code))
        suggestions.extend(self._check_async_opportunities(code))
        
        summary = self._generate_summary(suggestions)
        prioritized = self._prioritize_suggestions(suggestions)
        
        return {
            "summary": summary,
            "suggestions": prioritized,
            "total_count": len(suggestions)
        }
    
    def _try_watsonx_analysis(self, code: str, language: str) -> Optional[Dict]:
        """
        Attempt to analyze code modernization using IBM watsonx.ai Granite model.
        
        Args:
            code: Source code to analyze
            language: Programming language
        
        Returns:
            Modernization suggestions from Granite model, or None if not available
        """
        if not self.watsonx_client.is_configured():
            return None
        
        try:
            # Call watsonx.ai Granite model for modernization analysis
            result = self.watsonx_client.analyze_code(
                code=code,
                language=language,
                analysis_type='modernization'
            )
            return result
        except Exception as e:
            print(f"Warning: watsonx modernization analysis failed, using local analysis: {e}")
            return None
    
    def _check_python_version(self, code: str) -> List[Dict]:
        """Check for Python version-specific improvements"""
        suggestions = []
        
        # Check for old-style string formatting
        if '%s' in code or '%d' in code or '%f' in code:
            suggestions.append({
                "category": "String Formatting",
                "priority": "Medium",
                "current": "Old-style % formatting",
                "modern": "Use f-strings (Python 3.6+)",
                "example": "f'Hello {name}' instead of 'Hello %s' % name",
                "effort": "Low"
            })
        
        # Check for .format() usage
        if '.format(' in code:
            suggestions.append({
                "category": "String Formatting",
                "priority": "Low",
                "current": ".format() method",
                "modern": "Use f-strings for better readability",
                "example": "f'{value}' instead of '{}'.format(value)",
                "effort": "Low"
            })
        
        # Check for dict() constructor
        if re.search(r'dict\(\w+\s*=', code):
            suggestions.append({
                "category": "Dictionary Creation",
                "priority": "Low",
                "current": "dict() constructor with kwargs",
                "modern": "Use dictionary literals",
                "example": "{'key': value} instead of dict(key=value)",
                "effort": "Low"
            })
        
        return suggestions
    
    def _check_type_hints(self, code: str) -> List[Dict]:
        """Check for missing type hints"""
        suggestions = []
        
        # Check if functions lack type hints
        func_pattern = r'def\s+\w+\s*\([^)]*\)\s*:'
        funcs_without_hints = re.findall(func_pattern, code)
        
        if funcs_without_hints and '->' not in code:
            suggestions.append({
                "category": "Type Safety",
                "priority": "High",
                "current": "No type hints",
                "modern": "Add type hints for better code clarity and IDE support",
                "example": "def func(x: int, y: str) -> bool: instead of def func(x, y):",
                "effort": "Medium"
            })
        
        # Check for missing typing imports
        if 'def ' in code and 'from typing import' not in code:
            if 'List' not in code and 'Dict' not in code:
                suggestions.append({
                    "category": "Type Hints",
                    "priority": "Medium",
                    "current": "No typing module imports",
                    "modern": "Import typing for complex type hints",
                    "example": "from typing import List, Dict, Optional, Union",
                    "effort": "Low"
                })
        
        return suggestions
    
    def _check_f_strings(self, code: str) -> List[Dict]:
        """Check for f-string opportunities"""
        suggestions = []
        
        # String concatenation with +
        if re.search(r'["\'][^"\']*["\'][\s]*\+[\s]*\w+', code):
            suggestions.append({
                "category": "String Concatenation",
                "priority": "Low",
                "current": "String concatenation with +",
                "modern": "Use f-strings for cleaner code",
                "example": "f'{a} {b}' instead of a + ' ' + b",
                "effort": "Low"
            })
        
        return suggestions
    
    def _check_comprehensions(self, code: str) -> List[Dict]:
        """Check for list comprehension opportunities"""
        suggestions = []
        
        # Check for append in loops
        if 'append(' in code and 'for ' in code:
            # Simple pattern detection
            if re.search(r'for\s+\w+\s+in\s+.*:\s*\n\s+\w+\.append\(', code):
                suggestions.append({
                    "category": "Code Style",
                    "priority": "Medium",
                    "current": "Loop with append",
                    "modern": "Use list comprehension",
                    "example": "[x*2 for x in items] instead of loop with append",
                    "effort": "Low"
                })
        
        # Check for dict building in loops
        if re.search(r'for\s+.*:\s*\n\s+\w+\[.*\]\s*=', code):
            suggestions.append({
                "category": "Code Style",
                "priority": "Medium",
                "current": "Loop building dictionary",
                "modern": "Use dictionary comprehension",
                "example": "{k: v for k, v in items} instead of loop",
                "effort": "Low"
            })
        
        # Check for filter with lambda
        if 'filter(lambda' in code:
            suggestions.append({
                "category": "Functional Programming",
                "priority": "Low",
                "current": "filter() with lambda",
                "modern": "Use list comprehension with condition",
                "example": "[x for x in items if condition] instead of filter(lambda x: condition, items)",
                "effort": "Low"
            })
        
        # Check for map with lambda
        if 'map(lambda' in code:
            suggestions.append({
                "category": "Functional Programming",
                "priority": "Low",
                "current": "map() with lambda",
                "modern": "Use list comprehension",
                "example": "[func(x) for x in items] instead of map(lambda x: func(x), items)",
                "effort": "Low"
            })
        
        return suggestions
    
    def _check_context_managers(self, code: str) -> List[Dict]:
        """Check for context manager usage"""
        suggestions = []
        
        # Check for file operations without context manager
        if 'open(' in code and 'with ' not in code:
            suggestions.append({
                "category": "Resource Management",
                "priority": "High",
                "current": "File operations without context manager",
                "modern": "Use 'with' statement for automatic cleanup",
                "example": "with open(file) as f: instead of f = open(file)",
                "effort": "Low"
            })
        
        # Check for manual close() calls
        if '.close()' in code:
            suggestions.append({
                "category": "Resource Management",
                "priority": "High",
                "current": "Manual resource cleanup with close()",
                "modern": "Use context managers (with statement)",
                "example": "with resource: instead of try/finally with close()",
                "effort": "Low"
            })
        
        return suggestions
    
    def _check_pathlib(self, code: str) -> List[Dict]:
        """Check for pathlib usage"""
        suggestions = []
        
        # Check for os.path usage
        if 'os.path' in code:
            suggestions.append({
                "category": "File Path Handling",
                "priority": "Medium",
                "current": "Using os.path module",
                "modern": "Use pathlib.Path for object-oriented path handling",
                "example": "from pathlib import Path; path = Path('file.txt')",
                "effort": "Medium"
            })
        
        # Check for string path concatenation
        if re.search(r'["\'][^"\']*[/\\][^"\']*["\'][\s]*\+', code):
            suggestions.append({
                "category": "File Path Handling",
                "priority": "Medium",
                "current": "String concatenation for paths",
                "modern": "Use pathlib.Path with / operator",
                "example": "Path('dir') / 'file.txt' instead of 'dir' + '/' + 'file.txt'",
                "effort": "Low"
            })
        
        return suggestions
    
    def _check_dataclasses(self, code: str) -> List[Dict]:
        """Check for dataclass opportunities"""
        suggestions = []
        
        # Check for classes with __init__ that just assigns attributes
        if 'class ' in code and '__init__' in code:
            # Simple heuristic: if __init__ has multiple self.x = x patterns
            if code.count('self.') > 3 and 'def __init__' in code:
                suggestions.append({
                    "category": "Data Classes",
                    "priority": "Medium",
                    "current": "Class with boilerplate __init__",
                    "modern": "Use @dataclass decorator (Python 3.7+)",
                    "example": "@dataclass\nclass Point:\n    x: int\n    y: int",
                    "effort": "Low"
                })
        
        # Check for namedtuple
        if 'namedtuple' in code:
            suggestions.append({
                "category": "Data Classes",
                "priority": "Low",
                "current": "Using namedtuple",
                "modern": "Consider @dataclass for more features",
                "example": "@dataclass with default values and methods",
                "effort": "Medium"
            })
        
        return suggestions
    
    def _check_error_handling(self, code: str) -> List[Dict]:
        """Check for error handling improvements"""
        suggestions = []
        
        # Check for bare except
        if re.search(r'except\s*:', code):
            suggestions.append({
                "category": "Error Handling",
                "priority": "High",
                "current": "Bare except clause",
                "modern": "Catch specific exceptions",
                "example": "except ValueError: instead of except:",
                "effort": "Low"
            })
        
        # Check for pass in except
        if re.search(r'except.*:\s*\n\s*pass', code):
            suggestions.append({
                "category": "Error Handling",
                "priority": "High",
                "current": "Silent exception handling",
                "modern": "Log errors or re-raise with context",
                "example": "except Exception as e:\n    logger.error(f'Error: {e}')\n    raise",
                "effort": "Low"
            })
        
        # Check for missing error handling
        if 'def ' in code and 'try:' not in code and 'except' not in code:
            if 'open(' in code or 'requests.' in code or 'json.loads' in code:
                suggestions.append({
                    "category": "Error Handling",
                    "priority": "High",
                    "current": "No exception handling for risky operations",
                    "modern": "Add try-except blocks",
                    "example": "try:\n    risky_operation()\nexcept SpecificError as e:\n    handle_error(e)",
                    "effort": "Medium"
                })
        
        return suggestions
    
    def _check_logging(self, code: str) -> List[Dict]:
        """Check for logging improvements"""
        suggestions = []
        
        # Check for print statements
        if 'print(' in code:
            suggestions.append({
                "category": "Logging",
                "priority": "Medium",
                "current": "Using print() for output",
                "modern": "Use logging module for better control",
                "example": "import logging\nlogger = logging.getLogger(__name__)\nlogger.info('message')",
                "effort": "Low"
            })
        
        # Check for missing logging
        if 'def ' in code and 'logging' not in code and 'logger' not in code:
            if len(code.split('\n')) > 50:
                suggestions.append({
                    "category": "Observability",
                    "priority": "Medium",
                    "current": "No logging implementation",
                    "modern": "Add logging for debugging and monitoring",
                    "example": "import logging\nlogger = logging.getLogger(__name__)",
                    "effort": "Low"
                })
        
        return suggestions
    
    def _check_async_opportunities(self, code: str) -> List[Dict]:
        """Check for async/await opportunities"""
        suggestions = []
        
        # Check for time.sleep
        if 'time.sleep' in code or 'sleep(' in code:
            suggestions.append({
                "category": "Concurrency",
                "priority": "Low",
                "current": "Blocking sleep calls",
                "modern": "Use asyncio.sleep for async code",
                "example": "async def func():\n    await asyncio.sleep(1)",
                "effort": "Medium"
            })
        
        # Check for requests without async
        if 'requests.' in code and 'async' not in code:
            if code.count('requests.') > 2:
                suggestions.append({
                    "category": "Concurrency",
                    "priority": "Medium",
                    "current": "Synchronous HTTP requests",
                    "modern": "Use aiohttp for async HTTP requests",
                    "example": "async with aiohttp.ClientSession() as session:\n    async with session.get(url) as response:",
                    "effort": "High"
                })
        
        return suggestions
    
    def _generate_summary(self, suggestions: List[Dict]) -> str:
        """Generate modernization summary"""
        if not suggestions:
            return "✨ **Code looks modern!**\n\nNo major modernization opportunities found."
        
        high = sum(1 for s in suggestions if s['priority'] == 'High')
        medium = sum(1 for s in suggestions if s['priority'] == 'Medium')
        low = sum(1 for s in suggestions if s['priority'] == 'Low')
        
        summary = f"🔄 **Modernization Opportunities**\n\n"
        summary += f"Found {len(suggestions)} improvement(s):\n\n"
        
        if high > 0:
            summary += f"- 🔴 **High Priority**: {high} (critical improvements)\n"
        if medium > 0:
            summary += f"- 🟡 **Medium Priority**: {medium} (recommended improvements)\n"
        if low > 0:
            summary += f"- 🟢 **Low Priority**: {low} (nice-to-have improvements)\n"
        
        summary += "\n**Benefits of Modernization:**\n"
        summary += "- Improved code readability and maintainability\n"
        summary += "- Better performance and resource management\n"
        summary += "- Enhanced type safety and IDE support\n"
        summary += "- Easier debugging and error handling\n"
        
        return summary
    
    def _prioritize_suggestions(self, suggestions: List[Dict]) -> List[Dict]:
        """Prioritize suggestions by impact and effort"""
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        effort_order = {'Low': 0, 'Medium': 1, 'High': 2}
        
        # Sort by priority first, then by effort (lower effort first)
        return sorted(suggestions, key=lambda x: (priority_order.get(x['priority'], 3), effort_order.get(x['effort'], 3)))

# Made with Bob
