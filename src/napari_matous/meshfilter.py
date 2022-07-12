from magicgui import magic_factory
import napari
import open3d as o3d
from napari.qt.threading import thread_worker
from typing_extensions import Annotated
from pathlib import Path
from napari.layers import Surface
import numpy as np


@magic_factory(call_button='View Mesh')
def load_mesh(viewer: "napari.viewer.Viewer",
              mesh_path: Path,
              filter_choice: Annotated[str, {"choices": ["None",
                                                         "Filter Sharpen",
                                                         "Filter Smooth Laplacian",
                                                         "Filter Smooth Simple",
                                                         "Filter smooth Taubin"]}]
              ):
    def view_data(mesh_obj):
        surface = (np.asarray(mesh_obj.vertices), np.asarray(mesh_obj.triangles))
        viewer.add_surface(surface, name=mesh_path.name + '_mesh')

    @thread_worker()
    def filter_sharpen(mesh_obj):
        return o3d.geometry.TriangleMesh.filter_sharpen(mesh_obj)

    @thread_worker
    def filter_smooth_laplacian(mesh_obj):
        return o3d.geometry.TriangleMesh.filter_smooth_laplacian(mesh_obj)

    @thread_worker
    def filter_smooth_simple(mesh_obj):
        return o3d.geometry.TriangleMesh.filter_smooth_simple(mesh_obj)

    @thread_worker
    def filter_smooth_taubin(mesh_obj):
        return o3d.geometry.TriangleMesh.filter_smooth_taubin(mesh_obj)

    mesh = o3d.io.read_triangle_mesh(str(mesh_path))

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
