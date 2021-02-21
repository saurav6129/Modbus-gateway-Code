import logging
import pytest
import time 
import re
from datetime import datetime
from random import randint
from time import sleep
from pyModbusTCP.client import ModbusClient
from system_interfaces.testrig.modbus import *
from configuration import constants
from configuration.dut import DUT
from system_interfaces.ecs_foundation.fnd_api.proxy import *
from system_interfaces.systemd.fnd_service import WingdModbusGateway
from tests.systemtests.parameterize import *
from state_machine.control_unit import *
from system_interfaces.testrig.multi_io.date_time_diff import *




command_select_for_journal = {
								1:"journalctl -r | grep 'unknown modbus Coil addr ' -m 1",
								2:"journalctl -r | grep 'unknown modbus InputRegisters ' -m 1",#normal
								3:"journalctl -r | grep 'unknown modbus InputRegister ' -m 1",#ratelimited
								4:"journalctl -r | grep 'Modbus write action not allowed in WiCE ' -m 1",
								5:"journalctl -r | grep 'Modbus write action log is ratelimited ' -m 1",
								6:"journalctl -r | grep 'has started polling data ' -m 1"}


#function to fetch and perform 
def get_command_to_run_journal(logger,fsm_targets,current_time,command_id):

    logger.info("Wait if uptime of GTU is smaller than 120s. ")
    while True:
        uptime = fsm_targets[DUT.GTU1.value].run(" cat /proc/uptime | cut -d ' ' -f1")
        assert uptime[2] == 0
        uptime = float(uptime[0][0])
        if uptime > 120.0:
            break
        sleep(1)
		
    logger.info("Defining log target")
    log_targets = [DUT.GTU1.value]
    logger.info("Reading journal on GTU-1 after 10 sec")
    journal_remote_command = command_select_for_journal[command_id]
    log_result = fsm_targets[DUT.GTU1.value].run(journal_remote_command)
    logger.info("The logged message on the GTU is {}".format(log_result)
    logger.info("The time of modbus request is {}".format(current_time))
    diff_log = extract_date_diff(logger,log_result,current_time)
    return diff_log
	
	

