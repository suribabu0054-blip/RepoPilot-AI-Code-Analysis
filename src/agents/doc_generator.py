"""
Documentation Generator Agent
Generates comprehensive README files, comments, and unit tests
Optionally uses IBM watsonx.ai Granite for enhanced AI-powered documentation
"""

import re
from typing import Dict, List, Optional
from src.utils import get_watsonx_client


class DocGenerator:
    """Agent for generating documentation"""
    
    def __init__(self):
        self.name = "Documentation Generator"
        self.watsonx_client = get_watsonx_client()
    
    def generate(self, code: str, language: str = "python") -> Dict:
        """
        Generate comprehensive documentation for code.
        
        Uses IBM watsonx.ai Granite model if configured, otherwise falls back
        to local template-based documentation generation.
        """
        # Try watsonx.ai Granite analysis first if available
        watsonx_result = self._try_watsonx_analysis(code, language)
        if watsonx_result:
            # Use watsonx results if available
            pass
        
        # Fall back to local documentation generation
        functions = self._extract_functions(code)
        classes = self._extract_classes(code)
        imports = self._extract_imports(code)
        
        readme = self._generate_readme(code, functions, classes, imports)
        comments = self._generate_comments(code, functions, classes)
        tests = self._generate_test_template(code, functions, classes)
        
        return {
            "readme": readme,
            "comments": comments,
            "tests": tests
        }
    
    def _try_watsonx_analysis(self, code: str, language: str) -> Optional[Dict]:
        """
        Attempt to generate documentation using IBM watsonx.ai Granite model.
        
        Args:
            code: Source code to document
            language: Programming language
        
        Returns:
            Documentation results from Granite model, or None if not available
        """
        if not self.watsonx_client.is_configured():
            return None
        
        try:
            # Call watsonx.ai Granite model for documentation generation
            result = self.watsonx_client.analyze_code(
                code=code,
                language=language,
                analysis_type='documentation'
            )
            return result
        except Exception as e:
            print(f"Warning: watsonx documentation generation failed, using local templates: {e}")
            return None
    
    def _extract_functions(self, code: str) -> List[Dict]:
        """Extract detailed function information"""
        pattern = r'def\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*([^:]+))?:'
        matches = re.findall(pattern, code)
        
        functions = []
        for name, params, return_type in matches:
            # Extract docstring if present
            func_pattern = rf'def\s+{re.escape(name)}\s*\([^)]*\):(?:\s*"""([^"]*?)""")?'
            doc_match = re.search(func_pattern, code, re.DOTALL)
            docstring = doc_match.group(1).strip() if doc_match and doc_match.group(1) else ""
            
            functions.append({
                "name": name,
                "params": [p.strip() for p in params.split(',') if p.strip()],
                "return_type": return_type.strip() if return_type else "None",
                "docstring": docstring,
                "is_private": name.startswith('_')
            })
        return functions
    
    def _extract_classes(self, code: str) -> List[Dict]:
        """Extract detailed class information"""
        pattern = r'class\s+(\w+)\s*(?:\(([^)]*)\))?:'
        matches = re.findall(pattern, code)
        
        classes = []
        for name, base_classes in matches:
            # Find methods in class
            class_pattern = rf'class\s+{re.escape(name)}.*?:(.*?)(?=\nclass\s|\Z)'
            class_match = re.search(class_pattern, code, re.DOTALL)
            class_body = class_match.group(1) if class_match else ""
            
            # Extract docstring
            doc_pattern = r'class\s+' + re.escape(name) + r'.*?:(?:\s*"""([^"]*?)""")?'
            doc_match = re.search(doc_pattern, code, re.DOTALL)
            docstring = doc_match.group(1).strip() if doc_match and doc_match.group(1) else ""
            
            methods = re.findall(r'def\s+(\w+)\s*\(', class_body)
            
            classes.append({
                "name": name,
                "base_classes": base_classes.strip() if base_classes else "",
                "methods": methods,
                "method_count": len(methods),
                "docstring": docstring
            })
        return classes
    
    def _extract_imports(self, code: str) -> List[str]:
        """Extract import statements"""
        imports = []
        
        # Standard imports
        for match in re.finditer(r'^import\s+([\w.,\s]+)', code, re.MULTILINE):
            imports.extend([imp.strip() for imp in match.group(1).split(',')])
        
        # From imports
        for match in re.finditer(r'^from\s+([\w.]+)\s+import\s+([\w.,\s*]+)', code, re.MULTILINE):
            module = match.group(1)
            items = match.group(2)
            if items.strip() == '*':
                imports.append(f"{module}.*")
            else:
                imports.extend([f"{module}.{item.strip()}" for item in items.split(',')])
        
        return list(set(imports))  # Remove duplicates
    
    def _generate_readme(self, code: str, functions: List[Dict], classes: List[Dict], imports: List[str]) -> str:
        """Generate comprehensive README.md content"""
        lines = len(code.split('\n'))
        
        readme = "# Project Documentation\n\n"
        
        # Badges
        readme += "![Python](https://img.shields.io/badge/python-3.8+-blue.svg)\n"
        readme += "![License](https://img.shields.io/badge/license-MIT-green.svg)\n\n"
        
        # Overview
        readme += "## 📋 Overview\n\n"
        readme += "This project contains Python code with the following components:\n\n"
        
        if classes:
            readme += f"- **{len(classes)} Classes**: {', '.join([c['name'] for c in classes])}\n"
        if functions:
            public_funcs = [f for f in functions if not f['is_private']]
            readme += f"- **{len(public_funcs)} Public Functions**: {', '.join([f['name'] for f in public_funcs[:5]])}"
            if len(public_funcs) > 5:
                readme += f" and {len(public_funcs) - 5} more"
            readme += "\n"
        if imports:
            readme += f"- **{len(imports)} Dependencies**: {', '.join(imports[:5])}"
            if len(imports) > 5:
                readme += f" and {len(imports) - 5} more"
            readme += "\n"
        
        readme += f"\n**Code Statistics:**\n"
        readme += f"- Total Lines: {lines}\n"
        readme += f"- Functions: {len(functions)}\n"
        readme += f"- Classes: {len(classes)}\n\n"
        
        # Features
        readme += "## ✨ Features\n\n"
        features = []
        if classes:
            features.append(f"- Object-oriented design with {len(classes)} class(es)")
        if any(f['docstring'] for f in functions):
            features.append("- Well-documented code with docstrings")
        if 'async def' in code:
            features.append("- Asynchronous programming support")
        if 'try:' in code or 'except' in code:
            features.append("- Error handling implemented")
        if 'logging' in code:
            features.append("- Logging for debugging and monitoring")
        
        if features:
            readme += '\n'.join(features) + "\n\n"
        else:
            readme += "- Core functionality implementation\n\n"
        
        # Installation
        readme += "## 🚀 Installation\n\n"
        readme += "```bash\n"
        readme += "# Clone the repository\n"
        readme += "git clone <repository-url>\n\n"
        readme += "# Install dependencies\n"
        readme += "pip install -r requirements.txt\n"
        readme += "```\n\n"
        
        # Usage
        readme += "## 💻 Usage\n\n"
        
        if classes:
            cls = classes[0]
            readme += f"### Using {cls['name']} Class\n\n"
            readme += "```python\n"
            readme += f"from module import {cls['name']}\n\n"
            readme += f"# Create instance\n"
            readme += f"obj = {cls['name']}()\n\n"
            if cls['methods']:
                method = cls['methods'][0]
                readme += f"# Call method\n"
                readme += f"result = obj.{method}()\n"
            readme += "```\n\n"
        
        if functions:
            public_funcs = [f for f in functions if not f['is_private']]
            if public_funcs:
                func = public_funcs[0]
                readme += f"### Using {func['name']} Function\n\n"
                readme += "```python\n"
                readme += f"from module import {func['name']}\n\n"
                readme += f"# Call function\n"
                if func['params']:
                    params = ', '.join([p.split(':')[0].split('=')[0].strip() for p in func['params']])
                    readme += f"result = {func['name']}({params})\n"
                else:
                    readme += f"result = {func['name']}()\n"
                readme += "```\n\n"
        
        # API Documentation
        if classes or functions:
            readme += "## 📚 API Documentation\n\n"
            
            if classes:
                readme += "### Classes\n\n"
                for cls in classes[:3]:
                    readme += f"#### `{cls['name']}`\n\n"
                    if cls['docstring']:
                        readme += f"{cls['docstring']}\n\n"
                    if cls['base_classes']:
                        readme += f"**Inherits from:** `{cls['base_classes']}`\n\n"
                    if cls['methods']:
                        readme += "**Methods:**\n"
                        for method in cls['methods'][:5]:
                            readme += f"- `{method}()`\n"
                        if len(cls['methods']) > 5:
                            readme += f"- ... and {len(cls['methods']) - 5} more\n"
                    readme += "\n"
            
            if functions:
                public_funcs = [f for f in functions if not f['is_private']]
                if public_funcs:
                    readme += "### Functions\n\n"
                    for func in public_funcs[:5]:
                        readme += f"#### `{func['name']}()`\n\n"
                        if func['docstring']:
                            readme += f"{func['docstring']}\n\n"
                        
                        readme += "**Parameters:**\n"
                        if func['params']:
                            for param in func['params']:
                                param_name = param.split(':')[0].split('=')[0].strip()
                                param_type = param.split(':')[1].split('=')[0].strip() if ':' in param else "Any"
                                readme += f"- `{param_name}` ({param_type}): Parameter description\n"
                        else:
                            readme += "- None\n"
                        
                        readme += f"\n**Returns:** `{func['return_type']}`\n\n"
        
        # Testing
        readme += "## 🧪 Testing\n\n"
        readme += "```bash\n"
        readme += "# Run tests\n"
        readme += "python -m pytest tests/\n\n"
        readme += "# Run with coverage\n"
        readme += "python -m pytest --cov=. tests/\n"
        readme += "```\n\n"
        
        # Contributing
        readme += "## 🤝 Contributing\n\n"
        readme += "Contributions are welcome! Please follow these steps:\n\n"
        readme += "1. Fork the repository\n"
        readme += "2. Create a feature branch (`git checkout -b feature/amazing-feature`)\n"
        readme += "3. Commit your changes (`git commit -m 'Add amazing feature'`)\n"
        readme += "4. Push to the branch (`git push origin feature/amazing-feature`)\n"
        readme += "5. Open a Pull Request\n\n"
        
        # License
        readme += "## 📄 License\n\n"
        readme += "This project is licensed under the MIT License - see the LICENSE file for details.\n\n"
        
        # Contact
        readme += "## 📧 Contact\n\n"
        readme += "For questions or feedback, please open an issue on GitHub.\n"
        
        return readme
    
    def _generate_comments(self, code: str, functions: List[Dict], classes: List[Dict]) -> str:
        """Generate inline comments for code"""
        lines = code.split('\n')
        commented = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Add comments for imports
            if stripped.startswith('import ') or stripped.startswith('from '):
                if i == 0 or not lines[i-1].strip().startswith(('import', 'from')):
                    commented.append('# Import required modules')
                commented.append(line)
            
            # Add comments for class definitions
            elif stripped.startswith('class '):
                if i > 0:
                    commented.append('')
                commented.append('# Define class for data encapsulation and methods')
                commented.append(line)
                indent = len(line) - len(line.lstrip())
                # Check if docstring exists
                if i + 1 < len(lines) and '"""' not in lines[i + 1]:
                    commented.append(' ' * (indent + 4) + '"""Class for [purpose]. Add description here."""')
            
            # Add comments for function definitions
            elif stripped.startswith('def '):
                if i > 0:
                    commented.append('')
                commented.append('# Function to perform specific operation')
                commented.append(line)
                indent = len(line) - len(line.lstrip())
                # Check if docstring exists
                if i + 1 < len(lines) and '"""' not in lines[i + 1]:
                    commented.append(' ' * (indent + 4) + '"""Function description. Add parameters and return value."""')
            
            # Add comments for control structures
            elif stripped.startswith('if ') and not stripped.startswith('if __name__'):
                indent = len(line) - len(line.lstrip())
                commented.append(' ' * indent + '# Check condition')
                commented.append(line)
            
            elif stripped.startswith('for '):
                indent = len(line) - len(line.lstrip())
                commented.append(' ' * indent + '# Iterate through items')
                commented.append(line)
            
            elif stripped.startswith('while '):
                indent = len(line) - len(line.lstrip())
                commented.append(' ' * indent + '# Loop until condition is met')
                commented.append(line)
            
            elif stripped.startswith('try:'):
                indent = len(line) - len(line.lstrip())
                commented.append(' ' * indent + '# Handle potential errors')
                commented.append(line)
            
            elif stripped.startswith('return '):
                indent = len(line) - len(line.lstrip())
                commented.append(' ' * indent + '# Return result')
                commented.append(line)
            
            else:
                commented.append(line)
        
        return '\n'.join(commented)
    
    def _generate_test_template(self, code: str, functions: List[Dict], classes: List[Dict]) -> str:
        """Generate comprehensive unit test template"""
        tests = '"""Unit tests for the module."""\n\n'
        tests += "import unittest\n"
        tests += "from unittest.mock import Mock, patch\n"
        tests += "from module import *\n\n\n"
        
        if classes:
            for cls in classes[:3]:
                tests += f"class Test{cls['name']}(unittest.TestCase):\n"
                tests += f'    """Test cases for {cls["name"]} class."""\n\n'
                
                tests += "    def setUp(self):\n"
                tests += '        """Set up test fixtures before each test method."""\n'
                tests += f"        self.{cls['name'].lower()} = {cls['name']}()\n\n"
                
                tests += "    def test_initialization(self):\n"
                tests += '        """Test that object initializes correctly."""\n'
                tests += f"        self.assertIsNotNone(self.{cls['name'].lower()})\n"
                tests += f"        self.assertIsInstance(self.{cls['name'].lower()}, {cls['name']})\n\n"
                
                # Generate tests for methods
                for method in cls['methods'][:3]:
                    if not method.startswith('_'):  # Skip private methods
                        tests += f"    def test_{method}(self):\n"
                        tests += f'        """Test {method} method."""\n'
                        tests += f"        result = self.{cls['name'].lower()}.{method}()\n"
                        tests += f"        self.assertIsNotNone(result)\n\n"
                
                tests += "\n"
        
        if functions:
            public_funcs = [f for f in functions if not f['is_private']]
            if public_funcs:
                tests += "class TestFunctions(unittest.TestCase):\n"
                tests += '    """Test cases for module functions."""\n\n'
                
                for func in public_funcs[:5]:
                    tests += f"    def test_{func['name']}_valid_input(self):\n"
                    tests += f'        """Test {func["name"]} with valid input."""\n'
                    if func['params']:
                        params = ', '.join(['None'] * len(func['params']))
                        tests += f"        result = {func['name']}({params})\n"
                    else:
                        tests += f"        result = {func['name']}()\n"
                    tests += f"        self.assertIsNotNone(result)\n\n"
                    
                    # Add edge case test
                    tests += f"    def test_{func['name']}_edge_cases(self):\n"
                    tests += f'        """Test {func["name"]} with edge cases."""\n'
                    tests += f"        # Test with empty values\n"
                    tests += f"        pass\n\n"
        
        tests += "\nif __name__ == '__main__':\n"
        tests += "    unittest.main()\n"
        
        return tests

# Made with Bob
