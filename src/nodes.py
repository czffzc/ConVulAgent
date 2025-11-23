"""
LangGraph nodes for code review workflow.
Each node processes the state and passes it to the next node.
"""
import os
from datetime import datetime
from typing import Dict
from src.state import ReviewState
from src.deepseek_agent import DeepSeekAgent
from src.prompts import BUG_DETECTION_PROMPT, OPTIMIZATION_PROMPT


def add_line_numbers(code: str) -> str:
    """Add line numbers to code for accurate reporting."""
    lines = code.split('\n')
    numbered_lines = [f"{i+1:4d} | {line}" for i, line in enumerate(lines)]
    return '\n'.join(numbered_lines)


def parse_code_node(state: ReviewState) -> ReviewState:
    """
    Node 1: Parse and prepare code for analysis.
    
    - Reads the code file
    - Detects programming language
    - Validates file size
    - Prepares metadata
    """
    print(" Parsing code...")
    
    file_path = state['file_path']
    
    # Read code content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
    except Exception as e:
        print(f" Error reading file: {e}")
        state['code_content'] = ""
        state['metadata'] = {"error": str(e)}
        return state
    
    # Detect language from file extension
    ext_to_lang = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.go': 'go',
        '.rb': 'ruby',
        '.php': 'php',
    }
    
    ext = os.path.splitext(file_path)[1]
    language = ext_to_lang.get(ext, 'unknown')
    
    # Update state
    state['code_content'] = code_content
    state['language'] = language
    state['metadata'] = {
        'file_name': os.path.basename(file_path),
        'file_size': len(code_content),
        'lines_of_code': len(code_content.split('\n')),
        'timestamp': datetime.now().isoformat(),
        'language': language
    }
    
    print(f" Parsed {language} file: {state['metadata']['lines_of_code']} lines")
    return state


def bug_detection_node(state: ReviewState) -> ReviewState:
    """
    Node 2: Detect bugs using DeepSeek-R1.
    
    - Sends code to LLM with bug detection prompt
    - Parses bug findings
    - Filters by confidence threshold
    """
    print(" Detecting bugs...")
    
    code = state['code_content']
    language = state['language']
    
    if not code or language == 'unknown':
        print("  Skipping bug detection - invalid code or language")
        state['bugs'] = []
        return state
    
    # Add line numbers to code for accurate reporting
    numbered_code = add_line_numbers(code)
    
    # Initialize agent and detect bugs
    agent = DeepSeekAgent()
    result = agent.detect_bugs(numbered_code, language, BUG_DETECTION_PROMPT)
    
    # Extract bugs from result
    bugs = result.get('bugs', [])
    
    # Filter by confidence (>= 0.7)
    filtered_bugs = [b for b in bugs if b.get('confidence', 0) >= 0.7]
    
    state['bugs'] = filtered_bugs
    print(f" Found {len(filtered_bugs)} bugs (confidence >= 0.7)")
    
    return state


def optimization_node(state: ReviewState) -> ReviewState:
    """
    Node 3: Suggest optimizations using DeepSeek-R1.
    
    - Sends code to LLM with optimization prompt
    - Parses optimization suggestions
    - Categories: performance, security, best practices
    """
    print(" Analyzing optimizations...")
    
    code = state['code_content']
    language = state['language']
    
    if not code or language == 'unknown':
        print("  Skipping optimization - invalid code or language")
        state['optimizations'] = []
        return state
    
    # Add line numbers to code for accurate reporting
    numbered_code = add_line_numbers(code)
    
    # Initialize agent and get optimizations
    agent = DeepSeekAgent()
    result = agent.suggest_optimizations(numbered_code, language, OPTIMIZATION_PROMPT)
    
    # Extract optimizations
    optimizations = result.get('optimizations', [])
    
    state['optimizations'] = optimizations
    print(f" Found {len(optimizations)} optimization opportunities")
    
    return state


def report_generation_node(state: ReviewState) -> ReviewState:
    """
    Node 4: Generate final report.
    
    - Compiles all findings
    - Calculates severity metrics
    - Formats output as JSON
    """
    print(" Generating report...")
    
    bugs = state['bugs']
    optimizations = state['optimizations']
    metadata = state['metadata']
    
    # Calculate severity distribution
    severity_count = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    for bug in bugs:
        severity = bug.get('severity', 'low')
        severity_count[severity] = severity_count.get(severity, 0) + 1
    
    # Determine overall severity
    if severity_count['critical'] > 0:
        overall_severity = 'CRITICAL'
    elif severity_count['high'] > 0:
        overall_severity = 'HIGH'
    elif severity_count['medium'] > 0:
        overall_severity = 'MEDIUM'
    else:
        overall_severity = 'LOW'
    
    # Build report
    report = {
        'summary': {
            'file': metadata.get('file_name', 'unknown'),
            'language': metadata.get('language', 'unknown'),
            'lines_of_code': metadata.get('lines_of_code', 0),
            'timestamp': metadata.get('timestamp', ''),
            'bugs_found': len(bugs),
            'optimizations_found': len(optimizations),
            'overall_severity': overall_severity,
        },
        'severity_distribution': severity_count,
        'bugs': bugs,
        'optimizations': optimizations,
        'metadata': metadata
    }
    
    state['report'] = report
    print(f" Report generated: {len(bugs)} bugs, {len(optimizations)} optimizations")
    
    return state
