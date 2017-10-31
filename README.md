
Requirements
------------
This coding challenge has been developed in Python 3.4.4 version.
Python 3.x is required to run this code

Python modules that are required and imported during code execution:
sys,
collections,
csv,
datetime,
statistics


Approach
--------------------------------
Decided to use Generators to iterate through the input file and process it 'lazily' line by line. This would enable us to process huge files that would not fit in memory. This function uses the 'yield' command to yield a value, remember its state so after the value has been dealt with it yields the next value and so on..

Filtered out unnecessary columns before performing computations on each row

Used dictionary data structures:
1) to keep track of the record keys (CMTE_ID, ZIP_CODE) and (CMTE_ID, TRANSACTION_DT)
2) to compute the values to store along with the keys - the running median, transaction counts, total contributions

As each row is read from the input file, the computations that are required for both the output files is performed - medianvals_by_zip and medianvals_by_date

Additionally, used list of lists data structure to store the computations (running median, total etc) required for medianvals_by_zip output file. The list data structure would help preserve the order of the lines appearing in the input file.

Alternative Approach to be Explored Further
-------------------------------------------
Process the input data file in chunks instead of row by row. The Pandas library has some useful functions:
The pandas.read_csv() has a chunksize parameter that we can use to specify the number of rows to be processed in each chunk

Example code:
filechunk_iter = pandas.read_csv(<inputfile>, chunksize=1000)
for chunk in filechunk_iter:
   <process chunk>

But this approach would require code that can work only on a portion of the data file, store intermediate results and combine these results in the end

Source Code and Run Instructions
--------------------------------
The source code is in the file 'find_political_donors.py', located in the src folder
The shell script 'run.sh' contains the following command which will execute the code:

python ./src/find_political_donors.py ./input/itcont.txt ./output/medianvals_by_zip.txt ./output/medianvals_by_date.txt

Flow of Execution
-----------------
The 'main()' module defines the structure of the input file and outlines the fields in it. It calls the 'parse_input()'' module and passes the input filename parameter to it. The 'parse_input()' module in turn calls the 'read_input()' module that reads the input file and hands over a row at a time to be processed. Once one row has been processed, the next row is handed over.
The 'parse_input()' module performs the needed computations and returns the following to the 'main()' module:
1) list of lists data structure to be written out to the medianvals_by_zip output file  
2) dictionary data structure to be sorted and then written out to the median_amt_by_date output file
