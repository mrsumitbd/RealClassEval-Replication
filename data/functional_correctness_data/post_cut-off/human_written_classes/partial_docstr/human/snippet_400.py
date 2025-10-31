from cosmos_rl.utils.logging import logger
import torch.distributed._functional_collectives as funcol
import torch
from cosmos_rl.utils import constant, network_util
import threading
import time
from datetime import timedelta
from torch import distributed as dist
from cosmos_rl.dispatcher.command import Command, BuildMeshCommand
import torch.distributed.distributed_c10d as c10d

class DistKVStore:

    def __init__(self, group: dist.ProcessGroup, master_rank: int, shutdown_event: threading.Event):
        self.group = group
        self.rank = self.group.rank()
        self.world_size = self.group.size()
        self.master_rank = master_rank if -1 < master_rank < self.world_size else 0
        self.counter = 0
        self.lock = threading.Lock()
        self.shutdown_event = shutdown_event
        self.local_store = None
        self.__init_local_store()

    def __init_local_store(self):
        if self.world_size == 1:
            return
        if self.rank == self.master_rank:
            local_ips = network_util.get_eth_ips()
            assert len(local_ips) > 0, 'No IP addresses found'
            local_ip = local_ips[0]
            free_port = network_util.find_available_port(22000)
            max_retry = 300
            for _ in range(max_retry):
                try:
                    self.local_store = dist.TCPStore(host_name='0.0.0.0', port=free_port, is_master=True, timeout=timedelta(seconds=constant.COSMOS_TCP_STORE_TIMEOUT))
                    break
                except Exception:
                    logger.error(f'[DistKVStore] Failed to bind port {free_port}, try another')
                    time.sleep(1)
                    free_port = network_util.find_available_port(20000)
            logger.info(f'Local store started at {local_ip}:{free_port}')
            dist.broadcast_object_list([local_ip, free_port], src=self.master_rank, device=torch.device('cpu'), group=self.group)
        else:
            broadcast_object_list = [None, None]
            dist.broadcast_object_list(broadcast_object_list, src=self.master_rank, device=torch.device('cpu'), group=self.group)
            local_ip, local_port = broadcast_object_list
            assert local_ip is not None and local_port is not None, 'Failed to broadcast local store info'
            while True:
                try:
                    self.local_store = dist.TCPStore(host_name=local_ip, port=local_port, is_master=False, timeout=timedelta(seconds=constant.COSMOS_TCP_STORE_TIMEOUT))
                    break
                except Exception as e:
                    logger.error(f'Failed to connect to local store: {e}')
                    time.sleep(3)
                    continue

    def blocking_wait(self, keys: list[str]):
        assert self.world_size > 1, 'Only master rank can wait for command'
        timeout = 10
        n_max_retries = max(1, int(constant.COSMOS_TCP_STORE_TIMEOUT / timeout))
        for _ in range(n_max_retries):
            try:
                self.local_store.wait(keys, timedelta(seconds=timeout))
                return
            except Exception as e:
                logger.debug(f'Failed to wait for kv store blocking wait: {e}')
                if self.shutdown_event is not None and self.shutdown_event.is_set():
                    raise RuntimeError('Stop signal received')
        raise RuntimeError('Failed to wait for kv store blocking wait')

    def broadcast_command(self, command: Command, src: int=0) -> Command:
        """
        Broadcast a command to all ranks.
        """
        if self.world_size == 1:
            return command
        __key = f'#BROADCAST-{self.counter}'
        __key_dones = [f'{__key}-done-{i}' for i in range(self.world_size)]
        __last_key = f'#BROADCAST-{self.counter - 1}'
        __last_key_dones = [f'{__last_key}-done-{i}' for i in range(self.world_size)]
        error_raised = False
        cmd = None
        while self.shutdown_event is None or not self.shutdown_event.is_set():
            try:
                if src == self.rank:
                    self.local_store.set(__key, command.pack())
                else:
                    self.blocking_wait([__key])
                cmd_raw = self.local_store.get(__key)
                cmd = Command.depack(cmd_raw)
                self.local_store.set(__key_dones[self.rank], '1')
                self.blocking_wait(__key_dones)
            except Exception as e:
                if self.rank == src:
                    logger.error(f'Failed to broadcast command: {e}')
                error_raised = True
                continue
            finally:
                if not error_raised:
                    if self.rank == src:
                        self.local_store.delete_key(__last_key)
                        for _d in __last_key_dones:
                            self.local_store.delete_key(_d)
                    self.counter += 1
                    break
        return cmd