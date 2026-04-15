import math, time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from chord import build_finger_table, lookup, ring_size, successor
from simulation import simulate

st.set_page_config(page_title="Chord Simulator", layout="wide")
st.title("🔗 Chord P2P Lookup Simulator")

# ── Session state: node list ──────────────────────────────────
if "nodes" not in st.session_state:
    st.session_state.nodes = [0, 8, 16, 25, 35, 45, 55]

nodes = st.session_state.nodes

# ── Sidebar: add / remove nodes ───────────────────────────────
with st.sidebar:
    st.header("Manage Nodes")
    add_id = st.number_input("Add node ID (0–63)", 0, 63, 10, step=1)
    if st.button("➕ Add Node"):
        if add_id not in nodes:
            nodes.append(add_id)
            st.session_state.nodes = sorted(nodes)
            st.rerun()
        else:
            st.warning("Node already exists.")

    rem_id = st.selectbox("Remove node", sorted(nodes))
    if st.button("❌ Remove Node") and len(nodes) > 2:
        nodes.remove(rem_id)
        st.session_state.nodes = sorted(nodes)
        st.rerun()

    st.markdown("---")
    st.write(f"**Nodes ({len(nodes)}):** {sorted(nodes)}")

# ─────────────────────────────────────────────────────────────
# Ring drawing helper
# ─────────────────────────────────────────────────────────────
def draw_ring(nodes, path=None, key=None):
    N = ring_size()
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_facecolor("#0f172a"); fig.patch.set_facecolor("#0f172a")

    # Draw circle
    circle = plt.Circle((0,0), 1, fill=False, color="#334155", lw=2)
    ax.add_patch(circle)

    def pos(node_id):
        angle = math.radians(90 - 360 * node_id / N)
        return math.cos(angle), math.sin(angle)

    # Highlight path edges
    if path and len(path) > 1:
        for i in range(len(path)-1):
            x1,y1 = pos(path[i]); x2,y2 = pos(path[i+1])
            ax.annotate("", xy=(x2,y2), xytext=(x1,y1),
                arrowprops=dict(arrowstyle="->", color="#38bdf8", lw=2))

    # Draw all nodes
    for n in nodes:
        x, y = pos(n)
        color = "#facc15" if (path and n == path[0]) else \
                "#4ade80" if (path and n == path[-1]) else \
                "#38bdf8" if (path and n in path) else "#94a3b8"
        ax.plot(x, y, "o", color=color, ms=10, zorder=5)
        ax.text(x*1.18, y*1.18, str(n), color=color,
                ha="center", va="center", fontsize=8, fontweight="bold")

    # Draw key position
    if key is not None:
        x, y = pos(key)
        ax.plot(x, y, "D", color="#f472b6", ms=8, zorder=6)
        ax.text(x*1.18, y*1.18, f"k={key}", color="#f472b6",
                ha="center", va="center", fontsize=7)

    ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4)
    return fig

# ─────────────────────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🌐 Ring & Lookup", "📊 O(log N) Scaling", "📋 Batch Simulation"])

# ══════════════════ TAB 1: Ring & Lookup ══════════════════════
with tab1:
    col1, col2 = st.columns([1, 1])

    with col2:
        st.subheader("Key Lookup")
        start = st.selectbox("Start node", sorted(nodes))
        key   = st.slider("Key to look up", 0, 63, 20)
        animate = st.checkbox("Animate hops", value=True)
        run_btn = st.button("🔍 Lookup", use_container_width=True)

        # Finger table
        st.subheader("Finger Table")
        ft_node = st.selectbox("Show finger table for", sorted(nodes))
        ft = build_finger_table(ft_node, nodes)
        st.dataframe(pd.DataFrame(ft), hide_index=True, use_container_width=True)

    with col1:
        st.subheader("Ring Topology")
        ring_placeholder = st.empty()

        if run_btn:
            path = lookup(start, key, nodes)
            hops = len(path) - 1

            if animate:
                for step in range(1, len(path)+1):
                    ring_placeholder.pyplot(draw_ring(nodes, path[:step], key))
                    time.sleep(0.5)
            else:
                ring_placeholder.pyplot(draw_ring(nodes, path, key))

            responsible = successor(key, nodes)
            st.success(f"Key **{key}** → Node **{responsible}** in **{hops}** hops")
            st.write("Path: " + " → ".join(str(n) for n in path))
        else:
            ring_placeholder.pyplot(draw_ring(nodes))

# ══════════════════ TAB 2: O(log N) ══════════════════════════
with tab2:
    st.subheader("Average Hops vs Number of Nodes")
    st.write("Builds rings of size 2–30 nodes and measures average hops via SimPy.")

    if st.button("▶ Run Experiment"):
        data = []
        for n in range(2, 31, 2):
            ring_nodes = list(range(0, 64, max(1, 64//n)))[:n]
            results = simulate(ring_nodes, num_lookups=30, seed=7)
            avg = sum(r["hops"] for r in results) / len(results)
            data.append({"N": n, "Avg Hops": round(avg, 2), "log2(N)": round(math.log2(n), 2)})

        df = pd.DataFrame(data)
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor("#0f172a"); ax.set_facecolor("#131720")
        ax.plot(df["N"], df["Avg Hops"], "o-", color="#38bdf8", label="Simulated avg hops")
        ax.plot(df["N"], df["log2(N)"], "--", color="#f472b6", label="log₂(N) theoretical")
        ax.set_xlabel("Number of Nodes", color="#94a3b8")
        ax.set_ylabel("Avg Hops", color="#94a3b8")
        ax.tick_params(colors="#94a3b8")
        ax.legend(); ax.grid(alpha=0.2)
        st.pyplot(fig)
        st.dataframe(df, hide_index=True, use_container_width=True)

# ══════════════════ TAB 3: Batch Sim ═════════════════════════
with tab3:
    st.subheader("Batch Simulation (SimPy)")
    n_lookups = st.slider("Number of lookups", 5, 50, 20)

    if st.button("▶ Run Simulation"):
        results = simulate(sorted(nodes), num_lookups=n_lookups)
        df = pd.DataFrame([{
            "Key": r["key"], "Start": r["start"],
            "Responsible": r["responsible"],
            "Hops": r["hops"], "Latency": r["latency"],
            "Path": "→".join(str(x) for x in r["path"])
        } for r in results])

        c1, c2, c3 = st.columns(3)
        c1.metric("Avg Hops", f"{df['Hops'].mean():.2f}")
        c2.metric("Max Hops", int(df['Hops'].max()))
        c3.metric("Avg Latency", f"{df['Latency'].mean():.1f}")

        st.dataframe(df, hide_index=True, use_container_width=True)
