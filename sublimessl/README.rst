SSL for Linux
=============

I really, really miss the SSL package in Sublime Text and I always used external python installation for doing SSL requests.

For enabling other packages to use SSL, I re-distribute this
part of great `SFTP Package`_ from `Will Bond`_ as single 
open source licensed package, which is permitted by him according to a post in `Sublime Text User Echo`_.

.. _Will Bond: http://wbond.net
.. _SFTP Package: http://wbond.net/sublime_packages/sftp
.. _Sublime Text User Echo: http://sublimetext.userecho.com/topic/50801-bundle-python-ssl-module/


Usage
-----

SSL is only available after this SSL.py has been loaded.  So 
you must import packages, which need SSL support rather in
``plugin_loaded()`` or locally in your functions than globally
at start of your plugin.

If you really have to import your packages globally, you can try::

    import some_package_using_ssl

    def plugin_loaded():
        from imp import reload
        reload(some_package_using_ssl)

(Just an idea, I did not test this)

Changes
-------

2014-03-15
    Reload Package Control after SSL Package is Installed.  (If package control 
    did not work anymore, you had to disable SSL, restart and then you could use 
    it.)

Author
------

Will Bond (http://wbond.net).

--------------------------------------------------------------------------------

Redistributed by Kay-Uwe (Kiwi) Lorenz <kiwi@franka.dyndns.org> (http://quelltexter.org)

Support my work on `Sublime Text Plugins`_: `Donate via Paypal`_

.. _Sublime Text Plugins:
    https://sublime.wbond.net/browse/authors/Kay-Uwe%20%28Kiwi%29%20Lorenz%20%28klorenz%29
    
.. _Donate via Paypal:
    https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WYGR49LEGL9C8A
