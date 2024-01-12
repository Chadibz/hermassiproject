import fitz
from ArabicOcr import arabicocr
import cv2
import tempfile
import os
import tkinter as tk
from tkinter import filedialog

# Function to handle button click and perform OCR
def process_pdf():
    pdf_path = filedialog.askopenfilename(title="Select PDF file", filetypes=[("PDF files", "*.pdf")])
    if not pdf_path:
        return  # User canceled file selection

    output_directory = filedialog.askdirectory(title="Select Output Directory")

    if not output_directory:
        return  # User canceled directory selection

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    pdf_document = fitz.open(pdf_path)

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        image = page.get_pixmap()

        temp_image = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        temp_image.close()
        temp_image_path = temp_image.name

        image.save(temp_image_path)

        # Perform OCR on the generated image
        results = arabicocr.arabic_ocr(temp_image_path, os.path.join(output_directory, f'out_{page_num}.jpg'))
        words = [result[1] for result in results]

        txt_file_path = os.path.join(output_directory, 'output_text.txt')
        with open(txt_file_path, 'a', encoding='utf-8') as myfile:
            myfile.write(' '.join(words) + '\n')

        img = cv2.imread(os.path.join(output_directory, f'out_{page_num}.jpg'), cv2.IMREAD_UNCHANGED)
        cv2.imshow("arabic ocr", img)
        cv2.waitKey(0)

    pdf_document.close()

# Create the main window
root = tk.Tk()
root.title("Arabic OCR PDF Reader")

# Create and place the button
button = tk.Button(root, text="Select PDF", command=process_pdf)
button.pack(pady=20)

# Start the main loop
root.mainloop()
