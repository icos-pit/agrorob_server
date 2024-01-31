## Description
![Screenshot from 2023-11-01 17:53:53](system.png)
## Docker image
To containerize and run the application using Docker, refer to:

https://github.com/icos-pit/agrorob_containers/

## Branches description
### master 
Zenoh config from environment variable and client mode 
```
session = zenoh.open({"mode":"client","connect":{"endpoints": [os.environ["ZENOH_URL"]]}})
```
### dev 
Zenoh local config and peer mode

```
session = zenoh.open({})
```
## Installation

```
$ pip install pycdr==0.1.5

$ pip install eclipse-zenoh

$ python -m pip install Django
```
Install [zenoh-bridge-dds][def]

## Running the application
Open a new terminal
```
$ source /opt/ros/<ros_distro>
$ ros2 bag play <bag file> --loop
```
Open a new terminal
```
$ zenoh-bridge-dds -m peer
```
```
$ zenoh-bridge-dds -m client -e tcp/ip:port
```
Open a new terminal
```
$ cd agrorob_server
$ python manage.py runserver 
```
## Expected result
![Screenshot from 2023-11-01 17:53:53](map.png)

[def]: https://github.com/eclipse-zenoh/zenoh-plugin-dds?tab=readme-ov-file#linux-debian