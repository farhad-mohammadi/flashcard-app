from PIL import Image, ImageDraw, ImageFont
from utils.config import FONT_PATH
import arabic_reshaper
from bidi.algorithm import get_display

def create_text_image(text, image_size=(800, 450), text_percentage= (1, 1), dark_mode= False):
    if dark_mode:
        background_color = 'black'
        font_color = 'yellow'
    else:
        background_color = 'white'
        font_color = 'black'
    image = Image.new('RGB', image_size, background_color)
    draw = ImageDraw.Draw(image)
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    text = bidi_text
    font_size = calculate_font_size(text, image_size, text_percentage)
    font = ImageFont.truetype(FONT_PATH, font_size)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    position = ((image_size[0] - text_width) / 2, (image_size[1] - text_height) / 2 )
    draw.text(position, text, font=font, fill=font_color)
    return image

def calculate_font_size(text, image_size, text_percentage, max_font_size=150):
    target_width = image_size[0] * text_percentage[0]
    target_height = image_size[1] * text_percentage[1]
    for font_size in range(max_font_size, 0, -1):
        font = ImageFont.truetype(FONT_PATH, font_size)
        draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        if text_width <= target_width and text_height <= target_height:
            return font_size
    return 1 

create_text_image('Select\na Topics', dark_mode= True)