import fitz  # PyMuPDF
from ArabicOcr import arabicocr
import cv2
import tempfile
import os

# Path to your PDF file
pdf_path = '1.pdf'
output_directory = 'output_images'

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

    with open('file.txt', 'a', encoding='utf-8') as myfile:
        myfile.write(' '.join(words) + '\n')

    img = cv2.imread(os.path.join(output_directory, f'out_{page_num}.jpg'), cv2.IMREAD_UNCHANGED)
    cv2.imshow("arabic ocr", img)
    cv2.waitKey(0)

pdf_document.close()
