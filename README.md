# BigAutomotiveCompany AG (BAC) 
## CoolAutonomousFeature (CAF) demo

the concept of the task was based on these Framework requirement:
- Initialize the test environment
- Create a a test orcestrator
- Creating Test data
- Run tests thorugh a script
- Generate test reports based on the results

#### Test enviroment
The goal was to create a enviroment where it can recivce a signal input and it returns the evaulated result.
The test enviroment is a docker container, where it is operates as a socket server and has the CoolAutonoumusFeatures.
The server waits for a client connection, gets the signal from the recived data, and in the CAF class evaulates the signal, and returns to the client the result.
#### Test orcestrator
In this task, the job of the test orcestrator is based on the gathered test case inputs communicates with the test enviroment and gather the test results result.
This is also a docker container, where the "run" script operates the test run, and using the socket client to send the test case inputs. After that saves the results.
#### Test data
The test datas are json files. These contains the specification of the signal. Each test case has it's own inputs.
The test cases has their own references, which contains the expected results. These will be compared to the test result during the test case run.
#### Test Case script run
The test case script follows these steps:
- The user choose the feature and project to run their test case.
- After the user chooses what test to run, the script deploys the feature test enviroment container and creates the test orcestrator.
- Creates the result folder, creates the test input data based on the project, copies the references, and sends the inputs to the test orcestrator.
- After the test case run, the script gets and analizeses the test case results. After it checks if the result json values are the same between the reference.
- After the evaulation, it creates a test report, where gives a reason why the test case passed or failed.