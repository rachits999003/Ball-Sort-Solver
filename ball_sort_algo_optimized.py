import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import random
from copy import deepcopy
import time

class BallSortPuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ball Sort Puzzle Solver")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Define default colors
        self.default_colors = {
            'r': '#FF5555',  # red
            'g': '#55AA55',  # green
            'b': '#5555FF',  # blue
            'y': '#FFFF55',  # yellow
            'p': '#FF55FF',  # purple
            'c': '#55FFFF',  # cyan
            'o': '#FFA500',  # orange
            'm': '#AA55AA',  # magenta
        }
        
        # Store current colors (can be customized by user)
        self.colors = self.default_colors.copy()
        
        # Game state variables
        self.numberOfStacks = 6
        self.stackHeight = 4
        self.stacks = ["gbbb", "ybry", "yggy", "rrrg", "", ""]
        self.grid = []
        self.selected_stack = None
        self.animation_speed = 500  # ms
        self.solution_steps = []
        self.current_step = 0
        self.is_animating = False
        
        # Create frames
        self.create_frames()
        
        # Create widgets
        self.create_control_panel()
        self.create_visualization_area()
        self.create_solution_controls()
        
        # Initialize the grid
        self.initialize_grid()
        self.draw_stacks()
    
    def create_frames(self):
        # Main layout frames
        self.control_frame = tk.Frame(self.root, bg="#e0e0e0", padx=10, pady=10)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.right_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.visualization_frame = tk.Frame(self.right_frame, bg="#f0f0f0", padx=10, pady=10)
        self.visualization_frame.pack(fill=tk.BOTH, expand=True)
        
        self.solution_frame = tk.Frame(self.right_frame, bg="#e8e8e8", padx=10, pady=10, height=100)
        self.solution_frame.pack(fill=tk.X, side=tk.BOTTOM)
    
    def create_control_panel(self):
        # Title
        title_label = tk.Label(self.control_frame, text="Ball Sort Puzzle", font=("Arial", 16, "bold"), bg="#e0e0e0")
        title_label.pack(pady=(0, 15))
        
        # Number of stacks
        stack_frame = tk.Frame(self.control_frame, bg="#e0e0e0")
        stack_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(stack_frame, text="Number of Stacks:", bg="#e0e0e0").pack(side=tk.LEFT)
        self.stack_var = tk.IntVar(value=self.numberOfStacks)
        stack_spin = ttk.Spinbox(stack_frame, from_=3, to=12, width=5, textvariable=self.stack_var)
        stack_spin.pack(side=tk.RIGHT)
        
        # Stack height
        height_frame = tk.Frame(self.control_frame, bg="#e0e0e0")
        height_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(height_frame, text="Stack Height:", bg="#e0e0e0").pack(side=tk.LEFT)
        self.height_var = tk.IntVar(value=self.stackHeight)
        height_spin = ttk.Spinbox(height_frame, from_=2, to=8, width=5, textvariable=self.height_var)
        height_spin.pack(side=tk.RIGHT)
        
        # Animation speed
        speed_frame = tk.Frame(self.control_frame, bg="#e0e0e0")
        speed_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(speed_frame, text="Animation Speed:", bg="#e0e0e0").pack(side=tk.LEFT)
        self.speed_scale = ttk.Scale(speed_frame, from_=50, to=1000, value=self.animation_speed, 
                                    orient=tk.HORIZONTAL, length=150,
                                    command=lambda val: self.update_speed(float(val)))
        self.speed_scale.pack(side=tk.RIGHT)
        
        # Color customization
        color_label = tk.Label(self.control_frame, text="Customize Colors:", font=("Arial", 12), bg="#e0e0e0")
        color_label.pack(pady=(15, 5), anchor=tk.W)
        
        self.color_buttons_frame = tk.Frame(self.control_frame, bg="#e0e0e0")
        self.color_buttons_frame.pack(fill=tk.X, pady=5)
        
        self.create_color_buttons()
        
        # Control buttons
        btn_frame = tk.Frame(self.control_frame, bg="#e0e0e0")
        btn_frame.pack(fill=tk.X, pady=(15, 5))
        
        self.new_puzzle_btn = tk.Button(btn_frame, text="New Random Puzzle", command=self.generate_random_puzzle)
        self.new_puzzle_btn.pack(fill=tk.X, pady=2)
        
        self.create_puzzle_btn = tk.Button(btn_frame, text="Create Custom Puzzle", command=self.open_puzzle_creator)
        self.create_puzzle_btn.pack(fill=tk.X, pady=2)
        
        self.reset_btn = tk.Button(btn_frame, text="Reset Current Puzzle", command=self.reset_puzzle)
        self.reset_btn.pack(fill=tk.X, pady=2)
        
        self.solve_btn = tk.Button(btn_frame, text="Solve Puzzle", command=self.solve_puzzle)
        self.solve_btn.pack(fill=tk.X, pady=2)
        
        # Help button
        help_btn = tk.Button(self.control_frame, text="Help", command=self.show_help)
        help_btn.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
    
    def create_color_buttons(self):
        # Clear existing color buttons
        for widget in self.color_buttons_frame.winfo_children():
            widget.destroy()
            
        # Create grid of color buttons
        row, col = 0, 0
        for color_char, color_hex in self.colors.items():
            btn_frame = tk.Frame(self.color_buttons_frame, bg="#e0e0e0", padx=2, pady=2)
            btn_frame.grid(row=row, column=col, padx=3, pady=3)
            
            color_btn = tk.Button(btn_frame, bg=color_hex, width=2, height=1,
                                 command=lambda c=color_char: self.change_color(c))
            color_btn.pack(side=tk.LEFT)
            
            tk.Label(btn_frame, text=color_char, bg="#e0e0e0", width=1).pack(side=tk.RIGHT)
            
            col += 1
            if col > 3:  # 4 buttons per row
                col = 0
                row += 1
                
        # Reset colors button
        reset_colors_btn = tk.Button(self.color_buttons_frame, text="Reset Colors", 
                                     command=self.reset_colors)
        reset_colors_btn.grid(row=row+1, column=0, columnspan=4, pady=(5, 0), sticky=tk.EW)
    
    def create_visualization_area(self):
        self.canvas = tk.Canvas(self.visualization_frame, bg="white", height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind click event to the canvas
        self.canvas.bind("<Button-1>", self.on_stack_click)
    
    def create_solution_controls(self):
        # Status label
        self.status_label = tk.Label(self.solution_frame, text="Ready", bg="#e8e8e8", font=("Arial", 10))
        self.status_label.pack(pady=(0, 10))
        
        # Control buttons
        buttons_frame = tk.Frame(self.solution_frame, bg="#e8e8e8")
        buttons_frame.pack()
        
        self.prev_btn = tk.Button(buttons_frame, text="⏮ Previous", state=tk.DISABLED, 
                                command=self.previous_step)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.play_btn = tk.Button(buttons_frame, text="▶ Play", state=tk.DISABLED, 
                                command=self.play_solution)
        self.play_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = tk.Button(buttons_frame, text="⏸ Pause", state=tk.DISABLED, 
                                 command=self.pause_solution)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = tk.Button(buttons_frame, text="Next ⏭", state=tk.DISABLED, 
                                command=self.next_step)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        # Step counter
        self.step_counter = tk.Label(self.solution_frame, text="Step: 0/0", bg="#e8e8e8")
        self.step_counter.pack(pady=5)
    
    def initialize_grid(self):
        self.grid = []
        self.stackHeight = self.height_var.get()
        self.numberOfStacks = self.stack_var.get()
        
        # Create grid from stacks
        for i in range(min(len(self.stacks), self.numberOfStacks)):
            self.grid.append(self.stacks[i])
        
        # Add additional empty stacks if needed
        while len(self.grid) < self.numberOfStacks:
            self.grid.append("")
    
    def draw_stacks(self):
        self.canvas.delete("all")
        
        # Calculate dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:  # Canvas not yet fully initialized
            self.root.after(100, self.draw_stacks)
            return
            
        stack_width = min(80, (canvas_width - 40) // self.numberOfStacks)
        ball_radius = stack_width // 2 - 2
        spacing = (canvas_width - (stack_width * self.numberOfStacks)) // (self.numberOfStacks + 1)
        
        max_stack_height = self.stackHeight + 1  # +1 for some padding
        tube_height = max_stack_height * (ball_radius * 2 + 2)
        
        # Draw tubes
        for i in range(self.numberOfStacks):
            x1 = spacing + i * (stack_width + spacing)
            y1 = (canvas_height - tube_height) // 2
            x2 = x1 + stack_width
            y2 = y1 + tube_height
            
            # Draw tube outline
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="#888", width=2, fill="#f8f8f8")
            
            # Draw tube bottom (rounded)
            self.canvas.create_arc(x1, y2-stack_width, x2, y2, 
                                  start=0, extent=180, outline="#888", width=2, fill="#f8f8f8")
            
            # Draw stack number
            self.canvas.create_text(x1 + stack_width//2, y2 + 20, 
                                   text=str(i+1), font=("Arial", 12))
            
            # Draw selection indicator if this stack is selected
            if i == self.selected_stack:
                self.canvas.create_rectangle(x1-3, y1-25, x2+3, y1-5, 
                                           fill="#ffcc00", outline="#ff8800", width=2)
                self.canvas.create_text(x1 + stack_width//2, y1-15, 
                                      text="Selected", font=("Arial", 8))
            
            # Draw balls in this stack
            stack = self.grid[i]
            for j, ball in enumerate(stack):
                ball_y = y2 - (j+1) * (ball_radius*2 + 2)
                self.draw_ball(x1 + stack_width//2, ball_y, ball_radius, ball)
    
    def draw_ball(self, x, y, radius, color_char):
        # Get the color for this ball
        color = self.colors.get(color_char, "#999999")  # Default gray if color not found
        
        # Draw the ball
        self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
                               fill=color, outline="#000000", width=1)
        
        # Draw the letter inside the ball
        self.canvas.create_text(x, y, text=color_char, font=("Arial", int(radius*0.8)))
    
    def on_stack_click(self, event):
        if self.is_animating:
            return
            
        # Calculate which stack was clicked
        canvas_width = self.canvas.winfo_width()
        stack_width = min(80, (canvas_width - 40) // self.numberOfStacks)
        spacing = (canvas_width - (stack_width * self.numberOfStacks)) // (self.numberOfStacks + 1)
        
        for i in range(self.numberOfStacks):
            x1 = spacing + i * (stack_width + spacing)
            x2 = x1 + stack_width
            
            if x1 <= event.x <= x2:
                # This stack was clicked
                if self.selected_stack is None:
                    # Select this stack
                    self.selected_stack = i
                else:
                    # Try to move from selected stack to this stack
                    if self.selected_stack != i:
                        self.try_move(self.selected_stack, i)
                    # Deselect in any case
                    self.selected_stack = None
                
                self.draw_stacks()
                break
    
    def try_move(self, from_stack, to_stack):
        move_count = self.count_movable_balls(self.grid[from_stack], self.grid[to_stack], self.stackHeight)
        if move_count == 0:
            messagebox.showinfo("Invalid Move", "This move is not allowed!")
            return False
        
        # Move the balls
        balls_to_move = self.grid[from_stack][-move_count:]
        self.grid[to_stack] += balls_to_move  # Add the balls
        self.grid[from_stack] = self.grid[from_stack][:-move_count]  # Remove the balls
        
        # Check if puzzle is solved
        if self.is_solved(self.grid, self.stackHeight):
            self.draw_stacks()
            messagebox.showinfo("Congratulations!", "You solved the puzzle!")
        
        return True
    
    def update_speed(self, value):
        self.animation_speed = value
    
    def change_color(self, color_char):
        current_color = self.colors.get(color_char, "#999999")
        new_color = colorchooser.askcolor(color=current_color, title=f"Choose color for '{color_char}'")
        
        if new_color[1]:  # If a color was selected (not canceled)
            self.colors[color_char] = new_color[1]
            self.create_color_buttons()  # Refresh color buttons
            self.draw_stacks()  # Redraw stacks with new colors
    
    def reset_colors(self):
        self.colors = self.default_colors.copy()
        self.create_color_buttons()
        self.draw_stacks()
    
    def generate_random_puzzle(self):
        if self.is_animating:
            self.pause_solution()
        
        # Reset solution
        self.solution_steps = []
        self.current_step = 0
        self.update_solution_controls()
        
        # Get configuration
        num_stacks = self.stack_var.get()
        stack_height = self.height_var.get()
        
        # Need at least 2 empty tubes
        filled_stacks = num_stacks - 2
        
        # Create colors
        available_colors = list(self.colors.keys())
        if filled_stacks > len(available_colors):
            messagebox.showinfo("Warning", f"Only {len(available_colors)} colors available. Some colors will be reused.")
        
        # Create balls (stack_height of each color)
        balls = []
        for i in range(filled_stacks):
            color = available_colors[i % len(available_colors)]
            balls.extend([color] * stack_height)
        
        # Shuffle balls
        random.shuffle(balls)
        
        # Create stacks
        self.stacks = []
        for i in range(filled_stacks):
            start_idx = i * stack_height
            end_idx = (i + 1) * stack_height
            self.stacks.append(''.join(balls[start_idx:end_idx]))
        
        # Add empty stacks
        for _ in range(num_stacks - filled_stacks):
            self.stacks.append("")
        
        # Initialize and draw
        self.initialize_grid()
        self.draw_stacks()
        
        # Update status
        self.status_label.config(text="New puzzle generated")
    
    def reset_puzzle(self):
        if self.is_animating:
            self.pause_solution()
            
        # Reset solution
        self.solution_steps = []
        self.current_step = 0
        self.update_solution_controls()
        
        # Reset grid to initial state
        self.initialize_grid()
        self.selected_stack = None
        self.draw_stacks()
        
        # Update status
        self.status_label.config(text="Puzzle reset")
    
    def solve_puzzle(self):
        # Check if grid is valid
        if not self.check_grid(self.grid):
            messagebox.showinfo("Invalid Puzzle", "This puzzle configuration is invalid!")
            return
        
        if self.is_solved(self.grid, self.stackHeight):
            messagebox.showinfo("Already Solved", "This puzzle is already solved!")
            return
        
        self.status_label.config(text="Solving puzzle...")
        self.root.update()
        
        # Reset solution
        self.solution_steps = []
        answer_mod = []
        visited = set()
        
        # Make a copy of the grid for solving
        grid_copy = deepcopy(self.grid)
        
        # Solve the puzzle
        if self.solve_puzzle_algorithm(grid_copy, self.stackHeight, visited, answer_mod):
            # Process solution
            answer_mod.reverse()
            self.solution_steps = answer_mod
            self.current_step = 0
            
            # Update controls
            self.update_solution_controls()
            self.status_label.config(text=f"Solution found! {len(self.solution_steps)} moves")
            
            # Enable solution controls
            self.play_btn.config(state=tk.NORMAL)
            self.next_btn.config(state=tk.NORMAL)
        else:
            messagebox.showinfo("No Solution", "Could not find a solution for this puzzle!")
            self.status_label.config(text="No solution found")
    
    def play_solution(self):
        if not self.solution_steps:
            return
            
        self.is_animating = True
        self.play_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        
        # Start animation
        self.animate_solution()
    
    def animate_solution(self):
        if not self.is_animating or self.current_step >= len(self.solution_steps):
            self.is_animating = False
            self.pause_btn.config(state=tk.DISABLED)
            return
            
        # Get current move
        move = self.solution_steps[self.current_step]
        from_stack, to_stack, ball_count = move
        
        # Display move
        self.status_label.config(text=f"Moving {ball_count} ball(s) from stack {from_stack+1} to stack {to_stack+1}")
        
        # Perform the move
        balls_to_move = self.grid[from_stack][-ball_count:]
        self.grid[to_stack] += balls_to_move
        self.grid[from_stack] = self.grid[from_stack][:-ball_count]
        
        # Update display
        self.draw_stacks()
        self.current_step += 1
        self.step_counter.config(text=f"Step: {self.current_step}/{len(self.solution_steps)}")
        
        # Update button states
        self.update_solution_controls()
        
        # Schedule next animation step
        if self.is_animating and self.current_step < len(self.solution_steps):
            self.root.after(int(self.animation_speed), self.animate_solution)
    
    def pause_solution(self):
        self.is_animating = False
        self.play_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
    
    def next_step(self):
        if not self.solution_steps or self.current_step >= len(self.solution_steps):
            return
            
        # Get current move
        move = self.solution_steps[self.current_step]
        from_stack, to_stack, ball_count = move
        
        # Display move
        self.status_label.config(text=f"Moving {ball_count} ball(s) from stack {from_stack+1} to stack {to_stack+1}")
        
        # Perform the move
        balls_to_move = self.grid[from_stack][-ball_count:]
        self.grid[to_stack] += balls_to_move
        self.grid[from_stack] = self.grid[from_stack][:-ball_count]
        
        # Update display
        self.draw_stacks()
        self.current_step += 1
        self.step_counter.config(text=f"Step: {self.current_step}/{len(self.solution_steps)}")
        
        # Update button states
        self.update_solution_controls()
    
    def previous_step(self):
        if not self.solution_steps or self.current_step <= 0:
            return
            
        # Reset to beginning and replay until the previous step
        self.initialize_grid()
        original_step = self.current_step - 1
        self.current_step = 0
        
        for step in range(original_step):
            move = self.solution_steps[step]
            from_stack, to_stack, ball_count = move
            
            # Perform the move
            balls_to_move = self.grid[from_stack][-ball_count:]
            self.grid[to_stack] += balls_to_move
            self.grid[from_stack] = self.grid[from_stack][:-ball_count]
        
        # Update display
        self.status_label.config(text=f"Moved back to step {original_step}")
        self.draw_stacks()
        self.current_step = original_step
        self.step_counter.config(text=f"Step: {self.current_step}/{len(self.solution_steps)}")
        
        # Update button states
        self.update_solution_controls()
    
    def update_solution_controls(self):
        # Update step counter
        total_steps = len(self.solution_steps)
        self.step_counter.config(text=f"Step: {self.current_step}/{total_steps}")
        
        # Update button states
        if total_steps == 0:
            state = tk.DISABLED
            self.prev_btn.config(state=state)
            self.play_btn.config(state=state)
            self.pause_btn.config(state=state)
            self.next_btn.config(state=state)
        else:
            # Previous button
            self.prev_btn.config(state=tk.NORMAL if self.current_step > 0 else tk.DISABLED)
            
            # Next button
            self.next_btn.config(state=tk.NORMAL if self.current_step < total_steps else tk.DISABLED)
            
            # Play button
            play_state = tk.NORMAL if self.current_step < total_steps and not self.is_animating else tk.DISABLED
            self.play_btn.config(state=play_state)
            
            # Pause button
            self.pause_btn.config(state=tk.NORMAL if self.is_animating else tk.DISABLED)
    
    def open_puzzle_creator(self):
        if self.is_animating:
            self.pause_solution()
        
        # Create a new toplevel window
        creator_window = tk.Toplevel(self.root)
        creator_window.title("Custom Puzzle Creator")
        creator_window.geometry("800x600")
        creator_window.configure(bg="#f0f0f0")
        creator_window.transient(self.root)  # Make it modal
        
        # Main frames
        top_frame = tk.Frame(creator_window, bg="#f0f0f0", padx=10, pady=10)
        top_frame.pack(fill=tk.X)
        
        canvas_frame = tk.Frame(creator_window, bg="white", padx=10, pady=10)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        bottom_frame = tk.Frame(creator_window, bg="#e0e0e0", padx=10, pady=10)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Configuration options in top frame
        config_frame = tk.Frame(top_frame, bg="#f0f0f0")
        config_frame.pack(side=tk.LEFT)
        
        # Number of stacks
        stack_frame = tk.Frame(config_frame, bg="#f0f0f0")
        stack_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(stack_frame, text="Number of Stacks:", bg="#f0f0f0").pack(side=tk.LEFT)
        creator_stack_var = tk.IntVar(value=self.numberOfStacks)
        stack_spin = ttk.Spinbox(stack_frame, from_=3, to=12, width=5, textvariable=creator_stack_var)
        stack_spin.pack(side=tk.LEFT, padx=5)
        
        # Stack height
        height_frame = tk.Frame(config_frame, bg="#f0f0f0")
        height_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(height_frame, text="Stack Height:", bg="#f0f0f0").pack(side=tk.LEFT)
        creator_height_var = tk.IntVar(value=self.stackHeight)
        height_spin = ttk.Spinbox(height_frame, from_=2, to=8, width=5, textvariable=creator_height_var)
        height_spin.pack(side=tk.LEFT, padx=5)
        
        # Update button
        update_btn = tk.Button(config_frame, text="Update Grid", 
                               command=lambda: update_creator_grid(creator_stack_var.get(), creator_height_var.get()))
        update_btn.pack(pady=5)
        
        # Color selection frame
        color_frame = tk.Frame(top_frame, bg="#f0f0f0")
        color_frame.pack(side=tk.RIGHT, padx=20)
        
        tk.Label(color_frame, text="Selected Color:", bg="#f0f0f0").pack()
        
        # Color selection buttons
        color_buttons_frame = tk.Frame(color_frame, bg="#f0f0f0")
        color_buttons_frame.pack()
        
        # Selected color variable
        selected_color_var = tk.StringVar(value=list(self.colors.keys())[0])
        
        # Create radio buttons for each color
        for i, (color_char, color_hex) in enumerate(self.colors.items()):
            color_btn = tk.Frame(color_buttons_frame, bg="#f0f0f0")
            color_btn.grid(row=i//4, column=i%4, padx=3, pady=3)
            
            radio = tk.Radiobutton(color_btn, bg=color_hex, width=2, 
                                   variable=selected_color_var, value=color_char)
            radio.pack(side=tk.LEFT)
            
            tk.Label(color_btn, text=color_char, bg="#f0f0f0").pack(side=tk.RIGHT)
        
        # Canvas for puzzle creator
        creator_canvas = tk.Canvas(canvas_frame, bg="white")
        creator_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Store grid configuration
        creator_grid = []
        
        # Function to update the grid based on new configuration
        def update_creator_grid(num_stacks, stack_height):
            nonlocal creator_grid
            
            # Save current grid configuration if any
            current_config = []
            for stack in creator_grid:
                current_config.append(stack[:])
            
            # Create new grid with requested dimensions
            creator_grid = ["" for _ in range(num_stacks)]
            
            # Restore previous configuration where possible
            for i in range(min(len(current_config), len(creator_grid))):
                creator_grid[i] = current_config[i][:stack_height]
                # Draw the grid
            draw_creator_grid()
        
        # Function to draw the grid
        def draw_creator_grid():
            creator_canvas.delete("all")
            
            # Calculate dimensions
            canvas_width = creator_canvas.winfo_width()
            canvas_height = creator_canvas.winfo_height()
            
            if canvas_width <= 1:  # Canvas not yet fully initialized
                creator_window.after(100, draw_creator_grid)
                return
                
            num_stacks = len(creator_grid)
            stack_height = creator_height_var.get()
            
            stack_width = min(80, (canvas_width - 40) // num_stacks)
            ball_radius = stack_width // 2 - 2
            spacing = (canvas_width - (stack_width * num_stacks)) // (num_stacks + 1)
            
            max_stack_height = stack_height + 1  # +1 for some padding
            tube_height = max_stack_height * (ball_radius * 2 + 2)
            
            # Draw tubes
            for i in range(num_stacks):
                x1 = spacing + i * (stack_width + spacing)
                y1 = (canvas_height - tube_height) // 2
                x2 = x1 + stack_width
                y2 = y1 + tube_height
                
                # Draw tube outline
                creator_canvas.create_rectangle(x1, y1, x2, y2, outline="#888", width=2, fill="#f8f8f8")
                
                # Draw tube bottom (rounded)
                creator_canvas.create_arc(x1, y2-stack_width, x2, y2, 
                                      start=0, extent=180, outline="#888", width=2, fill="#f8f8f8")
                
                # Draw stack number
                creator_canvas.create_text(x1 + stack_width//2, y2 + 20, 
                                       text=str(i+1), font=("Arial", 12))
                
                # Draw balls in this stack
                stack = creator_grid[i]
                for j, ball in enumerate(stack):
                    ball_y = y2 - (j+1) * (ball_radius*2 + 2)
                    
                    # Get the color for this ball
                    color = self.colors.get(ball, "#999999")  # Default gray if color not found
                    
                    # Draw the ball
                    creator_canvas.create_oval(x1 + stack_width//2 - ball_radius, 
                                           ball_y - ball_radius, 
                                           x1 + stack_width//2 + ball_radius, 
                                           ball_y + ball_radius, 
                                           fill=color, outline="#000000", width=1, 
                                           tags=f"ball_{i}_{j}")
                    
                    # Draw the letter inside the ball
                    creator_canvas.create_text(x1 + stack_width//2, ball_y, 
                                           text=ball, font=("Arial", int(ball_radius*0.8)),
                                           tags=f"text_{i}_{j}")
                
                # Create clickable area for this tube
                creator_canvas.create_rectangle(x1, y1, x2, y2+stack_width//2, 
                                             fill="", outline="", 
                                             tags=f"tube_{i}")
        
        # Function to handle tube clicks
        def on_tube_click(event):
            # Find which tube was clicked
            clicked_items = creator_canvas.find_withtag("current")
            if not clicked_items:
                return
                
            clicked_item = clicked_items[0]
            tags = creator_canvas.gettags(clicked_item)
            
            for tag in tags:
                if tag.startswith("tube_"):
                    tube_idx = int(tag.split("_")[1])
                    
                    # Get current stack and its height
                    current_stack = creator_grid[tube_idx]
                    max_height = creator_height_var.get()
                    
                    # If stack is not full, add the selected color
                    if len(current_stack) < max_height:
                        selected_color = selected_color_var.get()
                        creator_grid[tube_idx] += selected_color
                    # If stack has balls, remove the top one
                    elif len(current_stack) > 0:
                        creator_grid[tube_idx] = current_stack[:-1]
                    
                    # Redraw the grid
                    draw_creator_grid()
                    break
        
        # Bind click events
        creator_canvas.bind("<Button-1>", on_tube_click)
        
        # Add buttons to bottom frame
        clear_btn = tk.Button(bottom_frame, text="Clear All", 
                             command=lambda: [creator_grid.clear(), 
                                             creator_grid.extend(["" for _ in range(creator_stack_var.get())]), 
                                             draw_creator_grid()])
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        validate_btn = tk.Button(bottom_frame, text="Validate Puzzle", 
                               command=lambda: validate_puzzle())
        validate_btn.pack(side=tk.LEFT, padx=5)
        
        load_btn = tk.Button(bottom_frame, text="Load Current Puzzle", 
                           command=lambda: load_current_puzzle())
        load_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = tk.Button(bottom_frame, text="Save & Use This Puzzle", 
                           command=lambda: save_puzzle())
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        cancel_btn = tk.Button(bottom_frame, text="Cancel", 
                             command=creator_window.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        # Function to validate the puzzle
        def validate_puzzle():
            # Count total balls of each color
            color_counts = {}
            stack_height = creator_height_var.get()
            
            for stack in creator_grid:
                for ball in stack:
                    if ball:  # Skip empty slots
                        color_counts[ball] = color_counts.get(ball, 0) + 1
            
            # Check if each color has exactly stack_height balls
            valid = True
            error_message = ""
            
            if not color_counts:
                valid = False
                error_message = "Puzzle is empty! Add some balls."
            else:
                for color, count in color_counts.items():
                    if count != stack_height:
                        valid = False
                        error_message = f"Color '{color}' has {count} balls, but should have exactly {stack_height}."
                        break
            
            if valid:
                # Check if puzzle is already solved
                if self.is_solved(creator_grid, stack_height):
                    messagebox.showinfo("Validation", "Puzzle is valid but already solved!")
                else:
                    messagebox.showinfo("Validation", "Puzzle is valid!")
            else:
                messagebox.showerror("Validation Error", error_message)
            
            return valid
        
        # Function to load the current puzzle
        def load_current_puzzle():
            nonlocal creator_grid
            creator_grid = deepcopy(self.grid)
            creator_stack_var.set(len(self.grid))
            creator_height_var.set(self.stackHeight)
            draw_creator_grid()
        
        # Function to save the puzzle and use it
        def save_puzzle():
            if validate_puzzle():
                self.stacks = deepcopy(creator_grid)
                self.numberOfStacks = len(creator_grid)
                self.stackHeight = creator_height_var.get()
                self.stack_var.set(self.numberOfStacks)
                self.height_var.set(self.stackHeight)
                
                # Reset solution
                self.solution_steps = []
                self.current_step = 0
                self.update_solution_controls()
                
                # Update the main grid
                self.initialize_grid()
                self.selected_stack = None
                self.draw_stacks()
                
                # Close the creator window
                creator_window.destroy()
                
                # Update status
                self.status_label.config(text="Custom puzzle loaded")
        
        # Initialize the creator grid
        creator_grid = ["" for _ in range(creator_stack_var.get())]
        
        # Draw the initial grid after a short delay to let the window render
        creator_window.after(100, draw_creator_grid)
    
    def show_help(self):
        help_text = """
        Ball Sort Puzzle - Help
        
        Objective:
        Sort all the balls so that each tube contains balls of only one color.
        
        How to play:
        1. Click on a tube to select it (source).
        2. Click on another tube to move the top ball(s) from the source tube.
        
        Rules:
        - You can only move balls from the top of a tube.
        - You can only move balls to an empty tube or on top of a ball of the same color.
        - You can move multiple balls at once if they are the same color.
        
        Controls:
        - Click 'New Random Puzzle' to generate a new puzzle.
        - Click 'Create Custom Puzzle' to design your own puzzle.
        - Click 'Reset Current Puzzle' to start over.
        - Click 'Solve Puzzle' to find and animate a solution.
        - Use the solution controls to step through or animate the solution.
        
        Customize:
        - Adjust the number of tubes and stack height.
        - Click on color buttons to customize the colors.
        - Adjust the animation speed with the slider.
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("500x600")
        help_window.configure(bg="white")
        
        tk.Label(help_window, text="Ball Sort Puzzle - Help", font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        
        text_area = tk.Text(help_window, wrap=tk.WORD, bg="white", font=("Arial", 11))
        text_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        text_area.insert(tk.END, help_text)
        text_area.config(state=tk.DISABLED)
        
        close_btn = tk.Button(help_window, text="Close", command=help_window.destroy)
        close_btn.pack(pady=10)
    
    # Algorithm helper methods
    def is_solved(self, grid, stack_height):
        for stack in grid:
            # Empty stacks are ok
            if not stack:
                continue
                
            # If stack is not full, it's not solved
            if len(stack) != stack_height:
                return False
                
            # If not all balls are the same color, it's not solved
            first_color = stack[0]
            if any(ball != first_color for ball in stack):
                return False
        
        return True
    
    def check_grid(self, grid):
        # Count balls of each color
        color_counts = {}
        
        for stack in grid:
            for ball in stack:
                color_counts[ball] = color_counts.get(ball, 0) + 1
        
        # Check that each color has exactly stack_height balls
        stack_height = self.stackHeight
        for color, count in color_counts.items():
            if count != stack_height:
                return False
        
        return True
    
    def count_movable_balls(self, from_stack, to_stack, stack_height):
        # If source stack is empty, no balls can be moved
        if not from_stack:
            return 0
            
        # Get the top ball from source
        top_ball = from_stack[-1]
        
        # Count how many identical balls are at the top
        count = 0
        for i in range(len(from_stack)-1, -1, -1):
            if from_stack[i] == top_ball:
                count += 1
            else:
                break
        
        # If destination is empty, all identical balls can be moved
        if not to_stack:
            return count
            
        # If destination's top ball is different, no balls can be moved
        if to_stack[-1] != top_ball:
            return 0
            
        # If moving would exceed stack height, limit the count
        if len(to_stack) + count > stack_height:
            return stack_height - len(to_stack)
            
        return count
    
    
    def get_valid_moves(self, grid, stack_height):
        moves = []
        num_stacks = len(grid)

        for i in range(num_stacks):
            from_stack = grid[i]
            if not from_stack:
                continue

            top_ball = from_stack[-1]
            for j in range(num_stacks):
                if i == j:
                    continue
                to_stack = grid[j]

                # Prevent no-gain shuffling into empty tubes
                if not to_stack:
                    if len(set(from_stack)) == 1 and len(from_stack) == stack_height:
                        continue
                    if from_stack.count(top_ball) == 1:
                        continue

                # Skip if destination not compatible
                if to_stack and (to_stack[-1] != top_ball or len(to_stack) >= stack_height):
                    continue

                # Use count_movable_balls logic to determine move count
                move_count = self.count_movable_balls(from_stack, to_stack, stack_height)
                if move_count > 0:
                    moves.append((i, j, move_count))

        return moves



    def solve_puzzle_algorithm(self, grid, stack_height, visited, answer_mod):
        grid_str = '|'.join(''.join(stack) for stack in grid)
        if grid_str in visited:
            return False
        visited.add(grid_str)

        if self.is_solved(grid, stack_height):
            return True

        for from_idx, to_idx, move_count in self.get_valid_moves(grid, stack_height):
            balls_to_move = grid[from_idx][-move_count:]
            grid[to_idx] += balls_to_move
            grid[from_idx] = grid[from_idx][:-move_count]

            if self.solve_puzzle_algorithm(grid, stack_height, visited, answer_mod):
                answer_mod.append((from_idx, to_idx, move_count))
                return True

            # Undo
            grid[from_idx] += balls_to_move
            grid[to_idx] = grid[to_idx][:-move_count]

        return False
def main():
    root = tk.Tk()
    app = BallSortPuzzleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()