import cv2
import os

def convert_images_to_gray(folder_path):
    """
    Converte todas as imagens na pasta para escala de cinza e sobrescreve os arquivos.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        outputFolder = os.path.join('t1', filename)
        # Carrega a imagem
        image = cv2.imread(file_path)

        # Converte para grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Salva a imagem em escala de cinza, sobrescrevendo o arquivo original
        
        cv2.imwrite(outputFolder, gray_image)

folder_path = 't1'
output_path = 't1'
convert_images_to_gray(folder_path)
