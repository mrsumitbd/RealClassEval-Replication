import logging
from os import path as osp
import os
import gmsh

class STPRefine:

    def __init__(self, geo_path, save_path, stpID, index, compute_closest_point=False):
        self.geo_path = geo_path
        self.save_path = save_path
        self.stpID = stpID
        self.index = index
        self.compute_closest_point = compute_closest_point

    def refine_stl(self, boxes, maxsize, minsize):
        src_jsons_path = os.listdir(self.geo_path)
        src_jsons_path = [d for d in os.listdir(self.geo_path) if d.endswith('.json')]
        src_jsons_path = [os.path.join(self.geo_path, d) for d in src_jsons_path]
        for src_path in src_jsons_path:
            copy_json_file(src_path, self.save_path)
        gmsh.initialize()
        gmsh.option.setNumber('General.Terminal', 0)
        gmsh.clear()
        gmsh.model.add('step_mesh')
        step_path = osp.join(self.geo_path, self.stpID)
        gmsh.model.occ.importShapes(step_path)
        gmsh.model.occ.synchronize()
        logging.info('stp loaded.')
        for i in range(len(boxes)):
            refine_box = {'xmin': boxes[i][0][0], 'xmax': boxes[i][1][0], 'ymin': boxes[i][0][1], 'ymax': boxes[i][1][1], 'zmin': boxes[i][0][2], 'zmax': boxes[i][1][2], 'size_min': minsize[i], 'size_max': maxsize[i]}
            logging.info(refine_box)
            global_size = 5.0
            gmsh.model.mesh.field.add('Box', i)
            gmsh.model.mesh.field.setNumber(i, 'XMin', refine_box['xmin'])
            gmsh.model.mesh.field.setNumber(i, 'XMax', refine_box['xmax'])
            gmsh.model.mesh.field.setNumber(i, 'YMin', refine_box['ymin'])
            gmsh.model.mesh.field.setNumber(i, 'YMax', refine_box['ymax'])
            gmsh.model.mesh.field.setNumber(i, 'ZMin', refine_box['zmin'])
            gmsh.model.mesh.field.setNumber(i, 'ZMax', refine_box['zmax'])
            gmsh.model.mesh.field.setNumber(i, 'VIn', refine_box['size_min'])
            gmsh.model.mesh.field.setNumber(i, 'VOut', refine_box['size_max'])
            gmsh.model.mesh.field.setAsBackgroundMesh(i)
            gmsh.option.setNumber('Mesh.MeshSizeMax', global_size)
            gmsh.option.setNumber('Mesh.Algorithm', 2)
            gmsh.model.mesh.generate(2)
            gmsh.model.mesh.optimize('Laplace2D')
            logging.info(f'geom at index {i} re-meshing has been completed.')
        os.makedirs(self.save_path, exist_ok=True)
        gmsh.write(osp.join(self.save_path, f'{self.stpID[:-4]}.stl'))
        logging.info(f"The new stl file is saved to {osp.join(self.save_path, f'{self.stpID[:-4]}.stl')}")
        gmsh.finalize()