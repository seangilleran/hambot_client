import os
import logging

from hambot import Hambot
from hambot.models import Image, Temperature


# Set up config defaults and make sure everything is in order.
INSTANCE_PATH = os.getenv(
    'HAMBOT_INSTANCE_PATH',
    os.path.join(os.getcwd(), 'instance'))
if not os.path.exists(INSTANCE_PATH):
    os.makedirs(INSTANCE_PATH)

IMAGE_PATH = os.getenv(
    'HAMBOT_IMAGE_PATH',
    os.path.join(INSTANCE_PATH, 'images'))
if not os.path.exists(IMAGE_PATH):
    os.makedirs(IMAGE_PATH)

KEY_PATH = os.getenv(
    'HAMBOT_KEY_PATH',
    os.path.join(INSTANCE_PATH, 'enigma.key'))
if not os.path.exists(KEY_PATH):
    raise RuntimeError('Could not find key file at ' + KEY_PATH)

API_URL = os.getenv('HAMBOT_API_URL', 'http://localhost:5000/api/')
TOKEN = os.getenv('HAMBOT_TOKEN', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')

# Start logging.
DEBUG = os.getenv('HAMBOT_DEBUG', False)
LOG_FILE_PATH = os.getenv(
    'HAMBOT_LOG_FILE_PATH',
    os.path.join(INSTANCE_PATH, 'client.log'))
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filename=LOG_FILE_PATH,
    filemode='a+')
logging.getLogger('').addHandler(logging.StreamHandler())
logging.debug('Hambot configured and operational!')

###

hb = Hambot(API_URL, KEY_PATH)

Image.dir = IMAGE_PATH
img = Image.from_usb_camera()
img.fix(rotation=90)
hb.upload_image(img, TOKEN)

t = Temperature.get_from_sensor()
hb.upload_temperature(t, token)
