from pgmpy.readwrite import XMLBIFWriter
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete.CPD import TabularCPD
from pyprojroot import here


DET_MATCH = ((1, 0), (0, 1))
DET_MISMATCH = ((0, 1), (1, 0))

if __name__ == "__main__":
    # set up a chain
    G = BayesianNetwork()
    G.add_nodes_from(["A", "B", "C", "D", "E"])
    G.add_edges_from([("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")])

    # set up the CPDs
    p_A = TabularCPD("A", 2, [[0.5], [0.5]])
    p_BgA = TabularCPD("B", 2, DET_MATCH, evidence=["A"], evidence_card=[2])
    p_CgB = TabularCPD("C", 2, DET_MATCH, evidence=["B"], evidence_card=[2])
    p_DgC = TabularCPD("D", 2, DET_MISMATCH, evidence=["C"], evidence_card=[2])
    p_EgD = TabularCPD("E", 2, DET_MATCH, evidence=["D"], evidence_card=[2])
    G.add_cpds(p_A, p_BgA, p_CgB, p_DgC, p_EgD)

    # save it to an XML file
    writer = XMLBIFWriter(model=G)
    writer.write_xmlbif(here("data/chains/chain_0.xbn"))

    # The chain with a mismatch in B/C
    G = BayesianNetwork()
    G.add_nodes_from(["A", "B", "C", "D", "E"])
    G.add_edges_from([("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")])
    p_A = TabularCPD("A", 2, [[0.5], [0.5]])
    p_BgA = TabularCPD("B", 2, DET_MATCH, evidence=["A"], evidence_card=[2])
    p_CgB = TabularCPD("C", 2, DET_MISMATCH, evidence=["B"], evidence_card=[2])
    p_DgC = TabularCPD("D", 2, DET_MATCH, evidence=["C"], evidence_card=[2])
    p_EgD = TabularCPD("E", 2, DET_MATCH, evidence=["D"], evidence_card=[2])
    G.add_cpds(p_A, p_BgA, p_CgB, p_DgC, p_EgD)
    writer = XMLBIFWriter(model=G)
    writer.write_xmlbif(here("data/chains/chain_1.xbn"))

    # The chain with mismatches in A/B and C/D
    G = BayesianNetwork()
    G.add_nodes_from(["A", "B", "C", "D", "E"])
    G.add_edges_from([("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")])
    p_A = TabularCPD("A", 2, [[0.5], [0.5]])
    p_BgA = TabularCPD("B", 2, DET_MISMATCH, evidence=["A"], evidence_card=[2])
    p_CgB = TabularCPD("C", 2, DET_MATCH, evidence=["B"], evidence_card=[2])
    p_DgC = TabularCPD("D", 2, DET_MISMATCH, evidence=["C"], evidence_card=[2])
    p_EgD = TabularCPD("E", 2, DET_MATCH, evidence=["D"], evidence_card=[2])
    G.add_cpds(p_A, p_BgA, p_CgB, p_DgC, p_EgD)
    writer = XMLBIFWriter(model=G)
    writer.write_xmlbif(here("data/chains/chain_2.xbn"))

    # The chain with mismatches in B/C and D/E
    G = BayesianNetwork()
    G.add_nodes_from(["A", "B", "C", "D", "E"])
    G.add_edges_from([("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")])
    p_A = TabularCPD("A", 2, [[0.5], [0.5]])
    p_BgA = TabularCPD("B", 2, DET_MATCH, evidence=["A"], evidence_card=[2])
    p_CgB = TabularCPD("C", 2, DET_MISMATCH, evidence=["B"], evidence_card=[2])
    p_DgC = TabularCPD("D", 2, DET_MATCH, evidence=["C"], evidence_card=[2])
    p_EgD = TabularCPD("E", 2, DET_MISMATCH, evidence=["D"], evidence_card=[2])
    G.add_cpds(p_A, p_BgA, p_CgB, p_DgC, p_EgD)
    writer = XMLBIFWriter(model=G)
    writer.write_xmlbif(here("data/chains/chain_3.xbn"))
