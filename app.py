import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab, Image
import easyocr
import numpy as np

# Initialize the EasyOCR reader
reader = easyocr.Reader(['vi', 'en'])

def get_ocr(image):
    result = reader.readtext(image)
    text = ' '.join([result[i][1] for i in range(len(result))])
    return text

def paste_image():
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
        
        # Display the recognized text
        text_display.delete(1.0, tk.END)  # Clear previous text
        text_display.insert(tk.END, text)  # Insert new text
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("OCR Clipboard App")
root.geometry("400x300")

# Create a button to paste the image
paste_button = tk.Button(root, text="Paste Image (Ctrl + V)", command=paste_image)
paste_button.pack(pady=20)

# Create a text box to display recognized text
text_display = tk.Text(root, wrap=tk.WORD, height=10)
text_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Bind Ctrl+V to the paste function
root.bind('<Control-v>', lambda event: paste_image())

# Run the application
root.mainloop()
