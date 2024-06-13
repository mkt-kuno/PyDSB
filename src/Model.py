import utils
import time

class Model:
    def __init__(self) -> None:
        self._config = utils.ConfigLoader('./config.yaml')
        #self._config = utils.ConfigLoader('./test.yaml')
        self._driver_loaded = []
        for _, value in self._config.devices.items():
            driver = utils.DriverLoader(value)
            if driver is None:
                continue
            self._driver_loaded.append(driver)
            ai = value.interface["ai"]
            print("dev_id: %s" % (str(value.id)))
            for ch in range(ai.num_ch):
                chs_key = str(ch)
                if chs_key in ai.chs:
                    dchannel = ai.chs[chs_key]
                    print("\tch_id: %s" % (str(dchannel.id)))
        
    def init_all_devices(self):
        for driver in self._driver_loaded:
            driver.init()
    
    def start_all_devices(self):
        for driver in self._driver_loaded:
            driver.start()
    
    def stop_all_devices(self):
        for driver in self._driver_loaded:
            driver.stop()

    def exit_all_devices(self):
        for driver in self._driver_loaded:
            driver.exit()

    def get_di_config_list(self) -> list[utils.DChannel]:
        pass

    def get_ai_config_list(self) -> list[utils.DChannel]:
        pass

    # def test_get_channel_list(self) -> list[utils.DChannel]:
    #     config = utils.ConfigLoader('./test.yaml')
    #     for key, value in config.devices.items():
    #         return value.interface["ai"].chs["0"]

if __name__  == "__main__":
    model = Model()
    model.get_ai_config_list()
    # dev = None
    # for key, value in config.devices.items():
    #     dev = Model()._driver_loader(value)
    # import drivers.dummy_wave
    # dev = drivers.dummy_wave.Driver()
    # dev.start()
    # for _ in range(10):
    #     print(dev.get_analog_data())
    #     time.sleep(0.1)
    # dev.stop()
    pass