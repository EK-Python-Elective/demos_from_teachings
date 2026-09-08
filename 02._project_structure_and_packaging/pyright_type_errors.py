"""A menu of deliberate type errors for the pyright demo in session 2, part 3.

Teaching fixture. Most of this *runs* (or crashes only much later) — the point is
that pyright flags it now, before you ship it.

    uvx pyright pyright_type_errors.py

pyright's default mode ("standard") is what the fork uses, so a plain run
reproduces what the fork's CI reports. Each block names the rule pyright applies
and the shape of the message.
"""

from __future__ import annotations

# 1. Wrong literal for a declared type — reportAssignmentType.
#    "Type 'str' is not assignable to declared type 'int'"
#    Runs fine at runtime; nothing stops you. That gap is the whole pitch.
testnumber: int = "I am not an int"


# 2. Reassignment to an incompatible type — reportAssignmentType, on the 2nd line.
count: int = 0
count = "done"


# 3. Wrong argument type — reportArgumentType.
#    "Argument of type 'str' cannot be assigned to parameter 'n' of type 'int'"
def double(n: int) -> int:
    return n * 2


double("hello")


# 4. Wrong return type — reportReturnType.
#    "Type 'int' is not assignable to return type 'str'"
def get_name() -> str:
    return 42


# 5. Possibly None — reportOptionalMemberAccess.
#    "'upper' is not a known attribute of 'None'"
#    The most common real bug pyright catches. Previews `| None` / narrowing (session 3):
#    the fix is `if found is not None:` before using it.
def first_word(text: str) -> str | None:
    parts = text.split()
    return parts[0] if parts else None


found = first_word("")
print(found.upper())


# 6. Wrong element in a container — reportAssignmentType.
#    "Type 'str' is not assignable to type 'int'"
nums: list[int] = [1, 2, "3"]


# 7. Typo'd attribute / method — reportAttributeAccessIssue.
#    "'uppr' is not a known attribute of 'str'"
#    No annotations anywhere — pyright knows str's methods.
print("hello".uppr())


# 8. Missing argument — reportCallIssue.
#    "Argument missing for parameter 'greeting'"
def greet(name: str, greeting: str) -> None:
    print(greeting, name)


greet("Sam")
