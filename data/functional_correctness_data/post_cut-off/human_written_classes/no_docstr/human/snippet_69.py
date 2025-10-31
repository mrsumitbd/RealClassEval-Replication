import uuid
import requests
from openai import OpenAI
from functools import partial
from tqdm import tqdm
import json
import copy
import random
from typing import List, Optional
from multiprocessing import Process, Queue
import time

class BaseGenerator:

    def __init__(self, remote_engine_url, remote_buffer_url, num_repeat_per_sample=1, queue_size=1000000, num_process=10, task_type='math', max_tokens=4096, num_repeats=10, skip_instance_ids: Optional[List[str]]=None):
        self.queue_size = queue_size
        self.num_process = num_process
        self.remote_engine_url = remote_engine_url
        self.remote_buffer_url = remote_buffer_url
        self.num_repeat_per_sample = num_repeat_per_sample
        self.task_type = task_type
        self.max_tokens = max_tokens
        self.num_repeats = num_repeats
        self.skip_instance_ids = list(skip_instance_ids) if skip_instance_ids is not None else None
        if self.skip_instance_ids is not None:
            print(f'BaseGenerator initialized with {len(self.skip_instance_ids)} instance_ids to skip')
            self.skip_instance_ids = self.skip_instance_ids * self.num_repeat_per_sample
        if '/v1' in remote_engine_url:
            self.client = OpenAI(api_key='test', base_url=remote_engine_url)
        else:
            remote_engine_url = remote_engine_url.strip('/') + '/v1'
            self.client = OpenAI(api_key='test', base_url=remote_engine_url)

    def send_data_to_buffer(self, data):
        remote_buffer_url = self.remote_buffer_url.rstrip('/') + '/buffer/write'
        for _ in range(2):
            try:
                response = requests.post(remote_buffer_url, json=data)
                if response.status_code == 200:
                    break
                else:
                    print(f'send data to buffer failed, status code: {response.status_code}')
                    continue
            except Exception as e:
                print(f'send data to buffer failed, error: {e}')
                continue

    def run(self, input_file, rollout_func, reward_func):
        task_queue, done_queue = (Queue(maxsize=self.queue_size), Queue(maxsize=self.queue_size))

        def read_data_into_queue():
            cnt = 0
            items = []
            skipped_count = 0
            with open(input_file, 'r') as f:
                for i, line in enumerate(f):
                    item = json.loads(line)
                    if 'instance_id' not in item:
                        item['instance_id'] = i
                    items.append(item)
            random.shuffle(items)
            for _ in range(self.num_repeats):
                for item in items:
                    for _ in range(self.num_repeat_per_sample):
                        item_repeat = copy.deepcopy(item)
                        if 'uid' not in item_repeat:
                            item_repeat['uid'] = str(uuid.uuid4())
                        if self.skip_instance_ids is not None and item_repeat['instance_id'] in self.skip_instance_ids:
                            print(f"Skipping instance_id: {item_repeat['instance_id']}")
                            self.skip_instance_ids.remove(item_repeat['instance_id'])
                            skipped_count += 1
                            continue
                        task_queue.put(item_repeat)
                    cnt += 1
                time.sleep(300)
            if skipped_count > 0:
                remaining_skip_count = len(self.skip_instance_ids) if self.skip_instance_ids is not None else 0
                print(f'Rollout summary: skipped {skipped_count} instance_ids, {remaining_skip_count} still in skip list')
            for _ in range(self.num_process):
                task_queue.put('STOP')
        processes = []
        SAMPLING_PARAMS['max_tokens'] = self.max_tokens
        for _ in range(self.num_process):
            process = Process(target=partial(worker_process, client=self.client, sampling_params=SAMPLING_PARAMS), args=(task_queue, done_queue, rollout_func, reward_func))
            process.start()
            processes.append(process)
        process = Process(target=read_data_into_queue)
        process.start()
        progress_bar = tqdm()
        num_finished = 0
        while num_finished < self.num_process:
            item = done_queue.get()
            if item == 'COMPLETE':
                num_finished += 1
            else:
                assert 'reward' in item, f'reward not in item: {item}'
                assert 'instance_id' in item, f'instance_id not in item: {item}'
                self.send_data_to_buffer(item)
                progress_bar.update(1)
        progress_bar.close()
        return 'finished'

    def entry(self, input_file, rollout_func, reward_func, num_epoch=1):
        for _ in range(num_epoch):
            status = self.run(input_file, rollout_func, reward_func)