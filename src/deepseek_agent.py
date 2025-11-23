"""
DeepSeek-R1 agent using OpenAI or Ollama for local inference.
"""
import json
from typing import Dict, Any
import requests
import ollama
import yaml
import os


class DeepSeekAgent:
    """Wrapper for DeepSeek-R1 model via OpenAI or Ollama."""

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the agent with configuration."""
        if not os.path.exists(config_path):
            print(f"Warning: Configuration file '{config_path}' not found. Using default settings.")
            self.use_openai = False
            self.ollama_base_url = "http://localhost:11434"
            self.model_name = "deepseek-r1:latest"
            self.temperature = 0.1
            self.max_tokens = 2048
            return

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # OpenAI configuration
        self.openai_base_url = config.get('openai', {}).get('base_url', None)
        self.openai_api_key = config.get('openai', {}).get('api_key', None)

        # Ollama configuration
        self.ollama_base_url = config.get('ollama', {}).get('base_url', "http://localhost:11434")
        self.model_name = config['model']['name']
        self.temperature = config['model']['temperature']
        self.max_tokens = config['model']['max_tokens']

        # Determine which API to use
        self.use_openai = bool(self.openai_api_key)

    def query_openai(self, prompt: str) -> Dict[str, Any]:
        """Query OpenAI API."""
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        response = requests.post(f"{self.openai_base_url}/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def query_ollama(self, prompt: str) -> Dict[str, Any]:
        """Query Ollama API."""
        return ollama.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            options={
                'temperature': self.temperature,
                'num_predict': self.max_tokens,
            }
        )

    def query(self, prompt: str, parse_json: bool = True) -> Dict[str, Any]:
        """
        Send a query to the selected model (OpenAI or Ollama).

        Args:
            prompt: The input prompt
            parse_json: Whether to parse response as JSON

        Returns:
            Response as dictionary or raw text
        """
        try:
            if self.use_openai:
                response = self.query_openai(prompt)
                content = response['choices'][0]['message']['content']
            else:
                response = self.query_ollama(prompt)
                content = response['message']['content']

            if parse_json:
                # Try to extract JSON from markdown code blocks
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0].strip()
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0].strip()

                return json.loads(content)

            return {"response": content}

        except json.JSONDecodeError as e:
            print(f" JSON parsing error: {e}")
            print(f"Raw response: {content[:200]}...")
            return {"error": "json_parse_error", "raw_response": content}

        except Exception as e:
            print(f" Error querying model: {e}")
            return {"error": str(e)}

    def detect_bugs(self, code: str, language: str, prompt_template: str) -> Dict:
        """Detect bugs in code using specialized prompt."""
        prompt = prompt_template.format(code=code, language=language)
        return self.query(prompt, parse_json=True)

    def suggest_optimizations(self, code: str, language: str, prompt_template: str) -> Dict:
        """Suggest optimizations using specialized prompt."""
        prompt = prompt_template.format(code=code, language=language)
        return self.query(prompt, parse_json=True)

    def generate_summary(self, bug_count: int, opt_count: int, prompt_template: str) -> str:
        """Generate executive summary."""
        prompt = prompt_template.format(bug_count=bug_count, opt_count=opt_count)
        result = self.query(prompt, parse_json=False)
        return result.get('response', 'No summary generated')
