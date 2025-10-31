from queue import Queue
import sys
import io

class Revvity:
    _success: bool = False
    _status: str = 'Idle'
    _status_queue: Queue = Queue()

    def __init__(self):
        self._status = 'Idle'
        self._success = False
        self._status_queue = Queue()

    @property
    def success(self) -> bool:
        return self._success

    @property
    def status(self) -> str:
        if not self._status_queue.empty():
            self._status = self._status_queue.get()
        return self._status

    def _run_script(self, file_path: str):
        output = io.StringIO()
        sys.stdout = output
        try:
            winprep_c.test_mtp_script(file_path)
        except Exception as e:
            print(e)
            self._status_queue.put(f'Error: {str(e)}')
        finally:
            sys.stdout = sys.__stdout__
        for line in output.getvalue().splitlines():
            print(line)
            self._status_queue.put(line)
            self._status = line

    def run(self, file_path: str, params: str, resource: dict={'AichemecoHiwo': {'id': 'AichemecoHiwo'}}):
        self._status = 'Running'
        winprep_c.test_mtp_script(file_path)
        workstation = list(resource.values())[0]
        input_plate_wells = list(workstation['children']['test-GL96-2A02']['children'].values())
        output_plate_wells = list(workstation['children']['HPLC_Plate']['children'].values())
        for j in range(8):
            output_plate_wells[j]['data']['liquid'] += input_plate_wells[j]['data']['liquid']
            output_plate_wells[j]['sample_id'] = input_plate_wells[j]['sample_id']
        self._status = 'Idle'
        self._success = True