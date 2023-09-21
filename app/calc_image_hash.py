import cv2
import difflib


def calc_image_hash(img):
    """Функция вычисления хэша входящей картинки"""
    image = cv2.imread(img)  # Прочитать картинку
    resized = cv2.resize(
        image, (8, 8), interpolation=cv2.INTER_AREA
    )  # Уменьшить картинку
    gray_image = cv2.cvtColor(
        resized, cv2.COLOR_BGR2GRAY
    )  # Перевод картинки в ч/б формат

    avg = (
        gray_image.mean()
    )  # среднее значение яркости пикселей на черно-белом изображении
    ret, threshold_image = cv2.threshold(
        gray_image, avg, 255, 0
    )  # Бинаризация по порогу (будет представлять собой черно-белое изображение, где объекты обычно являются белыми на черном фоне)

    # Расчет хэша
    _hash = ""
    for x in range(8):
        for y in range(8):
            val = threshold_image[x, y]
            if val == 255:
                _hash = _hash + "1"
            else:
                _hash = _hash + "0"

    return _hash

