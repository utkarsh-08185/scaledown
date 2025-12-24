# ScaleDown

ScaleDown is an intelligent prompt compression framework that reduces LLM token usage while preserving semantic meaning.

## Key Features

*   **HASTE Optimizer**: Intelligently selects relevant code using AST analysis and semantic search.
*   **Context Compression**: Rewrites prompts to be dense and token-efficient using the ScaleDown API.
*   **Modular Pipeline**: Chain optimizers and compressors for custom workflows.
*   **Easy Integration**: Drop-in Python client for seamless usage.

---
## Installation

Install using `uv` (recommended) or `pip`:


From PyPI (if published):

```bash
pip install scaledown
```
*(Requires `HasteContext` for local optimization: `pip install HasteContext>=0.2.1`)*

---

## Configuration

`ScaleDownCompressor` needs an API key and an API URL. The URL has a sensible default and can be overridden via an environment variable.

### Environment variables

- `SCALEDOWN_API_KEY` – your ScaleDown API key (used by the package-wide `scaledown.get_api_key()`).
- `SCALEDOWN_API_URL` – optional override for the compression endpoint.  
  Defaults to:

```
https://api.scaledown.xyz/compress/raw
```

Example:

```bash
export SCALEDOWN_API_KEY="sk-your-key"
export SCALEDOWN_API_URL="your-api-url"
```

---

## Quickstart

### Single prompt compression

```python
from scaledown.compressor.scaledown_compressor import ScaleDownCompressor

# Initialize the compressor
compressor = ScaleDownCompressor(
    target_model="gpt-4o",
    rate="auto",
    api_key="sk-your-key",        # or rely on scaledown.get_api_key()
    temperature=None,
    preserve_keywords=False,
    preserve_words=None,
)

context = "Very long context, e.g. conversation history or a document..."
prompt = "Summarize the main points in 3 bullet points."

compressed = compressor.compress(context=context, prompt=prompt)

# `compressed` is a CompressedPrompt instance (string subclass)
print("Compressed text:")
print(compressed)

print("\nMetrics:")
print(compressed.metrics)
# Example keys: original_prompt_tokens, compressed_prompt_tokens, latency_ms, model_used, timestamp
```

---

## Batch and broadcast usage

`ScaleDownCompressor.compress` supports multiple input modes:

- `context: str`, `prompt: str` → single compression.
- `context: List[str]`, `prompt: List[str]` (same length) → batched compression.
- `context: List[str]`, `prompt: str` → prompt is broadcast to all contexts.

### Batched compression

```python
contexts = [
    "Conversation / document A ...",
    "Conversation / document B ...",
]
prompts = [
    "Summarize conversation A.",
    "Summarize conversation B.",
]

batch_results = compressor.compress(context=contexts, prompt=prompts)

for i, res in enumerate(batch_results):
    print(f"=== Result {i} ===")
    print(res)
    print(res.metrics)
```

### Broadcast prompt

```python
docs = [
    "First document about topic X...",
    "Second document about topic Y...",
    "Third document about topic Z...",
]

query = "Extract the 3 most important facts."

broadcast_results = compressor.compress(context=docs, prompt=query)

for res in broadcast_results:
    print(res)
```
### Pipeline example
```python
import scaledown as sd
from scaledown.optimizer import HasteOptimizer
from scaledown.compressor import ScaleDownCompressor
from scaledown.pipeline import Pipeline
```

1. Initialize Components
```python
optimizer = HasteOptimizer(top_k=5, semantic=True)
compressor = ScaleDownCompressor(target_model="gpt-4o")
```
2. Create Pipeline
```python
pipe = Pipeline([
('haste', optimizer),
('compressor', compressor)
])
```
3. Run on your code file
```python
result = pipe.run(
query="Explain the training loop",
file_path="my_model.py",
prompt="Summarize the key logic"
)

print(f"Original Tokens: {len(result.original_content) // 4} (approx)")
print(f"Final Tokens: {result.metrics['total_tokens']}")
print(f"Optimized Content:\n{result.final_content}")
```
---

## Error handling

The package defines custom exceptions:

- `AuthenticationError` – raised when no API key is available (`scaledown.get_api_key()` and constructor both fail to provide one).
- `APIError` – raised when the HTTP request to the ScaleDown API fails (network issues, non‑2xx responses, etc.).

Example:

```python
from scaledown import Pipeline
from scaledown.exceptions import AuthenticationError, OptimizerError, APIError

try:
    pipe = Pipeline([...])
    result = pipe.run(query="fix bug", file_path="app.py", prompt="Analyze this")
    
except AuthenticationError:
    print("Invalid or missing API Key.")
except OptimizerError as e:
    print(f"HASTE Optimization failed: {e}")
except APIError as e:
    print(f"Compression API failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

```

---

## Development

### Setup

```bash
git clone https://github.com/ilatims-b/scaledown.git
cd scaledown
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

### Running tests

Tests live in the `tests/` directory and use `pytest`.

```bash
pip install pytest requests
pytest -v
```

The tests mock HTTP calls so they do not hit the real ScaleDown API.

---

## Project structure (simplified)

```
scaledown/
    __init__.py           # Top-level exports (set_api_key, etc.)
    types.py              # Data classes (PipelineResult, OptimizedContext)
    exceptions.py         # Custom exceptions
    
    pipeline/             # Pipeline orchestration
        __init__.py
        pipeline.py       # Pipeline class logic
        
    optimizer/            # Context Selection (Local)
        __init__.py
        base.py           # BaseOptimizer interface
        haste.py          # HasteOptimizer implementation
        
    compressor/           # Context Compression (Remote)
        __init__.py
        base.py           # BaseCompressor interface
        scaledown_compressor.py  # ScaleDown API client
        config.py         # API configuration
        
tests/                    # Pytest suite
    test_pipeline.py
    test_haste.py
    test_compressor.py
    test_config.py
```

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.