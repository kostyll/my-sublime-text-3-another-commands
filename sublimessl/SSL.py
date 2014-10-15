import sublime, os, sys

#
# this code is taken from SFTP.py, http://wbond.net/sublime_packages/sftp
# which can be used for open source packages, according to 
#
# http://sublimetext.userecho.com/topic/50801-bundle-python-ssl-module/
#
st_version = int(sublime.version()[0])

arch_lib_path = None
if sublime.platform() == 'linux':
    arch_lib_path = os.path.join(os.path.dirname(__file__), 'lib',
        'st%d_linux_%s' % (st_version, sublime.arch()))
    print('SSL: enabling custom linux ssl module')
    for ssl_ver in ['1.0.0', '10', '0.9.8']:
        lib_path = os.path.join(arch_lib_path, 'libssl-' + ssl_ver)
        sys.path.append(lib_path)
        try:
            import _ssl
            print('SSL: successfully loaded _ssl module for libssl.so.%s' % ssl_ver)
            break
        except (ImportError) as ex:
            print('SSL: _ssl module import error - ' + str(ex))

    if '_ssl' in sys.modules:
        try:
            if sys.version_info < (3,):
                plat_lib_path = os.path.join(sublime.packages_path(), 'SSL',
                    'lib', 'st2_linux')
                m_info = imp.find_module('ssl', [plat_lib_path])
                m = imp.load_module('ssl', *m_info)
            else:
                import ssl




        except (ImportError) as ex:
            print('SSL: ssl module import error - ' + str(ex))

def plugin_loaded():
    from imp import reload

    # package control may not work correctly if SSL installed
    # so reload all Package Control modules to get SSL included
    # right
    print("(SSL) start reloading Package Control")

    import ssl

    # make sure http.client knows about ssl
    import http.client
    reload(http.client)

    # make sure urllib knows about ssl
    import urllib
    reload(urllib)

    import urllib.request
    reload(urllib.request)

    import urllib.response
    reload(urllib.response)

    # package Control udel ses SSL
    reload(sys.modules['Package Control.package_control.reloader'])