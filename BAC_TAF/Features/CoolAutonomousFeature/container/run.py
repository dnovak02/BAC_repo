#! /usr/bin/python3

import os
import TAF_client
import json

def save_result(json_signal,tc_name,filepath):
    filename = filepath+"/"+tc_name+"_result.json"
    openedfile = open(filename,"w+")
    openedfile.write(json_signal)
    openedfile.close()

def call_client(signal,file,filepath):
    result = TAF_client.client_program(signal)
    name = file.split(".")
    save_result(result,name[0],filepath)

filepath = "Test_Case_Result"
os.system("mkdir "+filepath+" > /dev/null")
for root,dir,filename in os.walk("./Test_Cases"):
    for file in filename:
        f = open(root+"/"+file)
        json_signal = json.load(f)
        call_client(json_signal,file,filepath)