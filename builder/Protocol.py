from Dissector import Dissector
from PCAP import PCAP


class Protocol:
    def __init__(self, name):
        self.name = name
        self.dissector = Dissector(self)

    def get_dissector(self):
        return self.dissector

    def getPackets(self, fileName):
        self.pcap = PCAP(fileName).getPackets()
