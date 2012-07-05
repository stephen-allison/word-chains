from collections import defaultdict
import sys
import string
import heapq

def make_graph(n):
    with open('/usr/share/dict/words') as f:
        words = set(word.lower() for word in f.read().splitlines() if len(word) == n)
    print 'there are '+str(len(words))+' words of this length'
    graph = defaultdict(list)
    for word in words:
        graph[word] = Node(word,similar_words(word, words))
    return graph

def similar_words(word, words):
    sim_words = set()
    for i in range(len(word)):
        for c in string.ascii_lowercase:
            new_word = word[:i]+c+word[i+1:]
            if new_word in words and new_word != word:
                sim_words.add(new_word)
    return sim_words

def walk(graph, start, end):
    heap = []
     
    start_node = graph[start]
    if not start_node:
        print 'no path from '+start
        return []
    end_node = graph[end]
    if not end_node:
        print 'no path to '+end
        return []

    start_node.dist = 0

    for n in graph.values():
        heapq.heappush(heap,n)
    
    unvisited = set(graph.values())
    
    while len(unvisited) > 0:
        node = heapq.heappop(heap)

        for n in node.neighbours:
            neighbour = graph[n]
            new_dist = 1 + node.dist
            if new_dist < neighbour.dist:
                neighbour.dist = new_dist
                neighbour.previous = node
        unvisited.remove(node)
        heap.sort()
        
    path = []
    node = graph[end]
    while True:
        path.append(node.word)
        print node
        if node.word == start:
            break
        node = node.previous
    path.reverse()
    return  path

class Node:
    def __init__(self,word,neighbours):
        self.word = word
        self.neighbours = neighbours
        self.dist = float('inf')
        self.previous = None

    def __lt__(self,other):
        return self.dist < other.dist

    def __le__(self,other):
        return self.dist <= other.dist

    def __eq__(self,other):
        return self.dist == other.dist

    def __ne__(self,other):
        return self.dist != other.dist

    def __ge__(self,other):
        return self.dist >= other.dist

    def __gt__(self,other):
        return self.dist > other.dist

    def __str__(self):
        return self.word+" ("+str(self.dist)+")"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return self.word.__hash__()




def solve(start_word, end_word):
    assert len(start_word) == len(end_word)
    graph = make_graph(len(start_word))
    return walk(graph, start_word, end_word)

def find(start, finish):
    print " -> ".join(solve(start,finish))

if __name__ == "__main__":
    start_word, end_word = sys.argv[1:]
    find(start_word, end_word)
