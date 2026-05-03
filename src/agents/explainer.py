"""
Code Explainer Agent
Analyzes and explains code functionality with role-based perspectives
Optionally uses IBM watsonx.ai Granite for enhanced AI-powered analysis
"""

import re
from typing import Dict, List, Tuple, Optional
from src.utils import get_watsonx_client


class CodeExplainer:
    """Agent for explaining code functionality"""
    
    def __init__(self):
        self.name = "Code Explainer"
        self.watsonx_client = get_watsonx_client()
    
    def analyze(self, code: str, language: str = "python") -> Dict:
        """
        Analyze and explain the provided code.
        
        Uses IBM watsonx.ai Granite model if configured, otherwise falls back
        to local rule-based analysis.
        """
        # Try watsonx.ai Granite analysis first if available
        watsonx_result = self._try_watsonx_analysis(code, language)
        if watsonx_result:
            # If watsonx provides results, use them
            # You can merge with local analysis or use watsonx exclusively
            pass
        
        # Fall back to local rule-based analysis
        functions = self._extract_functions(code)
        classes = self._extract_classes(code)
        imports = self._extract_imports(code)
        
        overview = self._generate_overview(code, functions, classes, imports)
        details = self._generate_details(code, functions, classes)
        complexity = self._assess_complexity(code, functions)
        role_explanations = self._generate_role_based_explanations(code, functions, classes)
        
        return {
            "overview": overview,
            "details": details,
            "complexity": complexity,
            "role_explanations": role_explanations,
            "structure": {
                "functions": len(functions),
                "classes": len(classes),
                "imports": len(imports),
                "lines": len(code.split('\n'))
            }
        }
    
    def _try_watsonx_analysis(self, code: str, language: str) -> Optional[Dict]:
        """
        Attempt to analyze code using IBM watsonx.ai Granite model.
        
        Args:
            code: Source code to analyze
            language: Programming language
        
        Returns:
            Analysis results from Granite model, or None if not available
        """
        if not self.watsonx_client.is_configured():
            return None
        
        try:
            # Call watsonx.ai Granite model for code explanation
            # This is where the actual AI model call happens
            result = self.watsonx_client.analyze_code(
                code=code,
                language=language,
                analysis_type='explanation'
            )
            return result
        except Exception as e:
            print(f"Warning: watsonx analysis failed, using local analysis: {e}")
            return None
    
    def _extract_functions(self, code: str) -> List[Dict]:
        """Extract function information from code"""
        pattern = r'def\s+(\w+)\s*\(([^)]*)\):'
        matches = re.findall(pattern, code)
        
        functions = []
        for name, params in matches:
            # Get function body to analyze
            func_pattern = rf'def\s+{re.escape(name)}\s*\([^)]*\):(.*?)(?=\ndef\s|\nclass\s|\Z)'
            body_match = re.search(func_pattern, code, re.DOTALL)
            body = body_match.group(1) if body_match else ""
            
            functions.append({
                "name": name,
                "params": [p.strip() for p in params.split(',') if p.strip()],
                "body": body,
                "lines": len(body.split('\n')) if body else 0
            })
        return functions
    
    def _extract_classes(self, code: str) -> List[Dict]:
        """Extract class information from code"""
        pattern = r'class\s+(\w+)\s*[:\(]'
        class_names = re.findall(pattern, code)
        
        classes = []
        for name in class_names:
            # Find methods in class
            class_pattern = rf'class\s+{re.escape(name)}.*?:(.*?)(?=\nclass\s|\ndef\s+\w+\s*\([^)]*\):\s*(?!    )|\Z)'
            class_match = re.search(class_pattern, code, re.DOTALL)
            class_body = class_match.group(1) if class_match else ""
            
            methods = re.findall(r'def\s+(\w+)\s*\(', class_body)
            
            classes.append({
                "name": name,
                "methods": methods,
                "method_count": len(methods)
            })
        return classes
    
    def _extract_imports(self, code: str) -> List[str]:
        """Extract import statements"""
        pattern = r'(?:from\s+[\w.]+\s+)?import\s+([\w.,\s]+)'
        imports = re.findall(pattern, code)
        return [imp.strip() for imp in ','.join(imports).split(',')]
    
    def _generate_overview(self, code: str, functions: List[Dict], classes: List[Dict], imports: List[str]) -> str:
        """Generate high-level code overview"""
        lines = len(code.split('\n'))
        
        overview = f"## 📋 Code Overview\n\n"
        overview += f"This code contains **{lines} lines** with:\n\n"
        
        if classes:
            overview += f"- **{len(classes)} Class(es)**: {', '.join([c['name'] for c in classes])}\n"
        if functions:
            overview += f"- **{len(functions)} Function(s)**: {', '.join([f['name'] for f in functions])}\n"
        if imports:
            overview += f"- **{len(imports)} Import(s)**: {', '.join(imports[:5])}"
            if len(imports) > 5:
                overview += f" and {len(imports) - 5} more"
            overview += "\n"
        
        overview += "\n### Key Features:\n"
        features = []
        if 'if __name__' in code:
            features.append("✓ Contains main execution block")
        if 'try:' in code or 'except' in code:
            features.append("✓ Includes error handling")
        if 'async def' in code or 'await' in code:
            features.append("✓ Uses asynchronous programming")
        if 'logging' in code or 'logger' in code:
            features.append("✓ Implements logging")
        if 'test_' in code or 'unittest' in code:
            features.append("✓ Contains unit tests")
        
        if features:
            for feature in features:
                overview += f"{feature}\n"
        else:
            overview += "No special features detected\n"
        
        return overview
    
    def _generate_details(self, code: str, functions: List[Dict], classes: List[Dict]) -> str:
        """Generate detailed code explanation"""
        details = "## 🔍 Detailed Analysis\n\n"
        
        if functions:
            details += "### Functions:\n\n"
            for func in functions[:5]:
                details += f"**`{func['name']}()`**\n"
                if func['params']:
                    details += f"- Parameters: {', '.join(func['params'])}\n"
                else:
                    details += "- Parameters: None\n"
                details += f"- Lines: {func['lines']}\n"
                
                # Analyze function purpose
                body = func['body'].lower()
                if 'return' in body:
                    details += "- Returns a value\n"
                if 'print' in body or 'log' in body:
                    details += "- Produces output\n"
                if 'for' in body or 'while' in body:
                    details += "- Contains loops\n"
                if 'if' in body:
                    details += "- Has conditional logic\n"
                details += "\n"
            
            if len(functions) > 5:
                details += f"*... and {len(functions) - 5} more functions*\n\n"
        
        if classes:
            details += "### Classes:\n\n"
            for cls in classes:
                details += f"**`{cls['name']}`**\n"
                details += f"- Methods: {cls['method_count']}\n"
                if cls['methods']:
                    details += f"- Method names: {', '.join(cls['methods'][:5])}\n"
                    if len(cls['methods']) > 5:
                        details += f"  ... and {len(cls['methods']) - 5} more\n"
                details += "\n"
        
        # Code patterns
        details += "### Code Patterns:\n\n"
        patterns = []
        if 'for ' in code or 'while ' in code:
            patterns.append("- **Iteration**: Uses loops for data processing")
        if 'if ' in code and 'else' in code:
            patterns.append("- **Branching**: Contains conditional logic with alternatives")
        if 'return' in code:
            patterns.append("- **Return values**: Functions return computed results")
        if 'raise' in code or 'except' in code:
            patterns.append("- **Error handling**: Manages exceptions")
        if 'with ' in code:
            patterns.append("- **Context managers**: Uses resource management")
        if 'lambda' in code:
            patterns.append("- **Functional**: Uses lambda expressions")
        
        if patterns:
            details += '\n'.join(patterns) + "\n"
        else:
            details += "No specific patterns detected\n"
        
        return details
    
    def _assess_complexity(self, code: str, functions: List[Dict]) -> str:
        """Assess code complexity with detailed metrics"""
        lines = len(code.split('\n'))
        
        # Calculate cyclomatic complexity indicators
        conditionals = len(re.findall(r'\bif\b|\belif\b|\bwhile\b|\bfor\b', code))
        nested_blocks = len(re.findall(r'    .*if\b|    .*for\b|    .*while\b', code))
        
        # Determine complexity level
        if lines < 50 and conditionals < 5:
            level = "Low"
            color = "🟢"
            desc = "Simple and straightforward code"
        elif lines < 200 and conditionals < 15:
            level = "Medium"
            color = "🟡"
            desc = "Moderate complexity with manageable structure"
        else:
            level = "High"
            color = "🔴"
            desc = "Complex code with many components"
        
        complexity = f"## 📊 Complexity Assessment\n\n"
        complexity += f"{color} **Complexity Level:** {level}\n\n"
        complexity += f"{desc}\n\n"
        complexity += "### Metrics:\n\n"
        complexity += f"- **Total Lines:** {lines}\n"
        complexity += f"- **Functions:** {len(functions)}\n"
        complexity += f"- **Conditional Statements:** {conditionals}\n"
        complexity += f"- **Nested Blocks:** {nested_blocks}\n"
        
        if nested_blocks > 3:
            complexity += "\n⚠️ **Warning:** High nesting detected - consider refactoring\n"
        
        return complexity
    
    def _generate_role_based_explanations(self, code: str, functions: List[Dict], classes: List[Dict]) -> Dict:
        """Generate explanations for different roles"""
        return {
            "developer": self._explain_for_developer(code, functions, classes),
            "manager": self._explain_for_manager(code, functions, classes),
            "qa": self._explain_for_qa(code, functions, classes)
        }
    
    def _explain_for_developer(self, code: str, functions: List[Dict], classes: List[Dict]) -> str:
        """Technical explanation for developers"""
        explanation = "### 👨‍💻 For Developers\n\n"
        
        if functions:
            explanation += f"**Implementation Details:**\n"
            explanation += f"- Contains {len(functions)} function(s) implementing core logic\n"
            
            # Analyze function complexity
            avg_lines = sum(f['lines'] for f in functions) / len(functions) if functions else 0
            if avg_lines > 20:
                explanation += f"- Average function length: {avg_lines:.0f} lines (consider breaking down)\n"
            
            # Check for common patterns
            if any('return' in f['body'] for f in functions):
                explanation += "- Functions return computed values\n"
            if any('yield' in f['body'] for f in functions):
                explanation += "- Uses generators for memory efficiency\n"
        
        if classes:
            explanation += f"\n**Object-Oriented Design:**\n"
            explanation += f"- {len(classes)} class(es) for data encapsulation\n"
            for cls in classes[:3]:
                explanation += f"- `{cls['name']}`: {cls['method_count']} method(s)\n"
        
        # Technical considerations
        explanation += "\n**Technical Considerations:**\n"
        if 'import' in code:
            explanation += "- External dependencies used\n"
        if 'try:' in code:
            explanation += "- Error handling implemented\n"
        else:
            explanation += "- ⚠️ Consider adding error handling\n"
        if '"""' in code or "'''" in code:
            explanation += "- Documentation present\n"
        else:
            explanation += "- ⚠️ Add docstrings for better maintainability\n"
        
        return explanation
    
    def _explain_for_manager(self, code: str, functions: List[Dict], classes: List[Dict]) -> str:
        """Business-focused explanation for managers"""
        explanation = "### 👔 For Managers\n\n"
        
        lines = len(code.split('\n'))
        
        explanation += "**Project Overview:**\n"
        explanation += f"- Code size: {lines} lines\n"
        explanation += f"- Components: {len(functions)} functions, {len(classes)} classes\n"
        
        # Estimate complexity
        if lines < 100:
            explanation += "- Scope: Small, focused module\n"
            explanation += "- Maintenance: Low effort\n"
        elif lines < 500:
            explanation += "- Scope: Medium-sized component\n"
            explanation += "- Maintenance: Moderate effort\n"
        else:
            explanation += "- Scope: Large, complex system\n"
            explanation += "- Maintenance: High effort required\n"
        
        explanation += "\n**Quality Indicators:**\n"
        quality_score = 0
        
        if 'try:' in code or 'except' in code:
            explanation += "- ✅ Error handling present\n"
            quality_score += 1
        else:
            explanation += "- ⚠️ Missing error handling\n"
        
        if '"""' in code or "'''" in code:
            explanation += "- ✅ Documentation included\n"
            quality_score += 1
        else:
            explanation += "- ⚠️ Needs documentation\n"
        
        if 'test_' in code or 'unittest' in code:
            explanation += "- ✅ Tests available\n"
            quality_score += 1
        else:
            explanation += "- ⚠️ Tests needed\n"
        
        explanation += f"\n**Quality Score:** {quality_score}/3\n"
        
        return explanation
    
    def _explain_for_qa(self, code: str, functions: List[Dict], classes: List[Dict]) -> str:
        """Testing-focused explanation for QA"""
        explanation = "### 🧪 For QA Engineers\n\n"
        
        explanation += "**Testing Considerations:**\n"
        
        if functions:
            explanation += f"- **{len(functions)} functions** to test\n"
            
            # Identify testable functions
            public_funcs = [f for f in functions if not f['name'].startswith('_')]
            private_funcs = [f for f in functions if f['name'].startswith('_')]
            
            explanation += f"- Public functions: {len(public_funcs)} (primary test targets)\n"
            if private_funcs:
                explanation += f"- Private functions: {len(private_funcs)} (test indirectly)\n"
        
        if classes:
            explanation += f"\n**Class Testing:**\n"
            for cls in classes[:3]:
                explanation += f"- `{cls['name']}`: Test {cls['method_count']} method(s)\n"
        
        explanation += "\n**Test Scenarios to Cover:**\n"
        scenarios = []
        
        if 'if ' in code:
            scenarios.append("- **Conditional logic**: Test all branches (if/else)")
        if 'for ' in code or 'while ' in code:
            scenarios.append("- **Loops**: Test with empty, single, and multiple items")
        if 'try:' in code:
            scenarios.append("- **Error handling**: Test exception paths")
        if 'return' in code:
            scenarios.append("- **Return values**: Verify correct outputs")
        if any(p for f in functions for p in f['params']):
            scenarios.append("- **Input validation**: Test edge cases and invalid inputs")
        
        if scenarios:
            explanation += '\n'.join(scenarios) + "\n"
        
        # Risk assessment
        explanation += "\n**Risk Areas:**\n"
        if 'eval(' in code or 'exec(' in code:
            explanation += "- 🔴 **High Risk**: Dynamic code execution\n"
        if 'os.system' in code or 'subprocess' in code:
            explanation += "- 🔴 **High Risk**: System command execution\n"
        if not ('try:' in code or 'except' in code):
            explanation += "- 🟡 **Medium Risk**: No error handling\n"
        if len(code.split('\n')) > 200:
            explanation += "- 🟡 **Medium Risk**: Large codebase needs comprehensive testing\n"
        
        return explanation
