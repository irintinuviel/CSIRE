import datetime
import random

from lxml import etree
from datetime import datetime
from pytz import timezone
import uuid
from readExcel import getSheets

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

def koperta(dane):
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

        for c in e[3]:
            # TODO nie dla wszystkich produktów potrzebne
            zuzycie = zuzycieRoczne(e[2])
            roczneZuzycie.append([c,zuzycie])

        addtopayload(Payload, e[0], e[1], roczneZuzycie)

    return root

#az do konca pliku
#kiedy jest juz 1000, kod ppe+sformatowana napisowo rrr-mm-dd.xml

def addtopayload(payload,kodPPE,taryfa,roczneZuzycie):

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
        print(e[0])
        EnergyProduct = etree.SubElement(BasicData, u+"EnergyProduct")

        ProductType = etree.SubElement(EnergyProduct, u+"ProductType")
        ProductType.text = e[0]
        podstawa = e[1]/1000
        ResolutionDuration = etree.SubElement(EnergyProduct, u+"ResolutionDuration")
        ResolutionDuration.text = ResolutionDurationText

        # TODO DST +- 1pomiar
        slownik = getSheets()
        tabela = slownik[taryfa]
        pomiary = []

        for r in tabela:
            if date == r[0].date():
                pomiary = r

        SEQText = 1


        for i in range(1,len(pomiary)):
            if pomiary[i] is not None:
                if e[0] in napiecia:
                    pomiar = round(random.uniform(220,240),4)
                elif e[0] in straty:
                    pomiar= round(random.random()*0.01,4)
                else:
                    pomiar = round(pomiary[i] * podstawa / 4, 4)

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

def saveToFile(element,num):
    filename = "6.1.1.5"+str(datetime.now().strftime("_%y-%m-%d_"))+str(num)+".xml"
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

    # Parse the XML document
    xml_document = etree.parse(filename)

    # Validate the XML document against the schema
    is_valid = xmlschema.validate(xml_document)

    if is_valid:
        print("The XML document is valid.")
    else:
        print("The XML document is not valid.")
        # To print the list of validation errors
        print(xmlschema.error_log)


def readFile(filename):
    data= []
    with open(filename, mode='r') as file:
        for line in file.readlines():
            line = line.strip().split(",")
            line[3] = line[3].split(":")
            data.append(line)
    return data


def addtokoperta():
    alldata= readFile("sampleppe.csv")
    data=[]
    k= 0
    count = 0
    for l in alldata:

        data.append(l)
        count+=1
        #TODO ZMIEN TA 1000
        if count > 10:
            k+=1
            saveToFile(koperta(data),k)
            count= 0
            data= []
    k+=1
    saveToFile(koperta(data),k)

addtokoperta()

