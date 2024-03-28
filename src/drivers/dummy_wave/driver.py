import Utils
import Model

import time
import numpy as np
import math

class Driver(Model.CDriver):
    def __init__(self, config:Utils.DDevice = Utils.DDevice()) -> None:
        super().__init__(config)
        self._mode = "sin"
        if isinstance(config, Utils.DDevice) and 'mode' in config.environment:
            mode = config.environment['mode']
            if mode in ("sin","cos","tan", "square"):
                self._mode = mode
    
    def start(self):
        pass
    def stop(self):
        pass
    def get_analog_data(self, ch: int = -1):
        ret = np.array(np.float32(0.0))
        match self._mode:
            case "sin":
                ret = np.array([math.sin(time.time()*2)], dtype=np.float32)
            case "cos":
                ret = np.array([math.cos(time.time()*2)], dtype=np.float32)
            case "tan":
                ret = np.array([math.tan(time.time()*2)], dtype=np.float32)
            case "square":
                ret = np.array([math.sin(time.time()*2) > 0], dtype=np.float32) * 2 - 1.0
            
        return ret
