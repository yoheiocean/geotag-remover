import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image

selected_files = []

def choose_files():
    filetypes = [("Image files", "*.jpg;*.jpeg;*.png")]
    selected = filedialog.askopenfilenames(filetypes=filetypes)
    selected_files.extend(selected)
    file_count = len(selected_files)
    if file_count > 0:
        file_label.configure(text=f"{file_count} files selected.", fg="#666")
    else:
        file_label.configure(text="No files selected.", fg="#666")

def remove_geotags():
    for file_path in selected_files:
        if os.path.isfile(file_path):
            image = Image.open(file_path)
            if 'gps_info' in image.info:
                del image.info['gps_info']
            image.save(file_path)
            image.close()
        elif os.path.isdir(file_path):
            for filename in os.listdir(file_path):
                file = os.path.join(file_path, filename)
                if os.path.isfile(file) and filename.endswith(('.jpg', '.jpeg', '.png')):
                    image = Image.open(file)
                    if 'gps_info' in image.info:
                        del image.info['gps_info']
                    image.save(file)
                    image.close()

    selected_files.clear()  # Reset selected files list
    file_label.configure(text="No files selected.", fg="#666")  # Update label text

    submit_button.configure(state=tk.NORMAL)
    status_label.configure(text="GPS data successfully removed.", fg="salmon")

def submit():
    submit_button.configure(state=tk.DISABLED)
    status_label.configure(text="Processing...", fg="black")
    remove_geotags()

# Define a custom font
custom_font = ("Corbel", 12)

window = tk.Tk()
window.title("Geotag Removal Tool")

# Change background color to gray (#222)
window.configure(bg="#222")

# Apply custom font to all components
window.option_add("*Font", custom_font)

window_width = 400  # Specify the desired width of the window
window_height = 200  # Specify the desired height of the window

# Calculate the screen dimensions to center the window
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window size and position
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Add padding at the top
top_padding = tk.Frame(window, height=30, bg="#222")
top_padding.pack()

choose_button = tk.Button(
    window, 
    text="Choose files", 
    command=choose_files, 
    relief="flat",  # Set button relief to flat
    bg="#333", 
    fg="#DDD",
    activebackground="#333",  # Set button background color when pressed
    activeforeground="#DDD",  # Set button text color when pressed
)
choose_button.pack()

file_label = tk.Label(window, text="No files selected.", bg="#222", fg="#666")
file_label.pack()

submit_button = tk.Button(
    window, 
    text="Remove", 
    command=submit, 
    relief="flat",  # Set button relief to flat
    bg="#333", 
    fg="#DDD",
    activebackground="#333",  # Set button background color when pressed
    activeforeground="#DDD",  # Set button text color when pressed
)
submit_button.pack(pady=10)

status_label = tk.Label(window, text="", fg="red", bg="#222")
status_label.pack()

window.mainloop()
