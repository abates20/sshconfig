import os
import re

class Host:
    """
    A class representing an SSH host configuration.

    Attributes
    ----------
    host : str
        The hostname or alias of the host.
    (Other attributes) : various
        Various SSH configuration options.
    """

    def __init__(self, host: str, **kwargs):
        """
        Initialize a Host instance.

        Parameters
        ----------
        Host : str
            The hostname or alias of the host.
        **kwargs
            Additional SSH configuration options.
        """

        self.host: str = host

        for k, v in kwargs.items():
            self[k] = v

    def __repr__(self):
        return f"Host('{self.host}')"

    def __str__(self):
        return f"Host {self.host}"

    def __setitem__(self, name, value):
        self.__setattr__(str(name).lower(), value)

    def __getitem__(self, name):
        name = str(name).lower()
        if name not in dir(self):
            return None
        return self.__getattribute__(name)

    def update(self, **kwargs):
        """
        Update the SSH configuration options of the host.

        Parameters
        ----------
        **kwargs
            Additional SSH configuration options.
        """
        for name, value in kwargs.items():
            self[name] = value

    def options(self):
        """
        Get the SSH configuration options of the host.

        Only includes options that have been specified (i.e., are not `None`).

        Returns
        -------
        dict
            A dictionary containing the SSH configuration options of the host.
        """
        opts: dict[str, ] = {}
        for o in dir(self):
            if not (o.startswith("_") or callable(self[o]) or self[o] is None):
                opts[o] = self[o]
        return opts

    def to_string(self):
        """
        Convert the SSH configuration of the host into a string representation
        that is suitable for writing to the SSH config file.

        Returns
        -------
        str
            A string representation of the SSH configuration of the host.
        """
        options = self.options()
        host = options.pop("host")
        string = f"Host {host}"
        for name, value in options.items():
            string += f"\n\t{name} {value}"
        return string
    
    def matches(self, alias):
        pattern = regex(self.host)
        return bool(re.match(pattern, alias))


class SSHConfig:
    """
    A class representing an SSH configuration file.

    Attributes
    ----------
    _default_path : str
        The default path for the SSH configuration file.
    """

    _default_path = os.path.expanduser("~/.ssh/config")

    def __init__(self, filepath: str = None):
        """
        Initialize an SSHConfig instance.

        Parameters
        ----------
        filepath : str, optional
            The filepath of the SSH configuration file. Defaults to None.
        """
        if filepath is None:
            self.filepath = SSHConfig._default_path
            if not os.path.exists(self.filepath):
                raise FileNotFoundError(f"No filepath was provided and the default path ({SSHConfig._default_path}) does not exist.")
        else:
            self.filepath = filepath

        self.hosts: list[Host] = []

    def __repr__(self) -> str:
        return f"SSHConfig({self.filepath})"

    def __str__(self) -> str:
        return f"SSH config file ({self.filepath})"

    def read(self) -> list[Host]:
        """
        Read the SSH configuration file and parse it into a list of Host objects.

        Returns
        -------
        list[Host]
            A list of Host objects parsed from the SSH configuration file.
        """
        with open(self.filepath, "r") as f:
            lines = f.readlines()

        self.hosts: list[Host] = []
        current_host = None
        host_pattern = r"^Host (.+)$"
        for line in lines:
            new_host = re.match(host_pattern, line.rstrip())

            if new_host:
                current_host = Host(new_host.group(1))
                self.hosts.append(current_host)

            elif current_host is not None:
                items = line.strip().split()
                if len(items) ==  0:
                    continue

                name, value = items
                current_host[name] = value

        return self.hosts

    def to_string(self):
        """
        Convert the SSH configuration into a string representation that
        is suitable for writing to the SSH config file.

        Returns
        -------
        str
            A string representation of the SSH configuration.
        """
        return "\n\n".join([x.to_string() for x in self.hosts])

    def write(self):
        """
        Write the SSH configuration to the file.
        """
        contents = self.to_string()
        with open(self.filepath, "w") as f:
            f.write(contents)

def regex(pattern: str):
    "Convert the shell pattern to a regex pattern"
    # Convert . to \.
    pattern = pattern.replace(".", r"\.")

    # Convert wildcard characters
    pattern = pattern.replace("*", ".*")
    pattern = pattern.replace("?", f".")

    return pattern

def get_config(alias, filepath = None):
    """
    Get the SSH configuration for a specific alias.

    Parameters
    ----------
    alias : str
        The alias for which to retrieve the SSH configuration.
    filepath : str, optional
        The filepath of the SSH configuration file. Defaults to None.

    Returns
    -------
    Host
        The SSH configuration for the specified alias.
    """
    config_file = SSHConfig(filepath)
    config = Host(alias)
    for host in reversed(config_file.read()):
        if host.matches(alias):
            options = host.options()

            # Don't update the Host option
            del options["Host"]

            config.update(**options)
            
    return config

def get_alias(hostname, filepath = None):
    """
    Get the alias corresponding to a specific hostname.

    Parameters
    ----------
    hostname : str
        The hostname for which to retrieve the alias.
    filepath : str, optional
        The filepath of the SSH configuration file. Defaults to None.

    Returns
    -------
    str
        The alias corresponding to the specified hostname.
        Returns None if no matching alias is found.
    """
    config_file = SSHConfig(filepath)
    for host in config_file.read():
        if host["HostName"] == hostname:
            return host.host
    return None