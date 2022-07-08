from skimage.filters import threshold_otsu, try_all_threshold
from skimage.morphology import closing, square
from skimage.color import rgb2gray
from napari.layers import Labels
from magicgui import magic_factory
from napari.layers import Image
import matplotlib.pyplot as plt


def segment(image):
    fig, ax = try_all_threshold(image, figsize=(30, 15), verbose=False)
    plt.show()
    thresh = threshold_otsu(image)
    bw = closing(image > thresh, square(3))
    return bw


@magic_factory(layout='vertical', call_button='Segment')
def segment_image(image: Image) -> Labels:

    print(image.data.shape)

    input_arr = image.data  # np.squeeze(input.data)
    print(input_arr.shape)

    temp_idx = 2 if len(input_arr.shape) == 4 else 1

    print(input_arr.shape[temp_idx:])

    if image.rgb:
        image = rgb2gray(image.data)

    label_image = segment(image)

    return Labels(label_image, name='segmentation', color={0: 'black', 1: 'white'})
