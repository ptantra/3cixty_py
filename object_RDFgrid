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
        rf = csv.reader(f, delimiter=',')
        return rf
    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
        raise

def definePrefixes():
    prefixes = {'locationOnt': 'http://data.linkedevents.org/def/location#',
                'geom': 'http://geovocab.org/geometry#',
                'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
                'gsp': 'http://www.opengis.net/ont/geosparql#',
                'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                'locn': 'http://www.w3.org/ns/locn#',
                'sf':'http://www.opengis.net/ont/sf#'
                }
    return prefixes

def bindingPrefixes(g, prefixes):
    for key in prefixes:
        g.bind(key, prefixes[key])
    return g

def getGridData(row):
    cellId = row[0]
    cellPoly = row[1]
    cellLat=row[2]
    cellLon=row[3]
    cellPoint=row[4]
    lst = [cellId, cellPoly, cellLat, cellLon, cellPoint]
    return lst

def createGridGraph(arg, g):

    locationOnt = Namespace("http://data.linkedevents.org/def/location#")
    geo = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
    geom= Namespace('http://geovocab.org/geometry#')
    gs = Namespace("http://www.opengis.net/ont/geosparql#")
    locn = Namespace("http://www.w3.org/ns/locn#")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    sf = Namespace('http://www.opengis.net/ont/sf#')

    cellLondon= URIRef("http://data.linkedevents.org/location/" + "%s")% arg[0]
    cellCentroid= URIRef("http://data.linkedevents.org/location/" + "%s" + "/centroid") % arg[0]
    cellGeometry= URIRef("http://data.linkedevents.org/location/" + "%s" + "/geometry") % arg[0]

    g.add((cellLondon, rdf.type, locationOnt.cell))
    g.add((cellLondon, geom.centroid, cellCentroid ))
    g.add((cellLondon, geo.location, cellGeometry))

    g.add((cellGeometry, rdf.type, sf.Polygon))
    g.add((cellGeometry, locn.geometry, Literal(arg[1], datatype=gs.wktLiteral)))

    g.add((cellCentroid, rdf.type, sf.Point))
    g.add((cellCentroid, locn.centroid, Literal(arg[4], datatype=gs.wktLiteral)))

    prefixes=definePrefixes()
    bindingPrefixes(g, prefixes)

    return g

def main():
    pathf = "/Users/patrick/3cixty/IN/AB/Grid/"
    inFile = pathf + "ldn_cellsMERGE.csv"
    outFile = pathf + "ldn_cells.ttl"

    csv = readCsv(inFile)
    next(csv, None)  # FILE WITH HEADERS

    store = plugin.get('IOMemory', Store)()
    g = Graph(store)

    prefixes = definePrefixes()
    print('Binding Prefixes')
    bindingPrefixes(g, prefixes)

    print('Creating graph-Hotel...')  # AMENDED

    #This one generates the 'turtle' graph. Please deactivate the script for the 'nt' graph below
    for row in csv:
        lstData = getGridData(row)
        createGridGraph(lstData, g).serialize(outFile, format='turtle')

    print ('DONE! Time elapsed ' + str((time.time() - start_time)))

if __name__ == "__main__":
    main()
