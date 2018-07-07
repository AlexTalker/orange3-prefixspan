from AnyQt.QtGui import QStandardItemModel, QStandardItem
from AnyQt.QtWidgets import QGridLayout, QStyle, QTableView
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.filedialogs import RecentPathsWComboMixin, open_filename_dialog
from Orange.widgets.widget import Output, Input
from Orange.data.io import CSVReader
from prefixspan import PrefixSpan
import os

class OWFrequentSequence(widget.OWWidget):
    name = "Frequent Sequence"
    id = "orangecontrib.sequence.widgets.owfrequentsequence"
    description = "Mine frequent sequences from a basket."
    #icon = "icons/File.svg"
    priority = 10
    category = "Data"
    keywords = ["data", "file", "load", "read"]
    class Inputs:
        object = Input("Object", object)
    class Outputs:
        object = Output("Object", object)
        
    auto_find = settings.Setting(False)
    min_support = settings.Setting(1)
    k = settings.Setting(5)
    min_len = settings.Setting(1)
    sampling_type = settings.Setting(0)# Frequent first
    closed = settings.Setting(False)
    #generator = settings.Setting(False)
    
    def __init__(self):
        super().__init__()
        self.data = None
        table = self.table = QTableView(self,
            showGrid=False,
            sortingEnabled=True,
            alternatingRowColors=True)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(table.verticalHeader().minimumSectionSize())
        table.horizontalHeader().setStretchLastSection(True)
        table.setModel(QStandardItemModel(table))
        self.mainArea.layout().addWidget(table)
        self.sampling_box = gui.vBox(self.controlArea, "Sampling Type")
        sampling = gui.radioButtons(self.sampling_box, self, "sampling_type")
        fq_button = gui.appendRadioButton(sampling, "Frequent")
        k_button = gui.appendRadioButton(sampling, "Top-K")
        self.param_box = gui.vBox(self.controlArea, "Parameters")
        gui.spin(self.param_box, self, 'min_support', 1, 10 ** 6, label='Min. support:')
        gui.spin(self.param_box, self, 'k', 1, 10 ** 3, label='K:')
        gui.spin(self.param_box, self, 'min_len', 1, 10**2, label='Min. length:')
        gui.checkBox(self.param_box, self, 'closed', label='Closed patterns')
        #gui.checkBox(self.param_box, self, 'generator', label='Generator patterns')
        box = gui.widgetBox(self.controlArea, 'Find sequantual patterns')
        
        self.button = gui.auto_commit(
            box, self, 'auto_find', 'Find Patterns', commit=lambda: self.find_patterns(),
            callback=lambda: self.auto_find and self.find_patterns())

    # Fix up number's sorting
    class NumericItem(QStandardItem):
        def __init__(self, num):
            super().__init__(str(num))
        def __lt__(self, other):
            return int(self.text()) < int(other.text())

    def find_patterns(self):
        print(self.sampling_type)
        db = self.data
        ps = PrefixSpan(db)
        result = None
        opts = {
            "closed": self.closed,
            # Somehow does not work
            #"generator": self.generator
        }
        from pprint import pprint
        pprint(opts)
        if self.sampling_type:
            result = ps.topk(self.k, **opts)
        else:
            result = ps.frequent(self.min_support, **opts)
        self.Outputs.object.send(result)
        self.table.model().clear()
        model = QStandardItemModel(self.table)
        for col,label in enumerate(["Support", "Pattern"]):
            item = QStandardItem(label)
            model.setHorizontalHeaderItem(col, item)
        for support, pattern in result:
            if len(pattern) < self.min_len:
                continue
            sitem = self.NumericItem(support)
            pitem = QStandardItem(str(pattern))
            model.appendRow([ sitem, pitem ])
        self.table.setModel(model)

    @Inputs.object
    def set_object(self, data):
        self.data = data

if __name__ == "__main__":
    import sys
    from AnyQt.QtWidgets import QApplication
    a = QApplication(sys.argv)
    db = [
        [0, 1, 2, 3, 4],
        [1, 1, 1, 3, 4],
        [2, 1, 2, 2, 0],
        [1, 1, 1, 2, 2],
    ]
    ow = OWFrequentSequence()
    ow.set_object(db)
    ow.show()
    a.exec_()
    #ow.saveSettings()