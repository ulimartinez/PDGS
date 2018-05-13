from Dissector import TShark
import pdb
import sys, os, subprocess, re

class PCAP:
    def __init__(self, fileName):
        self.tshark = TShark()
        self.fileName = fileName
        self.readCaptureFile()


    def readCaptureFile(self):
        params = [self.tshark.find_path(), "-r"+self.fileName]
        self.capture = self.tshark.run_command(params, stderr=None)


    def getPackets(self):
        packets = self.capture.split('\n')
        return self.filterPackets(packets)

    def filterPackets(self, packets):
        counter = 0
        info = ""
        filteredPackets = dict()
        for x in range(0, len(packets)-1):

            packets[x] = packets[x].split(' ')
            packets[x] = filter(None, packets[x])
            packets[x][1].strip(' ')
            packets[x] = filter(lambda k: "\xe2\x86\x92" not in k, packets[x])
            filteredPackets[x] = dict([("No", packets[x][0]), ("Time", packets[x][1]),
            ("Source", packets[x][2]), ("Destination", packets[x][3]), ("Protocol", packets[x][4])])
            for y in range(4, len(packets[x])):
                info += packets[x][y] +" "
                filteredPackets[x]["Info"] = info
            info = ""
        return filteredPackets
