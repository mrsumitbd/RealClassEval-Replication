import torch.multiprocessing as mp
from queue import Empty

class ParallelWrapper:

    def __init__(self, cfg_degree: int, sp_ulysses_degree: int, sp_ring_degree: int, tp_degree: int, use_fsdp: bool=False, master_port: int=29500, device_type: str='cuda'):
        super().__init__()
        self._module_name = None
        self.world_size = cfg_degree * sp_ulysses_degree * sp_ring_degree * tp_degree
        spawn_ctx = mp.get_context('spawn')
        self.queue_in = [spawn_ctx.Queue() for _ in range(self.world_size)]
        self.queue_out = spawn_ctx.Queue()
        self.ctx = mp.spawn(_worker_loop, args=(self.world_size, self.queue_in, self.queue_out, cfg_degree, sp_ulysses_degree, sp_ring_degree, tp_degree, use_fsdp, master_port, device_type), nprocs=self.world_size, join=False)

    def load_module(self, init_fn, **kwargs):
        data = ['load_module', init_fn, kwargs]
        for q in self.queue_in:
            q.put(data)
        try:
            res = self.queue_out.get(timeout=PARALLEL_FWD_TIMEOUT_SEC)
            if isinstance(res, Exception):
                raise res
            self._module_name = init_fn.__self__.__name__
        except Empty:
            logger.error('[ParallelWrapper] load_module timeout')
            raise RuntimeError('[ParallelWrapper] load_module timeout')
        except Exception as e:
            logger.error(f'[ParallelWrapper] load_module error: {e}')
            raise RuntimeError(f'[ParallelWrapper] load_module error: {e}')
        logger.info('[ParallelWrapper] load_module done')

    def unload_module(self):
        data = ['unload_module', None, None]
        for q in self.queue_in:
            q.put(data)
        try:
            res = self.queue_out.get(timeout=PARALLEL_FWD_TIMEOUT_SEC)
            if isinstance(res, Exception):
                raise res
        except Empty:
            logger.error('[ParallelWrapper] unload_module timeout')
            raise RuntimeError('[ParallelWrapper] unload_module timeout')
        except Exception as e:
            logger.error(f'[ParallelWrapper] unload_module error: {e}')
            raise RuntimeError(f'[ParallelWrapper] unload_module error: {e}')
        logger.info('[ParallelWrapper] unload_module done')

    def __call__(self, *args, **kwargs):
        data = ['__call__', args, kwargs]
        for q in self.queue_in:
            q.put(data)
        try:
            res = self.queue_out.get(timeout=PARALLEL_FWD_TIMEOUT_SEC)
            if isinstance(res, Exception):
                raise res
        except Empty:
            logger.error(f'[ParallelWrapper] {self._module_name}.__call__ timeout')
            raise RuntimeError(f'[ParallelWrapper] {self._module_name}.__call__ timeout')
        except Exception as e:
            logger.error(f'[ParallelWrapper] {self._module_name}.__call__ error: {e}')
            raise RuntimeError(f'[ParallelWrapper] {self._module_name}.__call__ error: {e}')
        logger.info(f'[ParallelWrapper] {self._module_name}.__call__ done')
        return res

    def __getattr__(self, name):

        def wrapped_func(*args, **kwargs):
            data = [name, args, kwargs]
            for q in self.queue_in:
                q.put(data)
            try:
                res = self.queue_out.get(timeout=PARALLEL_FWD_TIMEOUT_SEC)
                if isinstance(res, Exception):
                    raise res
            except Empty:
                logger.error(f'[ParallelWrapper] {self._module_name}.{name} timeout')
                raise RuntimeError(f'[ParallelWrapper] {self._module_name}.{name} timeout')
            except Exception as e:
                logger.error(f'[ParallelWrapper] {self._module_name}.{name} error: {e}')
                raise RuntimeError(f'[ParallelWrapper] {self._module_name}.{name} error: {e}')
            logger.info(f'[ParallelWrapper] {self._module_name}.{name} done')
            return res
        return wrapped_func

    def __del__(self):
        for p in self.ctx.processes:
            p.terminate()
            p.join()
        for p in self.queue_in:
            p.close()
        self.queue_out.close()