import tkinter as tk
from tkinter import filedialog, ttk
import pyttsx3
import PyPDF2
import threading

class PDFReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Text-to-Speech Reader")

        self.engine = pyttsx3.init()
        self.playing = False
        self.thread = None

        self.text_content = ""

        # UI Layout
        self.build_gui()

    def build_gui(self):
        # Load PDF Button
        load_btn = ttk.Button(self.root, text="Load PDF", command=self.load_pdf)
        load_btn.pack(pady=10)

        # Volume Slider
        self.volume_slider = tk.Scale(self.root, from_=0, to=1, resolution=0.1,
                                      orient=tk.HORIZONTAL, label="Volume", command=self.update_volume)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(padx=20, pady=5)

        # Speed Slider
        self.speed_slider = tk.Scale(self.root, from_=100, to=300,
                                     orient=tk.HORIZONTAL, label="Speed (WPM)", command=self.update_speed)
        self.speed_slider.set(150)
        self.speed_slider.pack(padx=20, pady=5)

        # Control Buttons
        controls = tk.Frame(self.root)
        controls.pack(pady=10)

        self.play_btn = ttk.Button(controls, text="Play", command=self.play)
        self.play_btn.grid(row=0, column=0, padx=10)

        self.stop_btn = ttk.Button(controls, text="Stop", command=self.stop)
        self.stop_btn.grid(row=0, column=1, padx=10)

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return

        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                self.text_content = ""
                for page in reader.pages:
                    self.text_content += page.extract_text()
            print("PDF loaded successfully.")
        except Exception as e:
            print("Error:", e)

    def update_volume(self, val):
        self.engine.setProperty('volume', float(val))

    def update_speed(self, val):
        self.engine.setProperty('rate', int(val))

    def play(self):
        if not self.text_content:
            print("No PDF loaded.")
            return
        if self.playing:
            return
        self.playing = True
        self.thread = threading.Thread(target=self._speak_text)
        self.thread.start()

    def _speak_text(self):
        self.engine.say(self.text_content)
        self.engine.runAndWait()
        self.playing = False

    def stop(self):
        if self.playing:
            self.engine.stop()
            self.playing = False

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFReaderApp(root)
    root.mainloop()
