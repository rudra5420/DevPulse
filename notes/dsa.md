Data Structures & Algorithms notes — patterns, complexity, and C++ implementations.

---

## 1. Arrays

Properties: contiguous memory, O(1) random access by index, O(n) insertion/deletion at arbitrary positions (everything after shifts).

Patterns worth memorizing:
- **Two pointers** — e.g. finding a pair that sums to a target in a sorted array; move left pointer up / right pointer down based on comparison to target. O(n) instead of O(n²).
- **Sliding window** — maintain a window [left, right] that expands/shrinks based on a condition; great for longest/shortest subarray satisfying X.
- **Prefix sum** — precompute `prefix[i] = sum(arr[0..i])` so any range sum is `prefix[r] - prefix[l-1]` in O(1).
- **Kadane’s algorithm** — maximum subarray sum in O(n):

```cpp
int maxSubArray(vector<int>& nums) {
    int best = nums[0], cur = nums[0];
    for (int i = 1; i < nums.size(); i++) {
        cur = max(nums[i], cur + nums[i]);
        best = max(best, cur);
    }
    return best;
}
```

---

## 2. Linked Lists

```cpp
struct Node {
    int val;
    Node* next;
    Node(int v) : val(v), next(nullptr) {}
};
```

Why use one over an array: O(1) insertion/deletion at the front (or anywhere, given a pointer to the node); no need to know size ahead of time; no shifting cost. Tradeoff: O(n) random access, extra memory per node for the pointer.

Classic patterns:
- **Fast/slow pointers** (tortoise and hare) — detect cycles, find the middle node, find the start of a cycle.
- **Reversing a list** iteratively:
```cpp
Node* reverse(Node* head) {
    Node* prev = nullptr;
    while (head) {
        Node* next = head->next;
        head->next = prev;
        prev = head;
        head = next;
    }
    return prev;
}
```
- **Dummy head node trick** — simplifies edge cases (empty list, removing the head) by always having a placeholder node before the real head.

---

## 3. Trees

```cpp
struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};
```

Traversals:
- **In-order** (left, root, right) — gives sorted order for a BST.
- **Pre-order** (root, left, right) — useful for copying/serializing a tree.
- **Post-order** (left, right, root) — useful for deleting a tree or computing subtree-dependent values.
- **Level-order** (BFS) — uses a queue, processes the tree level by level.

BST property: for every node, all left-subtree values < node value < all right-subtree values. Gives O(log n) search/insert/delete if balanced; degrades to O(n) on a skewed tree.

Self-balancing trees (AVL, Red-Black) maintain O(log n) guarantees by rebalancing on insert/delete — this is what `std::map`/`std::set` use under the hood.

Common interview patterns: height/diameter of a tree, lowest common ancestor (LCA), checking if a tree is balanced/symmetric, serializing/deserializing a tree.

---

## 4. Graphs

Representations:
- **Adjacency list** — `vector<vector<int>> adj(n)` — space-efficient for sparse graphs, the default choice in most problems.
- **Adjacency matrix** — `vector<vector<int>> adj(n, vector<int>(n))` — O(1) edge lookup, but O(n²) space; fine for dense graphs or small n.

Traversals:
- **BFS** — explores level by level using a queue; finds shortest path in unweighted graphs.
- **DFS** — explores as deep as possible before backtracking, using a stack (explicit or recursive call stack); useful for connectivity, cycle detection, topological sort.

Key algorithms:
- **Dijkstra’s** — shortest path from a source in a weighted graph with non-negative edges. O((V+E) log V) with a priority queue.
- **Bellman-Ford** — shortest path that also handles negative edge weights and detects negative cycles. O(VE).
- **Topological sort** — ordering of nodes in a DAG such that every edge goes from earlier to later; via DFS post-order reversal or Kahn’s algorithm (BFS with in-degree tracking).
- **Union-Find (DSU)** — efficiently tracks connected components; used heavily in Kruskal’s MST algorithm and cycle detection in undirected graphs.
- **MST** — Kruskal’s (sort edges, union-find) or Prim’s (priority queue, grow from a node); both O(E log E)-ish.

---

## 5. Dynamic Programming

Core idea: break a problem into overlapping subproblems, solve each once, and reuse the result (memoization or tabulation) instead of recomputing.

Two implementation styles:
- **Top-down (memoization)** — write the natural recursive solution, cache results (e.g. via a hash map or array).
- **Bottom-up (tabulation)** — build the solution iteratively from the smallest subproblems up, typically using an array/table.

Classic patterns:
- **0/1 Knapsack** — for each item, decide take/skip: `dp[i][w]` = best value using first i items with capacity w.
- **LIS** (Longest Increasing Subsequence) — `dp[i]` = length of the longest increasing subsequence ending at index i. O(n²) naive, O(n log n) with binary search.
- **LCS** (Longest Common Subsequence) — `dp[i][j]` = LCS length of first i chars of A and first j chars of B.
- **Coin change** (unbounded knapsack) — minimum coins to make an amount, or count ways to make an amount.

How to recognize a DP problem: the problem asks for an optimum (min/max) or a count, and naive recursion would revisit the same subproblem multiple times (overlapping subproblems + optimal substructure).

---

## 6. Greedy Algorithms

Core idea: make the locally optimal choice at each step, hoping (and, ideally, proving) it leads to a globally optimal solution.

Greedy is faster than DP when it works, but it doesn’t always work — needs a correctness proof (exchange argument, matroid structure, etc.), not just intuition.

Classic examples:
- **Activity selection** — sort by end time, greedily pick the next activity that starts after the previous one ends. Provably optimal.
- **Huffman coding** — repeatedly merge the two lowest-frequency nodes to build an optimal prefix-free encoding tree.
- **Kruskal’s MST** — sort edges by weight, greedily add if it doesn’t form a cycle (checked via union-find).
- **Fractional knapsack** — take items in order of value/weight ratio, taking fractions if needed; works for the fractional version (the 0/1 version needs DP instead).

Greedy vs DP gut check: if you can prove a locally optimal choice never gets beaten by a different choice later (no need to keep multiple options open), greedy is enough. If the optimal choice depends on what you decide elsewhere, you need DP to consider the alternatives.

---

*Next to explore: segment trees, Fenwick trees (range queries), trie-based string problems, network flow (max-flow/min-cut), advanced graph (SCC via Tarjan/Kosaraju).*
