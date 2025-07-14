import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class ChatWindow:
    def __init__(self, title="EVA Chat", width=400, height=500, x_offset=1000, y_offset=100):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(f"{width}x{height}+{x_offset}+{y_offset}")
        self.window.resizable(False, False)

        # Create the chat area
        self.chat_area = ScrolledText(
            self.window,
            wrap=tk.WORD,
            font=("Consolas", 11),
            state=tk.DISABLED
        )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Keep window on top and hidden at start
        self.window.attributes("-topmost", True)
        self.window.withdraw()

    def show(self):
        """Make the chat window visible."""
        self.window.deiconify()

    def hide(self):
        """Hide the chat window."""
        self.window.withdraw()

    def add_message(self, sender, message):
        """Add a message to the chat window."""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def run(self):
        """Start the Tkinter main loop."""
        self.window.mainloop()
