import unittest
import nose2

from unittest import expectedFailure
from mock import Mock, MagicMock

import drone


class DroneProtocolMathTestCase(unittest.TestCase):
    def test_denormalization(self):
        denorm = drone._denormalize_
        self.assertEqual(denorm(-1), 0)
        self.assertEqual(denorm(-0.5), 64)
        self.assertEqual(denorm(0), 128)
        self.assertEqual(denorm(0.5), 191)
        self.assertEqual(denorm(1), 255)


class AtGroundDroneProtocolTestCase(unittest.TestCase):
    # @expectedFailure
    def test_idle(self):
        expected_command = '6680800080008099'.decode('hex')
        command = drone.get_command_string(
            roll=0.0, pitch=0.0, throttle=0.0, yaw=0.0, command=None,
            altitude_hold=False
        )
        self.assertEqual(command, expected_command)

    def test_idle_altitude_hold(self):
        expected_command = '6680808080000099'.decode('hex')
        command = drone.get_command_string(
            roll=0.0, pitch=0.0, throttle=0.0, yaw=0.0, command=None,
        )
        self.assertEqual(command, expected_command)

    def test_spin_up_altitude_hold(self):
        expected_command = '6680808080010199'.decode('hex')
        command = drone.get_command_string(
            roll=0.0, pitch=0.0, throttle=0.0, yaw=0.0, command='spin_up',
        )
        self.assertEqual(command, expected_command)

    def test_shut_engines_altitude_hold(self):
        expected_command = '6680808080040499'.decode('hex')
        command = drone.get_command_string(
            roll=0.0, pitch=0.0, throttle=0.0, yaw=0.0, command='shut_off',
        )
        self.assertEqual(command, expected_command)

    @expectedFailure
    def test_land_altitude_hold(self):
        expected_command = '00'.decode('hex')
        command = drone.get_command_string(
            roll=0.0, pitch=0.0, throttle=0.0, yaw=0.0, command='land',
        )
        self.assertEqual(command, expected_command)


class InFlightDroneProtocolTestCase(unittest.TestCase):
    """ these values are from adria's post:
    https://hackaday.io/project/19680-controlling-a-jjrc-h37-elfie-quad-from-a-pc/log/\
    53557-a-basic-script-to-monitor-the-controller-input-sent-to-the-quadcopter-by-udp
    """
    def test_flight(self):
        # 66807f0180007e99 roll:128 pitch:127 throttle:1 yaw:128 commands:00000000 err:7e
        expected_command = '66807f0180007e99'
        command = drone.get_command_string(
            roll=0.0, pitch=-0.004, throttle=0.004, yaw=0.0, command=None,
            altitude_hold=False
        ).encode('hex')
        self.assertEqual(command, expected_command)

        # 666b840080006f99 roll:107 pitch:132 throttle:0 yaw:128 commands:00000000 err:6f
        expected_command = '666b840080006f99'
        command = drone.get_command_string(
            roll=-0.16, pitch=0.035, throttle=0.0, yaw=0.0, command=None,
            altitude_hold=False
        ).encode('hex')
        self.assertEqual(command, expected_command)