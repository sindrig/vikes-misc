from suds.client import Client

WSDL_URL = 'http://www2.ksi.is/vefthjonustur/mot.asmx?WSDL'
VIKES = '103'

client = Client(WSDL_URL)
