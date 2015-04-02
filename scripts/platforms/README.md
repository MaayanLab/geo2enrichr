# platforms

These scripts handle mapping platform probe IDs to canonical human gene symbols. The scripts are run by following steps:

1. Place a newline-separated list of platforms (GPL...) in `input.txt`.
2. Run `python download.py` to download the appropriate platform files. Any errors will be logged to `log.txt`.
3. Run `python clean.py`. This will create new, cleaned copies of the GPL files in the `cleaned` directory. "Cleaned" means that all metadata and unnecessary columns have been removed. This script attempts to find the gene symbol column programmatically by searching for the left-most column with the string "gene symbol" (case insensitive). The resultant files will be tab-separated lists in which each line contains the platform, probe ID, and gene symbol.
4. Run `python convert.py`. This script ensures that all gene symbols are canonical human gene symbols. If they are not, it first checks a dictionary of synonyms, then mouse gene symbols, and then finally mouse synonyms. If the gene symbol is a mouse gene symbol, the script attempts to convert it to a canonical human gene symbol. If it fails to convert the gene symbol to a canonical human gene symbol, the script discards the line. If any file has less than 5000 gene symbols, it removes the file (from the `symbols` directory). It logs failures to `log_symbols.txt`.
5. Run `python concat.py` to concat the files in the `symbols` directory into a single output file `output.txt`. **This script will will not add it to the output file if it is already supported.** If you need to update an existing platform, you must manually override this guard.

Double check the log files and intermediate output files. If everything looks good, manually copy and paste `output.txt` to into `probe2gene.txt`.

Finally:

6. Run `js.py` to build a JavaScript array that is used by the front-end to tell immediately if a platform is supported or not.
