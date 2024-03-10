import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.title("Long Webpage Example")

    # Create a Canvas widget to contain the frames
    canvas = tk.Canvas(root)
    canvas.pack(side="left", fill="both", expand=True)

    # Add a Frame to the Canvas
    frame1 = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame1, anchor="nw")

    # Add widgets to the first frame
    label1 = ttk.Label(frame1, text="Section 1", font=("Arial", 12, "bold"))
    label1.pack(pady=10)

    # Add more widgets to frame1 as needed

    # Add another Frame to the Canvas
    frame2 = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame2, anchor="nw")

    # Add widgets to the second frame
    label2 = ttk.Label(frame2, text="Section 2", font=("Arial", 12, "bold"))
    label2.pack(pady=10)

    # Add more widgets to frame2 as needed

    # Create vertical scrollbar for the Canvas
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the Canvas to scroll vertically with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Resize the Canvas scroll region when the window size changes
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.bind("<Configure>", on_configure)

    root.mainloop()

if __name__ == "__main__":
    main()
