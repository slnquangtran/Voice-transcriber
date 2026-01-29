import customtkinter as ctk
import os
import sys
from PIL import Image

# Import the Voice Transcriber App
try:
    from app import HybridTranscriberApp
except ImportError as e:
    print(f"Error importing app: {e}")
    HybridTranscriberApp = None

# Import the Study Assistant GUI
try:
    from study_gui import StudyAssistantGUI
except ImportError as e:
    print(f"Error importing study gui: {e}")
    StudyAssistantGUI = None

class MainMenuApp(ctk.CTk): 
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("NoteForge")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        self.geometry(f"800x600+{x}+{y}")

        self.current_child = None

        self.create_widgets()

    def create_widgets(self):
        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Header space
        self.grid_rowconfigure(1, weight=2) # Buttons
        self.grid_rowconfigure(2, weight=1) # Footer

        # --- Header ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(40, 20))
        
        ctk.CTkLabel(
            header_frame, 
            text="⚡ NOTEFORGE", 
            font=("Segoe UI", 36, "bold"),
            text_color="#3B8ED0"
        ).pack()
        
        ctk.CTkLabel(
            header_frame,
            text="Real-Time Transcription & Intelligent Note Summarization",
            font=("Segoe UI", 15),
            text_color="gray"
        ).pack(pady=5)

        # --- Buttons Area ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=1, column=0)

        # Button Style
        btn_width = 280
        btn_height = 50
        btn_font = ("Segoe UI", 16)

        # 1. Real-Time Transcription
        self.btn_transcriber = ctk.CTkButton(
            btn_frame,
            text="   🎤  Real-Time Transcription   ",
            font=btn_font,
            width=btn_width,
            height=btn_height,
            command=self.open_voice_transcriber
        )
        self.btn_transcriber.pack(pady=15)

        # 2. Note Summarization
        self.btn_study = ctk.CTkButton(
            btn_frame,
            text="   📝  Note Summarization   ",
            font=btn_font,
            width=btn_width,
            height=btn_height,
            fg_color="#8E44AD",
            hover_color="#9B59B6",
            command=self.open_study_assistant
        )
        self.btn_study.pack(pady=15)

        # 3. Settings
        self.btn_settings = ctk.CTkButton(
            btn_frame,
            text="   ⚙️  Settings   ",
            font=btn_font,
            width=btn_width,
            height=btn_height,
            fg_color="transparent",
            border_width=2,
            border_color="#3B8ED0",
            text_color=("gray10", "#DCE4EE"),
            command=self.open_settings
        )
        self.btn_settings.pack(pady=15)

        # 4. Exit
        self.btn_exit = ctk.CTkButton(
            btn_frame,
            text="   ❌  Exit   ",
            font=btn_font,
            width=btn_width,
            height=btn_height,
            fg_color="#C0392B",
            hover_color="#E74C3C",
            command=self.exit_app
        )
        self.btn_exit.pack(pady=15)

        # --- Footer ---
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=2, column=0, sticky="ew", pady=20)
        
        ctk.CTkLabel(
            footer_frame,
            text="v2.1 AI Edition | Powered by Vosk, Whisper & Spacy",
            font=("Segoe UI", 12),
            text_color="gray"
        ).pack(side="bottom")

    def open_voice_transcriber(self):
        if HybridTranscriberApp is None:
            print("App module not found")
            return

        # Hide Main Menu
        self.withdraw()

        # Open Child Window
        self.current_child = HybridTranscriberApp(self)
        
        def on_child_close():
            self.current_child.destroy()
            self.current_child = None
            self.deiconify() # Show Menu again
            
        self.current_child.protocol("WM_DELETE_WINDOW", on_child_close)
        self.current_child.focus()

    def open_study_assistant(self):
        if StudyAssistantGUI is None:
            print("Study GUI module not found")
            return
        
        self.withdraw()
        self.current_child = StudyAssistantGUI(self)
        
        def on_child_close():
            self.current_child.destroy()
            self.current_child = None
            self.deiconify()
            
        self.current_child.protocol("WM_DELETE_WINDOW", on_child_close)
        self.current_child.focus()

    def open_settings(self):
        toplevel = ctk.CTkToplevel(self)
        toplevel.geometry("300x200")
        toplevel.title("Settings")
        toplevel.focus()
        ctk.CTkLabel(toplevel, text="Settings", font=("Bold", 20)).pack(pady=20)
        ctk.CTkLabel(toplevel, text="Global config coming soon...").pack(pady=10)

    def exit_app(self):
        self.quit()
        sys.exit()

if __name__ == "__main__":
    app = MainMenuApp()
    app.mainloop()
