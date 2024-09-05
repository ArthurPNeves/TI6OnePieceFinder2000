import cv2
from skimage.metrics import structural_similarity as ssim
from concurrent.futures import ThreadPoolExecutor
import ImageDownsizer, ImageFinder, ImageConverter, ImageSplitter, EpisodeToFrames


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
    rawInputfolder = './ProcessingInput'
    # Caminho para a pasta de saída onde as imagens redimensionadas serão salvas
    donwSizeOutput = './ImageProcessing/DownSizeImages'

    # Fator de escala para redimensionar as imagens (ex: 0.5 = 50% do tamanho original)
    scale_factor = 0.0625

    # Create an instance of ImageDownsizer
    downsizer = ImageDownsizer.ImageDownsizer(scale_factor)
    # Executa o redimensionamento das imagens na pasta
    downsizer.downscale_folder_images(rawInputfolder, donwSizeOutput)
    ####
    
    ####IMAGE CONVERTER DEMONSTRATION
    # Usage example
    donwSizeInput = donwSizeOutput
    convertedOutput = './ImageProcessing/GrayScaleImage'
    converter = ImageConverter.ImageConverter(donwSizeInput, convertedOutput)
    converter.convert_images_to_gray()
    ####
    
    ####IMAGE SPLITTER DEMONSTRATION    
    convertedInput = convertedOutput  # Substitua pelo caminho da sua pasta de entrada
    output_folder = './ProcessedOutput'  # Substitua pelo caminho da sua pasta de saída

    splitter = ImageSplitter.ImageSplitter(convertedInput, output_folder)
    splitter.split_folder_images()
    ####



if __name__ == '__main__':
    
    
    ####VIDEO TO FRAMES DEMONSTRATION
    #video_path = 'op1.mkv'
    #processedInput = './ProcessedInput'
#
    #video_to_frames = EpisodeToFrames(video_path, processedInput)
    #video_to_frames.extract_frames()
    ####

    
    
    
    ####IMAGE LOADING AND SEARCHING
    
    finder = ImageFinder.ImageFinder()
    # Caminho para a imagem do usuário
    user_image_path = './DesiredFrame/nami40x30.jpg'
    # Caminho para a pasta com imagens
    folder_path = './ProcessedOutput'

    imageProcessing()

    # Carrega a imagem do usuário
    user_image = cv2.imread(user_image_path)
    # Compara a imagem do usuário com as imagens na pasta
    top_matches = finder.compare_images(user_image, folder_path)

    # Imprime os nomes das 3 imagens mais semelhantes
    print("As 3 imagens mais semelhantes são:")
    for score, filename in top_matches:
        print(f"{filename} com SSIM: {score:.4f}")
    ####
