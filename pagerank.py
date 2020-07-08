import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    model = {}
    # Getting the links from the page
    linked_pages = corpus[page]

    # If the page has no link, assing equal probability to all the pages
    if len(linked_pages) == 0:

        for link in corpus:
            model[link] = 1 / len(corpus)
    else:
        for link in corpus:
            # If the link is in the linked pages the expression has two parts
            if link in linked_pages:
                model[link] = (1 - damping_factor) / len(corpus) + damping_factor / len(linked_pages)
            # Otherwise is just one
            else:
                model[link] = (1 - damping_factor) / len(corpus)

    
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = {}
    # Initializing the samples dictionary
    for key in corpus:
        ranks[key] = 0
    # Selecting a first random page
    current_sample = random.choice(list(corpus.keys()))
    ranks[current_sample] += 1

    # Getting the transition model for each page
    transitions = {}
    for key in corpus:
        transitions[key] = transition_model(corpus, key, damping_factor)
    
    # Now the PageRank is calculated
    for iteration in range(n-1):
        current_sample = get_sample(current_sample,transitions[current_sample])
        ranks[current_sample] += 1

    # The result for each page is divided by the n iterations to calculate the percentage
    for key,item in ranks.items():
        ranks[key] = item / n
    
    return ranks

def get_sample(page, transition_mod):
    """
    Calculates the next sample given a page and its transition model
    """
    random_value = random.random()
    limit_range = 0

    # The interval of 0-1 is divided into ranges depending on the percentages
    # from the transition model. If the random value is lower than the current range,
    # that page key is returned.
    for link,percentage in transition_mod.items():
        limit_range += percentage
        if random_value < limit_range:
            return link

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = {}
    ranks_old = {}
    DELTA = 0.001
    max_difference = 1
    # Initializing the ranks dictionary
    for key in corpus:
        ranks[key] = 1 / len(corpus)
    

    while max_difference >= DELTA:

        # Update the old ranks dictionary
        ranks_old = ranks.copy()
        deltas = []
        max_difference = 1

        for page in ranks:
        
            # The summation part of the formula is calculated
            summation = 0

            # We iterate through every possible page that could link to our page
            for possible_parent in corpus:
                # If it is linked, the formula is used
                if page in corpus[possible_parent]:
                    summation += ranks_old[possible_parent] / len(corpus[possible_parent])
                # If the page has no links, it is assume it contains a link to every page
                elif len(corpus[possible_parent]) == 0:
                    summation += ranks_old[possible_parent] / len(corpus)

            # formula:
            ranks[page] = ((1 - damping_factor) / len(corpus)) + damping_factor * summation
            # Calculate the difference between the new rank and the previous r
            deltas.append(abs(ranks[page] - ranks_old[page]))


        
        # Get new maximum difference
        max_difference = max(deltas)

    return ranks


if __name__ == "__main__":
    main()
