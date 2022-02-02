import json
from collections import deque


def phrasel_search(P, Queries):
    # Write your solution here
    ans = []
    suffix_tree = {}
    extra_token_limit = 1
    for phrase in P:
        tree = suffix_tree
        #replacing all '$' in our strings handles possibility of interfering with
        #use of '$' as phrase-ending character
        phrase.replace('$', '')
        words = phrase.split(' ')
        words.append('$')
        for word in words:
            tree = tree.setdefault(word, {})
    for query in Queries:
        query_tokens = query.split(' ')
        query_phrases = []
        for start_index, query_token in enumerate(query_tokens):
            tree = suffix_tree
            current_phrase = deque()
            current_index = start_index
            extra_tokens = 0
            current_phrase.append(query_token)
            
            #loop breaks if the current phrase queue is empty for safety
            while current_phrase:
                current_word = current_phrase.pop()
                if tree.get(current_word):
                    tree = tree.get(current_word)
                    current_phrase.append(current_word)
                    if tree.get("$") == {}:
                        # the following conditional is necessary -- it handles cases of degenerate phrases
                        # i.e., a phrase 'field example' and 'field example pop' should return
                        # field example and field example pop. In degenerate cases,
                        #more than 1 key will be present.
                        if len(tree.keys()) == 1:
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
                if current_index < len(query_tokens):
                    current_phrase.append(query_tokens[current_index])
        if query_phrases:
            ans.append(query_phrases)

    return ans

if __name__ == "__main__":
    with open('sample.json', 'r') as f:
        sample_data = json.loads(f.read())
        P, Queries = sample_data['phrases'], sample_data['queries']
        returned_ans = phrasel_search(P, Queries)
        print('============= ALL TEST PASSED SUCCESSFULLY ===============')
