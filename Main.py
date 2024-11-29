import cv2
import time
import os
from concurrent.futures import ThreadPoolExecutor
from skimage.metrics import structural_similarity as ssim
import ImageDownsizer
import  ImageFinder


"""
Does The image Processing in a Preset/Custom Order
To make a custom order insert an array of Size 5 with

G - GrayScale
D - Downsize
S - Split

Preset = Downsize, GrayScale, Split
"""
def imageProcessing():
    ######DOWNSIZER DEMOSNTRATION
    # Caminho para a pasta de entrada com imagens originais
    rawInputfolder = 'frames20x15grey'
    # Caminho para a pasta de saída onde as imagens redimensionadas serão salvas
    donwSizeOutput = 'frames40x30grey'

    # Fator de escala para redimensionar as imagens (ex: 0.5 = 50% do tamanho original)
    scale_factor = 0.2

    # Create an instance of ImageDownsizer
    downsizer = ImageDownsizer.ImageDownsizer(scale_factor, 2)
    # Executa o redimensionamento das imagens na pasta
    downsizer.downscale_folder_images(rawInputfolder, donwSizeOutput)
    ####
    
    ####IMAGE CONVERTER DEMONSTRATION
    # Usage example
    #donwSizeInput = donwSizeOutput
    #convertedOutput = './ImageProcessing/GrayScaleImage'
    #converter = ImageConverter.ImageConverter(donwSizeInput, convertedOutput)
    #converter.convert_images_to_gray()
    ####
    
    ####IMAGE SPLITTER DEMONSTRATION    
    #convertedInput = convertedOutput  # Substitua pelo caminho da sua pasta de entrada
    #output_folder = 'frames10x7grey1quarto'  # Substitua pelo caminho da sua pasta de saída

    #splitter = ImageSplitter.ImageSplitter(convertedInput, output_folder)
    #splitter.split_folder_images()
    ####


def get_lmdb_files(folder_path):
    return [f for f in os.listdir(folder_path) if f.endswith('.lmdb')]

if __name__ == '__main__':
     
    
    finder = ImageFinder.ImageFinder(num_threads=2)
    # Caminho para a imagem do usuário
    
    
    # Carregar a imagem original
    caminho_imagem = "frame_11107.jpg"  # Substitua pelo caminho da sua imagem
    imagem = cv2.imread(caminho_imagem)

    # Redimensionar para 20x15 e converter para tons de cinza
    imagem_cinza_20x15 = cv2.resize(imagem, (20, 15))
    imagem_cinza_20x15 = cv2.cvtColor(imagem_cinza_20x15, cv2.COLOR_BGR2GRAY)
    
    # Redimensionar para 40x30 mantendo as cores originais
    imagem_colorida_40x30 = cv2.resize(imagem, (40, 30))
    

    # Caminho para a pasta com arquivos lmdb
    folder_path = 'Teste'

    lmdb_files = get_lmdb_files(folder_path)
    all_top_matches = []

    for lmdb_file in lmdb_files:
        episode_number = lmdb_file.split('_')[1].split('.')[0]
        lmdb_file_path = os.path.join(folder_path, lmdb_file)

        top_matches = finder.compare_images(imagem_cinza_20x15, lmdb_file_path)
        
        for score, filename in top_matches:
            all_top_matches.append((score, filename, episode_number))

    # Ordena todas as correspondências e pega as 100 melhores
    all_top_matches.sort(reverse=False, key=lambda x: x[0])
    top100_matches = all_top_matches[:100]

    print("As 100 imagens mais semelhantes são:")
    for score, filename, episode_number in top100_matches:
        print(f"{filename} do Episódio {episode_number} com PIXEL X PIXEL: {score:.4f}")

    start_time1 = time.time()
    ImagensUpscale = finder.upScaleTop100Images('EpFrames40x30', top100_matches)
    end_time1 = time.time()
    total_time1 = end_time1 - start_time1
    print(f"Tempo total de Upscale: {total_time1:.2f} segundos")

    top3 = finder.compare_imagesImgPaths(imagem_colorida_40x30, ImagensUpscale)

    print("As 3 imagens mais semelhantes são:")
    for score, filename, episodenumber in top3:
        print(f"{filename} com SSIM: {score:.4f} do Episódio {episodenumber}")
        
        
    # Extraindo o número do nome
    number_str = filename.split('_')[1].split('.')[0]  # Divide pelo '_' e depois pega o número antes de '.'
    number = int(number_str)

    # Realizando os cálculos
    result = (number / 44300) * 1.440

    # Aproximando o valor (arredondando para o inteiro mais próximo)
    result_rounded = round(result)
    
    {
        "Episodio": episodenumber,
        "result": result
    }
