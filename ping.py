class Ping(object):

    def __init__(self, ip, port=4370):
        self.ip = ip

    def test(self):
        """
        Returns True if host responds to a ping request

        :return: bool
        """
        import subprocess, platform
        # Ping parameters as function of OS
        ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1 -W 5"
        args = "ping " + " " + ping_str + " " + self.ip
        need_sh = False if  platform.system().lower()=="windows" else True
        # Ping
        return subprocess.call(args,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=need_sh) == 0