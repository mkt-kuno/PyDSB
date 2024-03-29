import utils

import importlib
import math
import time
import numpy as np

class CDriver:
    def get_driver_type(self):
        pass
    def __init__(self, config:utils.DDevice = utils.DDevice()) -> None:
        pass
    def init(self):
        pass
    def start(self):
        pass
    def stop(self):
        pass
    def get_analog_data(self):
        pass
    def get_digital_data(self):
        pass
    def set_analog_data(self):
        pass
    def set_digital_data(self):
        pass

class Model:
    def _driver_loader(self, dev_config: utils.DDevice) -> CDriver:
        ret = None
        try:
            ret = importlib.import_module(f"drivers.{dev_config.driver}").Driver(dev_config)
            if isinstance(ret, CDriver) != False:
                ret = None
        except Exception as e:
            pass
        return ret

    def test_get_channel_list(self) -> list[utils.DChannel]:
        config = utils.ConfigLoader('./test.yaml')
        for key, value in config.devices.items():
            return value.interface["ai"].chs["0"]

if __name__  == "__main__":
    config = utils.ConfigLoader('./test.yaml')
    dev = None
    for key, value in config.devices.items():
        dev = Model()._driver_loader(value)
    # import drivers.dummy_wave
    # dev = drivers.dummy_wave.Driver()
    dev.start()
    while True:
        print(dev.get_analog_data())
        time.sleep(0.1)