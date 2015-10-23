__author__ = 'patrick'

import csv
import uuid
import pyproj
from rdflib import URIRef, Literal, Namespace, plugin, Graph, ConjunctiveGraph
from rdflib.store import Store
from collections import defaultdict

 # initialise graph variable, read dictionary and bing prefixes
def __init__(self):
    store = plugin.get('IOMemory', Store)()
    self.g=Graph(store)
    prefixes=self.readDict()
    self.bindingPrefixes(prefixes)

def readCsv(inputfile):
    try:
        f=open(inputfile);
        rf=csv.reader(f,delimiter=',');
        return rf;
    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
        raise

def readDict(self):
    dict = defaultdict(list)
    with open('dictionary.csv','rb') as f:
        r = csv.DictReader(f)
        for row in r:
            for (k,v) in row.items():
                dict[k]=v
    f.close()
    return dict

def getUid(self,s,n):
    idencode=s.encode('utf-8')
    uid=uuid.uuid5(n, idencode)
    return uid

def convertProj(self,lon,lat):
    Bng = pyproj.Proj(init='epsg:27700')
    Wgs84 = pyproj.Proj(init='epsg:4326')
    wgsLon,wgsLat = pyproj.transform(Bng,Wgs84,lon, lat)
    return wgsLon,wgsLat

def writeDict(self,prefixes):
    with open('dictionary.csv','wb') as f:
        w = csv.writer(f)
        w.writerow(prefixes.keys())
        w.writerow(prefixes.values())
    f.close()

def bindingPrefixes(self,prefixes):
    for key in prefixes:
        self.g.bind(key, prefixes[key])

def getTrainData(row): #amended

    #naptan = Namespace("http://transport.data.gov.uk/def/naptan/")
    #uid=uuid.uuid5(naptan, idencode)
    #idencode=row[0].encode('utf-8')
    objectID  = row[1]
    uid=getUid(row[0])

    stopLat=''
    stopLong=''
    try:
        stopLat,stopLong=ConvertProj(row[4],row[5])
    except TypeError as e:
        print ("wrong lat, long -".format(e))

    noAddress=""
    stopid = objectID
    stopGeometry = "POINT ("+str(stopLat) +" "+str(stopLong)+")"
    stopRoute = URIRef('http://data.linkedevents.org/transit/London/route/')
    stopGUID = uid
    #stopTitle = Literal(str(row[3]))
    #stopAddress = Literal(noAddress)
    #stopLocnAddress = Literal(noAddress)
    #stopAddressLocality = Literal('London')
    #stopAdminUnitL2 = Literal('London')
    #stopPublisher = URIRef('https://tfl.gov.uk/modes/buses/')
    stopBusinessType = URIRef('http://data.linkedevents.org/kos/3cixty/busstop')
    #stopLabel = Literal('Station name- '+str(row[3])) #amended to suit

    #lst = [stopid, stopLat, stopLong, stopGeometry, stopRoute, stopGUID, stopTitle, stopAddress, stopLocnAddress,\
    #       stopAddressLocality, stopAdminUnitL2, stopPublisher, stopBusinessType, stopLabel]
    lst = [stopid, stopLat, stopLong, stopGeometry, stopRoute, stopGUID]
    return lst


def createTrainStop(self,stopId):
    singleStop = URIRef("http://data.linkedevents.org/transit/London/station/" + stopId)
    return singleStop


def createGeometry(self, stopsGUID):
    singleGeometry = URIRef(('http://data.linkedevents.org/location/%s/geometry') % stopsGUID)
    return singleGeometry

def createAddress(self, stopsGUID):
    singleAddress = URIRef(('http://data.linkedevents.org/location/%s/address') % stopsGUID)
    return singleAddress

def writeRDF(self,outputfile):
     self.g.serialize(outputfile,format='turtle')

def creatRDF(self,row):

    nspaces=self.readDict()

    schema = Namespace(nspaces.get('schema'))
    rdf = Namespace(nspaces.get('rdf'))
    naptan = Namespace(nspaces.get('naptan'))
    #dc = Namespace(nspaces.get('dc'))
    geo = Namespace(nspaces.get('geo'))
    #geosparql = Namespace(nspaces.get('geosparql'))
    #geom = Namespace(nspaces.get('geom'))
    xsd = Namespace(nspaces.get('xsd'))
    transit = Namespace(nspaces.get('transit'))
    #dcterms = Namespace(nspaces.get('dcterms'))
    dul = Namespace(nspaces.get('dul'))
    locn = Namespace(nspaces.get('locn'))
    #locationOnt = Namespace(nspaces.get('locationOnt'))
    #rdfs = Namespace(nspaces.get('rdfs'))

    stopid  = row[1]
    uid=self.getUid(row[0],naptan)

    stopLat,stopLong=convertProj(row[5],row[6]) ##COLUMN MUMBERS UPDATED TO SUIT###
    #stopLat,stopLong=convertProj(row[4],row[5])

    noAddress=""
    stopGeometry = "POINT ("+str(stopLat) +" "+str(stopLong)+")"
    stopRoute = URIRef('http://data.linkedevents.org/transit/London/station/')
    stopRouteService = URIRef('http://data.linkedevents.org/transit/London/routeService/') ##NEW OBJECT##
    stopGUID = uid
    #stopTitle = Literal(str(row[3]))
    #stopAddress = Literal(noAddress)
    #stopLocnAddress = Literal(noAddress)
    #stopAddressLocality = Literal('London')
    #stopAdminUnitL2 = Literal('London')
    #stopPublisher = URIRef('https://tfl.gov.uk/modes/buses/')
    #stopBusinessType = URIRef('http://data.linkedevents.org/kos/3cixty/busstop')
    #stopLabel = Literal('Bus Stop - '+str(row[3]))

    singleStop = self.createTrainStop(stopid)
    singleAddress = self.createAddress(stopGUID)
    singleGeometry = self.createGeometry(stopGUID)

    self.g.add((singleStop, rdf.type, naptan.Station))
    self.g.add((singleStop, rdf.type, transit.Station))
    self.g.add((singleStop, rdf.type, dul.Place))
    #self.g.add((singleStop, dc.identifier, Literal(stopid)))
    #self.g.add((singleStop, geom.geometry, singleGeometry))
    #self.g.add((singleStop, schema.geo, singleGeometry))
    #self.g.add((singleAddress, rdf.type, schema.PostalAddress))
    #self.g.add((singleAddress, rdf.type, dcterms.Location))
    #self.g.add((singleAddress, dcterms.title, stopTitle))
    #self.g.add((singleAddress, schema.streetAddress, stopAddress))
    #self.g.add((singleAddress, locn.address, stopLocnAddress))
    #self.g.add((singleAddress, schema.addressLocality, stopAddressLocality))
    #self.g.add((singleAddress, locn.adminUnitL12, stopAdminUnitL2))
    self.g.add((singleGeometry, rdf.type, geo.Point))
    self.g.add((singleGeometry, geo.lat, Literal(stopLat, datatype=xsd.double)))
    self.g.add((singleGeometry, geo.long, Literal(stopLong, datatype=xsd.double)))
    self.g.add((singleGeometry, locn.geometry, Literal(stopGeometry, datatype=geosparql.wktLiteral)))
    self.g.add((singleStop, geo.location, singleGeometry))
    self.g.add((singleStop, transit.route, stopRoute))
    self.g.add((singleStop, transit.routeService, stopRouteService)) ##NEW PREDICATE##
    self.g.add((singleStop, schema.name, singleAddress))
    ##??DELETE??##self.g.add((singleBranch, transit.route, stopRoute))
    #self.g.add((singleStop, locn.address, singleAddress))
    #self.g.add((singleStop, dc.publisher, stopPublisher))
    #self.g.add((singleStop, locationOnt.businessType, stopBusinessType))
    #self.g.add((singleStop, rdfs.label, stopLabel))
    return self

def main():
    #root = tk.Tk()
    #root.withdraw()
    #inFile = filedialog.askopenfilename()
    pathf="/Users/patrick/3cixty/IN/open data sources"
    inFileB = pathf+"RailReferences_Naptan_151022.csv" ###specify file
    outFileB=pathf+"train_stations.ttl"
    #inFileBR = pathf+"busline_content.csv"
    #outFileBR=pathf+"busR.ttl"
    #inFileBC = pathf+"buscorrespondence.csv"
    #outFileBC=pathf+"busC.ttl"

    csvB=readCsv(inFileB)
    #csvBR=readCsv(inFileBR)
    #csvBC=readCsv(inFileBC)


    next(csvB, None)  #FILE WITH HEADERS
    #next(csvBR, None)  #FILE WITH HEADERS
    #next(csvBC, None)  #FILE WITH HEADERS

    store = plugin.get('IOMemory', Store)()
    g = Graph(store)
    graph = ConjunctiveGraph(store)
    #busline_store = plugin.get('IOMemory', Store)()
    #busline_g= Graph(busline_store)
    #busline_graph = ConjunctiveGraph(busline_store)
    #busC_store = plugin.get('IOMemory', Store)()
    #busC_g= Graph(busC_store)
    #busC_graph = ConjunctiveGraph(busC_store)


    prefixes=definePrefixes()
    print('Binding Prefixes')
    bindingPrefixes(graph,prefixes)
    #bindingPrefixes(busline_graph,prefixes)
    #bindingPrefixes(busC_graph,prefixes)

    print('Creating graph-Train...') #amended
    for row in csvB:
        lstData = getTrainData(row)
        createBusGraph(lstData,g)
    createBusGraph(lstData,g).serialize(outFileB,format='turtle')

 # print('Creating graph-BusR...')
 # for row in csvBR:
 #     lstData = getBusLineData(row)
 #     createBuslineGraph(lstData,busline_g)
 # createBuslineGraph(lstData,busline_g).serialize(outFileBR,format='turtle')

 # print('Creating graph-BusC...')
 # for row in csvBR:
    #    lstData = getBusCData(row)
    #    createBusCGraph(lstData,busC_g)
    # createBusCGraph(lstData,busC_g).serialize(outFileBC,format='turtle')
    #nzip = pathf+time.strftime("%Y-%m-%d")+'.zip'
    # nzipB = pathf+outFileB+'.zip'
    # nzipBR = pathf+outFileBR+'.zip'
    # createZip(nzipB,outFileB)
    #createZip(nzipBR,outFileBR)
    #print ('DONE!')

if __name__ == "__main__":
    main();


