import grequests


def request(doc, size):
    tasks = []
    for i in doc:
        tasks.append(grequests.get(i[1]))
    
    for i in range(0, len(tasks), 1000):
        res = grequests.map(tasks[i:i+1000], size=size)
        print(i)
    return res

    


if __name__ == '__main__':
    root_dir = './no_body_urls.txt'

    doc = []
    with open(root_dir, 'r') as f:
        for l in f:
            nid, url = l.split('\t')
            doc.append([nid, url])
            
    res = request(doc, size=128)
    not_access = []
    
    for i, r in zip(range(len(res)), res):
        if r.status_code != 200:
            not_access.append([doc[i][0], doc[i][1]])
    
    with open('./not-access-urls.txt', 'w') as f:
        for nid, url in not_access:
            f.write("{}\t{}\n".format(nid, url))



        
