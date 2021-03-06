Systemd-Service
===============

Simple API to automate the creation of custom daemons for GNU/Linux.

|GitHub top language| |PyPI - License| |PyPI| |PyPI - Status| |PyPI -
Python Version| |GitHub last commit| |CodeFactor Grade| |Documentation
Status|

.. |GitHub top language| image:: https://img.shields.io/github/languages/top/un-gcpds/systemd-service
.. |PyPI - License| image:: https://img.shields.io/pypi/l/systemd-service
.. |PyPI| image:: https://img.shields.io/pypi/v/systemd-service
.. |PyPI - Status| image:: https://img.shields.io/pypi/status/systemd-service
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/systemd-service
.. |GitHub last commit| image:: https://img.shields.io/github/last-commit/un-gcpds/systemd-service
.. |CodeFactor Grade| image:: https://img.shields.io/codefactor/grade/github/UN-GCPDS/systemd-service
.. |Documentation Status| image:: https://readthedocs.org/projects/systemd-service/badge/?version=latest
   :target: https://systemd-service.readthedocs.io/en/latest/?badge=latest

A daemon is a service process that runs in the background and supervises
the system or provides functionality to other processes. Traditionally,
daemons are implemented following a scheme originating in SysV Unix.
Modern daemons should follow a simpler yet more powerful scheme, as
implemented by systemd.

**Systemd-Service** is a Python module to automate the creation of
daemons under GNU/Linux environments.

Install
-------

.. code:: ipython3

    pip install -U systemd-service

Handle daemons
--------------

.. code:: ipython3

    from systemd_service import Service
    
    daemon = Service("stream_rpyc")
    
    daemon.stop()     # Start (activate) the unit.
    daemon.start()    # Stop (deactivate) the unit.
    daemon.reload()   # Reload the unit.  
    daemon.restart()  # Start or restart the unit.
    
    daemon.enable()   # Enable the unit.
    daemon.disable()  # Disable the unit.
    
    daemon.remove()   # Remove the file unit.

This commands are uquivalent to the ``systemctl`` calls, for example run
in terminal the folowing command:

$ systemctl enable stream_rpyc

Can be running inside a Python environment with using
``systemd_service``

.. code:: ipython3

    from systemd_service import Service
    
    daemon = Service("stream_rpyc")
    daemon.enable()

Creating services
-----------------

Similar to the previous scripts, the services can be created using
``systemd_service``:

.. code:: ipython3

    daemon = Service("stream_rpyc")
    daemon.create_service()

If the service must be initialized after other service

.. code:: ipython3

    daemon = Service("stream_rpyc")
    daemon.create_service(after='ntpd')

Creating timers
---------------

Defines a timer relative to when the machine was booted up:

.. code:: ipython3

    daemon = Service("stream_rpyc")
    daemon.create_timer(on_boot_sec=15)

Example
-------

This module is useful when is combined with package scripts declaration
in ``setup.py`` file:

.. code:: ipython3

    # setup.py
    
    scripts=[
        "cmd/stream_rpyc",
    ]

The script could looks like:

.. code:: ipython3

    #!/usr/bin/env python
    
    import sys
    
    if sys.argv[-1] == "systemd":
        from systemd_service import Service
        daemon = Service("stream_rpyc")
        daemon.create_timer(on_boot_sec=10, after='network.target kafka.service')
    
    else:
        from my_module.submodule import my_service
        print("Run 'stream_rpyc systemd' as superuser to create the daemon.")
        my_service()

Then the command can be called as a simple script but with the
``systemd`` argument the command will turn into a service.

.. code:: ipython3

    $ stream_rpyc
    # Command executed normally

.. code:: ipython3

    $ stream_rpyc systemd
    # Service created
