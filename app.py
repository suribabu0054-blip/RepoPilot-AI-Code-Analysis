"""
RepoPilot - AI-Powered Code Analysis Tool
Main Streamlit Application
"""

import streamlit as st
from src.agents import (
    CodeExplainer,
    SecurityScanner,
    DocGenerator,
    CodeModernizer,
    ImprovementPlanner
)
from graph import create_pipeline


# Page configuration
st.set_page_config(
    page_title="RepoPilot - AI Code Analysis",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #0f62fe;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-size: 1.1rem;
    }
    .stButton>button {
        background-color: #0f62fe;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)


def initialize_agents():
    """Initialize all analysis agents and pipeline"""
    if 'agents_initialized' not in st.session_state:
        # Initialize individual agents (for backward compatibility)
        st.session_state.explainer = CodeExplainer()
        st.session_state.security_scanner = SecurityScanner()
        st.session_state.doc_generator = DocGenerator()
        st.session_state.modernizer = CodeModernizer()
        st.session_state.planner = ImprovementPlanner()
        
        # Initialize the multi-agent pipeline
        st.session_state.pipeline = create_pipeline()
        st.session_state.agents_initialized = True


def render_header():
    """Render application header"""
    st.markdown('<div class="main-header">🚀 RepoPilot – AI Development Co-Pilot powered by IBM Bob + Granite</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">AI-Powered Code Analysis & Improvement Tool</div>',
        unsafe_allow_html=True
    )
    
    # IBM Badge
    st.info("🔵 Powered by IBM watsonx.ai + IBM Bob IDE")
    
    # Project overview
    with st.expander("📖 About RepoPilot", expanded=False):
        st.markdown("""
        **RepoPilot** is an intelligent code analysis platform that helps developers understand,
        secure, and modernize their codebase using AI-powered agents.
        
        **Built using:**
        - 🤖 **IBM Bob IDE** (core development assistant)
        - 🧠 **IBM watsonx.ai Granite model** (optional AI analysis)
        - 🔄 **LangGraph multi-agent pipeline**
        - 🎨 **Streamlit UI**
        
        **Key Benefits:**
        - 🎯 **Instant Code Understanding**: Get detailed explanations of complex code
        - 🛡️ **Security First**: Identify vulnerabilities before they become problems
        - 📚 **Auto Documentation**: Generate README files and unit tests automatically
        - 🚀 **Stay Modern**: Get suggestions to upgrade to latest best practices
        - 📈 **Strategic Planning**: Receive prioritized improvement roadmaps
        
        Perfect for code reviews, onboarding, security audits, and technical debt management!
        """)


def render_sidebar():
    """Render sidebar with information"""
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=RepoPilot", use_container_width=True)
        
        st.markdown("### 🚀 5 Core Capabilities")
        
        with st.expander("🔍 Code Explainer", expanded=False):
            st.markdown("""
            **Understand complex code instantly**
            - Line-by-line explanations
            - Complexity analysis
            - Code structure metrics
            - Function & class breakdown
            """)
        
        with st.expander("🔒 Security Scanner", expanded=False):
            st.markdown("""
            **Detect vulnerabilities early**
            - SQL injection detection
            - XSS vulnerability checks
            - Hardcoded secrets finder
            - Insecure crypto detection
            - Severity-based prioritization
            """)
        
        with st.expander("📝 Documentation Generator", expanded=False):
            st.markdown("""
            **Auto-generate documentation**
            - Professional README files
            - Unit test templates
            - Inline code comments
            - API documentation
            """)
        
        with st.expander("✨ Code Modernizer", expanded=False):
            st.markdown("""
            **Upgrade to best practices**
            - Modern syntax suggestions
            - Performance improvements
            - Design pattern recommendations
            - Framework updates
            """)
        
        with st.expander("📊 Improvement Planner", expanded=False):
            st.markdown("""
            **Strategic roadmap creation**
            - Prioritized action items
            - Effort vs impact analysis
            - Phased implementation plan
            - Technical debt tracking
            """)
        
        st.markdown("---")
        st.markdown("### 🎯 Quick Start")
        st.markdown("""
        1. **Load Example** or paste your code
        2. Select programming language
        3. Click **Analyze Code** button
        4. Review results in tabs
        5. **Download Full Report**
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Pro Tips")
        st.markdown("""
        - Start with the example code
        - Check all 5 analysis tabs
        - Download the full report
        - Use for code reviews
        - Perfect for onboarding
        """)


def render_code_input():
    """Render code input section"""
    st.markdown("### 📝 Enter Your Code")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Language selector
        language = st.selectbox(
            "Programming Language",
            ["Python", "JavaScript", "Java", "TypeScript", "Go"],
            index=0
        )
    
    with col2:
        # Example code button - more prominent
        st.markdown("<br>", unsafe_allow_html=True)  # Align with selectbox
        if st.button("📋 Load Example Code", type="secondary", use_container_width=True):
            st.session_state.example_loaded = True
    
    # Code input
    code_input = st.text_area(
        "Paste your code here:",
        height=300,
        placeholder="# Paste your code here...\ndef hello_world():\n    print('Hello, World!')",
        help="Paste the code you want to analyze"
    )
    
    return code_input, language.lower()


def get_example_code():
    """Get example code for demonstration"""
    return '''import os
import hashlib

# User authentication function
def authenticate_user(username, password):
    # Hardcoded credentials (BAD PRACTICE!)
    admin_password = "admin123"
    
    if username == "admin" and password == admin_password:
        return True
    
    # Using MD5 for password hashing (WEAK!)
    hashed = hashlib.md5(password.encode()).hexdigest()
    
    # SQL query with string formatting (SQL INJECTION RISK!)
    query = "SELECT * FROM users WHERE username='%s' AND password='%s'" % (username, hashed)
    
    # Execute query (dangerous!)
    result = os.system(query)
    
    return result

def process_data(items):
    result = []
    for item in items:
        result.append(item * 2)
    return result
'''


def generate_full_report(results, code, language):
    """Generate a comprehensive Markdown report"""
    report = f"""# RepoPilot Analysis Report

## 📋 Code Overview
**Language:** {language.title()}
**Analysis Date:** {st.session_state.get('analysis_date', 'N/A')}

---

## 🔍 Code Explanation

{results['explanation']['overview']}

{results['explanation']['details']}

### Complexity Analysis
{results['explanation']['complexity']}

### Code Metrics
- **Lines of Code:** {results['explanation']['structure']['lines']}
- **Functions:** {results['explanation']['structure']['functions']}
- **Classes:** {results['explanation']['structure']['classes']}
- **Imports:** {results['explanation']['structure']['imports']}

---

## 🔒 Security Analysis

{results['security']['summary']}

### Detected Vulnerabilities
"""
    
    if results['security']['vulnerabilities']:
        for i, vuln in enumerate(results['security']['vulnerabilities'], 1):
            report += f"""
#### {i}. {vuln['type']} - {vuln['severity']}
- **Description:** {vuln['description']}
- **Location:** {vuln['line']}
- **Fix:** {vuln['fix']}
"""
    else:
        report += "\n✅ No vulnerabilities detected!\n"
    
    report += f"""
### Security Recommendations
{results['security']['recommendations']}

---

## 📝 Documentation

### Generated README
```markdown
{results['documentation']['readme']}
```

---

## ✨ Modernization Suggestions

{results['modernization']['summary']}
"""
    
    if results['modernization']['suggestions']:
        report += "\n### Recommendations\n"
        for i, suggestion in enumerate(results['modernization']['suggestions'], 1):
            report += f"""
#### {i}. {suggestion['category']} - {suggestion['priority']} Priority
- **Current:** {suggestion['current']}
- **Modern:** {suggestion['modern']}
- **Effort:** {suggestion['effort']}
"""
    
    report += f"""
---

## 📊 Improvement Roadmap

{results['roadmap']['summary']}

### Phased Implementation Plan
"""
    
    for phase_name, improvements in results['roadmap']['roadmap'].items():
        if improvements:
            report += f"\n#### {phase_name}\n"
            for imp in improvements:
                report += f"- **{imp['area']}**: {imp['issue']} (Priority: {imp['priority']}, Effort: {imp['effort']})\n"
                report += f"  - {imp['suggestion']}\n"
    
    report += """
---

## 📌 Original Code

```{language}
{code}
```

---

*Generated by RepoPilot - AI-Powered Code Analysis Tool*
""".format(language=language, code=code)
    
    return report


def analyze_code(code, language):
    """Run all analysis agents on the code using the multi-agent pipeline"""
    with st.spinner("🔄 Analyzing your code with multi-agent pipeline..."):
        try:
            from datetime import datetime
            st.session_state.analysis_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Use the multi-agent pipeline for sequential execution
            results = st.session_state.pipeline.run(code, language)
            
            # Check for errors in pipeline execution
            if results.get('errors'):
                st.warning(f"⚠️ Pipeline completed with {len(results['errors'])} warning(s)")
                for error in results['errors']:
                    st.warning(f"  • {error}")
            
            st.session_state.analysis_results = results
            st.session_state.analyzed_code = code
            st.session_state.analyzed_language = language
            return True
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
            return False


def render_explanation_tab():
    """Render code explanation tab"""
    if 'analysis_results' not in st.session_state:
        st.info("👆 Analyze code to see results")
        return
    
    results = st.session_state.analysis_results['explanation']
    
    # Overview
    st.markdown(results['overview'])
    
    # Details
    st.markdown("---")
    st.markdown(results['details'])
    
    # Complexity
    st.markdown("---")
    st.markdown(results['complexity'])
    
    # Role-based explanations
    if 'role_explanations' in results:
        st.markdown("---")
        st.markdown("## 🎭 Role-Based Explanations")
        
        role_tabs = st.tabs(["👨‍💻 Developer", "👔 Manager", "🧪 QA Engineer"])
        
        with role_tabs[0]:
            st.markdown(results['role_explanations']['developer'])
        
        with role_tabs[1]:
            st.markdown(results['role_explanations']['manager'])
        
        with role_tabs[2]:
            st.markdown(results['role_explanations']['qa'])
    
    # Structure metrics
    st.markdown("---")
    st.markdown("### 📊 Code Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Lines of Code", results['structure']['lines'])
    with col2:
        st.metric("Functions", results['structure']['functions'])
    with col3:
        st.metric("Classes", results['structure']['classes'])
    with col4:
        st.metric("Imports", results['structure']['imports'])


def render_security_tab():
    """Render security scan tab"""
    if 'analysis_results' not in st.session_state:
        st.info("👆 Analyze code to see results")
        return
    
    results = st.session_state.analysis_results['security']
    
    # Summary
    st.markdown(results['summary'])
    
    # Vulnerabilities
    if results['vulnerabilities']:
        st.markdown("---")
        st.markdown("### 🔍 Detected Vulnerabilities")
        
        for i, vuln in enumerate(results['vulnerabilities'], 1):
            severity_color = {
                'Critical': '🔴',
                'High': '🟠',
                'Medium': '🟡',
                'Low': '🟢'
            }
            
            with st.expander(f"{severity_color.get(vuln['severity'], '⚪')} {vuln['type']} - {vuln['severity']}"):
                st.markdown(f"**Description:** {vuln['description']}")
                st.markdown(f"**Location:** {vuln['line']}")
                st.markdown(f"**Fix:** {vuln['fix']}")
    
    # Recommendations
    st.markdown("---")
    st.markdown(results['recommendations'])
    
    # Severity chart
    if results['vulnerabilities']:
        st.markdown("---")
        st.markdown("### 📊 Severity Distribution")
        severity_data = results['severity_count']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🔴 Critical", severity_data['critical'])
        with col2:
            st.metric("🟠 High", severity_data['high'])
        with col3:
            st.metric("🟡 Medium", severity_data['medium'])
        with col4:
            st.metric("🟢 Low", severity_data['low'])


def render_documentation_tab():
    """Render documentation & tests tab"""
    if 'analysis_results' not in st.session_state:
        st.info("👆 Analyze code to see results")
        return
    
    results = st.session_state.analysis_results['documentation']
    
    # README
    st.markdown("### 📄 Generated README.md")
    st.code(results['readme'], language='markdown')
    
    if st.button("📥 Download README"):
        st.download_button(
            label="Download README.md",
            data=results['readme'],
            file_name="README.md",
            mime="text/markdown"
        )
    
    # Tests
    st.markdown("---")
    st.markdown("### 🧪 Generated Unit Tests")
    st.code(results['tests'], language='python')
    
    if st.button("📥 Download Tests"):
        st.download_button(
            label="Download test_code.py",
            data=results['tests'],
            file_name="test_code.py",
            mime="text/x-python"
        )
    
    # Comments
    st.markdown("---")
    st.markdown("### 💬 Code with Comments")
    st.code(results['comments'], language='python')


def render_modernization_tab():
    """Render code modernization tab"""
    if 'analysis_results' not in st.session_state:
        st.info("👆 Analyze code to see results")
        return
    
    results = st.session_state.analysis_results['modernization']
    
    # Summary
    st.markdown(results['summary'])
    
    # Suggestions
    if results['suggestions']:
        st.markdown("---")
        st.markdown("### 💡 Modernization Suggestions")
        
        for i, suggestion in enumerate(results['suggestions'], 1):
            priority_color = {
                'High': '🔴',
                'Medium': '🟡',
                'Low': '🟢'
            }
            
            with st.expander(f"{priority_color.get(suggestion['priority'], '⚪')} {suggestion['category']} - {suggestion['priority']} Priority"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Current:** {suggestion['current']}")
                    st.markdown(f"**Effort:** {suggestion['effort']}")
                
                with col2:
                    st.markdown(f"**Modern:** {suggestion['modern']}")
                    st.markdown(f"**Example:**")
                    st.code(suggestion['example'], language='python')
    else:
        st.success("✨ Your code is already modern!")


def render_roadmap_tab():
    """Render improvement roadmap tab"""
    if 'analysis_results' not in st.session_state:
        st.info("👆 Analyze code to see results")
        return
    
    results = st.session_state.analysis_results['roadmap']
    
    # Summary
    st.markdown(results['summary'])
    
    # Roadmap phases
    if results['improvements']:
        st.markdown("---")
        st.markdown("### 🗺️ Phased Roadmap")
        
        for phase_name, improvements in results['roadmap'].items():
            if improvements:
                st.markdown(f"#### {phase_name}")
                
                for imp in improvements:
                    with st.expander(f"{imp['area']}: {imp['issue']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Priority:** {imp['priority']}")
                            st.markdown(f"**Effort:** {imp['effort']}")
                        
                        with col2:
                            st.markdown(f"**Impact:** {imp['impact']}")
                            st.markdown(f"**Score:** {imp.get('score', 'N/A')}")
                        
                        st.markdown(f"**Suggestion:** {imp['suggestion']}")
                
                st.markdown("---")


def main():
    """Main application function"""
    # Initialize
    initialize_agents()
    
    # Render UI
    render_header()
    render_sidebar()
    
    # Code input section
    code_input, language = render_code_input()
    
    # Load example if requested
    if st.session_state.get('example_loaded', False):
        code_input = get_example_code()
        st.session_state.example_loaded = False
        st.rerun()
    
    # Analyze button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        analyze_button = st.button("🔍 Analyze Code", type="primary", use_container_width=True)
    
    if analyze_button and code_input.strip():
        if analyze_code(code_input, language):
            st.success("✅ Analysis complete! Scroll down to view results.")
            st.balloons()
    elif analyze_button:
        st.warning("⚠️ Please enter some code to analyze")
    
    # Results tabs
    if 'analysis_results' in st.session_state:
        st.markdown("---")
        
        # Download full report button
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            full_report = generate_full_report(
                st.session_state.analysis_results,
                st.session_state.analyzed_code,
                st.session_state.analyzed_language
            )
            st.download_button(
                label="📥 Download Full Report",
                data=full_report,
                file_name=f"repopilot_analysis_{st.session_state.analysis_date.replace(':', '-').replace(' ', '_')}.md",
                mime="text/markdown",
                type="primary",
                use_container_width=True
            )
        
        st.markdown("## 📊 Analysis Results")
        
        tabs = st.tabs([
            "🔍 Code Explainer",
            "🔒 Security Scanner",
            "📝 Documentation & Tests",
            "✨ Code Modernizer",
            "📊 Improvement Planner"
        ])
        
        with tabs[0]:
            render_explanation_tab()
        
        with tabs[1]:
            render_security_tab()
        
        with tabs[2]:
            render_documentation_tab()
        
        with tabs[3]:
            render_modernization_tab()
        
        with tabs[4]:
            render_roadmap_tab()


if __name__ == "__main__":
    main()
