# [start-snippet-1]
import sys
import numpy

import Orange.data
from Orange.widgets import widget, gui
from Orange.widgets.utils.signals import Input, Output

import requests
import pandas as pd
from Orange.data import Table, Domain, ContinuousVariable, StringVariable



class OWDataSamplerA(widget.OWWidget):
    name = "Data Sampler"
    description = "Randomly selects a subset of instances from the data set"
    icon = "icons/DataSamplerA.svg"
    priority = 10

    api_url = 'https://pokeapi.co/api/v2/pokemon?offset=0&limit=10'
    response = requests.get(api_url)
    if response.status_code == 200:
        # Parse the JSON response
        data_json = response.json()

        # Convert the JSON data to a Pandas DataFrame
        #df = pd.DataFrame(data_json)

        # Create a domain for Orange with appropriate variable types
        #domain = Domain(
        #    [ContinuousVariable(name) if pd.api.types.is_numeric_dtype(df[name]) else StringVariable(name) for name in df.columns]
        #)

        # Create an Orange Table from the Pandas DataFrame
        #orange_table = Table.from_numpy(domain, X=df.values)

        # Output the Orange Table
        #output_data = orange_table
        print(f"Data: {data_json}")
    else:
        # If the API request was not successful, print an error message
        print(f"Error: Unable to fetch data from the API. Status Code: {response.status_code}")

    class Inputs:
        data = Input("Data", Orange.data.Table)

    class Outputs:
        sample = Output("Sampled Data", Orange.data.Table)

    want_main_area = False


    def __init__(self):
        super().__init__()

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(
            box, "No data on input yet, waiting to get something.")
        self.infob = gui.widgetLabel(box, '')
        box2 = gui.widgetBox(self.controlArea, "Pokemon")
        self.infoa2 = gui.widgetLabel(
            box2, "No Data")
        self.infob2 = gui.widgetLabel(box2, '')
        self.infob2.setText(data_json.result)
# [end-snippet-1]

# [start-snippet-2]
    @Inputs.data
    def set_data(self, dataset):
        if dataset is not None:
            self.infoa.setText("%d instances in input data set" % len(dataset))
            indices = numpy.random.permutation(len(dataset))
            indices = indices[:int(numpy.ceil(len(dataset) * 0.1))]
            sample = dataset[indices]
            self.infob.setText("%d sampled instances" % len(sample))
            self.Outputs.sample.send(sample)
        else:
            self.infoa.setText(
                "No data on input yet, waiting to get something.")
            self.infob.setText('')
            self.Outputs.sample.send(None)
# [end-snippet-2]

# [start-snippet-3]


def main(argv=sys.argv):
    from AnyQt.QtWidgets import QApplication
    app = QApplication(list(argv))
    args = app.arguments()
    if len(args) > 1:
        filename = args[1]
    else:
        filename = "iris"

    ow = OWDataSamplerA()
    ow.show()
    ow.raise_()

    dataset = Orange.data.Table(filename)
    ow.set_data(dataset)
    ow.handleNewSignals()
    app.exec_()
    ow.set_data(None)
    ow.handleNewSignals()
    return 0


if __name__ == "__main__":
    sys.exit(main())

# [end-snippet-3]