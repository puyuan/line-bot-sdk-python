# -*- coding: utf-8 -*-

from linebot import constants


class TestConstants():
    def test_constants(self):
        assert constants.API_URL_BASE == 'https://trialbot-api.line.me'
        assert constants.API_VERSION == 'v1'
        assert constants.API_URL_EVENTS == 'https://trialbot-api.line.me/v1/events'

        assert constants.TO_CHANNEL == 1383378250

    def test_content_type(self):
        assert constants.ContentType.TEXT == 1
        assert constants.ContentType.IMAGE == 2
        assert constants.ContentType.VIDEO == 3
        assert constants.ContentType.AUDIO == 4
        assert constants.ContentType.LOCATION == 7
        assert constants.ContentType.STICKER == 8
        assert constants.ContentType.CONTACT == 10
        assert constants.ContentType.RICH_MESSAGE == 12
