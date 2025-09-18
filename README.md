# A* Pathfinding with GUI (Tkinter)

This project demonstrates the **A* search algorithm** on a custom graph of nodes and paths, with an animated **Tkinter GUI**.  
It allows you to set a **start node** and **goal node**, then watch A* explore the graph step by step until it finds the shortest path.

---

## Features
- Interactive **graph visualization** with nodes and edges.
- **Click left mouse** to set the **Start node (S)**.
- **Click right mouse** to set the **Goal node (G)**.
- Press **Enter ↵** to run the **A* search**.
- Animated step-by-step exploration with color-coded nodes:
  - **Green** = Start node  
  - **Red** = Goal node  
  - **Yellow** = Final path from Start → Goal  
  - **Black** = Explored nodes (closed list, shows order numbers)  
  - **Blue** = Frontier nodes (open list, shows order numbers)  
  - **White** = Unvisited nodes  

---

## Requirements
- Python 3.x  
- Tkinter (comes pre-installed with most Python distributions)

---

## How to Run
1. Save the script as `astar_gui.py`
2. Run it with:
   ```bash
   python astar_gui.py
   ```
3. Interact with the GUI:
   - Left-click a node → set as **Start**  
   - Right-click a node → set as **Goal**  
   - Press **Enter** → watch the algorithm animate step by step  

---

## Example Graph
The script includes a predefined set of `available_paths` that form a small maze-like graph with:
- Multiple branches  
- Loops  
- Dead ends  
- A valid path leading from top-left `(0,0)` to bottom-right `(7,7)`  

---

## Learning Notes
- The algorithm uses **Manhattan distance (L1 norm)** as the heuristic.  
- The open list is a **min-heap** (`heapq` in Python).  
- Each search step is delayed using `after(300, ...)` to show animation (300 ms per step).  

---

## Demo Screenshot (conceptual)
```
Check the attached files
```

---

## Credits
Developed for educational purposes to demonstrate how **A** explores and finds the shortest path in a graph.
