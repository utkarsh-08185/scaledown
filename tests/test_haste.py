import pytest
import tempfile
import os
import scaledown as sd

TEST_CODE = """
def dependency(x):
    return x + 1

def target_function(x):
    return dependency(x) * 2

class UnusedClass:
    pass
"""

@pytest.fixture
def temp_python_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(TEST_CODE)
        temp_path = f.name
    yield temp_path
    if os.path.exists(temp_path):
        os.unlink(temp_path)

def test_initialization():
    opt = sd.HasteOptimizer(top_k=5, semantic=False)
    assert opt.top_k == 5
    assert opt.semantic is False

def test_optimization_bm25(temp_python_file):
    opt = sd.HasteOptimizer(top_k=1, semantic=False)
    result = opt.optimize(
        context="",
        query="target_function",
        file_path=temp_python_file
    )
    
    assert isinstance(result, sd.OptimizedContext)
    assert "def target_function" in result.content
    assert "def dependency" in result.content
    assert "class UnusedClass" not in result.content

def test_metrics_integrity(temp_python_file):
    opt = sd.HasteOptimizer(semantic=False)
    result = opt.optimize(context="", query="target_function", file_path=temp_python_file)
    
    assert result.metrics.original_tokens > 0
    assert result.metrics.optimized_tokens > 0
    assert result.metrics.optimized_tokens <= result.metrics.original_tokens
