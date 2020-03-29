from unittest import TestCase

from gw_bot.api.API_Image import API_Image
from osbot_utils.utils.Dev import Dev


class test_API_Image(TestCase):

    def setUp(self):
        self.img_file = '/tmp/temp_image.png'
        self.api    = API_Image(img_file=self.img_file)
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_add_text(self):
        self.api.new_rgb()
        self.api.add_text('This is some text')
        self.api.save()

    def test_info(self):
        assert self.api.info() == {'error': 'no image'}

    def test_new_rgb(self):
        kvargs = {'color' : 'lightblue' , 'width': 100 , 'height': 100 }
        assert self.api.new_rgb(**kvargs).save().info() == {'height': 100, 'width': 100}