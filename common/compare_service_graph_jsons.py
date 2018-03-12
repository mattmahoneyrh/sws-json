
class compare_service_graphs():

    def __init__(self):
        a = 1

    def kiali_to_istio_nodes(self, ijson=None, kjson=None):

        assert ijson, "Istio json is required"
        assert kjson, "Kiali json is required"

        knodes = self.remove_group_nodes(kjson.get('elements').get('nodes'))

        inodes_count = len(ijson.get('nodes'))
        snodes_count = len(kjson.get('elements').get('nodes'))

        assert inodes_count == snodes_count, "Node counts do not match: inode_count: {}  snode_count: {}"\
                                             .format(inodes_count, snodes_count)

        # Verify Services
        for iservice in ijson.get('nodes'):
            found_service = False
            for snode in knodes:
                stext = snode.get('data').get('text').split(' ', 1)[0]
                sversion = snode.get('data').get('version')

                if (stext in iservice) and (sversion in iservice):
                    # print "Matched service: {} {}".format (stext, sversion)
                    found_service = True
                    break

            assert found_service, "Istio Service not in Kiali Nodes: {}".format(iservice)

        return True


    def kiali_to_istio_edges(self, ijson=None, kjson=None):

        assert ijson, "Istio json is required"
        assert kjson, "Kiali json is required"

        knodes = self.remove_group_nodes(kjson.get('elements').get('nodes'))

        iedges = ijson.get('edges')
        kedges = kjson.get('elements').get('edges')

        assert len(iedges) == len(kedges), "Edges counts do not match: ielements_edges: {}  selements_edges: {}" \
                                            .format(len(iedges), len(kedges))

        # Translate Service Graph into something more readable/comparable/debuggable

        t_sedges = []
        for edge in kedges:
            dict = {}
            source_id = edge.get('data').get('source')
            target_id = edge.get('data').get('target')

            for node in knodes:
                id = node.get('data').get('id')
                text = node.get('data').get('text').split(' ', 1)[0]
                version = node.get('data').get('version')

                if id == source_id:
                    dict['source_id'] = source_id
                    dict['source'] = text
                    dict['source_version'] = version
                elif id == target_id:
                    dict['target_id'] = target_id
                    dict['target'] = text
                    dict['target_version'] = version

            if dict: t_sedges.append(dict)

        # Validate Source/Target edges

        for iedge in iedges:
            isource = iedge.get('source')
            itarget = iedge.get('target')
            found_it = False

            for kedge in t_sedges:
                source = kedge.get('source')
                source_version = kedge.get('source_version')
                target = kedge.get('target')
                target_version = kedge.get('target_version')
                if (((source in isource) and (source_version in isource)) and
                        ((target in itarget) and (target_version in itarget))):
                    found_it = True

            assert found_it, "Did not find source: {}  {}  target: {} {}"\
                              .format(source, source_version, target, target_version)

        return True

    # Remove 'Group' Nodes, because they do not exist in Istio Service Graph
    def remove_group_nodes(self, nodes=None):
        assert nodes

        groups = []
        for i in range(0, len(nodes)):
            node = nodes[i].get('data')
            if ('link_prom_graph' not in nodes[i].get('data')):
                #print "Removin node: {}".format(node)
                groups.append(i)

        for group in groups:
            nodes.pop(group)

        return nodes