import cv2
import os

class ImageSplitter:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def split_image_horizontally(self, image):
        """
        Divide uma imagem em duas metades horizontais (superior e inferior).

        Args:
            image (numpy.ndarray): A imagem a ser dividida.

        Returns:
            tuple: Duas metades da imagem (superior, inferior).
        """
        height, width = image.shape[:2]
        mid_point = height // 2

        top_half = image[:mid_point, :]
        bottom_half = image[mid_point:, :]

        return top_half, bottom_half

    def split_folder_images(self):
        """
        Divide todas as imagens em uma pasta de entrada em duas metades horizontais
        e salva as metades em uma pasta de saída.
        """
        # Verifica se a pasta de saída existe; se não, cria-a
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            print(f"Pasta de saída '{self.output_folder}' criada.")
        else:
            print(f"Pasta de saída '{self.output_folder}' já existe.")

        # Extensões de arquivos suportadas
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

        # Lista todos os arquivos na pasta de entrada
        files = os.listdir(self.input_folder)
        total_files = len(files)
        processed_files = 0

        for filename in files:
            # Verifica se o arquivo tem uma extensão de imagem válida
            if filename.lower().endswith(valid_extensions):
                input_path = os.path.join(self.input_folder, filename)

                # Carrega a imagem
                image = cv2.imread(input_path)
                if image is None:
                    print(f"Erro ao carregar a imagem: {filename}. Pulando...")
                    continue

                # Divide a imagem em duas metades
                top_half, bottom_half = self.split_image_horizontally(image)

                # Define os nomes dos arquivos de saída
                name, ext = os.path.splitext(filename)
                top_filename = f"{name}_top{ext}"
                bottom_filename = f"{name}_bottom{ext}"

                # Define os caminhos completos para salvar as imagens divididas
                top_output_path = os.path.join(self.output_folder, top_filename)
                bottom_output_path = os.path.join(self.output_folder, bottom_filename)

                # Salva as imagens divididas
                cv2.imwrite(top_output_path, top_half)
                cv2.imwrite(bottom_output_path, bottom_half)

                #print(f"Imagem '{filename}' dividida em '{top_filename}' e '{bottom_filename}'.")
                processed_files += 1

        print(f"\nProcessamento concluído. {processed_files} de {total_files} arquivos foram processados.")