import os.path
from gzip import GzipFile
import zlib
from urllib2 import urlopen, URLError
from StringIO import StringIO


LOG = 'log_download.txt'


def download(accession):
    CHUNK_SIZE = 1024
    decompressor = zlib.decompressobj(16+zlib.MAX_WBITS)
    url = _construct_GPL_url(accession)
    response = _get_file_by_url(url, accession)
    if not response:
        return
    with open('downloaded/' + accession + '.txt', 'wb+', encoding='utf-8') as f:
        while True:
            bin_chunk = response.read(CHUNK_SIZE)
            if not bin_chunk:
                break
            string = decompressor.decompress(bin_chunk)
            f.write(string)
        print('Downloaded ' + accession)


def _get_file_by_url(url, accession, attempts=5):
    response = None
    f = open(LOG, 'a', encoding='utf-8')
    while attempts > 0:
        try:
            response = urlopen(url)
        except URLError as e:
            pass
        if response is not None:
            break
        else:
            attempts -= 1
    else:
        f.write('Download failure ' + accession + '\n')
    f.close()
    return response


def _unzip(compressed_string):
    f = StringIO(compressed_string)
    decompressed = GzipFile(fileobj=f)
    return decompressed.read()


def _construct_GPL_url(accession):
    number_digits = len(accession) - 3;    ## "GPL" is of length 3
    if number_digits < 4:
        folder = accession[:3] + "nnn"
    elif 3 < number_digits < 5 :
        folder = accession[:4] + "nnn"
    else:
        folder = accession[:5] + "nnn"
    #url = '/'.join(["ftp://ftp.ncbi.nlm.nih.gov/geo/platforms", 
    #                folder,
    #                accession,
    #                "annot",
    #                accession + ".annot.gz"])
    url = 'ftp://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL11nnn/GPL11154/soft/'
    return url


# ftp://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL11nnn/GPL11154/soft/GPL11154_family.soft.gz
# ftp://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL11nnn/GPL11154/annot/GPL11154.annot.gzi
if __name__ == '__main__':
    f = open(LOG, 'w+', encoding='utf-8')
    f.close()

    f = open('input.txt', encoding='utf-8')
    for l in f:
        line = l.strip()
        download(line)
    f.close()
