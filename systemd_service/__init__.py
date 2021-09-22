import os


########################################################################
class Service:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, name, path=None):
        """Constructor"""
        self.name = name
        self.path = path

    # ----------------------------------------------------------------------
    def stop(self, unit='service'):
        """"""
        os.system(f"systemctl stop {self.name}.{unit}")

    # ----------------------------------------------------------------------
    def start(self, unit='service'):
        """"""
        os.system(f"systemctl start {self.name}.{unit}")

    # ----------------------------------------------------------------------
    def restart(self, unit='service'):
        """"""
        os.system(f"systemctl restart {self.name}.{unit}")

    # ----------------------------------------------------------------------
    def enable(self, unit='service'):
        """"""
        os.system(f"systemctl enable {self.name}.{unit}")

    # ----------------------------------------------------------------------
    def reload(self):
        """"""
        os.system("systemctl daemon-reload")

    # ----------------------------------------------------------------------
    def remove(self, unit='service'):
        """"""
        file = f"/etc/systemd/system/{self.name}.{unit}"
        if os.path.exists(file):
            os.remove(file)

    # ----------------------------------------------------------------------
    def create_service(self, after=None):
        """"""

        if after:
            after = f'After={after}'
        else:
            after = ''

        systemd_script = f'''[Unit]
Description="{self.name}"
{after}
StartLimitIntervalSec=500
StartLimitBurst=5

[Service]
Type=simple
ExecStart={self.path}
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target'''

        self.stop()
        self.remove()
        with open(f"/etc/systemd/system/{self.name}.service", 'w') as file:
            file.write(systemd_script)
        self.reload()

    # ----------------------------------------------------------------------
    def create_timer(self, on_boot_sec=15, *args, **kwargs):
        """"""
        systemd_script = f'''[Unit]
Description = "{self.name}"

[Timer]
OnBootSec = {on_boot_sec}s
Unit = {self.name}.service

[Install]
WantedBy = timers.target
        '''

        self.create_service(*args, **kwargs)
        self.stop(unit='timer')
        self.remove(unit='timer')
        with open(f"/etc/systemd/system/{self.name}.timer", 'w') as file:
            file.write(systemd_script)
        self.reload()
