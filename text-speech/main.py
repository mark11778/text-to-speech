import tkinter as tk
from tkinter import filedialog, ttk
import pyttsx3
import threading
from pdf2image import convert_from_path
import pytesseract
import os
import tempfile
import time

class PDFReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF OCR Text-to-Speech Reader")

        self.engine = pyttsx3.init()
        self.playing = False
        self.thread = None

        self.text_content = ""

        self.build_gui()

    def build_gui(self):
        load_btn = ttk.Button(self.root, text="Load PDF", command=self.load_pdf)
        load_btn.pack(pady=10)

        self.volume_slider = tk.Scale(self.root, from_=0, to=1, resolution=0.1,
                                      orient=tk.HORIZONTAL, label="Volume", command=self.update_volume)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(padx=20, pady=5)

        self.speed_slider = tk.Scale(self.root, from_=100, to=300,
                                     orient=tk.HORIZONTAL, label="Speed (WPM)", command=self.update_speed)
        self.speed_slider.set(150)
        self.speed_slider.pack(padx=20, pady=5)

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
        start = time.time()
        try:
            print("Converting PDF to images for OCR...")
            with tempfile.TemporaryDirectory() as tempdir:
                images = convert_from_path(file_path, dpi=300)
                self.text_content = ""
                for i, image in enumerate(images):
                    text = pytesseract.image_to_string(image)
                    self.text_content += text + "\n"
                    print(f"Processed page {i+1}")

            print("OCR completed.")
            end = time.time()
            print(f"time elapsed: {(end - start)}")
            print(f"Extracted text:\n{self.text_content}")
        except Exception as e:
            print("Error during OCR:", e)

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
