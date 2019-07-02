import csv
import json
import requests


def main():
    with open('sigs2accessions.csv') as f, open('out.txt', 'w+') as o:
        reader = csv.reader(f)
        for line in reader:
            extraction_id = line[0]
            is_geo = line[1] == '0'
            if is_geo:
                continue

            accession = line[2]
            url = get_url(accession)
            sess = requests.session()
            response = sess.get(url)
            if response.ok:
                try:
                    data = json.loads(response.text)
                    id = accession[3:]

                    title = data['result'][id]['title']
                    summary = data['result'][id]['summary']

                    out_line = '\t'.join([extraction_id, title, summary])
                    print(out_line)
                    o.write(out_line)
                except KeyError:
                    print('--------------- key error')
                    o.write('error with %s' % extraction_id)

def get_url(accession):
    is_gds = 'GDS' in accession
    BASE_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?&retmax=1&retmode=json'
    db = 'gds' if is_gds else 'geoprofiles'
    return '&'.join([BASE_URL, 'db=' + db, 'id=' + accession[3:]])


if __name__ == '__main__':
    main()