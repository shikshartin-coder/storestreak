def compute_lps(pattern):
    # Longest Proper Prefix that is suffix array
    lps = [0] * len(pattern)

    prefi = 0
    for i in range(1, len(pattern)):
        
        # Phase 3: roll the prefix pointer back until match or 
        # beginning of pattern is reached
        while prefi and pattern[i] != pattern[prefi]:
            prefi = lps[prefi - 1]

        # Phase 2: if match, record the LSP for the current `i`
        # and move prefix pointer
        if pattern[prefi] == pattern[i]:
            prefi += 1
            lps[i] = prefi

        # Phase 1: is implicit here because of the for loop and 
        # conditions considered above

    return lps

def kmp(pattern, text):
    match_indices = []
    pattern_lps = compute_lps(pattern)

    patterni = 0
    for i, ch in enumerate(text):
        
        # Phase 3: if a mismatch was found, roll back the pattern
        # index using the information in LPS
        while patterni and pattern[patterni] != ch:
            patterni = pattern_lps[patterni - 1]

        # Phase 2: if match
        if pattern[patterni] == ch:
            # If the end of a pattern is reached, record a result
            # and use infromation in LSP array to shift the index
            if patterni == len(pattern) - 1:
                match_indices.append(i - patterni)
                break
            
            else:
                # Move the pattern index forward
                patterni += 1

        # Phase 1: is implicit here because of the for loop and 
        # conditions considered above
    return match_indices

def search_pattern(pattern, search_objects_list):
    if pattern == None or pattern == "":
        return []
    tuples_list = []
    return_search_list = []
    for search_object in search_objects_list:
        search_string = search_object['name']
        match_indices = kmp(pattern.lower(), search_string.lower().replace(" ",""))
        if match_indices != []:
            tuples_list.append((match_indices[0],search_object))
    tuples_list_sorted = sorted(tuples_list, key=lambda tup: tup[0])
    
    for index, tuple in enumerate(tuples_list_sorted):
        return_search_list.append((tuple[1]))

    return return_search_list
