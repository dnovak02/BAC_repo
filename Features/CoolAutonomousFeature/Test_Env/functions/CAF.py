#!/bin/bash/python3
import os
import json

class CAF:
    
    Actual_Vehicle_Speed = 0
    Sensor_Input_Ok = False
    Vehicle_State = 0
    CAF_Is_Active = False
    CAF_Is_Off_Alert = 0
    CAF_Vehicle_Speed_Limit = 0
    CAF_TimeOut = 0
    
    Over_CAF_Vehicle_Speed_Limit = False
    Prev_Over_CAF_Vechicle_Speed_Limit = False
    Speed_Limit_Timestamp = 0
    Current_Timestamp = 0
    
    def __init__(self):
        pass
    
    def get_Config_Data(self,config_name):
        directory = './Projects'
        config = []
        for filename in os.scandir(directory):
            if(config_name in filename.path):
                config_file = open(filename.path+"/data.json")
                config = json.load(config_file)
        return config
    
    def wrap_up_json(self):
        CAF_Result_Dict = {}
        CAF_Result_Dict["CAF_Is_Active"] = self.CAF_Is_Active
        CAF_Result_Dict["CAF_Is_Off_Alert"] = self.CAF_Is_Off_Alert
        return json.dumps(CAF_Result_Dict)
    
    def config_Setup(self,config_name):
        config=self.get_Config_Data(config_name)
        self.CAF_Vehicle_Speed_Limit = int(config["CAF_Vehicle_Speed_Limit"])
        self.CAF_TimeOut = int(config["CAF_TimeOut"])
        
    def signal_Parsing(self,signal_string):
        signal=json.loads(signal_string)
        
        self.config_Setup(signal["Project"])
        
        self.Actual_Vehicle_Speed=int(signal["Actual_Vehicle_Speed"])
        self.Sensor_Input_Ok=bool(signal["Sensor_Input_Ok"])
        self.Vehicle_State=int(signal["Vehicle_State"])
        self.Current_Timestamp=signal["Timestamp"]
        
    def check_Speed_Limit(self):
        if(self.CAF_Vehicle_Speed_Limit>=self.Actual_Vehicle_Speed*3.6):
            self.Over_CAF_Vehicle_Speed_Limit = False
        else: self.Over_CAF_Vehicle_Speed_Limit = True
        
    def check_Limit_Time(self):
        if(not self.Over_CAF_Vehicle_Speed_Limit):
            self.Speed_Limit_Timestamp = 0
        if(not self.Prev_Over_CAF_Vechicle_Speed_Limit and self.Over_CAF_Vehicle_Speed_Limit):
            self.Speed_Limit_Timestamp = self.Current_Timestamp
            self.Prev_Over_CAF_Vechicle_Speed_Limit = True
            return False
        if(self.Prev_Over_CAF_Vechicle_Speed_Limit and self.Over_CAF_Vehicle_Speed_Limit):
            if(self.Current_Timestamp-self.Speed_Limit_Timestamp>self.CAF_TimeOut):
                return True
        return False
                
    def check_Sensor_Input_OK(self):
        if not self.Sensor_Input_Ok:
            return True
        return False
    
    def check_Vehicle_State(self):
        if(not self.Vehicle_State==1):
            return True
        return False
    
    def set_Fault_Event(self):
        self.CAF_Is_Active = False
        self.CAF_Is_Off_Alert = 2
    
    def check_Fault_Event(self):
        if(self.check_Limit_Time() or self.check_Sensor_Input_OK() or self.check_Vehicle_State()):
            self.set_Fault_Event()

    def check_CAF_Active(self):
        if(not self.Over_CAF_Vehicle_Speed_Limit and self.Sensor_Input_Ok and self.Vehicle_State==1):
            self.CAF_Is_Active = True
            
    def evaulate(self):
        self.check_Speed_Limit()
        self.check_CAF_Active()
        self.check_Fault_Event()
        return self.wrap_up_json()