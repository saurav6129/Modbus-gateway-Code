import logging
import pytest
from time import sleep

from pyModbusTCP.client import ModbusClient

from configuration import constants
from configuration.dut import DUT
from system_interfaces.ecs_foundation.fnd_api.proxy import *
from system_interfaces.systemd.fnd_service import WingdModbusGateway
from tests.systemtests.parameterize import *
from system_interfaces.testrig.multi_io.modbus_log import*

datamap_config = "./configuration/datamap_config/io/rs485/rs485_modbus_datamap.json"

args_param_generator = {"io": "ETH_POINT",
                        "unit_list": [DUT.GTU1],
                        "port_lists": [[2]],
                        "mark_lists": [[pytest.mark.targets_on(targets=[DUT.GTU1.value]),
                                        pytest.mark.targets_install_config(targets=[DUT.GTU1.value],
                                                                           config=datamap_config)]]}

unit_io_tuples, unit_io_ids = generate_io_unit_test_parameter(**args_param_generator)


def setup_modbus_gateway(logger, fsm, moodbus_id):
    modbus_gateway = WingdModbusGateway(ssh=fsm, link_name="eth-point-{}".format(moodbus_id))
    modbus_gateway.stop()

    logger.info("Upload wingd-modbus-gateway config.")
    modbus_gateway.upload_config("./configuration/datamap_config/io/rs485/wingd-modbus-gateway_new.json")
    sleep(1)

    logger.info("Start wingd-modbus-gateway")
    assert modbus_gateway.start()[2] == 0


@pytest.mark.parametrize("unit, io_channel", unit_io_tuples, ids=unit_io_ids)
#@pytest.mark.requirements(at=["WINGDECSAT-156"], rq=["WINGDECSRQ-245"])
def test_modbus_log(target_testrig, logger, fsm_targets, unit, io_channel):

    
   
    fsm = fsm_targets[unit.value]
    fnd_api = fsm.get_fnd_api()
    sleep(10)
    setup_modbus_gateway(logger, fsm, io_channel)
    sleep(2)
    ip_target = fsm_targets[unit.value].get_ip_eth_point(io_channel)
    logger.info("Target ip is {}".format(ip_target))
    modbus_client = ModbusClient(host=ip_target, port=502, auto_open=True, auto_close=True)
    logger.info("modbus_client response {}".format(modbus_client))
	
	#Sending Modbus request on invalid coil
    logger.info("Sending Modbus Request on invalid coil")
    modbus_client.read_coils(15000,1)
    sleep(0.4)
    current_time = datetime.now()
    response = get_command_to_run_journal(logger,fsm_targets,current_time,1)
    assert response <= 10.00
    sleep(5)
	
	#Sending single request to read invalid registers
    logger.info("Sending Modbus Read invalid register request")
    modbus_client.read_coils(36720,1)
    sleep(0.4)
    current_time = datetime.now()
    response = get_command_to_run_journal(logger,fsm_targets,current_time,2)
    assert response <= 10.00
    sleep(2)
	
	#Sending continuous request on coil to check rate limited message
    #changed time to 1 sec
    logger.info("Shooting continuous request on invalid coil")
    for i in range(0,6):
        modbus_client.read_coils(15000,1)
        sleep(1)
    current_time = datetime.now()
    sleep(5)
    response = get_command_to_run_journal(logger,fsm_targets,current_time,1)
    assert response <= 10.00
    sleep(5)
	
	#Shooting continuous request on invalid register to check limited message
    #changed time to 0.1 from 0.4
    #Ticket no 214 testcase 1
    logger.info("Shooting continuous request on invalid input register")
    for i in range(0,6):
        modbus_client.read_input_registers(36720,1)
        sleep(0.1)
    current_time = datetime.now()
    sleep(5)
    response = get_command_to_run_journal(logger,fsm_targets,current_time,3)
    assert response <=10.00
    sleep(5)
	
    #Write request on the coil
    logger.info("Write coil request")
    modbus_client.write_single_coil(10001,1)
    sleep(0.4)
    current_time = datetime.now()
    response = get_command_to_run_journal(logger,fsm_targets,current_time,4)
    assert response <= 10.00
    sleep(5)
    
    #Write rate limited coil
    logger.info("Write multiple coil request")
    for i in range (0,6):
        modbus_client.write_single_coil(10001,1)
        sleep(0.4)
    current_time = datetime.now()
    sleep(5)
    response = get_command_to_run_journal(logger,fsm_targets,current_time,5)
    assert response <= 10.00
    sleep(5)
    
    #Write rate limited register
    logger.info("Write on multiple register")
    for i in range(0,6):
        modbus_client.write_single_register(30001,1)
        sleep(0.4)
    current_time = datetime.now()
    sleep(5)
    response = get_command_to_run_journal(logger,fsm_targets,current_time,5)
    assert response <= 10.00
    sleep(5)
    
    
    #Valid Read Request
    logger.info("Sending Modbus Read invalid Discrete input request")
    modbus_client.read_input_registers(2,1)
    sleep(0.4)
    current_time = datetime.now()
    response = get_command_to_run_journal(logger,fsm_targets,current_time,6)
    assert response <= 10.00
    sleep(5)
    
    #Valid Read Request Rate Limited
    #changed time to 0.1 from 0.4 sec
    logger.info("Sending Modbus Read input register valid  request")
    for i in range(0,6):
        modbus_client.read_input_registers(1, 1)
        sleep(0.1)
    
    current_time = datetime.now()
    response = get_command_to_run_journal(logger,fsm_targets,current_time,6)
    assert response <= 10.00
    sleep(5)
    