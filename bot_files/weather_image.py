from PIL import Image, ImageDraw, ImageFont
from config import bot_root
from api_module import get_random_string
import messages as msg


async def generator_weather_image(data, ln) -> str:
    """
    Генератор зображення з погодою
    :param data: Дані про погоду
    :return: Готове зображення
    """
    # Фонове зображення
    base = Image.open("%s/weather_back.png" % bot_root).convert("RGBA")

    # Завантажуємо шрифт
    title = ImageFont.truetype("%s/Ubuntu-Medium.ttf" % bot_root, 30)
    t = ImageFont.truetype("%s/Ubuntu-Medium.ttf" % bot_root, 46)
    t_small = ImageFont.truetype("%s/Ubuntu-Medium.ttf" % bot_root, 16)
    des = ImageFont.truetype("%s/Ubuntu-Medium.ttf" % bot_root, 19)

    # Створюємо платформу для малювання
    d = ImageDraw.Draw(base)

    # Наносимо заголовок
    d.text((85, 100), "%s, %s" % (data['name'], data['country']), font=title, fill=(255, 255, 255, 255))

    # Температура
    d.text((83, 54), "%s°" % data['temp'], font=t, fill=(255, 255, 255, 255))
    d.text((400, 290), "%s %s°" % (msg.weather_feel_temp[ln], data['temp']), font=t_small, fill=(255, 255, 255, 255))

    # Опис погоди
    d.text((85, 144), "%s" % data['description'], font=des, fill=(255, 255, 255, 255))

    # Вологість
    d.text((85, 180), "%s: %s%s" % (msg.weather_humidity[ln], data['humidity'], '%'), font=des, fill=(255, 255, 255, 255))

    # Тиск
    d.text((85, 216), "%s: %s %s" % (msg.weather_pressure[ln], data['pressure'], msg.weather_pressure_m[ln]), font=des, fill=(255, 255, 255, 255))

    # Накладає іконку погоди
    icon_dir = '%s/weather_icons/%s.png' % (bot_root, data['icon'])
    icon = Image.open(icon_dir)
    base.paste(icon, (373, 88), icon)

    # Отримуємо зображення
    id_ = await get_random_string(16)
    img = 'image_%s.png' % id_
    root_dir = '%s/images/%s' % (bot_root, img)
    base.save(root_dir, 'PNG')

    return root_dir
