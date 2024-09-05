import cv2
import os

class ImageConverter:
    def __init__(self, folder_path, output_path):
        self.folder_path = folder_path
        self.output_path = output_path

    def convert_images_to_gray(self):
        """
        Converte todas as imagens na pasta para escala de cinza e sobrescreve os arquivos.
        """
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            output_folder = os.path.join(self.output_path, filename)
            # Carrega a imagem
            image = cv2.imread(file_path)

            # Converte para grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Salva a imagem em escala de cinza, sobrescrevendo o arquivo original
            cv2.imwrite(output_folder, gray_image)