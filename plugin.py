import sublime
import sublime_plugin

# TODO: json-like data parsing neet to be implemented
# view.run_command("pretify_dict_data")

import os
import sys
import pprint

root_location = os.path.dirname(__file__)

third_party_path = os.path.join(root_location,'thirdparty')

requests_path = os.path.join(root_location,'requests')
sublimessl = os.path.join(root_location,'sublimessl')

pyparsing_path = os.path.join(third_party_path,'pyparsing/src')

sys.path.insert(0, requests_path)
sys.path.insert(0, sublimessl)
sys.path.insert(0, pyparsing_path)

import pyparsing
# from pyparsing import *
from pyparsing import (
    Word, Literal,
    alphas, nums, alphanums,
    OneOrMore, ZeroOrMore,
    Or, And,
    Forward, Optional, Group,Suppress
)

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

# rus_alphas = 'їійцукенгшщзхъфывапролджэячсмитьбюІЇЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
rus_alphas = ""
comma = ','

string = Word(alphas+rus_alphas+nums+ alphanums)
quoted_string = Or(string,Or('"' + string + '"',"'"+string + "'"))

number = Word(nums+'.,')

value = Forward()
member = Forward()
array = Forward()
dict_ = Forward()

elements = OneOrMore(value)
members = OneOrMore(member)

member << quoted_string+Suppress(':')+ value
value << (string|quoted_string|number|array|dict_)
array << Suppress("[") + Optional(elements) + Suppress("]")

dict_ << Suppress("{") + Optional(members) + Suppress("}")



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


class PretyDictPrinter(object):
    def __init__(self,text):
        self.text = text

    def print_pretty(self):
        text = self.text
        results = dict_.parseString(text)
        pprint.pprint(results)


class PretifyDictDataCommand(sublime_plugin.TextCommand):
    """
    Reprints text from ugly view to pretty
    """
    def run(self,edit):
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region)
                prety_printer = PretyDictPrinter(text)
                prety_text = prety_printer.print_pretty()

                # self.view.run_command("insert",{"characters":prety_text})


class ShowGitBranchesCommand(sublime_plugin.TextCommand):
    """
    Show the list of existing git repo branches
    """
    def run(self,edit):
        file = view.file_name()
        print (file)
        directory = os.path.dirname(file)
        print (directory)


class SwitchGitBrancheCommand(sublime_plugin.TextCommand):
    """
    Switch to git branch
    """
    def run(self,edit):
        pass
