import datetime

from lxml import etree
from datetime import datetime
from pytz import timezone
import uuid
from readExcel import getSheets

#Początek stałych
now_utc = datetime.now(timezone('UTC'))
today = now_utc.astimezone(timezone('CET'))

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


def koperta():
    root = etree.Element("DailyMeteringPointMeasurementsNotification")

    Header = etree.SubElement(root, "Header")
    MessageId = etree.SubElement(Header, "MessageId")
    MessageId.text = MessageIdText
    MessageType= etree.SubElement(Header,"MessageType")
    MessageType.text = MessageTypeText
    MessageTypeResponsibleOrganization = etree.SubElement(Header,"MessageTypeResponsibleOrganization")
    MessageTypeResponsibleOrganization.text = MessageTypeResponsibleOrganizationText
    MessageTimestamp = etree.SubElement(Header,"MessageTimestamp")
    MessageTimestamp.text = MessageTimestampText
    PhysicalSenderId = etree.SubElement(Header,"PhysicalSenderId")
    PhysicalSenderId.text = PhysicalSenderIdText
    PhysicalSenderIdResponsibleOrganization = etree.SubElement(Header,"PhysicalSenderIdResponsibleOrganization")
    PhysicalSenderIdResponsibleOrganization.text= PhysicalSenderIdResponsibleOrganizationText
    JuridicalSenderId = etree.SubElement(Header,"JuridicalSenderId")
    JuridicalSenderId.text = JuridicalSenderIdText
    JuridicalSenderIdResponsibleOrganization = etree.SubElement(Header,"JuridicalSenderIdResponsibleOrganization")
    JuridicalSenderIdResponsibleOrganization.text = JuridicalSenderIdResponsibleOrganizationText
    PhysicalRecipientId = etree.SubElement(Header,"PhysicalRecipientId")
    PhysicalRecipientId.text = PhysicalRecipientIdText
    PhysicalRecipientIdResponsibleOrganization = etree.SubElement(Header,"PhysicalRecipientIdResponsibleOrganization")
    PhysicalRecipientIdResponsibleOrganization.text = PhysicalRecipientIdResponsibleOrganizationText
    JuridicalRecipientId = etree.SubElement(Header,"JuridicalRecipientId")
    JuridicalRecipientId.text = JuridicalRecipientIdText
    JuridicalRecipientIdResponsibleOrganization = etree.SubElement(Header,"JuridicalRecipientIdResponsibleOrganization")
    JuridicalRecipientIdResponsibleOrganization.text = JuridicalRecipientIdResponsibleOrganizationText

    ProcessEnergyContext = etree.SubElement(root, "ProcessEnergyContext")
    BusinessProcess = etree.SubElement(ProcessEnergyContext,"BusinessProcess")
    BusinessProcess.text = BusinessProcessText
    BusinessProcessResponsibleOrganization = etree.SubElement(ProcessEnergyContext,"BusinessProcessResponsibleOrganization")
    BusinessProcessResponsibleOrganization.text = BusinessProcessResponsibleOrganizationText
    SenderBusinessRoleIdentifier = etree.SubElement(ProcessEnergyContext,"SenderBusinessRoleIdentifier")
    SenderBusinessRoleIdentifier.text = SenderBusinessRoleIdentifierText
    SenderBusinessRoleResponsibleOrganization = etree.SubElement(ProcessEnergyContext,"SenderBusinessRoleResponsibleOrganization")
    SenderBusinessRoleResponsibleOrganization.text = SenderBusinessRoleResponsibleOrganizationText
    IndustryClassificationId = etree.SubElement(ProcessEnergyContext,"IndustryClassificationId")
    IndustryClassificationId.text = IndustryClassificationIdText
    BusinessProcessMessageType = etree.SubElement(ProcessEnergyContext, "BusinessProcessMessageType")
    BusinessProcessMessageType.text = BusinessProcessMessageTypeText

    Payload= etree.SubElement(root, "Payload")

    addtopayload(Payload, "12345", "B11", 2000)

    return root


def addtopayload(payload,kodPPE,taryfa,roczneZuzycie):
    roczneZuzycie/=1000
    DailyMeteringPointMeasurementsForward = etree.SubElement(payload, "DailyMeteringPointMeasurementsForward")
    ReferenceTransactionId= etree.SubElement(DailyMeteringPointMeasurementsForward, "ReferenceTransactionId")
    ReferenceTransactionId.text = ReferenceTransactionIdText

    DataSubject = etree.SubElement(DailyMeteringPointMeasurementsForward, "DataSubject")
    DataSubjectType = etree.SubElement(DataSubject, "DataSubject")
    DataSubjectType.text = DataSubjectTypeText
    MeteringPointData_Basic = etree.SubElement(DataSubject, "MeteringPointData_Basic")
    MeteringPointCode = etree.SubElement(MeteringPointData_Basic, "MeteringPointCode")
    MeteringPointCode.text = kodPPE

    BasicData = etree.SubElement(DailyMeteringPointMeasurementsForward, "BasicData")
    date = today.date()
    PeriodStart = etree.SubElement(BasicData, "PeriodStart")
    PeriodStart.text = str(date) + "T00:00:00+02:00"
    PeriodEnd = etree.SubElement(BasicData, "PeriodEnd")
    PeriodEnd.text = str(date) + "T23:59:59+02:00"
    DataVersionNumber = etree.SubElement(BasicData, "DataVersionNumber")
    DataVersionNumber.text = DataVersionNumberText
    EnergyProduct = etree.SubElement(BasicData, "EnergyProduct")

    ProductType = etree.SubElement(EnergyProduct, "ProductType")
    ProductType.text = "CK1125"
    ResolutionDuration = etree.SubElement(EnergyProduct, "ResolutionDuration")
    ResolutionDuration.text = ResolutionDurationText

    # TODO DST +- 1pomiar
    slownik = getSheets()
    tabela = slownik[taryfa]
    pomiary = []

    for r in tabela:
        if date == r[0].date():
            print("super!")
            pomiary = r

    SEQText = 1
    for i in range(1,len(pomiary)):
        if pomiary[i] is not None:
            pomiar= round(pomiary[i]*roczneZuzycie/4, 4)

            for j in range(0,4):
                EnergyProductMeasurement = etree.SubElement(EnergyProduct, "EnergyProductMeasurement")
                SEQ = etree.SubElement(EnergyProductMeasurement, "SEQ")
                SEQ.text = str(SEQText)
                Volume = etree.SubElement(EnergyProductMeasurement, "Volume")
                VolumeText = str(pomiar)
                Volume.text = VolumeText
                QQ = etree.SubElement(EnergyProductMeasurement, "QQ")
                QQ.text = "CK0031"
                SEQText+=1



def prettyprint(element, **kwargs):
    xml = etree.tostring(element, pretty_print=True, **kwargs)
    print(xml.decode(), end='')

#wynik do pliku 6.1.1.5 timestamp.xml

def saveToFile(element):
    filename = "6.1.1.5.xml"
    f = open(filename, "w")
    xml = etree.tostring(element).decode('UTF-8')
    f.write(xml)
    f.close()

saveToFile(koperta())


