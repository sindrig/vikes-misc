from suds.client import Client

NAME = 'Fótbolti'
ID = 'ksi'
WSDL_URL = 'http://www2.ksi.is/vefthjonustur/mot.asmx?WSDL'
VIKES = '103'

client = Client(WSDL_URL)
