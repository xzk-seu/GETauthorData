import requests
import json
import random
from Logger import logger
import warnings
import time
import os
from multiprocessing import Pool
warnings.filterwarnings("ignore")

_MAXRETRY = 6
_ERRORMESSAGE = "id: {0} | Error: {1}"
_INFOMESSAGE = "id: {0} has done."
_RESULT_PATH = os.path.join(os.getcwd(), "result", "top100author")
_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'academic.microsoft.com',
    'Cookie': 'msacademic=25bcc582-e762-4073-a219-2742783e18cc; ai_user=iGCCu|2018-08-21T03:48:49.213Z; MC1=GUID=865157eb0f744a43b5c84d940f20405c' + str(random.randint(100, 200)) + '&HASH=8651&LV=201809&V=4&LU=1536480320543; AMCV_EA76ADE95776D2EC7F000101%40AdobeOrg=-894706358%7CMCIDTS%7C17800%7CMCMID%7C29525519319229170001339901827044472388%7CMCAAMLH-1538483649%7C11%7CMCAAMB-1538483649%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCCIDH%7C-629512180%7CMCOPTOUT-1537886049s%7CNONE%7CvVersion%7C2.3.0; aamoptsegs=aam%3Dtest; MUID=3CD3DE2F3E4762BF3FB5D2063A4761D8; ARRAffinity=8463499082e39d2b88debe78834cc4844d3316c54a3bab90504386ef74fc71c3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
}

proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
proxyUser = "HW2RF1Z9C18A526D"
proxyPass = "9323ABC212FF1BFA"
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}
_PROXIES = {
    "http": proxyMeta,
    "https": proxyMeta,
}


_HOST = 'https://academic.microsoft.com/api/search/GetEntityResults?correlationId=79cbcd7b-4903-41e0-9070-521a2af21680'
_SESSION = requests.session()


def _get_request(url, param=None):
    resp = _SESSION.get(
        url,
        params=param,
        headers=_HEADERS,
        # proxies=_PROXIES,
        # verify=False,
        timeout=random.choice(range(30, 100))
    )
    resp.encoding = "utf-8"
    if resp.status_code == 200:
        return resp.text
    else:
        raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))


def _post_request(url, data):
    resp = _SESSION.post(
        url,
        data=data,
        # params=param,
        headers=_HEADERS,
        # proxies=_PROXIES,
        # verify=False,
        timeout=random.choice(range(30, 100))
    )
    resp.encoding = "utf-8"
    if resp.status_code == 200:
        return resp.text
    else:
        raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))


def get_author_data(entity_id):
    tries = 0
    js = dict()
    param = {'entityId': entity_id}
    while tries < _MAXRETRY:
        tries += 1
        try:
            html = _get_request(_HOST, param)
            js = json.loads(html.strip())
            break
        except Exception as e:
            if tries < _MAXRETRY:
                logger.info(_ERRORMESSAGE.format(str(entity_id), str(e)) + " | tries: %d" % tries)
            else:
                logger.error(_ERRORMESSAGE.format(str(entity_id), str(e)) + " | tries: %d" % tries)
            time.sleep(tries)
    return js


def get_author_paper(entity_id, index):
    offset = 8
    data = {
        'Query':  "And(Ty='0',Composite(AA.AuId=%d))" % entity_id,
        'Filters': "Pt = '0'",
        'Limit': offset,
        'Offset': index * offset,
        'OrderBy': '',
        'SortAscending': 'false'
    }
    r = _post_request(_HOST, data)
    return r


if __name__ == '__main__':
    g = get_author_paper(2116639004, 0)
    publication_count = json.loads(g)['publicationResults']
    print(publication_count)
    print(len(publication_count['publications']))
    t = json.dumps(publication_count['publications'][0], indent=4)
    print(t)
    # for c in range(1, publication_count//8)
    # r = get_author_data(2116639004)
    # for k in r.keys():
    #     print(k)
    # print(r)
    # r = _get_request(url)
    # print(r)
