import os
import logging

import requests
from enigma_operator import EnigmaOperator

from hambot.models import Image


class Hambot():

    def __init__(self, api_url, key_path):
        self.api_url = api_url
        self.key_path = key_path
        self.e = EnigmaOperator(key_path)

    def upload_image(self, image, token, upload_path='images/'):
        """
        Upload an image to the server using POST and Enigma.
        """

        assert os.path.exists(image.path)

        url = self.api_url + upload_path
        files = {
            'file': open(image.path, 'rb')}
        headers = {
            'Authorization': 'Enigma {t}'.format(t=self.e.encrypt(token))}
        logging.debug('Attempting upload image to {url}'.format(url=url))
        res = requests.post(url, files=files, headers=headers)

        logging.info('Status code: {c}'.format(c=res.status_code))
        for h in res.headers:
            logging.info('{h}: {c}'.format(h=h, c=res.headers[h]))
        logging.info('Content: {c}'.format(c=res.text))
        return res

    def upload_temperature(self, temperature, token, upload_path='temperaturelog/'):
        """
        Upload a temperature reading to the server using POST and Engima.
        """

        assert temperature.reading and temperature.timestamp

        url = self.api_url + upload_path
        data = temperature.to_dict()
        headers = {
            'Authorization': 'Enigma {t}'.format(t=self.e.encrypt(token))}
        logging.debug('Attempting upload temperature to {url}'.format(url=url))
        res = requests.post(url, json=data, headers=headers)

        logging.info('Status code: {c}'.format(c=res.status_code))
        for h in res.headers:
            logging.info('{h}: {c}'.format(h=h, c=res.headers[h]))
        logging.info('Content: {c}'.format(c=res.text))
        return res


