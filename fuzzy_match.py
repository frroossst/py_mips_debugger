def get_closest_match_from_list(string, lst):
    lst = [str(item) for item in lst]
    closest_match = None
    highest_similarity = -1
    
    for item in lst:
        similarity = calculate_similarity(string, item)
        
        if similarity > highest_similarity:
            closest_match = item
            highest_similarity = similarity
    
    return closest_match

def calculate_similarity(str1, str2):
    # Convert both strings to lowercase
    str1 = str1.lower()
    str2 = str2.lower()

    # Calculate the Levenshtein distance between the two strings
    distance = 0
    for i in range(min(len(str1), len(str2))):
        if str1[i] != str2[i]:
            distance += 1
    distance += abs(len(str1) - len(str2))

    # Calculate the similarity between the two strings
    similarity = 1 - (distance / max(len(str1), len(str2)))

    return similarity
