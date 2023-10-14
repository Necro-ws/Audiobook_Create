import pyttsx3
import pdfplumber
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from threading import Thread


def convert_pdf_to_audio():

    pdf_file = filedialog.askopenfilename(filetypes=[('PDF Files', '*.pdf')])
    if not pdf_file:
        return

    def pdf_to_text():

        engine = pyttsx3.init()
        engine.setProperty('voice', 'brazil')

        pdf = pdfplumber.open(pdf_file)
        pages = pdf.pages

        text = ''
        for page in pages:
            text += page.extract_text()
            
        text = text.replace('\n', ' ')

        engine.save_to_file(text, 'file.mp3')
        engine.runAndWait()
        messagebox.showinfo('Complete','Audiobook loaded successfully!')
        save_button['state'] = 'normal'

    progress_bar['maximum'] = 100
    progress_bar['value'] = 0
    save_button['state'] = 'disabled'

    def update_progress_bar():
        for i in range(101):
            progress_bar['value'] = i
            root.update_idletasks()

    progress_thread = Thread(target=pdf_to_text)
    progress_thread.start()

    progress_update_thread = Thread(target=update_progress_bar)
    progress_update_thread.start()

def save_audio():
    audio_file = filedialog.asksaveasfilename(defaultextension='.mp3', filetypes=[('MP3 Files', '*.mp3')])
    if audio_file:
        import shutil
        shutil.move('file.mp3', audio_file)
        messagebox.showinfo('Save', 'Audiobook saved successfully!')
        progress_bar['value'] = 0
        save_button['state'] = 'disabled'

root = tk.Tk()
root.title('PDF to Audiobook Converter')
root.configure(background='#e5d8c9')
font = tkFont.Font(family='Comic Sans MS', size= 11, weight='bold', slant='italic')
root.option_add('*font', font)
root.option_add('*foreground', '#444444')


frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

choose_file_button = tk.Button(root, text='Choose PDF', command=convert_pdf_to_audio, activeforeground='#444444')
choose_file_button.pack(padx=10, pady=10)

progress_bar_collor = ttk.Style()
progress_bar_collor.theme_use('clam')
progress_bar_collor.configure('color.Horizontal.TProgressbar', foreground='#e5d8c9', background='#e5d8c9')
progress_bar = ttk.Progressbar(frame, style='color.Horizontal.TProgressbar' ,orient='horizontal', length=300, mode='determinate')
progress_bar.pack(padx=10, pady=10)

save_button = tk.Button(root, text='Save', command=save_audio, state='disabled', activeforeground='#444444')
save_button.pack(padx=10, pady=10)

root.mainloop()