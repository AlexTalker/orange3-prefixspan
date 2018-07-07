from AnyQt.QtWidgets import QGridLayout, QStyle, QSizePolicy as Policy
from Orange.widgets import widget, gui
from Orange.widgets.utils.filedialogs import RecentPathsWComboMixin, open_filename_dialog
from Orange.widgets.widget import Output
from Orange.data.io import CSVReader
from csv import reader

import os

class OWCSVReader(widget.OWWidget, RecentPathsWComboMixin):
    name = "CSV File"
    id = "orangecontrib.sequence.widgets.owcsvreader"
    description = "Read data from an input csv file."
    #icon = "icons/File.svg"
    priority = 10
    category = "Data"
    keywords = ["data", "file", "load", "read"]
    class Outputs:
        object = Output("Object", object)
    def __init__(self):
        super().__init__()
        RecentPathsWComboMixin.__init__(self)
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)
        #vbox = gui.radioButtons(None, self, "source", box=True, addSpace=True,
            #callback=self.load_data, addToLayout=False)

        #rb_button = gui.appendRadioButton(vbox, "File:", addToLayout=False)
        #layout.addWidget(rb_button, 0, 0, Qt.AlignVCenter)
        box = gui.hBox(None, addToLayout=False, margin=0)
        box.setSizePolicy(Policy.MinimumExpanding, Policy.Fixed)
        self.file_combo.setSizePolicy(Policy.MinimumExpanding, Policy.Fixed)
        self.file_combo.activated[int].connect(self.select_file)
        box.layout().addWidget(self.file_combo)
        layout.addWidget(box, 0, 0)
        file_button = gui.button(
            None, self, '...', callback=self.browse_file, autoDefault=False)
        file_button.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        file_button.setSizePolicy(Policy.Maximum, Policy.Fixed)
        layout.addWidget(file_button, 0, 1)

    def browse_file(self):
        start_file = os.path.expanduser("~/")
        filename, _, _ = open_filename_dialog(start_file, None, [CSVReader])
        self.add_path(filename)
        with open(filename, newline='') as csvfile:
            self.Outputs.object.send(list(reader(csvfile)))

if __name__ == "__main__":
    import sys
    from AnyQt.QtWidgets import QApplication
    a = QApplication(sys.argv)
    ow = OWCSVReader()
    ow.show()
    a.exec_()
    #ow.saveSettings()