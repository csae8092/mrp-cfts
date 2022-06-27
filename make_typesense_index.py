import glob
import os
import ciso8601
import time

from acdh_cfts_pyutils import CFTS_COLLECTION
from acdh_tei_pyutils.tei import TeiReader
from tqdm import tqdm

files = sorted(glob.glob('./data/editions/*-P-*.xml'))
project_name = "mrp"

records = []
for x in tqdm(files, total=len(files)):
    record = {}
    record['project'] = "mrp"
    record['id'] = os.path.split(x)[-1].replace('.xml', '')
    record['rec_id'] = record['id']
    record['resolver'] = f"https://mrp.oeaw.ac.at/pages/show.html?document={record['id']}.xml"
    doc = TeiReader(x)
    record['title'] = " ".join(" ".join(doc.any_xpath('.//tei:body/tei:div/tei:head[1]//text()')).split())
    try:
        date = doc.any_xpath('.//tei:meeting[1]/tei:date[1]/@when')[0]
    except IndexError:
        date = None
    if date is not None:
        record['year'] = int(date[:4])
        if len(date) == 10:
            ts = ciso8601.parse_datetime(date)
        else:
            ts = ciso8601.parse_datetime(f"{record['year']}-01-01")
    else:
        record['year'] = 1000
        ts = ciso8601.parse_datetime("1000-01-01")
    record['date'] = int(time.mktime(ts.timetuple()))
    body = doc.any_xpath('.//tei:body')[0]
    record['full_text'] = " ".join(''.join(body.itertext()).split())
    records.append(record)

make_index = CFTS_COLLECTION.documents.import_(records, {'action': 'upsert'})
print(make_index)
print('done with central indexing')
