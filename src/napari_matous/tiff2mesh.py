"""
Tiff 2 Mesh

Tool which converts biological tiff segmentation
ground truth into 3D meshes using marching cubes
algorithm and provides the option to save the mesh
to a desired location.
"""
import open3d
import numpy as np
import napari
from napari.qt.threading import thread_worker
from magicgui import magic_factory
from scipy import ndimage as ndi
from pathlib import Path
from skimage.io import imread
from skimage.measure import marching_cubes
from typing_extensions import Annotated


@magic_factory(call_button='Create Mesh')
def tiff_2_mesh(viewer: "napari.viewer.Viewer",
                tiff_path: Path,
                output_path: Annotated[Path, {"mode": "d"}]):
    """
    Tool which takes the inputted tiff mesh
    and output directory and generates a triangle
    mesh and optionally saves it to a directory of
    the users choice.

    Args:
        output_path: Directory of the output file
        viewer: layers of the napari viewer
        tiff_path: path to the tiff stack

    Returns:
        3D mesh representation of the tiff stack
        and optionally saves the mesh to a
        desired directory.
    """

    def tiff_preprocessing(stack):
        """
        Fills any holes or gaps int the
        tiff segmentations.

        Args:
            stack: Stack of images stored as ndarray

        Returns:
            ndarray of tiff images with any holes filled
        """
        filled_stack = np.empty(np.array(stack).shape)

        for i in range(len(stack)):
            filled_stack[i] = ndi.binary_fill_holes(stack[i])

        return filled_stack

    @thread_worker
    def create_mesh(stack):
        """
        Creates a 3D mesh using the inputted stack
        using the 'marching cubes' algorithm provided
        by 'scikit.measure'

        Args:
            stack: ndarray of images to convert into the mesh

        Returns: vertices and triangles as a ndarray

        """
        verts, faces, _, _ = marching_cubes(stack, spacing=(4, 1, 1))

        mesh = open3d.geometry.TriangleMesh()

        mesh.vertices = open3d.utility.Vector3dVector(np.array(verts))
        mesh.triangles = open3d.utility.Vector3iVector(np.array(faces).astype(np.int64))

        return np.asarray(mesh.vertices), np.asarray(mesh.triangles), mesh

    def view_data(mesh):
        """
        Adds the generated mesh to the napari viewer by adding a new
        napari surface layer, and optionally saves the file to a directory
        of the users choice.

        Args:
            mesh: generated mesh stored as vertices and triangles
            to be added to the napari viewer

        Returns:
            napari surface layer of mesh is added to the viewer
        """
        if str(output_path) != '.':
            file = open(str(output_path)+'/output.obj', 'w+')
            open3d.io.write_triangle_mesh(file.name, mesh[2])
            file.close()

        viewer.add_surface((mesh[0], mesh[1]), name=tiff_path.name + '_mesh')

    assert str(tiff_path) != '.', "Tiff path is empty, please select valid path"

    tiff_stack = imread(str(tiff_path))  # Reads the tiff file

    processed_stack = tiff_preprocessing(tiff_stack)  # Fills any holes or gaps in the segmentations

    # Starts thread for the 'create_mesh' function
    worker = create_mesh(processed_stack)
    worker.returned.connect(view_data)
    worker.start()
