import utils

import copy
import json
import numpy as np
import serial
import time
import threading

class Driver(utils.CDriver):
    def __init__(self, config:utils.DDevice = utils.DDevice()) -> None:
        super().__init__(config)
        self._port = "COM4"
        self._is_running = False
        self._data = []
        if isinstance(config, utils.DDevice) and 'port' in config.environment:
            self._port = config.environment['port']
    
    def task(self):
        ser = serial.Serial('COM4', 115200)
        while self._is_running:
            line = ser.readline()
            line = line.decode('ascii')
            try:
                j = json.loads(line)
                if 'hx711' not in j:
                    continue
                data = np.array(j['hx711'], dtype=np.float32)/np.iinfo(np.int32).max
                self._lock.acquire()
                self._data = copy.deepcopy(data)
                self._lock.release()
            except json.JSONDecodeError as err:
                continue
            except Exception as err:
                print(err)
                break
            time.sleep(0.1)
        ser.close()

    def start(self):
        self._thread = threading.Thread(target=self.task, daemon=True)
        self._lock = threading.Lock()
        self._is_running = True
        self._thread.start()
        
    def stop(self):
        self._is_running = False
        self._thread.join()

    def get_analog_data(self, ch: int = -1):
        ret = []
        self._lock.acquire()
        ret = copy.deepcopy(self._data)
        self._lock.release()
        return ret
