"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir


def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestants."""
    # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py

    load_one = True
    load_two = True
    load_three = True
    power_reference = 0.0
    pv_mode = PVMode.ON


    
    if msg.grid_status:
        if msg.bessSOC != 1:
            if msg.bessSOC <=0.7 and msg.solar_production > 0:
                if msg.solar_production < msg.current_load:
                    power_reference = msg.current_load - msg.solar_production - 3
            else:
                 if msg.solar_production == 0:
                    if  msg.bessSOC<0.50:
                        power_reference = msg.current_load - 5
                    else:
                        power_reference = msg.current_load
                 else:
                     power_reference = msg.current_load - msg.solar_production
    else:
        load_three = False
        if msg.bessSOC <= 0.30:
            load_two = False
            
        if msg.bessSOC != 1:
            if msg.bessSOC >= 0.90 and msg.solar_production > 0:
                if msg.solar_production < msg.current_load:
                    power_reference = msg.current_load - msg.solar_production
            else:
                 if msg.solar_production == 0:
                    power_reference = msg.current_load
                 else:
                     power_reference = msg.current_load - msg.solar_production
        
             
                    
                
                
                

    # Dummy result is returned in every cycle here
    return ResultsMessage(data_msg=msg,
                          load_one=load_one,
                          load_two=load_two,
                          load_three=load_three,
                          power_reference=power_reference,
                          pv_mode=pv_mode)


def run(args) -> None:
    prepare_dot_dir()
    config_outs(args, 'solution')

    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
