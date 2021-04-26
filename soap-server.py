import logging
import time
from spyne.decorator import srpc, rpc
from spyne.service import ServiceBase
from spyne.model.complex import ComplexModel
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer
from spyne.model.primitive import Unicode
from spyne.protocol.http import HttpRpc

from spyne.util.simple import wsgi_soap_application
class CorsService(ServiceBase):
    origin = '*'

def _on_method_return_object(ctx):
    ctx.transport.resp_headers['Access-Control-Allow-Origin'] = \
                                              ctx.descriptor.service_class.origin

CorsService.event_manager.add_listener('method_return_object', 
                                                        _on_method_return_object)
class HelloWorldService(CorsService):
    
    @srpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(name, times):
        '''
        Docstrings for service methods appear as documentation in the wsdl
        <b>what fun</b>
        @param name the name to say hello to
        @param the number of times to say hello
        @return the completed array
        '''

        for i in range(times):
            yield u'Hello, %s' % name

    @srpc(_returns=Unicode)
    def getTime():
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        return u'%s' % (current_time)

if __name__=='__main__':
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:7789")
    logging.info("wsdl is at: http://localhost:7789/?wsdl")

    wsgi_app = wsgi_soap_application([HelloWorldService], 'spyne.examples.hello.soap')
    server = make_server('127.0.0.1', 7789, wsgi_app)
    server.serve_forever()