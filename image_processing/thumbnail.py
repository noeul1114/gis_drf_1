from io import BytesIO

from PIL import Image


def generate_thumbnail(input_image):
    # PILLOW 에서 제공하는 Image 클래스 이용 이미지를 열어줌
    img = Image.open(input_image)

    # 이미지 프로세싱 결과물을 임시저장해놓을 메모리를 할당
    output = BytesIO()

    # 이미지 사이즈를 확인하고 비율을 계싼
    width, height = img.size
    ratio = height / width
    pixel = 250

    # 원하는 이미지 사이즈로 이미지를 변형
    img = img.convert('RGB')
    img.thumbnail((pixel, round(pixel * ratio)))

    # 이미지를 이전에 만든 메모리 공간에 저장
    img.save(output, format='JPEG', quality=95)

    # 이미지를 저장하면서 이동한 메모리 포인터를
    # 다시 첫번째 위치로 이동 (밑에 있는 InMemoryUploadedFile 에서
    # 이미지를 읽게 하도록 위함
    output.seek(0)

    return output
