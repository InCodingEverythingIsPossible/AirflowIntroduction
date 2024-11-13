# Airflow Introduction


## Docker setup
1. Enable virtualization on processor in bios
2. Enable Windows system features
   - Virtual Machine Platform
   - Windows Subsystem for Linux
3. Enter powershell to set default version of wsl
   - Command `wsl --set-default-version 2`
4. Install ubuntu
   - Enter microsoft store
   - Download ubuntu for example Ubuntu 22.04.05 LTS
   - After installation launch Ubuntu
   - Create first user and check if it's works
5. Install docker
   - Install docker from official website of docker
   - During installation checkmark "Install required Windows components for WSL 2"
   - Change assigned resources in C:\Users\{Your_account}\.wslconfig
   - Microsoft tutorial [wsl_config_tutorial](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#configure-global-options-with-wslconfig)

## Airflow setup
1. You need configured docker on your computer
2. Download yaml file -> [Sample yaml file](https://airflow.apache.org/docs/apache-airflow/2.10.2/docker-compose.yaml)
3. Put yaml file in your project folder
4. Create .env file with parameters in your project folder
   - `AIRFLOW_IMAGE_NAME=apache/airflow:2.10.2`
   - `AIRFLOW_UID=50000`
5. Run database migration and create first user
   - `docker compose up airflow-init`

<br>
<br>

## Run and stop container section


### Build docker container in interactive mode

Build container `docker compose up`  
Stop interactive mode  `CTRL + C`


### Build docker container in separate mode

Build container `docker compose up -d`  
Stop separate mode `docker compose stop`  
Stop and delete container `docker compose down`

### Indicates which docker configuration file to run

Sample `docker compose -f docker-compose-elastic-search.yaml up -d`  
Command `docker compose -f {yaml_name} up -d`

### Indicates which docker configuration file to stop

Sample `docker compose -f docker-compose-elastic-search.yaml stop`  
Command `docker compose -f {yaml_name} stop`

### Checks if containers are healthy

Command `docker ps`

### Download airflow providers

Sample `pip install apache-airflow-providers-postgres`  
Command `pip install {provider}`  
Provider && Modules [list on website](https://registry.astronomer.io/)


## Operation on container instances

### Run small virtual machine on container

Sample `docker exec -it airflowintroduction-airflow-scheduler-1 /bin/bash`  
Command `docker exec -it {scheduler_instantion} /bin/bash`

### Test airflow task 
Run command on small vm in airflow_scheduler instance

Sample `airflow tasks test user_processing create_table 2022-01-01`  
Command `airflow tasks test {dag_id} {task_id} {date_in_past_for_test}`

### Write sql command in postgres container
Run command on small vm in postgres instance

1. Command `psql -Uairflow`
2. Write your sql code

### Test if elastic search is working
Run command on small vm in airflow_scheduler instance

Command `curl -X GET 'http://elastic:9200'`

### Check plugins which were created
Run command on small vm in airflow_scheduler instance

Command `airflow plugins`


## Add airflow flower instance to the container
Airflow flower monitor and administrate Celery Clusters

Command `docker compose --profile flower up -d`

## Yaml file hints

### Copy airflow configuration file to your directory
Variables in yaml overwrites variables in airflow.cfg file

Sample airflow.cfg `executor = SequentialExecutor`  
Sample yaml file `AIRFLOW__CORE__EXECUTOR: CeleryExecutor`


Sample `docker cp airflowintroduction-airflow-scheduler-1:/opt/airflow/airflow.cfg .`  
Command `docker cp {airflow_scheduler_instance}:/opt/airflow/airflow.cfg .`

### Delete example DAGs from GUI
Enter yaml file which you use

Change parameter `AIRFLOW__CORE__LOAD_EXAMPLES: 'false'`

### Assign worker to specific queue

Sample :  
&nbsp;&nbsp;&nbsp; airflow-worker-2:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    <<: *airflow-common  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    command: celery worker -q high_cpu

### Send task to specific queue

    transform = BashOperator(
        task_id='transform',
        queue='high_cpu',
        bash_command='sleep 30'
    )


## Powershell useful commands

### Run wsl service

Command `wsl`

### Shutdown wsl service

Command `wsl --shutdown`

### Check running ubuntu instance

Command `wsl --list --running --verbose`

### Check all ubuntu instance

Command `wsl --list --running --verbose`