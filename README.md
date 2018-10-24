# python-kafka
Repo for python and kafka 

### OS - Windows 10 Enterprise

# Setup Docker for windows

Download docker for windows

Download winutils for windows and save it in %UserProfile%\venv\hadoop\bin and add its location to PATH from 
https://github.com/steveloughran/winutils/blob/master/hadoop-2.7.1/bin/winutils.exe

# Setup Kafka
docker run -d --net=confluent --name=zookeeper -e ZOOKEEPER_CLIENT_PORT=2182 -p 2182:2182 confluentinc/cp-zookeeper:5.0.0

docker run -d --net=confluent --name=kafka -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2182 -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:29092 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 -p 29092:29092 confluentinc/cp-kafka:5.0.0

docker run --net=confluent --rm confluentinc/cp-kafka:5.0.0 kafka-topics --create --topic browser-topic --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2182

docker run --net=confluent --rm confluentinc/cp-kafka:5.0.0 kafka-topics --create --topic vehicle-topic --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2182

docker run --net=confluent --rm confluentinc/cp-kafka:5.0.0 kafka-topics --list --zookeeper zookeeper:2182

docker run --net=confluent --rm confluentinc/cp-kafka:5.0.0 kafka-topics --describe --topic browser-topic --zookeeper zookeeper:2182

## To view the topic content
docker run --net=confluent --rm confluentinc/cp-kafka:5.0.0 kafka-console-consumer --bootstrap-server kafka:9092 --topic browser-topic  --from-beginning

# Setup Anaconda

## Install miniconda - it will create virtual env "%UserProfile%\venv" - install further packages in this virtual env
cd %UserProfile%

powershell -command "& { (New-Object Net.WebClient).DownloadFile('https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe', 'mc3.exe') }"

start /wait "" mc3.exe /InstallationType=JustMe /AddToPath=0 /RegisterPython=0 /NoRegistry=0 /S /D=%UserProfile%\anaconda3

### Activate virtual env
%UserProfile%\anaconda3\Scripts\activate.bat

conda install -y anaconda=5.0.1 conda-build _ipyw_jlab_nb_ext_conf

## Add to PATH
set PATH=C:\ProgramData\Oracle\Java\javapath;c:\oracle\ora12c\bin;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\Program Files (x86)\Enterprise Vault\EVClient\;C:\Program Files (x86)\WebEx\Productivity Tools;C:\Users\singhgo\AppData\Local\Microsoft\WindowsApps;C:\Users\singhgo\anaconda3\;C:\Users\singhgo\anaconda3\Scripts
