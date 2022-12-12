# BigAutomotiveCompany AG (BAC) 
## CoolAutonomousFeature (CAF) demo

This is a proof of concept of the testframework for CoolAutonomousFeature 

the concept of the task was based on these Framework requirement:
- Initialize the test environment
- Create a Test Automation Framework
- Creating Test data
- Run tests thorugh a script
- Generate test reports based on the results

The requrements for this proof of concept:
- Linux Eviroment
- Python3
- Docker

#### Test Enviroment
The goal is to create a enviroment where it can recivce a signal input and it returns the result of the feature. 
The test enviroment is a docker container, where it is operates as a socket server and has the CoolAutonoumusFeatures. The reason to put it in a docker container, that the resource should be menaged in a containerised enviroment.
The server waits for a client connection, gets the signal from the recived data, and in the CAF class evaulates the signal, and returns to the client the result.
#### Test Framework
In this task, the job of the test framework is, based on the gathered test case inputs, communicates through TCP with the test enviroment and gather the test results. The test framework resources should be handled seperatly same as for the test enviroment. 
So this is also a docker container, where the "run" script operates the signal sending. It uses the socket client to send the test case inputs. After that the run script also saves the gathered results.
#### Test Data
The test datas are json files. These contains predefined signals that is same. Each test case has it's own inputs.
The test cases has their own references, which contains the expected results. These will be compared to the test result during the test case run.
#### Test Case Script Run
The test case script follows these steps:
- The user choose the feature and project to run their test case.
- After the user chooses what test to run, the script deploys the feature test enviroment container and creates the test orcestrator.
- Creates the result folder, creates the test input data based on the project, copies the references, and sends the inputs to the test framework.
- Next the test case run, the script gets and analizeses the test case results. Then, it checks if the result json values are the same as the reference.
- The next step is to it creates a test report in the result folder, where it gives a reason why the test case passed or failed.
- At the end removes the docker containers.

#### Run the script

To run the test case script use it in the BAC_repo folder as:

```sh
python3




