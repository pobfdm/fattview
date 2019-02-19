import xml.etree.ElementTree as ET

class fatt():
	
	def __init__(self, xmlfile):
		self.tree = ET.parse(xmlfile)
		
	
	def getTextFromNode(self,node,e=0):
		''' Specificare il path del nodo (esempio: "./FatturaElettronicaHeader/DatiTrasmissione/IdTrasmittente/IdPaese") '''
		root = self.tree.getroot()
		try:
			return(root.findall(node)[e].text)
		except IndexError:
			return "VUOTO"
	
	
	
	def getCountLinee(self):
		root = self.tree.getroot()
		r=0
		try:
			for c in root.findall('./FatturaElettronicaBody/DatiBeniServizi/DettaglioLinee/NumeroLinea'):
				r=r+1
			return r	
		except IndexError:			
			return r
		
	def getDescrizioneFromLinea(self,l):
		root = self.tree.getroot()
		try:
			return(root.findall("./FatturaElettronicaBody/DatiBeniServizi/DettaglioLinee/Descrizione")[l-1].text)
		except IndexError:
			return "VUOTO"
			
	def printAllDescrizioni(self): #for testing
		root = self.tree.getroot()
		n=0
		for d in root.findall('./FatturaElettronicaBody/DatiBeniServizi/DettaglioLinee/Descrizione'):		
			n=n+1
			print("Descrizione numero: %d\n %s" %  (n, d.text))
	
	def printAllRiferimentoNumeroLinea(self): #for testing
		root = self.tree.getroot()
		n=0
		res=[]
		for d in root.findall('./FatturaElettronicaBody/DatiGenerali/DatiOrdineAcquisto/RiferimentoNumeroLinea'):		
			n=n+1
			print("RiferimentoNumeroLinea:  %s" %  (d.text))
			res.append(d.text)
	
	
	def countChildElementByName(self,node):
		root = self.tree.getroot()
		r=0
		try:
			for c in root.findall(node):
				r=r+1
			return r	
		except IndexError:			
			return r
