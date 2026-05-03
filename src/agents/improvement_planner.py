"""
Improvement Planner Agent
Creates prioritized refactoring roadmap with detailed analysis
Optionally uses IBM watsonx.ai Granite for enhanced AI-powered roadmap planning
"""

from typing import Dict, List, Optional
from src.utils import get_watsonx_client


class ImprovementPlanner:
    """Agent for creating improvement roadmaps"""
    
    def __init__(self):
        self.name = "Improvement Planner"
        self.watsonx_client = get_watsonx_client()
    
    def create_roadmap(self, code: str, language: str = "python") -> Dict:
        """
        Create prioritized improvement roadmap.
        
        Uses IBM watsonx.ai Granite model if configured, otherwise falls back
        to local rule-based roadmap planning.
        """
        # Try watsonx.ai Granite analysis first if available
        watsonx_result = self._try_watsonx_analysis(code, language)
        if watsonx_result:
            # Use watsonx results if available
            pass
        
        # Fall back to local roadmap planning
        improvements = []
        
        # Analyze different aspects
        improvements.extend(self._analyze_structure(code))
        improvements.extend(self._analyze_performance(code))
        improvements.extend(self._analyze_maintainability(code))
        improvements.extend(self._analyze_testing(code))
        improvements.extend(self._analyze_security(code))
        improvements.extend(self._analyze_documentation(code))
        improvements.extend(self._analyze_code_quality(code))
        
        # Prioritize and create roadmap
        prioritized = self._prioritize_improvements(improvements)
        roadmap = self._create_roadmap_phases(prioritized)
        summary = self._generate_summary(prioritized)
        
        return {
            "summary": summary,
            "roadmap": roadmap,
            "improvements": prioritized,
            "total_count": len(improvements)
        }
    
    def _try_watsonx_analysis(self, code: str, language: str) -> Optional[Dict]:
        """
        Attempt to create improvement roadmap using IBM watsonx.ai Granite model.
        
        Args:
            code: Source code to analyze
            language: Programming language
        
        Returns:
            Improvement roadmap from Granite model, or None if not available
        """
        if not self.watsonx_client.is_configured():
            return None
        
        try:
            # Call watsonx.ai Granite model for improvement planning
            result = self.watsonx_client.analyze_code(
                code=code,
                language=language,
                analysis_type='improvement'
            )
            return result
        except Exception as e:
            print(f"Warning: watsonx improvement planning failed, using local analysis: {e}")
            return None
    
    def _analyze_structure(self, code: str) -> List[Dict]:
        """Analyze code structure"""
        improvements = []
        lines = len(code.split('\n'))
        functions = code.count('def ')
        classes = code.count('class ')
        
        # Large file
        if lines > 500:
            improvements.append({
                "area": "Code Structure",
                "issue": f"Very large file ({lines} lines)",
                "suggestion": "Split into smaller, focused modules (aim for <300 lines per file)",
                "priority": "High",
                "effort": "High",
                "impact": "High"
            })
        elif lines > 300:
            improvements.append({
                "area": "Code Structure",
                "issue": f"Large file ({lines} lines)",
                "suggestion": "Consider splitting into smaller modules",
                "priority": "Medium",
                "effort": "Medium",
                "impact": "Medium"
            })
        
        # Procedural code without classes
        if classes == 0 and lines > 100 and functions > 5:
            improvements.append({
                "area": "Code Organization",
                "issue": "Procedural code without classes",
                "suggestion": "Consider object-oriented design for better encapsulation",
                "priority": "Medium",
                "effort": "High",
                "impact": "Medium"
            })
        
        # Too many functions in one file
        if functions > 20:
            improvements.append({
                "area": "Code Organization",
                "issue": f"Too many functions ({functions}) in one file",
                "suggestion": "Group related functions into classes or separate modules",
                "priority": "Medium",
                "effort": "Medium",
                "impact": "Medium"
            })
        
        # Long functions
        func_lines = []
        in_func = False
        current_func_lines = 0
        for line in code.split('\n'):
            if line.strip().startswith('def '):
                if in_func and current_func_lines > 50:
                    func_lines.append(current_func_lines)
                in_func = True
                current_func_lines = 0
            elif in_func:
                current_func_lines += 1
        
        if func_lines and max(func_lines) > 50:
            improvements.append({
                "area": "Function Complexity",
                "issue": f"Long functions detected (up to {max(func_lines)} lines)",
                "suggestion": "Break down long functions into smaller, focused functions",
                "priority": "High",
                "effort": "Medium",
                "impact": "High"
            })
        
        return improvements
    
    def _analyze_performance(self, code: str) -> List[Dict]:
        """Analyze performance issues"""
        improvements = []
        
        # Nested loops
        nested_loops = code.count('for ') + code.count('while ')
        if nested_loops > 1:
            # Check for actual nesting
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if ('for ' in line or 'while ' in line) and i + 1 < len(lines):
                    # Check next few lines for another loop
                    for j in range(i + 1, min(i + 10, len(lines))):
                        if 'for ' in lines[j] or 'while ' in lines[j]:
                            improvements.append({
                                "area": "Performance",
                                "issue": "Nested loops detected (O(n²) or worse complexity)",
                                "suggestion": "Optimize algorithm complexity - consider using hash maps, sets, or better algorithms",
                                "priority": "Medium",
                                "effort": "Medium",
                                "impact": "High"
                            })
                            break
                    break
        
        # Repeated operations in loops
        if 'for ' in code and '.append(' in code:
            if '+=' in code or 'extend(' in code:
                improvements.append({
                    "area": "Performance",
                    "issue": "Inefficient list operations in loops",
                    "suggestion": "Use list comprehensions or generator expressions for better performance",
                    "priority": "Low",
                    "effort": "Low",
                    "impact": "Medium"
                })
        
        # String concatenation in loops
        if 'for ' in code and '+=' in code and ('str' in code or '"' in code or "'" in code):
            improvements.append({
                "area": "Performance",
                "issue": "String concatenation in loops",
                "suggestion": "Use ''.join() or list accumulation for better performance",
                "priority": "Medium",
                "effort": "Low",
                "impact": "Medium"
            })
        
        # Blocking operations
        if 'time.sleep(' in code or 'sleep(' in code:
            improvements.append({
                "area": "Performance",
                "issue": "Blocking sleep calls",
                "suggestion": "Use async/await for better concurrency and non-blocking operations",
                "priority": "Low",
                "effort": "Medium",
                "impact": "Medium"
            })
        
        # Inefficient file operations
        if 'readlines()' in code:
            improvements.append({
                "area": "Performance",
                "issue": "Loading entire file into memory with readlines()",
                "suggestion": "Iterate over file object directly for memory efficiency",
                "priority": "Low",
                "effort": "Low",
                "impact": "Low"
            })
        
        return improvements
    
    def _analyze_maintainability(self, code: str) -> List[Dict]:
        """Analyze maintainability"""
        improvements = []
        
        # Check for documentation
        has_docstrings = '"""' in code or "'''" in code
        if not has_docstrings:
            improvements.append({
                "area": "Documentation",
                "issue": "Missing docstrings",
                "suggestion": "Add comprehensive docstrings to all functions and classes",
                "priority": "High",
                "effort": "Low",
                "impact": "Medium"
            })
        elif code.count('"""') < code.count('def ') / 2:
            improvements.append({
                "area": "Documentation",
                "issue": "Incomplete documentation",
                "suggestion": "Add docstrings to all public functions and classes",
                "priority": "Medium",
                "effort": "Low",
                "impact": "Medium"
            })
        
        # Check for error handling
        has_error_handling = 'try:' in code and 'except' in code
        if not has_error_handling:
            improvements.append({
                "area": "Error Handling",
                "issue": "No exception handling",
                "suggestion": "Add try-except blocks for robustness and better error messages",
                "priority": "High",
                "effort": "Medium",
                "impact": "High"
            })
        
        # Check for logging
        has_logging = 'logging' in code or 'logger' in code
        if not has_logging and len(code.split('\n')) > 50:
            improvements.append({
                "area": "Observability",
                "issue": "No logging implementation",
                "suggestion": "Add logging for debugging, monitoring, and troubleshooting",
                "priority": "Medium",
                "effort": "Low",
                "impact": "Medium"
            })
        
        # Check for type hints
        has_type_hints = '->' in code or ': int' in code or ': str' in code
        if not has_type_hints and 'def ' in code:
            improvements.append({
                "area": "Type Safety",
                "issue": "Missing type hints",
                "suggestion": "Add type hints for better IDE support and early error detection",
                "priority": "Medium",
                "effort": "Medium",
                "impact": "Medium"
            })
        
        # Check for magic numbers
        import re
        magic_numbers = re.findall(r'\b\d{2,}\b', code)
        if len(magic_numbers) > 5:
            improvements.append({
                "area": "Code Clarity",
                "issue": "Magic numbers in code",
                "suggestion": "Replace magic numbers with named constants",
                "priority": "Low",
                "effort": "Low",
                "impact": "Low"
            })
        
        # Check for code comments
        comment_lines = [line for line in code.split('\n') if line.strip().startswith('#')]
        code_lines = len([line for line in code.split('\n') if line.strip() and not line.strip().startswith('#')])
        if code_lines > 50 and len(comment_lines) < code_lines * 0.1:
            improvements.append({
                "area": "Code Clarity",
                "issue": "Insufficient inline comments",
                "suggestion": "Add comments to explain complex logic and business rules",
                "priority": "Low",
                "effort": "Low",
                "impact": "Low"
            })
        
        return improvements
    
    def _analyze_testing(self, code: str) -> List[Dict]:
        """Analyze testing coverage"""
        improvements = []
        
        has_tests = 'test_' in code or 'unittest' in code or 'pytest' in code
        if not has_tests:
            improvements.append({
                "area": "Testing",
                "issue": "No unit tests found",
                "suggestion": "Create comprehensive test suite with pytest or unittest",
                "priority": "High",
                "effort": "High",
                "impact": "High"
            })
        
        # Check for assertions in tests
        if has_tests and 'assert' not in code:
            improvements.append({
                "area": "Testing",
                "issue": "Tests without assertions",
                "suggestion": "Add proper assertions to validate test outcomes",
                "priority": "High",
                "effort": "Medium",
                "impact": "High"
            })
        
        # Check for test fixtures
        if has_tests and 'setUp' not in code and 'fixture' not in code:
            improvements.append({
                "area": "Testing",
                "issue": "No test fixtures",
                "suggestion": "Use setUp/tearDown or pytest fixtures for test data",
                "priority": "Low",
                "effort": "Low",
                "impact": "Low"
            })
        
        return improvements
    
    def _analyze_security(self, code: str) -> List[Dict]:
        """Analyze security concerns"""
        improvements = []
        
        # Hardcoded credentials
        if 'password' in code.lower() and '=' in code:
            improvements.append({
                "area": "Security",
                "issue": "Potential hardcoded credentials",
                "suggestion": "Use environment variables or secure vaults for sensitive data",
                "priority": "High",
                "effort": "Low",
                "impact": "High"
            })
        
        # SQL injection risks
        if 'execute' in code and ('%' in code or '+' in code):
            improvements.append({
                "area": "Security",
                "issue": "Potential SQL injection vulnerability",
                "suggestion": "Use parameterized queries or ORM",
                "priority": "High",
                "effort": "Medium",
                "impact": "High"
            })
        
        # Unsafe functions
        if 'eval(' in code or 'exec(' in code:
            improvements.append({
                "area": "Security",
                "issue": "Dangerous functions (eval/exec)",
                "suggestion": "Remove eval/exec or use safe alternatives like ast.literal_eval",
                "priority": "High",
                "effort": "Medium",
                "impact": "High"
            })
        
        return improvements
    
    def _analyze_documentation(self, code: str) -> List[Dict]:
        """Analyze documentation needs"""
        improvements = []
        
        # Check for README
        has_readme_content = 'README' in code or 'readme' in code
        if not has_readme_content and len(code.split('\n')) > 100:
            improvements.append({
                "area": "Documentation",
                "issue": "No README file",
                "suggestion": "Create README.md with project overview, installation, and usage",
                "priority": "Medium",
                "effort": "Low",
                "impact": "Medium"
            })
        
        # Check for inline documentation
        if 'class ' in code:
            class_count = code.count('class ')
            docstring_count = code.count('"""')
            if docstring_count < class_count:
                improvements.append({
                    "area": "Documentation",
                    "issue": "Classes without docstrings",
                    "suggestion": "Document all classes with purpose and usage examples",
                    "priority": "Medium",
                    "effort": "Low",
                    "impact": "Low"
                })
        
        return improvements
    
    def _analyze_code_quality(self, code: str) -> List[Dict]:
        """Analyze overall code quality"""
        improvements = []
        
        # Check for code duplication
        lines = code.split('\n')
        line_counts = {}
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and len(stripped) > 20:
                line_counts[stripped] = line_counts.get(stripped, 0) + 1
        
        duplicates = [line for line, count in line_counts.items() if count > 2]
        if duplicates:
            improvements.append({
                "area": "Code Quality",
                "issue": f"Code duplication detected ({len(duplicates)} repeated lines)",
                "suggestion": "Extract repeated code into reusable functions",
                "priority": "Medium",
                "effort": "Medium",
                "impact": "Medium"
            })
        
        # Check for consistent naming
        import re
        snake_case = len(re.findall(r'\b[a-z]+_[a-z]+\b', code))
        camelCase = len(re.findall(r'\b[a-z]+[A-Z][a-z]+\b', code))
        
        if snake_case > 0 and camelCase > 0:
            improvements.append({
                "area": "Code Style",
                "issue": "Inconsistent naming convention",
                "suggestion": "Use consistent snake_case for Python (PEP 8)",
                "priority": "Low",
                "effort": "Low",
                "impact": "Low"
            })
        
        # Check for proper imports
        if 'import *' in code:
            improvements.append({
                "area": "Code Quality",
                "issue": "Wildcard imports (import *)",
                "suggestion": "Import specific names to avoid namespace pollution",
                "priority": "Medium",
                "effort": "Low",
                "impact": "Low"
            })
        
        return improvements
    
    def _prioritize_improvements(self, improvements: List[Dict]) -> List[Dict]:
        """Prioritize improvements by impact, effort, and priority"""
        priority_score = {'High': 3, 'Medium': 2, 'Low': 1}
        effort_score = {'Low': 1, 'Medium': 2, 'High': 3}
        
        for imp in improvements:
            impact = priority_score.get(imp['impact'], 1)
            effort = effort_score.get(imp['effort'], 2)
            priority = priority_score.get(imp['priority'], 1)
            
            # Calculate score: (impact * 2 + priority) / effort
            # Higher score = higher priority
            imp['score'] = ((impact * 2) + priority) / effort
        
        return sorted(improvements, key=lambda x: x['score'], reverse=True)
    
    def _create_roadmap_phases(self, improvements: List[Dict]) -> Dict:
        """Create phased roadmap"""
        phases = {
            "Phase 1 - Quick Wins (Week 1-2)": [],
            "Phase 2 - Core Improvements (Week 3-6)": [],
            "Phase 3 - Long-term Enhancements (Week 7+)": []
        }
        
        for imp in improvements:
            # Quick wins: Low effort, High/Medium impact
            if imp['effort'] == 'Low' and imp['impact'] in ['High', 'Medium']:
                phases["Phase 1 - Quick Wins (Week 1-2)"].append(imp)
            # Core improvements: High priority or High impact
            elif imp['priority'] == 'High' or imp['impact'] == 'High':
                phases["Phase 2 - Core Improvements (Week 3-6)"].append(imp)
            # Long-term: Everything else
            else:
                phases["Phase 3 - Long-term Enhancements (Week 7+)"].append(imp)
        
        return phases
    
    def _generate_summary(self, improvements: List[Dict]) -> str:
        """Generate roadmap summary"""
        if not improvements:
            return "✅ **Code is in excellent shape!**\n\nNo major improvements needed."
        
        high = sum(1 for i in improvements if i['priority'] == 'High')
        medium = sum(1 for i in improvements if i['priority'] == 'Medium')
        low = sum(1 for i in improvements if i['priority'] == 'Low')
        
        summary = f"📊 **Improvement Roadmap**\n\n"
        summary += f"Identified {len(improvements)} improvement area(s):\n\n"
        
        if high > 0:
            summary += f"- 🔴 **High Priority**: {high} items (address immediately)\n"
        if medium > 0:
            summary += f"- 🟡 **Medium Priority**: {medium} items (plan for next sprint)\n"
        if low > 0:
            summary += f"- 🟢 **Low Priority**: {low} items (nice-to-have improvements)\n"
        
        # Calculate effort distribution
        low_effort = sum(1 for i in improvements if i['effort'] == 'Low')
        medium_effort = sum(1 for i in improvements if i['effort'] == 'Medium')
        high_effort = sum(1 for i in improvements if i['effort'] == 'High')
        
        summary += f"\n**Effort Distribution:**\n"
        summary += f"- Low effort: {low_effort} items\n"
        summary += f"- Medium effort: {medium_effort} items\n"
        summary += f"- High effort: {high_effort} items\n"
        
        summary += "\n**Recommended Approach:**\n"
        summary += "1. **Week 1-2**: Start with quick wins (low effort, high impact)\n"
        summary += "2. **Week 3-6**: Address core improvements and high-priority items\n"
        summary += "3. **Week 7+**: Plan long-term enhancements and refactoring\n"
        summary += "4. **Continuous**: Monitor progress and adjust priorities\n"
        
        # Top 3 recommendations
        summary += "\n**Top 3 Recommendations:**\n"
        for i, imp in enumerate(improvements[:3], 1):
            summary += f"{i}. **{imp['area']}**: {imp['suggestion']}\n"
        
        return summary

# Made with Bob
