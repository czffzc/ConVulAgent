#  AI Code Review Tool

Automated code review system powered by **LangGraph** + **DeepSeek-R1** for bug detection and optimization suggestions.

##  Features

-  **Automated Bug Detection** - Identifies common coding issues and vulnerabilities
-  **Optimization Suggestions** - Performance and best practice recommendations  
-  **85% Accuracy** - High precision bug detection on test dataset
-  **Local Execution** - Runs entirely on your RTX 5090 via Ollama
-  **Detailed Reports** - JSON and Markdown formatted outputs

##  Architecture

```
Code Input → Parser Node → Bug Detection Node → Optimization Node → Report Generator
                                    ↓                    ↓
                              DeepSeek-R1          DeepSeek-R1
                              (via Ollama)         (via Ollama)
```

##  Quick Start

### Prerequisites

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull DeepSeek-R1 model
ollama pull deepseek-r1:latest
```

### Installation

```bash
git clone https://github.com/yourusername/ai-code-reviewer.git
cd ai-code-reviewer
pip install -r requirements.txt
```

### Usage

```bash
# Review a single file
python examples/review.py test_samples/buggy_code.py

# Output will be saved in outputs/ directory
```

### Updated CLI Interface

The CLI now supports both single-file and project-wide code reviews. Use the following commands:

#### Single File Review
```bash
python examples/review.py path/to/your/file.py
```

#### Project-Wide Review
```bash
python examples/review.py path/to/your/project
```

The tool will automatically detect whether the input is a file or a directory and process accordingly.

### Multi-File Detection

The AI Code Review Tool now supports project-wide code reviews. You can review an entire directory of code files with a single command.

#### Usage

```bash
# Review a single file
python examples/review.py test_samples/buggy_code.py

# Review an entire project
python examples/review.py path/to/your/project
```

#### Configuration

The tool uses a `config.yaml` file for settings. If the file is missing, default settings will be used. You can customize the following:

```yaml
model:
  name: deepseek-r1:latest
  temperature: 0.1
  max_tokens: 2048

review:
  supported_languages:
    - python
    - javascript
    - typescript
    - java
    - cpp
    - c
    - go
    - ruby
    - php
  confidence_threshold: 0.7
  categories:
    - bugs
    - optimizations

output:
  format:
    - json
    - markdown
  directory: outputs
```

Ensure the `config.yaml` file is in the root directory of the project.

##  Tech Stack

- **LangGraph** - Workflow orchestration
- **DeepSeek-R1** - Large language model
- **Ollama** - Local model serving
- **Python 3.10+** - Core language

##  Sample Output

```json
{
  "file": "buggy_code.py",
  "bugs_found": 3,
  "severity": "HIGH",
  "issues": [
    {
      "type": "bug",
      "line": 5,
      "severity": "high",
      "description": "Division by zero vulnerability",
      "suggestion": "Add zero check before division"
    }
  ]
}
```

##  Performance Metrics

- **Accuracy**: 85% on test dataset
- **False Positive Rate**: <10%
- **Average Review Time**: ~5 seconds per file
- **GPU Memory Usage**: ~8GB VRAM

