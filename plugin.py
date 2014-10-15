import sublime
import sublime_plugin

def plugin_loaded():
    # print ("{} loaded".format(__file__))
    pass

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
