import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageToPDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        self.root.geometry("800x600")
        
        self.images = []   # Store (path, thumbnail) tuples
        self.thumbnails = []

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Images", command=self.add_images).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Move Up", command=self.move_up).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Move Down", command=self.move_down).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Create PDF", command=self.create_pdf).grid(row=0, column=3, padx=5)

        # Canvas for thumbnails
        self.canvas = tk.Canvas(root, width=750, height=450, bg="white")
        self.canvas.pack(pady=10)

        self.frame = tk.Frame(self.canvas, bg="white")
        self.scroll_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.config(yscrollcommand=self.scroll_y.set)
        self.frame.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))

    def add_images(self):
        paths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.tiff")]
        )
        for path in paths:
            img = Image.open(path)
            img.thumbnail((150, 150))  # Make thumbnail
            thumb = ImageTk.PhotoImage(img)
            self.images.append(path)
            self.thumbnails.append(thumb)

        self.refresh_display()

    def refresh_display(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        for i, thumb in enumerate(self.thumbnails):
            lbl = tk.Label(self.frame, image=thumb)
            lbl.grid(row=i, column=0, pady=5, padx=10)
            tk.Label(self.frame, text=f"{i+1}", font=("Arial", 12)).grid(row=i, column=1, padx=10)

    def move_up(self):
        selected = len(self.images) - 1
        if selected > 0:
            self.images[selected-1], self.images[selected] = self.images[selected], self.images[selected-1]
            self.thumbnails[selected-1], self.thumbnails[selected] = self.thumbnails[selected], self.thumbnails[selected-1]
            self.refresh_display()

    def move_down(self):
        selected = len(self.images) - 1
        if selected < len(self.images) - 1:
            self.images[selected+1], self.images[selected] = self.images[selected], self.images[selected+1]
            self.thumbnails[selected+1], self.thumbnails[selected] = self.thumbnails[selected], self.thumbnails[selected+1]
            self.refresh_display()

    def create_pdf(self):
        if not self.images:
            messagebox.showwarning("No Images", "Please add images first!")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save PDF As"
        )
        if not save_path:
            return

        try:
            first = Image.open(self.images[0]).convert("RGB")
            rest = [Image.open(img).convert("RGB") for img in self.images[1:]]
            first.save(save_path, save_all=True, append_images=rest)
            messagebox.showinfo("Success", f"PDF saved as:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToPDFApp(root)
    root.mainloop()
