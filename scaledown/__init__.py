import os
from typing import Optional

# Import config functions first
from scaledown.config import set_api_key, get_api_key

# Import modules
from scaledown.compressor import ScaleDownCompressor
from scaledown.optimizer import HasteOptimizer
from scaledown.pipeline import Pipeline, make_pipeline
from scaledown.types import CompressedPrompt, OptimizedContext
from scaledown.exceptions import AuthenticationError, APIError, ScaleDownError

# Global configuration state
_API_KEY: Optional[str] = os.environ.get("SCALEDOWN_API_KEY")

__all__ = [
    "ScaleDownCompressor",
    "HasteOptimizer",
    "Pipeline",
    "make_pipeline",
    "set_api_key",
    "get_api_key",
    "CompressedPrompt",
    "OptimizedContext",
    "AuthenticationError",
    "APIError",
    "ScaleDownError"
]
