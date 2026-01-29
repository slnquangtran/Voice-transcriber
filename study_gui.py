import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os

# Import Logic
try:
    from study_assistant import ConceptualAssistant
except ImportError:
    ConceptualAssistant = None

class StudyAssistantGUI(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.title("NoteForge - Note Summarization")
        self.geometry("1000x800")
        self.center_window()
        
        self.assistant = None
        self.processed_data = None
        
        # Initialize assistant immediately (no heavy model loading)
        if ConceptualAssistant:
            self.assistant = ConceptualAssistant()
            status_text = "Ready. Load a file to generate lecture notes."
        else:
            status_text = "Error: missing logic module."
        
        self.status_var = ctk.StringVar(value=status_text)
        self.create_widgets()

    def center_window(self):
        self.update_idletasks()
        width = 1000
        height = 800
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Header ---
        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        ctk.CTkLabel(header, text="📝 Note Summarization", font=("Segoe UI", 20, "bold")).pack(side="left", padx=20, pady=10)
        
        self.btn_load = ctk.CTkButton(header, text="📂 Load File (TXT/PPTX)", command=self.load_file)
        self.btn_load.pack(side="right", padx=20)

        # --- Main Content Area ---
        self.notes_box = ctk.CTkTextbox(self, font=("Consolas", 12), wrap="word")
        self.notes_box.grid(row=1, column=0, padx=20, pady=0, sticky="nsew")

        # --- Footer ---
        footer = ctk.CTkFrame(self, height=60)
        footer.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        
        self.progress_bar = ctk.CTkProgressBar(footer, width=200)
        self.progress_bar.pack(side="left", padx=10, pady=10)
        self.progress_bar.set(0)
        
        self.lbl_status = ctk.CTkLabel(footer, textvariable=self.status_var)
        self.lbl_status.pack(side="left", padx=10)
        
        self.btn_process = ctk.CTkButton(footer, text="📝 Generate Lecture Notes", command=self.start_processing, fg_color="#27AE60", hover_color="#229954")
        self.btn_process.pack(side="right", padx=10, pady=10)
        
        self.btn_export = ctk.CTkButton(footer, text="💾 Export PDF", command=self.export_pdf, state="disabled")
        self.btn_export.pack(side="right", padx=10)

        self.loaded_filepath = None

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("PowerPoint", "*.pptx"), ("All Files", "*.*")])
        if filepath:
            self.loaded_filepath = filepath # Store path, don't read text yet if binary
            
            try:
                # Basic preview
                if filepath.endswith(".txt"):
                    with open(filepath, "r", encoding="utf-8") as f:
                        preview = f.read(500)
                    self.notes_box.delete("1.0", "end")
                    self.notes_box.insert("1.0", f"Preview (TXT):\n{preview}...")
                else:
                    self.notes_box.delete("1.0", "end")
                    self.notes_box.insert("1.0", f"Preview (PPTX):\nLoaded slides from {os.path.basename(filepath)}\n\nClick 'Generate Lecture Notes' to process.")
                
                self.status_var.set(f"Loaded: {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}")

    def start_processing(self):
        if not self.loaded_filepath: 
            return

        self.status_var.set("Generating lecture notes...")
        self.progress_bar.set(0)
        self.btn_process.configure(state="disabled")
        
        threading.Thread(target=self.run_pipeline, daemon=True).start()

    def run_pipeline(self):
        if not self.assistant: return
        
        def update_status(msg, progress=0):
            self.status_var.set(msg)
            self.progress_bar.set(progress)

        try:
            # Use process_file which handles parsing
            results = self.assistant.process_file(self.loaded_filepath, progress_callback=update_status)
            self.processed_data = results
            self.after(0, self.display_results)
        except Exception as e:
            self.status_var.set(f"Error: {e}")
            print(f"Pipeline Error: {e}")
            self.after(0, lambda: self.btn_process.configure(state="normal"))

    def display_results(self):
        data = self.processed_data
        
        if not data or "error" in data:
            error_msg = data.get("error", "Unknown error") if data else "No data"
            messagebox.showerror("Processing Error", error_msg)
            self.btn_process.configure(state="normal")
            self.status_var.set("Error occurred.")
            return

        # Display the formatted lecture notes
        self.notes_box.delete("1.0", "end")
        self.notes_box.insert("1.0", data.get('notes', 'No notes generated'))
        
        self.btn_export.configure(state="normal")
        self.btn_process.configure(state="normal")
        self.status_var.set("Lecture notes generated successfully!")

    def export_pdf(self):
        if not self.processed_data: return
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if path:
            self.assistant.export_to_pdf(self.processed_data, path)
            messagebox.showinfo("Export", f"Saved to {path}")

if __name__ == "__main__":
    app = StudyAssistantGUI()
    app.mainloop()
