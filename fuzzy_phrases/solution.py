import json
from collections import deque


def phrasel_search(P, Queries):
    # Write your solution here
    ans = []
    suffix_tree = {}
    
    #build a suffix-tree-like structure from the given phrases
    #the keys of the next dictionary are the possible next words
    #a next key of "$" indicates the previous word was terminal for a phrase
    for phrase in P:
        tree = suffix_tree
        words = phrase.split(' ')
        words.append('$')
        for word in words:
            tree = tree.setdefault(word, {})
            
    #now iterate over queries, splitting up 
    for query in Queries:
        query_tokens = query.split(' ')
        query_phrases = []
        
        for start_index, query_token in enumerate(query_tokens):
            tree = suffix_tree
            current_phrase = deque()
            current_index = start_index
            extra_words = 0
            
            while current_index < len(query_tokens):
                current_phrase.append(query_tokens[current_index])
                test_word = current_phrase.pop()
                
                if tree.get(test_word):
                    tree = tree.get(test_word)
                    
                    if tree.get("$") == {}:
                        current_phrase.append(test_word)
                        query_phrases.append(" ".join(list(current_phrase)))
                        break
                else:
                    extra_words += 1
                    if not current_phrase or extra_words > 1:
                        break
                current_phrase.append(test_word)
                current_index += 1
                
        if query_phrases:
            ans.append(query_phrases)
    return ans

if __name__ == "__main__":
    with open('sample.json', 'r') as f:
        sample_data = json.loads(f.read())
        P, Queries = sample_data['phrases'], sample_data['queries']
        returned_ans = phrasel_search(P, Queries)
        print('============= ALL TEST PASSED SUCCESSFULLY ===============')
