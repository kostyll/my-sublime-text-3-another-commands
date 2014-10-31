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

PLUGIN_DEBUG = True

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


def debug_lambda (func,comment=None):
    def wrapper(*args,**kwargs):
        if comment is not None:
            print (comment)
        # print ("func = {}".format(func))
        print (args,kwargs)
        return func(*args,**kwargs)
    if PLUGIN_DEBUG:
        return wrapper
    else:
        return func

class JsonLikeDataParser(object):

    def __init__(self,text):
        rus_alphas = 'їійцукенгшщзхъфывапролджэячсмитьбюІЇЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
        comma = ','

        string = OneOrMore(Word(alphas+rus_alphas+alphanums+'.'))
        string.setParseAction(lambda t:t)

        quoted_string = (
                         Suppress('"') + Optional(string) + Suppress('"')|
                         Suppress("'") + Optional(string) + Suppress("'")|
                         string
                         )
        ('string')
        def string_handler(t):
            asList = t.asList()
            if len(t) == 0:
                return {
                    'type':'string',
                    'value':'',
                }
            else:
                return {
                    'type':'string',
                    'value':asList[0]
                }
        quoted_string.setParseAction(debug_lambda(
                    string_handler,
                    comment="parsed string"
                )
            )

        number = OneOrMore(Word(nums+'.'))
        ('number')
        number.setParseAction(debug_lambda(
            lambda t:{
                        'type':'number',
                        'value':t.asList()[0]
                    },
                    comment="parsing number"
                ),
            )

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
            'type':'member',
            'key':t.asList()[0],
            'value':t.asList()[1]
        })


        value << (
                  number|
                  # string|
                  quoted_string|
                  array|
                  dict_
                  )
        ('value')

        array << (Suppress("[") + Optional(elements) + Suppress("]"))
        ('array')
        array.setParseAction(lambda t:{
            'type':'array',
            'elements':t.asList()
        })

        dict_ << (Suppress("{") + Optional(members) + Suppress("}"))
        ('dict')
        dict_.setParseAction(lambda t: {
            'type': 'dict',
            'members':t.asList()
        })

        self.parsed = dict_.parseString(text)

    def __call__(self):
        return self.parsed


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
        """{1:2,b.1:3.3,b.s:[{a:2,'b':[12,"s",5]},"s",5]}""",
    ]
    for test in tests:
        try:
            print ("TEST:")
            parsed = JsonLikeDataParser(test)().asList()[0]['members']
            print ("Test\n{}\npassed".format(parsed))
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
        self.indent = 1
        self.parsed = JsonLikeDataParser(text)().asList()[0]

    def pprint(self,string,newl=True):
        result = "{}{}".format(" "*self.indent*self.level,string)
        if PLUGIN_DEBUG:
            print(result)
        self.result += result
        if newl:
            self.result += '\n'

    def _pretify(self,parsed=None):
        p = self.pprint
        try:
            self.level += 1
            type_ = parsed['type']
            # pprint("type = {}".format(type_))
            if type_ == "dict":
                p('{')
                for member in parsed['members']:
                    self._pretify(member)
                    p(',')
                p('}')
            if type_ == "array":
                self.pprint('[')
                for element in parsed['elements']:
                    # self.pprint("member = ")
                    self._pretify(element)
                    p(',')
                self.pprint(']')
            if type_ == "member":
                # self.pprint(parsed['key']['value'])
                p(parsed['key']['value'],newl=False)
                p(':',newl=False)
                self._pretify(parsed['value'])
            if type_ == "number":
                # self.pprint("number = ")
                p(parsed['value'])
            if type_ == "string":
                # self.pprint("string = ")
                p(parsed['value'])
            self.level -= 1
        except KeyError:
            pass
            # print (parsed)

    def get_pretified(self):
        parsed = self.parsed
        self.level = -1
        self.result = ""
        self._pretify(parsed)
        return self.result


class PretifyDictDataCommand(sublime_plugin.TextCommand):
    """
    Reprints text from ugly view to pretty
    """
    def run(self,edit):
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region)
                prety_printer = PretyDictPrinter(text)
                pretty_text = prety_printer.get_pretified()
                print (pretty_text)

                # self.view.run_command("insert",{"characters":pretty_text})
                self.view.replace(edit,region,pretty_text)


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
