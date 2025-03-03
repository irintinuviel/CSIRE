import argparse
import concurrent.futures
import datetime
import logging
import os
import random
import string
import sys
import threading
from contextlib import redirect_stdout
from os import listdir
from os.path import isdir
from lxml import etree
from datetime import datetime
from pytz import timezone
import uuid

from setuptools import namespaces
from funkcjekolejki import send_file_to_queue, load_config, init_logging, get_messages_from_queue
from generatorPPE import generatePPE
from readExcel import czytajProfileStandardowe, czytajOBIS

#Początek stałych
nsmap = {
    "u1": "urn:pl:oire:unk_6_1_1_1:v1",
    "u5": "urn:pl:oire:unk_6_1_1_5:v1",
    "u7": "urn:pl:oire:unk_7_1_1_4:v1",
    "u2": "urn:pl:oire:unk_6_2_1_1:v1",
    "t": "urn:pl:oire:technical:v1"
}
t = "{{{0}}}".format(nsmap["t"])

now_utc = datetime.now(timezone('UTC'))
today = now_utc.astimezone(timezone('CET'))

napiecia = ["CK1141", "CK1142", "CK1143"]
straty = ["CK1144", "CK1145", "CK1146", "CK1147"]

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

BusinessProcessText = "6.1."
BusinessProcessResponsibleOrganizationText = "x"
SenderBusinessRoleIdentifierText = "CK0086"
SenderBusinessRoleResponsibleOrganizationText = "260"
IndustryClassificationIdText = "23"

ReferenceTransactionIdText = str(uuid.uuid4())
DataSubjectTypeText = "CK0150"
DataVersionNumberText = "1"
ResolutionDurationText = "CK0098"

billingmethods = ["CK0131", "CK0130"]
weights = [0.98, 0.02]
#Koniec stałych

def zuzycie_roczne(klasa):
    podstawa = podstawy[klasa[0]]
    return random.uniform(1 / 5, 5) * podstawa

def koperta(dane, slownik, typ, doba):
    if typ == "6.1.1.1":
        root = etree.Element("{urn:pl:oire:unk_6_1_1_1:v1}DailyMeteringPointMeasurementsNotification", nsmap=nsmap)
        BusinessProcessMessageTypeText = "6.1.1.1."
        u = "{{{0}}}".format(nsmap["u1"])
    elif typ == "7.1.1.4":
        root = etree.Element("{urn:pl:oire:unk_7_1_1_4:v1}DailyMeteringPointMeasurementsNotification", nsmap=nsmap)
        BusinessProcessMessageTypeText = "7.1.1.4."
        u = "{{{0}}}".format(nsmap["u7"])
    elif typ == "6.2.1.1":
        root = etree.Element("{urn:pl:oire:unk_6_2_1_1:v1}NewMeasurementsNotification", nsmap=nsmap)
        BusinessProcessMessageTypeText = "6.2.1.1."
        u = "{{{0}}}".format(nsmap["u2"])
    else:
        root = etree.Element("{urn:pl:oire:unk_6_1_1_5:v1}DailyMeteringPointMeasurementsForwardNotification",
                             nsmap=nsmap)
        u = "{{{0}}}".format(nsmap["u5"])
        BusinessProcessMessageTypeText = "6.1.1.5."

    Header = etree.SubElement(root, u + "Header")
    MessageId = etree.SubElement(Header, t + "MessageId")
    MessageId.text = MessageIdText
    MessageType = etree.SubElement(Header, t + "MessageType")
    MessageType.text = MessageTypeText
    MessageTypeResponsibleOrganization = etree.SubElement(Header, t + "MessageTypeResponsibleOrganization")
    MessageTypeResponsibleOrganization.text = MessageTypeResponsibleOrganizationText
    MessageTimestamp = etree.SubElement(Header, t + "MessageTimestamp")
    MessageTimestamp.text = MessageTimestampText
    PhysicalSenderId = etree.SubElement(Header, t + "PhysicalSenderId")
    PhysicalSenderId.text = PhysicalSenderIdText
    PhysicalSenderIdResponsibleOrganization = etree.SubElement(Header, t + "PhysicalSenderIdResponsibleOrganization")
    PhysicalSenderIdResponsibleOrganization.text = PhysicalSenderIdResponsibleOrganizationText
    JuridicalSenderId = etree.SubElement(Header, t + "JuridicalSenderId")
    JuridicalSenderId.text = JuridicalSenderIdText
    JuridicalSenderIdResponsibleOrganization = etree.SubElement(Header, t + "JuridicalSenderIdResponsibleOrganization")
    JuridicalSenderIdResponsibleOrganization.text = JuridicalSenderIdResponsibleOrganizationText
    PhysicalRecipientId = etree.SubElement(Header, t + "PhysicalRecipientId")
    PhysicalRecipientId.text = PhysicalRecipientIdText
    PhysicalRecipientIdResponsibleOrganization = etree.SubElement(Header,
                                                                  t + "PhysicalRecipientIdResponsibleOrganization")
    PhysicalRecipientIdResponsibleOrganization.text = PhysicalRecipientIdResponsibleOrganizationText
    JuridicalRecipientId = etree.SubElement(Header, t + "JuridicalRecipientId")
    JuridicalRecipientId.text = JuridicalRecipientIdText
    JuridicalRecipientIdResponsibleOrganization = etree.SubElement(Header,
                                                                   t + "JuridicalRecipientIdResponsibleOrganization")
    JuridicalRecipientIdResponsibleOrganization.text = JuridicalRecipientIdResponsibleOrganizationText

    ProcessEnergyContext = etree.SubElement(root, u + "ProcessEnergyContext")
    BusinessProcess = etree.SubElement(ProcessEnergyContext, t + "BusinessProcess")
    BusinessProcess.text = BusinessProcessText
    BusinessProcessResponsibleOrganization = etree.SubElement(ProcessEnergyContext,
                                                              t + "BusinessProcessResponsibleOrganization")
    BusinessProcessResponsibleOrganization.text = BusinessProcessResponsibleOrganizationText
    SenderBusinessRoleIdentifier = etree.SubElement(ProcessEnergyContext, t + "SenderBusinessRoleIdentifier")
    SenderBusinessRoleIdentifier.text = SenderBusinessRoleIdentifierText
    SenderBusinessRoleResponsibleOrganization = etree.SubElement(ProcessEnergyContext,
                                                                 t + "SenderBusinessRoleResponsibleOrganization")
    SenderBusinessRoleResponsibleOrganization.text = SenderBusinessRoleResponsibleOrganizationText
    IndustryClassificationId = etree.SubElement(ProcessEnergyContext, t + "IndustryClassificationId")
    IndustryClassificationId.text = IndustryClassificationIdText
    BusinessProcessMessageType = etree.SubElement(ProcessEnergyContext, t + "BusinessProcessMessageType")
    BusinessProcessMessageType.text = BusinessProcessMessageTypeText

    payload = etree.SubElement(root, u + "Payload")

    if typ == "6.2.1.1":
        generuj_dane_wskazan(dane, slownik, payload, u)
    else:
        generuj_dane_profilowe(dane, slownik, payload, doba, typ, u)

    return root


def generuj_dane_profilowe(dane, slownik, payload, doba, typ, u):
    for e in dane:
        roczneZuzycie = []
        taryfa = e[1]
        tabela = slownik[taryfa]

        for c in e[3]:
            # TODO nie dla wszystkich produktów potrzebne
            zuzycie = zuzycie_roczne(e[2])
            roczneZuzycie.append([c, zuzycie])

        profile_payload(payload, e[0], tabela, roczneZuzycie, doba, typ, u)


def generuj_dane_wskazan(dane, slownikOBIS, payload, u):
    for e in dane:

        stref = int(e[1][2])
        liczydla = []
        for c in e[3]:
            if c in slownikOBIS.keys():
                max = len(slownikOBIS.get(c))
                for i in range(0, stref):
                    if i < max:
                        liczydla.append(slownikOBIS[c][i])

        wskazania_payload(payload, e[0], liczydla, u)


def wskazania_payload(payload, kodPPE, liczydla, u):
    NewMeasurements = etree.SubElement(payload, u + "NewMeasurements")
    ReferenceTransactionId = etree.SubElement(NewMeasurements, u + "ReferenceTransactionId")
    ReferenceTransactionId.text = ReferenceTransactionIdText

    DataSubject = etree.SubElement(NewMeasurements, u + "DataSubject")
    DataSubjectType = etree.SubElement(DataSubject, u + "DataSubject")
    DataSubjectType.text = DataSubjectTypeText
    MeteringPointData_Basic = etree.SubElement(DataSubject, u + "MeteringPointData_Basic")
    MeteringPointCode = etree.SubElement(MeteringPointData_Basic, u + "MeteringPointCode")
    MeteringPointCode.text = kodPPE

    BasicData = etree.SubElement(NewMeasurements, u + "BasicData")
    DataVersionNumber = etree.SubElement(BasicData, u + "DataVersionNumber")
    DataVersionNumber.text = DataVersionNumberText
    MeasurementDataType = etree.SubElement(BasicData, u + "MeasurementDataType")
    MeasurementDataType.text = "CK0555"
    ExcessPowerConsumptionBillingMethod = etree.SubElement(BasicData, u + "ExcessPowerConsumptionBillingMethod")
    #suma
    ExcessPowerConsumptionBillingMethod.text = "CK0012"
    PublicationReason = etree.SubElement(BasicData, u + "PublicationReason")
    PublicationReasonType = etree.SubElement(PublicationReason, u + "PublicationReason")
    PublicationReasonType.text = random.choices(billingmethods, weights, k=1)[0]
    Meter = etree.SubElement(NewMeasurements, u + "Meter")
    MeterNumber = etree.SubElement(Meter, u + "MeterNumber")
    MeterNumber.text = ''.join(random.choices(string.digits, k=20))

    for e in liczydla:
        MeteringRegister = etree.SubElement(Meter, u + "MeteringRegister")
        RegisterType = etree.SubElement(MeteringRegister, u + "RegisterType")
        RegisterType.text = e
        EnergyMeasurement = etree.SubElement(MeteringRegister, u + "EnergyMeasurement")
        MeasurementType = etree.SubElement(EnergyMeasurement, u + "MeasurementType")
        #wskazanie jednostkowe
        MeasurementType.text = "CK0533"
        MeasurementSource = etree.SubElement(EnergyMeasurement, u + "MeasurementSource")
        #zdalny
        MeasurementSource.text = "CK0830"
        MeasurementDateTime = etree.SubElement(EnergyMeasurement, u + "MeasurementDateTime")
        MeasurementDateTime.text = datetime.now(timezone('UTC')).isoformat()
        MeterRegisterValue = etree.SubElement(EnergyMeasurement, u + "MeterRegisterValue")
        MeterRegisterValue.text = str(round(random.uniform(1, 10000), 4))
        MeterMultiplier = etree.SubElement(EnergyMeasurement, u + "MeterMultiplier")
        MeterMultiplier.text = str(1)
        MeterRegisterEventType = etree.SubElement(EnergyMeasurement, u + "MeterRegisterEventType")
        MeterRegisterEventType.text = "CK0576"


def profile_payload(payload, kodPPE, pomiary, roczneZuzycie, doba, typ, u):
    if typ == "6.1.1.1":
        DailyMeteringPointMeasurementsForward = etree.SubElement(payload, u + "DailyMeteringPointMeasurements")
        ReferenceTransactionId = etree.SubElement(DailyMeteringPointMeasurementsForward, u + "ReferenceTransactionId")
        ReferenceTransactionId.text = ReferenceTransactionIdText
    elif typ == "7.1.1.4":
        DailyMeteringPointMeasurementsForward = etree.SubElement(payload, u + "DailyMeteringPointMeasurements")
        Miscellaneous = etree.SubElement(DailyMeteringPointMeasurementsForward, u + "Miscellaneous")
        ProcessInstanceId = etree.SubElement(Miscellaneous, u + "ProcessInstanceId")
        ProcessInstanceId.text = ReferenceTransactionIdText
    else:
        DailyMeteringPointMeasurementsForward = etree.SubElement(payload, u + "DailyMeteringPointMeasurementsForward")
        ReferenceTransactionId = etree.SubElement(DailyMeteringPointMeasurementsForward, u + "ReferenceTransactionId")
        ReferenceTransactionId.text = ReferenceTransactionIdText

    DataSubject = etree.SubElement(DailyMeteringPointMeasurementsForward, u + "DataSubject")
    DataSubjectType = etree.SubElement(DataSubject, u + "DataSubject")
    DataSubjectType.text = DataSubjectTypeText
    MeteringPointData_Basic = etree.SubElement(DataSubject, u + "MeteringPointData_Basic")
    MeteringPointCode = etree.SubElement(MeteringPointData_Basic, u + "MeteringPointCode")
    MeteringPointCode.text = kodPPE

    BasicData = etree.SubElement(DailyMeteringPointMeasurementsForward, u + "BasicData")

    PeriodStart = etree.SubElement(BasicData, u + "PeriodStart")
    PeriodStart.text = str(doba) + "T00:00:00+02:00"
    PeriodEnd = etree.SubElement(BasicData, u + "PeriodEnd")
    PeriodEnd.text = str(doba) + "T23:59:59+02:00"

    if not typ == "7.1.1.4":
        DataVersionNumber = etree.SubElement(BasicData, u + "DataVersionNumber")
        DataVersionNumber.text = DataVersionNumberText

    for e in roczneZuzycie:
        EnergyProduct = etree.SubElement(BasicData, u + "EnergyProduct")

        ProductType = etree.SubElement(EnergyProduct, u + "ProductType")
        ProductType.text = e[0]
        podstawa = e[1] * 0.001
        ResolutionDuration = etree.SubElement(EnergyProduct, u + "ResolutionDuration")
        ResolutionDuration.text = ResolutionDurationText

        # TODO DST +- 1pomiar

        SEQText = 1

        for i in range(1, len(pomiary)):
            if pomiary[i] is not None:
                if e[0] in napiecia:
                    pomiar = round(random.uniform(220, 240), 4)
                elif e[0] in straty:
                    pomiar = round(random.random() * 0.01, 4)
                else:
                    pomiar = round(pomiary[i] * podstawa * 0.25, 4)

                for j in range(0, 4):
                    EnergyProductMeasurement = etree.SubElement(EnergyProduct, u + "EnergyProductMeasurement")
                    SEQ = etree.SubElement(EnergyProductMeasurement, u + "SEQ")
                    SEQ.text = str(SEQText)
                    Volume = etree.SubElement(EnergyProductMeasurement, u + "Volume")
                    VolumeText = str(pomiar)
                    Volume.text = VolumeText
                    QQ = etree.SubElement(EnergyProductMeasurement, u + "QQ")
                    QQ.text = "CK0031"
                    SEQText += 1

def save_to_file(element, num, katalog, doba, typ):
    if typ == "6.1.1.1":
        filename = katalog + "/6.1.1.1" + str(doba.strftime("_%y-%m-%d_")) + str(num) + ".xml"
    elif typ == "7.1.1.4":
        filename = katalog + "/7.1.1.4" + str(doba.strftime("_%y-%m-%d_")) + str(num) + ".xml"
    elif typ == "6.2.1.1":
        filename = katalog + "/6.2.1.1" + str(doba.strftime("_%y-%m-%d_")) + str(num) + ".xml"
    else:
        filename = katalog + "/6.1.1.5" + str(doba.strftime("_%y-%m-%d_")) + str(num) + ".xml"
    f = open(filename, "w")
    xml = etree.tostring(element).decode('UTF-8')
    f.write(xml)
    f.close()


#funkcja walidujaca wg pliku xsd
def validate(filename):
    xml_document = etree.parse(filename)

    typ = xml_document.xpath('//t:BusinessProcessMessageType/text()', namespaces=nsmap)[0]

    if typ == "6.1.1.1.":
        schemaname = 'xsdfiles/6_1_1_1.xsd'
    elif typ == "7.1.1.4.":
        schemaname = 'xsdfiles/7_1_1_4.xsd'
    elif typ == "6.2.1.1.":
        schemaname = 'xsdfiles/6_2_1_1.xsd'
    else:
        schemaname = 'xsdfiles/6_1_1_5.xsd'
    # Load the XML Schema
    with open(schemaname, 'rb') as schema_file:
        xmlschema_doc = etree.parse(schema_file)
        xmlschema = etree.XMLSchema(xmlschema_doc)

    is_valid = xmlschema.validate(xml_document)

    if is_valid:
        print(filename + " is valid.")
    else:
        print(filename + " is not valid.")
        print(xmlschema.error_log)

def read_ppe_file(filename):
    data = []
    with open(filename, mode='r') as file:
        for line in file.readlines():
            line = line.strip().split(",")
            line[3] = line[3].split(":")
            data.append(line)
    return data


def szukaj_dla_doby(slownik, doba):
    slowniknew = {}
    for k in slownik.keys():
        for e in slownik[k]:
            if e[0].date() == doba:
                slowniknew[k] = e[1:]
    return slowniknew


def generuj_profile(ppe, profil, katalog, doba, paczka, typ):
    doba = datetime.strptime(doba, "%Y%m%d").date()
    alldata = read_ppe_file(ppe)
    slownik = czytajProfileStandardowe(profil)
    slownik = szukaj_dla_doby(slownik, doba)
    data = []
    k = 0
    count = 0
    threadnum = 6

    threads = []
    for l in alldata:
        data.append(l)
        count += 1

        if count >= paczka:
            k += 1
            thread = threading.Thread(target=save_to_file,
                                      args=(koperta(data, slownik, typ, doba), k, katalog, doba, typ))
            threads.append(thread)
            thread.start()
            count = 0
            data = []

        while len(threads) >= threadnum:
            for t in threads:
                if not t.is_alive():
                    threads.remove(t)

    if data:
        k += 1
        thread = threading.Thread(target=save_to_file, args=(koperta(data, slownik, typ, doba), k, katalog, doba, typ))
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()


def generuj_wskazania(ppe, plikklas, katalog, paczka, typ):
    alldata = read_ppe_file(ppe)
    slownikOBIS = czytajOBIS(plikklas)
    data = []
    k = 0
    count = 0
    threadnum = 6

    threads = []
    for l in alldata:
        data.append(l)
        count += 1

        if count >= paczka:
            k += 1
            thread = threading.Thread(target=save_to_file,
                                      args=(koperta(data, slownikOBIS, typ, None), k, katalog, today.date(), typ))
            threads.append(thread)
            thread.start()
            count = 0
            data = []

        while len(threads) >= threadnum:
            for t in threads:
                if not t.is_alive():
                    threads.remove(t)

    if data:
        k += 1
        thread = threading.Thread(target=save_to_file,
                                  args=(koperta(data, slownikOBIS, typ, None), k, katalog, today.date(), typ))
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()



class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


parser = MyParser()
subparsers = parser.add_subparsers(dest='subcommand')
subparsers.required = True

parser_ppe = subparsers.add_parser('generuj-ppe')

parser_ppe.add_argument(
    '-i',
    required=True,
    dest='plik_konfig',
    help='Nazwa pliku konfiguracyjnego'
)
parser_ppe.add_argument(
    '-s',
    default='profil_standardowy.xlsx',
    required=False,
    dest='plik_profil',
    help='Nazwa pliku z profilem standardowym, domyslnie profil_standardowy.xlsx'
)
parser_ppe.add_argument(
    '-o',
    required=True,
    dest='plik_wynikowy',
    help='Nazwa pliku wynikowego'
)

parser_6_1_1_5 = subparsers.add_parser('generuj-6.1.1.5')

parser_6_1_1_5.add_argument(
    '-i',
    default='ppe.csv',
    required=False,
    dest='plik_ppe',
    help='Nazwa pliku z ppe, domyslnie ppe.csv'
)
parser_6_1_1_5.add_argument(
    '-s',
    default='profil_standardowy.xlsx',
    required=False,
    dest='plik_profil',
    help='Nazwa pliku z profilem standardowym, domyslnie profil_standardowy.xlsx'
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

parser_6_1_1_1 = subparsers.add_parser('generuj-6.1.1.1')
parser_6_1_1_1.add_argument(
    '-i',
    default='ppe.csv',
    required=False,
    dest='plik_ppe',
    help='Nazwa pliku z ppe, domyslnie ppe.csv'
)
parser_6_1_1_1.add_argument(
    '-s',
    default='profil_standardowy.xlsx',
    required=False,
    dest='plik_profil',
    help='Nazwa pliku z profilem standardowym, domyslnie profil_standardowy.xlsx'
)
parser_6_1_1_1.add_argument(
    '-o',
    required=True,
    dest='katalog_wynikowy',
    help='Sciezka do katalogu wynikowego'
)
parser_6_1_1_1.add_argument(
    '-d',
    required=True,
    dest='doba',
    help='Doba w formacie RRRRMMDD'
)
parser_6_1_1_1.add_argument(
    '-p',
    required=False,
    default=1000,
    dest='paczka',
    help='Wielkosc paczki, domyslnie 1000'
)

parser_7_1_1_4 = subparsers.add_parser('generuj-7.1.1.4')
parser_7_1_1_4.add_argument(
    '-i',
    default='ppe.csv',
    required=False,
    dest='plik_ppe',
    help='Nazwa pliku z ppe, domyslnie ppe.csv'
)
parser_7_1_1_4.add_argument(
    '-s',
    default='profil_standardowy.xlsx',
    required=False,
    dest='plik_profil',
    help='Nazwa pliku z profilem standardowym, domyslnie profil_standardowy.xlsx'
)
parser_7_1_1_4.add_argument(
    '-o',
    required=True,
    dest='katalog_wynikowy',
    help='Sciezka do katalogu wynikowego'
)
parser_7_1_1_4.add_argument(
    '-d',
    required=True,
    dest='doba',
    help='Doba w formacie RRRRMMDD'
)
parser_7_1_1_4.add_argument(
    '-p',
    required=False,
    default=1000,
    dest='paczka',
    help='Wielkosc paczki, domyslnie 1000'
)

parser_6_2_1_1 = subparsers.add_parser('generuj-6.2.1.1')
parser_6_2_1_1.add_argument(
    '-i',
    default='ppe.csv',
    required=False,
    dest='plik_ppe',
    help='Nazwa pliku z ppe, domyslnie ppe.csv'
)
parser_6_2_1_1.add_argument(
    '-s',
    required=True,
    dest='plik_konfig',
    help='Nazwa pliku konfiguracyjnego'
)
parser_6_2_1_1.add_argument(
    '-o',
    required=True,
    dest='katalog_wynikowy',
    help='Sciezka do katalogu wynikowego'
)
parser_6_2_1_1.add_argument(
    '-p',
    required=False,
    default=1000,
    dest='paczka',
    help='Wielkosc paczki, domyslnie 1000'
)

parser_walid = subparsers.add_parser('waliduj')
parser_walid.add_argument(
    '-i',
    required=True,
    dest='plik',
    help='Nazwa pliku do walidacji'
)
parser_walid.add_argument(
    '-o',
    required=False,
    dest='plik_wynikowy',
    help='Nazwa pliku wynikowego'
)

parser_dkolejki = subparsers.add_parser('do-kolejki')
parser_dkolejki.add_argument(
    '-i',
    required=True,
    dest='katalog',
    help='Sciezka do katalogu z plikami'
)
parser_dkolejki.add_argument(
    '-s',
    required=True,
    dest='plik_konfig',
    help='Sciezka do pliku konfiguracyjnego'
)
parser_dkolejki.add_argument(
    '-n',
    required=False,default=4,
    dest="liczba_watkow",
    help='Liczba watkow, domyslnie 4'
)

parser_zkolejki = subparsers.add_parser('z-kolejki')
parser_zkolejki.add_argument(
    '-s',
    required=True,
    dest='plik_konfig',
    help='Sciezka do pliku konfiguracyjnego'
)
parser_zkolejki.add_argument(
    '-q',
    required=True,
    dest='kolejka',
    help='Adres kolejki'
)
parser_zkolejki.add_argument(
    '-o',
    required=True,
    dest='katalog',
    help='Sciezka do katalogu wynikowego'
)

args = parser.parse_args()

if args.subcommand == 'generuj-ppe':
    print('plik konfiguracyjny: %s plik wynikowy: %s profil standardowy: %s' % (
    args.plik_konfig, args.plik_wynikowy, args.plik_profil))
    generatePPE(args.plik_konfig, args.plik_profil, args.plik_wynikowy)

if args.subcommand == 'generuj-6.1.1.5':
    print('ppe: %s profil standardowy: %s katalog: %s doba: %s paczka: %s' % (
    args.plik_ppe, args.plik_profil, args.katalog_wynikowy, args.doba, args.paczka))
    generuj_profile(args.plik_ppe, args.plik_profil, args.katalog_wynikowy, args.doba, args.paczka, "6.1.1.5")
if args.subcommand == 'generuj-6.1.1.1':
    print('ppe: %s profil standardowy: %s katalog: %s doba: %s paczka: %s' % (
    args.plik_ppe, args.plik_profil, args.katalog_wynikowy, args.doba, args.paczka))
    generuj_profile(args.plik_ppe, args.plik_profil, args.katalog_wynikowy, args.doba, args.paczka, "6.1.1.1")
if args.subcommand == 'generuj-7.1.1.4':
    print('ppe: %s profil standardowy: %s katalog: %s doba: %s paczka: %s' % (
    args.plik_ppe, args.plik_profil, args.katalog_wynikowy, args.doba, args.paczka))
    generuj_profile(args.plik_ppe, args.plik_profil, args.katalog_wynikowy, args.doba, args.paczka, "7.1.1.4")
if args.subcommand == 'generuj-6.2.1.1':
    print('ppe: %s plik konfiguracyjny: %s katalog: %s paczka: %s' % (
    args.plik_ppe, args.plik_konfig, args.katalog_wynikowy, args.paczka))
    generuj_wskazania(args.plik_ppe, args.plik_konfig, args.katalog_wynikowy, args.paczka, "6.2.1.1")

if args.subcommand == 'do-kolejki':
    print('katalog: %s plik konfiguracyjny: %s liczba watkow: %s' % (args.katalog, args.plik_konfig,args.liczba_watkow))
    config = load_config(args.plik_konfig)
    init_logging('log.txt')
    num_threads = args.liczba_watkow
    folder = args.katalog
    files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(send_file_to_queue, config, file): file for file in files[:num_threads]}
        logging.info(futures)

        for file in files[num_threads:]:
            done, _ = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
            for future in done:
                futures.pop(future)
            futures[executor.submit(send_file_to_queue, config, file)] = file

if args.subcommand == 'z-kolejki':
    print('kolejka: %s katalog wynikowy: %s plik konfiguracyjny: %s' % (args.kolejka,args.katalog, args.plik_konfig))
    config = load_config(args.plik_konfig)
    init_logging('log.txt')
    que_address= args.kolejka
    folder = args.katalog
    get_messages_from_queue(args.kolejka, config, folder)



if args.subcommand == 'waliduj':
    if isdir(args.plik):
        if args.plik_wynikowy is None:
            for filename in listdir(args.plik):
                pathname = args.plik + "/" + filename
                validate(pathname)
        else:
            for filename in listdir(args.plik):
                pathname = args.plik + "/" + filename
                with open(args.plik_wynikowy, 'a') as f:
                    with redirect_stdout(f):
                        validate(pathname)
    else:
        if args.plik_wynikowy is None:
            validate(args.plik)
        else:
            with open(args.plik_wynikowy, 'a') as f:
                with redirect_stdout(f):
                    validate(args.plik)