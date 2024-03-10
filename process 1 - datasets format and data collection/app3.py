import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.title("Scrollable Text Example")

    # Create a Text widget
    text = tk.Text(root, wrap="word", width=40, height=10)
    text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Create a Scrollbar widget
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=text.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Attach the scrollbar to the Text widget
    text.config(yscrollcommand=scrollbar.set)

    # Add some sample text to the Text widget
    sample_text = "This is a long sample text. " * 20
    text.insert("end", sample_text)

    # Make the Text widget resizable
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()
