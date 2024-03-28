from enum import Enum
from dataclasses import dataclass
from types import MappingProxyType
from ruamel.yaml import YAML

class EInterfaceType(Enum):
    ai = 0
    ao = 1
    di = 2
    do = 3

@dataclass(frozen=True)
class DLabel:
    label: str
    unit: str

@dataclass(frozen=True)
class DChannel:
    ch: int # Key
    id: str
    unit: str
    raw: DLabel
    phy: DLabel

@dataclass(frozen=True)
class DInterface:
    name: EInterfaceType # Key
    num_ch: int
    chs: MappingProxyType[DChannel]

@dataclass(frozen=True)
class DDevice:
    name: str = "" # Key
    driver: str = ""
    id: str = ""
    description: str = ""
    #filter: str
    interface: MappingProxyType = MappingProxyType({})
    environment: MappingProxyType = MappingProxyType({})

@dataclass(frozen=True)
class DConfig:
    globals: MappingProxyType = MappingProxyType({})
    service: MappingProxyType = MappingProxyType({})
    devices: MappingProxyType[DDevice] = MappingProxyType({})

def _DChannelGenerator(index:int, value):
    _ch = index
    _id = _unit = ""
    _raw = DLabel(label="", unit="")
    _phy = DLabel(label="", unit="")
    if 'ch' in value:
        _ch = value['ch']
    if 'id' in value:
        _id = value['id']
    if 'unit' in value:
        _unit = value['unit']
    if 'raw' in value:
        _label = ""
        if 'label' in value['raw']:
            _label = value['raw']['label']
        if 'unit' in value['raw']:
            _unit = value['raw']['unit']
        _raw = DLabel(label=_label, unit=_unit)
    if 'phy' in value:
        _label = ""
        if 'label' in value['raw']:
            _label = value['raw']['label']
        if 'unit' in value['raw']:
            _unit = value['raw']['unit']
        _phy = DLabel(label=_label, unit=_unit)
    return DChannel(ch=_ch, id=_id, unit=_unit, raw=_raw, phy=_phy)

def _DInterfaceGenerator(key: str, value):
    _name = EInterfaceType.ai
    _num_ch = 0
    _chs = MappingProxyType({})
    match key:
        case 'ai':
            _name = EInterfaceType.ai
        case 'ao':
            _name = EInterfaceType.ao
        case 'di':
            _name = EInterfaceType.di
        case 'do':
            _name = EInterfaceType.do
    if 'num_ch' in value:
        _num_ch = value['num_ch']
    if 'chs' in value:
        for index, value in enumerate(value['chs']):
            _chs = _DChannelGenerator(index, value)
    return DInterface(name=_name, num_ch=_num_ch, chs=_chs)

def _DDeviceGenerator(key: str, value):
    _driver = _id = _description = ""
    _interface = MappingProxyType({})
    _environment = MappingProxyType({})
    if 'driver' in value:
        _driver = value['driver']
    if 'id' in value:
        _id = value['id']
    if 'description' in value:
        _description = value['description']
    if 'interface' in value:
        _interface = {}
        for key, val in value['interface'].items():
            _interface[key] = _DInterfaceGenerator(key, val)
        _interface = MappingProxyType(_interface)
    if 'environment' in value:
        _environment = MappingProxyType(value['environment'])
    return DDevice(name=key, driver=_driver, id=_id,
                   description=_description,
                   interface= _interface,
                   environment=_environment)


def ConfigLoader(path: tuple[DDevice]):
    config = DConfig()
    yaml=YAML(typ="safe")
    with open(path, 'r') as f:
        config = yaml.load(f)
    
    _devices = {}
    if "devices" in config:
        for key, value in config["devices"].items():
            _devices[key] = _DDeviceGenerator(key, value)
    config = DConfig(devices=MappingProxyType(_devices))
    return config

if __name__ == "__main__":
    config = ConfigLoader('./config.yaml')
    print(config.devices)