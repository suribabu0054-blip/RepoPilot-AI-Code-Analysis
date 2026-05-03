"""
IBM watsonx.ai Granite Integration Client
Provides AI-powered code analysis using IBM watsonx.ai Granite models.
Falls back to local rule-based analysis if credentials are not available.
"""

import os
from typing import Optional, Dict, Any


class WatsonxClient:
    """
    Client for IBM watsonx.ai Granite model integration.
    
    Environment Variables Required:
    - WATSONX_API_KEY: Your IBM Cloud API key
    - WATSONX_PROJECT_ID: Your watsonx.ai project ID
    - WATSONX_URL: watsonx.ai API endpoint (optional, defaults to us-south)
    
    If credentials are missing, automatically falls back to local analysis.
    """
    
    def __init__(self):
        """Initialize watsonx client with environment variables."""
        self.api_key = os.getenv('WATSONX_API_KEY')
        self.project_id = os.getenv('WATSONX_PROJECT_ID')
        self.url = os.getenv('WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')
        
        # Model configuration - using Granite Code Instruct model for code analysis
        self.model_id = "ibm/granite-8b-code-instruct"
        
        # Check if credentials are available
        self.is_available = bool(self.api_key and self.project_id)
        
        # Initialize client only if credentials are present
        self.client = None
        if self.is_available:
            try:
                self._initialize_client()
            except Exception as e:
                print(f"Warning: Failed to initialize watsonx client: {e}")
                self.is_available = False
    
    def _initialize_client(self):
        """
        Initialize the IBM watsonx.ai client using ModelInference.
        """
        try:
            from ibm_watsonx_ai import APIClient
            from ibm_watsonx_ai import Credentials
            from ibm_watsonx_ai.foundation_models import ModelInference
            from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
            from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
            
            # Create credentials
            credentials = Credentials(
                url=self.url,
                api_key=self.api_key
            )
            
            # Initialize API client
            api_client = APIClient(credentials)
            api_client.set.default_project(self.project_id)
            
            # Initialize ModelInference with Granite model
            self.client = ModelInference(
                model_id=self.model_id,
                api_client=api_client,
                params={
                    GenParams.DECODING_METHOD: "greedy",
                    GenParams.MAX_NEW_TOKENS: 2048,
                    GenParams.MIN_NEW_TOKENS: 1,
                    GenParams.TEMPERATURE: 0.7,
                    GenParams.TOP_K: 50,
                    GenParams.TOP_P: 1,
                    GenParams.REPETITION_PENALTY: 1.0
                }
            )
            
            print(f"Watsonx.ai Granite model initialized successfully: {self.model_id}")
            
        except ImportError as e:
            print(f"Warning: ibm-watsonx-ai package not installed: {e}")
            self.is_available = False
            self.client = None
        except Exception as e:
            print(f"Warning: Failed to initialize watsonx client: {e}")
            self.is_available = False
            self.client = None
    
    def is_configured(self) -> bool:
        """
        Check if watsonx client is properly configured.
        
        Returns:
            bool: True if credentials are available and client is ready
        """
        return self.is_available and self.client is not None
    
    def analyze_code(self, code: str, language: str, analysis_type: str) -> Optional[Dict[str, Any]]:
        """
        Analyze code using IBM watsonx.ai Granite model.
        
        Args:
            code: Source code to analyze
            language: Programming language (python, javascript, etc.)
            analysis_type: Type of analysis (explanation, security, documentation, etc.)
        
        Returns:
            Dict with analysis results, or None if watsonx is not available
        """
        if not self.is_configured():
            return None
        
        try:
            # Build prompt based on analysis type
            prompt = self._build_prompt(code, language, analysis_type)
            
            # Generate response using Granite model
            response = self.client.generate_text(prompt=prompt)
            
            return {
                'success': True,
                'analysis': response,
                'model': self.model_id,
                'source': 'watsonx.ai',
                'analysis_type': analysis_type
            }
            
        except Exception as e:
            print(f"Warning: watsonx analysis failed: {e}")
            return None
    
    def _build_prompt(self, code: str, language: str, analysis_type: str) -> str:
        """
        Build appropriate prompt for Granite model based on analysis type.
        
        Args:
            code: Source code to analyze
            language: Programming language
            analysis_type: Type of analysis requested
        
        Returns:
            Formatted prompt string for the model
        """
        prompts = {
            'explanation': f"""You are an expert code analyst. Analyze the following {language} code and provide a comprehensive explanation.

Code:
```{language}
{code}
```

Please provide:
1. **High-level Overview**: What does this code do?
2. **Detailed Explanation**: Explain key components, functions, and logic
3. **Complexity Assessment**: Evaluate the code complexity
4. **Code Structure**: Analyze functions, classes, and organization
5. **Best Practices**: Comment on code quality and adherence to best practices

Provide a clear, structured analysis that helps developers understand this code.""",
            
            'security': f"""You are a security expert. Perform a comprehensive security analysis of the following {language} code.

Code:
```{language}
{code}
```

Identify:
1. **Security Vulnerabilities**: Check for OWASP Top 10 issues (SQL injection, XSS, etc.)
2. **Hardcoded Secrets**: Look for API keys, passwords, or credentials
3. **Insecure Functions**: Identify dangerous functions (eval, exec, etc.)
4. **Weak Cryptography**: Check for MD5, SHA1, or weak encryption
5. **Authentication Issues**: Analyze authentication and authorization
6. **Recommended Fixes**: Provide specific remediation steps for each issue

Provide severity levels (Critical, High, Medium, Low) for each finding.""",
            
            'documentation': f"""You are a technical writer. Generate comprehensive documentation for the following {language} code.

Code:
```{language}
{code}
```

Generate:
1. **README.md**: Complete project documentation with:
   - Overview and features
   - Installation instructions
   - Usage examples
   - API documentation
2. **Inline Comments**: Add helpful comments explaining the code
3. **Unit Test Template**: Create a test template with test cases

Make the documentation clear, professional, and helpful for developers.""",
            
            'modernization': f"""You are a code modernization expert. Analyze the following {language} code for modernization opportunities.

Code:
```{language}
{code}
```

Suggest:
1. **Modern Syntax**: Recommend modern language features (f-strings, type hints, etc.)
2. **Performance Improvements**: Identify optimization opportunities
3. **Design Patterns**: Suggest better design patterns
4. **Framework Updates**: Recommend modern libraries and frameworks
5. **Best Practices**: Highlight areas not following current best practices

Prioritize suggestions by impact and effort required.""",
            
            'improvement': f"""You are a software architect. Create a comprehensive improvement roadmap for the following {language} code.

Code:
```{language}
{code}
```

Provide:
1. **Prioritized Improvements**: List improvements by priority (High, Medium, Low)
2. **Effort vs Impact Analysis**: Estimate effort and impact for each improvement
3. **Phased Implementation Plan**: Organize into phases (Quick Wins, Core Improvements, Long-term)
4. **Technical Debt Assessment**: Identify and quantify technical debt
5. **Actionable Recommendations**: Provide specific, actionable steps

Create a strategic roadmap that balances quick wins with long-term improvements."""
        }
        
        return prompts.get(analysis_type, prompts['explanation'])
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of watsonx integration.
        
        Returns:
            Dict with configuration status and details
        """
        return {
            'configured': self.is_configured(),
            'api_key_set': bool(self.api_key),
            'project_id_set': bool(self.project_id),
            'url': self.url if self.is_available else None,
            'model_id': self.model_id if self.is_configured() else None,
            'mode': 'watsonx.ai Granite' if self.is_configured() else 'local rule-based'
        }


# Global instance for easy access
_watsonx_client = None


def get_watsonx_client() -> WatsonxClient:
    """
    Get or create the global watsonx client instance.
    
    Returns:
        WatsonxClient: Singleton instance of the client
    """
    global _watsonx_client
    if _watsonx_client is None:
        _watsonx_client = WatsonxClient()
    return _watsonx_client


def is_watsonx_available() -> bool:
    """
    Quick check if watsonx is available and configured.
    
    Returns:
        bool: True if watsonx can be used
    """
    client = get_watsonx_client()
    return client.is_configured()

# Made with Bob
