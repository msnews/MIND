import grequests
import requests

def request(doc, size):
    tasks = []
    index = 0
    res = []
    for i in doc:
        index += 1
        res.append(requests.get(i[1])) 
        if index % 1000 == 0:
           print(index)
    return res

    


if __name__ == '__main__':
    root_dir = './no_body_urls.txt'

    doc = []
    with open(root_dir, 'r') as f:
        for l in f:
            nid, url = l.strip('\n').split('\t')
            doc.append([nid, url])
            
    res = request(doc[:1000], size=128)
    not_access = []
    
    for i, r in zip(range(len(res)), res):
        if r.status_code != 200:
            not_access.append([doc[i][0], doc[i][1]])
    
    with open('./not-access-urls.txt', 'w') as f:
        for nid, url in not_access:
            f.write("{}\t{}\n".format(nid, url))



        
