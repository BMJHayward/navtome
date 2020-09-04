# Nav Tome (wip)
For navigating the Tomes of biology: genomes, proteomes etc...
Currently supports fasta and genbank files

Create a virtual environment with python 3.7 or newer. Virtualenv/Pip is recommended over
Conda as there are some issues with Qt and its dependencies.  

To setup, open your preferred terminal and type:  

`pip install -r src/main/python/requirements.txt`  

If you're on windows, add this as well:  

`pip install -r src/main/python/requirementsWindows.txt`  

Then:  

`fbs run`  


#### Contains:
 - a basic web browser to download data from NCBI
 - a parser for the various file types to extract sequence data
 - basic machine learning algorithms
 - distance matrices
 - translation tables
 - naive backtranslation
 - ngrams, trigrams, nucleotide and peptide distribution
 - many sequence similarity calculations
   - cosine
   - levenshtein
   - least common sequence/substrings
   - tversky
   - zlib



