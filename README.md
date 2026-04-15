# Chord P2P Lookup Simulator

This project implements a simulation of the Chord Peer-to-Peer (P2P) Lookup Protocol using Python, SimPy, and Streamlit. It demonstrates how distributed systems perform efficient key lookups using consistent hashing and finger tables.

---

## Overview

Chord is a distributed hash table (DHT) protocol in which nodes are organized in a circular identifier space called a ring. Each node is responsible for a range of keys, and lookups are performed by routing queries through intermediate nodes.

This project models the Chord protocol and provides both simulation and visualization of its behavior.

---

## Features

* Ring-based node organization
* Key lookup using finger tables
* Interactive visualization of lookup paths
* Batch simulation using SimPy
* Performance analysis showing logarithmic scaling
* Dynamic addition and removal of nodes

---

## Working Principle

The system uses a 6-bit identifier space, resulting in 64 possible positions (0 to 63).

* The successor function identifies the node responsible for a given key by selecting the first node greater than or equal to the key.
* Each node maintains a finger table with entries based on powers of two, which allows faster routing.
* The lookup process uses these entries to move closer to the target node in fewer steps.
* This reduces lookup time from linear complexity to logarithmic complexity.

---

## Project Structure

* chord.py: Implements core Chord logic including ring structure, successor, finger table, and lookup
* simulation.py: Handles discrete-event simulation using SimPy and measures performance
* app.py: Provides a Streamlit-based interface for visualization and interaction

---
## Application Modules

Ring and Lookup:
Displays the ring structure and allows users to perform key lookups with path visualization.

O(log N) Scaling:
Runs experiments to compare simulated hops with theoretical logarithmic growth.

Batch Simulation:
Executes multiple lookups and displays metrics such as hops, latency, and lookup paths.

---

## Conclusion

This project demonstrates how the Chord protocol enables efficient and scalable key lookup in distributed systems. The combination of simulation and visualization helps in understanding both its working and performance characteristics.

---

## Author

K N V H S Sai Kalyani
