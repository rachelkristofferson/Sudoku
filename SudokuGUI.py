"""
Author: Rachel Kristofferson (GUI extension)
Date: 7/27/2024
Class: CSC115
Project: Final - Sudoku
File Name: SudokuGUI_fixed.py
Description: A beautiful Sudoku puzzle with GUI interface.
"""

import random
import tkinter as tk
from tkinter import messagebox, StringVar, ttk
from tkinter import font as tkfont

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.root.configure(bg="#fcfcfc")
        self.highlight_color = "#00AAFF"
        
        # Create custom fonts
        self.title_font = tkfont.Font(family="Arial", size=28, weight="bold")
        self.cell_font = tkfont.Font(family="Arial", size=16, weight="bold")
        self.button_font = tkfont.Font(family="Arial", size=12)
        self.pencil_font = tkfont.Font(family="Arial", size=8)
        self.num_button_font = tkfont.Font(family="Arial", size=16, weight="bold")
        
        # Set minimum window size
        self.root.minsize(600, 800)  # Larger minimum size
        
        # Game variables
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.selected_row = -1
        self.selected_col = -1
        self.original_cells = set()
        self.pencil_marks = {}
        
        # Track auto-pencil state
        self.auto_pencil_active = False
        self.auto_pencil_btn = None  # Will be assigned in the UI creation
        
        # Create UI and start a new game
        self.create_ui()
        self.new_game()
    
    # All button-referenced methods are defined FIRST to avoid reference issues
    
    def clear_cell(self):
        """Clear the selected cell"""
        # Check if a cell is selected
        if self.selected_row < 0 or self.selected_col < 0:
            return
        
        # Check if the cell is an original cell
        if (self.selected_row, self.selected_col) in self.original_cells:
            return
        
        # Clear the board
        self.board[self.selected_row][self.selected_col] = 0
        
        # Clear pencil marks
        self.pencil_marks[(self.selected_row, self.selected_col)] = set()
        
        # Update the display
        self.cell_buttons[self.selected_row][self.selected_col].config(
            text="",
            font=self.cell_font,
            bg="#00AAFF"  # Keep the highlight
        )
        
        # If auto-pencil is active, update pencil marks
        if self.auto_pencil_active:
            self.auto_pencil_marks()
    
    def clear_pencil_marks(self):
        """Clear all pencil marks for the selected cell"""
        # Check if a cell is selected
        if self.selected_row < 0 or self.selected_col < 0:
            return
        
        # Check if the cell is an original cell
        if (self.selected_row, self.selected_col) in self.original_cells:
            return
        
        # Clear pencil marks
        self.pencil_marks[(self.selected_row, self.selected_col)] = set()
        
        # Update the display
        if self.board[self.selected_row][self.selected_col] == 0:
            self.cell_buttons[self.selected_row][self.selected_col].config(
                text="",
                font=self.cell_font,
                bg="#00AAFF"  # Maintain highlight
            )
    
    def toggle_auto_pencil(self):
        """Toggle auto pencil marks on/off"""
        self.auto_pencil_active = not self.auto_pencil_active
        
        if self.auto_pencil_active:
            # Auto pencil is now active - apply it
            self.auto_pencil_btn.config(bg="#ADD8E6")  # Light blue background to show it's active
            self.auto_pencil_marks()
        else:
            # Auto pencil is now inactive - clear all pencil marks
            self.auto_pencil_btn.config(bg="white")  # Reset background
            self.clear_all_pencil_marks()
    
    def clear_all_pencil_marks(self):
        """Clear all pencil marks from the board"""
        for row in range(9):
            for col in range(9):
                # Skip filled cells
                if self.board[row][col] != 0:
                    continue
                
                # Clear pencil marks
                self.pencil_marks[(row, col)] = set()
                
                # Update display
                self.cell_buttons[row][col].config(
                    text="",
                    font=self.cell_font,
                    bg="#00AAFF" if (row == self.selected_row and col == self.selected_col) else "white"
                )
    
    def auto_pencil_marks(self):
        """Automatically fill in all possible pencil marks for empty cells"""
        # Process all cells
        for row in range(9):
            for col in range(9):
                # Skip filled or original cells
                if self.board[row][col] != 0:
                    continue
                
                # Clear existing pencil marks
                self.pencil_marks[(row, col)] = set()
                
                # Find all valid numbers
                valid_nums = set()
                for num in range(1, 10):
                    if self.is_valid_placement(self.board, row, col, num):
                        valid_nums.add(num)
                
                # Update the display
                if valid_nums:
                    # Format pencil marks in a 3x3 grid
                    text = ""
                    for i in range(1, 10):
                        if i in valid_nums:
                            text += str(i)
                        else:
                            text += " "
                        
                        if i % 3 == 0 and i < 9:
                            text += "\n"
                        elif i % 3 != 0:
                            text += " "
                    
                    # Keep highlight for currently selected cell
                    bg_color = "#00AAFF" if (row == self.selected_row and col == self.selected_col) else "white"
                    
                    self.cell_buttons[row][col].config(
                        text=text,
                        font=self.pencil_font,
                        fg="#757575",
                        bg=bg_color
                    )
                
                # Store the marks
                self.pencil_marks[(row, col)] = valid_nums
    
    def check_solution(self):
        """Check if the current board state is correct"""
        # Check if the board is filled
        if not self.is_board_filled():
            messagebox.showinfo("Not Complete", "The board is not completely filled yet.")
            return
        
        # Check if the solution is valid
        if self.is_board_valid():
            messagebox.showinfo("Congratulations!", "Your solution is correct!")
        else:
            messagebox.showerror("Incorrect", "Your solution is not valid. Check for errors.")
    
    def new_game(self):
        """Start a new game with the selected difficulty"""
        # Reset variables
        self.selected_row = -1
        self.selected_col = -1
        self.original_cells = set()
        
        # Reset auto-pencil state
        self.auto_pencil_active = False
        if self.auto_pencil_btn:
            self.auto_pencil_btn.config(bg="white")
        
        # Clear all cells and pencil marks
        for row in range(9):
            for col in range(9):
                self.cell_buttons[row][col].config(text="", bg="white", fg="#333333", font=self.cell_font)
                self.pencil_marks[(row, col)] = set()
        
        # Generate a new puzzle
        self.generate_puzzle()
        
        # Update the display
        self.update_display()
    
    def maintain_highlight(self, row, col):
        """Force highlight to remain after button release"""
        if row == self.selected_row and col == self.selected_col:
            self.cell_buttons[row][col].config(bg="#00AAFF")
            # Schedule another check to make sure highlight stays
            self.root.after(50, lambda: self.cell_buttons[row][col].config(bg="#00AAFF"))
    
    def select_cell(self, row, col):
        """Handles cell selection, applying highlight and tracking the active cell"""
        # Reset all cells to white
        for r in range(9):
            for c in range(9):
                self.cell_buttons[r][c].config(bg="white")

        # Highlight the selected cell
        self.cell_buttons[row][col].config(bg="#00AAFF")

        # Store the currently selected cell
        self.selected_cell = (row, col)
            
        
    def place_number(self, num):
        """Place a number in the selected cell"""
        # Check if a cell is selected
        if self.selected_row < 0 or self.selected_col < 0:
            return
        
        # Remember the selected position
        row, col = self.selected_row, self.selected_col
        
        # Check if the cell is an original cell
        if (row, col) in self.original_cells:
            return
        
        # Handle different input modes
        if self.input_mode.get() == "pencil":
            self.toggle_pencil_mark(num)
            
            # 🔹 Ensure the cell stays highlighted even when adding a pencil mark
            self.cell_buttons[row][col].config(bg="#00AAFF")
            return
        
        # Check if the move is valid
        if self.is_valid_placement(self.board, row, col, num):
            # Update the board
            self.board[row][col] = num
            
            # Update the display - KEEP HIGHLIGHT
            self.cell_buttons[row][col].config(
                text=str(num),
                font=self.cell_font,
                fg="#333333",
                bg="#00AAFF"  # Keep highlight color after placing a number
            )
            
            # Clear any pencil marks
            self.pencil_marks[(row, col)] = set()
            
            # If auto-pencil is active, update pencil marks
            if self.auto_pencil_active:
                self.auto_pencil_marks()
                
                # Re-highlight the selected cell after auto-pencil update
                self.cell_buttons[row][col].config(bg="#00AAFF")
            
            # Check if the board is solved
            if self.is_board_filled() and self.is_board_valid():
                messagebox.showinfo("Congratulations!", "You've solved the puzzle!")
        else:
            messagebox.showerror("Error", "Invalid move! Try another number.")
            
            # 🔹Ensure the highlight stays even after an invalid move
            self.cell_buttons[row][col].config(bg="#00AAFF")

    def toggle_pencil_mark(self, num):
        """Toggle a pencil mark in the selected cell"""
        # Check if a cell is selected
        if self.selected_row < 0 or self.selected_col < 0:
            return
        
        # Check if the cell is an original cell or has a value
        if ((self.selected_row, self.selected_col) in self.original_cells or
            self.board[self.selected_row][self.selected_col] != 0):
            return
        
        # Toggle the pencil mark
        pos = (self.selected_row, self.selected_col)
        
        # Get current pencil marks
        marks = self.pencil_marks[pos]
        
        # Toggle the mark
        if num in marks:
            marks.remove(num)
        else:
            marks.add(num)
        
        # Update the display
        if marks:
            # Format pencil marks in a 3x3 grid
            text = ""
            for i in range(1, 10):
                if i in marks:
                    text += str(i)
                else:
                    text += " "
                
                if i % 3 == 0 and i < 9:
                    text += "\n"
                elif i % 3 != 0:
                    text += " "
            
            self.cell_buttons[self.selected_row][self.selected_col].config(
                text=text,
                font=self.pencil_font,
                fg="#757575",
                bg="#00AAFF"  # Maintain highlight
            )
        else:
            self.cell_buttons[self.selected_row][self.selected_col].config(
                text="",
                font=self.cell_font,
                bg="#00AAFF"  # Maintain highlight
            )

    # Main UI creation method
    def create_ui(self):
        """Create the complete user interface"""
        # Create main container with padding
        container = tk.Frame(self.root, bg="#fcfcfc", padx=30, pady=30)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Create title
        title_label = tk.Label(
            container, 
            text="SUDOKU", 
            font=self.title_font,
            fg="#333333",
            bg="#fcfcfc"
        )
        title_label.pack(pady=(0, 20))
        
        # Create header frame
        header_frame = tk.Frame(container, bg="#fcfcfc")
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Difficulty selection
        diff_frame = tk.Frame(header_frame, bg="#fcfcfc")
        diff_frame.pack(side=tk.LEFT)
        
        tk.Label(
            diff_frame,
            text="Difficulty:",
            font=self.button_font,
            bg="#fcfcfc",
            fg="#333333"
        ).pack(side=tk.LEFT, padx=5)
        
        # Style for combobox
        style = ttk.Style()
        style.configure("TCombobox", 
                        fieldbackground="white",
                        background="white")
        
        self.difficulty = StringVar(self.root)
        self.difficulty.set("easy")
        diff_combo = ttk.Combobox(
            diff_frame,
            textvariable=self.difficulty,
            values=["easy", "medium", "hard"],
            width=8,
            state="readonly",
            font=self.button_font
        )
        diff_combo.pack(side=tk.LEFT, padx=5)
        
        # Start button
        start_button = tk.Button(
            header_frame,
            text="New Game",
            font=self.button_font,
            bg="white",
            fg="black",
            padx=15,
            pady=5,
            relief=tk.FLAT,
            borderwidth=0,
            command=self.new_game
        )
        start_button.pack(side=tk.RIGHT)
        
        # Game board container
        board_container = tk.Frame(container, bg="#fcfcfc")
        board_container.pack(pady=10)
        
        # Create board
        board_frame = tk.Frame(board_container, bg="#333333", padx=1, pady=1)
        board_frame.pack()
        
        # Create 3x3 boxes
        self.box_frames = {}
        for box_row in range(3):
            for box_col in range(3):
                box_frame = tk.Frame(
                    board_frame,
                    bg="#333333",
                    padx=1,
                    pady=1,
                    highlightbackground="#333333",
                    highlightthickness=1
                )
                box_frame.grid(row=box_row, column=box_col, padx=0, pady=0)
                self.box_frames[(box_row, box_col)] = box_frame
        
        # Create cells
        self.cell_buttons = [[None for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                # Calculate box position
                box_row, box_col = row // 3, col // 3
                inner_row, inner_col = row % 3, col % 3
                
                # Create cell frame
                cell_frame = tk.Frame(
                    self.box_frames[(box_row, box_col)],
                    width=46,
                    height=46,
                    bg="white",
                    
                )
                cell_frame.grid(row=inner_row, column=inner_col)
                cell_frame.grid_propagate(False)
                
                # Use a Button with explicit background control
                button = tk.Button(
                    cell_frame,
                    text="",
                    font=self.cell_font,
                    bg="white",  # Default white background
                    fg="#333333",
                    relief=tk.FLAT,
                    borderwidth=0,
                    highlightcolor="#00AAFF",  # Highlight color
                    activebackground="#00AAFF",  # Color when active
                    command=lambda r=row, c=col: self.select_cell(r, c)
                )
                button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=45, height=45)
                
                # Bind mouse click to ensure selection
                button.bind("<Button-1>", lambda event, r=row, c=col: self.select_cell(r, c))
                
                self.cell_buttons[row][col] = button
                
                # Initialize pencil marks
                self.pencil_marks[(row, col)] = set()

        # Create bottom controls with fixed height
        bottom_part = tk.Frame(container, bg="#fcfcfc", height=250)
        bottom_part.pack(fill=tk.X, pady=5) 
        bottom_part.pack_propagate(False)  # Prevent shrinking
        
        # Mode selection with reduced padding
        mode_frame = tk.Frame(bottom_part, bg="#fcfcfc")
        mode_frame.pack(pady=2, fill=tk.X)  # Reduced padding
        
        mode_label = tk.Label(
            mode_frame,
            text="Mode:",
            font=self.button_font,
            bg="#fcfcfc",
            fg="#333333"
        )
        mode_label.pack(side=tk.LEFT, padx=(0,5))
        
        self.input_mode = StringVar(value="normal")
        
        normal_radio = tk.Radiobutton(
            mode_frame,
            text="Normal",
            variable=self.input_mode,
            value="normal",
            bg="#fcfcfc",
            font=self.button_font,
            selectcolor="#e6f7ff"
        )
        normal_radio.pack(side=tk.LEFT, padx=5)
        
        pencil_radio = tk.Radiobutton(
            mode_frame,
            text="Pencil",
            variable=self.input_mode,
            value="pencil",
            bg="#fcfcfc",
            font=self.button_font,
            selectcolor="#e6f7ff"
        )
        pencil_radio.pack(side=tk.LEFT, padx=5)
        
        # Number buttons with reduced padding
        num_frame = tk.Frame(bottom_part, bg="#fcfcfc")
        num_frame.pack(pady=5)
        
        # Create a 3x3 grid of number buttons with reduced padding
        for num in range(1, 10):
            btn = tk.Button(
                num_frame,
                text=str(num),
                font=self.num_button_font,
                width=2,
                height=1,
                bg="white",
                fg="#333333",
                relief=tk.FLAT,
                borderwidth=0,
                command=lambda n=num: self.place_number(n)
            )
            btn.grid(row=(num-1)//3, column=(num-1)%3, padx=5, pady=5)  # Reduced padding
        
        # Action frame padding reduced
        action_frame = tk.Frame(bottom_part, bg="#fcfcfc", height=50)
        action_frame.pack(fill=tk.X, pady=5)
        action_frame.pack_propagate(False)  # Prevent collapsing
        
        # Button parameters - REDUCED HEIGHT
        button_width = 120
        button_height = 30
        padding = 10
        
        # Button positions
        window_width = 600 - 60  # Account for padding
        start_x = 30  # Start with some padding
        
        # Create action buttons with explicit positions - MOVED UP BY SETTING Y=5
        button_texts = ["Clear", "Clear Pencil", "Auto Pencil", "Check"]
        button_commands = [self.clear_cell, self.clear_pencil_marks, 
                            self.toggle_auto_pencil, self.check_solution]
        
        for i, (text, cmd) in enumerate(zip(button_texts, button_commands)):
            x_pos = start_x + i * (button_width + padding)
            btn = tk.Button(
                action_frame,
                text=text,
                font=self.button_font,
                bg="white",
                fg="black",
                relief=tk.FLAT,
                borderwidth=0,
                command=cmd
            )
            btn.place(x=x_pos, y=5, width=button_width, height=button_height)
            
            # Store the Auto Pencil button to change its appearance when toggled
            if text == "Auto Pencil":
                self.auto_pencil_btn = btn
        
        # Add keyboard bindings
        for i in range(1, 10):
            def key_handler(event, digit=i):
                self.place_number(digit)
            self.root.bind(str(i), key_handler)

    # Remaining game logic methods
    def generate_puzzle(self):
        """Generate a Sudoku puzzle with the given difficulty"""
        # Create a solved puzzle first
        self.generate_solved_board()
        
        # Save the solution
        self.solution = [row[:] for row in self.board]
        
        # Remove numbers based on difficulty
        cells_to_remove = {
            "easy": 40,
            "medium": 50,
            "hard": 55
        }.get(self.difficulty.get(), 40)
        
        # Get all positions
        positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(positions)
        
        # Try to remove cells
        removed = 0
        for row, col in positions:
            if removed >= cells_to_remove:
                break
                
            # Remember the value
            backup = self.board[row][col]
            self.board[row][col] = 0
            
            # Check if the puzzle still has a unique solution
            # For performance reasons, we only check every few cells
            if removed % 5 == 0:
                temp_board = [row[:] for row in self.board]
                if self.count_solutions(temp_board) == 1:
                    removed += 1
                else:
                    self.board[row][col] = backup
            else:
                removed += 1
        
        # Mark original cells
        self.original_cells = set()
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != 0:
                    self.original_cells.add((row, col))

    def generate_solved_board(self):
        """Generate a completely solved Sudoku board"""
        # Clear the board
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        
        # Fill the board using backtracking
        self.solve_board(self.board)

    def solve_board(self, board):
        """Solve the given board using backtracking"""
        # Find an empty cell
        empty_found = False
        row, col = 0, 0
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    row, col = r, c
                    empty_found = True
                    break
            if empty_found:
                break
        
        # If no empty cells, the board is solved
        if not empty_found:
            return True
        
        # Try digits 1-9 in random order
        digits = list(range(1, 10))
        random.shuffle(digits)
        for num in digits:
            # Check if the digit is valid
            if self.is_valid_placement(board, row, col, num):
                # Place the digit
                board[row][col] = num
                
                # Recursively solve the rest
                if self.solve_board(board):
                    return True
                
                # If that doesn't work, backtrack
                board[row][col] = 0
        
        # No solution found
        return False

    def count_solutions(self, board, limit=2):
        """Count the number of solutions up to the limit"""
        solutions = [0]  # Using a list to allow modification in nested function
        
        def backtrack():
            # Stop if we've reached the limit
            if solutions[0] >= limit:
                return
            
            # Find an empty cell
            empty_found = False
            row, col = 0, 0
            for r in range(9):
                for c in range(9):
                    if board[r][c] == 0:
                        row, col = r, c
                        empty_found = True
                        break
                if empty_found:
                    break
            
            # If no empty cells, we found a solution
            if not empty_found:
                solutions[0] += 1
                return
            
            # Try each digit
            for num in range(1, 10):
                if self.is_valid_placement(board, row, col, num):
                    # Place the digit
                    board[row][col] = num
                    
                    # Recursively count
                    backtrack()
                    
                    # Backtrack
                    board[row][col] = 0
        
        # Start counting
        backtrack()
        return solutions[0]

    def is_valid_placement(self, board, row, col, num):
        """Check if a number can be placed at a position"""
        # Check row
        for c in range(9):
            if board[row][c] == num:
                return False
        
        # Check column
        for r in range(9):
            if board[r][col] == num:
                return False
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if board[r][c] == num:
                    return False
        
        # If we get here, the placement is valid
        return True

    def update_display(self):
        """Update the display to match the current board state"""
        for row in range(9):
            for col in range(9):
                value = self.board[row][col]
                
                # Update cell text
                if value != 0:
                    self.cell_buttons[row][col].config(
                        text=str(value),
                        fg="#1565C0" if (row, col) in self.original_cells else "#333333"
                    )
                else:
                    self.cell_buttons[row][col].config(text="")

    def is_board_filled(self):
        """Check if the board is completely filled"""
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return False
        return True

    def is_board_valid(self):
        """Check if the current board state is valid"""
        # Check rows
        for row in range(9):
            if not self.is_unit_valid([self.board[row][col] for col in range(9)]):
                return False
        
        # Check columns
        for col in range(9):
            if not self.is_unit_valid([self.board[row][col] for row in range(9)]):
                return False
        
        # Check 3x3 boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box_values = []
                for r in range(box_row, box_row + 3):
                    for c in range(box_col, box_col + 3):
                        box_values.append(self.board[r][c])
                if not self.is_unit_valid(box_values):
                    return False
        
        return True

    def is_unit_valid(self, unit):
        """Check if a unit (row, column, or box) contains all numbers 1-9"""
        return sorted(unit) == list(range(1, 10))


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()