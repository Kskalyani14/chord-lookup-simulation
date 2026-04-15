M = 6  # bits → ring has 2^M = 64 slots

def ring_size():
    return 2 ** M

def successor(key, nodes):
    """Return the first node >= key (wraps around)."""
    for n in sorted(nodes):
        if n >= key:
            return n
    return sorted(nodes)[0]

def build_finger_table(node_id, nodes):
    """Return M-entry finger table for node_id."""
    table = []
    for i in range(M):
        start = (node_id + 2**i) % ring_size()
        table.append({"i": i+1, "start": start, "successor": successor(start, nodes)})
    return table

def lookup(start, key, nodes):
    """Simulate hop-by-hop Chord lookup. Returns path (list of node ids)."""
    target = successor(key, nodes)
    path = [start]
    current = start

    for _ in range(M + 1):
        if current == target:
            break
        ft = build_finger_table(current, nodes)
        # Pick closest preceding finger
        next_hop = ft[0]["successor"]  # default: go to successor
        for entry in reversed(ft):
            f = entry["successor"]
            a, b = current, target
            # Is f strictly between current and target on ring?
            if a != b:
                if a < b:
                    in_range = a < f < b
                else:
                    in_range = f > a or f < b
                if in_range:
                    next_hop = f
                    break
        path.append(next_hop)
        current = next_hop
        if current == target:
            break

    return path
