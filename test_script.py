"""
Full ScaleDown Pipeline Integration Test (REAL API)
Tests HASTE Optimizer + ScaleDown Compressor chain with actual network calls.
"""
import os
import tempfile
import sys
import scaledown as sd
from scaledown.optimizer import HasteOptimizer
from scaledown.compressor import ScaleDownCompressor
from scaledown.pipeline import Pipeline
from scaledown.types import CompressedPrompt
from scaledown.exceptions import AuthenticationError, APIError

# -------------------------------------------------------------------------
# 🔑 CONFIGURATION
# -------------------------------------------------------------------------
# REPLACE THIS WITH YOUR ACTUAL API KEY
API_KEY = os.environ.get("SCALEDOWN_API_KEY", "yVlJ8qWWVF6wj8RZUfNHm7fUYqNBVEFr3Rrfep67")

if API_KEY == "YOUR_REAL_API_KEY_HERE":
    print("⚠️  WARNING: Using placeholder API key. The API call will likely fail.")
    print("   Export your key: export SCALEDOWN_API_KEY='sk_...'\n")

# Set the API key globally
sd.set_api_key(API_KEY)

# -------------------------------------------------------------------------
# Test Setup
# -------------------------------------------------------------------------
TEST_CODE = """
def calculate_sum(numbers):
    \"\"\"Calculate sum of numbers.\"\"\"
    total = 0
    for num in numbers:
        total += num
    return total

def calculate_average(numbers):
    \"\"\"Calculate average of numbers.\"\"\"
    if len(numbers) == 0:
        return 0
    return calculate_sum(numbers) / len(numbers)

class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    def process(self):
        return calculate_average(self.data)
"""

print("=" * 70)
print("SCALEDOWN PIPELINE REAL API TEST")
print("=" * 70)

with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(TEST_CODE)
    TEST_FILE_PATH = f.name

try:
    # -------------------------------------------------------------------------
    # 1. Initialize Components
    # -------------------------------------------------------------------------
    print("\n1. Initializing Pipeline...")
    
    optimizer = HasteOptimizer(
        top_k=2,
        semantic=False  # Local BM25 only for speed
    )
    
    compressor = ScaleDownCompressor(
        target_model="gpt-4o",
        rate="auto"
    )
    
    pipe = Pipeline([
        ('haste', optimizer),
        ('compressor', compressor)
    ])
    print(" Pipeline created successfully")

    # -------------------------------------------------------------------------
    # 2. Run Pipeline (REAL NETWORK CALL)
    # -------------------------------------------------------------------------
    print(f"\n2. Calling API (Key: {API_KEY[:4]}...{API_KEY[-4:] if len(API_KEY)>8 else ''})...")
    
    result = pipe.run(
        context=TEST_CODE,
        query="calculate_average function",
        file_path=TEST_FILE_PATH,
        prompt="Summarize this function"
    )
    
    print(" API call successful!")
    
    if isinstance(result, CompressedPrompt):
        print(" Result is a CompressedPrompt object")

    # -------------------------------------------------------------------------
    # 3. Results
    # -------------------------------------------------------------------------
    print("\n3. Results:")
    print("-" * 30)
    print(f"Original Context Size:  {len(TEST_CODE)} chars")
    print(f"Compressed Output:      {result.content}")
    print(f"Tokens Used:            {result.tokens[0]} -> {result.tokens[1]}")
    print(f"Savings:                {result.savings_percent:.1f}%")
    print(f"Latency:                {result.latency}ms")
    print("-" * 30)

    print("\nREAL API TEST PASSED!")

except AuthenticationError:
    print("\nAUTHENTICATION FAILED: Invalid API Key.")
    print("   Please check your SCALEDOWN_API_KEY environment variable.")

except APIError as e:
    print(f"\n API ERROR: {str(e)}")
    print("   The server might be down or unreachable.")

except Exception as e:
    print(f"\nUNEXPECTED ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

finally:
    if os.path.exists(TEST_FILE_PATH):
        os.unlink(TEST_FILE_PATH)
