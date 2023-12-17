from charlcd import buffered as lcd
from charlcd.drivers.gpio import Gpio
import RPi.GPIO as GPIO
import math
import logging

logger = logging.getLogger(__name__)

GPIO.setmode(GPIO.BCM)

STATUS_LOADED = 1
STATUS_STARTED = 2

STATUS_ERROR = 4
STATUS_CRASHED = 5


class ModuleStatus(object):
    def __init__(self, name, x, y, status=1):
        self.status = 1
        self.name = name
        self.x = x
        self.y = y


class Dump(object):
    display = {}
    modules = {}
    enabled = False
    lock = False

    def __init__(self, enabled):
        Dump.enabled = enabled
        if enabled:
            logger.info("LCD enabled")
            drv = Gpio()
            drv.pins['E2'] = 10
            drv.pins['E'] = 24
            Dump.display = lcd.CharLCD(40, 4, drv, 0, 0)
            Dump.display.init()

    @classmethod
    def module_status(cls, params):
        if params['name'] not in cls.modules:
            x = 0
            y = 0
            x = math.floor(len(cls.modules) / 4)
            y = len(cls.modules) % 4
            mod_status = ModuleStatus(params['name'], x*7, y)
            cls.modules[params['name']] = mod_status
        if "status" in params:
            cls.modules[params['name']].status = params['status']

        cls.draw_status(cls.modules[params['name']])

    @classmethod
    def display_event(cls, params):
        cls.display.write(params['text'])
        cls.display.flush()

    @classmethod
    def draw_status(cls, module_status):
        if cls.enabled:
            if module_status.status == STATUS_LOADED:
                text = "."
            if module_status.status == STATUS_STARTED:
                text = "+"
            if module_status.status == STATUS_ERROR:
                text = "#"
            if module_status.status == STATUS_CRASHED:
                text = "!"

            cls.display.write(
                text+module_status.name,
                module_status.x,
                module_status.y
            )
            while cls.lock == True:
                pass
            cls.lock = True
            cls.display.flush()
            cls.lock = False

    @classmethod
    def refresh(cls):
        if cls.enabled:
            cls.display.flush(True)
