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
    OneOrMore, ZeroOrMore,empty,
    Or, And,
    Forward, Optional, Group,Suppress, delimitedList
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
    test_json_like_parser()

def json_like_data_parser(text):
    rus_alphas = 'їійцукенгшщзхъфывапролджэячсмитьбюІЇЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
    comma = ','

    string = OneOrMore(Word(alphas+rus_alphas+alphanums+'.'))
    string.setParseAction(lambda t:{
        'type':'str',
        'str':t.asList()[0]
    })

    quoted_string = (
                     string|
                     Suppress('"') + Optional(string) + Suppress('"')|
                     Suppress("'") + Optional(string) + Suppress("'")
                     )
    ('string')
    # quoted_string.setParseAction(lambda t:{
    #     'str':t.asList()[0]
    # })

    number = OneOrMore(Word(nums+'.'))('number')
    number.setParseAction(lambda t:{
        'type':'number',
        'number':t.asList()[0]
    })

    value = Forward()
    member = Forward()
    array = Forward()
    dict_ = Forward()

    elements = delimitedList(value)
    ('elements')

    members = delimitedList(member)
    ('members')

    member << (
               value+Suppress(':')+Optional(ZeroOrMore(' '))+value
               )
    ('member')
    member.setParseAction(lambda t:{
        'key':t.asList()[0],
        'value':t.asList()[1]
    })


    value << (
              number|
              string|
              quoted_string|
              array|
              dict_
              )
    ('value')

    array << (Suppress("[") + Optional(elements) + Suppress("]"))
    ('array')

    dict_ << (Suppress("{") + Optional(members) + Suppress("}"))
    ('dict')
    dict_.setParseAction(lambda t: {
                        'members':t.asList()
                    })

    return dict_.parseString(text).asList()

def test_json_like_parser():
    passed = failed = 0
    tests = [
        """{a:2,'b':[12,"s",5]}""",
        """{a:2,'b':[12,"s",{a:3,x:2}]}""",
        """{aaaa:2,'b':[12,"s",5]}""",
        """{aaaa:2,'b.s':[12,"s",5]}""",
        """{aaaa:2,b.s:[12,"s",5]}""",
        """{'їійцукенгшщзхъфывапролджэячсмитьбюІЇЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ':\t\t3}""",
        """{1:2,b.1:3.3,b.s:[12,"s",5]}""",
    ]
    for test in tests:
        try:
            print ("TEST:")
            print (json_like_data_parser(test))
            print ("Test\n{}\npassed".format(test))
            passed += 1
        except (Exception) as e:
            print ("Test\n{}\nfailed with message:{}".format(test,e))
            # break
            failed += 1
    print ("Passed {},Failed {} tests".format(passed,failed))



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
