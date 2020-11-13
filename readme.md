# How To Use the Program

## Link Budget Program
### Setting up
1. Software required: 
 
    1.1  Microsoft Access, Microsoft Access ODBC Drive (32-bit), python3-x 32 bit.

2. Add python3-x 32-bit to your cmd path.
3. Download the file, open the directory contain `requirement.txt` in the command line, type 

    `pip install -r requirement.txt`
4. Put the required earth station and satellite mdb file into the directory

5. Run `python main.py`

### Program flow
1. User will be prompted uplink/downlink
2. User will have to select the correct mdb file for earth station and satellite
3. The program will display the beam available for link budget analysis
4. Select the correspondig receiving/transmitting link
5. User will be promped to input the additional losses, e.g. cable, rain, path...
6. A tablulated result showing the link budget at the end will be provided.
7. User can choose to perform the analysis for the next link. If not, press `N + Enter` to exist the program.

### Future work
1. Save the result to another mdb file or csv file.

## DCT Program
1. Software required: MatLab.
2. Just run dct.m in MatLab.