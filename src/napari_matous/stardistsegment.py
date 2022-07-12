"""
Stardist Segmentation Tool

Tool that applies stardist pre-trained
segmentation models to user inputted
images
"""
from csbdeep.utils import normalize
from magicgui import magic_factory
from napari.layers import Image
from napari.qt.threading import thread_worker
from skimage.color import rgb2gray, gray2rgb, rgba2rgb
from stardist.models import StarDist2D
from typing_extensions import Annotated


@magic_factory(call_button='Segment')
def stardist_segment_image(image: Image,
                           viewer: "napari.viewer.Viewer",
                           model_choice: Annotated[str, {"choices": ["2D versatile fluo",
                                                                     "2D versatile he"]}]):
    """
    Function that takes a user inputted image and
    applies a pre-trained segmentation model of
    their choice and outputs the segmentations as a
    napari Label and adds it to the napari Viewer

    Args:
        image: Image to apply the segmentation to
        viewer: The napari viewer layer
        model_choice: Pre-trained model to segment image

    Returns:
        Napari Label layer containing the segmentations of the user
        inputted image
    """
    def get_data(return_value):
        """
        Gets data outputted from the model and adds it
        to the napari viewer

        Args:
            return_value:
                Outputted segmentations from the segmentation model
        Returns:
            Napari label layer containing the segmentations
        """
        data = return_value
        viewer.add_labels(data, name='Stardist Segmentation')

    @thread_worker
    def segment_2d_versatile_fluo(img):
        """
        Function which applies the stardist
        2D Versatile Fluo segmentation model to the
        user inputted image.

        Args:
            img: Image to apply the segmentation to

        Returns:
            Segmented labels of the inputted image
        """

        model = StarDist2D.from_pretrained('2D_versatile_fluo')

        if not img.rgb:
            labels, _ = model.predict_instances(normalize(img.data))  # gray
            return labels

        if img.data.shape[2] == 4:  # rgba -> rgb -> grey
            img = rgb2gray(rgba2rgb(img.data))
            labels, _ = model.predict_instances(normalize(img))
            return labels

        if img.rgb:
            img = rgb2gray(img.data)  # rgb -> grey
            labels, _ = model.predict_instances(normalize(img))
            return labels

    @thread_worker
    def segment_2d_versatile_he(img):
        """
        Function which applies the stardist
        2D Versatile He segmentation model to the
        user inputted image.

        Args:
            img: Image to apply the segmentation to

        Returns:
            Segmented labels of the inputted image
        """
        if not img.rgb:
            img = gray2rgb(img.data)

        model = StarDist2D.from_pretrained('2D_versatile_he')
        labels, _ = model.predict_instances(normalize(img.data))

        return labels

    # Starts thread worker for each model depending on model choice
    if model_choice == "2D versatile fluo":
        worker = segment_2d_versatile_fluo(image)
        worker.returned.connect(get_data)
        worker.start()
    else:
        worker = segment_2d_versatile_he(image)
        worker.returned.connect(get_data)
        worker.start()
