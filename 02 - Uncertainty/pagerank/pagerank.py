import os
import random
import re
import sys
import numpy as np

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
    damping_prob = (1 - damping_factor) * (1 / len(corpus.keys()))
    distribution = {key: damping_prob for key in corpus.keys()}

    if corpus[page]:
        for value in corpus[page]:
            distribution[value] += damping_factor * (1 / len(corpus[page]))
    else:
        for key in distribution.keys():
            distribution[key] += damping_factor * (1 / len(corpus.keys()))

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    ranking = {key: 0 for key in corpus.keys()}

    curr_page = list(corpus.keys())[random.randint(0, len(corpus.keys())-1)]

    for _ in range(n):
        curr_distribution = transition_model(corpus, curr_page, damping_factor)
        ranking[curr_page] += 1
        curr_page = np.random.choice(
            list(curr_distribution.keys()),
            1,
            p=list(curr_distribution.values())
        )[0]

    for key in ranking.keys():
        ranking[key] /= n

    return ranking


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = len(corpus)
    base = ((1 - damping_factor) / pages)

    curr_distribution = {key: 1/pages for key in corpus.keys()}
    next_distribution = {key: 0 for key in corpus.keys()}
    max_change = 1 / pages

    while max_change > 0.001:
        max_change = 0

        for page in corpus.keys():
            page_prob = 0
            for alt_page in corpus.keys():
                # Base case, no connecting pages
                if len(corpus[alt_page]) == 0:
                    page_prob += curr_distribution[alt_page] * (1 / pages)

                elif page in corpus[alt_page]:
                    page_prob += curr_distribution[alt_page] / len(corpus[alt_page])
            # Add current pages new probability to the new distribution
            next_distribution[page] = base + (damping_factor * page_prob)

        # Normalise features and adjust max change rankings
        normalisation = sum(next_distribution.values())
        for key in next_distribution.keys():
            next_distribution[key] /= normalisation
            change = abs(next_distribution[key] - curr_distribution[key])
            if change > max_change:
                max_change = change

        curr_distribution = next_distribution.copy()

    return curr_distribution


if __name__ == "__main__":
    main()
