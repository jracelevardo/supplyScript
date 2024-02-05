
import tkinter as tk
from tkinter import filedialog, END
import supp

class LexerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SupplyScript Lexer")
        self.root.geometry("600x400")


        self.bg_color = "#c3b091"  # pastel green
        self.button_color_run = "#add8e6"  # light blue
        self.button_color_select = "#ffff99"  # light yellow

        self.root.configure(bg=self.bg_color)

        # Title Label
        self.title_label = tk.Label(root, text="SupplyScript", font=('Franklin Gothic Demi Cond', 12), fg="#8B4513",
                                    bg=self.bg_color)
        self.title_label.grid(row=0, column=0, sticky='nw', padx=(10, 0))

        # Input Terminal
        self.input_label = tk.Label(root, text="Input", font=('Franklin Gothic Demi Cond', 12), bg=self.bg_color)
        self.input_label.grid(row=1, column=0, sticky='n')

        self.input_text = tk.Text(root, wrap="word", height=15, width=40, bg="white", fg="black",
                                  font=('Franklin Gothic Book', 10))
        self.input_text.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        # Output Terminal
        self.output_label = tk.Label(root, text="Output", font=('Franklin Gothic Demi Cond', 12), bg=self.bg_color)
        self.output_label.grid(row=1, column=1, sticky='n')

        self.output_text = tk.Text(root, wrap="word", height=15, width=40, state=tk.DISABLED, bg="white", fg="black",
                                   font=('Franklin Gothic Book', 10))
        self.output_text.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")

        # Buttons
        self.run_button = tk.Button(root, text="Run", command=self.run_lexer, bg=self.button_color_run,
                                    font=('Franklin Gothic Book', 10))
        self.run_button.grid(row=3, column=0, pady=5, padx=(10, 5), sticky='ew')

        self.select_file_button = tk.Button(root, text="Select File", command=self.select_file,
                                            bg=self.button_color_select, font=('Franklin Gothic Book', 10))
        self.select_file_button.grid(row=3, column=1, pady=5, padx=(5, 10), sticky='ew')

        # row and column expansion
        root.rowconfigure(2, weight=1)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

    def run_lexer(self):
        input_code = self.input_text.get("1.0", tk.END)

        try:
            result, error = supp.run_from_code(input_code)

            # Clear existing content
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)

            if error:
                self.output_text.insert(tk.END, f"Error: {error}\n")
            else:
                for token in result:
                    self.output_text.insert(tk.END, f"{token}\n")

                self.output_text.insert(tk.END, f"\nOutput saved to: symbol_table.txt\n")
            
            self.output_text.config(state=tk.DISABLED)

        except Exception as e:
            self.output_text.insert(tk.END, f"An error occurred: {str(e)}\n")


    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("SupplyScript files", "*.supp")])
        if file_path:
            with open(file_path, 'r') as file:
                file_content = file.read()
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert(tk.END, file_content)

if __name__ == "__main__":
    root = tk.Tk()
    app = LexerApp(root)
    root.mainloop()