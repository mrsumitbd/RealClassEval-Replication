from argparse import ArgumentParser
import json

class SensorCmdLine:

    @staticmethod
    def check(sensor_class, args):
        """
        Method to call Sensor.check after parsing args from cmdline
        :param sensor_class: sensor class
        :param args: inline arguments
        :return: True or False
        """
        parser = SensorCmdLine.parsers(sensor_class)
        parsed = parser.parse_args(args)
        return sensor_class.check(json.loads(parsed.data))

    @staticmethod
    def parsers(sensor_class):
        argparser = ArgumentParser(prog=sensor_class.usage, description=sensor_class.description)
        subparsers = argparser.add_subparsers()
        check = subparsers.add_parser('check', help='Check a Sensor')
        check.add_argument('-d', '--data', dest='data', required=True, help='String containing a valid json object')
        check.set_defaults(func=Sensor.check)
        return argparser