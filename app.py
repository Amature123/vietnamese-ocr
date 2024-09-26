import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageGrab
import easyocr
import numpy as np
from deep_translator import (GoogleTranslator,
                             ChatGptTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeeplTranslator,
                             QcriTranslator,
                             single_detection)

import os 
from dotenv import load_dotenv
load_dotenv()
# Initialize the EasyOCR reader
language_dict = {'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'assamese': 'as', 'aymara': 'ay', 'azerbaijani': 'az', 'bambara': 'bm', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bhojpuri': 'bho', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-CN', 'chinese (traditional)': 'zh-TW', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dhivehi': 'dv', 'dogri': 'doi', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'ewe': 'ee', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'guarani': 'gn', 'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'iw', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'ilocano': 'ilo', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'kinyarwanda': 'rw', 'konkani': 'gom', 'korean': 'ko', 'krio': 'kri', 'kurdish (kurmanji)': 'ku', 'kurdish (sorani)': 'ckb', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt', 'luganda': 'lg', 'luxembourgish': 'lb', 'macedonian': 'mk', 'maithili': 'mai', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'meiteilon (manipuri)': 'mni-Mtei', 'mizo': 'lus', 'mongolian': 'mn', 'myanmar': 'my', 'norwegian': 'no', 'odia (oriya)': 'or', 'oromo': 'om', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'quechua': 'qu', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'sanskrit': 'sa', 'scots gaelic': 'gd', 'sepedi': 'nso', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'tatar': 'tt', 'telugu': 'te', 'thai': 'th', 'tigrinya': 'ti', 'tsonga': 'ts', 'turkish': 'tr', 'turkmen': 'tk', 'twi': 'ak', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'}

languages_key = list(language_dict.keys())

laguages_value = list(language_dict.values())

reader = easyocr.Reader(['vi','en','de','fr'])

###Main shit
def get_ocr(image):

    result = reader.readtext(image)
    text = ' '.join([result[i][1] for i in range(len(result))])
    return text

def get_languages():
    return clicked.get()

def translate_text(text, source, target):
    translated = GoogleTranslator(source=source, target=target).translate(text=text)
    return translated


def paste_image_and_translate():
    # Grab the image from the clipboard
    try:
        image = ImageGrab.grabclipboard()
        if image is None:
            messagebox.showwarning("Warning", "No image found in clipboard!")
            return
        
        # Convert the image to a NumPy array
        image_np = np.array(image)

        # Perform OCR
        text = get_ocr(image_np)
        
        detect_text = single_detection(text, api_key=os.getenv('API'))

        # Display the recognized text
        text_display.delete(1.0, tk.END)  # Clear previous text
        translation_display.delete(1.0, tk.END)  # Clear previous text

        text_display.insert(tk.END, text)  # Insert new text
        translation_display.insert(tk.END, translate_text(text,detect_text,get_languages())) 
        


    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("OCR Clipboard App")
root.geometry("400x300")

# Create a button to paste the image
paste_button = tk.Button(root, text="Paste Image (Ctrl + V)", command=paste_image_and_translate)
paste_button.pack(pady=20)


clicked = StringVar()
clicked.set("vietnamese")

drop = OptionMenu(root,clicked,*languages_key)
drop.pack()
# Create a text box to display recognized text
text_display = tk.Text(root, wrap=tk.WORD, height=5)
text_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Create translation textboxes
translation_display = tk.Text(root, wrap=tk.WORD, height=5)
translation_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Bind Ctrl+V to the paste function
root.bind('<Control-v>', lambda event: paste_image_and_translate())

# Run the application
root.mainloop()
