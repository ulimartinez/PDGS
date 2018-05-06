from builder.Dissector import Dissector


class Protocol:
    def __init__(self, name):
        self.name = name
        self.dissector = Dissector(self)

    def get_dissector(self):
        return self.dissector


proto = Protocol("Awesome")
proto.get_dissector().dissect_packet("packet.pcap")
