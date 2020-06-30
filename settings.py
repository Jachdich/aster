from PyQt5 import QtWidgets
import logger, json
from gui import Dialog, HighlightedTextBox, ColourButton
from stylesheets import managerInstance as styleSheetManager

class AppearanceTab(QtWidgets.QWidget):
    def __init__(self, initialX=600, initialY=400):
        super().__init__()
        logger.log(logger.DEBUG, "Starting AppearanceTab GUI construction...")

        self.colours = {"builtin": None}
        
        self.tabs = QtWidgets.QTabWidget(self)
        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.tabs, 0, 0, 10, 10)
        
        self.tab_syntax = QtWidgets.QWidget()
        self.tab_syntax_layout = QtWidgets.QGridLayout()
        self.tab_syntax.setLayout(self.tab_syntax_layout)
        self.tabs.addTab(self.tab_syntax, "Syntax")

        self.tab_interface = QtWidgets.QWidget()
        self.tab_interface_layout = QtWidgets.QGridLayout()
        self.tab_interface.setLayout(self.tab_interface_layout)
        self.tabs.addTab(self.tab_interface, "Interface")

        self.tab_ssheets = QtWidgets.QWidget()
        self.tab_ssheets_layout = QtWidgets.QGridLayout()
        self.tab_ssheets.setLayout(self.tab_ssheets_layout)
        self.tabs.addTab(self.tab_ssheets, "Stylesheets")

        self.init_tabs()
        self.resize(initialX, initialY)
        logger.log(logger.DEBUG, "AppearanceTab GUI construction complete")

    def init_tabs(self):
        with open("styles.json", "r") as f:
            self.styles = json.loads(f.read())

        #syntax highlighting
        self.l_keyw = QtWidgets.QLabel(self)
        self.t_keyw = HighlightedTextBox(self)
        self.t_keyw.insertPlainText(", ".join(self.styles["words"]["keywords"]))
        self.l_keyw.setText("Keywords")
        self.tab_syntax_layout.addWidget(self.t_keyw, 1, 0)

        self.builtin_selection_layout = QtWidgets.QHBoxLayout()
        self.keyword_selection_layout = QtWidgets.QHBoxLayout()

        self.l_builtin = QtWidgets.QLabel(self)
        self.t_builtin = HighlightedTextBox(self)
        self.t_builtin.insertPlainText(", ".join(self.styles["words"]["builtins"]))
        self.l_builtin.setText("Builtins")
        self.builtin_selection_layout.addWidget(self.l_builtin)
        self.tab_syntax_layout.addWidget(self.t_builtin, 1, 1)

        self.keyword_selection_layout.addWidget(self.l_keyw)

        self.colour_layout = QtWidgets.QGridLayout()

        self.recolour_labels = []
        self.recolour_entries= []
        self.recolour_buttons= []
        y = 0
        for i in [("string","String"),       ("string2", "Docstring"),
                  ("builtin", "Builtins"),   ("keyword", "Keywords"),
                  ("defclass", "def/class"), ("operator", "Operators"),
                  ("numbers", "Numbers"),    ("comment", "Comments"),
                  ("self", "Self")]:

            self.recolour_labels.append(QtWidgets.QLabel(i[1], self))
            self.recolour_entries.append(QtWidgets.QLineEdit(self))
            self.recolour_entries[-1].setText("Placeholder")
            self.recolour_buttons.append(ColourButton(lambda x: self.changeSyntaxColour(i[0], x), self.styles["colours"][i[0]][0], self))

            self.colour_layout.addWidget(self.recolour_labels[-1], y, 0)
            self.colour_layout.addWidget(self.recolour_buttons[-1], y, 1)
            self.colour_layout.addWidget(self.recolour_entries[-1], y, 2)
            y += 1

        

        self.tab_syntax_layout.addLayout(self.builtin_selection_layout, 0, 1)
        self.tab_syntax_layout.addLayout(self.keyword_selection_layout, 0, 0)
        self.tab_syntax_layout.addLayout(self.colour_layout, 2, 0)

        #interface style

        self.l_foreground = QtWidgets.QLabel("Foreground", self)
        self.l_background = QtWidgets.QLabel("Background", self)
        self.l_light_background = QtWidgets.QLabel("Light background", self)
        self.l_dark_background = QtWidgets.QLabel("Dark  background", self)

        self.b_bg_colour = ColourButton(lambda x: self.changeColour("bg", x), self.styles["colours"]["bg"])
        self.b_fg_colour = ColourButton(lambda x: self.changeColour("fg", x), self.styles["colours"]["fg"])
        self.b_light_colour = ColourButton(lambda x: self.changeColour("light", x), self.styles["colours"]["light"])
        self.b_dark_colour = ColourButton(lambda x: self.changeColour("dark", x), self.styles["colours"]["dark"])

        self.tab_interface_layout.addWidget(self.l_foreground, 0, 0)
        self.tab_interface_layout.addWidget(self.l_background, 1, 0)
        self.tab_interface_layout.addWidget(self.l_light_background, 2, 0)
        self.tab_interface_layout.addWidget(self.l_dark_background, 3, 0)

        self.tab_interface_layout.addWidget(self.b_fg_colour,       0, 1)
        self.tab_interface_layout.addWidget(self.b_bg_colour,       1, 1)
        self.tab_interface_layout.addWidget(self.b_light_colour, 2, 1)
        self.tab_interface_layout.addWidget(self.b_dark_colour, 3, 1)

        #Stylesheets

        self.c_stylesheet = QtWidgets.QComboBox(self)
        for sheet in styleSheetManager.raw_stylesheets:
            self.c_stylesheet.addItem(sheet)

        self.c_stylesheet.activated[str].connect(self.change_stylesheet)

        self.t_stylesheet = QtWidgets.QPlainTextEdit(self)

        self.tab_ssheets_layout.addWidget(self.c_stylesheet)
        self.tab_ssheets_layout.addWidget(self.t_stylesheet)
        self.change_stylesheet(self.c_stylesheet.itemText(self.c_stylesheet.currentIndex()))

    def change_stylesheet(self, sheet):
        self.t_stylesheet.clear()
        self.t_stylesheet.insertPlainText(styleSheetManager.raw_stylesheets[sheet])

    def changeColour(self, name, colour):
        self.colours[name] = colour
        logger.log(logger.INFO, name + " colour changed to " + colour)

    def changeSyntaxColour(self, name, colour):
        self.colours[name] = [colour, "{bg}", "normal"]
        logger.log(logger.INFO, name + " colour changed to " + colour)
 
    def apply(self):
        logger.log(logger.DEBUG, "Starting apply of settings")
        keywords = self.t_keyw.toPlainText().replace(" ", "")
        if keywords.endswith(","):
            keywords = keywords[:-1]
        builtins = self.t_builtin.toPlainText().replace(" ", "")
        if builtins.endswith(","):
            builtins = builtins[:-1]

        keywords = keywords.split(",")
        builtins = builtins.split(",")
        self.styles["words"]["builtins"] = builtins
        self.styles["words"]["keywords"] = keywords
        for key in self.colours:
            if self.colours[key] == None: continue
            self.styles["colours"][key] = self.colours[key]
            
        with open("styles.json", "w") as f:
            f.write(json.dumps(self.styles, sort_keys=False, indent=4))
        logger.log(logger.DEBUG, "Finished writing stylesheets")
        """
        run_file("syntax.py")
        run_file("gui.py")
        for widget in needs_to_be_updated:
            widget.update()"""

class SettingsDialog(Dialog):
    def __init__(self, initialX=600, initialY=400):
        super().__init__(initialX, initialY)
        logger.log(logger.DEBUG, "Starting SettingsDialog GUI construction...")
        self.tabs = QtWidgets.QTabWidget(self)
        self.layout.addWidget(self.tabs)
        self.tabs.resize(initialX, initialY)
        
        self.tab_appearance = AppearanceTab()
        self.tab_appearance.setStyleSheet("QWidget, QWidget * {color: #dddddd; background-color: #333333;}")
        self.tabs.addTab(self.tab_appearance, "Appearance")

        self.tab_server = QtWidgets.QWidget()
        self.tab_server_layout = QtWidgets.QGridLayout()
        self.tab_server.setLayout(self.tab_server_layout)
        self.tabs.addTab(self.tab_server, "Server")

        self.tab_appearance1 = QtWidgets.QWidget()
        self.tab_appearance1_layout = QtWidgets.QGridLayout()
        self.tab_appearance1.setLayout(self.tab_appearance1_layout)
        self.tabs.addTab(self.tab_appearance1, "Old")

        self.b_apply = QtWidgets.QPushButton(self)
        self.b_apply.setText("Apply")
        self.b_apply.clicked.connect(self.tab_appearance.apply)
        self.layout.addWidget(self.b_apply)
        self.resize(initialX, initialY)
        logger.log(logger.DEBUG, "SettingsDialog GUI construction complete")
