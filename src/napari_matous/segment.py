from skimage.filters import threshold_otsu, try_all_threshold
from skimage.morphology import closing, square
from skimage.color import rgb2gray
from napari.layers import Labels
from magicgui import magic_factory
from napari.layers import Image


def segment(image):
    thresh = threshold_otsu(image)
    bw = closing(image > thresh, square(3))
    return bw


@magic_factory(layout='vertical', call_button='Segment')
def segment_image(image: Image) -> Labels:

    if image.rgb:
        image = rgb2gray(image.data)

    label_image = segment(image)

    return Labels(label_image, name='segmentation', color={0: 'black', 1: 'white'})
