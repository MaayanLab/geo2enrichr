"""Downloads GEO SOFT files.
"""


from gzip import GzipFile
import zlib
from urllib.request import urlopen, URLError
from io import StringIO

from g2e.exceptions import SoftFileParseException


def download(accession, downloaded_file_path):
    """Downloads GEO file based on accession number. Side effect is a
    downloaded SOFT file on disk.

    For reading and unzipping binary chunks, see:
        http://stackoverflow.com/a/27053335/1830334
        http://stackoverflow.com/a/2424549/1830334
    """
    CHUNK_SIZE = 1024
    decompressor = zlib.decompressobj(16+zlib.MAX_WBITS)

    if 'GDS' in accession:
        url = _construct_GDS_url(accession)
    else:
        url = _construct_GSE_url(accession)
    response = _get_file_by_url(url)
    
    with open(downloaded_file_path, 'w+') as f:
        while True:
            bin_chunk = response.read(CHUNK_SIZE)
            if not bin_chunk:
                break
            string = decompressor.decompress(bin_chunk)
            f.write(string)


def _get_file_by_url(url, attempts=5):
    """Attempts to get the file from URL. Tries 5 times before giving up.
    """
    print('Downloading GEO SOFT file from: ' + url)
    while attempts > 0:
        try:
            response = urlopen(url)
        except URLError as e:
            message = 'Failed to download data from GEO.'
            raise SoftFileParseException(message,
                                         python_error=e,
                                         status_code=404)
        if response is not None:
            break
        else:
            attempts -= 1
    else:
        raise IOError('urllib2 failed 5x to download the file.')
    return response


def _unzip(compressed_string):
    """Unzips the file without allowing it to touch the disk.
    """
    f = StringIO(compressed_string)
    decompressed = GzipFile(fileobj=f)
    return decompressed.read()


def _construct_GDS_url(accession):
    url = $$('a[href^="ftp://"]')[0].href
    return url


def _construct_GSE_url(accession):
    url = $('a[href^="ftp://"]')[0].href
    return url
