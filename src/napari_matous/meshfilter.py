"""
Mesh Filter

Tool that allows a user to input a mesh file and
either view it and not apply or a filter, or
apply a filter then view it.
"""
import napari
import numpy as np
import open3d as o3d
from magicgui import magic_factory
from napari.qt.threading import thread_worker
from pathlib import Path
from typing_extensions import Annotated


@magic_factory(call_button='View Mesh')
def load_mesh(viewer: "napari.viewer.Viewer",
              mesh_path: Path,
              filter_choice: Annotated[str, {"choices": ["None",
                                                         "Filter Sharpen",
                                                         "Filter Smooth Laplacian",
                                                         "Filter Smooth Simple",
                                                         "Filter smooth Taubin"]}]
              ):
    """
    Function that apply a filter to
    a user inputted mesh and outputs it
    to the napari viewer

    Args:
        viewer: layers of the napari viewer
        mesh_path: path to the mesh file
        filter_choice: filter to be applied to the mesh

    Returns:
        Mesh with filter applied to the napari viewer
    """
    def view_data(filtered_mesh):
        """
        Takes the output of the filters and adds
        it to the napari viewer

        Args:
            filtered_mesh: The filtered mesh

        Returns:
            Adds surface layer to viewer containing the filtered mesh
        """
        surface = (np.asarray(filtered_mesh.vertices), np.asarray(filtered_mesh.triangles))
        viewer.add_surface(surface, name=mesh_path.name + '_mesh')

    @thread_worker()
    def filter_sharpen(mesh_obj):
        """
        Applies a 'sharpen' filter to a mesh

        Args:
            mesh_obj: Mesh object to be filtered

        Returns:
            Filtered mesh object
        """
        return o3d.geometry.TriangleMesh.filter_sharpen(mesh_obj)

    @thread_worker
    def filter_smooth_laplacian(mesh_obj):
        """
        Applies a 'smooth laplacian' filter to a mesh

        Args:
            mesh_obj: Mesh object to be filtered

        Returns:
            Filtered mesh object
        """
        return o3d.geometry.TriangleMesh.filter_smooth_laplacian(mesh_obj)

    @thread_worker
    def filter_smooth_simple(mesh_obj):
        """
        Applies a 'smooth simple' filter to a mesh

        Args:
            mesh_obj: Mesh object to be filtered

        Returns:
            Filtered mesh object
        """
        return o3d.geometry.TriangleMesh.filter_smooth_simple(mesh_obj)

    @thread_worker
    def filter_smooth_taubin(mesh_obj):
        """
        Applies a 'smooth taubin' filter to a mesh

        Args:
            mesh_obj: Mesh object to be filtered

        Returns:
            Filtered mesh object
        """
        return o3d.geometry.TriangleMesh.filter_smooth_taubin(mesh_obj)

    mesh = o3d.io.read_triangle_mesh(str(mesh_path))  # Reads mesh from file path

    if filter_choice == "None":
        view_data(mesh)
    elif filter_choice == "Filter Sharpen":
        worker = filter_sharpen(mesh)
        worker.returned.connect(view_data)
        worker.start()
    elif filter_choice == "Filter Smooth Laplacian":
        worker = filter_smooth_laplacian(mesh)
        worker.returned.connect(view_data)
        worker.start()
    elif filter_choice == "Filter Smooth Simple":
        worker = filter_smooth_simple(mesh)
        worker.returned.connect(view_data)
        worker.start()
    else:
        worker = filter_smooth_taubin(mesh)
        worker.returned.connect(view_data)
        worker.start()
