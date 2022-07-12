from skimage.color import rgb2gray, gray2rgb, rgba2rgb
from magicgui import magic_factory
from napari.layers import Image, Labels
from stardist.models import StarDist2D
from typing_extensions import Annotated
from csbdeep.utils import normalize
from stardist.data import test_image_nuclei_2d
from napari.qt.threading import thread_worker


@magic_factory(call_button='Segment')
def stardist_segment_image(image: Image,
                           viewer: "napari.viewer.Viewer",
                           model_choice: Annotated[str, {"choices": ["2D versatile fluo",
                                                                     "2D versatile he"]}]):
    def get_data(return_value):
        data = return_value
        viewer.add_labels(data, name='Stardist Segmentation')

    @thread_worker
    def segment_2d_versatile_fluo(img):

        # print(img.data.shape[2])

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

        if not img.rgb:
            img = gray2rgb(img.data)

        model = StarDist2D.from_pretrained('2D_versatile_he')
        labels, _ = model.predict_instances(normalize(img.data))

        return labels

    if model_choice == "2D versatile fluo":
        worker = segment_2d_versatile_fluo(image)
        worker.returned.connect(get_data)
        worker.start()
    else:
        worker = segment_2d_versatile_he(image)
        worker.returned.connect(get_data)
        worker.start()
