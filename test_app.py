"""Quick test to verify RepoPilot functionality"""
from graph import create_pipeline

# Test code
test_code = '''def hello():
    return "world"
'''

print("Testing RepoPilot pipeline...")
pipeline = create_pipeline()
result = pipeline.run(test_code, 'python')

# Check all expected keys are present
expected_keys = ['explanation', 'security', 'documentation', 'modernization', 'roadmap', 'errors']
missing_keys = [k for k in expected_keys if k not in result]

if missing_keys:
    print(f"FAILED - Missing keys: {missing_keys}")
else:
    print("PASSED - All agent outputs present")
    print(f"Keys found: {list(result.keys())}")
    print(f"Errors: {len(result.get('errors', []))}")
    
    # Check each agent output
    for key in ['explanation', 'security', 'documentation', 'modernization', 'roadmap']:
        if result[key]:
            print(f"  ✓ {key}: OK")
        else:
            print(f"  ✗ {key}: EMPTY")

# Made with Bob
