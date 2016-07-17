import os
import logging
from datetime import datetime

import pytz
from tzlocal import get_localzone

class Image():

    dir = ''

    def __init__(self, filename):
        self.filename = filename
        self.path = os.path.join(self.dir, filename)

    @classmethod
    def from_usb_camera(cls):
        """
        Capture a photo from the usb camera. Note that this is somewhat
        unreliable--the RPI should be rebooted after each attempt.
        """
        import pygame.camera
        import pygame.image

        pygame.camera.init()
        logging.debug('Looking for cameras...')
        cam_list = pygame.camera.list_cameras()
        if not cam_list:
            raise RuntimeError('Could not access camera. Are you root?')
        logging.debug('Camera found')
        with pygame.camera.Camera(cam_list[0]) as cam:
            logging.debug('Starting camera...')
            cam.start()
            img = cam.get_image()
            logging.debug('Done')
        pygame.camera.quit()

        rv = cls('{name}.{ext}'.format(
            name=datetime.now().strftime('%m%d%Y%H%M%S'), ext='jpg'))
        pygame.image.save(img, rv.path)
        if not os.path.exists(rv.path):
            raise RuntimeError('No image was created at {p}'.format(p=rv.path))
        logging.info('Saved new image to {p}'.format(p=rv.path))
        return rv

    @classmethod
    def from_file(cls, filename):
        """
        Get a photo from a file. Useful for debugging.
        """

        path = os.path.join(cls.dir, filename)
        if not os.path.exists(path):
            raise RuntimeError('No such file: {p}').format(p=path)
        logging.debug('Found image at {p}'.format(p=path))
        return cls(path)

    def fix(self, rotation=0, brightness=1.5):
        """
        Webcam images tend to be rather dark--this lightens them up.
        Also, it flips it around to match the orientation of the camera.
        """
        from PIL import Image as Img  # Prevent conflict.
        from PIL import ImageEnhance

        img = Img.open(self.path)
        enh = ImageEnhance.Brightness(img)
        enh.enhance(brightness)

        # We only want specific values for rotation.
        assert (rotation == 0 or rotation == 90 or
                rotation == 180 or rotation == 270)
        if rotation == 90:
            img = img.transpose(Img.ROTATE_90)
        elif rotation == 180:
            img = img.transpose(Img.ROTATE_180)
        if rotation == 270:
            img = img.transpose(Img.ROTATE_270)

        img.save(self.path)


class Temperature():

    def __init__(self, reading):
        self.timestamp = datetime.now(tz=get_localzone())
        self.reading = reading

    @classmethod
    def get_from_api(cls, city_id, api_key):
        """Get temperature data from OpenWeatherMap API"""
        import requests

        url = 'http://api.openweathermap.org/data/2.5/'
        url += 'weather?id={id}'.format(id=city_id)
        url += '&APPID={key}'.format(key=api_key)
        url += '&units=metric'
        logging.debug('Requesting data from {url}'.format(url=url))
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        logging.debug('Output: {d}'.format(d=str(data)))
        if not data.get('main') and not data['main'].get('temp'):
            raise RuntimeError('Could not parse temperature data')
        rv = float(data['main']['temp'])
        logging.info('API reports current temp is {t}°C'.format(t=str(rv)))
        return cls(rv)

    @classmethod
    def get_from_sensor(cls):
        """The sensor requires a resistor I don't have. Boo!'"""
        raise NotImplementedError()

    def to_dict(self):
        return dict(
            timestamp=self.timestamp.isoformat(),
            reading=str(self.reading)
        )

    def __str__(self):
        return '{timestamp} {reading}'.format(
            timestamp=self.timestamp.isoformat(),
            reading=str(self.reading)
        )
