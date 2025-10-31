import wandb
from loguru import logger as log
from collections import deque
import torch
import time
import os
import numpy as np
import statistics

class OnPolicyRunner:

    def __init__(self, env, train_cfg, log_dir=None, wandb=False, device='cpu', **kwargs):
        self.cfg = train_cfg['runner']
        self.alg_cfg = train_cfg['algorithm']
        self.policy_cfg = train_cfg['policy']
        self.device = device
        self.env = env
        if self.env.num_privileged_obs is not None:
            num_critic_obs = self.env.num_privileged_obs
        else:
            num_critic_obs = self.env.num_obs
        self.use_vision = self.env.use_vision
        actor_critic_class = eval(self.cfg['policy_class_name'])
        if hasattr(self.env, 'obs_context_len'):
            obs_context_len = self.env.obs_context_len
        else:
            obs_context_len = 1
        args = kwargs['args']
        actor_critic = actor_critic_class(self.env.num_obs, num_critic_obs, self.env.num_actions, obs_context_len=obs_context_len, **self.policy_cfg, device=self.device, args=args).to(self.device)
        alg_class = eval(self.cfg['algorithm_class_name'])
        self.alg = alg_class(actor_critic, device=self.device, **self.alg_cfg)
        self.num_steps_per_env = self.cfg['num_steps_per_env']
        self.save_interval = self.cfg['save_interval']
        self.wandb = wandb
        if self.use_vision:
            obs_vision_shape = [obs_context_len, 3, self.env.cfg.sensor.camera.height, self.env.cfg.sensor.camera.width] if obs_context_len != 1 else [3, self.env.cfg.sensor.camera.height, self.env.cfg.sensor.camera.width]
        else:
            obs_vision_shape = None
        obs_shape = [obs_context_len, self.env.num_obs] if obs_context_len != 1 else [self.env.num_obs]
        self.alg.init_storage(self.env.num_envs, self.num_steps_per_env, obs_shape, obs_vision_shape, [self.env.num_privileged_obs], [self.env.num_actions])
        self.log_dir = log_dir
        self.writer = None
        self.tot_timesteps = 0
        self.tot_time = 0
        self.current_learning_iteration = 0
        self.env.reset()

    def learn(self, num_learning_iterations, init_at_random_ep_len=False, wandb=False):
        if init_at_random_ep_len:
            self.env.episode_length_buf = torch.randint_like(self.env.episode_length_buf, high=int(self.env.max_episode_length))
        obs = self.env.get_observations()
        if self.use_vision:
            obs_vision = self.env.get_visual_observations().to(self.device)
        privileged_obs = self.env.get_privileged_observations()
        critic_obs = privileged_obs if privileged_obs is not None else obs
        obs, critic_obs = (obs.to(self.device), critic_obs.to(self.device))
        self.alg.actor_critic.train()
        ep_infos = []
        ep_metrics = []
        rewbuffer = deque(maxlen=100)
        lenbuffer = deque(maxlen=100)
        donebuffer = deque(maxlen=100)
        cur_reward_sum = torch.zeros(self.env.num_envs, dtype=torch.float, device=self.device)
        cur_episode_length = torch.zeros(self.env.num_envs, dtype=torch.float, device=self.device)
        self.tot_iter = self.current_learning_iteration + num_learning_iterations
        self.start_iter = self.current_learning_iteration
        for it in range(self.start_iter, self.tot_iter):
            start = time.time()
            with torch.inference_mode():
                for i in range(self.num_steps_per_env):
                    if self.use_vision:
                        actions = self.alg.act((obs, obs_vision), (critic_obs, obs_vision))
                    else:
                        actions = self.alg.act(obs, critic_obs)
                    obs, privileged_obs, rewards, dones, infos = self.env.step(actions)
                    if self.use_vision:
                        obs_vision = self.env.get_visual_observations().to(self.device)
                    critic_obs = privileged_obs if privileged_obs is not None else obs
                    obs, critic_obs, rewards, dones = (obs.to(self.device), critic_obs.to(self.device), rewards.to(self.device), dones.to(self.device))
                    self.alg.process_env_step(rewards, dones, infos)
                    if self.log_dir is not None:
                        if 'episode' in infos:
                            ep_infos.append(infos['episode'])
                        if 'episode_metrics' in infos:
                            ep_metrics.append(infos['episode_metrics'])
                        cur_reward_sum += rewards
                        cur_episode_length += 1
                        new_ids = (dones > 0).nonzero(as_tuple=False)
                        rewbuffer.extend(cur_reward_sum[new_ids][:, 0].cpu().numpy().tolist())
                        lenbuffer.extend(cur_episode_length[new_ids][:, 0].cpu().numpy().tolist())
                        donebuffer.append(len(new_ids) / self.env.num_envs)
                        cur_reward_sum[new_ids] = 0
                        cur_episode_length[new_ids] = 0
                stop = time.time()
                collection_time = stop - start
                start = stop
                if self.use_vision:
                    self.alg.compute_returns((critic_obs, obs_vision))
                else:
                    self.alg.compute_returns(critic_obs)
            mean_value_loss, mean_surrogate_loss = self.alg.update()
            stop = time.time()
            learn_time = stop - start
            if self.log_dir is not None:
                self.log(locals())
            if it % self.save_interval == 0:
                self.save(os.path.join(self.log_dir, f'model_{it}.pt'))
            ep_infos.clear()
            ep_metrics.clear()
            self.current_learning_iteration += 1
        self.save(os.path.join(self.log_dir, f'model_{self.current_learning_iteration}.pt'))

    def log(self, locs, width=67, pad=35):
        self.tot_timesteps += self.num_steps_per_env * self.env.num_envs
        self.tot_time += locs['collection_time'] + locs['learn_time']
        iteration_time = locs['collection_time'] + locs['learn_time']
        ep_string = ''
        wandb_dict = {}
        if locs['ep_infos']:
            for key in locs['ep_infos'][0]:
                infotensor = torch.tensor([], device=self.device)
                for ep_info in locs['ep_infos']:
                    if not isinstance(ep_info[key], torch.Tensor):
                        ep_info[key] = torch.Tensor([ep_info[key]])
                    if len(ep_info[key].shape) == 0:
                        ep_info[key] = ep_info[key].unsqueeze(0)
                    infotensor = torch.cat((infotensor, ep_info[key].to(self.device)))
                value = torch.mean(infotensor)
                wandb_dict['Episode/' + key] = value
                ep_string += f"{f'Mean episode {key}:':>{pad}} {value:.4f}\n"
        if locs['ep_metrics']:
            for key in locs['ep_metrics'][0]:
                info = []
                for ep_metric in locs['ep_metrics']:
                    info.append(ep_metric[key])
                value = np.mean(info)
                wandb_dict['Metric/' + key] = value
                ep_string += f"{f'Mean episode metric {key}:':>{pad}} {value:.4f}\n"
        std = self.alg.actor_critic.std.cpu().detach().numpy()
        mean_std = std.mean()
        entropy = self.alg.actor_critic.entropy.detach().mean().item()
        fps = int(self.num_steps_per_env * self.env.num_envs / (locs['collection_time'] + locs['learn_time']))
        if self.wandb:
            wandb_dict['Loss/value_function'] = locs['mean_value_loss']
            wandb_dict['Loss/surrogate'] = locs['mean_surrogate_loss']
            wandb_dict['Loss/entropy'] = entropy
            wandb_dict['Loss/learning_rate'] = self.alg.learning_rate
            wandb_dict['Perf/total_fps'] = fps
            wandb_dict['Perf/collection time'] = locs['collection_time']
            wandb_dict['Perf/learning_time'] = locs['learn_time']
            wandb_dict['Std/mean_std'] = mean_std
            for i, std in enumerate(self.alg.actor_critic.std):
                wandb_dict[f'Std/std_dim_{i}'] = std
            if len(locs['rewbuffer']) > 0:
                wandb_dict['Train/mean_reward'] = statistics.mean(locs['rewbuffer'])
                wandb_dict['Train/mean_episode_length'] = statistics.mean(locs['lenbuffer'])
                wandb_dict['Train/dones'] = statistics.mean(locs['donebuffer'])
            wandb.log(wandb_dict, step=locs['it'])
        str = f" \x1b[1m Learning iteration {locs['it']}/{self.tot_iter} \x1b[0m "
        if len(locs['rewbuffer']) > 0:
            log_string = f"{'#' * width}\n{str.center(width, ' ')}\n\n{'Computation:':>{pad}} {fps:.0f} steps/s (collection: {locs['collection_time']:.3f}s, learning {locs['learn_time']:.3f}s)\n{'Value function loss:':>{pad}} {locs['mean_value_loss']:.4f}\n{'Surrogate loss:':>{pad}} {locs['mean_surrogate_loss']:.4f}\n{'Mean action noise std:':>{pad}} {mean_std:.2f}\n{'Mean reward:':>{pad}} {statistics.mean(locs['rewbuffer']):.2f}\n{'Mean episode length:':>{pad}} {statistics.mean(locs['lenbuffer']):.2f}\n"
        else:
            log_string = f"{'#' * width}\n{str.center(width, ' ')}\n\n{'Computation:':>{pad}} {fps:.0f} steps/s (collection: {locs['collection_time']:.3f}s, learning {locs['learn_time']:.3f}s)\n{'Value function loss:':>{pad}} {locs['mean_value_loss']:.4f}\n{'Surrogate loss:':>{pad}} {locs['mean_surrogate_loss']:.4f}\n{'Mean action noise std:':>{pad}} {mean_std:.2f}\n"
        log_string += ep_string
        eta = self.tot_time / (locs['it'] + 1 - self.start_iter) * (locs['num_learning_iterations'] - (locs['it'] - self.start_iter))
        eta_hrs, eta_mins, eta_secs = (eta // 3600, eta % 3600 // 60, eta % 60)
        tot_hrs, tot_mins, tot_secs = (self.tot_time // 3600, self.tot_time % 3600 // 60, self.tot_time % 60)
        log_string += f"{'-' * width}\n{'Experiment name:':>{pad}} {self.cfg['experiment_name']}\n{'Run name:':>{pad}} {self.cfg['run_name']}\n{'Progress:':>{pad}} {self.start_iter}+{locs['it'] - self.start_iter}/{self.tot_iter - self.start_iter}+{self.start_iter}\n{'Device:':>{pad}} {self.device}\n{'Total timesteps:':>{pad}} {self.tot_timesteps}\n{'Iteration time:':>{pad}} {iteration_time:.2f}s\n{'Total time:':>{pad}} {tot_hrs:.0f} hrs {tot_mins:.0f} mins {tot_secs:.1f} s\n{'ETA:':>{pad}} {eta_hrs:.0f} hrs {eta_mins:.0f} mins {eta_secs:.1f} s\n"
        log.info(log_string)

    def save(self, path, infos=None):
        torch.save({'model_state_dict': self.alg.actor_critic.state_dict(), 'optimizer_state_dict': self.alg.optimizer.state_dict(), 'iter': self.current_learning_iteration, 'infos': infos}, path)

    def load(self, path, load_optimizer=True):
        try:
            loaded_dict = torch.load(path)
        except:
            loaded_dict = torch.load(path, map_location='cuda:0')
        self.alg.actor_critic.load_state_dict(loaded_dict['model_state_dict'], strict=False)
        if load_optimizer:
            self.alg.optimizer.load_state_dict(loaded_dict['optimizer_state_dict'])
        self.current_learning_iteration = loaded_dict['iter']
        return loaded_dict['infos']

    def get_inference_policy(self, device=None, hrl=False):
        self.alg.actor_critic.eval()
        if device is not None:
            self.alg.actor_critic.to(device)
        if hrl:
            return self.alg.actor_critic.act_inference_hrl
        else:
            return self.alg.actor_critic.act_inference