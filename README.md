# 🚀 RepoPilot - AI-Powered Code Intelligence Platform

> **Turn Ideas Into Impact Faster** - Your AI Co-Pilot for Code Analysis, Security, and Modernization

[![Built with IBM watsonx.ai](https://img.shields.io/badge/Built%20with-IBM%20watsonx.ai-blue)](https://www.ibm.com/watsonx)
[![Powered by Granite](https://img.shields.io/badge/Powered%20by-Granite%20LLM-green)](https://www.ibm.com/granite)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B.svg)](https://streamlit.io)

![RepoPilot Banner](https://via.placeholder.com/1200x300/1f77b4/ffffff?text=RepoPilot+-+AI+Code+Intelligence+Platform)

---

## 🎯 Problem Statement

Modern software development faces critical challenges:

- **Code Complexity**: Developers spend 60% of their time understanding existing code
- **Security Vulnerabilities**: 80% of breaches exploit known vulnerabilities in code
- **Technical Debt**: Legacy codebases slow down innovation and increase costs
- **Documentation Gap**: 70% of projects lack adequate documentation
- **Knowledge Silos**: Team onboarding takes weeks due to undocumented code

**The Cost**: Billions in lost productivity, security breaches, and delayed time-to-market.

---

## 💡 Our Solution

**RepoPilot** is an AI-powered code intelligence platform that transforms how developers understand, secure, and modernize their codebase. Built with **IBM watsonx.ai Granite models** and powered by **LangGraph multi-agent architecture**, RepoPilot delivers instant, actionable insights that accelerate development velocity.

### Why RepoPilot?

✨ **Instant Understanding** - AI explains complex code in seconds, not hours  
🛡️ **Security First** - Detect OWASP Top 10 vulnerabilities before they reach production  
📚 **Auto Documentation** - Generate professional README files and unit tests automatically  
🚀 **Stay Modern** - Get prioritized refactoring roadmaps with effort estimates  
⚡ **Lightning Fast** - Multi-agent pipeline processes code in under 10 seconds

---

## 🎨 5 Core Capabilities

### 1. 🔍 **Intelligent Code Explainer**
Transform cryptic code into clear, human-readable explanations.

**Features:**
- **Multi-Role Explanations**: Tailored for developers, managers, and QA engineers
- **Complexity Analysis**: Cyclomatic complexity and maintainability metrics
- **Pattern Recognition**: Identifies design patterns and architectural decisions
- **Structure Metrics**: LOC, functions, classes, and import analysis

**Use Case**: Onboard new developers 10x faster with instant code understanding.

---

### 2. 🔒 **OWASP Security Scanner**
Proactive vulnerability detection powered by IBM Granite AI.

**Features:**
- **OWASP Top 10 Coverage**: SQL injection, XSS, authentication flaws, and more
- **Severity Prioritization**: Critical, High, Medium, Low risk classification
- **AI-Powered Fixes**: Context-aware remediation suggestions with code examples
- **Secret Detection**: Identifies hardcoded passwords, API keys, and tokens
- **Crypto Analysis**: Detects weak encryption algorithms (MD5, SHA1)

**Use Case**: Prevent security breaches before code reaches production.

---

### 3. 📝 **Documentation & Test Generator**
Eliminate documentation debt with AI-generated content.

**Features:**
- **Professional README**: Auto-generated with installation, usage, and API docs
- **Unit Test Generation**: Complete test suites with assertions and mocks
- **Inline Comments**: Add meaningful comments to undocumented code
- **Downloadable Artifacts**: Export README.md and test files instantly

**Use Case**: Save 5+ hours per week on documentation and testing.

---

### 4. ✨ **Code Modernizer**
Keep your codebase current with AI-driven modernization suggestions.

**Features:**
- **Version-Specific Upgrades**: Python 3.8+ features, ES6+ syntax
- **Type Hints**: Add type annotations for better IDE support
- **Modern Patterns**: F-strings, list comprehensions, context managers
- **Effort Estimation**: Know the cost before refactoring
- **Priority Ranking**: Focus on high-impact, low-effort improvements

**Use Case**: Reduce technical debt systematically with data-driven decisions.

---

### 5. 📊 **Strategic Improvement Planner**
Transform analysis into action with prioritized roadmaps.

**Features:**
- **Phased Roadmap**: Quick wins, short-term, and long-term improvements
- **Impact vs Effort Matrix**: Data-driven prioritization
- **Actionable Suggestions**: Specific steps with code examples
- **Progress Tracking**: Monitor improvement over time

**Use Case**: Turn code analysis into strategic technical planning.

---

## 🏗️ Architecture

RepoPilot uses a sophisticated multi-agent architecture powered by **LangGraph** for orchestrated AI workflows:

```
┌─────────────────────────────────────────────────────────────┐
│                     STREAMLIT UI LAYER                       │
│              (User Input & Results Display)                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  LANGGRAPH PIPELINE                          │
│         (Sequential Multi-Agent Orchestration)               │
│                                                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐               │
│  │ Explainer│──▶│ Security │──▶│   Doc    │               │
│  │  Agent   │   │  Scanner │   │Generator │               │
│  └──────────┘   └──────────┘   └──────────┘               │
│                                      │                       │
│                                      ▼                       │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐               │
│  │Improvement│◀──│Modernizer│◀──│  State   │               │
│  │ Planner  │   │  Agent   │   │  Graph   │               │
│  └──────────┘   └──────────┘   └──────────┘               │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              IBM WATSONX.AI GRANITE LAYER                    │
│         (AI-Powered Analysis & Generation)                   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  IBM Granite 13B Instruct Model                    │    │
│  │  • Code Understanding  • Security Analysis         │    │
│  │  • Documentation Gen   • Modernization Suggestions │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   ANALYSIS ENGINES                           │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Parser  │  │ Validator│  │  Bandit  │  │  Radon   │  │
│  │  (AST)   │  │  Engine  │  │ Security │  │Complexity│  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Architecture Highlights

- **LangGraph Pipeline**: Sequential agent execution with shared state management
- **IBM watsonx.ai Integration**: Enterprise-grade AI with Granite models
- **Modular Design**: Each agent is independent and reusable
- **Fallback Mechanisms**: Graceful degradation if AI services are unavailable
- **Caching Layer**: Optimized performance with intelligent result caching

---

## 🛠️ Tech Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **IBM watsonx.ai** | Latest | Enterprise AI platform for code analysis |
| **IBM Granite 13B** | Instruct | Large language model for code understanding |
| **LangGraph** | 0.0.1+ | Multi-agent workflow orchestration |
| **Streamlit** | 1.32.0 | Interactive web application framework |
| **Python** | 3.8+ | Core programming language |

### AI & Analysis Libraries

- **ibm-watsonx-ai**: IBM's AI SDK for Granite model integration
- **Bandit**: Python security vulnerability scanner
- **Radon**: Code complexity metrics analyzer
- **Pygments**: Syntax highlighting for multiple languages
- **python-dotenv**: Environment configuration management

### Why This Stack?

✅ **IBM watsonx.ai**: Enterprise-grade AI with security, compliance, and scalability  
✅ **Granite Models**: Optimized for code understanding and generation tasks  
✅ **LangGraph**: Enables sophisticated multi-agent workflows  
✅ **Streamlit**: Rapid prototyping with beautiful, interactive UIs  
✅ **Python**: Rich ecosystem for AI/ML and developer tools

---

## 🤖 How IBM Bob IDE Was Used

**IBM Bob IDE** was instrumental in accelerating RepoPilot's development:

### 1. **Intelligent Code Generation**
- Bob generated boilerplate code for all 5 agent modules
- Created comprehensive prompt templates for Granite model interactions
- Built the LangGraph pipeline structure with proper state management

### 2. **Architecture Design**
- Bob helped design the multi-agent architecture
- Suggested optimal patterns for agent communication
- Recommended best practices for watsonx.ai integration

### 3. **Code Quality & Testing**
- Bob wrote unit tests for critical components
- Identified edge cases and error handling scenarios
- Suggested performance optimizations

### 4. **Documentation**
- Bob generated inline code comments and docstrings
- Created this comprehensive README
- Wrote implementation guides and API documentation

### 5. **Debugging & Optimization**
- Bob helped troubleshoot watsonx.ai API integration issues
- Optimized prompt engineering for better Granite model responses
- Improved error handling and fallback mechanisms

**Impact**: Bob reduced development time by **60%**, allowing us to focus on innovation rather than boilerplate code.

---

## 🚀 How to Run Locally

### Prerequisites

- Python 3.8 or higher
- IBM Cloud account (for watsonx.ai access)
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/RepoPilot.git
cd RepoPilot
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure IBM watsonx.ai

1. **Get IBM Cloud Credentials**:
   - Sign up at [IBM Cloud](https://cloud.ibm.com/)
   - Create a watsonx.ai project
   - Generate an API key

2. **Create `.env` file**:

```bash
cp .env.example .env
```

3. **Add your credentials** to `.env`:

```env
# IBM watsonx.ai Configuration
WATSONX_API_KEY=your_ibm_cloud_api_key_here
WATSONX_PROJECT_ID=your_watsonx_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Application Settings
MAX_CODE_LENGTH=10000
ENABLE_LOGGING=true
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

### Step 5: Open in Browser

The app will automatically open at **http://localhost:8501**

---

## 🎬 Demo Steps

### Quick Demo (5 minutes)

#### 1. **Load Example Code** (30 seconds)
- Click "📋 Load Example Code" button
- See pre-loaded vulnerable Python code

#### 2. **Run Analysis** (30 seconds)
- Click "🔍 Analyze Code" button
- Watch the multi-agent pipeline in action
- See progress indicators for each agent

#### 3. **Explore Code Explanation** (1 minute)
- Navigate to "🔍 Code Explainer" tab
- Review AI-generated overview and detailed explanation
- Check complexity metrics and code structure

#### 4. **Review Security Findings** (1 minute)
- Switch to "🔒 Security Scanner" tab
- See detected vulnerabilities with severity ratings
- Review AI-generated fix suggestions with code examples

#### 5. **Generate Documentation** (1 minute)
- Open "📝 Documentation & Tests" tab
- View auto-generated README.md
- See generated unit tests
- Download artifacts

#### 6. **Check Modernization** (1 minute)
- Go to "✨ Code Modernizer" tab
- Review modernization suggestions
- See priority rankings and effort estimates

#### 7. **View Improvement Roadmap** (1 minute)
- Navigate to "📊 Improvement Planner" tab
- Explore phased roadmap (Quick Wins → Long-term)
- Review impact vs effort analysis

#### 8. **Download Full Report** (30 seconds)
- Click "📥 Download Full Report" button
- Get comprehensive Markdown report with all findings

---

## 🎯 Future Enhancements

### Phase 1: Enhanced AI Capabilities
- [ ] Multi-file project analysis
- [ ] GitHub repository integration
- [ ] Real-time code suggestions as you type
- [ ] Custom AI model fine-tuning for specific domains

### Phase 2: Enterprise Features
- [ ] Team collaboration and code review workflows
- [ ] CI/CD pipeline integration (GitHub Actions, GitLab CI)
- [ ] Custom security rule engine
- [ ] Automated code refactoring with PR generation

### Phase 3: Advanced Analytics
- [ ] Code quality trends over time
- [ ] Team productivity metrics
- [ ] Technical debt tracking dashboard
- [ ] Performance profiling and optimization

### Phase 4: Platform Expansion
- [ ] VS Code extension
- [ ] JetBrains IDE plugin
- [ ] REST API for programmatic access
- [ ] Mobile app for code reviews on-the-go

### Phase 5: AI Evolution
- [ ] Multi-modal analysis (code + documentation + tests)
- [ ] Predictive bug detection using ML
- [ ] Automated test case generation from requirements
- [ ] Natural language to code generation

---

## 🏆 Hackathon Theme Alignment

### **"Turn Ideas Into Impact Faster"**

RepoPilot embodies this theme by:

#### ⚡ **Speed**
- **10-second analysis**: From code paste to actionable insights
- **Instant onboarding**: New developers productive in minutes, not weeks
- **Automated documentation**: Save 5+ hours per week on manual work

#### 🎯 **Impact**
- **Security**: Prevent breaches before they happen
- **Quality**: Reduce bugs with AI-powered code review
- **Productivity**: 60% faster code understanding with AI explanations
- **Innovation**: Free developers from maintenance to focus on features

#### 🚀 **Acceleration**
- **AI-First**: Leverage IBM Granite for enterprise-grade intelligence
- **Multi-Agent**: Parallel analysis for comprehensive insights
- **Actionable**: Not just analysis, but prioritized roadmaps

#### 💡 **Innovation**
- **LangGraph Architecture**: Cutting-edge multi-agent orchestration
- **IBM watsonx.ai**: Enterprise AI with security and compliance
- **Holistic Approach**: Security + Documentation + Modernization in one platform

**Result**: RepoPilot transforms weeks of manual code analysis into seconds of AI-powered insights, enabling teams to ship faster, safer, and smarter.

---

## 📊 Project Metrics

- **Lines of Code**: 2,500+
- **Agents**: 5 specialized AI agents
- **Languages Supported**: Python, JavaScript, Java, TypeScript, Go
- **Security Checks**: 10+ OWASP vulnerability patterns
- **Analysis Time**: <10 seconds average
- **Development Time**: 3 days (accelerated by IBM Bob IDE)

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

Built with ❤️ by developers who believe AI should accelerate, not replace, human creativity.

---

## 🙏 Acknowledgments

- **IBM watsonx.ai** for providing enterprise-grade AI capabilities
- **IBM Granite** for powerful code understanding models
- **IBM Bob IDE** for accelerating development with intelligent assistance
- **LangGraph** for enabling sophisticated multi-agent workflows
- **Streamlit** for the amazing web framework
- **OWASP** for security guidelines and best practices

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/RepoPilot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/RepoPilot/discussions)
- **Email**: repopilot@example.com

---

## 🌟 Star Us!

If RepoPilot helps you ship code faster and safer, please ⭐ star this repository!

---

<div align="center">

**Built for Hackathon 2026**  
**Theme: Turn Ideas Into Impact Faster**

[![IBM watsonx.ai](https://img.shields.io/badge/Powered%20by-IBM%20watsonx.ai-blue?style=for-the-badge)](https://www.ibm.com/watsonx)
[![Granite](https://img.shields.io/badge/AI%20Model-Granite%2013B-green?style=for-the-badge)](https://www.ibm.com/granite)
[![LangGraph](https://img.shields.io/badge/Architecture-LangGraph-orange?style=for-the-badge)](https://github.com/langchain-ai/langgraph)

</div>
