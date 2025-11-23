"""
Main CLI script for running code reviews.

Usage:
    python examples/review.py <file_path>
    
Example:
    python examples/review.py test_samples/buggy_code.py
"""
import sys
import os
import threading

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.workflow import run_review
from src.report_generator import (
    save_json_report,
    save_markdown_report,
    print_report_summary
)


def scan_directory(directory):
    """
    Recursively scan a directory for code files.

    Args:
        directory: Path to the directory to scan.

    Returns:
        List of file paths for all code files in the directory.
    """
    supported_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rb', '.php']
    code_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in supported_extensions):
                code_files.append(os.path.join(root, file))

    return code_files

def run_project_review(directory):
    """
    Run code review for all files in a directory.

    Args:
        directory: Path to the directory to review.

    Returns:
        List of reports for all reviewed files.
    """
    code_files = scan_directory(directory)
    reports = []

    def review_file(file_path):
        try:
            report = run_review(file_path)
            reports.append((file_path, report))
        except Exception as e:
            print(f"Error reviewing {file_path}: {e}")

    threads = []
    for file_path in code_files:
        thread = threading.Thread(target=review_file, args=(file_path,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return reports

def main():
    """Main entry point for CLI."""
    if len(sys.argv) < 2:
        print(" Usage: python examples/review.py <file_or_directory_path>")
        print("Example: python examples/review.py test_samples/buggy_code.py")
        sys.exit(1)

    path = sys.argv[1]

    if not os.path.exists(path):
        print(f" Path not found: {path}")
        sys.exit(1)

    try:
        if os.path.isfile(path):
            report = run_review(path)
            print_report_summary(report)
            json_path = save_json_report(report)
            md_path = save_markdown_report(report)
            print(f" Reports saved:\n   - JSON: {json_path}\n   - Markdown: {md_path}")
        elif os.path.isdir(path):
            reports = run_project_review(path)
            print("\nProject review complete. Reports generated for the following files:")
            for file_path, report in reports:
                print(f" - {file_path}")
        else:
            print(" Invalid path. Please provide a file or directory.")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n  Review interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n Error during review: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
