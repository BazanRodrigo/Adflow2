import easyocr

def recognize_text(img_path):
    reader = easyocr.Reader(['en'])
    textFinal = []
    texts = reader.readtext(img_path)
    for text in texts:
      textFinal.append(text[1])
    print(textFinal)