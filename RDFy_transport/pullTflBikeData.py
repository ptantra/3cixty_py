'''A python script converting raw bicycle data from the TFL api into RDF. Outputs as a turtle file.
Workfklow: API -> JSON -> CSV -> RDF -> TTL'''

import urllib, json, csv, uuid, time, re
from rdflib import URIRef, Literal, Namespace, plugin, Graph, ConjunctiveGraph
from rdflib.store import Store
from collections import defaultdict


pathf = "/Users/patrick/3cixty/IN/tfl/"

def apiJsonCsv(url):
    response = urllib.urlopen(url)
    x = json.load(response)

    f = csv.writer(open("/Users/patrick/3cixty/IN/tfl/londonBikes.csv", "wb+"))
    f.writerow(["id",
                "url",
                "commonName",
                "placeType",
                "bikePointsNo",
                "timeModified"
                "nFilledDocks",
                "nEmptyDocks",
                "nTotalDocks",
                "lat",
                "lon"])

    for x in x:
        f.writerow([x["id"],
                    x["url"],
                    x["commonName"],
                    x["placeType"],
                    x["additionalProperties"][0]['value'],
                    x["additionalProperties"][0]['modified'],
                    x["additionalProperties"][6]['value'],
                    x["additionalProperties"][7]['value'],
                    x["additionalProperties"][8]['value'],
                    x["lat"],
                    x["lon"]])

    return x


def readCsv(inputCsv):
    try:
        f = open(inputCsv, 'rU');
        rf = csv.reader(f, delimiter=',');
        return rf;
    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
        raise

def getBikeData(row):
    id = row[0]
    url= row[1]
    commonName = row[2]
    placeType = row[3]
    bikePointsNo = row[4]
    timeModified = row[5]
    nFilledDocks = row[6]
    nEmptyDocks = row[7]
    nTotalDocks = row[8]
    lat=row[9]
    lon=row[10]

    lst = [id,
           url,
           commonName,
           placeType,
           bikePointsNo,
           timeModified,
           nFilledDocks,
           nEmptyDocks,
           nTotalDocks,
           lat,
           lon]
    return lst


def definePrefixes():

#Vocabularies   -- THIS SHOULD BE A CONSTRUCTED BASED ON THE A DICTONARY DEFINITION
    prefixes = {'dc': 'http://purl.org/dc/elements/1.1/',
                'dcterms':'http://purl.org/dc/terms/',
                'dul': 'http://ontologydesignpatterns.org/ont/dul/DUL.owl#',
                'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
                'geom': 'http://geovocab.org/geometry#',
                'geosparql': 'http://www.opengis.net/ont/geosparql#','locationOnt': 'http://data.linkedevents.org/def/location#',
                'locn': 'http://www.w3.org/ns/locn#',
                'owl':'http://www.w3.org/2002/07/owl#',
                'locn': 'http://www.w3.org/ns/locn#',
                'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                'naptan':'http://transport.data.gov.uk/def/naptan/',
                'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
                'schema':'http://schema.org/',
                'vcard': 'http://www.w3.org/2006/vcard/ns#',
                'xsd': 'http://www.w3.org/2001/XMLSchema#'}
    return prefixes

def bindingPrefixes(graphs,prefixes):
    for key in prefixes:
        graphs.bind(key, prefixes[key])
    return graphs

def createBikeGraph(arg, g):

    nspaces = readDict()

    schema = Namespace(nspaces.get('schema'))
    naptan = Namespace(nspaces.get('naptan'))
    owl = Namespace(nspaces.get('owl'))
    xsd = Namespace(nspaces.get('xsd'))
    rdfs = Namespace(nspaces.get('rdfs'))
    vcard = Namespace(nspaces.get('vcard'))
    locationOnt = Namespace(nspaces.get('locationOnt'))
    geom = Namespace(nspaces.get('geom'))
    geo = Namespace(nspaces.get('geo'))
    geosparql = Namespace(nspaces.get('geosparql'))
    rdf = Namespace(nspaces.get('rdf'))
    dcterms = Namespace(nspaces.get('dcterms'))
    dul = Namespace(nspaces.get('dul'))
    locn = Namespace(nspaces.get('locn'))
    dc = Namespace(nspaces.get('dc'))

    bikeid = arg[0].split('_')[1].encode('utf-8')
    bikeGUID = getUid(bikeid, naptan)

    bikeLat, bikeLong = float(arg[8]), float(arg[9])
    bikeLats = str('{:f}'.format(bikeLat))
    bikeLongs = str('{:f}'.format(bikeLong))
    nTotalDocks = str(arg[7].encode('utf-8'))

    address = arg[2].split(',')
    bikeLabel = address[len(address) - 1].lstrip() + ' ' + str(bikeid)


    bikeGeometry = "POINT (" + str(bikeLat) + " " + str(bikeLong) + ")"
    bikeAddress = Literal(re.sub(r'&(?![A-Za-z]+[0-9]*;|#[0-9]+;|#x[0-9a-fA-F]+;)', r'and',arg[2]))
    bikeAddressSplit = Literal(bikeAddress.split(',', 1)[-1])
    bikeAddressLocality = Literal(bikeAddressSplit.replace(' ', '',1))
    bikeCreatedDate = arg[5]

    singleBike = createBikeParkID(bikeGUID)
    singleAddress = createAddress(bikeGUID)
    singleGeometry = createGeometry(bikeGUID)
    bikePublisher = URIRef('https://api.tfl.gov.uk/#BikePoint')
    bikeBusinessType = URIRef('http://data.linkedevents.org/kos/3cixty/bikestation')



    g.add((singleBike, rdf.type, dul.Place))
    g.add((singleBike, rdf.type, locationOnt.bikePark))
    g.add((singleBike, dcterms.identifier, Literal(bikeLabel)))
    g.add((singleBike, dcterms.description, Literal("London TFL Bike hire docks")))
    g.add((singleBike, schema.dateCreated, Literal(bikeCreatedDate, datatype=xsd.dateTime)))
    g.add((singleBike, locationOnt.nTotalDocks, Literal(nTotalDocks, datatype=xsd.int)))
    g.add((singleBike, dc.publisher, bikePublisher))
    g.add((singleBike, locationOnt.businessType, bikeBusinessType))

    g.add((singleBike, geom.geometry, singleGeometry))
    g.add((singleBike, schema.geo, singleGeometry))
    g.add((singleBike, geosparql.hasGeometry, singleGeometry))
    g.add((singleBike, locn.geometry, singleGeometry))

    g.add((singleBike, vcard.hasAddress, singleAddress))
    g.add((singleBike, locn.addresss, singleAddress))
    g.add((singleBike, schema.location, singleAddress))



    g.add((singleGeometry, rdf.type, geosparql.hasGeometry))
    g.add((singleGeometry, rdf.type, geom.geometry))
    g.add((singleGeometry, rdf.type, locn.geometry))
    g.add((singleGeometry, rdf.type, schema.geo))
    g.add((singleGeometry, geo.geometry, Literal(bikeGeometry, datatype=geosparql.wktLiteral)))
    g.add((singleGeometry, geo.lat, Literal(bikeLats, datatype=xsd.double)))
    g.add((singleGeometry, geo.long, Literal(bikeLongs, datatype=xsd.double)))
    g.add((singleGeometry, schema.latitude, Literal(bikeLats, datatype=xsd.double)))
    g.add((singleGeometry, schema.longitude, Literal(bikeLongs, datatype=xsd.double)))




    g.add((singleAddress, rdf.type, locn.address))
    g.add((singleAddress, rdf.type, schema.location))
    g.add((singleAddress, rdf.type, vcard.hasAddress))
    g.add((singleAddress, dcterms.title, bikeAddress))
    g.add((singleAddress, schema.streetAddress, bikeAddress))
    g.add((singleAddress, locn.address, bikeAddress))
    g.add((singleAddress, vcard.street_address, bikeAddress))
    g.add((singleAddress, schema.addressLocality, bikeAddressLocality))

    return g


def getUid(s, n):
    idencode = s.encode('utf-8')
    uid = uuid.uuid5(n, idencode)
    return uid

def readDict(): #needed?
    dict = defaultdict(list)
    with open(pathf + 'dictionary_bikes.csv','rb') as f:
        r = csv.DictReader(f)
        for row in r:
            for (k,v) in row.items():
                dict[k]=v
    f.close()
    return dict

import uuid


def createBikeParkID(bikeGUID):
    singlePark = URIRef("http://data.linkedevents.org/location/%s" % bikeGUID)
    return singlePark


def createGeometry(bikeGUID):
    singleGeometry = URIRef(('http://data.linkedevents.org/location/%s/geometry') % bikeGUID)
    return singleGeometry


def createAddress(bikeGUID):
    singleAddress = URIRef(('http://data.linkedevents.org/london/%s/address') % bikeGUID)
    return singleAddress


def main():

    url="https://api.tfl.gov.uk/BikePoint?app_id=5ee709d5&app_key=1739d498d997e956a2b80c62a8948ff0" #url for bike api
    apiJsonCsv(url) #json to csv conversion
    #inputCsv = pathf + "test.csv"
    inputCsv = pathf + "londonBikes.csv"
    outFile = pathf + "londonBikes.ttl"

    csvBike = readCsv(inputCsv) #create object from the resulting csv file

    next(csvBike) #skips the header

    bike_store = plugin.get('IOMemory', Store)()
    bike_g = Graph(bike_store)
    prefixes = definePrefixes()

    print('Binding Prefixes')
    bindingPrefixes(bike_g, prefixes)

    print('Creating graph-bike...')

    for row in csvBike: #loop through individual rows in the csv file **KEY**
        lstData= getBikeData(row)#activates the getBikeData() function **KEY**
        createBikeGraph(lstData, bike_g).serialize(outFile, format='turtle')

    print ('Done!!')


if __name__ == "__main__":
    main();



'''
url = "https://api.tfl.gov.uk/BikePoint?app_id=5ee709d5&app_key=1739d498d997e956a2b80c62a8948ff0"
response = urllib.urlopen(url)
x = json.load(response)


f = csv.writer(open("/Users/patrick/3cixty/IN/tfl/test.csv", "wb+"))
f.writerow(["id",
            "url",
            "commonName",
            "placeType",
            "bikePointsNo",
            "nFilledDocks",
            "nEmptyDocks",
            "nTotalDocks",
            "lat",
            "lon"])

for x in x:
    f.writerow([x["id"],
                x["url"],
                x["commonName"],
                x["placeType"],
                x["additionalProperties"][0]['value'],
                x["additionalProperties"][6]['value'],
                x["additionalProperties"][7]['value'],
                x["additionalProperties"][8]['value'],
                x["lat"],
                x["lon"]])

'''
