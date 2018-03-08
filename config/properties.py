import ConfigParser
import os.path

class properties():

    PROPERTIES_FILE='config/properties.properties'
    config = None

    def __init__(self):
        assert os.path.exists(self.PROPERTIES_FILE)

        self.config = ConfigParser.RawConfigParser()
        self.config.read(self.PROPERTIES_FILE)
        return

    def get_istio_service_graph_json_endpoint(self):
        return self.config.get('ServiceGraphJsonEndpoints', 'ServiceGraph.IstioJson');

    def get_sws_service_graph_json_endpoint(self):
        return self.config.get('ServiceGraphJsonEndpoints', 'ServiceGraph.SwsJson');

    def get_sws_service_graph_json_auth(self):
        auth={}
        auth['username'] = self.config.get('ServiceGraphJsonEndpoints', 'ServiceGraph.SWSJsonUsername')
        auth['password'] = self.config.get('ServiceGraphJsonEndpoints', 'ServiceGraph.SWSJsonPassword')
        return auth