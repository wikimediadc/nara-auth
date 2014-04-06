import sys, pickle, pprint, os
from wikitools import wiki
from wikitools import api
# create a Wiki object

pp = pprint.PrettyPrinter(indent=2)

site = wiki.Wiki("https://www.wikidata.org/w/api.php") # login - required for read-restricted wikis
pw = open('pw').read().strip()
site.login("US National Archives bot", pw)
# define the params for the query

def search_query(param):
    d =  {'action':'wbsearchentities',
            'search': param,
            'language': 'en',
            }
    return d

def edit_query(_id, data, tok):
    """
    data must be a string starting with " and ending with "
    """
    d = {'action': 'wbcreateclaim',
            'summary': 'an automated edit made by nick',
            'entity': _id,
            'property': 'P1223',
            'snaktype': 'value',
            'value': data,
            'token': tok,
            }
    return d

def get_token():
    d = {'action': 'tokens', 'type': 'edit'}
    request = api.APIRequest(site, d)
    resp = request.query()
    api.SET_TOKEN = True
    e_token = resp['tokens']['edittoken']
    api.EDIT_TOKEN = e_token
    return e_token

def search():
    path = 'nara-auth/smalllist.p'
    nara_records = pickle.load(open(path))
    found = []
    mults = []
    for i in range(0, len(nara_records)):
        elem = nara_records[i]
        dn = elem['display-name']
        q = search_query(dn)
        request = api.APIRequest(site, q)
        result = request.query()
        out_lst = result['search']
        if len(out_lst) == 1:
            elem['wikidata_id'] = out_lst[0]['id']
            found.append(elem)
            pp.pprint(result)
        elif len(out_lst) > 1:
            mults.append({'possibles': out_lst,
                'actual': elem})
        else:
            pass
        #pp.pprint(elem['display-name'])
        store_dicts("wikidata-naras.p", found) 
        store_dicts("unknown-mults.p", mults) 
    pp.pprint(found)

def single_edit(_id, data, tok):
    """Edits a single claim returning the entity id of that claim."""
    tok = get_token()
    q = edit_query(_id, data, tok)
    request = api.APIRequest(site, q)
    result = request.query()
    pp.pprint(result)
    return result['claim']['id']

def mass_edit(number=False):
    """
    Pulls formatted nara dictionaries initialized with a wikidata_id and
    updates the item in wikidata with the correct nara orginazation
    identifier    
    """
    tok = get_token()
    nara_records = pickle.load(open("wikidata-naras.p"))
    if not number: number = len(nara_records)
    for i in range(0, number):
        rec = nara_records[i]
        org_id = rec['organization-id']
        dn = rec['display-name']
        data = '"' + org_id + '"'
        wd_id = rec['wikidata_id']
        print "EDITING: <wd:%s, nara:%s, %s>" % (wd_id, org_id, dn)
        ent_id = single_edit(wd_id, data, tok)
        #print "REFERENCING"
        # Not working yet
        #res = set_reference(ent_id, org_id, tok)
    print "Ran this many iterations:", len(range(0, number))

def set_reference(claim_id, org_id, token):
    """claim_id is an IRI for claims,
       org_id is the nara archive org id
       token is a login token
    Given a wikidata claim id create the appropriate reference."""
    q = {"action": "wbsetreference",
         "statement": claim_id,
         "token": token,
         "baserevid": 119268185,
         "index": 0,
        # The reference snak for the National Archives RA..... 
         "snaks": '{
                "P123": [{"snaktype": "value", "property":"P123", "datavalue": 
                                 {"type":"wikibase-entityid", "value":{"entity-type":"item","numeric-id":518155}}}
                        ],
                "P854": [{"snaktype": "value", "property":"P854","datavalue":
                                 {"type":"string","value":"http://research.archives.gov/organization/%s" % org_id}}
                        ],
                "P31": [{"snaktype": "value", "property":"P31","datavalue":
                                 {"type":"wikibase-entityid","value":{"entity-type":"item","numeric-id":36524}}}
                       ],
                "P813": [{"snak": "value", "property":"P813","datavalue":
                                 {"type":"time","value": {"time": "+00000002014-04-06T00:00:00Z", "timezone": 0,"before": 0,"after": 0,"precision": 11,"calendarmodel": "http://www.wikidata.org/entity/Q1985727"}}}
                       ],
                "P364": [{"snaktype":"value", "property":"P364","datavalue":
                                 {"type":"wikibase-entityid","value":{"entity-type":"item","numeric-id":1860}}}
                       ]
                }'
            }
    result = api.APIRequest(site, q).query()
    pp.pprint(result)



def store_dicts(filename, objs):
    f = open(filename, 'w')
    pickle.dump(objs, f)

def deal_with_mults():
    """
    A command line program that presents information to deal with cases
    where multiple wikidata items are returned after searching wikidata
    using the display-name provided by the nara xml.
    """
    mults = pickle.load(open('unknown-mults.p'))
    correct = []
    for _dct in mults:
        print "="*30+"Query returned:"+"="*30
        i = 0
        nara_obj = _dct['actual']
        for poss in _dct["possibles"]:
            print("[%d]" % i)
            q = {'action': 'wbgetentities',
                    'ids:': _dct["possibles"][i]["id"],
                    'sites': 'enwiki'}
            resp = api.APIRequest(site, q).query()
            pp.pprint(resp)
            i += 1
        print("-"*30+"The NARA record:"+'-'*30)
        pp.pprint(nara_obj)
        choice = int(raw_input('Pick the wikidata item that fits best: '))
        if choice > len(_dct['possibles']):
            print "bad"
            continue
        nara_obj['wikidata_id'] = _dct["possibles"][choice]["id"]
        correct.append(nara_obj)
        store_dicts("fixed-mults.p", correct) 


if __name__ == '__main__':
    q, cmd = "", ""
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
    if cmd == "clean":
        tmp_files = ["./wikidata-naras.p",
                "./unknown-mults.p", 
                "./fixed-mults.p",]
        for f in tmp_files:
            try:
                os.remove(f)
            except OSError:
                pass
    if cmd == "search":
        search()
    if cmd == "mass_edit":
        mass_edit(3)
    if cmd == "one_edit":
        single_edit()
    if cmd == "deal_with_mults":
        deal_with_mults()
    if cmd == "create_ref":
        set_reference("Q1518467$DF5C5D13-F12D-4003-BB87-666B61323A46",
                142809, get_token())

