"""
Demonstration of `from __future__ import annotations` (PEP 563).

This shows how type annotations are stored differently:
- WITHOUT the import: annotations are evaluated as live objects at import time
- WITH the import: annotations are stored as strings
"""

# =============================================================================
# WITHOUT the import: annotations are actual class objects
# =============================================================================

class B:
    pass

class A:
    partner: B

print("WITHOUT __future__ import:")
print(f"  A.__annotations__ = {A.__annotations__}")
print(f"  Type of annotation: {type(A.__annotations__['partner'])}")
print()

# =============================================================================
# WITH the import: annotations are strings
# =============================================================================

# We need to use exec to demonstrate the difference in the same file
# because the __future__ import affects the entire module

code_with_future = """
from __future__ import annotations

class B:
    pass

class A:
    partner: B

print("WITH __future__ import:")
print(f"  A.__annotations__ = {A.__annotations__}")
print(f"  Type of annotation: {type(A.__annotations__['partner'])}")
"""

exec(code_with_future)
