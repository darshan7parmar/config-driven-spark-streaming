class DataStreamProvider:
    def __init__(self):
        pass

    def getStream(self, ssc, input):
        """get Stream Object returns the specific Dstream based on type."""
        if input['type'] == 'stream' and input['sub_type'] == 'socket':
            return ssc.socketTextStream(input["ip"], input["port"])
        return None
