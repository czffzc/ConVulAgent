"""
State definition for the code review workflow.
"""
from typing import TypedDict, List, Dict, Optional


class ReviewState(TypedDict):
    """
    State object that flows through the LangGraph nodes.
    
    Attributes:
        file_path: Path to the code file being reviewed
        code_content: Raw content of the code file
        language: Programming language detected
        parsed_structure: AST or structure information
        bugs: List of detected bugs
        optimizations: List of optimization suggestions
        report: Final formatted report
        metadata: Additional metadata (timestamps, model info, etc.)
    """
    file_path: str
    code_content: str
    language: Optional[str]
    parsed_structure: Optional[Dict]
    bugs: List[Dict]
    optimizations: List[Dict]
    report: Optional[Dict]
    metadata: Dict


class BugIssue(TypedDict):
    """Individual bug issue structure"""
    type: str  # "bug", "vulnerability", "error"
    line: int
    severity: str  # "critical", "high", "medium", "low"
    description: str
    suggestion: str
    confidence: float


class OptimizationSuggestion(TypedDict):
    """Individual optimization suggestion structure"""
    type: str  # "performance", "security", "best_practice", "code_smell"
    line: Optional[int]
    category: str
    description: str
    suggestion: str
    impact: str  # "high", "medium", "low"
