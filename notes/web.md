---

## 1. HTML, CSS & the DOM

- HTML provides structure/semantics — prefer semantic tags (`nav`, `main`, `article`, `section`) over generic `div` everywhere; helps accessibility and SEO.
- CSS box model: every element is content + padding + border + margin. `box-sizing: border-box` makes width/height include padding/border, which is usually what you actually want.
- **Flexbox** — one-dimensional layout (row or column); great for navbars, centering, evenly distributing items.
- **Grid** — two-dimensional layout; great for full page layouts with rows and columns.
- The DOM is a tree representation of the page that JavaScript can read/manipulate:
```js
const el = document.querySelector('.card');
el.classList.add('active');
el.addEventListener('click', () => console.log('clicked'));
```

---

## 2. JavaScript Fundamentals

- `var` vs `let` vs `const`: `var` is function-scoped and hoisted (legacy, avoid); `let`/`const` are block-scoped. Default to `const`, use `let` only when reassignment is needed.
- **Closures** — a function remembers variables from its enclosing scope even after that scope has finished executing:
```js
function counter() {
  let count = 0;
  return () => ++count;
}
const inc = counter();
inc(); // 1
inc(); // 2
```
- **Promises / async–await** — handle asynchronous operations (network calls, timers) without deeply nested callbacks:
```js
async function getUser(id) {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error('Failed to fetch user');
  return res.json();
}
```
- **Event loop basics** — JS is single-threaded; async operations are queued (microtasks for Promises, macrotasks for timers/IO) and run when the current call stack is clear.

---

## 3. HTTP & REST APIs

| Method | Purpose | Idempotent? |
|--------|---------|-------------|
| GET | retrieve a resource | yes |
| POST | create a resource | no |
| PUT | replace a resource entirely | yes |
| PATCH | partially update a resource | no (in practice, often treated as idempotent) |
| DELETE | remove a resource | yes |

Common status codes:
- `200 OK`, `201 Created`, `204 No Content`
- `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
- `500 Internal Server Error`, `503 Service Unavailable`

REST principles worth following:
- Resources are nouns in the URL (`/users/42/orders`), actions are HTTP verbs — avoid `getUser`-style endpoints.
- Statelessness: each request should carry everything the server needs (e.g. an auth token), not rely on server-side session state tied to a specific request sequence.
- Use proper status codes instead of always returning `200` with an error message buried in the body.

---

## 4. Frontend Frameworks (React basics)

```jsx
function Counter() {
  const [count, setCount] = useState(0);
  useEffect(() => {
    document.title = `Count: ${count}`;
  }, [count]); // re-run only when count changes
  return <button onClick={() => setCount(count + 1)}>Clicked {count} times</button>;
}
```

- Components are reusable, composable UI building blocks; React re-renders a component when its state or props change.
- `useState` holds local state; `useEffect` runs side effects (data fetching, subscriptions, DOM manipulation) in sync with renders, controlled by the dependency array.
- Props flow one-way, parent → child. Lifting state up to a common ancestor is the standard way to share state between sibling components.
- Keys in lists (`key={item.id}`) help React efficiently track which items changed/moved — always use a stable unique id, never the array index if the list can reorder.

---

## 5. Backend Basics (Node.js / Express)

```js
const express = require('express');
const app = express();
app.use(express.json());

app.get('/api/tasks', async (req, res) => {
  const tasks = await Task.find();
  res.json(tasks);
});

app.post('/api/tasks', async (req, res) => {
  try {
    const task = await Task.create(req.body);
    res.status(201).json(task);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

- **Middleware** runs between the request arriving and the route handler responding — used for auth checks, logging, body parsing, error handling.
- Error-handling middleware should be defined last (`app.use((err, req, res, next) => ...)`) to catch errors from any route.
- Environment variables (`.env` files, never committed) for secrets/config; different values per environment (dev/staging/prod).

---

## 6. Databases (just enough to be dangerous)

- **SQL** — relational, structured schema, tables with relationships, strong consistency guarantees. Good fit when data is relational and consistency matters (e.g. financial records). Examples: PostgreSQL, MySQL.
- **NoSQL** — document/key-value, flexible schema, often easier to scale horizontally. Good fit for rapidly evolving schemas or simple key-value access patterns. Examples: MongoDB, Redis.
- **Indexes** — speed up reads on specific columns/fields but slow down writes and use extra storage; index what you actually query on, not everything.
- **N+1 query problem** — a common performance bug where fetching a list, then fetching related data per-item in a loop, results in many more queries than necessary; fix with joins or batched/eager loading.

---

## 7. Deployment Basics

- **Static sites** — host on Vercel, Netlify, GitHub Pages, etc.; push to deploy.
- **Backend services** — containerize with Docker for consistent environments; deploy on Render, Railway, AWS/GCP/Azure, etc.
- **Environment parity** — try to keep dev, staging, and prod as similar as possible (same Node version, same env-var structure) to avoid "works on my machine" bugs.
- **CI/CD basics** — automatically run tests/builds on every push (e.g. via GitHub Actions), and only deploy after checks pass.

---

_Next to explore: authentication patterns (JWT vs sessions), caching layers (Redis), WebSockets for real-time features._
