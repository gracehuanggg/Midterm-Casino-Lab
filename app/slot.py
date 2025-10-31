import random

def pull_lever():
    random_images = [4, 8, 12, 16]
    ret = []
    for i in range(3):
        ind = random.randint(0, len(random_images) - 1)
        ret.append(random_images[ind])
    return ret