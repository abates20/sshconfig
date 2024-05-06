import os
import re

class OptionSet:

    _options: list[str] = []

    @classmethod
    def get(cls, value):
        _value = str(value).lower()
        for option in cls._options:
            if _value == option.lower():
                return option
        raise Exception(f"Not a valid value: {value}. Valid options are {', '.join(cls._options)}")

class LogLevel(OptionSet):
    QUIET = "QUIET"
    FATAL = "FATAL"
    ERROR = "ERROR"
    INFO = "INFO"
    VERBOSE = "VERBOSE"
    DEBUG = "DEBUG"
    DEBUG1 = "DEBUG1"
    DEBUG2 = "DEBUG2"
    DEBUG3 = "DEBUG3"

    _options = [QUIET, FATAL, ERROR, INFO, VERBOSE,
                DEBUG, DEBUG1, DEBUG2, DEBUG3]

class YesNo(OptionSet):
    YES = "yes"
    NO = "no"

    _options = [YES, NO]


class Host:

    def __init__(self, Host: str, **kwargs):
        self.Host: str = Host

        self.AddKeysToAgent: str = None
        self.AddressFamily: str = None

        self.BatchMode: str = None
        self.BindAddress: str = None
        self.BindInterface: str = None

        self.CanonicalDomains: str = None
        self.CanonicalizeFallbackLocal: str = None
        self.CanonicalizeHostname: str = None
        self.CanonicalizeMaxDots: str = None
        self.CanonicalizePermittedCNAMEs: str = None
        self.CASignatureAlgorithms: str = None
        self.CertificateFile: str = None
        self.ChannelTimeout: str = None
        self.CheckHostIP: str = None
        self.Ciphers: str = None
        self.ClearAllForwardings: str = None
        self.Compression: str = None
        self.ConnectionAttempts = None
        self.ConnectTimeout = None
        self.ControlMaster: str = None
        self.ControlPath: str = None
        self.ControlPersist: str = None

        self.DynamicForward: str = None

        self.EnableEscapeCommandline: str = None
        self.EnableSSHKeysign: str = None
        self.EscapeChar: str = None
        self.ExitOnForwardFailure: str = None

        self.FingerprintHash: str = None
        self.ForkAfterAuthentication: str = None
        self.ForwardAgent: str = None
        self.ForwardX11: str = None
        self.ForwardX11Timeout: str = None
        self.ForwardX11Trusted: str = None

        self.GatewayPorts: str = None
        self.GlobalKnownHostsFile: str = None
        self.GSSAPIAuthentication: str = None
        self.GSSAPIDelegateCredentials: str = None

        self.HashKnownHosts: str = None
        self.HostbasedAcceptedAlgorithms: str = None
        self.HostbasedAuthentication: str = None
        self.HostKeyAlgorithms: str = None
        self.HostKeyAlias: str = None
        self.Hostname: str = None

        self.IdentitiesOnly: str = None
        self.IdentityAgent: str = None
        self.IdentityFile: str = None
        self.IgnoreUnknown: str = None
        self.Include: str = None
        self.IPQoS: str = None

        self.KbdInteractiveAuthentication: str = None
        self.KbdInteractiveDevices: str = None
        self.KexAlgorithms: str = None
        self.KnownHostsCommand: str = None

        self.LocalCommand: str = None
        self.LocalForward: str = None
        self.LogLevel: str = None
        self.LogVerbose: str = None

        self.MACs: str = None

        self.NoHostAuthenticationForLocalhost: str = None
        self.NumberOfPasswordPrompts: str = None

        self.ObscureKeystrokeTiming: str = None

        self.PasswordAuthentication: str = None
        self.PermitLocalCommand: str = None
        self.PermitRemoteOpen: str = None
        self.PKCS11Provider: str = None
        self.Port: str = None
        self.PreferredAuthentications: str = None
        self.ProxyCommand: str = None
        self.ProxyJump: str = None
        self.ProxyUseFdpass: str = None
        self.PubkeyAcceptedAlgorithms: str = None
        self.PubkeyAuthentication: str = None

        self.RekeyLimit: str = None
        self.RemoteCommand: str = None
        self.RemoteForward: str = None
        self.RequestTTY: str = None
        self.RequiredRSASize: str = None
        self.RevokedHostKeys: str = None

        self.SecurityKeyProvider: str = None
        self.SendEnv: str = None
        self.ServerAliveCountMax = None
        self.ServerAliveInterval = None
        self.SessionType: str = None
        self.SetEnv: str = None
        self.StdinNull: str = None
        self.StreamLocalBindMask: str = None
        self.StreamLocalBindUnlink: str = None
        self.StrictHostKeyChecking: str = None
        self.SyslogFacility: str = None

        self.TCPKeepAlive: str = None
        self.Tag: str = None
        self.Tunnel: str = None
        self.TunnelDevice: str = None

        self.UpdateHostKeys: str = None
        self.User: str = None
        self.UserKnownHostsFile: str = None

        self.VerifyHostKeyDNS: str = None
        self.VisualHostKey: str = None

        self.XAuthLocation: str = None

        for k, v in kwargs.items():
            self[k] = v

    def __repr__(self):
        return f"Host('{self.Host}')"

    def __str__(self):
        return f"Host {self.Host}"

    def __setitem__(self, name, value):
        return self.__setattr__(name, value)

    def __getitem__(self, name):
        if name not in dir(self):
            return None
        return self.__getattribute__(name)

    def update(self, **kwargs):
        for name, value in kwargs.items():
            self[name] = value

    def options(self):
        opts: dict[str, ] = {}
        for o in dir(self):
            if not (o.startswith("_") or callable(self[o]) or self[o] is None):
                opts[o] = self[o]
        return opts

    def to_string(self):
        options = self.options()
        host = options.pop("Host")
        string = f"Host {host}"
        for name, value in options.items():
            string += f"\n\t{name} {value}"
        return string

    @property
    def ConnectionAttempts(self):
        return self._ConnectionAttempts

    @ConnectionAttempts.setter
    def ConnectionAttempts(self, value):
        self._ConnectionAttempts = int(value) if value else value

    @property
    def ConnectTimeout(self):
        return self._ConnectTimeout

    @ConnectTimeout.setter
    def ConnectTimeout(self, value):
        self._ConnectTimeout = int(value) if value else value

    @property
    def ControlPersist(self):
        return self._ControlPersist

    @ControlPersist.setter
    def ControlPersist(self, value):
        self._ControlPersist = YesNo.get(value) if value else value

    @property
    def ForwardX11(self):
        return self._ForwardX11

    @ForwardX11.setter
    def ForwardX11(self, value):
        self._ForwardX11 = YesNo.get(value) if value else value

    @property
    def LogLevel(self):
        return self._LogLevel

    @LogLevel.setter
    def LogLevel(self, value):
        self._LogLevel = LogLevel.get(value) if value else value

    @property
    def NumberOfPasswordPrompts(self):
        return self._NumberOfPasswordPrompts

    @NumberOfPasswordPrompts.setter
    def NumberOfPasswordPrompts(self, value):
        self._NumberOfPasswordPrompts = int(value) if value else value

    @property
    def ServerAliveCountMax(self):
        return self._ServerAliveCountMax

    @ServerAliveCountMax.setter
    def ServerAliveCountMax(self, value):
        self._ServerAliveCountMax = int(value) if value else value

    @property
    def ServerAliveInterval(self):
        return self._ServerAliveInterval

    @ServerAliveInterval.setter
    def ServerAliveInterval(self, value):
        self._ServerAliveInterval = int(value) if value else value


class SSHConfig:

    _default_path = os.path.expanduser("~/.ssh/config")

    def __init__(self, filepath: str = None):
        if filepath is None:
            self.filepath = SSHConfig._default_path
            if not os.path.exists(self.filepath):
                raise Exception(f"No filepath was provided and the default path ({SSHConfig._default_path}) does not exist.")
        else:
            self.filepath = filepath

        self.hosts: list[Host] = []

    def __repr__(self) -> str:
        return f"SSHConfig({self.filepath})"

    def __str__(self) -> str:
        return f"SSH config file ({self.filepath})"

    def read(self) -> list[Host]:
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
        return "\n\n".join([x.to_string() for x in self.hosts])

    def write(self):
        contents = self.to_string()
        with open(self.filepath, "w") as f:
            f.write(contents)
