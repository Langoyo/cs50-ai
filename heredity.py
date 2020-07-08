import csv
import itertools
import sys
import math

# Transition table from parent to child. First digit is from parent, second is from child
# It is taken into accoount the mutation factor
trans_parent_to_child = {
    0: {
        0: 0.99,
        1: 0.01
    },
    1: {
        0: 0.50,
        1: 0.50
    },
    2: {
        0: 0.01,
        1: 0.99
    }
}

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    probability = []
    # Childs depend on parents. Parents are saved into a list
    parents = [person for person in people if people[person]["father"] is None and people if people[person]["mother"] is None]
    #childs = [child for person in people if person not in parent] 

    # Creating a data structure that stores what it is asked for each person in this call
    data = extract_data(people, one_gene, two_genes, have_trait)

    # Iterating through the parents
    for person in parents:
        # Extracting the data of this parent
        gene = data[person]["gene"]
        trait = data[person]["has_trait"]
        # Calculating its probability
        probability.append(PROBS["gene"][gene] * PROBS["trait"][gene][trait])
    
    # Iterating through the childs
    for person in people:
        if person not in parents:
            # Getting required data for each child
            father = people[person]["father"]
            mother = people[person]["mother"]
            father_gene = data[father]["gene"]
            mother_gene = data[mother]["gene"]
            trait = data[person]["has_trait"]

            if data[person]["gene"] == 1:
                # As in the exapmle, cases in which only one parent transmits the disease
                probability.append((trans_parent_to_child[father_gene][1] * 
                trans_parent_to_child[mother_gene][0] +
                trans_parent_to_child[father_gene][0] * 
                trans_parent_to_child[mother_gene][1]) * PROBS["trait"][1][trait])
            elif data[person]["gene"] == 2:
                # Both parents must transmit the disease
                probability.append((trans_parent_to_child[father_gene][1] *
                trans_parent_to_child[mother_gene][1]) * PROBS["trait"][2][trait])
            else:
                # No parent transmit the disease
                probability.append((trans_parent_to_child[father_gene][0] * 
                trans_parent_to_child[mother_gene][0]) *
                                   PROBS["trait"][0][trait])
    
    return math.prod(probability)


def extract_data(people, one_gene, two_genes, have_trait):
    """
    Receives:
    people -> a dictionary/list with all the people in the problem
    one_gene -> set of people with one gene
    two_genes -> set of people with two genes
    have_trait -> set of people with the disease

    Function returns a dictionary which stores the gene and the trait of each person
    """
    data = {
        person: {
            "gene": 0,
                
            "has_trait": False
        }
        for person in people
    }
    for person in people:
        if person in one_gene:
            data[person]["gene"] = 1
        elif person in two_genes:
            data[person]["gene"] = 2
        else:
            data[person]["gene"] = 0

        data[person]["has_trait"] = person in have_trait
    return data


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    #  Extracting the gene and the trait of each person again
    data = extract_data(probabilities,one_gene,two_genes,have_trait)

    # Adding the new probability to the corresponding entry of the dictinoary
    for person in probabilities:
        genes = data[person]["gene"]
        trait = data[person]["has_trait"]
        probabilities[person]["gene"][genes] += p
        probabilities[person]["trait"][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # 1 = constant * (prob0 + prob1 + prob2) -> Solving the equation for constant and recalculating probabilities
        constant = 1 / (probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2])
        probabilities[person]["gene"][0] *= constant
        probabilities[person]["gene"][1] *= constant
        probabilities[person]["gene"][2] *= constant

        # 1 = constant * (probTrue +  probFalse) -> Solving the equation for constant and recalculating probabilities
        constant = 1 / (probabilities[person]["trait"][True] + probabilities[person]["trait"][False])
        probabilities[person]["trait"][True] *= constant
        probabilities[person]["trait"][False] *= constant

if __name__ == "__main__":
    main()
