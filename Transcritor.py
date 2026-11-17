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
        self.geometry("640x480")
        self.minsize(550, 400)

        # O modelo será carregado apenas quando necessário para a janela abrir rápido
        self.model = None

        # --- Cabeçalho ---
        self.title_label = ctk.CTkLabel(
            self, 
            text="Transcritor Automático de Áudio", 
            font=("Segoe UI", 20, "bold")
        )
        self.title_label.pack(pady=(20, 5))

        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="Suporta arquivos .wav e .opus", 
            font=("Segoe UI", 12),
            text_color="gray"
        )
        self.subtitle_label.pack(pady=(0, 15))

        # --- Botão de Ação ---
        self.select_button = ctk.CTkButton(
            self, 
            text="Selecionar Áudios para Transcrever", 
            font=("Segoe UI", 14, "bold"),
            height=40,
            command=self.select_files
        )
        self.select_button.pack(pady=10)

        # --- Caixa de Logs e Progresso ---
        self.progress = ctk.CTkTextbox(
            self, 
            font=("Consolas", 12), 
            wrap="word"
        )
        self.progress.pack(pady=10, padx=25, fill="both", expand=True)

        # --- Rodapé com Créditos ---
        self.footer_label = ctk.CTkLabel(
            self, 
            text="Desenvolvido por Osmair DEV | Riamso DEV", 
            font=("Segoe UI", 11),
            text_color="#888888"
        )
        self.footer_label.pack(side="bottom", pady=8)

        self.file_paths = []

    def append(self, message):
        """Garante que a atualização visual ocorra na thread principal do Tkinter."""
        self.after(0, self._append_text, message)

    def _append_text(self, message):
        self.progress.insert("end", message + "\n")
        self.progress.see("end")

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Escolha os arquivos de áudio",
            filetypes=[("Arquivos de Áudio", "*.wav *.opus")]
        )
        if files:
            self.file_paths = list(files)
            # Desativa o botão para evitar múltiplas execuções concorrentes
            self.select_button.configure(state="disabled", text="Processando...")
            threading.Thread(target=self.transcribe_all, daemon=True).start()

    def transcribe_all(self):
        try:
            # Carrega o modelo apenas no primeiro uso
            if self.model is None:
                self.append("⏳ Carregando modelo Whisper (base)... aguarde.")
                self.model = whisper.load_model("base")
                self.append("✔ Modelo carregado com sucesso!\n")

            for file in self.file_paths:
                nome_arquivo = os.path.basename(file)
                self.append(f"🎙️ Transcrevendo: {nome_arquivo}...")
                
                try:
                    result = self.model.transcribe(file, language="pt")
                    output_file = file + ".txt"
                    
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(result["text"])
                        
                    self.append(f"✔ Salvo em: {output_file}\n")
                except Exception as e:
                    self.append(f"❌ Erro ao transcrever {nome_arquivo}: {e}\n")

            self.append("✨ Todas as transcrições foram finalizadas!\n" + ("-" * 45))

        finally:
            # Reativa o botão ao término
            self.after(0, lambda: self.select_button.configure(
                state="normal", 
                text="Selecionar Áudios para Transcrever"
            ))

if __name__ == "__main__":
    app = WhisperApp()
    app.mainloop()
