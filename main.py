import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import torch
import whisper
from pydub import AudioSegment


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.flac")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)


def demucs_separate(audio_path):
    output_dir = os.path.join(os.getcwd(), 'separated')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        subprocess.run(['demucs', '-o', output_dir, audio_path])
    vocal_path = os.path.join(output_dir, 'htdemucs', os.path.basename(audio_path).replace(".mp3", "").replace(".wav", ""), 'vocals.wav')
    return vocal_path


def transcribe_audio(vocal_path):
    model = whisper.load_model("medium")
    result = model.transcribe(vocal_path)
    print(result)
    print(result['text'])
    segments = result['segments']
    lyrics = ""
    for s in segments:
        start = round(s['start'],2)
        end = round(s['end'],2)
        text = s['text']
        lyrics += (str)(start) + "s--" + (str)(end) + "s" + "\t" + text + "\n"
    # return result['text']
    return lyrics

def process_audio():
    audio_path = file_entry.get()
    if not audio_path:
        messagebox.showerror("Error", "Please select an audio file.")
        return

    try:
        vocal_path = demucs_separate(audio_path)
        transcription = transcribe_audio(vocal_path)

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, transcription)

    except Exception as e:
        messagebox.showerror("Error", str(e))


app = tk.Tk()
app.title("Audio Processor")

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

file_entry = tk.Entry(frame, width=50)
file_entry.pack(side=tk.LEFT, padx=(0, 10))

browse_button = tk.Button(frame, text="Browse", command=browse_file)
browse_button.pack(side=tk.LEFT)

process_button = tk.Button(app, text="Process", command=process_audio)
process_button.pack(pady=(10, 0))

result_text = tk.Text(app, height=20, width=80, wrap=tk.WORD)
result_text.pack(padx=10, pady=10)

app.mainloop()
