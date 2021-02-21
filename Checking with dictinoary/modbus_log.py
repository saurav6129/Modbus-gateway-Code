#Modbus log
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
from tests.systemtests.parameterize import *



def modbus_check_read_invalid_coil(logger,fsm_targets,current_time):
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
	
    logger.info("Reading journal on GTU-1 ")
    
    journal_remote_command = "journalctl -r | grep 'unknown modbus Coil addr ' -m 1"
    log_result = fsm_targets[DUT.GTU1.value].run(journal_remote_command)
	logger.info("The logged message on the GTU is {}".format(log_result)
	logger.info("The time of modbus request is {}".format(current_time))
	diff_log = extract_date_diff(logger,log_result,current_time)
	return diff_log


def modbus_check_read_invalid_register(logger,fsm_targets,current_time):
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
    
    journal_remote_command = "journalctl -r | grep 'unknown modbus InputRegister ' -m 1"
    log_result = fsm_targets[DUT.GTU1.value].run(journal_remote_command)
	logger.info("The logged message on the GTU is {}".format(log_result)
	logger.info("The time of modbus request is {}".format(current_time))
	diff_log = extract_date_diff(logger,log_result,current_time)
	return diff_log

	
def modbus_check_read_invalid_register_rate_limited(logger,fsm_targets,current_time):
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
    
    journal_remote_command = "journalctl -r | grep 'unknown modbus InputRegisters ' -m 1"
    log_result = fsm_targets[DUT.GTU1.value].run(journal_remote_command)
	logger.info("The logged message on the GTU is {}".format(log_result)
	logger.info("The time of modbus request is {}".format(current_time))
	diff_log = extract_date_diff(logger,log_result,current_time)
	return diff_log


def modbus_check_write_request(logger,fsm_targets,current_time):
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
    
    journal_remote_command = "journalctl -r | grep 'Modbus write action not allowed in WiCE ' -m 1"
    log_result = fsm_targets[DUT.GTU1.value].run(journal_remote_command)
	logger.info("The logged message on the GTU is {}".format(log_result)
	logger.info("The time of modbus request is {}".format(current_time))
	diff_log = extract_date_diff(logger,log_result,current_time)
	return diff_log
	

def modbus_check_write_request(logger,fsm_targets,current_time):
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
    
    journal_remote_command = "journalctl -r | grep 'Modbus write action not allowed in WiCE ' -m 1"
    log_result = fsm_targets[DUT.GTU1.value].run(journal_remote_command)
    logger.info("The logged message on the GTU is {}".format(log_result)
    logger.info("The time of modbus request is {}".format(current_time))
    diff_log = extract_date_diff(logger,log_result,current_time)
    return diff_log
    
def modbus_check_write_request_ratelimiter(logger,fsm_targets,current_time):
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
    
    journal_remote_command = "journalctl -r | grep 'Modbus write action log is ratelimited ' -m 1"
    log_result = fsm_targets[DUT.GTU1.value].run(journal_remote_command)
    logger.info("The logged message on the GTU is {}".format(log_result)
    logger.info("The time of modbus request is {}".format(current_time))
    diff_log = extract_date_diff(logger,log_result,current_time)
    return diff_log

def modbus_check_read_valid_request(logger,fsm_targets,current_time):
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
    
    journal_remote_command = "journalctl -r | grep 'has started polling data ' -m 1"
    log_result = fsm_targets[DUT.GTU1.value].run(journal_remote_command)
    logger.info("The logged message on the GTU is {}".format(log_result)
    logger.info("The time of modbus request is {}".format(current_time))
    diff_log = extract_date_diff(logger,log_result,current_time)
    return diff_log

    
    