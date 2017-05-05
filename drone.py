import socket


# The IP of the quadcopter plus the UDP port it listens to for control commands
IP = '172.16.10.1'
PORT = 8895


class ConnectionError(Exception):
    pass


# some basic math
def _denormalise_(value):
    """ converts value from [-1:+1] range to [0:255] """
    return int(round((value + 1.0)*127.5))


idle_command = '6680800180008199'.decode('hex')

def get_command_string(
        roll=0.0, pitch=0.0, throttle=0.0, yaw=0.0, command=None,
        altitude_hold=True, headless=False
    ):
    roll = _denormalise_(roll)
    pitch = _denormalise_(pitch)
    if not altitude_hold:
        if throttle < 0:
            throttle = 0
        throttle = throttle*2 - 1
    throttle = _denormalise_(throttle)
    yaw = _denormalise_(yaw)
    command = {
        None: 0x0,
        'calibrate': '?',
        'spin_up': 0x1,
        'shut_off': 0x4,
        'land': 0x0,  # TODO: fix
    }[command]
    checksum = roll ^ pitch ^ throttle ^ yaw ^ command
    return '66{:02x}{:02x}{:02x}{:02x}{cmd:02x}{csum:02x}99'.format(
        roll,
        pitch,
        throttle,
        yaw,
        cmd=command,
        csum=checksum,
    ).decode('hex')


class Drone(object):
    is_connected = False

    def connect(self, ip=IP, port=PORT):
        # initialize a UDP socket
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.connection.connect((ip, port))

    def execute(self, command):
        if not self.is_connected:
            self.connect()
        self.connection.send(command)

    def disconnect(self):
        pass
        # self.connection.close()