from pgmpy.readwrite import XMLBIFWriter
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete.CPD import TabularCPD
from pyprojroot import here


# Define conditional probability tables for deterministic matching and mismatching
DET_MATCH = ((1, 0), (0, 1))
DET_MISMATCH = ((0, 1), (1, 0))

def define_chain(connections):
    """
    Define a chain of variables with the specified conditional probability tables
    """
    G = BayesianNetwork()
    G.add_nodes_from(["A", "B", "C", "D", "E"])
    G.add_edges_from([("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")])
    p_A = TabularCPD("A", 2, [[0.5], [0.5]])
    p_BgA = TabularCPD("B", 2, connections[0], evidence=["A"], evidence_card=[2])
    p_CgB = TabularCPD("C", 2, connections[1], evidence=["B"], evidence_card=[2])
    p_DgC = TabularCPD("D", 2, connections[2], evidence=["C"], evidence_card=[2])
    p_EgD = TabularCPD("E", 2, connections[3], evidence=["D"], evidence_card=[2])
    G.add_cpds(p_A, p_BgA, p_CgB, p_DgC, p_EgD)

    return G


if __name__ == "__main__":

    # Define the chains and save them to xmlbif
    G0 = define_chain([DET_MATCH, DET_MATCH, DET_MISMATCH, DET_MATCH])
    writer = XMLBIFWriter(model=G0)
    writer.write_xmlbif(here("data/chains/chain_0.xbn"))

    G1 = define_chain([DET_MATCH, DET_MISMATCH, DET_MATCH, DET_MATCH])
    writer = XMLBIFWriter(model=G1)
    writer.write_xmlbif(here("data/chains/chain_1.xbn"))

    G2 = define_chain([DET_MISMATCH, DET_MATCH, DET_MISMATCH, DET_MATCH])
    writer = XMLBIFWriter(model=G2)
    writer.write_xmlbif(here("data/chains/chain_2.xbn"))

    G3 = define_chain([DET_MATCH, DET_MISMATCH, DET_MATCH, DET_MISMATCH])
    writer = XMLBIFWriter(model=G3)
    writer.write_xmlbif(here("data/chains/chain_3.xbn"))