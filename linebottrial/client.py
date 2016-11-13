# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import json
try:
    from urlparse import urlparse, urljoin
except:
    from urllib.parse import urlparse, urljoin

from linebottrial import builders
from linebottrial import constants
from linebottrial import messages
from linebottrial.requests import Request
from linebottrial.users import UserProfile


class LineBotClient():
    def __init__(
        self,
        api_base_url=constants.API_URL_BASE,
        api_version=constants.API_VERSION,
        **credentials
    ):
        self.__base_url = api_base_url
        self.__base_url = self.__generate_url(api_version)
        self.credentials = {
            'X-Line-ChannelID': credentials['channel_id'],
            'X-Line-ChannelSecret': credentials['channel_secret'],
            'X-Line-Trusted-User-With-ACL': credentials['channel_mid'],
        }

    def __generate_url(self, *paths):
        parsed_url = urlparse(self.__base_url)
        path = parsed_url.path.split('/')
        path.extend(paths)
        path = '/'.join(path)
        return urljoin(parsed_url.geturl(), path)

    def validate_signature(self, signature, content):
        return hmac.compare_digest(
            signature.encode('utf-8'),
            base64.b64encode(
                hmac.new(
                    self.credentials['X-Line-ChannelSecret'].encode('utf-8'),
                    msg=content.encode('utf-8'),
                    digestmod=hashlib.sha256
                ).digest()
            )
        )

    @property
    def multiple_message(self):
        return builders.MultipleMessage(self)

    @property
    def rich_message(self):
        return builders.RichMessage(self)

    def send_message(self, to_mid, message):
        request = Request(**{
            'url': self.__generate_url('events'),
            'credentials': self.credentials,
            'to_mid': to_mid,
            'message': message,
        })
        request.validate()
        return request.post()

    def send_text(self, **attrs):
        message = messages.TextMessage(text=attrs['text'])
        return self.send_message(attrs['to_mid'], message)

    def send_image(self, **attrs):
        message = messages.ImageMessage(
            image_url=attrs['image_url'],
            preview_url=attrs['preview_url'],
        )
        return self.send_message(attrs['to_mid'], message)

    def send_video(self, **attrs):
        message = messages.VideoMessage(
            video_url=attrs['video_url'],
            preview_url=attrs['preview_url'],
        )
        return self.send_message(attrs['to_mid'], message)

    def send_audio(self, **attrs):
        message = messages.AudioMessage(
            audio_url=attrs['audio_url'],
            duration=attrs['duration'],
        )
        return self.send_message(attrs['to_mid'], message)

    def send_location(self, **attrs):
        address = attrs.get('address')
        message = messages.LocationMessage(
            title=attrs['title'],
            address=address,
            latitude=attrs['latitude'],
            longitude=attrs['longitude'],
        )
        return self.send_message(attrs['to_mid'], message)

    def send_sticker(self, **attrs):
        message = messages.StickerMessage(
            stkpkgid=attrs['stkpkgid'],
            stkid=attrs['stkid'],
            stkver=attrs['stkver'],
        )
        return self.send_message(attrs['to_mid'], message)

    def __get(self, url):
        request = Request(**{
            'url': url,
            'credentials': self.credentials,
        })
        return request.get()

    def get_message_content(self, message_id):
        path = ['bot', 'message', str(message_id), 'content']
        url = self.__generate_url(*path)
        return self.__get(url)

    def get_message_content_preview(self, message_id):
        path = ['bot', 'message', str(message_id), 'content', 'preview']
        url = self.__generate_url(*path)
        return self.__get(url)

    def get_user_profile(self, *mids):
        url = self.__generate_url('profiles')
        url = '{}?mids={}'.format(url, ','.join(mids))
        response = self.__get(url)
        response_json = response.json()
        return [UserProfile(contact) for contact in response_json['contacts']]
