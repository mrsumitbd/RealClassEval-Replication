import subprocess

class NsightComputeReport:

    def __init__(self, report_path: str):
        self.report_path: str = report_path

    def visualize(self):
        command = _ncu_ui_template.format(ncu_ui_path=_ncu_ui_path, report_path=self.report_path)
        subprocess.run(command, shell=True)