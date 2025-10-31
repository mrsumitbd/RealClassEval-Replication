import numpy as np
from etk.timeseries.annotation.table_processor import parsed_table
from etk.timeseries.annotation.granularity_detector import GranularityDetector
from etk.timeseries.annotation import input_processor

class SimpleAnnotator:

    def __init__(self, infile):
        self.infile = infile

    def get_annotation_json(self):
        final_json = []
        for sheet, sheet_name, merged_cells in input_processor.process_excel(self.infile):
            table_properties = dict()
            sheet = sheet.to_array()
            sheet = np.array(sheet)
            remove_bom(sheet)
            row, col = sheet.shape
            assert col == 2
            header_present = is_header_present(sheet)
            start_row = 0
            if header_present:
                start_row = 1
            data_col = []
            for i in range(2):
                is_data_col = True
                for j in range(start_row, row):
                    if not is_data(sheet[j][i]):
                        is_data_col = False
                        break
                if is_data_col:
                    data_col.append(i)
            if len(data_col) == 2:
                logging.error('Ambiguous data. Multiple data columns present')
                break
            if len(data_col) == 0:
                logging.error('Cannot find data column')
                break
            data_col = data_col[0]
            date_col = data_col ^ 1
            table_properties['start_row'] = start_row + 1
            table_properties['end_row'] = row
            table_properties['time_column'] = parsed_table.get_excel_column_name(date_col)
            table_properties['header_present'] = header_present
            table_properties['ts_column'] = parsed_table.get_excel_column_name(data_col)
            table_properties['granularity'] = GranularityDetector.get_granularity(sheet[:, date_col])
            annotation = get_base_annotation(table_properties)
            final_json.append(annotation)
        return final_json