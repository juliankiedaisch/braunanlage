import ConfigParser
class config_mgmt():
    def __init__(self, filename, daten_obj):
        self.config = ConfigParser.ConfigParser()
        self.filename = filename
        self.daten_obj = daten_obj
        self.config.read(filename)
        for section in self.config.sections():
            self.get_config(section)
    def get_config(self, section):
        options = self.config.options(section)
        for option in options:
            try:
                setattr(self.daten_obj, option, self.config.get(section, option))
            except:
                print("exception on %s!" % option)
    def add_to_config(self, section, variable, value):
        cgfile = open(self.filename, "w")
        if section not in self.config.sections():
            self.config.add_section(section)
        #Daten werden in die Config-Datei geschrieben
        self.config.set(section, variable, value)
        self.config.write(cgfile)
        #Daten werden in das Daten-array geladen
        setattr(self.daten_obj, variable, value)
