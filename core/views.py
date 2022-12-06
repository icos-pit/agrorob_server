from django.shortcuts import render
from django.http import JsonResponse
import random
import zenoh
from zenoh import config, Reliability
from pycdr import cdr
from pycdr.types import int8, int16, float32, int32, uint32, float64
import time

lat = 51.9294
lng = 19.1151
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


# Initiate the zenoh-net API
session = zenoh.open({})
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


def rosout_callback(sample):
    log = Log.deserialize(sample.payload)
    print('[{}.{}] [{}]: {}'.format(log.stamp.sec,
                                    log.stamp.nanosec, log.name, log.msg))


# sub = session.declare_subscriber('/rt/rosout', rosout_callback)
sub = session.declare_subscriber('rt/ublox_gps_node/fix', fix_callback)
# Create your views here.
def index(request):
    context = { }
    return render(request, "index.html", context)

def getgpsfix(request):
    global lat,lng
    # lat = lat + 0.0001 * random.uniform(-1, 1)
    # lng = lng + 0.0001 * random.uniform(-1, 1)
    response = JsonResponse({'lat': lat, 'lng': lng})
    return response