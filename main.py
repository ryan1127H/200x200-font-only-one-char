import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def get_unique_filename(base_name, extension=".png"):
    filename = f"{base_name}{extension}"
    counter = 1
    
    while os.path.exists(filename):
        filename = f"{base_name}_{counter}{extension}"
        counter += 1
        
    return filename

def generate_char_image(char, font_path, size=200):
    image = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)

    font_size = int(size * 0.75)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        print("폰트 경로 이상함")
        return

    bbox = draw.textbbox((0, 0), char, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (size - text_width) / 2 - bbox[0]
    y = (size - text_height) / 2 - bbox[1]

    draw.text((x, y), char, fill=(0, 0, 0, 255), font=font)

    # 중복되지 않는 파일 이름 생성
    output_filename = get_unique_filename(char)

    image.save(output_filename)
    print(f"저장 완료: {output_filename}")

if __name__ == "__main__":
    target_char = input("한글 한 글자 입력: ").strip()
    #여기다가 경로 적기 vvvv 파이썬 특성 상 앞에 r 지우지 말것
    font_file = r"경로" 
    
    if target_char:
        generate_char_image(target_char[0], font_file)