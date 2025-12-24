import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
import scaledown as sd

TEST_CODE = """
def core_logic():
    return True
"""

@pytest.fixture
def temp_python_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(TEST_CODE)
        path = f.name
    yield path
    if os.path.exists(path):
        os.unlink(path)

@pytest.fixture
def pipeline():
    opt = sd.HasteOptimizer(semantic=False)
    comp = sd.ScaleDownCompressor(api_key="test_key")
    return sd.Pipeline([
        ('haste', opt),
        ('compressor', comp)
    ])

@patch('requests.post')
def test_full_pipeline_flow(mock_post, pipeline, temp_python_file):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": {
            "compressed_prompt": "def core_logic(): return True",
            "original_prompt_tokens": 20,
            "compressed_prompt_tokens": 10
        }
    }
    mock_post.return_value = mock_response

    result = pipeline.run(
        context=TEST_CODE,
        query="core_logic",
        file_path=temp_python_file,
        prompt="minimize"
    )

    assert isinstance(result, sd.CompressedPrompt)
    assert result.content == "def core_logic(): return True"
    assert mock_post.called
