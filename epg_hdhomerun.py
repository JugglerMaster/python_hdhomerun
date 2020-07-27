#!/usr/bin/env python



import sys, json, urllib, datetime, subprocess

import xml.etree.cElementTree as ET

from xml.dom import minidom

from pprint import pprint


def fixDefaultEncoding():

    # sys.setdefaultencoding() does not exist, here!

    reload(sys)  # Reload does the trick!

    sys.setdefaultencoding('UTF8')



def loadGuideFromWeb():

    #device_ip = subprocess.check_output(["hdhomerun_config", "discover"]).split()[5]

    discover_url = json.loads(urllib.urlopen("http://my.hdhomerun.com/discover").read())[0]["DiscoverURL"]

    #print device_ip



    #device_auth = json.loads(urllib.urlopen("http://%s/discover.json" % device_ip).read())['DeviceAuth']

    device_auth = json.loads(urllib.urlopen(discover_url).read())['DeviceAuth']

    #print device_auth



    return json.loads(urllib.urlopen("http://my.hdhomerun.com/api/guide.php?DeviceAuth=%s" % device_auth).read())

    

def generatXMLTV(data):

    timezone_offset = subprocess.check_output(['date', '+%z']).strip()

    xml = ET.Element("tv")

    for channel in data:

        xmlChannel = ET.SubElement(xml, "channel", id=channel['GuideName'])

        ET.SubElement(xmlChannel, "display-name").text = channel['GuideName'] 

        ET.SubElement(xmlChannel, "display-name").text = channel['GuideNumber']

        if 'Affiliate' in channel:

            ET.SubElement(xmlChannel, "display-name").text = channel['Affiliate']

        if 'ImageURL' in channel:

            ET.SubElement(xmlChannel, "icon", src=channel['ImageURL'])

        if 'URL' in channel:

            ET.SubElement(xmlChannel, "url").text = channel['URL']

        for program in channel["Guide"]:

            xmlProgram = ET.SubElement(xml, "programme", channel=channel['GuideName'])

            xmlProgram.set("start", datetime.datetime.fromtimestamp(program['StartTime']).strftime('%Y%m%d%H%M%S') + " " + timezone_offset)

            xmlProgram.set("stop", datetime.datetime.fromtimestamp(program['EndTime']).strftime('%Y%m%d%H%M%S') + " " + timezone_offset)

            ET.SubElement(xmlProgram, "title").text = program['Title']

            if 'EpisodeNumber' in program:

                

                adding = ""

                for char1 in program["EpisodeNumber"]:

                    if char1 == "E":

                        #print("Change to period :" + char1)

                        adding = adding + "."

                    elif char1 != "S":

                        adding = adding + char1

                    #print(adding)

                ET.SubElement(xmlProgram, "episode-num").text = adding

            if 'EpisodeTitle' in program:

                ET.SubElement(xmlProgram, "sub-title").text = program['EpisodeTitle']

            if 'Synopsis' in program:

                ET.SubElement(xmlProgram, "desc").text = program['Synopsis']

            if 'OriginalAirdate' in program:

                ET.SubElement(xmlProgram, "date").text = datetime.datetime.fromtimestamp(program['OriginalAirdate']).strftime('%Y%m%d%H%M%S') + " " + timezone_offset

            if 'PosterURL' in program:

                ET.SubElement(xmlProgram, "icon", src=program['PosterURL'])

            if 'Filter' in program:

                for filter in program['Filter']:

                    ET.SubElement(xmlProgram, "category").text = filter

            



    #return ET.tostring(xml)



    reformed_xml = minidom.parseString(ET.tostring(xml).encode('utf-8'))

    return reformed_xml.toprettyxml(encoding='utf-8')

def printGuide(data):

    for channel in data:

        print("-----------------CHANEL-----------------")

        print(channel['GuideNumber'])

        print(channel['GuideName'])

        if 'Affiliate' in channel:

            print(channel['Affiliate'])

        if 'ImageURL' in channel:

            print(channel['ImageURL'])

        if 'URL' in channel:

            print(channel['URL'])

        #VideoCodec

        #AudioCodec

        #HD

        #Favorite

        for program in channel["Guide"]:

            print("\t---------------PROGRAM---------------")

            print("\t" + program['Title'].encode('utf-8'))

            print("\t" + str(program['StartTime']))

            print("\t" + str(program['EndTime']))

            if 'EpisodeNumber' in program:

                print("\t" + program['EpisodeNumber'])

            if 'EpisodeTitle' in program:

                print("\t" + program['EpisodeTitle'].encode('utf-8'))

            if 'Synopsis' in program:

                print("\t" + program['Synopsis'].encode('utf-8'))

            if 'OriginalAirdate' in program:

                print("\t" + str(program['OriginalAirdate']))

            print("\t" + program['SeriesID'])

            if 'PosterURL' in program:

                print("\t" + program['PosterURL'])

            if 'Filter' in program:

                for filter in program['Filter']:

                    print("\t\t" + filter.encode('utf-8'))

                    

def saveStringToFile(strData, filename):

    with open(filename, 'w') as outfile:

        outfile.write(strData)

                    

def loadJsonFromFile(filename):

    return json.load(open(filename))



def saveJsonToFile(data, filename):

    with open(filename, 'w') as outfile:

        json.dump(data, outfile, indent=4)

                    

def main():

    fixDefaultEncoding()

    data = loadGuideFromWeb()

    #saveJsonToFile(data, "hdhomerun.json")

    #data = loadJsonFromFile("hdhomerun.json")

    

    xmltv = generatXMLTV(data)

    #print xmltv

    saveStringToFile(xmltv, "hdhomerun.xml")

    

    #printGuide(data)

  

if __name__== "__main__":

    main()
