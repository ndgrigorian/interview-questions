import json
from collections import deque


class SuffixTree:

    class Node:
        def __init__(self, lab):
            self.label = lab
            self.next_tokens = {}

    def __init__(self, phrases):
        self.root = self.Node(None)
        for phrase in phrases:
            # replacing all '$' in our strings handles possibility of interfering with
            # use of '$' as phrase-ending character
            phrase.replace('$', '')
            tokens = phrase.split(' ')
            tokens.append('$')
            current_node = self.root
            for token in tokens:
                if not current_node.next_tokens.get(token):
                    current_node.next_tokens[token] = self.Node(token)
                    current_node = current_node.next_tokens[token]
                else:
                    current_node = current_node.next_tokens[token]

    def tree_query(self, query, extra_token_limit = 0):
        query_phrases = []
        for start_index, token in enumerate(query):
            current_phrase = deque()
            current_index = start_index
            current_phrase.append(token)
            current_node = self.root
            extra_tokens = 0
            while current_phrase:
                current_word = current_phrase.pop()
                if current_node.next_tokens.get(current_word):
                    current_node = current_node.next_tokens.get(current_word)
                    current_phrase.append(current_word)
                    if current_node.next_tokens.get("$"):
                        # the following conditional is necessary -- it handles cases of degenerate phrases
                        # i.e., a phrase 'field example' and 'field example pop' should return
                        # field example and field example pop. In degenerate cases,
                        # more than 1 key will be present.
                        if len(current_node.next_tokens.keys()) == 1:
                            query_phrases.append(" ".join(list(current_phrase)))
                            break
                        else:
                            query_phrases.append(" ".join(list(current_phrase)))
                else:
                    extra_tokens += 1
                    if not current_phrase or extra_tokens > extra_token_limit:
                        break
                    current_phrase.append(current_word)

                current_index += 1
                if current_index < len(query):
                    current_phrase.append(query[current_index])
        return query_phrases


def phrasel_search(P, Queries):
    # Write your solution here
    ans = []
    extra_token_limit = 1
    suffix_tree = SuffixTree(P)

    for query in Queries:
        query_tokens = query.split(' ')
        query_phrases = suffix_tree.tree_query(query_tokens, extra_token_limit)
        if query_phrases:
            ans.append(query_phrases)
    return ans


if __name__ == "__main__":
    with open('sample.json', 'r') as f:
        sample_data = json.loads(f.read())
        P, Queries = sample_data['phrases'], sample_data['queries']
        returned_ans = phrasel_search(P, Queries)
        print('============= ALL TEST PASSED SUCCESSFULLY ===============')
