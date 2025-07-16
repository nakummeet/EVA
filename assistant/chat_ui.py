import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import time
from assistant.gemini_chat import handle_gemini


class ChatWindow:
    def __init__(self, title="EVA Chat", width=420, height=580):
        self.window = tk.Tk()
        self.window.title(title)

        # Center the window
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_offset = (screen_width - width) // 2
        y_offset = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x_offset}+{y_offset}")
        self.window.configure(bg="#0f0f0f")
        self.window.resizable(False, False)

        # --- CHAT AREA ---
        self.chat_area = ScrolledText(
            self.window,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            state=tk.DISABLED,
            bg="#1c1c1c",
            fg="#e0e0e0",
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.chat_area.pack(padx=10, pady=(10, 5), fill=tk.BOTH, expand=True)
        self.chat_area.tag_configure("user", justify="right", foreground="#7dd3fc")
        self.chat_area.tag_configure("bot", justify="left", foreground="#fca5a5")
        self.chat_area.tag_configure("typing", justify="left", foreground="#9ca3af")

        # Typing animation
        self.typing = False
        self.typing_start_index = None

        # --- INPUT AREA ---
        self.input_frame = tk.Frame(self.window, bg="#0f0f0f")
        self.input_frame.pack(fill=tk.X, pady=(0, 10), padx=10)

        self.entry = tk.Entry(
            self.input_frame,
            font=("Segoe UI", 11),
            bg="#2a2a2a",
            fg="white",
            insertbackground="white",
            relief=tk.FLAT
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            self.input_frame,
            text="Send",
            command=self.send_message,
            bg="#c026d3",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            activebackground="#a21caf",
            activeforeground="white"
        )
        self.send_button.pack(side=tk.RIGHT)

        self.window.attributes("-topmost", True)
        self.window.withdraw()

    def show(self):
        self.window.deiconify()
        self.add_message("🤖 EVA", "Hello! How can I help you today?")

    def hide(self):
        self.window.withdraw()

    def add_message(self, sender, message, tag="bot"):
        self.stop_typing_animation()
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"{sender}:\n", tag)
        self.chat_area.insert(tk.END, f"{message}\n\n", "none")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)


    def send_message(self, event=None):
        message = self.entry.get().strip()
        if message:
            self.add_message("🧑 You", message, tag="user")
            self.entry.delete(0, tk.END)

            # Start typing animation and get real response
            self.show_typing_animation()
            threading.Thread(target=lambda: self.simulate_bot_response_with(message), daemon=True).start()

    def simulate_bot_response_with(self, user_message):
        try:
            response = handle_gemini.handle(user_message)  # ✅ REAL LOGIC
        except Exception as e:
            response = f"Error: {e}"

        self.stop_typing_animation()
        self.add_message("🤖 EVA", response)

    def show_typing_animation(self):
        if self.typing: return
        self.typing = True

        def animate():
            dot_count = 0
            self.chat_area.config(state=tk.NORMAL)
            self.typing_start_index = self.chat_area.index(f"{tk.END}-1c")
            self.chat_area.config(state=tk.DISABLED)

            while self.typing:
                dots = "." * (dot_count % 4)
                indicator_text = f"🤖 EVA is typing{dots}{' '*(4-len(dots))}\n"
                self.chat_area.config(state=tk.NORMAL)
                self.chat_area.delete(self.typing_start_index, tk.END)
                self.chat_area.insert(tk.END, indicator_text, "typing")
                self.chat_area.config(state=tk.DISABLED)
                self.chat_area.see(tk.END)
                dot_count += 1
                time.sleep(0.5)

        threading.Thread(target=animate, daemon=True).start()

    def stop_typing_animation(self):
        if not self.typing: return
        self.typing = False
        self.chat_area.config(state=tk.NORMAL)
        if self.typing_start_index:
            self.chat_area.delete(self.typing_start_index, tk.END)
            self.typing_start_index = None
        self.chat_area.config(state=tk.DISABLED)

    def run(self):
        self.window.mainloop()