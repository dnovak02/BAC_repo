#! /usr/bin/python3
import os
from datetime import datetime
import json

def choose_folder(dir_name):
    for directory in os.walk(dir_name):
        name_list = directory[1]
        break
    return name_list

def print_input(name_list):
    i = 1
    for name in name_list:
        print(str(i)+".   "+name)
        i += 1
        
def get_item_chosen(dir_name,itemtype):
    name_list = choose_folder(dir_name)
    print("Chooseable "+itemtype+":")
    print_input(name_list)
    chosen = input("Choose your "+itemtype+" by number: \n")
    try:
        return name_list[int(chosen)-1]
    except:
        print("Wrong input")
        
def print_test_case_description(BAC_filepath,result_filepath):
    openedfile = open(BAC_filepath+"/Test_Case_list.txt")
    print("Test case description: \n")
    for line in openedfile:
        print(line)
    os.system("cp "+BAC_filepath+"/Test_Case_list.txt "+result_filepath)
        
def create_inputs_with_Projects(Project,filepath,BAC_TAF_filepath):
    for root,dir,filename in os.walk(BAC_TAF_filepath+"/Test_Case_Inputs/"):
        for file in filename:
            openedfile = open(root+"/"+file)
            json_test_case_input = json.load(openedfile)
            if(type(json_test_case_input) == list):
                for input in json_test_case_input:
                    input["Project"] = Project
            else:json_test_case_input["Project"] = Project
            openedfile.close()
            os.system("mkdir -p "+filepath+"/Test_Case_Inputs/")
            openedfile = open(filepath+"/Test_Case_Inputs/"+file,"w+")
            json.dump(json_test_case_input,openedfile)
            openedfile.close()        

def get_references(filepath,BAC_TAF_filepath):
    os.system("mkdir -p "+filepath+"/Test_Case_Reference")
    os.system("cp -r "+BAC_TAF_filepath+"/Test_Case_Reference "+filepath)

def copy_Json_To_Docker(filepath):
    os.system("docker cp "+filepath+"/Test_Case_Inputs bac_taf:/TAF/Test_Cases")
    
def prepare_test_case_run(Project,filepath,BAC_TAF_filepath):
    create_inputs_with_Projects(Project,filepath,BAC_TAF_filepath)
    get_references(filepath,BAC_TAF_filepath)
    copy_Json_To_Docker(filepath)
    
def start_containers(Feature):
    os.system("docker build -t test_env ./Features/"+Feature+"/")
    os.system("docker run -td --network=host --name=test_env docker.io/test_env:latest")
    os.system("docker exec test_env ./setup.py")
    os.system("docker build -t bac_taf ./BAC_TAF/Features/"+Feature+"/container")
    os.system("docker run -td --network=host --name=bac_taf docker.io/bac_taf:latest")

def run():
    os.system("docker exec bac_taf ./run.py")

def get_result(filepath):
    os.system("docker cp bac_taf:/TAF/Test_Case_Result "+filepath+"/Test_Case_Result")
    os.system("docker exec bac_taf rm -rf /TAF/Test_Case_Result")

def create_report(filepath):
    os.system("touch "+filepath+"/test_report.txt")

def get_Json_List(filepath,foldername):
    for root,dir,filename in os.walk(filepath+foldername):
        filename.sort()
        return filename
    
def load_Json_file(filepath,foldername,jsonname):
    json_file_Open = open(filepath+foldername+jsonname)
    json_loaded = json.load(json_file_Open)
    return json_loaded

def check_result_success(json_result,json_reference):
    result_passed = 0
    for result in json_result:
        if json_result[result] == json_reference[result]:
            result_passed +=1
    if(result_passed == len(json_result)):
        return True
    else: return False
    
def write_to_test_case_report(filepath,what_to_write):
    openedfile = open(filepath+"/test_report.txt","a")
    openedfile.write(what_to_write)
    openedfile.close()
    
def Test_result_evaulation(filepath):
    create_report(filepath)
    tc_result_list = get_Json_List(filepath,"/Test_Case_Result/")
    tc_ref_list = get_Json_List(filepath,"/Test_Case_Reference/")
    successful_tcs = 0
    max_tcs = len(tc_result_list)
    for i in range(max_tcs):
        json_result = load_Json_file(filepath,"/Test_Case_Result/",tc_result_list[i])
        json_reference = load_Json_file(filepath,"/Test_Case_Reference/",tc_ref_list[i])
        if(check_result_success(json_result,json_reference)):
            print("Test case "+str(i+1)+"\033[92m"+" passed!"+"\033[0m")
            successful_tcs += 1
            write_to_test_case_report(filepath,str(i+1)+". result and the reference MATHCHED\n")
        else:
            print("Test case "+str(i+1)+"\033[93m"+" failed!"+"\033[0m")
            write_to_test_case_report(filepath,str(i+1)+". result and the reference NOT MATHCHED\n")
    if(successful_tcs == max_tcs):
        print("All test cases were"+"\033[92m"+" successful!"+"\033[0m")
        os.system("mv "+filepath+" "+filepath+"_P")
    else:
        print("Test case senario were"+"\033[93m"+" unsuccesful!"+"\033[0m"+" check the test_report.")
        os.system("mv "+filepath+" "+filepath+"_F")
        
now = datetime.now()
dt_String = now.strftime("%d%m%Y%H%M%S")
Feature = get_item_chosen("./Features","Feature")
Project = get_item_chosen("./Features/"+Feature+"/Test_Env/Projects/","Project")
Test_Results_filepath = "Results/"+Feature+"/"+Project+"/"+dt_String
BAC_TAF_filepath = "BAC_TAF/Features/"+Feature
os.system("mkdir -p "+Test_Results_filepath)
print_test_case_description(BAC_TAF_filepath,Test_Results_filepath)
start_containers(Feature)
prepare_test_case_run(Project,Test_Results_filepath,BAC_TAF_filepath)
run()
get_result(Test_Results_filepath)
Test_result_evaulation(Test_Results_filepath)