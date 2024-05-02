import os
import re

class _patterns:
    host = r"^Host (.+)$"

class Host:

    def __init__(self, id: str = None):
        self.id: str = id
        self.User: str = None
        self.HostName: str = None
        self.ControlPath: str = None
        self.ControlPersist: str = None
        self.ControlMaster: str = None
        self.ForwardX11: str = None
        self.ServerAliveInternal: str = None

    def __setitem__(self, name, value):
        return self.__setattr__(name, value)

    def __getitem__(self, name):
        if name not in self.__dict__.keys():
            return None
        return self.__getattribute__(name)
    
    def update(self, **kwargs):
        for name, value in kwargs.items():
            if self[name] is None:
                self[name] = value


class SSHConfig:

    _default_path = os.path.expanduser("~/.ssh/config")

    def __init__(self, filepath: str = None):
        if filepath is None:
            self.filepath = SSHConfig._default_path
            if not os.path.exists(self.filepath):
                raise Exception(f"No filepath was provided and the default path ({SSHConfig._default_path}) does not exist.")
        else:
            self.filepath = filepath

    def __repr__(self) -> str:
        return f"SSHConfig({self.filepath})"
    
    def __str__(self) -> str:
        return f"SSH config file ({self.filepath})"
    
    def parse(self) -> list[Host]:
        with open(self.filepath, "r") as f:
            lines = f.readlines()

        hosts: list[Host] = []
        all_host = None
        current_host = None
        for i, line in enumerate(lines):
            new_host = re.match(_patterns.host, line.rstrip())

            if new_host:
                current_host = Host(new_host.group(1))

                if current_host.id == "*":
                    all_host = current_host
                else:
                    hosts.append(current_host)

            elif current_host != None:
                items = line.strip().split()
                if len(items) ==  0:
                    continue

                name, value = items
                current_host[name] = value

        if all_host != None:
            for host in hosts:
                host.update(**all_host.__dict__)

        return hosts