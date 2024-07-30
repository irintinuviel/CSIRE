import argparse
import datetime
import random
import threading

from lxml import etree
from datetime import datetime
from pytz import timezone
import uuid

from generatorPPE import generateData
from readExcel import getSheets
import concurrent.futures

#Początek stałych
nsmap = {
    "u": "urn:pl:oire:unk_6_1_1_5:v1",
    "t": "urn:pl:oire:technical:v1"
}
t = "{{{0}}}".format(nsmap["t"])
u = "{{{0}}}".format(nsmap["u"])

now_utc = datetime.now(timezone('UTC'))
today = now_utc.astimezone(timezone('CET'))

napiecia= ["CK1141","CK1142","CK1143"]
straty= ["CK1144","CK1145","CK1146","CK1147"]

podstawy = {
    "A": 200000000,
    "B": 20000000,
    "C": 1000000,
    "G": 2000
}


MessageIdText = str(uuid.uuid4())
MessageTypeText = "6.1_1"
MessageTypeResponsibleOrganizationText = "x"
MessageTimestampText = str(today.isoformat())
PhysicalSenderIdText = "19XPGEDYSTRYBUCR"
PhysicalSenderIdResponsibleOrganizationText = "305"
JuridicalSenderIdText = "19XPGEDYSTRYBUCR"
JuridicalSenderIdResponsibleOrganizationText = "305"
PhysicalRecipientIdText = "19XPL-RZE-SA---V"
PhysicalRecipientIdResponsibleOrganizationText = "305"
JuridicalRecipientIdText = "19XPL-RZE-SA---V"
JuridicalRecipientIdResponsibleOrganizationText = "305"

BusinessProcessText= "6.1."
BusinessProcessResponsibleOrganizationText = "x"
SenderBusinessRoleIdentifierText = "CK0086"
SenderBusinessRoleResponsibleOrganizationText = "260"
IndustryClassificationIdText = "23"
BusinessProcessMessageTypeText = "6.1.1.5."

ReferenceTransactionIdText = str(uuid.uuid4())
DataSubjectTypeText = "CK0150"
DataVersionNumberText = "1"
ResolutionDurationText = "CK0098"
#Koniec stałych

def zuzycieRoczne(klasa):
    podstawa= podstawy[klasa[0]]
    return random.uniform(1/5,5)* podstawa

def koperta(dane, slownik):
    root = etree.Element("{urn:pl:oire:unk_6_1_1_5:v1}DailyMeteringPointMeasurementsForwardNotification", nsmap=nsmap)

    Header = etree.SubElement(root, u+"Header")
    MessageId = etree.SubElement(Header, t+"MessageId")
    MessageId.text = MessageIdText
    MessageType= etree.SubElement(Header, t+"MessageType")
    MessageType.text = MessageTypeText
    MessageTypeResponsibleOrganization = etree.SubElement(Header, t+"MessageTypeResponsibleOrganization")
    MessageTypeResponsibleOrganization.text = MessageTypeResponsibleOrganizationText
    MessageTimestamp = etree.SubElement(Header, t+"MessageTimestamp")
    MessageTimestamp.text = MessageTimestampText
    PhysicalSenderId = etree.SubElement(Header, t+"PhysicalSenderId")
    PhysicalSenderId.text = PhysicalSenderIdText
    PhysicalSenderIdResponsibleOrganization = etree.SubElement(Header, t+"PhysicalSenderIdResponsibleOrganization")
    PhysicalSenderIdResponsibleOrganization.text= PhysicalSenderIdResponsibleOrganizationText
    JuridicalSenderId = etree.SubElement(Header, t+"JuridicalSenderId")
    JuridicalSenderId.text = JuridicalSenderIdText
    JuridicalSenderIdResponsibleOrganization = etree.SubElement(Header, t+"JuridicalSenderIdResponsibleOrganization")
    JuridicalSenderIdResponsibleOrganization.text = JuridicalSenderIdResponsibleOrganizationText
    PhysicalRecipientId = etree.SubElement(Header, t+"PhysicalRecipientId")
    PhysicalRecipientId.text = PhysicalRecipientIdText
    PhysicalRecipientIdResponsibleOrganization = etree.SubElement(Header, t+"PhysicalRecipientIdResponsibleOrganization")
    PhysicalRecipientIdResponsibleOrganization.text = PhysicalRecipientIdResponsibleOrganizationText
    JuridicalRecipientId = etree.SubElement(Header, t+"JuridicalRecipientId")
    JuridicalRecipientId.text = JuridicalRecipientIdText
    JuridicalRecipientIdResponsibleOrganization = etree.SubElement(Header, t+"JuridicalRecipientIdResponsibleOrganization")
    JuridicalRecipientIdResponsibleOrganization.text = JuridicalRecipientIdResponsibleOrganizationText

    ProcessEnergyContext = etree.SubElement(root, u+"ProcessEnergyContext")
    BusinessProcess = etree.SubElement(ProcessEnergyContext, t+"BusinessProcess")
    BusinessProcess.text = BusinessProcessText
    BusinessProcessResponsibleOrganization = etree.SubElement(ProcessEnergyContext, t+"BusinessProcessResponsibleOrganization")
    BusinessProcessResponsibleOrganization.text = BusinessProcessResponsibleOrganizationText
    SenderBusinessRoleIdentifier = etree.SubElement(ProcessEnergyContext, t+"SenderBusinessRoleIdentifier")
    SenderBusinessRoleIdentifier.text = SenderBusinessRoleIdentifierText
    SenderBusinessRoleResponsibleOrganization = etree.SubElement(ProcessEnergyContext, t+"SenderBusinessRoleResponsibleOrganization")
    SenderBusinessRoleResponsibleOrganization.text = SenderBusinessRoleResponsibleOrganizationText
    IndustryClassificationId = etree.SubElement(ProcessEnergyContext, t+"IndustryClassificationId")
    IndustryClassificationId.text = IndustryClassificationIdText
    BusinessProcessMessageType = etree.SubElement(ProcessEnergyContext, t+"BusinessProcessMessageType")
    BusinessProcessMessageType.text = BusinessProcessMessageTypeText

    Payload= etree.SubElement(root, u+"Payload")


    for e in dane:
        roczneZuzycie = []
        taryfa = e[1]
        tabela = slownik[taryfa]

        for c in e[3]:
            # TODO nie dla wszystkich produktów potrzebne
            zuzycie = zuzycieRoczne(e[2])
            roczneZuzycie.append([c,zuzycie])

        addtopayload(Payload, e[0], tabela, roczneZuzycie)

    return root


def addtopayload(payload,kodPPE,pomiary,roczneZuzycie):

    DailyMeteringPointMeasurementsForward = etree.SubElement(payload, u+"DailyMeteringPointMeasurementsForward")
    ReferenceTransactionId= etree.SubElement(DailyMeteringPointMeasurementsForward, u+"ReferenceTransactionId")
    ReferenceTransactionId.text = ReferenceTransactionIdText

    DataSubject = etree.SubElement(DailyMeteringPointMeasurementsForward, u+"DataSubject")
    DataSubjectType = etree.SubElement(DataSubject, u+"DataSubject")
    DataSubjectType.text = DataSubjectTypeText
    MeteringPointData_Basic = etree.SubElement(DataSubject, u+"MeteringPointData_Basic")
    MeteringPointCode = etree.SubElement(MeteringPointData_Basic, u+"MeteringPointCode")
    MeteringPointCode.text = kodPPE

    BasicData = etree.SubElement(DailyMeteringPointMeasurementsForward, u+"BasicData")
    date = today.date()
    PeriodStart = etree.SubElement(BasicData, u+"PeriodStart")
    PeriodStart.text = str(date) + "T00:00:00+02:00"
    PeriodEnd = etree.SubElement(BasicData, u+"PeriodEnd")
    PeriodEnd.text = str(date) + "T23:59:59+02:00"
    DataVersionNumber = etree.SubElement(BasicData, u+"DataVersionNumber")
    DataVersionNumber.text = DataVersionNumberText

    for e in roczneZuzycie:
        EnergyProduct = etree.SubElement(BasicData, u+"EnergyProduct")

        ProductType = etree.SubElement(EnergyProduct, u+"ProductType")
        ProductType.text = e[0]
        podstawa = e[1] * 0.001
        ResolutionDuration = etree.SubElement(EnergyProduct, u+"ResolutionDuration")
        ResolutionDuration.text = ResolutionDurationText

        # TODO DST +- 1pomiar

        SEQText = 1

        for i in range(1,len(pomiary)):
            if pomiary[i] is not None:
                if e[0] in napiecia:
                    pomiar = round(random.uniform(220,240),4)
                elif e[0] in straty:
                    pomiar= round(random.random()*0.01,4)
                else:
                    pomiar = round(pomiary[i] * podstawa * 0.25, 4)

                for j in range(0,4):
                    EnergyProductMeasurement = etree.SubElement(EnergyProduct, u+"EnergyProductMeasurement")
                    SEQ = etree.SubElement(EnergyProductMeasurement, u+"SEQ")
                    SEQ.text = str(SEQText)
                    Volume = etree.SubElement(EnergyProductMeasurement, u+"Volume")
                    VolumeText = str(pomiar)
                    Volume.text = VolumeText
                    QQ = etree.SubElement(EnergyProductMeasurement, u+"QQ")
                    QQ.text = "CK0031"
                    SEQText+=1


def prettyprint(element, **kwargs):
    xml = etree.tostring(element, pretty_print=True, **kwargs)
    print(xml.decode(), end='')

def saveToFile(element,num,katalog,doba):
    filename = katalog+"/6.1.1.5"+str(doba.strftime("_%y-%m-%d_"))+str(num)+".xml"
    f = open(filename, "w")
    xml = etree.tostring(element).decode('UTF-8')
    f.write(xml)
    f.close()


#funkcja walidujaca wg pliku xsd
def validate(filename):
    # Load the XML Schema
    with open('.\\6_1_1_5.xsd', 'rb') as schema_file:
        xmlschema_doc = etree.parse(schema_file)
        xmlschema = etree.XMLSchema(xmlschema_doc)

    xml_document = etree.parse(filename)
    is_valid = xmlschema.validate(xml_document)

    if is_valid:
        print("The XML document is valid.")
    else:
        print("The XML document is not valid.")
        print(xmlschema.error_log)


def readFile(filename):
    data= []
    with open(filename, mode='r') as file:
        for line in file.readlines():
            line = line.strip().split(",")
            line[3] = line[3].split(":")
            data.append(line)
    return data

def szukajDlaDoby(slownik,doba):
    slowniknew= {}
    for k in slownik.keys():
        for e in slownik[k]:
            if e[0].date() == doba:
                slowniknew[k] = e[1:]
    return slowniknew

def generujProfile(ppe,profil,katalog,doba,paczka):
    doba = datetime.strptime(doba, "%Y%m%d").date()
    alldata= readFile(ppe)
    slownik = getSheets(profil)
    slownik = szukajDlaDoby(slownik,doba)
    data=[]
    k= 0
    count = 0
    threadnum= 6

    threads=[]
    for l in alldata:
        data.append(l)
        count+=1

        if count >= paczka:
            k+=1
            thread = threading.Thread(target=saveToFile,args=(koperta(data,slownik),k,katalog,doba))
            threads.append(thread)
            thread.start()
            count= 0
            data= []

        while len(threads) >= threadnum:
            for t in threads:
                if not t.is_alive():
                    threads.remove(t)

    if data:
        k+=1
        thread = threading.Thread(target=saveToFile, args=(koperta(data, slownik), k,katalog,doba))
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()


parser = argparse.ArgumentParser(description='Generuj')
subparsers = parser.add_subparsers(dest='subcommand')
subparsers.required = True

parser_ppe = subparsers.add_parser('generuj-ppe')

parser_ppe.add_argument(
    '-i',
    required=True,
    dest='plik_konfiguracyjny',
    help='Nazwa pliku konfiguracyjnego'
)
parser_ppe.add_argument(
    '-s',
    default='profil_standardowy.xls', #POTRZEBNE
    required=False,
    dest='plik_profil',
    help='Nazwa pliku z profilem standardowym'
)
parser_ppe.add_argument(
    '-o',
    required=True,
    dest= 'plik_wynikowy',
    help='Nazwa pliku wynikowego'
)

parser_6_1_1_5 = subparsers.add_parser('generuj-6.1.1.5')

parser_6_1_1_5.add_argument(
    '-i',
    default='ppe.txt', #nie csv?
    required= False,
    dest='plik_ppe',
    help='Nazwa pliku z ppe, domyślnie ppe.txt'
)
parser_6_1_1_5.add_argument(
    '-s',
    default='profil_standardowy.xlsx', #XLSX, openpxl does not support old xls format
    required=False,
    dest='plik_profil',
    help='Nazwa pliku z profilem standardowym, domyślnie profil_standardowy.xls'
)
parser_6_1_1_5.add_argument(
    '-o',
    required=True,
    dest='katalog_wynikowy',
    help='Sciezka do katalogu wynikowego'
)
parser_6_1_1_5.add_argument(
    '-d',
    required=True,
    dest='doba',
    help='Doba w formacie RRRRMMDD'
)
parser_6_1_1_5.add_argument(
    '-p',
    required=False,
    default=1000,
    dest='paczka',
    help='Wielkosc paczki, domyslnie 1000'
)

args = parser.parse_args()

if args.subcommand == 'generuj-ppe':
    print('I will now generate from %s to %s' % (args.plik_konfiguracyjny, args.plik_wynikowy))
    generateData(args.plik_konfiguracyjny,args.plik_profil,args.plik_wynikowy)

if args.subcommand == 'generuj-6.1.1.5':
    print('ppe: %s profil standardowy: %s katalog: %s doba: %s paczka: %s' % (args.plik_ppe, args.plik_profil,args.katalog_wynikowy,args.doba,args.paczka))
    generujProfile(args.plik_ppe, args.plik_profil,args.katalog_wynikowy,args.doba,args.paczka)
#generujProfile("generatedPPE.csv", "Klasy-PP.xlsx","wynik", datetime.now().date().strftime("%Y%m%d"), 1000)


