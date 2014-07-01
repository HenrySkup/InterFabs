import os
import cherrypy

MEDIA_DIR = os.path.join(os.path.abspath("."), u"media")

class InterFab ( object ):

    @cherrypy.expose
    def index ( self ):
        return open(os.path.join(MEDIA_DIR, u'index.html'))

print os.path.join(MEDIA_DIR, u'css')

conf = {'/css': {'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(MEDIA_DIR, u'css')},
        '/js': {'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(MEDIA_DIR, u'js')},
        '/img': {'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(MEDIA_DIR, u'img')}
        }
print conf
cherrypy.quickstart(InterFab(), '/', config=conf)