import xlwings as xw

class Report:
    def __init__(self):
        self.work_book = xw.Book('Timber Connection Designer.xlsm')
        self.report_sheet = self.work_book.sheets['Designer']
        self.inputs_sheet = self.work_book.sheets['Inputs']

    def add_plots(self):
        # Use excel writing funcions to write results on the user spreadsheet
        er.add_plots(beam_connection)
        er.store_report(beam_connection, bk)

        er.add_plots(col_connection)
        er.store_report(col_connection, bk)

        def data_report(cxn):
        er.data_report(cxn)
            
    def design_report(cxn):
        er.design_report(cxn)

