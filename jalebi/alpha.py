from __future__ import with_statement
import cherrypy
import os
import serial
import sys
import wx
import threading
import time
import math
import cgi
import tempfile
import uuid
import random

MEDIA_DIR = os.path.join(os.path.abspath("."), u"media")

print 
# utility functions
def dist(x1, y1, z1, x2, y2, z2):
    return math.sqrt(
        pow(x1-x2, 2.0) +
        pow(y1-y2, 2.0) + 
        pow(z1-z2, 2.0)
    )

def noBodyProcess():
    cherrypy.request.process_request_body = False

cherrypy.tools.noBodyProcess = cherrypy.Tool('before_request_body', noBodyProcess)

class RMLSender:
    def __init__(self, port="/dev/ttyUSB0"):
        self.serial = serial.Serial(port, baudrate=9600, rtscts=True, timeout=0)
        self.cmds = []
        self.xr=[0,1]; self.yr=[0,1]; self.zr=[0,1]
        self.paths = []
        self.segments_done = []
        self.traverses = []
        self.traverses_done = []
        self.speed_feed = 15.0
        self.speed_plunge = 5.0
        self.total_distance = 1.0
        self.distance_milled = 0.0
        self.total_time = 1.0
        self.time_remaining = 1.0
        self.time_start = None
        self.current_cmd = ""
        self.cur_cmd_start = time.time()
        self.cur_cmd_duration = 0.0
        self.running = False
        self.thread = threading.Thread(target=self.thread_fn)
        self.should_stop = threading.Event()
        self.done = threading.Event()
        self.aborted = threading.Event()
        self.lock = threading.Lock()

    def load_file(self, filename):
        self.cmds = []
        f = open(filename, "r")
        data = f.read()
        f.close()
        self.cmds = data.split(";")
        self.calculate_metrics()

    def calculate_metrics(self):
        paths = []
        traverses = []
        cur_path = []
        xmin, ymin, zmin = 99999999, 999999999, 999999999
        xmax, ymax, zmax = 0, 0, 0
        xpos, ypos, zpos = 0, 0, 0
        zup, zdown = 0, 0
        speeds, speedz = 0.0, 0.0
        total_distance = 0.0
        total_time = 0.0
        in_path = False
        for cmd in self.cmds:
            cmd=cmd.strip()
            try:
                if cmd[:3] == "!PZ":
                    params = cmd[3:].split(',')
                    if len(params) < 2:
                        params = cmd[3:].split(' ')
                    zup = int(params[1])
                    zdown = int(params[0])
                    print "pen: %d up, %d down" % (zup, zdown)
                elif cmd[:2] == "VS":
                    params = cmd[2:].split(',')
                    if len(params) < 2:
                        params = cmd[2:].split(' ')
                    speeds = float(params[0])
                    print "xy speed: %f mm/s" % (speeds)
                elif cmd[:3] == "!VZ":
                    params = cmd[3:].split(',')
                    if len(params) < 2:
                        params = cmd[3:].split(' ')
                    speedz = float(params[0])
                    print "z speed: %f mm/s" % (speedz)
                elif cmd[:2] == "PU":
                    params = cmd[2:].split(',')
                    if len(params) < 2:
                        params = cmd[2:].split(' ')
                    if len(params) < 2:
                        continue
                    x = int(params[0])
                    y = int(params[1])
                    z = zup
                    d = dist(xpos, ypos, zpos, x, y, z)
                    total_distance += d
                    total_time += d / RML_UNITS / SPEED_TRAVERSE
                    traverses.append([(xpos, ypos, zpos), (x, y, z)])
                    xpos = x; ypos = y; zpos = z;
                    xmax = max(x, xmax); ymax = max(y, ymax); zmax = max(z, zmax)
                    xmin = min(x, xmin); ymin = min(y, ymin); zmin = min(z, zmin)
                    if len(cur_path) > 0:
                        paths.append(cur_path)
                        cur_path = []
                elif cmd[:1] == "Z":
                    params = cmd[1:].split(',')
                    if len(params) < 2:
                        params = cmd[1:].split(' ')
                    x = int(params[0])
                    y = int(params[1])
                    z = int(params[2])
                    dist_xy = math.hypot(xpos-x, ypos-y) / RML_UNITS
                    dist_z = float(zpos-z) / RML_UNITS
                    time_xy = dist_xy / speeds
                    time_z = dist_z / speedz
                    total_time += max(time_xy, time_z)
                    total_distance += dist(xpos, ypos, zpos, x, y, z)

                    xpos = x; ypos = y; zpos = z;
                    xmax = max(x, xmax); ymax = max(y, ymax); zmax = max(z, zmax)
                    xmin = min(x, xmin); ymin = min(y, ymin); zmin = min(z, zmin)
                    cur_path.append((x, y, z))
            except:
                print "ignoring: %s" % cmd
                pass
        self.paths = paths
        self.traverses = traverses
        self.speed_feed = speeds
        self.speed_plunge = speedz
        self.xr = (xmin, xmax)
        self.yr = (ymin, ymax)
        self.zr = (zmin, zmax)
        self.total_distance = total_distance
        if self.total_distance == 0: self.total_distance = 1.0
        self.total_time = total_time
        if self.total_time == 0: self.total_time = 1.0
        self.time_remaining = total_time

    def start(self):
        self.running = True
        self.time_start = time.time()
        self.thread.start()

    def abort(self):
	print self.running
	print not self.done.isSet()
        if self.running and not self.done.isSet():
            self.aborted.set()
            print "aborted"
        else:
            print "something went wrong"

    def thread_fn(self):
        xmax, ymax, zmax = 0, 0, 0
        xpos, ypos, zpos = 0, 0, 0
        zup, zdown = 0, 0
        speeds, speedz = 0.0, 0.0
        with self.lock:
            cmds = self.cmds
        for cmd in cmds:
            cmd = cmd.strip()
            if self.should_stop.isSet():
                cmd="PA;PA;!VZ10;!PZ0,100;PU0,0;PD0,0;!MC0;"
                self.serial.write(cmd)
                self.serial.close()
                self.aborted.set()
                return
            cmd=cmd.strip()
            with self.lock:
                self.current_cmd = cmd
                self.cur_cmd_start = time.time()
                self.cur_cmd_duration = 0.0
            while (self.serial.getDSR() != True):
               time.sleep(0.001)
            self.serial.write(cmd)
            try:
                if cmd[:3] == "!PZ":
                    params = cmd[3:].split(',')
                    if len(params) < 2:
                        params = cmd[3:].split(' ')
                    zup = int(params[1])
                    zdown = int(params[0])
                elif cmd[:2] == "VS":
                    params = cmd[2:].split(',')
                    if len(params) < 2:
                        params = cmd[2:].split(' ')
                    speeds = float(params[0])
                    with self.lock:
                        self.speed_feed = speeds
                elif cmd[:3] == "!VZ":
                    params = cmd[3:].split(',')
                    if len(params) < 2:
                        params = cmd[3:].split(' ')
                    speedz = float(params[0])
                    with self.lock:
                        self.speed_plunge = speedz
                elif cmd[:2] == "PU":
                    params = cmd[2:].split(',')
                    if len(params) < 2:
                        params = cmd[2:].split(' ')
                    if len(params) < 2:
                        continue
                    x = int(params[0])
                    y = int(params[1])
                    z = zup
                    d = dist(xpos, ypos, zpos, x, y, z)
                    t = d / RML_UNITS / SPEED_TRAVERSE
                    with self.lock:
                        self.cur_cmd_duration = t
                        self.time_remaining -= t
                        self.distance_milled += d
                        self.traverses_done.append(((xpos, ypos, zpos), (x, y, z)))
                    xpos = x; ypos = y; zpos = z;
                elif cmd[:1] == "Z":
                    params = cmd[1:].split(',')
                    if len(params) < 2:
                        params = cmd[1:].split(' ')
                    x = int(params[0])
                    y = int(params[1])
                    z = int(params[2])
                    dist_xy = math.hypot(xpos-x, ypos-y) / RML_UNITS
                    dist_z = float(zpos-z) / RML_UNITS
                    time_xy = dist_xy / speeds
                    time_z = dist_z / speedz
                    t = max(time_xy, time_z)
                    with self.lock:
                        self.cur_cmd_duration = t
                        self.time_remaining -= t
                        self.distance_milled += dist(xpos, ypos, zpos, x, y, z)
                        self.segments_done.append(((xpos, ypos, zpos), (x, y, z)))
                    xpos = x; ypos = y; zpos = z;
                time.sleep(self.cur_cmd_duration)
            except:
                print "ignoring: %s" % cmd
        self.done.set()

class myFieldStorage(cgi.FieldStorage):
    def make_file(self, binary=None):
        return tempfile.NamedTemporaryFile()

class InterFab ( object ):

    @cherrypy.expose
    def index ( self, message = 0, x = 0, y = 0 ):
        return open(os.path.join(MEDIA_DIR, u'index.html'))

    @cherrypy.expose
    def move ( self, x, y ):
        cmd = "rml_move " + x + " " + y
        os.system( cmd )
        path = "index?message=Moving bit to specified position.&x=" + x + "&y=" + y
        raise cherrypy.HTTPRedirect( path )

    @cherrypy.expose
    def init ( self, path ):
        self.rmob = RMLSender( "/dev/ttyUSB0" )
	RMLSender.__init__( self.rmob )
	RMLSender.load_file( self.rmob,path )
	RMLSender.start( self.rmob )
    
    @cherrypy.expose
    def abort ( self ) :
        RMLSender.abort( self.rmob )
        sys.exit(0)
	return "aborted"

    @cherrypy.expose
    @cherrypy.tools.noBodyProcess()
    def upload(self, theFile=None):
        cherrypy.response.timeout = 3600    
        lcHDRS = {}
        for key, val in cherrypy.request.headers.iteritems():
            lcHDRS[key.lower()] = val
	    
        formFields = myFieldStorage(fp=cherrypy.request.rfile,
	                                headers=lcHDRS,
	                                environ={'REQUEST_METHOD':'POST'},
	                                keep_blank_values=True)
	    
        theFile = formFields['theFile']
	uidr = ''.join(random.choice('0123456789ABCDEF') for i in range(10))
	path = '/tmp/' + uidr + "_" + theFile.filename
	os.link(theFile.file.name, path)
	self.init( path )
	raise cherrypy.HTTPRedirect( "index?message=Printing your file. Please keep patience." )

cherrypy.server.max_request_body_size = 20000
cherrypy.server.socket_timeout = 60
conf = {'/css': {'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(MEDIA_DIR, u'css')},
        '/js': {'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(MEDIA_DIR, u'js')},
        '/img': {'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(MEDIA_DIR, u'img')}
        }
print conf
cherrypy.quickstart(InterFab(), '/', config=conf)
