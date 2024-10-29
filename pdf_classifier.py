import tkinter as tk
from tkinter import ttk, Canvas, Frame, filedialog, messagebox
import fitz  # PyMuPDF
import os
import sqlite3
import csv

class PDFClassifier:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Quality Classifier")
        self.root.geometry("1024x768")

        # Set up SQLite database
        self.db_file = "classification_results.db"
        self.setup_database()

        # Let the user select a folder with PDFs
        self.pdf_files = []
        self.select_folder()

        # Set up scrollable canvas for PDF display
        self.canvas = Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.display_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.display_frame, anchor="nw")
        self.display_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Buttons and status layout
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(side=tk.BOTTOM, pady=10)

        # Good and Bad buttons (above navigation buttons)
        self.good_button = tk.Button(
            self.buttons_frame, text="Good", command=lambda: self.classify("Good"), 
            font=("Helvetica", 14), width=10, height=2, bg="green", fg="white"
        )
        self.good_button.grid(row=0, column=1, padx=10)

        self.bad_button = tk.Button(
            self.buttons_frame, text="Bad", command=lambda: self.classify("Bad"), 
            font=("Helvetica", 14), width=10, height=2, bg="red", fg="white"
        )
        self.bad_button.grid(row=0, column=2, padx=10)

        # Navigation buttons (below classification buttons)
        self.back_button = tk.Button(self.buttons_frame, text="Back", command=self.previous_pdf, font=("Helvetica", 12), width=8)
        self.back_button.grid(row=1, column=1, padx=10, pady=10)

        self.next_button = tk.Button(self.buttons_frame, text="Next", command=self.next_pdf, font=("Helvetica", 12), width=8)
        self.next_button.grid(row=1, column=2, padx=10, pady=10)

        # Export button
        export_button = tk.Button(
            self.buttons_frame, text="Export to CSV", command=self.export_to_csv, 
            font=("Helvetica", 12), width=12
        )
        export_button.grid(row=3, column=1, columnspan=2, pady=10)

        # Status label
        self.status_label = tk.Label(self.buttons_frame, text="", font=("Helvetica", 12))
        self.status_label.grid(row=2, column=1, columnspan=2, pady=10)

        # Display the first PDF if any
        if self.pdf_files:
            self.display_pdf()
        else:
            messagebox.showinfo("No PDFs Found", "No PDFs found in the selected folder.")
            self.root.quit()

    def setup_database(self):
        """Initialize the SQLite database and ensure the table exists."""
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS classifications (
                filename TEXT PRIMARY KEY,
                quality TEXT
            )
        """)
        self.conn.commit()

    def select_folder(self):
        """Let the user select a folder and load PDFs from it."""
        folder = filedialog.askdirectory(title="Select Folder with PDFs")
        if folder:
            self.pdf_files = [f for f in os.listdir(folder) if f.endswith(".pdf")]
            self.pdf_files = [os.path.join(folder, f) for f in self.pdf_files]
            self.current_index = 0  # Reset index
        else:
            messagebox.showwarning("No Folder Selected", "You must select a folder to continue.")
            self.root.quit()

    def get_classification(self, filename):
        """Retrieve the classification for a given PDF."""
        self.cursor.execute("SELECT quality FROM classifications WHERE filename = ?", (filename,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def save_classification(self, filename, quality):
        """Save or update the classification for a PDF."""
        self.cursor.execute("""
            INSERT INTO classifications (filename, quality) 
            VALUES (?, ?) 
            ON CONFLICT(filename) DO UPDATE SET quality = excluded.quality
        """, (filename, quality))
        self.conn.commit()

    def display_pdf(self):
        """Display the current PDF and update its classification status."""
        if 0 <= self.current_index < len(self.pdf_files):
            filepath = self.pdf_files[self.current_index]
            self.render_pdf_page(filepath)

            # Update status label with color
            filename = os.path.basename(filepath)
            status = self.get_classification(filename)
            if status:
                if status == "Good":
                    self.status_label.config(text=f"Current Status: {status}", fg="green")
                elif status == "Bad":
                    self.status_label.config(text=f"Current Status: {status}", fg="red")
            else:
                self.status_label.config(text="Current Status: Not Classified", fg="black")
        else:
            self.show_completion_message()

    def render_pdf_page(self, filepath):
        """Render the first page of the specified PDF."""
        self.current_file = filepath
        doc = fitz.open(filepath)
        first_page = doc.load_page(0)
        pix = first_page.get_pixmap()
        pix.save("temp.png")

        # Clear previous content
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        # Display the new PDF page
        img = tk.PhotoImage(file="temp.png")
        pdf_image = tk.Label(self.display_frame, image=img)
        pdf_image.image = img  # Keep reference to avoid garbage collection
        pdf_image.pack()

    def classify(self, quality):
        """Classify the current PDF and save the result."""
        filename = os.path.basename(self.current_file)
        self.save_classification(filename, quality)
        self.next_pdf()  # Move to the next PDF

    def next_pdf(self):
        """Move to the next PDF."""
        if self.current_index < len(self.pdf_files) - 1:
            self.current_index += 1
            self.display_pdf()

    def previous_pdf(self):
        """Move to the previous PDF."""
        if self.current_index > 0:
            self.current_index -= 1
            self.display_pdf()

    def export_to_csv(self):
        """Export the classification results to a CSV file."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT filename, quality FROM classifications")
        rows = cursor.fetchall()

        with open("classification_results.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Filename", "Quality"])
            writer.writerows(rows)

        print("Results exported to classification_results.csv.")


    def show_completion_message(self):
        """Display a completion message if all PDFs are classified."""
        self.display_frame.destroy()  # Clear the display frame
        self.pdf_label = tk.Label(self.root, text="All PDFs have been classified!", font=("Helvetica", 16))
        self.pdf_label.pack(expand=True)

    def run(self):
        """Run the Tkinter event loop."""
        self.root.mainloop()

    def close(self):
        """Close the database connection."""
        self.conn.close()

if __name__ == "__main__":
    app = PDFClassifier()
    try:
        app.run()
    finally:
        app.close()
