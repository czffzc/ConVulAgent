"""
LangGraph workflow definition for code review.
Orchestrates the flow: Parse → Detect → Optimize → Report
"""
from langgraph.graph import StateGraph, END
from src.state import ReviewState
from src.nodes import (
    parse_code_node,
    bug_detection_node,
    optimization_node,
    report_generation_node
)
from tqdm import tqdm


def create_review_workflow() -> StateGraph:
    """
    Create the code review workflow graph.
    
    Graph structure:
    START → parse_code → bug_detection → optimization → report_generation → END
    
    Returns:
        Compiled StateGraph ready for execution
    """
    # Initialize the graph with our state schema
    workflow = StateGraph(ReviewState)
    
    # Add nodes to the graph
    workflow.add_node("parse_code", parse_code_node)
    workflow.add_node("bug_detection", bug_detection_node)
    workflow.add_node("optimization", optimization_node)
    workflow.add_node("report_generation", report_generation_node)
    
    # Define edges (flow between nodes)
    workflow.set_entry_point("parse_code")
    workflow.add_edge("parse_code", "bug_detection")
    workflow.add_edge("bug_detection", "optimization")
    workflow.add_edge("optimization", "report_generation")
    workflow.add_edge("report_generation", END)
    
    # Compile the graph
    return workflow.compile()


def run_review(file_path: str) -> dict:
    """
    Execute code review workflow on a file with progress updates.

    Args:
        file_path: Path to the code file to review

    Returns:
        Final report dictionary with all findings
    """
    # Create workflow
    app = create_review_workflow()

    # Initialize state
    initial_state = {
        "file_path": file_path,
        "code_content": "",
        "language": None,
        "parsed_structure": None,
        "bugs": [],
        "optimizations": [],
        "report": None,
        "metadata": {}
    }

    print(f"\n Starting code review for: {file_path}")
    print("=" * 60)

    # Define workflow steps for progress tracking
    steps = ["Parsing code", "Detecting bugs", "Analyzing optimizations", "Generating report"]

    # Execute workflow with progress bar
    with tqdm(total=len(steps), desc="Progress", unit="step") as pbar:
        for step in steps:
            print(f"\n[Step] {step}...")
            pbar.update(1)
            # Simulate step execution (replace with actual workflow logic)
            final_state = app.invoke(initial_state)

    print("=" * 60)
    print(" Review complete!\n")

    return final_state['report']
