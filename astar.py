import tkinter as tk
import heapq

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self, other):
        return self.f < other.f

def build_graph(available_paths: list):
    graph = {}
    for path in available_paths:
        start_node = (path["x1"], path["y1"])
        end_node = (path["x2"], path["y2"])
        
        if start_node not in graph:
            graph[start_node] = []
        if end_node not in graph:
            graph[end_node] = []
        
        graph[start_node].append(end_node)
        graph[end_node].append(start_node)
    return graph

class AStarGUI:
    def __init__(self, master, available_paths):
        self.master = master
        self.available_paths = available_paths
        self.graph = build_graph(available_paths)
        
        self.start = None
        self.goal = None
        self.path = None
        self.open_list = []
        self.closed_list = set()
        self.end_node = None
        self.animating = False
        self.explored_order = {}  # <-- store order numbers
        self.step_count = 0

        self.canvas = tk.Canvas(master, width=600, height=600, bg="white")
        self.canvas.pack()
        self.draw_graph()
        
        self.canvas.bind("<Button-1>", self.set_start)
        self.canvas.bind("<Button-3>", self.set_goal)
        master.bind("<Return>", self.run_astar)
    
    def draw_graph(self):
        self.canvas.delete("all")
        # Draw edges
        for path in self.available_paths:
            x1, y1 = path["x1"]*40+30, path["y1"]*40+30
            x2, y2 = path["x2"]*40+30, path["y2"]*40+30
            self.canvas.create_line(x1,y1,x2,y2,fill="gray",width=2)
        
        # Draw nodes with colors + text
        for node in self.graph.keys():
            x, y = node[0]*40+30, node[1]*40+30
            color = "white"
            label = ""

            if node == self.start:
                color, label = "green", "S"
            elif node == self.goal:
                color, label = "red", "G"
            elif self.path and node in self.path:
                color = "yellow"
            elif node in self.closed_list:
                color, label = "black", str(self.explored_order.get(node,""))
            elif any(n.position == node for _,n in self.open_list):
                color, label = "blue", str(self.explored_order.get(node,""))

            # Node circle
            self.canvas.create_oval(x-12,y-12,x+12,y+12,fill=color,outline="black")
            # Node text
            if label:
                self.canvas.create_text(x,y,text=label,fill="white" if color in ["black","blue","red","green"] else "black",font=("Arial",10,"bold"))

    def set_start(self, event):
        grid_x, grid_y = event.x//40, event.y//40
        if (grid_x,grid_y) in self.graph:
            self.start = (grid_x,grid_y)
            self.reset_search()
        self.draw_graph()
    
    def set_goal(self, event):
        grid_x, grid_y = event.x//40, event.y//40
        if (grid_x,grid_y) in self.graph:
            self.goal = (grid_x,grid_y)
            self.reset_search()
        self.draw_graph()
    
    def reset_search(self):
        self.path = None
        self.open_list = []
        self.closed_list = set()
        self.animating = False
        self.explored_order = {}
        self.step_count = 0

    def run_astar(self, event=None):
        if not (self.start and self.goal):
            print("Set start and goal first!")
            return
        self.reset_search()
        start_node = Node(None, self.start)
        self.end_node = Node(None, self.goal)
        heapq.heappush(self.open_list, (start_node.f, start_node))
        self.animating = True
        self.animate_step()

    def animate_step(self):
        if not self.animating or not self.open_list:
            return
        
        _, current_node = heapq.heappop(self.open_list)
        self.closed_list.add(current_node.position)
        self.step_count += 1
        self.explored_order[current_node.position] = self.step_count

        # Goal check
        if current_node.position == self.end_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            self.path = path[::-1]
            self.animating = False
            self.draw_graph()
            return

        # Expand neighbors
        for neighbor_pos in self.graph.get(current_node.position, []):
            if neighbor_pos in self.closed_list:
                continue
            new_node = Node(current_node, neighbor_pos)
            new_node.g = current_node.g + 1
            new_node.h = abs(new_node.position[0] - self.end_node.position[0]) + \
                         abs(new_node.position[1] - self.end_node.position[1])
            new_node.f = new_node.g + new_node.h
            in_open = any(open_node.position == new_node.position and open_node.g <= new_node.g 
                          for _, open_node in self.open_list)
            if not in_open:
                heapq.heappush(self.open_list, (new_node.f, new_node))
        
        self.draw_graph()
        self.master.after(300, self.animate_step)  # <-- controls speed (ms per step)

        # -------------------------
        # Example Usage
        # -------------------------
        if __name__ == "__main__":
            available_paths = [
            {"x1":0,"y1":0,"x2":1,"y2":0},
            {"x1":1,"y1":0,"x2":2,"y2":0},
            {"x1":2,"y1":0,"x2":2,"y2":1},
            {"x1":2,"y1":1,"x2":3,"y2":1},
            {"x1":3,"y1":1,"x2":3,"y2":2},

            # extra branches
            {"x1":1,"y1":0,"x2":1,"y2":1},
            {"x1":1,"y1":1,"x2":1,"y2":2},
            {"x1":0,"y1":0,"x2":0,"y2":1},  # dead end

            # extend maze right side
            {"x1":3,"y1":2,"x2":4,"y2":2},
            {"x1":4,"y1":2,"x2":5,"y2":2},
            {"x1":5,"y1":2,"x2":6,"y2":2},
            {"x1":6,"y1":2,"x2":6,"y2":3},  # branch up
            {"x1":6,"y1":3,"x2":6,"y2":4},  # deeper branch (dead end)

            # upper detours
            {"x1":2,"y1":0,"x2":3,"y2":0},
            {"x1":3,"y1":0,"x2":4,"y2":0},
            {"x1":4,"y1":0,"x2":4,"y2":1},
            {"x1":4,"y1":1,"x2":4,"y2":2},  # loop back to main

            # left deeper dead end
            {"x1":0,"y1":1,"x2":0,"y2":2},
            {"x1":0,"y1":2,"x2":0,"y2":3},  # deeper dead path

            # vertical corridor middle
            {"x1":3,"y1":2,"x2":3,"y2":3},
            {"x1":3,"y1":3,"x2":3,"y2":4},
            {"x1":3,"y1":4,"x2":4,"y2":4},
            {"x1":4,"y1":4,"x2":5,"y2":4},

            # connect toward bottom right
            {"x1":5,"y1":4,"x2":6,"y2":4},
            {"x1":6,"y1":4,"x2":7,"y2":4},
            {"x1":7,"y1":4,"x2":7,"y2":5},
            {"x1":7,"y1":5,"x2":7,"y2":6},
            {"x1":7,"y1":6,"x2":7,"y2":7},  # goal
        ]

    
    root = tk.Tk()
    root.title("A* Pathfinding with Animation")
    app = AStarGUI(root, available_paths)
    root.mainloop()
