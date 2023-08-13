import unittest

from ...app.imagesource.Imagesource import Imagesource, Image


class TestImagesourceClass(unittest.TestCase):

    def setUp(self) -> None:
        self.imagesource =  Imagesource()
        
        self.image1 = Image("test", "https://example.com", self.imagesource)
        self.image2 = Image("second-test", "https://example.com", self.imagesource)
        
        self.imagesource.images=[self.image1, self.image2]


    def tearDown(self) -> None:
        self.imagesource = None
    
    def test_get_image_by_name(self):
        image1_from_imagesource = self.imagesource.get_image_by_name("test")
        image2_from_imagesource = self.imagesource.get_image_by_name("second-test")

        self.assertEqual(image1_from_imagesource, self.image1)
        self.assertEqual(image2_from_imagesource, self.image2)

    def test_get_non_existant_image(self):
        image_from_imagesource = self.imagesource.get_image_by_name("non-existant")

        self.assertIsNone(image_from_imagesource)

if __name__ == "__main__":
    unittest.main()