#!/bin/bash/python3
import os
import json

class CAF:
    
    actual_vehicle_speed = 0
    sensor_input_ok = False
    vehicle_state = 0
    caf_is_active = False
    caf_is_off_alert = 0
    
    caf_vehicle_speed_limit = 0
    caf_time_out = 0
    
    over_caf_speed_limit = False
    prev_over_caf_speed_limit = False
    speed_limit_timestamp = 0
    current_timestamp = 0
    
    
    
    def __init__(self):
        pass
    
    def get_config_data(self,config_name):
        directory = './Projects'
        config = []
        for filename in os.scandir(directory):
            if(config_name in filename.path):
                config_file = open(filename.path+"/data.json")
                config = json.load(config_file)
        return config
    
    def wrap_up_json(self):
        caf_result_dict = {}
        caf_result_dict["CAF_Is_Active"] = self.caf_is_active
        caf_result_dict["CAF_Is_Off_Alert"] = self.caf_is_off_alert
        return json.dumps(caf_result_dict)
    
    def config_setup(self,config_name):
        config=self.get_config_data(config_name)
        self.caf_vehicle_speed_limit = int(config["CAF_Vehicle_Speed_Limit"])
        self.caf_time_out = int(config["CAF_TimeOut"])
        
    def signal_parsing(self,signal_string):
        signal=json.loads(signal_string)
        
        self.config_setup(signal["Project"])
        
        self.actual_vehicle_speed=int(signal["Actual_Vehicle_Speed"])
        self.sensor_input_ok=bool(signal["Sensor_Input_Ok"])
        self.vehicle_state=int(signal["Vehicle_State"])
        self.current_timestamp=signal["Timestamp"]
        
    def check_speed_limit(self):
        if(self.caf_vehicle_speed_limit>=self.actual_vehicle_speed*3.6):
            self.over_caf_speed_limit = False
        else:
            self.over_caf_speed_limit = True
        
    def check_limit_time(self):
        if(not self.over_caf_speed_limit):
            self.Speed_Limit_Timestamp = 0
            self.prev_over_caf_speed_limit = False
        if(not self.prev_over_caf_speed_limit and self.over_caf_speed_limit):
            self.Speed_Limit_Timestamp = self.current_timestamp
            self.prev_over_caf_speed_limit = True
            return False
        if(self.prev_over_caf_speed_limit and self.over_caf_speed_limit):
            if(self.current_timestamp-self.speed_limit_timestamp>self.caf_time_out):
                return True
        return False
                
    def check_sensor_input_ok(self):
        if self.sensor_input_ok:
            return True
        return False
    
    def check_vehicle_state(self):
        if(self.vehicle_state==1):
            return True
        return False
    
    def set_fault_event(self):
        self.caf_is_active = False
        self.caf_is_off_alert = 2
    
    def check_fault_event(self):
        if(self.check_limit_time() or not self.check_sensor_input_ok() or not self.check_vehicle_state()):
            self.set_fault_event()

    def check_caf_active(self):
        if(not self.over_caf_speed_limit and self.check_sensor_input_ok() and self.check_vehicle_state()):
            self.caf_is_active = True
            
    def evaulate(self):
        self.check_speed_limit()
        self.check_caf_active()
        self.check_fault_event()
        return self.wrap_up_json()