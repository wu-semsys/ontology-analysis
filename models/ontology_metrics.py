import rdflib
from rdflib.namespace import RDF, RDFS, OWL

class OntologyMetrics:
    def __init__(self, graph):
        self.graph = graph

    def calculate_dl_expressivity(self):
        expressivity = set()
        
        graph = self.graph

        # Check for complex class constructors
        if any(graph.triples((None, OWL.unionOf, None))):
            expressivity.add('U')
        if any(graph.triples((None, OWL.intersectionOf, None))):
            expressivity.add('C')
        if any(graph.triples((None, OWL.complementOf, None))):
            expressivity.add('C')
        if any(graph.triples((None, OWL.someValuesFrom, None))):
            expressivity.add('E')
        if any(graph.triples((None, OWL.allValuesFrom, None))):
            expressivity.add('E')
            
        # Check for object and data properties
        if any(graph.triples((None, RDF.type, OWL.ObjectProperty))):
            expressivity.add('R')
        if any(graph.triples((None, RDF.type, OWL.DatatypeProperty))):
            expressivity.add('D')

        # Check for functional properties
        if any(graph.triples((None, RDF.type, OWL.FunctionalProperty))):
            expressivity.add('F')
        if any(graph.triples((None, RDF.type, OWL.InverseFunctionalProperty))):
            expressivity.add('I')

        # Check for cardinality restrictions
        if any(graph.triples((None, OWL.maxCardinality, None))) or \
        any(graph.triples((None, OWL.minCardinality, None))) or \
        any(graph.triples((None, OWL.cardinality, None))):
            expressivity.add('N')

        # Role hierarchies (subproperties)
        if any(graph.triples((None, RDFS.subPropertyOf, None))):
            expressivity.add('H')

        # Role composition (property chains)
        if any(graph.triples((None, OWL.propertyChainAxiom, None))):
            expressivity.add('R')

        # Reflexivity and irreflexivity
        if any(graph.triples((None, RDF.type, OWL.ReflexiveProperty))):
            expressivity.add('X')
        if any(graph.triples((None, RDF.type, OWL.IrreflexiveProperty))):
            expressivity.add('Y')

        # Transitivity
        if any(graph.triples((None, RDF.type, OWL.TransitiveProperty))):
            expressivity.add('T')

        # Symmetric and Asymmetric properties
        if any(graph.triples((None, RDF.type, OWL.SymmetricProperty))):
            expressivity.add('S')
        if any(graph.triples((None, RDF.type, OWL.AsymmetricProperty))):
            expressivity.add('A')

        # Inverse properties
        if any(graph.triples((None, OWL.inverseOf, None))):
            expressivity.add('I')

        # Qualified cardinality restrictions (checking if a property restriction has a specific type)
        for s, _, _ in graph.triples((None, OWL.onProperty, None)):
            if any(graph.triples((s, OWL.someValuesFrom, None))) or \
            any(graph.triples((s, OWL.allValuesFrom, None))):
                expressivity.add('Q')

        return ''.join(sorted(expressivity))

    def explain_dl_expressivity(self, expressivity):
        explanations = {
            'A': "Asymmetric properties: Properties that cannot be true in both directions.",
            'C': "Complex class constructors: Intersection, union, and complement of concepts.",
            'D': "Datatype properties: Properties that link individuals to data values.",
            'E': "Existential restrictions: Restrictions that require some relationship to exist.",
            'F': "Functional properties: Properties that have at most one value for each individual.",
            'H': "Role hierarchies: Subproperties that form a hierarchy.",
            'I': "Inverse properties: Properties that are the inverse of other properties.",
            'N': "Cardinality restrictions: Restrictions on the number of values a property can have.",
            'O': "Nominals: Enumerated classes of specific individuals.",
            'Q': "Qualified cardinality restrictions: Cardinality restrictions with specific value types.",
            'R': "Role constructors: Complex role constructs, including composition and hierarchy.",
            'X': "Reflexive properties: Properties that relate individuals to themselves.",
            'Y': "Irreflexive properties: Properties that do not relate individuals to themselves.",
            'S': "Symmetric properties: Properties that are true in both directions.",
            'T': "Transitive properties: Properties that imply the same property over chains of relationships.",
            'U': "Union of concepts: The disjunction of multiple concepts."
        }

        explanation_list = [explanations[char] for char in expressivity]
        return "\n".join(explanation_list)

    def detect_dl_constructs(self):
        graph = self.graph
        
        constructs = {
            "is_unionExists": any(graph.triples((None, OWL.unionOf, None))),
            "is_intersectionExists": any(graph.triples((None, OWL.intersectionOf, None))),
            "is_complementExists": any(graph.triples((None, OWL.complementOf, None))),
            "is_existentialRestrictionExists": any(graph.triples((None, OWL.someValuesFrom, None))),
            "is_universalRestrictionExists": any(graph.triples((None, OWL.allValuesFrom, None))),
            "is_objectPropertyExists": any(graph.triples((None, RDF.type, OWL.ObjectProperty))),
            "is_dataPropertyExists": any(graph.triples((None, RDF.type, OWL.DatatypeProperty))),
            "is_functionalPropertyExists": any(graph.triples((None, RDF.type, OWL.FunctionalProperty))),
            "is_inverseFunctionalPropertyExists": any(graph.triples((None, RDF.type, OWL.InverseFunctionalProperty))),
            "is_cardinalityRestrictionExists": any(graph.triples((None, OWL.maxCardinality, None))) or 
                                            any(graph.triples((None, OWL.minCardinality, None))) or 
                                            any(graph.triples((None, OWL.cardinality, None))),
            "is_roleHierarchyExists": any(graph.triples((None, RDFS.subPropertyOf, None))),
            "is_roleCompositionExists": any(graph.triples((None, OWL.propertyChainAxiom, None))),
            "is_reflexivePropertyExists": any(graph.triples((None, RDF.type, OWL.ReflexiveProperty))),
            "is_irreflexivePropertyExists": any(graph.triples((None, RDF.type, OWL.IrreflexiveProperty))),
            "is_transitivePropertyExists": any(graph.triples((None, RDF.type, OWL.TransitiveProperty))),
            "is_symmetricPropertyExists": any(graph.triples((None, RDF.type, OWL.SymmetricProperty))),
            "is_asymmetricPropertyExists": any(graph.triples((None, RDF.type, OWL.AsymmetricProperty))),
            "is_inversePropertyExists": any(graph.triples((None, OWL.inverseOf, None))),
            "is_qualifiedCardinalityRestrictionExists": False  # We'll set this below
        }

        # Check for qualified cardinality restrictions
        for s, _, _ in graph.triples((None, OWL.onProperty, None)):
            if any(graph.triples((s, OWL.someValuesFrom, None))) or any(graph.triples((s, OWL.allValuesFrom, None))):
                constructs["is_qualifiedCardinalityRestrictionExists"] = True
                break

        return constructs
    
    def calculate_ontology_metrics(self):
        g = self.graph

        # Count of explicit subclass relations
        subclass_triples = list(g.triples((None, RDFS.subClassOf, None)))
        
        # Calculate GCI: Any subclass relation where either side is not a simple class reference
        gci_count = 0
        for s, p, o in subclass_triples:
            if (not isinstance(s, rdflib.URIRef) or not isinstance(o, rdflib.URIRef)) or \
            any(g.triples((s, None, None))) or any(g.triples((o, None, None))):
                gci_count += 1

        # Attempt to calculate Hidden GCI (very simplistic approach)
        hidden_gci_count = 0
        # This could be extended with specific rules or patterns you expect to form hidden GCIs

        metrics = {
            "Axioms": len(g),
            "Logical axioms": 0,
            "Declaration axioms count": 0,
            
            "Class count": len(list(g.triples((None, RDF.type, OWL.Class)))),
            "Object Property count": len(list(g.triples((None, RDF.type, OWL.ObjectProperty)))),
            "Data Property count": len(list(g.triples((None, RDF.type, OWL.DatatypeProperty)))),
            "Individual count": len(list(g.triples((None, RDF.type, OWL.NamedIndividual)))),
            "Annotation Property count": len(list(g.triples((None, RDF.type, OWL.AnnotationProperty)))),
            
            "SubClassOf": len(subclass_triples),
            "EquivalentClasses": len(list(g.triples((None, OWL.equivalentClass, None)))),
            "DisjointClasses": len(list(g.triples((None, OWL.disjointWith, None)))),
            "GCI Count": gci_count,
            "Hidden GCI Count": hidden_gci_count,
            
            "SubObjectPropertyOf": len(list(g.triples((None, RDFS.subPropertyOf, None)))),
            "EquivalentObjectProperties": len(list(g.triples((None, OWL.equivalentProperty, None)))),
            "InverseObjectProperties": len(list(g.triples((None, OWL.inverseOf, None)))),
            "DisjointObjectProperties": len(list(g.triples((None, OWL.propertyDisjointWith, None)))),
            "FunctionalObjectProperty": len(list(g.triples((None, RDF.type, OWL.FunctionalProperty)))),
            "InverseFunctionalObjectProperty": len(list(g.triples((None, RDF.type, OWL.InverseFunctionalProperty)))),
            "TransitiveObjectProperty": len(list(g.triples((None, RDF.type, OWL.TransitiveProperty)))),
            "SymmetricObjectProperty": len(list(g.triples((None, RDF.type, OWL.SymmetricProperty)))),
            "AsymmetricObjectProperty": len(list(g.triples((None, RDF.type, OWL.AsymmetricProperty)))),
            "ReflexiveObjectProperty": len(list(g.triples((None, RDF.type, OWL.ReflexiveProperty)))),
            "IrreflexiveObjectProperty": len(list(g.triples((None, RDF.type, OWL.IrreflexiveProperty)))),
            "ObjectPropertyDomain": len(list(g.triples((None, RDFS.domain, None)))),
            "ObjectPropertyRange": len(list(g.triples((None, RDFS.range, None)))),
            "SubPropertyChainOf": len(list(g.triples((None, OWL.propertyChainAxiom, None)))),
            
            "SubDataPropertyOf": len(list(g.triples((None, RDFS.subPropertyOf, None)))),
            "EquivalentDataProperties": len(list(g.triples((None, OWL.equivalentProperty, None)))),
            "DisjointDataProperties": len(list(g.triples((None, OWL.propertyDisjointWith, None)))),
            "FunctionalDataProperty": len(list(g.triples((None, RDF.type, OWL.FunctionalProperty)))),
            "DataPropertyDomain": len(list(g.triples((None, RDFS.domain, None)))),
            "DataPropertyRange": len(list(g.triples((None, RDFS.range, None)))),
            
            "ClassAssertion": len(list(g.triples((None, RDF.type, None)))),
            "ObjectPropertyAssertion": len(list(g.triples((None, None, None)))),
            "DataPropertyAssertion": len(list(g.triples((None, None, None)))),
            "NegativeObjectPropertyAssertion": len(list(g.triples((None, OWL.sourceIndividual, None)))),
            "NegativeDataPropertyAssertion": len(list(g.triples((None, OWL.sourceIndividual, None)))),
            "SameIndividual": len(list(g.triples((None, OWL.sameAs, None)))),
            "DifferentIndividuals": len(list(g.triples((None, OWL.differentFrom, None)))),
            
            "AnnotationAssertion": len(list(g.triples((None, None, None)))),
            "AnnotationPropertyDomain": len(list(g.triples((None, RDFS.domain, None)))),
            "AnnotationPropertyRange": len(list(g.triples((None, RDFS.range, None)))),
            "SubAnnotationPropertyOf": len(list(g.triples((None, RDFS.subPropertyOf, None)))),
        }

        metrics["Logical axioms"] = (
            metrics["SubClassOf"] +
            metrics["EquivalentClasses"] +
            metrics["DisjointClasses"] +
            metrics["GCI Count"] +
            metrics["SubObjectPropertyOf"] +
            metrics["EquivalentObjectProperties"] +
            metrics["InverseObjectProperties"] +
            metrics["DisjointObjectProperties"] +
            metrics["FunctionalObjectProperty"] +
            metrics["InverseFunctionalObjectProperty"] +
            metrics["TransitiveObjectProperty"] +
            metrics["SymmetricObjectProperty"] +
            metrics["AsymmetricObjectProperty"] +
            metrics["ReflexiveObjectProperty"] +
            metrics["IrreflexiveObjectProperty"] +
            metrics["ObjectPropertyDomain"] +
            metrics["ObjectPropertyRange"] +
            metrics["SubDataPropertyOf"] +
            metrics["EquivalentDataProperties"] +
            metrics["DisjointDataProperties"] +
            metrics["FunctionalDataProperty"] +
            metrics["DataPropertyDomain"] +
            metrics["DataPropertyRange"] +
            metrics["ClassAssertion"] +
            metrics["ObjectPropertyAssertion"] +
            metrics["DataPropertyAssertion"] +
            metrics["NegativeObjectPropertyAssertion"] +
            metrics["NegativeDataPropertyAssertion"] +
            metrics["SameIndividual"] +
            metrics["DifferentIndividuals"]
        )

        metrics["Declaration axioms count"] = (
            metrics["Class count"] +
            metrics["Object Property count"] +
            metrics["Data Property count"] +
            metrics["Individual count"] +
            metrics["Annotation Property count"]
        )

        # Add more checks for other DL constructs and update expressivity
        
        metrics["DL Expressivity"] = self.calculate_dl_expressivity()
        metrics["DL Constructs"] = self.detect_dl_constructs()

        return metrics
