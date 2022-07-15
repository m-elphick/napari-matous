"""
gamer

Provides the gamer tools coarse,
scale and smooth to be applied to meshes.
"""
import pygamer
import napari
import meshio
import os
from magicgui import magic_factory
from pathlib import Path
from typing_extensions import Annotated
from napari.qt.threading import thread_worker


@magic_factory(call_button="Confirm Choices")
def gamer_tool(viewer: "napari.viewer.Viewer",
               input_mesh_path: Path,
               output_mesh_path: Annotated[Path, {"mode": "d"}],
               method_choice: Annotated[str, {"choices": ["Coarse",
                                                          "Scale",
                                                          "Smooth"]}]):
    """

    Tool that takes a mesh and provides three gamer
    tools coarse, scale and smooth to be applied to
    the mesh.

    Also gives the option to output the mesh to a
    user specified directory.

    Args:
        viewer: Layers of the napari viewer.
        input_mesh_path: Path to the input mesh.
        output_mesh_path: Path to the output directory.
        method_choice: Gamer method to be used (coarse, scale, mesh).

    Returns:
        Mesh that has had a gamer method applied to it.
    """
    def read_mesh_file():
        """
        Reads a users' mesh file and returns a pygamer
        'SurfaceMesh' to be used to apply the gamer
        methods to.

        If the user input a non .obj file then it
        will be read into a meshio mesh, then create
        a new file "input_mesh.obj" which will then be
        read into pygamer using the 'readOBJ' function

        Returns:
            A pygamer SurfaceMesh object of the users inputted mesh.
        """
        if str(input_mesh_path).endswith('.obj'):
            return pygamer.readOBJ(str(input_mesh_path))
        temp_mesh = meshio.read(str(input_mesh_path))
        temp_mesh.write("input_mesh.obj")
        return pygamer.readOBJ('input_mesh.obj')

    def output_mesh(method_output):
        """
        Outputs the processed mesh to the napari viewer
        as well as saves it as an .obj file if the user
        has selected an output directory.

        Args:
            method_output: The processed mesh that has been outputted
            from one of the gamer methods.

        Returns:
            A surface layer of the processed mesh to the napari
            viewer and or a .obj file representation of the processed
            mesh.
        """
        mesh = method_output[0]
        method_name = method_output[1]
        vertices, edges, faces = mesh.to_ndarray()
        viewer.add_surface((vertices, faces), name=str(input_mesh_path.name)+method_name)
        if str(output_mesh_path) != '.':
            file = open(str(output_mesh_path) + '/output_mesh.obj', 'w+')
            pygamer.writeOBJ(file.name, mesh)
            file.close()
        if os.path.exists('input_mesh.obj'):
            os.remove('input_mesh.obj')

    @thread_worker
    def gamer_coarse(mesh, rate, flat_rate, dense_weight):
        """
        Function that applies the coarse gamer function to
        the user inputted mesh.

        Args:
            mesh: User inputted mesh.
            rate: Threshold value for coarsening.
            flat_rate: Priority of decimating flat regions.
            dense_weight: Priority of decimating dense regions.

        Returns:
            Mesh which has had the coarse function applied to it.
        """
        mesh.coarse(rate=rate, flatRate=flat_rate, denseWeight=dense_weight)
        return mesh, "_coarse"

    @thread_worker
    def gamer_scale(mesh, scale):
        """
        Function that applies the scale gamer function to
        the user inputted mesh.

        Args:
            mesh: User inputted mesh.
            scale: Scale factor.

        Returns:
            Mesh which has had the coarse function applied to it.
        """
        mesh.scale(scale)
        mesh.fillHoles()
        return mesh, "_scale"

    @thread_worker
    def gamer_smooth(mesh, max_iter, preserve_ridges, ring):
        """
        Function that applies the smooth gamer function to the
        user inputted mesh.

        Args:
            mesh: User inputted mesh.
            max_iter: Maximum number of smoothing iterations.
            preserve_ridges: Prevent flipping of edges along ridges.
            ring: Number of LST rings to consider.

        Returns:
            Mesh which has had the smooth function applied to it.
        """
        mesh.smooth(max_iter=max_iter, preserve_ridges=preserve_ridges, rings=ring)
        return mesh, "_smooth"

    @magic_factory
    def coarse_gui(rate: float = 1,
                   flat_rate: float = 1,
                   dense_weight: float = 1):
        """
        The GUI of te coarse function which gets
        the users parameters for applying the coarse
        function.

        Args:
            rate: Threshold value for coarsening.
            flat_rate: Priority of decimating flat regions.
            dense_weight: Priority of decimating dense regions.

        Returns:
            A surface layer to the napari viewer containing the processed
            mesh and optionally a file containing the processed mesh.
        """
        mesh = read_mesh_file()
        mesh.compute_orientation()
        mesh.correctNormals()
        for v in mesh.vertexIDs:
            v.data().selected = True
        coarse_worker = gamer_coarse(mesh, rate, flat_rate, dense_weight)
        coarse_worker.returned.connect(output_mesh)
        coarse_worker.start()

    @magic_factory
    def scale_gui(scale: float = 1.0):
        """
            The GUI of te scale function which gets
            the users parameters for applying the scale
            function.
        Args:
            scale: Scale factor.

        Returns:
            A surface layer to the napari viewer containing the processed
            mesh and optionally a file containing the processed mesh.
        """
        mesh = read_mesh_file()
        mesh.compute_orientation()
        mesh.correctNormals()
        for v in mesh.vertexIDs:
            v.data().selected = True
        scale_worker = gamer_scale(mesh, scale)
        scale_worker.returned.connect(output_mesh)
        scale_worker.start()

    @magic_factory
    def smooth_gui(max_iterations: int = 6,
                   preserve_ridges: bool = False,
                   ring: int = 2):
        """
            The GUI of te smooth function which gets
            the users parameters for applying the smooth
            function.
        Args:
            max_iterations: Maximum number of smoothing iterations.
            preserve_ridges: Prevent flipping approach.
            ring: Number of LST rings to consider.

        Returns:
            A surface layer to the napari viewer containing the processed
            mesh and optionally a file containing the processed mesh.
        """
        mesh = read_mesh_file()
        mesh.compute_orientation()
        mesh.correctNormals()
        for v in mesh.vertexIDs:
            v.data().selected = True
        smooth_worker = gamer_smooth(mesh, max_iterations, preserve_ridges, ring)
        smooth_worker.returned.connect(output_mesh)
        smooth_worker.start()

    if method_choice == 'Coarse':
        coarse_gui().show()
    elif method_choice == 'Scale':
        scale_gui().show()
    elif method_choice == 'Smooth':
        smooth_gui().show()
