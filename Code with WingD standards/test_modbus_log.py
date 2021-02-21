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

def test_modbus_log_valid_input_registers(target_testrig, logger, fsm_targets, unit, io_channel):

	"""
    Requirement:WINGDECSAT-212
	Description
	Test Case 1: Log Modbus master session
	Requirement : WINGDECSAT-212

	Setup:

	WiCE 1-X Plus Test Rig
	GTU -1 is device under test (DUT)
	Systemtest server
	Given:

	GTU-1 is up and running.
	When:

	Setup connection with GTU1 on eth-pont-2
	Send multiple read command to gtu1 with valid input register address every 100ms.
	Read log message from gtu1.
 

	Then:

	Log shall be available
	
    """
	#Given
    fsm = fsm_targets[unit.value]
    fnd_api = fsm.get_fnd_api()
    sleep(10)
    setup_modbus_gateway(logger, fsm, io_channel)
    sleep(2)
    ip_target = fsm_targets[unit.value].get_ip_eth_point(io_channel)
    logger.info("Target ip is {}".format(ip_target))
    modbus_client = ModbusClient(host=ip_target, port=502, auto_open=True, auto_close=True)
    logger.info("modbus_client response {}".format(modbus_client))
	
	#When
	#Then
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

@pytest.mark.parametrize("unit, io_channel", unit_io_tuples, ids=unit_io_ids)
def test_modbus_log_write_access(target_testrig, logger, fsm_targets, unit, io_channel):

	"""
		Description
		Test Case 1: Modbus: Log unsuccessful master write access
		
		Requirement - WINGDECSAT-215
		Setup:

		WiCE 1-X Plus Test Rig
		GTU-1 is device under test (DUT)
		Systemtest server
		Given:

		GTU-1 is up and running
		When:

		Setup connection with DUT on ETH-POINT-2
		Send single write command to DUT
		Read log message from DUT
        
		Then:
		Unknown Modbus address log shall be available
		
	"""
	#Given
    fsm = fsm_targets[unit.value]
    fnd_api = fsm.get_fnd_api()
    sleep(10)
    setup_modbus_gateway(logger, fsm, io_channel)
    sleep(2)
    ip_target = fsm_targets[unit.value].get_ip_eth_point(io_channel)
    logger.info("Target ip is {}".format(ip_target))
    modbus_client = ModbusClient(host=ip_target, port=502, auto_open=True, auto_close=True)
    logger.info("modbus_client response {}".format(modbus_client))
	
	#When
	#Then
    logger.info("Write on single register")
    modbus_client.write_single_register(30001,1)
    sleep(0.4)
    current_time = datetime.now()
    sleep(5)
    response = get_command_to_run_journal(logger,fsm_targets,current_time,4)
    assert response <= 10.00
    sleep(5)
    

@pytest.mark.parametrize("unit, io_channel", unit_io_tuples, ids=unit_io_ids)	
def test_modbus_log_invalid_input_registers(target_testrig, logger, fsm_targets, unit, io_channel):

	"""
        Requirement : WINGDECSAT-213
		Description
		Test Case 1: Modbus: Log unsuccessful master read access with invalid address

		Setup:

		WiCE 1-X Plus Test Rig
		GTU -1 is device under test (DUT)
		Systemtest server
		Given:

		GTU-1 is up and running.
		When:

		Setup connection with GTU1 on eth-pont-2
		Send single read command to gtu1 with invalid or wrong input register address.
		Read log message from gtu1.
 

		Then:

		Unknown Modbus address log shall be available
	
    """
	#Given
    fsm = fsm_targets[unit.value]
    fnd_api = fsm.get_fnd_api()
    sleep(10)
    setup_modbus_gateway(logger, fsm, io_channel)
    sleep(2)
    ip_target = fsm_targets[unit.value].get_ip_eth_point(io_channel)
    logger.info("Target ip is {}".format(ip_target))
    modbus_client = ModbusClient(host=ip_target, port=502, auto_open=True, auto_close=True)
    logger.info("modbus_client response {}".format(modbus_client))
	
	#When
	#Then
    logger.info("Sending Modbus Read invalid register request")
    modbus_client.input_registers(36720,1)
    sleep(0.4)
    current_time = datetime.now()
    response = get_command_to_run_journal(logger,fsm_targets,current_time,2)
    assert response <= 10.00
    sleep(2)
    
@pytest.mark.parametrize("unit, io_channel", unit_io_tuples, ids=unit_io_ids)
def test_multiple_read_input_register(target_testrig, logger, fsm_targets, unit, io_channel):

	"""
        Requirement : WINGDECSAT-213
        Test Case 2: Modbus: Log unsuccessful master read access with invalid address
		Setup:

		WiCE 1-X Plus Test Rig
		GTU -1 is device under test (DUT)
		Systemtest server
		Given:

		GTU-1 is up and running.
		When:
	
		Setup connection with GTU1 on eth-pont-2
		Send multiple read command to gtu1 with invalid or wrong input register address every 1 sec.
		Read log message from gtu1.
 

		Then:

		Unknown Modbus address log shall be available
    """
	#Given
    fsm = fsm_targets[unit.value]
    fnd_api = fsm.get_fnd_api()
    sleep(10)
    setup_modbus_gateway(logger, fsm, io_channel)
    sleep(2)
    ip_target = fsm_targets[unit.value].get_ip_eth_point(io_channel)
    logger.info("Target ip is {}".format(ip_target))
    modbus_client = ModbusClient(host=ip_target, port=502, auto_open=True, auto_close=True)
    logger.info("modbus_client response {}".format(modbus_client))
	
	#When
	#Then
	#Check invalid messages
    logger.info("Shooting continuous request on invalid input register")
    for i in range(0,6):
        modbus_client.read_input_registers(36720,1)
        sleep(1)
    current_time = datetime.now()
    sleep(5)
    response = get_command_to_run_journal(logger,fsm_targets,current_time,2)
    assert response <=10.00
    sleep(5)

@pytest.mark.parametrize("unit, io_channel", unit_io_tuples, ids=unit_io_ids)
def multiple_read_valid_invalid_combination(target_testrig, logger, fsm_targets, unit, io_channel):
    
    """
        Requirement :WINGDECSAT-213
        Test Case 3: Modbus: Log unsuccessful master read access
    
        Setup:

        WiCE 1-X Plus Test Rig
        GTU -1 is device under test (DUT)
        Systemtest server
        Given:

        GTU-1 is up and running.
        When:

        Setup connection with GTU1 on eth-pont-2
        Send multiple read command to gtu1 with both valid and invalid input register address every 100 ms.
        Valid register address request will be send for more than 800ms after every invalid register address request.
        Read log message from gtu1.
 

        Then:

        Unknown Modbus address log shall be available
    
    """
    #Given
    fsm = fsm_targets[unit.value]
    fnd_api = fsm.get_fnd_api()
    sleep(10)
    setup_modbus_gateway(logger, fsm, io_channel)
    sleep(2)
    ip_target = fsm_targets[unit.value].get_ip_eth_point(io_channel)
    logger.info("Target ip is {}".format(ip_target))
    modbus_client = ModbusClient(host=ip_target, port=502, auto_open=True, auto_close=True)
    logger.info("modbus_client response {}".format(modbus_client))
    
    #When
    #Then
    logger.info("Shooting continuous valid and invalid request")
    for i in range(0,6):
        modbus_client.read_input_registers(36720,1)
        sleep(0.1)
        for i in range(0,4):
            modbus_client.read_input_registers(1,1)
            sleep(0.1)
    response = get_command_to_run_journal(logger,fsm_targets,current_time,2)
    assert response <=10.00
    sleep(5)

@pytest.mark.parametrize("unit, io_channel", unit_io_tuples, ids=unit_io_ids)
def test_rate_limited_register(target_testrig, logger, fsm_targets, unit, io_channel):
	
    """
        Requirement : WINGDECSAT-214
		Test Case 1: Modbus: Log unsuccessful master read access with invalid address

		Setup:

		WiCE 1-X Plus Test Rig
		GTU -1 is device under test (DUT)
		Systemtest server
		Given:

		GTU-1 is up and running.
		When:

		Setup connection with GTU1 on eth-pont-2
		Send multiple read command to gtu 1 with invalid or wrong input register address every 100ms.
		Read log message from gtu 1.
 

		Then:

		Rate limited log shall be available
	
	"""
	
	#Given
    fsm = fsm_targets[unit.value]
    fnd_api = fsm.get_fnd_api()
    sleep(10)
    setup_modbus_gateway(logger, fsm, io_channel)
    sleep(2)
    ip_target = fsm_targets[unit.value].get_ip_eth_point(io_channel)
    logger.info("Target ip is {}".format(ip_target))
    modbus_client = ModbusClient(host=ip_target, port=502, auto_open=True, auto_close=True)
    logger.info("modbus_client response {}".format(modbus_client))	
    #When
    #Then
    logger.info("Shooting continuous request on invalid input register")
    for i in range(0,6):
        modbus_client.read_input_registers(36720,1)
        sleep(0.1)
    current_time = datetime.now()
    sleep(5)
    response = get_command_to_run_journal(logger,fsm_targets,current_time,3)
    assert response <=10.00
    sleep(5)

@pytest.mark.parametrize("unit, io_channel", unit_io_tuples, ids=unit_io_ids)    
def multiple_read_valid_invalid(target_testrig, logger, fsm_targets, unit, io_channel):
    
    """
        Test Case 3: Modbus: Log unsuccessful master read access

        Setup:

        WiCE 1-X Plus Test Rig
        GTU -1 is device under test (DUT)
        Systemtest server
        Given:

        GTU-1 is up and running.
        When:
        Setup connection with GTU1 on eth-pont-2
        Send multiple read command to gtu1 with both valid and invalid input register address every 100 ms.
        Read log message from gtu1.
        Then:
        Rate limited log shall be available
    
    
    """
    #Given
    fsm = fsm_targets[unit.value]
    fnd_api = fsm.get_fnd_api()
    sleep(10)
    setup_modbus_gateway(logger, fsm, io_channel)
    sleep(2)
    ip_target = fsm_targets[unit.value].get_ip_eth_point(io_channel)
    logger.info("Target ip is {}".format(ip_target))
    modbus_client = ModbusClient(host=ip_target, port=502, auto_open=True, auto_close=True)
    logger.info("modbus_client response {}".format(modbus_client))
	
    #When
    #Then
    logger.info("Shooting continuous request on invalid input register")
    for i in range(0,6):
        modbus_client.read_input_registers(1, 1)
        sleep(.1)
        modbus_client.read_input_registers(36720,1)
        sleep(0.1)
    current_time = datetime.now()
    sleep(5)
    response = get_command_to_run_journal(logger,fsm_targets,current_time,3)
    assert response <=10.00
    sleep(5) 
        
    
    


  
    
    
    
	

	
	
	

    