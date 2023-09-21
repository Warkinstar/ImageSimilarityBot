import difflib


def compare_hash(hash1, hash2):
    """Сравнивает два хэша, чем меньше возвращаемое значение тем более похоже два хеша-изображений"""
    l = len(hash1)
    i = 0
    count = 0
    while i < l:
        if hash1[i] != hash2[i]:
            count = count + 1
        i = i + 1

    return count
