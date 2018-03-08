import requests
import ConfigParser


class json_requests():
    request = None

    def __init__(self, url=None, auth=None):
        assert url, "URL Required."

        #print "URL: {}".format(url)

        if auth:
            self.request = requests.get(url, auth=(auth.get('username'), auth.get('password')))
        else:
            self.request = requests.get(url)

    def get_istio_service_graph_json(self, debug=False):
        ijson = self.request.json()

        if debug:
            print "\n\nIstio Service Graph JSON:"

            print "\nNodes List:"
            for key, value in ijson.get('nodes').items():
                print (key, value)

            print "\n\nEdges List:"
            for e in ijson.get('edges'):
                print "Edge:"
                for key, value in e.items():
                    print (key, value)

        return ijson

    def get_sws_service_graph_json(self, debug=False):
        sjson = self.request.json()

        if debug:
            print "\n\nSWS Service Graph Nodes:"

            print "\nNodes List:"
            for n in sjson.get('elements').get('nodes'):
                print n.get('data')

            print "\n\nSWS Service Graph Edges:"

            print "\nEdges List:"
            for n in sjson.get('elements').get('edges'):
                print n.get('data')

        return sjson

