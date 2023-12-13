# api_fetcher_widget.py

import requests
import pandas as pd
from Orange.data import Table, Domain, ContinuousVariable, StringVariable
from Orange.widgets import widget, gui

class ApiFetcherWidget(widget.OWWidget):
    name = "API Fetcher"
    description = "Fetch data from an API and display it in an Orange Data Table."
    icon = "icons/ApiFetcherIcon.png"

    want_main_area = False

    class Outputs:
        data = widget.Output("Data", Table)

    def __init__(self):
        super().__init__()

        # Initialize the api_url attribute
        self.api_url = ""

        # GUI
        self.api_url_line_edit = gui.lineEdit(
            self.controlArea,
            self,
            "api_url",
            label="API URL",
            placeholderText="Enter API URL",
        )

        self.fetch_button = gui.button(
            self.controlArea,
            self,
            "Fetch Data",
            callback=self.fetch_data,
        )

    def fetch_data(self):
        api_url = self.api_url

        # Make a request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data_json = response.json()
            print(f"Data : {data_json['results']}")
            # Convert the JSON data to a Pandas DataFrame
            string_arr = [[entry['name'], entry['url']] for entry in data_json['results']]
            df = pd.DataFrame(data_json['results'])
            print(f"DF : {df.columns}")
            # Create a domain for Orange with appropriate variable types
            domain = Domain(
                [ContinuousVariable(name) if pd.api.types.is_numeric_dtype(df[name]) else StringVariable(name) for name in df.columns]
            )

            # Create an Orange Table from the Pandas DataFrame
            orange_table = Table.from_numpy(domain, X=df.values)

            # Output the Orange Table
            self.Outputs.data.send(orange_table)

        else:
            # If the API request was not successful, print an error message
            self.Error("Unable to fetch data from the API. Status Code: {}".format(response.status_code))

#if __name__ == "__main__":
#    widget.OWWidget.run_main(ApiFetcherWidget)
if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0
    WidgetPreview(ApiFetcherWidget).run()