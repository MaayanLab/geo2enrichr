GEO2Enrichr
===========

GDS example:
http://www.ncbi.nlm.nih.gov/sites/GDSbrowser

GSE example:
http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE1122

To get JSON
retmode=json

To set number of IDs returned
retmax=X


TODO:
- Set some global flag that rips GEO2Enrichr completely out of DOM if anything critical happens?


- To run, call the function: `process_SOFT_list('accessionlist_example.txt', use_chdir=True, getFuzzy=False)`.
- Characteristic direction results go into subfolder "ChDir_Lists".
- T-test results go into subfolder "ANOVA".

A sample query sequence is:
1. http://localhost:8083/g2e/dlgeo?accession=GDS670
2. http://localhost:8083/g2e/diffexp?filename=GDS670.soft&platform=GPL80&control=GSM18403-GSM18404-GSM18405&experimental=GSM18406-GSM18407-GSM18408
3. http://localhost:8083/g2e/static/genefiles/1415747594_geofiles_down_genes.txt


Example platform to probe ID mapping:
http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?view=data&acc=GPL80&id=41379&db=GeoDb_blob32