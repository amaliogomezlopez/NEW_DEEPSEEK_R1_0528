import tkinter as tk

class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple Calculator")
        
        # Initialize variables
        self.current_value = "0"
        self.operation = None
        self.previous_value = 0
        
        # Create display screen
        self.display_frame = tk.Frame(self.root, height=100, width=400)
        self.display_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.display_label = tk.Label(
            self.display_frame,
            text=self.current_value,
            font=('Arial', 25),
            anchor='e',
            background='#f5f5f5'
        )
        self.display_label.pack(ipady=15, expand=True)

        # Create button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(expand=True, fill="both")

        # Define buttons with their respective columns and row configurations for proper sizing
        button_data = [
            ('7', 1), ('8', 1), ('9', 1),
            ('4', 1), ('5', 1), ('6', 1),
            ('1', 1), ('2', 1), ('3', 1),
            ('C', 0.5, 'clear'), ('.', 0.5), ('=', 1)
        ]
        
        # Create buttons with grid layout and configure column weights
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)

        row = 0
        col = 0
        
        # Buttons from top to bottom, left to right
        self.buttons = {}
        for btn in ['7', '8', '9', '/', 
                   '4', '5', '6', '*', 
                   '1', '2', '3', '-', 
                   'C', '.', '=', '+']:
            if col == 0:
                width_val = 1
            elif col == 1 and btn in ('.', '='):
                width_val = 2
            else:
                width_val = 1
                
            self.buttons[btn] = tk.Button(
                button_frame,
                text=btn,
                font=('Arial', 15),
                command=lambda x=btn: self.click(x)
            )
            
            # Configure row and column weights for uniform expansion
            if (row, col) not in [(0,3), (1,3)]:
                button_frame.grid_rowconfigure(row, weight=1)
                
            self.buttons[btn].grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            row += 1
            if row == 4:
                row = 0
                col = (col + 1) % 3

    def click(self, key):
        # Handle button presses and update the display accordingly
        current_value = self.current_value
        
        if key in ('+', '-', '*', '/'):
            if self.operation is None:
                self.operation = key
                self.previous_value = float(current_value)
                self.reset_screen()
            else:
                try:
                    result = eval(f"{self.previous_value}{self.operation}{current_value}")
                    self.display_label.config(text=str(result))
                    self.current_value = str(result)
                    self.operation = key
                    self.previous_value = result
                except Exception as e:
                    pass
                    
        elif key == '=' or key == 'Enter':
            try:
                if self.operation is None:
                    return  # No operation to calculate
                
                # Evaluate the expression and display the result
                result = eval(f"{self.previous_value}{self.operation}{current_value}")
                self.display_label.config(text=str(result))
                self.current_value = str(result)
                self.operation = None
            except Exception as e:
                self.display_label.config(text="Error")
                
        elif key == 'C':
            # Clear the display and reset state
            self.reset()
            
        else:  # digits or decimal point
            if current_value.startswith('0') and len(current_value) < 2:
                new_text = key
            else:
                new_text = current_value + str(key)
                
            self.current_value = new_text
            
    def reset(self):
        self.current_value = "0"
        self.operation = None
        self.previous_value = 0
        
# Create the application window and calculator instance
root = tk.Tk()
calc = Calculator()

# Start the Tkinter event loop
root.mainloop()