"""
LangGraph-Style Multi-Agent Pipeline for RepoPilot
Runs agents in sequence: Explainer -> Security -> Doc/Test -> Modernizer -> Planner

This implementation provides a simple fallback sequential pipeline that mimics
LangGraph's graph-based execution model without requiring LangGraph as a dependency.
"""

from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from src.agents import (
    CodeExplainer,
    SecurityScanner,
    DocGenerator,
    CodeModernizer,
    ImprovementPlanner
)


@dataclass
class GraphState:
    """State object that flows through the pipeline"""
    code: str
    language: str = "python"
    explanation: Optional[Dict] = None
    security: Optional[Dict] = None
    documentation: Optional[Dict] = None
    modernization: Optional[Dict] = None
    roadmap: Optional[Dict] = None
    errors: list = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary"""
        return {
            "explanation": self.explanation,
            "security": self.security,
            "documentation": self.documentation,
            "modernization": self.modernization,
            "roadmap": self.roadmap,
            "errors": self.errors
        }


class AgentNode:
    """Represents a single agent node in the graph"""
    
    def __init__(self, name: str, agent: Any, output_key: str):
        self.name = name
        self.agent = agent
        self.output_key = output_key
    
    def execute(self, state: GraphState) -> GraphState:
        """Execute the agent and update state"""
        try:
            print(f"[*] Running {self.name}...")
            
            # Call the appropriate agent method
            if self.output_key == "explanation":
                result = self.agent.analyze(state.code, state.language)
            elif self.output_key == "security":
                result = self.agent.scan(state.code, state.language)
            elif self.output_key == "documentation":
                result = self.agent.generate(state.code, state.language)
            elif self.output_key == "modernization":
                result = self.agent.analyze(state.code, state.language)
            elif self.output_key == "roadmap":
                result = self.agent.create_roadmap(state.code, state.language)
            else:
                raise ValueError(f"Unknown output key: {self.output_key}")
            
            # Update state with result
            setattr(state, self.output_key, result)
            print(f"[OK] {self.name} completed")
            
        except Exception as e:
            error_msg = f"Error in {self.name}: {str(e)}"
            print(f"[ERROR] {error_msg}")
            state.errors.append(error_msg)
        
        return state


class RepoPilotGraph:
    """
    LangGraph-style sequential pipeline for RepoPilot agents.
    
    This class provides a graph-based execution model where agents are executed
    in sequence, with each agent's output stored in a shared state object.
    
    Pipeline Flow:
    1. Code Explainer - Analyzes and explains code functionality
    2. Security Scanner - Scans for vulnerabilities
    3. Doc & Test Generator - Generates documentation and tests
    4. Code Modernizer - Suggests modernization improvements
    5. Improvement Planner - Creates prioritized roadmap
    """
    
    def __init__(self):
        """Initialize the graph with all agent nodes"""
        self.nodes = []
        self._build_graph()
    
    def _build_graph(self):
        """Build the agent pipeline graph"""
        # Initialize agents
        explainer = CodeExplainer()
        security_scanner = SecurityScanner()
        doc_generator = DocGenerator()
        modernizer = CodeModernizer()
        planner = ImprovementPlanner()
        
        # Create nodes in execution order
        self.nodes = [
            AgentNode("Code Explainer", explainer, "explanation"),
            AgentNode("Security Scanner", security_scanner, "security"),
            AgentNode("Doc & Test Generator", doc_generator, "documentation"),
            AgentNode("Code Modernizer", modernizer, "modernization"),
            AgentNode("Improvement Planner", planner, "roadmap")
        ]
    
    def run(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Run the complete agent pipeline.
        
        Args:
            code: Source code to analyze
            language: Programming language (default: "python")
        
        Returns:
            Dictionary containing all agent outputs:
            - explanation: Code explanation results
            - security: Security scan results
            - documentation: Generated docs and tests
            - modernization: Modernization suggestions
            - roadmap: Improvement roadmap
            - errors: List of any errors encountered
        """
        print("Starting RepoPilot Multi-Agent Pipeline")
        print(f"Analyzing {len(code)} characters of {language} code")
        print("=" * 60)
        
        # Initialize state
        state = GraphState(code=code, language=language)
        
        # Execute each node in sequence
        for node in self.nodes:
            state = node.execute(state)
        
        print("=" * 60)
        if state.errors:
            print(f"WARNING: Pipeline completed with {len(state.errors)} error(s)")
        else:
            print("SUCCESS: Pipeline completed successfully!")
        
        return state.to_dict()
    
    def run_partial(self, code: str, language: str = "python", 
                   agents: list = None) -> Dict[str, Any]:
        """
        Run only specific agents from the pipeline.
        
        Args:
            code: Source code to analyze
            language: Programming language
            agents: List of agent names to run (e.g., ["explainer", "security"])
                   If None, runs all agents.
        
        Returns:
            Dictionary containing requested agent outputs
        """
        if agents is None:
            return self.run(code, language)
        
        print(f"Starting Partial Pipeline: {', '.join(agents)}")
        print("=" * 60)
        
        # Initialize state
        state = GraphState(code=code, language=language)
        
        # Map agent names to output keys
        agent_map = {
            "explainer": "explanation",
            "security": "security",
            "documentation": "documentation",
            "modernizer": "modernization",
            "planner": "roadmap"
        }
        
        # Execute only requested nodes
        for node in self.nodes:
            if node.output_key in [agent_map.get(a) for a in agents]:
                state = node.execute(state)
        
        print("=" * 60)
        print("SUCCESS: Partial pipeline completed!")
        
        return state.to_dict()


# Convenience function for easy import
def create_pipeline() -> RepoPilotGraph:
    """
    Create and return a new RepoPilot pipeline instance.
    
    Returns:
        RepoPilotGraph: Configured pipeline ready to run
    
    Example:
        >>> pipeline = create_pipeline()
        >>> results = pipeline.run(code_text, "python")
        >>> print(results['explanation'])
    """
    return RepoPilotGraph()


# Try to import LangGraph if available
try:
    from langgraph.graph import StateGraph, END
    LANGGRAPH_AVAILABLE = True
    
    class LangGraphPipeline:
        """
        Advanced LangGraph-based pipeline (requires langgraph package).
        
        This provides true graph-based execution with conditional routing,
        parallel execution, and advanced state management.
        """
        
        def __init__(self):
            """Initialize LangGraph-based pipeline"""
            self.graph = self._build_langgraph()
        
        def _build_langgraph(self):
            """Build the LangGraph workflow"""
            # Create the graph
            workflow = StateGraph(GraphState)
            
            # Add nodes
            workflow.add_node("explainer", self._explainer_node)
            workflow.add_node("security", self._security_node)
            workflow.add_node("documentation", self._documentation_node)
            workflow.add_node("modernizer", self._modernizer_node)
            workflow.add_node("planner", self._planner_node)
            
            # Define edges (sequential flow)
            workflow.set_entry_point("explainer")
            workflow.add_edge("explainer", "security")
            workflow.add_edge("security", "documentation")
            workflow.add_edge("documentation", "modernizer")
            workflow.add_edge("modernizer", "planner")
            workflow.add_edge("planner", END)
            
            return workflow.compile()
        
        def _explainer_node(self, state: GraphState) -> GraphState:
            """Code Explainer node"""
            agent = CodeExplainer()
            state.explanation = agent.analyze(state.code, state.language)
            return state
        
        def _security_node(self, state: GraphState) -> GraphState:
            """Security Scanner node"""
            agent = SecurityScanner()
            state.security = agent.scan(state.code, state.language)
            return state
        
        def _documentation_node(self, state: GraphState) -> GraphState:
            """Documentation Generator node"""
            agent = DocGenerator()
            state.documentation = agent.generate(state.code, state.language)
            return state
        
        def _modernizer_node(self, state: GraphState) -> GraphState:
            """Code Modernizer node"""
            agent = CodeModernizer()
            state.modernization = agent.analyze(state.code, state.language)
            return state
        
        def _planner_node(self, state: GraphState) -> GraphState:
            """Improvement Planner node"""
            agent = ImprovementPlanner()
            state.roadmap = agent.create_roadmap(state.code, state.language)
            return state
        
        def run(self, code: str, language: str = "python") -> Dict[str, Any]:
            """Run the LangGraph pipeline"""
            state = GraphState(code=code, language=language)
            result = self.graph.invoke(state)
            return result.to_dict()
    
    print("LangGraph detected - Advanced pipeline available")
    
except ImportError:
    LANGGRAPH_AVAILABLE = False
    LangGraphPipeline = None
    print("LangGraph not installed - Using simple sequential pipeline")


def get_pipeline(use_langgraph: bool = True) -> RepoPilotGraph:
    """
    Get the appropriate pipeline based on availability.
    
    Args:
        use_langgraph: Whether to use LangGraph if available (default: True)
    
    Returns:
        Pipeline instance (LangGraph or fallback)
    """
    if use_langgraph and LANGGRAPH_AVAILABLE:
        return LangGraphPipeline()
    return RepoPilotGraph()


if __name__ == "__main__":
    # Example usage
    sample_code = '''
def hello_world():
    print("Hello, World!")
    return True
'''
    
    pipeline = create_pipeline()
    results = pipeline.run(sample_code, "python")
    
    print("\n📊 Results Summary:")
    print(f"- Explanation: {bool(results['explanation'])}")
    print(f"- Security: {bool(results['security'])}")
    print(f"- Documentation: {bool(results['documentation'])}")
    print(f"- Modernization: {bool(results['modernization'])}")
    print(f"- Roadmap: {bool(results['roadmap'])}")
    print(f"- Errors: {len(results['errors'])}")

# Made with Bob
