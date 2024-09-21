import tkinter as tk
from app.config import Config
from threading import Thread
from app.scraper import Scraper
from app.communiator import Communicator
from tkinter import ttk


class Frontend:

    def __init__(self, root):
        # Set the root window title and fixed size
        root.title("Gmaps Reviews Scraper")
        root.geometry("650x500")
        root.resizable(False, False)  # Disable resizing of the window

        # Set a background color for the window
        root.config(bg="#f0f4f7")

        # Main heading
        self.heading_label = tk.Label(
            root,
            text="Gmaps Reviews Scraper",
            font=("Helvetica", 16, "bold"),
            bg="#f0f4f7",
            fg="#333",
        )
        self.heading_label.pack(pady=(20, 10))

        # Link input label and entry box
        self.label_link = tk.Label(
            root, text="Enter URL:", font=("Helvetica", 12), bg="#f0f4f7", fg="#333"
        )
        self.label_link.pack(anchor="w", padx=30)

        # Custom styling for entry box (rounded border and padding)
        self.link_input = tk.Entry(
            root,
            width=50,
            font=("Helvetica", 12),
            relief="flat",
            highlightthickness=2,
            highlightcolor="#cccccc",
        )
        self.link_input.pack(pady=5, padx=30)
        self.link_input.config(highlightbackground="#cccccc", borderwidth=0)
        self.link_input.bind("<FocusIn>", self.on_focus_in)
        self.link_input.bind("<FocusOut>", self.on_focus_out)

        # Format dropdown label and dropdown menu
        self.label_format = tk.Label(
            root, text="Select Format:", font=("Helvetica", 12), bg="#f0f4f7", fg="#333"
        )
        self.label_format.pack(anchor="w", padx=30, pady=(10, 5))

        # Define the dropdown options (Excel, JSON, CSV)
        self.format_options = ["excel", "json", "csv"]
        self.selected_format = tk.StringVar()
        self.selected_format.set(self.format_options[0])  # Default value

        # Dropdown menu
        self.format_dropdown = ttk.Combobox(
            root,
            textvariable=self.selected_format,
            values=self.format_options,
            state="readonly",
            font=("Helvetica", 12),
        )
        self.format_dropdown.pack(pady=5, padx=30)

        # Scrape button with rounded corners and hover effect
        self.scrape_button = tk.Button(
            root,
            text="Scrape",
            command=self.scrape_data,
            font=("Helvetica", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=12,
            height=2,
            relief="flat",
        )
        self.scrape_button.pack(pady=(30, 10))
        self.scrape_button.bind("<Enter>", self.on_hover)
        self.scrape_button.bind("<Leave>", self.off_hover)

        # Message box label
        self.label_message = tk.Label(
            root, text="Logs:", font=("Helvetica", 12), bg="#f0f4f7", fg="#333"
        )
        self.label_message.pack(anchor="w", padx=30, pady=(10, 5))

        # Create a frame to hold the message box and the scrollbar
        message_frame = tk.Frame(root)
        message_frame.pack(padx=30, pady=10)

        # Create a scrollbar and attach it to the frame
        self.scrollbar = tk.Scrollbar(message_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Textbox to display messages, attach the scrollbar
        self.message_box = tk.Text(
            message_frame,
            height=8,
            width=60,
            font=("Helvetica", 12),
            state="disabled",
            bg="#fff",
            yscrollcommand=self.scrollbar.set,
        )
        self.message_box.pack(side=tk.LEFT)

        # Configure the scrollbar to work with the text box
        self.scrollbar.config(command=self.message_box.yview)

        # Show welcome message at startup
        self.append_message("Welcome to Web Scraper!")

    def scrape_data(self):
        # Get the link input and selected format
        link = self.link_input.get()

        if link.strip() == "":
            message = f"Please enter valid link"
            self.append_message(message)
            return

        format_selected = self.selected_format.get()

        Config.set_url(link)
        Config.set_format(format_selected)

        # Append new message in the message box
        message = f"Scraping data from: {link} in {format_selected} format.\n"
        self.append_message(message)

        scraper = Scraper()

        thread = Thread(target=scraper.main)
        thread.start()

    def append_message(self, message):
        # Enable the textbox to insert new message
        self.message_box.config(state="normal")

        message = f"• {message}\n\n"

        self.message_box.insert(tk.END, message)  # Append new message
        self.message_box.config(state="disabled")  # Disable editing again
        self.message_box.see(tk.END)  # Scroll to the latest message

    def on_focus_in(self, event):
        """Callback for focus in event of text input"""

        event.widget.config(highlightcolor="#4CAF50", highlightthickness=2)

    def on_focus_out(self, event):
        """Callback for focus out event of text input"""

        event.widget.config(highlightcolor="#cccccc", highlightthickness=2)

    def on_hover(self, event):
        """Callback for on hover event of button"""

        event.widget.config(bg="#45a049")

    def off_hover(self, event):
        """Callback for off hover event of button"""

        event.widget.config(bg="#4CAF50")


def run_frontend():
    # Initialize the main Tkinter application
    root = tk.Tk()
    app = Frontend(root)
    Communicator.set_frontend_obj(app)
    root.mainloop()
