"""
Data entry for weight lifting tracking
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

import trudge.csv_util as csv


COLUMN_LABELS = {
    "date": "Date",
    "name": "Type",
    "reps": "Reps",
    "weight": "Weight (lb)",
    "rest": "Preceding Rest (min)",
    "positive": "Positive Tempo (s)",
    "hold": "Hold Time (s)",
    "negative": "Negative Tempo (s)",
    "effort": "Effort (1-5)",
    "notes": "Notes",
}


class Trudge(toga.App):

    # TODO: have file path as an input
    CSV_PATH = "/Users/roco/src/trudge_ws/trudge/tests/data/data.csv"

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.table = toga.Table(
            headings=[COLUMN_LABELS[c] for c in csv.COLUMNS], 
            data=csv.parse_file(self.CSV_PATH)
        )

        self.box = toga.Box(style=Pack(direction=COLUMN))
        self.box.add(self.table)

        self.command_group = toga.Group("Command Group")

        self.add_set_command = toga.Command(
            self.add_set_action,
            text = "Add",
            tooltip = "Add a new set at the end",
            # icon = 
            group = self.command_group
        )

        self.commands.add(
            self.add_set_command
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.box
        self.main_window.show()

    def add_set_action(self, *args, **kwargs):
        print("add_set_action")
        print("\targs: {}".format(args))
        print("\tkwargs: {}".format(kwargs))


def main():
    return Trudge()
