import csv
import uuid
import pyproj
import random
from random import seed
import string
from rdflib import URIRef, Literal, Namespace, plugin, Graph, BNode
from rdflib.store import Store
import time

start_time = time.time()

def readCsv(inputfile):
    try:
        f = open(inputfile, 'rU')
        rf = csv.reader(f, delimiter=';')
        return rf
    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
        raise

def getUid(r0):#use this script to create NON-COMPLIANT uuid
    hotelUri = Namespace("http://data.linkedevents.org/places/London/hotels")
    idencode = r0.encode('utf-8')
    uid = uuid.uuid5(hotelUri, idencode)
    return uid

def definePrefixes():
    prefixes = {'schema': 'http://schema.org/',
                'owl': 'http://www.w3.org/2002/07/owl#',
                'xsd': 'http://www.w3.org/2001/XMLSchema#',
                'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
                'locationOnt': 'http://data.linkedevents.org/def/location#',
                'locationRes': 'http://data.linkedevents.org/location/',
                'geom': 'http://geovocab.org/geometry#',
                'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
                'gsp': 'http://www.opengis.net/ont/geosparql#',
                'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                'dcterms': 'http://purl.org/dc/terms/',
                'dul': 'http://ontologydesignpatterns.org/ont/dul/DUL.owl#',
                'locn': 'http://www.w3.org/ns/locn#',
                'foaf': 'http://xmlns.com/foaf/0.1/',
                'dc': 'http://purl.org/dc/elements/1.1/',
                #'time': 'http://www.w3.org/2006/time#',
                'acco': 'http://purl.org/acco/ns#',
                'gr': 'http://purl.org/goodrelations/v1#',
                'envo': 'http://purl.obolibrary.org/obo/#',
                'time':'http://www.w3.org/TR/owl-time#',
                'gn':'http://www.geonames.org/ontology/#'}
    return prefixes

def bindingPrefixes(g, prefixes):
    for key in prefixes:
        g.bind(key, prefixes[key])
    return g

def createAirQualityId(airQualId):
    airQualId = URIRef('http://data.linkedevents.org/places/London/environment/' + airQualId)
    return airQualId

def createArea():
    area = URIRef('http://data.linkedevents.org/environment/London/area/' + Literal())
    return area

def createAreaGeom():
    areaGeom = URIRef(createArea() + '/geometry')
    return areaGeom

def getAirQualData(row):
    airQualId = row[0]
    airQualGUID = getUid(row[0])
    airQualTitle = Literal(str(row[1]))
    airQualSpatial= row[2]
    airQualIndustryCommercial = row[3]
    airQualDomestic = row[4]
    airQualTransport = row[5]
    airQualNetEmission = row[6]
    airQualTotal = row[7]
    population = row[8]
    airQualPublisher = URIRef('http://data.london.gov.uk/dataset/carbon-dioxide-emissions-borough/resource/33dbca4d-d8d9-45cb-ac14-3ebcac3ed65b')

    lst = [airQualId, airQualGUID, airQualTitle, airQualSpatial,
           airQualIndustryCommercial, airQualDomestic, airQualTransport,
           airQualNetEmission, airQualTotal, population,
           airQualPublisher]
    return lst

def createAirQualGraph(arg, g):
    schema = Namespace("http://schema.org/")
    xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
    rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    locationOnt = Namespace("http://data.linkedevents.org/def/location#")
    geo = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
    gs = Namespace("http://www.opengis.net/ont/geosparql#")
    locn = Namespace("http://www.w3.org/ns/locn#")
    dc = Namespace("http://purl.org/dc/elements/1.1/")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    acco = Namespace("http://purl.org/acco/ns#")
    gr = Namespace('http://purl.org/goodrelations/v1#')
    foaf = Namespace('http://xmlns.com/foaf/0.1/')
    dcterms = Namespace('http://purl.org/dc/terms/')
    dul = Namespace('http://ontologydesignpatterns.org/ont/dul/DUL.owl#')
    envo = Namespace('http://purl.obolibrary.org/obo/#')
    time = Namespace('http://www.w3.org/TR/owl-time#')
    gn= Namespace('http://www.geonames.org/ontology/#')

    #area = createArea()
    area = URIRef('http://data.linkedevents.org/places/London/area/' + Literal(arg[0]))
    #geom = createAreaGeom()
    geom = URIRef('http://data.linkedevents.org/places/London/area/' + Literal(arg[0])) +'/geometry'
    measureIndCom = URIRef("http://data.linkedevents.org/location/airquality/" + "%s" + "/industryCommercial") % arg[0]
    measureDom = URIRef("http://data.linkedevents.org/location/airquality/" + "%s" + "/domestic") % arg[0]
    measureTrans = URIRef("http://data.linkedevents.org/location/airquality/" + "%s" + "/transport") % arg[0]
    measureNetEmis = URIRef("http://data.linkedevents.org/location/airquality/" + "%s" + "/netEmission") % arg[0]
    measureTotal = URIRef("http://data.linkedevents.org/location/airquality/" + "%s" + "/emissionTotal") % arg[0]
    measurePop = URIRef("http://data.linkedevents.org/location/airquality/" + "%s" + "/population") % arg[0]
    measurePerCapEmis = URIRef("http://data.linkedevents.org/location/airquality/" + "%s" + "/perCapitaEmission") % arg[0]

    g.add((area, rdf.type, schema.AdministrativeArea))
    g.add((area, rdf.type, dul.Place))
    g.add((area, rdf.type, schema.Place))
    g.add((area, rdfs.label, Literal(arg[2])))
    g.add((area, dcterms.identifier, Literal(arg[0])))
    g.add((area, dcterms.publisher, Literal(arg[10])))
    g.add((area, geo.location, geom))
    g.add((area, envo.EnvironmentalMaterial, measureIndCom))
    g.add((area, envo.EnvironmentalMaterial, measureDom))
    g.add((area, envo.EnvironmentalMaterial, measureTrans))
    g.add((area, envo.EnvironmentalMaterial, measureNetEmis))
    g.add((area, envo.EnvironmentalMaterial, measureTotal))
    g.add((area, gn.population, measurePop))
    g.add((area, envo.EnvironmentalMaterial, measurePerCapEmis))

    g.add((geom, rdf.type, geo.Multipolygon))
    g.add((geom, locn.geometry, Literal(arg[3], datatype=xsd.wktliteral)))

    g.add((measureIndCom, rdf.type, envo.EnvironmentalMaterial))
    g.add((measureIndCom, rdfs.comment, Literal('CO2 measured in kiloton (kt)')))
    g.add((measureIndCom, time.instance, Literal('2013', datatype=xsd.gYear)))
    g.add((measureIndCom, dcterms.description, Literal('Industry and Commercial')))
    g.add((measureIndCom, envo.AtmosphericCarbonDioxide, Literal(arg[4], datatype=xsd.decimal)))

    g.add((measureDom, rdf.type, envo.EnvironmentalMaterial))
    g.add((measureDom, rdfs.comment, Literal('CO2 measured in kiloton (kt)')))
    g.add((measureDom, time.instance, Literal('2013', datatype=xsd.gYear)))
    g.add((measureDom, dcterms.description, Literal('Domestic')))
    g.add((measureDom, envo.AtmosphericCarbonDioxide, Literal(arg[5], datatype=xsd.decimal)))

    g.add((measureTrans, rdf.type, envo.EnvironmentalMaterial))
    g.add((measureTrans, rdfs.comment, Literal('CO2 measured in kiloton (kt)')))
    g.add((measureTrans, time.instance, Literal('2013', datatype=xsd.gYear)))
    g.add((measureTrans, dcterms.description, Literal('Transport')))
    g.add((measureTrans, envo.AtmosphericCarbonDioxide, Literal(arg[6], datatype=xsd.decimal)))

    g.add((measureNetEmis, rdf.type, envo.EnvironmentalMaterial))
    g.add((measureNetEmis, rdfs.comment, Literal('CO2 measured in kiloton (kt)')))
    g.add((measureNetEmis, time.instance, Literal('2013', datatype=xsd.gYear)))
    g.add((measureNetEmis, dcterms.description, Literal('Net Emission')))
    g.add((measureNetEmis, envo.AtmosphericCarbonDioxide, Literal(arg[7], datatype=xsd.decimal)))

    g.add((measureTotal, rdf.type, envo.EnvironmentalMaterial))
    g.add((measureTotal, rdfs.comment, Literal('CO2 measured in kiloton (kt)')))
    g.add((measureTotal, time.instance, Literal('2013', datatype=xsd.gYear)))
    g.add((measureTotal, dcterms.description, Literal('Emission Grand Total')))
    g.add((measureTotal, envo.AtmosphericCarbonDioxide, Literal(arg[8], datatype=xsd.decimal)))

    g.add((measurePop, rdf.type, gn.feature))
    g.add((measurePop, rdfs.comment, Literal('mid year estimate of population')))
    g.add((measurePop, time.instance, Literal('2013', datatype=xsd.gYear)))
    g.add((measurePop, dcterms.description, Literal('Population')))
    g.add((measurePop, gn.population, Literal((arg[9]), datatype=xsd.double)))

    prefixes=definePrefixes()
    bindingPrefixes(g, prefixes)

    return g

def main():
    pathf = "/Users/patrick/3cixty/IN/London DataStore/151124/"
    inFile = pathf + "airquality2013merge.csv"
    outFile = pathf + "airquality2013merge.ttl"

    csv = readCsv(inFile)
    next(csv, None)  # FILE WITH HEADERS

    store = plugin.get('IOMemory', Store)()
    g = Graph(store)

    prefixes = definePrefixes()
    print('Binding Prefixes')
    bindingPrefixes(g, prefixes)

    print('Creating graph-air quality...')

    for row in csv:
        lstData = getAirQualData(row)
        createAirQualGraph(lstData, g).serialize(outFile, format='turtle')

    print ('DONE! Time elapsed ' + str((time.time() - start_time)))

if __name__ == "__main__":
    main()
