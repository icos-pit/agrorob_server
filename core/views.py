from django.shortcuts import render
from django.http import JsonResponse
import random
import zenoh
from zenoh import config, Reliability
from pycdr import cdr
from pycdr.types import int8, int16, float32, int32, uint32, float64, int64
import time
import math 
import os

lat = 51.9294
lng = 19.1151
yaw = 0
gnss_status_ = -100
outside_temp_ = -100
robot_speed_ms_ = -100
engine_rotation_speed_rpm_ = -100
engine_running_ = -100
engine_coolant_temp_celsius_ = -100
engine_fuel_level_percent_ = -100
engine_oil_pressure_bar_ = -100


@cdr
class Vector3:
    x: float64
    y: float64
    z: float64


@cdr
class Twist:
    linear: Vector3
    angular: Vector3

# Declare the types of Log message to be decoded and subscribed to via zenoh


@cdr
class Time:
    sec: int32
    nanosec: uint32


@cdr
class Log:
    stamp: Time
    level: int8
    name: str
    msg: str
    file: str
    function: str
    line: uint32


@cdr
class GPS_Log:
    stamp: Time
    frame_id: str
    # status
    status: int8
    # service
    service: int16

    latitude: float64
    longtitude: float64
    altitude: float64
    # position_cov: float64[9]
    # pos_cov_type: int8

@cdr
class TEMP_Log:
    stamp: Time
    frame_id: str
    temperature: float64

@cdr
class LOG_Log:
    velocity_ms: float64

@cdr
class ENGINE_Log:
    engine_rotation_speed_rpm: int64	
    engine_running: bool               	
    engine_coolant_temp_celsius: int32
    engine_fuel_level_percent: int32
    engine_oil_pressure_bar: int32

@cdr
class MAG_Log:
    stamp: Time
    frame_id: str
    mag: Vector3



# Initiate the zenoh-net API
# session = zenoh.open({"mode":"client","connect":{"endpoints": ["tcp/150.254.225.124:8447"]}})
session = zenoh.open({"mode":"client","connect":{"endpoints": [os.environ["ZENOH_URL"]]}})
# session = zenoh.open({})



def fix_callback(sample):
    global lat, lng
    log = GPS_Log.deserialize(sample.payload)
    # print('[{}.{}] [{}]: {}'.format(
    # log.stamp.sec, log.stamp.nanosec, log.name, log.msg))
    print(
        f"Received {sample.kind} ('{sample.key_expr}':)")
    print(type(sample.payload))
    # print(sample.payload)
    print('[{}.{}]'.format(
        log.stamp.sec, log.stamp.nanosec))
    print('status:{}, service: {}, frame_id:{}'.format(
        log.status, log.service, log.frame_id))
    print('{},{},{}'.format(log.latitude,
          log.longtitude, log.altitude))
    lat = log.latitude
    lng = log.longtitude

def fix_moving_callback(sample):
    global gnss_status_
    log = GPS_Log.deserialize(sample.payload)
    print(
        f"Received {sample.kind} ('{sample.key_expr}':)")
    print(type(sample.payload))
    # print(sample.payload)
    print('moving base status:{}, service: {}, frame_id:{}'.format(
        log.status, log.service, log.frame_id))
    print("this is maving base")
    gnss_status_ = log.status
    
    
def temp_callback(sample):
    log = TEMP_Log.deserialize(sample.payload)
    global outside_temp_
    print('outside_temp:{}'.format(log.temperature))
    outside_temp_ = log.temperature

def logs_callback(sample):
    log = LOG_Log.deserialize(sample.payload)
    global robot_speed_ms_
    print('robot_speed_ms:{}'.format(log.velocity_ms))
    robot_speed_ms_ = log.velocity_ms

def engine_callback(sample):
    log = ENGINE_Log.deserialize(sample.payload)
    global engine_rotation_speed_rpm_, engine_running_, engine_coolant_temp_celsius_
    global engine_fuel_level_percent_, engine_oil_pressure_bar_ 
    print('engine_rotation:{}, engine_running: {}, coolant_temp:{}, fuel_level_percent:{} ,engine_oil_pressure_bar:{}'.format(
        log.engine_rotation_speed_rpm, log.engine_running, log.engine_coolant_temp_celsius, log.engine_fuel_level_percent, log.engine_oil_pressure_bar))
    engine_rotation_speed_rpm_ = log.engine_rotation_speed_rpm
    engine_running_ = log.engine_running
    engine_coolant_temp_celsius_ = log.engine_coolant_temp_celsius
    engine_fuel_level_percent_ = log.engine_fuel_level_percent
    engine_oil_pressure_bar_ = log.engine_oil_pressure_bar

  

def mag_callback(sample):
    global yaw
    log = MAG_Log.deserialize(sample.payload)
    print('z_rotation:{}'.format(log.mag.z))
    yaw = abs(math.degrees(log.mag.z))


def rosout_callback(sample):
    log = Log.deserialize(sample.payload)
    print('[{}.{}] [{}]: {}'.format(log.stamp.sec,
                                    log.stamp.nanosec, log.name, log.msg))


# sub = session.declare_subscriber('/rt/rosout', rosout_callback)
# sub = session.declare_subscriber('rt/ublox_gps_node/fix', fix_callback)
sub_fix = session.declare_subscriber('rt/ublox_rover/fix', fix_callback) #
sub_moving_fix = session.declare_subscriber('rt/ublox_moving_base/fix', fix_moving_callback) #
sub_temp = session.declare_subscriber('rt/temperature', temp_callback) #
sub_logs = session.declare_subscriber('rt/agrorob/logs', logs_callback) #
sub_engine = session.declare_subscriber('rt/agrorob/engine_state', engine_callback) #
sub_imu_mag = session.declare_subscriber('rt/imu/mag', mag_callback)


# Create your views here.
def index(request):
    context = { }
    return render(request, "index.html", context)

def getgpsfix(request):
    global lat,lng,yaw
    # lat = lat + 0.0001 * random.uniform(-1, 1)
    # lng = lng + 0.0001 * random.uniform(-1, 1)
    response = JsonResponse({'lat': lat-0.000060, 'lng': lng-0.000060, 'yaw': yaw})
    return response

def getrobotstatus(request):
    global gnss_status_ 
    global outside_temp_ 
    global robot_speed_ms_ 
    global engine_rotation_speed_rpm_
    global engine_running_ 
    global engine_coolant_temp_celsius_
    global engine_fuel_level_percent_
    global engine_oil_pressure_bar_
    
    # lat = lat + 0.0001 * random.uniform(-1, 1)
    # lng = lng + 0.0001 * random.uniform(-1, 1)
    response = JsonResponse({'gnss_status_ ': gnss_status_,
                              'outside_temp_ ': outside_temp_,
                              'robot_speed_ms_ ': robot_speed_ms_,
                              'engine_rotation_speed_rpm_': engine_rotation_speed_rpm_,
                              'engine_running_ ': engine_running_,
                              'engine_coolant_temp_celsius_': engine_coolant_temp_celsius_,
                              'engine_fuel_level_percent_': engine_fuel_level_percent_,
                              'engine_oil_pressure_bar_': engine_oil_pressure_bar_
                             })
    return response