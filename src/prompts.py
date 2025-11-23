"""
Prompt templates for DeepSeek-R1 code review tasks.
"""

BUG_DETECTION_PROMPT = """You are an expert code reviewer specializing in bug detection.

Analyze the following {language} code and identify ALL bugs, errors, and vulnerabilities.

CODE (with line numbers):
```{language}
{code}
```

IMPORTANT: Use the EXACT line numbers shown in the code above.

Focus on:
- Logic errors (off-by-one, null pointer, division by zero)
- Security vulnerabilities (SQL injection, XSS, buffer overflow)
- Memory issues (leaks, dangling pointers)
- Concurrency issues (race conditions, deadlocks)
- Exception handling problems

For EACH bug found, provide:
1. Line number
2. Severity (critical/high/medium/low)
3. Clear description
4. Specific fix suggestion
5. Confidence level (0.0-1.0)

Respond in JSON format:
{{
  "bugs": [
    {{
      "line": <line_number>,
      "severity": "<severity>",
      "type": "<bug_type>",
      "description": "<what's wrong>",
      "suggestion": "<how to fix>",
      "confidence": <0.0-1.0>
    }}
  ]
}}

If no bugs found, return: {{"bugs": []}}
"""

OPTIMIZATION_PROMPT = """You are an expert code reviewer specializing in optimization and best practices.

Analyze the following {language} code for optimization opportunities.

CODE (with line numbers):
```{language}
{code}
```

IMPORTANT: Use the EXACT line numbers shown in the code above.

Focus on:
- Performance improvements (algorithm efficiency, caching, lazy loading)
- Code quality (readability, maintainability, DRY principle)
- Best practices (naming conventions, design patterns)
- Security hardening
- Resource management

For EACH optimization, provide:
1. Type (performance/security/best_practice/code_smell)
2. Line number (if applicable)
3. Description of current issue
4. Specific improvement suggestion
5. Expected impact (high/medium/low)

Respond in JSON format:
{{
  "optimizations": [
    {{
      "type": "<type>",
      "line": <line_number or null>,
      "category": "<specific_category>",
      "description": "<current_issue>",
      "suggestion": "<improvement>",
      "impact": "<impact_level>"
    }}
  ]
}}

If no optimizations needed, return: {{"optimizations": []}}
"""

SUMMARY_PROMPT = """Summarize the code review findings concisely.

BUGS FOUND: {bug_count}
OPTIMIZATIONS: {opt_count}

Provide a brief executive summary (2-3 sentences) covering:
- Overall code quality
- Critical issues requiring immediate attention
- General recommendations

Summary:"""
