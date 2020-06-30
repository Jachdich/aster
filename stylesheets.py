from constants import *
from json import loads
 
def format_colours(S, colours):
    fgcolour    = colours["fg"]
    bgcolour    = colours["bg"]
    lightcolour = colours["light"]
    darkcolour  = colours["dark"]
    return S.format(fg=fgcolour, bg=bgcolour, dark=darkcolour, light=lightcolour)


class StyleSheetManager:
    def __init__(self):
        self.raw_stylesheets = None
        self.fgcolour    = None
        self.bgcolour    = None
        self.lightcolour = None
        self.darkcolour  = None

        self.colours = None
        self.stylesheets = None
        self.StyleSheet = None

    def saveSheet(sheetName, sheetContents):
        print("NOPE NOT TODAY THANK YOU")
    
    def loadSheets(self):
        with open("styles.json", "r") as f:
            styles_json = loads(f.read())

        with open("stylesheets.qss", "r") as f:
            self.raw_stylesheets = f.read()

        styles = styles_json["colours"]
        self.fgcolour    = styles["fg"]
        self.bgcolour    = styles["bg"]
        self.lightcolour = styles["light"]
        self.darkcolour  = styles["dark"]


        self.colours = {"fg"   : self.fgcolour,
                        "bg"   : self.bgcolour,
                        "light": self.lightcolour,
                        "dark" : self.darkcolour}

        self.StyleSheet = format_colours(self.raw_stylesheets, self.colours)

