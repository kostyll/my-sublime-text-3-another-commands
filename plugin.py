import sublime
import sublime_plugin

import os
import sys

root_location = os.path.dirname(__file__)

requests_path = os.path.join(root_location,'requests')
sublimessl = os.path.join(root_location,'sublimessl')

sys.path.insert(0, requests_path)
sys.path.insert(0, sublimessl)

from SSL import ssl

def plugin_loaded():
    # print ("{} loaded".format(__file__))
    from imp import reload
    # NEED TO DO SOME MONKEY PATCHING ACTIONS
    # reload(somelib.somemodule)
    # somelib.somemodule.ssl = ssl
    # For e.g.:
    # reload(yandex_translate)
    # reload(yandex_translate.requests)
    # reload(yandex_translate.requests.packages.urllib3.connection)
    # yandex_translate.requests.packages.urllib3.connection.ssl = ssl

    # func = yandex_translate.requests.packages.urllib3.response.HTTPResponse.stream
    # def urllib3_HTTPResponse_stream_wrapper(func):
    #     return lambda self,amt=None,decode_content=None:func(self,None,decode_content)
    # yandex_translate.requests.packages.urllib3.response.HTTPResponse.stream = urllib3_HTTPResponse_stream_wrapper(func)
    # print ("Plugin RussianVariableTranslate is loaded")

class ItemizeLatexStringsCommand(sublime_plugin.TextCommand):
    """
    Replaces every selected line with prefix '\\item{' and suffix '}'
    """
    def run(self, edit):
        # print ("Run {}".format(self))
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region)
                # print (text)
                result_text = []
                for line in text.split('\n'):
                    # print ("line=",line)
                    result_line = "\\item{"+line+'}'
                    result_text.append(result_line)
                # print (result_text)
                self.view.run_command("insert",{"characters":"\n".join(result_text)})


class ShowGitBranchesCommand(sublime_plugin.TextCommand):
    """
    Show the list of existing git repo branches
    """
    def run(self,edit):
        file = view.file_name()
        print (file)
        directory = os.path.dirname(file)
        print (directory)
