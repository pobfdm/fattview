#!/usr/bin/env python3
from efatt import *
from fpdf.fpdf import FPDF	
from utils import *
import sys, subprocess

def openPDF():	
		if sys.platform == 'linux':
			subprocess.call(["xdg-open", pdfFile])
		elif sys.platform == 'win32':
			try:
				subprocess.call(["sumatra.exe", pdfFile])
			except :
				os.startfile(pdfFile)
				





if __name__== '__main__':
	
	
	try:
		myfatt=fatt(sys.argv[1])
	except IndexError:
		myfatt=fatt("esempio_privato_piu_linee_IT01234567890_FPR02.xml")
	
	fattHeader = {}
	fattHeader['IdPaeseTrasmittente']=myfatt.getTextFromNode('./FatturaElettronicaHeader/DatiTrasmissione/IdTrasmittente/IdPaese')
	fattHeader['IdCodiceTrasmittente']=myfatt.getTextFromNode('./FatturaElettronicaHeader/DatiTrasmissione/IdTrasmittente/IdCodice')
	fattHeader['ProgressivoInvio']=myfatt.getTextFromNode('./FatturaElettronicaHeader/DatiTrasmissione/ProgressivoInvio')
	fattHeader['FormatoTrasmissione']=myfatt.getTextFromNode('./FatturaElettronicaHeader/DatiTrasmissione/FormatoTrasmissione')
	fattHeader['CodiceDestinatario']=myfatt.getTextFromNode('./FatturaElettronicaHeader/DatiTrasmissione/CodiceDestinatario')
	fattHeader['PECDestinatario']=myfatt.getTextFromNode('./FatturaElettronicaHeader/DatiTrasmissione/PECDestinatario')
	
	#CedentePrestatore
	fattHeader['IdPaeseCedentePrestatore']=myfatt.getTextFromNode('./FatturaElettronicaHeader/CedentePrestatore/DatiAnagrafici/IdFiscaleIVA/IdPaese')
	fattHeader['IdCodiceCedentePrestatore']=myfatt.getTextFromNode('./FatturaElettronicaHeader/CedentePrestatore/DatiAnagrafici/IdFiscaleIVA/IdCodice')
	fattHeader['DenominazioneCedentePrestatore']=myfatt.getTextFromNode('./FatturaElettronicaHeader/CedentePrestatore/DatiAnagrafici/Anagrafica/Denominazione')
	fattHeader['RegimeFiscaleCedentePrestatore']=myfatt.getTextFromNode('./FatturaElettronicaHeader/CedentePrestatore/DatiAnagrafici/RegimeFiscale')
	fattHeader['IndirizzoSedePrestatore']=myfatt.getTextFromNode('./FatturaElettronicaHeader/CedentePrestatore/Sede/Indirizzo')
	fattHeader['CAPSedePrestatore']=myfatt.getTextFromNode('./FatturaElettronicaHeader/CedentePrestatore/Sede/CAP')
	fattHeader['ComuneSedePrestatore']=myfatt.getTextFromNode('./FatturaElettronicaHeader/CedentePrestatore/Sede/Comune')
	fattHeader['ProvinciaSedePrestatore']=myfatt.getTextFromNode('./FatturaElettronicaHeader/CedentePrestatore/Sede/Provincia')
	fattHeader['NazioneSedePrestatore']=myfatt.getTextFromNode('./FatturaElettronicaHeader/CedentePrestatore/Sede/Nazione')
	
	# Cessionario Committente
	fattHeader['CodiceFiscaleCessionarioCommittente']=myfatt.getTextFromNode('./FatturaElettronicaHeader/CessionarioCommittente/DatiAnagrafici/CodiceFiscale')
	fattHeader['DenominazioneCessionarioCommittente']=myfatt.getTextFromNode('./FatturaElettronicaHeader/CessionarioCommittente/DatiAnagrafici/Anagrafica/Denominazione')
	fattHeader['DenominazioneCessionarioCommittente']=myfatt.getTextFromNode('./FatturaElettronicaHeader/CessionarioCommittente/DatiAnagrafici/Anagrafica/Denominazione')
	fattHeader['IndirizzoSedeCessionarioCommittente']=myfatt.getTextFromNode('./FatturaElettronicaHeader/CessionarioCommittente/Sede/Indirizzo')
	fattHeader['CAPSedeCessionarioCommittente']=myfatt.getTextFromNode('./FatturaElettronicaHeader/CessionarioCommittente/Sede/CAP')
	fattHeader['ComuneSedeCessionarioCommittente']=myfatt.getTextFromNode('./FatturaElettronicaHeader/CessionarioCommittente/Sede/Comune')
	fattHeader['ProvinciaSedeCessionarioCommittente']=myfatt.getTextFromNode('./FatturaElettronicaHeader/CessionarioCommittente/Sede/Provincia')	
	fattHeader['NazioneSedeCessionarioCommittente']=myfatt.getTextFromNode('./FatturaElettronicaHeader/CessionarioCommittente/Sede/Nazione')
	
	# Body fattura elettronica
	fattBody = {}
	fattBody['TipoDocumento']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiGenerali/DatiGeneraliDocumento/TipoDocumento')
	fattBody['Divisa']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiGenerali/DatiGeneraliDocumento/Divisa')
	fattBody['Data']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiGenerali/DatiGeneraliDocumento/Data')
	fattBody['Numero']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiGenerali/DatiGeneraliDocumento/Numero')
	fattBody['Causale0']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiGenerali/DatiGeneraliDocumento/Causale',0)
	fattBody['Causale1']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiGenerali/DatiGeneraliDocumento/Causale',1)
	if fattBody['Causale1']=='VUOTO': fattBody['Causale1']=''
	
	# DatiOrdineAcquisto
	
	#Quanti sono
	count = myfatt.countChildElementByName('./FatturaElettronicaBody/DatiGenerali/DatiOrdineAcquisto/RiferimentoNumeroLinea')
	
	#I dati ordine acquisto saranno contenuti in questa lista nella forma ['1|§|66685|§|1', '2|§|87456893|§|3', '3|§|6540845|§|6'  etc...]
	datiOrdineAcquisto=[]
	
	for i in range(count):
		RiferimentoNumeroLinea = myfatt.getTextFromNode('./FatturaElettronicaBody/DatiGenerali/DatiOrdineAcquisto/RiferimentoNumeroLinea',i)
		IdDocumento = myfatt.getTextFromNode('./FatturaElettronicaBody/DatiGenerali/DatiOrdineAcquisto/IdDocumento',i)
		NumItem = myfatt.getTextFromNode('./FatturaElettronicaBody/DatiGenerali/DatiOrdineAcquisto/NumItem',i)
		
		datiOrdineAcquisto.append({
									'RiferimentoNumeroLinea':RiferimentoNumeroLinea,
									'IdDocumento': IdDocumento,
									'NumItem': NumItem
									})
	
	
	
	#DatiTrasporto
	fattBody['DatiAnagraficiVettoreIdPaese']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiGenerali/DatiTrasporto/DatiAnagraficiVettore/IdFiscaleIVA/IdPaese')
	fattBody['DatiAnagraficiVettoreIdCodice']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiGenerali/DatiTrasporto/DatiAnagraficiVettore/IdFiscaleIVA/IdCodice')
	fattBody['DatiAnagraficiVettoreDenominazione']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiGenerali/DatiTrasporto/DatiAnagraficiVettore/Anagrafica/Denominazione')
	fattBody['DataOraConsegnaVettore']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiGenerali/DatiTrasporto/DataOraConsegna')
	
	
	#Dati linee fattura
	linee=[]
	count = myfatt.countChildElementByName('./FatturaElettronicaBody/DatiBeniServizi/DettaglioLinee/NumeroLinea')
	for i in range(count):
		NumeroLinea=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiBeniServizi/DettaglioLinee/NumeroLinea',i)
		Descrizione=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiBeniServizi/DettaglioLinee/Descrizione',i)
		Quantita=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiBeniServizi/DettaglioLinee/Quantita',i)
		PrezzoUnitario=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiBeniServizi/DettaglioLinee/PrezzoUnitario',i)
		PrezzoTotale=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiBeniServizi/DettaglioLinee/PrezzoTotale',i)
		AliquotaIVA=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiBeniServizi/DettaglioLinee/AliquotaIVA',i)
		linee.append({
						'NumeroLinea':NumeroLinea,
						'Descrizione':Descrizione,
						'Quantita':Quantita,
						'PrezzoUnitario':PrezzoUnitario,
						'PrezzoTotale':PrezzoTotale,
						'AliquotaIVA':AliquotaIVA
						})
	
	
	#Riepilogo
	fattBody['DatiRiepilogoAliquotaIVA']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiBeniServizi/DatiRiepilogo/AliquotaIVA')
	fattBody['DatiRiepilogoImponibileImporto']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiBeniServizi/DatiRiepilogo/ImponibileImporto')
	fattBody['DatiRiepilogoImposta']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiBeniServizi/DatiRiepilogo/Imposta')
	fattBody['DatiRiepilogoEsigibilitaIVA']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiBeniServizi/DatiRiepilogo/EsigibilitaIVA')
	
	#Dati Pagamento
	fattBody['DatiPagamentoCondizioniPagamento']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiPagamento/CondizioniPagamento')
	fattBody['DatiPagamentoModalitaPagamento']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiPagamento/DettaglioPagamento/ModalitaPagamento')
	fattBody['DatiPagamentoDataScadenzaPagamento']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiPagamento/DettaglioPagamento/DataScadenzaPagamento')
	fattBody['DatiPagamentoImportoPagamento']=myfatt.getTextFromNode('./FatturaElettronicaBody/DatiPagamento/DettaglioPagamento/ImportoPagamento')
	
	
	#Stampo dati su stdout (debug)
	#print(fattHeader)
	print(fattBody)
	#print(datiOrdineAcquisto)
	#print(linee)
	
	
	
	
	#Scrittura del PDF
	from fpdf.fpdf import FPDF
	
	
	try:
		pdfFile=getTempDir()+os.path.basename(sys.argv[1])+'.pdf'
	except:
		pdfFile=getTempDir()+'fattview.pdf'
	
	class PDF(FPDF):
		def header(self):
			# Arial bold 15
			self.set_font('Arial', '', 8)
			# Move to the right
			self.cell(80)
			# Title
			self.cell(50, 9, 'Fattura elettronica', 0, 0, 'C')
			# Line break
			self.ln(20)

		# Page footer
		def footer(self):
			# Position at 1.5 cm from bottom
			self.set_y(-15)
			# Arial italic 8
			self.set_font('Arial', 'I', 8)
			# Page number
			self.cell(0, 10, 'Pagina ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

	
	###
	pdf = PDF('P', 'mm', 'A4')
	pdf.alias_nb_pages()
	pdf.add_page()
	
	#Dati relativi alla trasmissione
	pdf.set_font('Arial', 'B', 13)
	pdf.multi_cell(200,14, "Dati relativi alla trasmissione", 0, 'J', False)
	
	#Header fattura
	pdf.set_font('Arial', '', 12)
	pdf.cell(70, 10, "Identificativo del trasmittente: ", 1, 0, 'C')
	pdf.cell(70, 10, fattHeader['IdPaeseTrasmittente']+fattHeader['IdCodiceTrasmittente'], 1, 1, 'C')
	
	pdf.cell(70, 10, "Progressivo di invio: ", 1, 0, 'C')
	pdf.cell(70, 10, fattHeader['ProgressivoInvio'], 1, 1, 'C')
	
	pdf.cell(70, 10, "Formato Trasmissione: ", 1, 0, 'C')
	pdf.cell(70, 10, fattHeader['FormatoTrasmissione'], 1, 1, 'C')
	
	pdf.cell(70, 10, "Codice identificativo destinatario: ", 1, 0, 'C')
	pdf.cell(70, 10,fattHeader['CodiceDestinatario'], 1, 1, 'C')	
	
	pdf.cell(70, 10, "PEC destinatario: ", 1, 0, 'C')
	pdf.cell(70, 10,fattHeader['PECDestinatario'], 1, 1, 'C')	
	
	
	# Dati del cedente / prestatore
	pdf.multi_cell(200,8, '', 0, 'J', False)
	pdf.set_font('Arial', 'B', 13)
	pdf.multi_cell(200,14, "Dati del cedente / prestatore", 0, 'J', False)
	pdf.set_font('Arial', 'I', 13)
	pdf.multi_cell(200,14, "Dati Anagrafici", 0, 'J', False)
	
	pdf.set_font('Arial', '', 12)
	pdf.cell(70, 10, "Identificativo fiscale ai fini IVA: ", 1, 0, 'C')
	pdf.cell(110, 10,fattHeader['IdPaeseCedentePrestatore']+fattHeader['IdCodiceCedentePrestatore'], 1, 1, 'C')	
	
	pdf.cell(70, 10, "Denominazione: ", 1, 0, 'C')
	pdf.set_font('Arial', '', 9)
	pdf.cell(110, 10,fattHeader['DenominazioneCedentePrestatore'], 1, 1, 'C')
	pdf.set_font('Arial', '', 12)
	pdf.cell(70, 10, "Regime Fiscale: ", 1, 0, 'C')
	pdf.cell(110, 10,fattHeader['RegimeFiscaleCedentePrestatore'], 1, 1, 'C')		
	
	pdf.set_font('Arial', 'I', 13)
	pdf.multi_cell(200,14, "Dati della sede", 0, 'J', False)
	
	pdf.set_font('Arial', '', 12)
	pdf.cell(30, 10, "Indirizzo: ", 1, 0, 'C')
	pdf.cell(150, 10,fattHeader['IndirizzoSedePrestatore'], 1, 1, 'C')	
	
	pdf.cell(30, 10, "CAP: ", 1, 0, 'C')
	pdf.cell(150, 10,fattHeader['CAPSedePrestatore'], 1, 1, 'C')
	
	pdf.cell(30, 10, "Comune: ", 1, 0, 'C')
	pdf.cell(150, 10,fattHeader['ComuneSedePrestatore'], 1, 1, 'C')
	
	pdf.cell(30, 10, "Provincia: ", 1, 0, 'C')
	pdf.cell(150, 10,fattHeader['ProvinciaSedePrestatore'], 1, 1, 'C')
	
	pdf.cell(30, 10, "Nazione: ", 1, 0, 'C')
	pdf.cell(150, 10,fattHeader['NazioneSedePrestatore'], 1, 1, 'C')
	
	pdf.add_page()
	
	#Dati del cessionario / committente
	pdf.set_font('Arial', 'B', 13)
	pdf.multi_cell(200,14, "Dati del cessionario / committente", 0, 'J', False)
	pdf.set_font('Arial', 'I', 13)
	pdf.multi_cell(200,14, "Dati Anagrafici", 0, 'J', False)
	
	pdf.cell(50, 10, "Codice fiscale: ", 1, 0, 'C')
	pdf.cell(130, 10,fattHeader['CodiceFiscaleCessionarioCommittente'], 1, 1, 'C')
	pdf.cell(50, 10, "Denominazione: ", 1, 0, 'C')
	pdf.cell(130, 10,fattHeader['DenominazioneCessionarioCommittente'], 1, 1, 'C')
	
	pdf.set_font('Arial', 'I', 13)
	pdf.multi_cell(200,14, "Dati della sede", 0, 'J', False)
	
	pdf.cell(30, 10, "Indirizzo: ", 1, 0, 'C')
	pdf.cell(150, 10,fattHeader['IndirizzoSedeCessionarioCommittente'], 1, 1, 'C')
	
	pdf.cell(30, 10, "CAP: ", 1, 0, 'C')
	pdf.cell(150, 10,fattHeader['CAPSedeCessionarioCommittente'], 1, 1, 'C')
	
	pdf.cell(30, 10, "Comune: ", 1, 0, 'C')
	pdf.cell(150, 10,fattHeader['ComuneSedeCessionarioCommittente'], 1, 1, 'C')
	
	pdf.cell(30, 10, "Provincia: ", 1, 0, 'C')
	pdf.cell(150, 10,fattHeader['ProvinciaSedeCessionarioCommittente'], 1, 1, 'C')
	
	pdf.cell(30, 10, "Nazione: ", 1, 0, 'C')
	pdf.cell(150, 10,fattHeader['NazioneSedeCessionarioCommittente'], 1, 1, 'C')
	
	#Dati generali Documento
	pdf.multi_cell(200,8, '', 0, 'J', False)
	pdf.set_font('Arial', 'B', 13)
	pdf.multi_cell(200,14, "Dati generali documento", 0, 'J', False)
	pdf.set_font('Arial', '', 12)
	
	pdf.cell(50, 10, "Tipo Documento: ", 1, 0, 'C')
	pdf.cell(130, 10,fattBody['TipoDocumento'], 1, 1, 'C')
	
	pdf.cell(50, 10, "Valuta: ", 1, 0, 'C')
	pdf.cell(130, 10,fattBody['Divisa'], 1, 1, 'C')
	
	pdf.cell(50, 10, "Data: ", 1, 0, 'C')
	pdf.cell(130, 10,fattBody['Data'], 1, 1, 'C')
	
	pdf.cell(50, 10, "Numero: ", 1, 0, 'C')
	pdf.cell(130, 10,fattBody['Numero'], 1, 1, 'C')
	
	pdf.cell(180, 10, "Causale: ", 1, 1, 'C')
	pdf.set_font('Arial', '', 9)
	pdf.multi_cell(180,6, fattBody['Causale0']+'\n'+fattBody['Causale1'], 1, 'J', False)
	pdf.set_font('Arial', '', 12)
	
	#Dati ordine acquisto
	pdf.multi_cell(200,8, '', 0, 'J', False)
	pdf.set_font('Arial', 'B', 13)
	pdf.multi_cell(200,14, "Dati ordine acquisto:", 0, 'J', False)
	pdf.set_font('Arial', '', 12)
	
	for dati in datiOrdineAcquisto:
			pdf.cell(80, 10, "Numero linea di fattura a cui si riferisce: ", 1, 0, 'C')
			pdf.cell(100, 10,dati['RiferimentoNumeroLinea'], 1, 1, 'C')
			pdf.cell(80, 10, "Identificativo ordine di acquisto: ", 1, 0, 'C')
			pdf.cell(100, 10,dati['IdDocumento'], 1, 1, 'C')
			pdf.cell(80, 10, "Numero linea ordine di acquisto: ", 1, 0, 'C')
			pdf.cell(100, 10,dati['NumItem'], 1, 1, 'C')
			pdf.multi_cell(200,8, '', 0, 'J', False)
	
	
	#Dati relativi al trasporto
	pdf.multi_cell(200,8, '', 0, 'J', False)
	pdf.set_font('Arial', 'B', 13)
	pdf.multi_cell(200,14, "Dati relativi al trasporto:", 0, 'J', False)
	pdf.set_font('Arial', '', 12)	
	pdf.set_font('Arial', 'I', 13)
	pdf.multi_cell(200,14, "Dati del vettore:", 0, 'J', False)
	pdf.set_font('Arial', '', 12)
	
	pdf.cell(80, 10, "Identificativo fiscale ai fini IVA: ", 1, 0, 'C')
	pdf.cell(110, 10, fattBody['DatiAnagraficiVettoreIdPaese']+fattBody['DatiAnagraficiVettoreIdCodice'], 1, 1, 'C')
	pdf.cell(80, 10, "Denominazione: ", 1, 0, 'C')
	pdf.cell(110, 10, fattBody['DatiAnagraficiVettoreDenominazione'], 1, 1, 'C')	
	pdf.cell(80, 10, "Data/ora consegna: ", 1, 0, 'C')
	pdf.cell(110, 10, fattBody['DataOraConsegnaVettore'], 1, 1, 'C')	
	
	
	#Dati linee fattura
	pdf.add_page()
	pdf.set_font('Arial', 'B', 13)
	pdf.multi_cell(200,14, "Dati relativi alle linee di dettaglio della fornitura", 0, 'J', False)
	pdf.set_font('Arial', 'B', 9)
	pdf.cell(15, 8, "Nr. Linea", 1, 0, 'C')
	pdf.cell(85, 8, "Descrizione", 1, 0, 'C')
	pdf.cell(15, 8, "Qu.ta'", 1, 0, 'C')
	pdf.cell(25, 8, "Prezzo unitario", 1, 0, 'C')
	pdf.cell(25, 8, "Prezzo totale", 1, 0, 'C')
	pdf.cell(25, 8, "IVA", 1, 1, 'C')
	pdf.set_font('Arial', '', 8)
	
	for linea in linee:
		x_at_start= pdf.get_x()
		y_at_start= pdf.get_y()
		
		pdf.cell(15, 8, linea['NumeroLinea'], 1, 0, 'C')
		pdf.multi_cell(85,8, linea['Descrizione'], 1, 'J', False)
		x_after_dscr = pdf.get_x()
		y_after_dscr = pdf.get_y()
		pdf.set_xy(x_at_start+85+15, y_at_start)
		pdf.cell(15, 8, linea['Quantita'], 1, 0, 'C')
		pdf.cell(25, 8, linea['PrezzoUnitario'], 1, 0, 'C')
		pdf.cell(25, 8, linea['PrezzoTotale'], 1, 0, 'C')
		pdf.cell(25, 8, linea['AliquotaIVA'], 1, 1, 'C')
		pdf.set_xy(10,y_after_dscr)	
	
	#Riepilogo
	pdf.multi_cell(200,8, '', 0, 'J', False)
	pdf.set_font('Arial', 'B', 13)
	pdf.multi_cell(200,14, "Dati di riepilogo per aliquota IVA e natura", 0, 'J', False)
	pdf.set_font('Arial', '', 12)		
	pdf.cell(45, 8, "AliquotaIVA: "+fattBody['DatiRiepilogoAliquotaIVA'], 1, 0, 'C')
	pdf.cell(77, 8, "Tot. imponibile/importo: "+fattBody['DatiRiepilogoImponibileImporto'], 1, 1, 'C')
	pdf.cell(77, 8, "Tot. imposta: "+fattBody['DatiRiepilogoImposta'], 1, 0, 'C')	
	pdf.cell(45, 8, "Esigibilità IVA: "+fattBody['DatiRiepilogoEsigibilitaIVA'], 1, 0, 'C')
	
	#Dati pagamento
	pdf.multi_cell(200,8, '', 0, 'J', False)
	pdf.set_font('Arial', 'B', 13)
	pdf.multi_cell(200,14, "Dati prelativi al pagamento:", 0, 'J', False)
	pdf.set_font('Arial', '', 12)
	
	pdf.cell(60, 10, "Condizioni di pagamento: ", 1, 0, 'C')
	pdf.cell(130, 10,fattBody['DatiPagamentoCondizioniPagamento'], 1, 1, 'C')	
	
	pdf.cell(60, 10, "Modalita' di pagamento: ", 1, 0, 'C')
	pdf.cell(130, 10,fattBody['DatiPagamentoModalitaPagamento'], 1, 1, 'C')	
	
	pdf.cell(60, 10, "Scadenza pagamento: ", 1, 0, 'C')
	pdf.cell(130, 10,fattBody['DatiPagamentoDataScadenzaPagamento'], 1, 1, 'C')	
	
	pdf.cell(60, 10, "Importo pagamento: ", 1, 0, 'C')
	pdf.cell(130, 10,fattBody['DatiPagamentoImportoPagamento'], 1, 1, 'C')	
	
	
	
	try:
		pdf.output(pdfFile, 'F')	
		openPDF()
	except:
		print("Qualcosa è andato storto...")
	
	
	
	

