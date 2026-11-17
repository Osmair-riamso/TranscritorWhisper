import customtkinter as ctk
from tkinter import filedialog
import os
import threading
import whisper

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class WhisperApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Transcritor de Áudio - Whisper")
        self.geometry("600x400")

        self.model = whisper.load_model("base")

        self.label = ctk.CTkLabel(self, text="Selecione arquivos .wav ou .opus para transcrição", font=("Arial", 16))
        self.label.pack(pady=20)

        self.select_button = ctk.CTkButton(self, text="Selecionar Áudios", command=self.select_files)
        self.select_button.pack(pady=10)

        self.progress = ctk.CTkTextbox(self, height=200)
        self.progress.pack(pady=10, padx=20, fill="both", expand=True)

        self.file_paths = []

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Áudio", "*.wav *.opus")])
        if files:
            self.file_paths = list(files)
            threading.Thread(target=self.transcribe_all).start()

    def transcribe_all(self):
        for file in self.file_paths:
            self.append(f"Transcrevendo: {os.path.basename(file)}")
            try:
                result = self.model.transcribe(file, language="pt")
                output_file = file + ".txt"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(result["text"])
                self.append(f"✔ Transcrição salva em: {output_file}\n")
            except Exception as e:
                self.append(f"❌ Erro ao transcrever {os.path.basename(file)}: {e}\n")

    def append(self, message):
        self.progress.insert("end", message + "\n")
        self.progress.see("end")

if __name__ == "__main__":
    app = WhisperApp()
    app.mainloop()
