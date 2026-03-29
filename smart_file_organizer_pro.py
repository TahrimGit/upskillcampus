import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ---------------- FILE CATEGORIES ----------------
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Music": [".mp3", ".wav"],
}

# ---------------- BACKEND FUNCTION ----------------
def organize_files(directory):
    if not os.path.exists(directory):
        messagebox.showerror("Error", "Selected directory does not exist!")
        return

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    total_files = len(files)

    if total_files == 0:
        messagebox.showinfo("Info", "No files to organize!")
        return

    progress_bar["maximum"] = total_files
    moved_count = 0
    skipped_count = 0

    for index, filename in enumerate(files):
        file_path = os.path.join(directory, filename)
        file_extension = os.path.splitext(filename)[1].lower()
        moved = False

        for folder, extensions in FILE_CATEGORIES.items():
            if file_extension in extensions:
                folder_path = os.path.join(directory, folder)
                os.makedirs(folder_path, exist_ok=True)

                destination = os.path.join(folder_path, filename)

                if not os.path.exists(destination):
                    shutil.move(file_path, destination)
                    moved_count += 1
                else:
                    skipped_count += 1

                moved = True
                break

        if not moved:
            other_folder = os.path.join(directory, "Others")
            os.makedirs(other_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(other_folder, filename))
            moved_count += 1

        progress_bar["value"] = index + 1
        root.update_idletasks()

    result_label.config(
        text=f"Moved: {moved_count} | Skipped: {skipped_count} | Total: {total_files}"
    )

    messagebox.showinfo("Success", "Files organized successfully!")

# ---------------- GUI FUNCTIONS ----------------
def browse_directory():
    folder_selected = filedialog.askdirectory()
    entry_path.delete(0, tk.END)
    entry_path.insert(0, folder_selected)

def start_organizing():
    directory = entry_path.get()
    if directory == "":
        messagebox.showwarning("Warning", "Please select a folder first!")
    else:
        organize_files(directory)

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Smart File Organizer Pro")
root.geometry("650x420")
root.configure(bg="#1e1e2f")
root.resizable(False, False)

# Optional icon
# root.iconbitmap("icon.ico")

# Title
title_label = tk.Label(
    root,
    text="Smart File Organizer Pro",
    font=("Segoe UI", 20, "bold"),
    bg="#1e1e2f",
    fg="#00ffcc"
)
title_label.pack(pady=20)

# Frame
frame = tk.Frame(root, bg="#2b2b3c", padx=20, pady=20)
frame.pack(pady=10)

entry_path = tk.Entry(
    frame,
    width=50,
    font=("Segoe UI", 11)
)
entry_path.grid(row=0, column=0, padx=5, pady=10)

browse_btn = tk.Button(
    frame,
    text="Browse",
    command=browse_directory,
    font=("Segoe UI", 10, "bold"),
    bg="#4a90e2",
    fg="white",
    padx=10,
    pady=5
)
browse_btn.grid(row=0, column=1, padx=5)

organize_btn = tk.Button(
    root,
    text="Organize Files",
    command=start_organizing,
    font=("Segoe UI", 12, "bold"),
    bg="#00cc66",
    fg="white",
    width=20,
    height=2
)
organize_btn.pack(pady=20)

# Progress Bar
progress_bar = ttk.Progressbar(root, length=500, mode="determinate")
progress_bar.pack(pady=10)

# Result Label
result_label = tk.Label(
    root,
    text="Moved: 0 | Skipped: 0 | Total: 0",
    font=("Segoe UI", 11),
    bg="#1e1e2f",
    fg="white"
)
result_label.pack(pady=10)

# Footer
footer = tk.Label(
    root,
    text="Python Internship Project | Advanced File Management System",
    font=("Segoe UI", 9),
    bg="#1e1e2f",
    fg="gray"
)
footer.pack(side="bottom", pady=10)

root.mainloop()