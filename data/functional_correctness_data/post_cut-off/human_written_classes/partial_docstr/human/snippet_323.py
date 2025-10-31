import numpy as np
from typing import List, Tuple, Union

class SurfaceExtractor:

    def _compute_box_stat(self, bounds: Union[Tuple[float], List[float], float], octree_resolution: int):
        """
        Compute grid size, bounding box minimum coordinates, and bounding box size based on input
        bounds and resolution.

        Args:
            bounds (Union[Tuple[float], List[float], float]): Bounding box coordinates or a single
            float representing half side length.
                If float, bounds are assumed symmetric around zero in all axes.
                Expected format if list/tuple: [xmin, ymin, zmin, xmax, ymax, zmax].
            octree_resolution (int): Resolution of the octree grid.

        Returns:
            grid_size (List[int]): Grid size along each axis (x, y, z), each equal to octree_resolution + 1.
            bbox_min (np.ndarray): Minimum coordinates of the bounding box (xmin, ymin, zmin).
            bbox_size (np.ndarray): Size of the bounding box along each axis (xmax - xmin, etc.).
        """
        if isinstance(bounds, float):
            bounds = [-bounds, -bounds, -bounds, bounds, bounds, bounds]
        bbox_min, bbox_max = (np.array(bounds[0:3]), np.array(bounds[3:6]))
        bbox_size = bbox_max - bbox_min
        grid_size = [int(octree_resolution) + 1, int(octree_resolution) + 1, int(octree_resolution) + 1]
        return (grid_size, bbox_min, bbox_size)

    def run(self, *args, **kwargs):
        """
        Abstract method to extract surface mesh from grid logits.

        This method should be implemented by subclasses.

        Raises:
            NotImplementedError: Always, since this is an abstract method.
        """
        return NotImplementedError

    def __call__(self, grid_logits, **kwargs):
        """
        Process a batch of grid logits to extract surface meshes.

        Args:
            grid_logits (torch.Tensor): Batch of grid logits with shape (batch_size, ...).
            **kwargs: Additional keyword arguments passed to the `run` method.

        Returns:
            List[Optional[Latent2MeshOutput]]: List of mesh outputs for each grid in the batch.
                If extraction fails for a grid, None is appended at that position.
        """
        outputs = []
        for i in range(grid_logits.shape[0]):
            try:
                vertices, faces = self.run(grid_logits[i], **kwargs)
                vertices = vertices.astype(np.float32)
                faces = np.ascontiguousarray(faces)
                outputs.append(Latent2MeshOutput(mesh_v=vertices, mesh_f=faces))
            except Exception:
                import traceback
                traceback.print_exc()
                outputs.append(None)
        return outputs