import simpy
import random
from chord import lookup

HOP_DELAY = 1  # simulated time units per hop

def run_lookup(env, start, key, nodes, results):
    """SimPy process: simulate one lookup with hop delays."""
    path = lookup(start, key, nodes)
    hops = len(path) - 1
    yield env.timeout(hops * HOP_DELAY)
    results.append({
        "key": key,
        "start": start,
        "path": path,
        "hops": hops,
        "responsible": path[-1],
        "latency": env.now,
    })

def simulate(nodes, num_lookups=20, seed=42):
    """Run num_lookups random lookups on nodes using SimPy. Returns results list."""
    random.seed(seed)
    env = simpy.Environment()
    results = []
    for _ in range(num_lookups):
        start = random.choice(nodes)
        key = random.randint(0, 63)
        env.process(run_lookup(env, start, key, nodes, results))
    env.run()
    return results
