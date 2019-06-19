# GEO2Enrichr

#### What is GEO2Enrichr?

GEO2Enrichr is a browser extension and web application for extracting gene sets from the [Gene Expression Omnibus (GEO)](http://www.ncbi.nlm.nih.gov/geo/) and custom Simple Omnibus In Text (SOFT) files and then piping those lists to [Enrichr](http://amp.pharm.mssm.edu/Enrichr/), a gene set enrichment analysis tool. The web server and additional information can be found on the [Ma'ayan Lab's server](http://amp.pharm.mssm.edu/g2e/).

#### Where can I learn more?

[GEO2Enrichr: browser extension and server app to extract gene sets from GEO and analyze them for biological functions.](http://www.ncbi.nlm.nih.gov/pubmed/25971742) Gundersen GW, Jones MR, Rouillard AD, Kou Y, Monteiro CD, Feldmann AS, Hu KS, Ma'ayan A. Bioinformatics. 2015 Sep 15;31(18):3060-2. doi: 10.1093.

## For Ma'ayan Lab developers

#### How do I setup my development environment?
```bash
# first time: setup venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# before you start coding (when in a new terminal)
source venv/bin/activate
```

#### How do I test GEO2Enrichr?

Run `bash test.sh`

#### How do I deploy GEO2Enrichr?

See `DEPLOY.md`.

#### How do I configure GEO2Enrichr?
Create a config file at `g2e/config/config.ini`
```ini
[mode]
debug=true

[cookies]
secret_key=secret_key

[admin]
admin_key=admin_key

[db]
uri=mysql://user:pass@host:port/db?charset=utf8
```

#### How do I run GEO2Enrichr?
```bash
python run.py
# Go to http://localhost:8083/g2e/
```
