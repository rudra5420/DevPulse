// dfs.cpp
// Depth-First Search (DFS) on a graph — both recursive and iterative.
//
// How it works:
//   Explore as far down one path as possible before backtracking.
//   Recursive DFS uses the call stack implicitly;
//   iterative DFS uses an explicit stack data structure.
//
// Time complexity:  O(V + E)
// Space complexity: O(V)  (visited array + recursion/explicit stack)
//
// Use cases: connectivity checks, cycle detection, topological sort,
//            finding connected components, maze/path exploration.

#include <bits/stdc++.h>
using namespace std;

// --- Recursive DFS ---------------------------------------------------

void dfsRecursiveHelper(int node,
                        const vector<vector<int>>& adj,
                        vector<bool>& visited,
                        vector<int>& order) {
    visited[node] = true;
    order.push_back(node);
    for (int neighbor : adj[node])
        if (!visited[neighbor])
            dfsRecursiveHelper(neighbor, adj, visited, order);
}

vector<int> dfsRecursive(int n,
                         const vector<vector<int>>& adj,
                         int source) {
    vector<bool> visited(n, false);
    vector<int> order;
    dfsRecursiveHelper(source, adj, visited, order);
    return order;
}

// --- Iterative DFS (explicit stack) ----------------------------------
// Useful when recursion depth could blow the call stack on large graphs.

vector<int> dfsIterative(int n,
                         const vector<vector<int>>& adj,
                         int source) {
    vector<bool> visited(n, false);
    vector<int> order;
    stack<int> st;
    st.push(source);

    while (!st.empty()) {
        int node = st.top(); st.pop();
        if (visited[node]) continue;  // may be pushed more than once
        visited[node] = true;
        order.push_back(node);

        // Push neighbors in reverse so traversal order matches the recursive
        // version (purely cosmetic; doesn’t affect correctness).
        for (int i = static_cast<int>(adj[node].size()) - 1; i >= 0; i--) {
            int neighbor = adj[node][i];
            if (!visited[neighbor])
                st.push(neighbor);
        }
    }
    return order;
}

int main() {
    int n = 6;
    vector<vector<int>> adj(n);

    auto addEdge = [&](int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    };

    addEdge(0, 1); addEdge(0, 2);
    addEdge(1, 3); addEdge(2, 4);
    addEdge(3, 5); addEdge(4, 5);

    vector<int> recOrder = dfsRecursive(n, adj, 0);
    cout << "Recursive DFS order: ";
    for (int x : recOrder) cout << x << " ";
    cout << "\n";

    vector<int> iterOrder = dfsIterative(n, adj, 0);
    cout << "Iterative DFS order: ";
    for (int x : iterOrder) cout << x << " ";
    cout << "\n";

    return 0;
}
