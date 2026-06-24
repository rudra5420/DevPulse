Core Python concepts, kept practical — things I actually use, not just syntax trivia.

---

## 1. Data Types

Built-in categories:
- **Numeric** — `int`, `float`, `complex`. Python ints have arbitrary precision (no overflow like fixed-width C ints).
- **Sequence** — `str`, `list`, `tuple`. Strings and tuples are immutable; lists are mutable.
- **Mapping** — `dict`. Insertion-ordered since Python 3.7.
- **Set** — `set`, `frozenset`. Unordered, unique elements, O(1) average membership check.
- **Boolean** — `bool`, subclass of int (`True == 1`, `False == 0`).
- **NoneType** — `None`, Python's null.

Mutability matters:
```python
a = [1, 2, 3]
b = a          # b refers to the SAME list
b.append(4)
print(a)       # [1, 2, 3, 4] — a changed too!

c = (1, 2, 3)  # tuple — immutable, safe to use as a dict key
```

Type hints (not enforced at runtime, but invaluable for tooling/readability):
```python
def add(x: int, y: int) -> int:
    return x + y
```

---

## 2. OOP in Python

```python
class Animal:
    def __init__(self, name: str):
        self.name = name
    def speak(self) -> str:
        raise NotImplementedError

class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} says Woof!"
```

Key concepts:
- **Encapsulation** — Python uses convention, not enforcement (`_protected`, `__private` name-mangled, not truly private).
- **Inheritance** — `class Dog(Animal)`: Dog inherits Animal's attributes/methods.
- **Polymorphism** — different classes implementing the same method name (`speak`), called interchangeably.
- **Dunder methods** — `__init__`, `__str__`, `__repr__`, `__eq__`, `__len__`, etc. let custom classes integrate with built-in syntax.
- **Class vs instance attributes** — class attributes are shared across all instances unless overridden per-instance.
- `staticmethod` vs `classmethod` vs instance methods — static methods don't take self/cls; class methods take cls and are often used for alternate constructors.

---

## 3. File Handling

Always prefer context managers — they guarantee the file is closed even if an exception occurs:
```python
with open("data.txt", "r", encoding="utf-8") as f:
    contents = f.read()
# file is automatically closed here, even on error
```

Common modes: `r` (read), `w` (write, truncates!), `a` (append), `r+` (read/write). Add `b` for binary (e.g. `rb`).

Reading line by line (memory-efficient for big files):
```python
with open("biglog.txt") as f:
    for line in f:
        process(line)
```

Working with structured data:
```python
import json, csv

with open("config.json") as f:
    config = json.load(f)

with open("data.csv", newline="") as f:
    reader = csv.DictReader(f)
    rows = [row for row in reader]
```

---

## 4. Decorators

A decorator wraps a function to add behavior without modifying the function itself:
```python
import functools, time

def timer(func):
    @functools.wraps(func)  # preserves original function's name/docstring
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
```

Common built-in/standard-library decorators: `staticmethod`, `classmethod`, `property`, `functools.lru_cache` (memoization — very useful for recursive solutions in DSA problems).

Decorators with arguments need an extra layer of nesting (a decorator factory):
```python
def retry(times: int):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == times - 1:
                        raise
        return wrapper
    return decorator
```

---

## 5. Generators

Generators produce values lazily, one at a time, instead of building a full list in memory:
```python
def fibonacci(limit: int):
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b

for num in fibonacci(50):
    print(num)
```

Why they matter:
- **Memory efficiency** — never holds the entire sequence in memory at once.
- **Composable** — generators can be chained with `map`, `filter`, generator expressions.
- `yield` pauses function execution and resumes from the same point on the next call.

Generator expression (like a list comprehension but lazy):
```python
squares = (x * x for x in range(1_000_000))  # no memory blow-up
```

`yield from` delegates to a sub-generator:
```python
def chain(*iterables):
    for it in iterables:
        yield from it
```

---

## 6. Async Programming

Why async exists: for IO-bound work (network calls, file IO, DB queries), a program spends most of its time waiting. `async/await` lets a single thread juggle many waiting tasks instead of blocking on each one sequentially.

```python
import asyncio, aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = ["https://example.com"] * 5
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*[fetch(session, u) for u in urls])
    return results

asyncio.run(main())
```

Key concepts:
- `async def` defines a coroutine — calling it returns a coroutine object; it doesn't run immediately.
- `await` hands control back to the event loop while waiting on something, letting other coroutines run.
- `asyncio.gather` runs multiple coroutines concurrently and waits for all to finish.
- Async is about **concurrency, not parallelism** — it's still single-threaded; it just avoids blocking on IO wait.
- For CPU-bound work, use `multiprocessing` instead.

Common mistake: mixing blocking calls (e.g. `time.sleep`, blocking `requests.get`) inside an `async def` function — this blocks the entire event loop. Use async-native equivalents (`asyncio.sleep`, `aiohttp`) instead.

---

*Next to explore: context managers (`__enter__`/`__exit__`), metaclasses, multiprocessing vs threading vs asyncio tradeoffs.*
