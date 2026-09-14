import os

from PIL import Image, ImageDraw, ImageFont


# Windows에서 파일명으로 사용할 수 없는 문자
INVALID_FILENAME_CHARS = '<>:"/\\|?*'


def get_unique_filename(base_name, extension=".png"):
    filename = f"{base_name}{extension}"
    counter = 1

    while os.path.exists(filename):
        filename = f"{base_name}_{counter}{extension}"
        counter += 1

    return filename


def make_safe_filename(char):
    # Windows에서 사용할 수 없는 문자만 Unicode 이름으로 변환 <>:"/\\|?* 방지용임
    if char in INVALID_FILENAME_CHARS:
        return f"U+{ord(char):04X}"

    # Windows 예약 파일명 관련 문제 방지
    if char in [".", " "]:
        return f"U+{ord(char):04X}"

    return char


def generate_char_image(char, font_path, size=200):
    image = Image.new(
        "RGBA",
        (size, size),
        (255, 255, 255, 255)
    )

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

    draw.text(
        (x, y),
        char,
        fill=(0, 0, 0, 255),
        font=font
    )

    # 파일명 생성
    safe_filename = make_safe_filename(char)

    output_filename = get_unique_filename(safe_filename)

    image.save(output_filename)

    print(f"저장 완료: {output_filename}")


if __name__ == "__main__":
    target_char = input(
        "문자 1개 입력 (한글/영문/숫자/특수기호): "
    ).strip()

    # 폰트 경로 앞에 r 지우면 안대 !!!! 지울거면 \이거 / 이걸로 바꿔
    font_file = r"C:\Users\ryan\Desktop\새 폴더\Maplestory OTF Light.otf"

    if target_char:
        generate_char_image(target_char[0], font_file)
    else:
        print("문자를 입력해줘.")
