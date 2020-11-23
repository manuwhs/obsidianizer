from typing import Optional

# import cv2
import numpy as np
from PIL import Image
from wordcloud import STOPWORDS, ImageColorGenerator, WordCloud


def generate_word_cloud_image(
    input_image_filepath: str,
    text: str,
    output_image_filepath: Optional[str] = None,
    background_color: str = "transparent",
) -> WordCloud:
    """ Create that word cloud broh"""
    image = Image.open(input_image_filepath)

    image_rgba = image.convert("RGBA")
    # image_rgba = cv2.cvtColor(image, cv2.COLOR_GRAY2RGBA)

    mask = np.array(image_rgba)

    if background_color == "transparent":
        background_color = "rgba(255, 255, 255, 1)"

    wordcloud = WordCloud(
        background_color=background_color,
        max_words=1000,
        mask=mask,
        stopwords=STOPWORDS,
        mode="RGBA",
    ).generate(text)

    image_colors = ImageColorGenerator(mask)
    wordcloud.recolor(color_func=image_colors)

    # Write image to disk
    if output_image_filepath is not None:
        wordcloud.to_file(output_image_filepath)

    return wordcloud
