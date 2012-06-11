from collections import defaultdict, deque
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

#def walk(start_node, end_node, graph, visited=set(), chain=[]):
#    graph_words = graph[start_node]
#    if end_node in graph_words:
#        print "win"
#        return
#    for word in graph_words:
#        visited.add(word)

#def walk(graph, start, end):
#    paths = deque([[start]])
#    while True:
#        path = paths.popleft()
#        current_node = path[-1]
#        next_nodes = graph[current_node]
#        if end in next_nodes:
#            return path + [end]
#        paths.extend([path + [node] for node in next_nodes])


def walk(graph, start, end):
    heap = []
    
    start_node = graph[start]
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

def make_node(word,neighbours):
    return {'word':word, 'neighbours':neighbours}


def fail(start,end):
    print "No path found from "+start+" to "+end+""

def get_path_heap_element(path, end):
    last_in_path = path[-1]
    d = distance(last_in_path, end)
    return (d, path)

def distance(word1, word2):
    if len(word1) != len(word2):
        return float('inf')
    deltas = 0
    for i in range(len(word1)):
        a = word1[i] 
        b = word2[i]
        if a != b:
            deltas = deltas + 1
    return deltas


def solve(start_word, end_word):
    assert len(start_word) == len(end_word)
    graph = make_graph(len(start_word))
    return walk(graph, start_word, end_word)

def wordchain(start, finish):
    print " -> ".join(solve(start,finish))

if __name__ == "__main__":
    start_word, end_word = sys.argv[1:]
    wordchain(start_word, end_word)
