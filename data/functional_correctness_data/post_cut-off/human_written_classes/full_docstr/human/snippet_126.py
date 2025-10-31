import torch
from third_party.gsnet.utils.collision_detector import ModelFreeCollisionDetector
from graspnetAPI import Grasp, GraspGroup
from third_party.gsnet.models.graspnet import GraspNet, pred_decode
import open3d as o3d
import time
import numpy as np
from third_party.gsnet.dataset.graspnet_dataset import minkowski_collate_fn

class GSNet:
    """This class is used to grasp an object from a point cloud."""

    def __init__(self):
        """This function is used to initialize the configuration."""
        self.checkpoint_path = 'third_party/gsnet/assets/minkuresunet_realsense_tune_epoch20.tar'
        self.seed_feat_dim = 512
        self.num_point = 15000
        self.batch_size = 1
        self.voxel_size = 0.005
        self.collision_thresh = 0.01
        self.voxel_size_cd = 0.01
        self.infer = False
        self.vis = False
        self.dump_dir = 'logs'
        self.camera = 'realsense'
        self.scene = '0188'
        self.index = '0000'

    def inference(self, cloud_masked, max_grasps=200):
        """This function is used to infer the grasp from the point cloud."""
        if len(cloud_masked) >= self.num_point:
            idxs = np.random.choice(len(cloud_masked), self.num_point, replace=False)
        else:
            idxs1 = np.arange(len(cloud_masked))
            idxs2 = np.random.choice(len(cloud_masked), self.num_point - len(cloud_masked), replace=True)
            idxs = np.concatenate([idxs1, idxs2], axis=0)
        cloud_sampled = cloud_masked[idxs]
        data_dict = {'point_clouds': cloud_sampled.astype(np.float32), 'coors': cloud_sampled.astype(np.float32) / self.voxel_size, 'feats': np.ones_like(cloud_sampled).astype(np.float32)}
        batch_data = minkowski_collate_fn([data_dict])
        net = GraspNet(seed_feat_dim=self.seed_feat_dim, is_training=False)
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        net.to(device)
        checkpoint = torch.load(self.checkpoint_path)
        net.load_state_dict(checkpoint['model_state_dict'])
        net.eval()
        tic = time.time()
        for key in batch_data:
            if 'list' in key:
                for i in range(len(batch_data[key])):
                    for j in range(len(batch_data[key][i])):
                        batch_data[key][i][j] = batch_data[key][i][j].to(device)
            else:
                batch_data[key] = batch_data[key].to(device)
        with torch.no_grad():
            end_points = net(batch_data)
            if end_points is None:
                return None
            grasp_preds = pred_decode(end_points)
        preds = grasp_preds[0].detach().cpu().numpy()
        gg = GraspGroup(preds)
        if self.collision_thresh > 0:
            cloud = data_dict['point_clouds']
            mfcdetector = ModelFreeCollisionDetector(cloud, voxel_size=self.voxel_size_cd)
            collision_mask_mfc = mfcdetector.detect(gg, approach_dist=0.05, collision_thresh=self.collision_thresh)
            gg = gg[~collision_mask_mfc]
        gg = gg.nms()
        gg = gg.sort_by_score()
        if gg.__len__() > max_grasps:
            gg = gg[:max_grasps]
        return gg

    def visualize(self, cloud, gg: GraspGroup=None, g: Grasp=None, image_only=False):
        """This function is used to visualize the grasp group or grasp."""
        pcd = cloud
        if image_only:
            points = np.asarray(pcd.points)
            rotation = np.array([[0, 1, 0], [0, 0, -1], [-1, 0, 0]])
            rotation_along_x = np.array([[1, 0, 0], [0, np.cos(70), -np.sin(70)], [0, np.sin(70), np.cos(70)]])
            rotation = rotation_along_x @ rotation
            points = points @ rotation.T
            pcd.points = o3d.utility.Vector3dVector(points)
            vis = o3d.visualization.Visualizer()
            vis.create_window(visible=True)
            vis.add_geometry(pcd)
            grippers = gg.to_open3d_geometry_list()
            vertices = np.asarray(grippers[0].vertices)
            vertices = vertices @ rotation.T
            grippers[0].vertices = o3d.utility.Vector3dVector(vertices)
            vis.add_geometry(*grippers)
            vis.poll_events()
            vis.update_renderer()
            image = vis.capture_screen_float_buffer()
            import imageio
            image = np.asarray(image)
            imageio.imwrite('get_started/output/motion_planning/gsnet_visualization.png', (image * 255).astype(np.uint8))
            vis.destroy_window()
            return
        if gg is not None:
            grippers = gg.to_open3d_geometry_list()
            o3d.visualization.draw_geometries([pcd, *grippers])
        elif g is not None:
            gripper = g.to_open3d_geometry()
            o3d.visualization.draw_geometries([pcd, gripper])
        else:
            o3d.visualization.draw_geometries([pcd])