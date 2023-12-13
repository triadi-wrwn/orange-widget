from Orange.data import Table
from Orange.widgets import gui
from Orange.widgets.widget import OWWidget
from AnyQt.QtWidgets import QApplication, QLabel
from orangecontrib.text import Corpus


class OWWordFinder(OWWidget):
    name = "Word Finder"
    description = "Display whether a word is in a text or not."
    icon = "icons/WordFinder.svg"
    priority = 1

    inputs = [('Corpus', Table, 'set_data')]
    # This widget will have no output, but in case you want one, you define it as below.
    # outputs = [('Selected Documents', Table, )]

    want_control_area = False

    def __init__(self):
        super().__init__()

        self.corpus = None
        self.word = ""

        gui.widgetBox(self.mainArea, orientation="vertical")
        self.input = gui.lineEdit(self.mainArea, self, '',
                                  orientation="horizontal",
                                  label='Query:')
        self.input.setFocus()
        self.input.textChanged.connect(self.search)

        self.view = QLabel()
        self.mainArea.layout().addWidget(self.view)

    def set_data(self, data=None):
        if data is not None and not isinstance(data, Corpus):
            self.corpus = Corpus.from_table(data.domain, data)
        self.corpus = data
        self.search()

    def search(self):
        self.word = self.input.text()
        result = any(self.word in doc for doc in self.corpus.tokens)
        self.view.setText(str(result))


if __name__ == '__main__':
    app = QApplication([])
    widget = OWWordFinder()
    corpus = Corpus.from_file('bookexcerpts')
    corpus = corpus[:3]
    widget.set_data(corpus)
    widget.show()
    app.exec()