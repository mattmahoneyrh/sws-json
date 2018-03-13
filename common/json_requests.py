import requests

class json_requests():
    request = None

    def __init__(self, url=None, auth=None):
        assert url, "URL Required."

        #print "URL: {}".format(url)

        if auth:
            self.request = requests.get(url, auth=(auth.get('username'), auth.get('password')))
        else:
            self.request = requests.get(url)

        assert 503 != self.request.status_code

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

    def get_kiali_service_graph_json(self, debug=False):
        kjson = self.request.json()

        if debug:
            print "\n\nKiali Service Graph Nodes:"

            print "\nNodes List:"
            for n in kjson.get('elements').get('nodes'):
                print n.get('data')

            print "\n\nKiali Service Graph Edges:"

            print "\nEdges List:"
            for n in kjson.get('elements').get('edges'):
                print n.get('data')

        return kjson

