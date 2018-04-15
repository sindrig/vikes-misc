from suds.client import Client

WSDL_URL = 'http://ws.hsi.is/vefthjonustur/mot.asmx?WSDL'
VIKES = '468'

client = Client(WSDL_URL)
