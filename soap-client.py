from suds.client import Client
hello_client = Client('http://localhost:7789/?wsdl')
print(type(hello_client.service.say_hello("Obing", 5)))