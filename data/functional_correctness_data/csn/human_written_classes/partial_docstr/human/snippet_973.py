from dipper.graph.Graph import Graph
from dipper.models.Model import Model
from dipper.utils.GraphUtils import GraphUtils

class Pathway:
    """
    This provides convenience methods to deal with gene and protein collections
    in the context of pathways.
    """

    def __init__(self, graph):
        if isinstance(graph, Graph):
            self.graph = graph
        else:
            raise ValueError('{} is not a graph'.format(graph))
        self.model = Model(self.graph)
        self.globaltt = self.graph.globaltt
        self.globaltcid = self.graph.globaltcid
        self.curie_map = self.graph.curie_map
        self.gut = GraphUtils(self.curie_map)

    def addPathway(self, pathway_id, pathway_label, pathway_type=None, pathway_description=None):
        """
        Adds a pathway as a class.  If no specific type is specified, it will
        default to a subclass of "GO:cellular_process" and "PW:pathway".
        :param pathway_id:
        :param pathway_label:
        :param pathway_type:
        :param pathway_description:
        :return:
        """
        if pathway_type is None:
            pathway_type = self.globaltt['cellular_process']
        self.model.addClassToGraph(pathway_id, pathway_label, pathway_type, pathway_description)
        self.model.addSubClass(pathway_id, self.globaltt['pathway'])

    def addGeneToPathway(self, gene_id, pathway_id):
        """
        When adding a gene to a pathway, we create an intermediate
        'gene product' that is involved in
        the pathway, through a blank node.

        gene_id RO:has_gene_product _gene_product
        _gene_product RO:involved_in pathway_id

        :param pathway_id:
        :param gene_id:
        :return:
        """
        gene_product = ':'.join(('_', self.gut.digest_id(gene_id.replace(':', '') + 'product')))
        self.model.addIndividualToGraph(gene_product, None, self.globaltt['gene_product'])
        self.graph.addTriple(gene_product, self.globaltt['label'], pathway_id)
        self.graph.addTriple(gene_id, self.globaltt['has gene product'], gene_product)
        self.addComponentToPathway(gene_product, pathway_id)

    def addComponentToPathway(self, component_id, pathway_id):
        """
        This can be used directly when the component is directly involved in
        the pathway.  If a transforming event is performed on the component
        first, then the addGeneToPathway should be used instead.

        :param pathway_id:
        :param component_id:
        :param component_category: biolink category for component_id
        :param pathway_category: biolink category for pathway_id
        :return:
        """
        self.graph.addTriple(component_id, self.globaltt['involved in'], pathway_id)