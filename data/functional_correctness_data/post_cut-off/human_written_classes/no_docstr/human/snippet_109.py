import subprocess

class NvidiaSmiUtil:

    @staticmethod
    def get_nvlink_adjacency_matrix():
        output = subprocess.check_output(['nvidia-smi', 'topo', '-m'], text=True)
        lines = [line.strip() for line in output.split('\n') if line.startswith('GPU')]
        device_count = len(lines)
        matrix = [[-1 for _ in range(device_count)] for _ in range(device_count)]
        for i, line in enumerate(lines):
            parts = line.split()
            for j in range(1, len(parts)):
                if 'NV' in parts[j]:
                    matrix[i][j - 1] = 1
        return matrix

    @staticmethod
    def get_gpu_numa_node(gpu_index=0):
        try:
            cmd = f'nvidia-smi --query-gpu=pci.bus_id --format=csv,noheader,nounits -i {gpu_index}'
            pci_id = subprocess.check_output(cmd, shell=True).decode().strip()
            pci_address = pci_id.replace('00000000:', '').lower()
            numa_node_path = f'/sys/bus/pci/devices/0000:{pci_address}/numa_node'
            with open(numa_node_path, 'r') as f:
                numa_node = int(f.read().strip())
            assert numa_node >= 0
            return numa_node if numa_node >= 0 else 0
        except Exception as e:
            print(f'Error: {e}')
            return -1