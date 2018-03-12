import pytest
from common.json_requests import json_requests
from common.compare_service_graph_jsons import compare_service_graphs
from config.properties import properties

@pytest.fixture
def request_urls():
    ijson = json_requests(url=properties().get_istio_service_graph_json_endpoint()).get_istio_service_graph_json()
    sjson = json_requests(url=properties().get_kiali_service_graph_json_endpoint(),
                          auth=properties().get_kiali_service_graph_json_auth()).get_kiali_service_graph_json()

    dict = {'ijson':ijson, 'sjson':sjson}

    return dict

def test_service_graph_json_nodes(request_urls):
    print "Begin test_service_graph_json_nodes"
    assert compare_service_graphs().kiali_to_istio_nodes(ijson=request_urls.get('ijson'), kjson=request_urls.get('sjson'))

def test_service_graph_json_edges(request_urls):
    print "Begin test_service_graph_json_edges"
    assert compare_service_graphs().kiali_to_istio_edges(ijson=request_urls.get('ijson'), kjson=request_urls.get('sjson'))

