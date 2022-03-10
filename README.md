# parse-hamnosys
Sign language HamNoSys notation parsing tool.

## Usage
```
$ python parse-hamnosys.py -sf <source_file> -df <destination_file>
```

## Usage example
```
$ python parse-hamnosys.py -sf hamnosys_example.txt -df hamnosys_parsed.txt
```

## Source file format
Default input file format is defined by the [HearAI](https://github.com/hearai/hearai) project requrements. As in[hamnosys_example.txt](hamnosys_example.txt) parser requires a file that has 6 columns separated with a space sign " ". Due to this, if any of the columns contains space, it must be removed or replaced (for example with "_" sign) before passing to the parser. Parsers operates only on HamNoSys notation, that is stored in the last (6th) column. It shall start with HamNoSys sign (No quote nor apostrophe sign is allowed).
Input file columns and description:
* Name - name of a video file that given notation refers to
* Start - sign start time (on a video)
* End - sign end time (on a vide)
* Dict - word number in a dictionary
* Word - translation to a spoken language
* Hamnosys - Notation 

## Destination File format
Destination file consists of following columns separated by the space " " sign:
* Name - name of a video file that given notation refers to, directly copied from source file
* Start - sign start time (on a video), directly copied from source file
* End - sign end time (on a vide), directly copied from source file
* Symmetry operator - Number that represents one of the classes (please refer to json file), parsed from notation
* Dominant - Handshape - Baseform - Number that represents one of the classes (please refer to json file), parsed from notation
* Dominant - Handshape - Thumb position - Number that represents one of the classes (please refer to json file), parsed from notation
* Dominant - Handshape - bending - Number that represents one of the classes (please refer to json file), parsed from notation
* Dominant - Handposition - extended finger direction - Number that represents one of the classes (please refer to json file), parsed from notation
* Dominant - Handposition - palm orientation - Number that represents one of the classes (please refer to json file), parsed from notation
* Dominant - Handposition - LR - Number that represents one of the classes (please refer to json file), parsed from notation
* Dominant - Handposition - TB - Number that represents one of the classes (please refer to json file), parsed from notation
* Dominant - Handposition - Distance - Number that represents one of the classes (please refer to json file), parsed from notation

## hamnosys_example.txt
File created using [Korpusowy słownik polskiego języka migowego](https://www.slownikpjm.uw.edu.pl/)
Joanna Łacheta, Małgorzata Czajkowska-Kisil, Jadwiga Linde-Usiekniewicz, Paweł Rutkowski (red.), 2016, Korpusowy słownik polskiego języka migowego, Warszawa: Wydział Polonistyki Uniwersytetu Warszawskiego, ISBN: 978-83-64111-49-5 (publikacja online).

## Font
HamNoSys font is required to be installed to properly undestand subcesction [Classes](#classes).
It can be downloaded directly from [DSG Corpus](https://www.sign-lang.uni-hamburg.de/dgs-korpus/index.php/hamnosys-97.html) website.

## Classes
### Symmetry operator
Symmetry operator class consists of 9 symbols (0 to 8). Following list represents class number to symbol mapping:
0.  None
1.  
2.  
3.  
4.  
5.  
6.  
7.  
8.  

###  Handshape - Baseform
Handshape - baseform class consists of 12 symbols (0 to 11). Following list represents class number to symbol mapping:
1.  
2.  
3.  
4.  
5.  
6.  
7.  
8.  
9.  
10.  
11.  
12.  

###  Handshape - Thumb position
Handshape - thumb position class consists of 4 symbols (0 to 3). Following list represents class number to symbol mapping ([Handshape - base form sign](#handshape---baseform) sign is used only as a reference):
0.  None
1.  
2.  
3.  

###  Handshape - Bending
Handshape - bending class consists of 6 symbols (0 to 5). Following list represents class number to symbol mapping ([Handshape - base form sign](#handshape---baseform) sign is used only as a reference):
0.   (none) 
1.  
2.  
3.  
4.  
5.  

###  Handposition - Extended finger direction
Handposition - extended finger direction class consists of 18 symbols (0 to 17). Following list represents class number to symbol mapping:
0.  
1.  
2.  
3.  
4.  
5.  
6.  
7.  
8.  
9.  
10.  
11.  
12.  
13.  
14.  
15.  
16.  
17.  
###  Handposition - Palm orientation
Handshape - palm orientation class consists of 8 symbols (0 to 7). Following list represents class number to symbol mapping:
0.  
1.  
2.  
3.  
4.  
5.  
6.  
7.  

###  Handposition - Left/Right
Handposition - left/right class consists of 5 symbols (0 to 4). Following list represents class number to symbol mapping ([Handposition - Top/Bottom sign](#handposition---topbottom) is used only as a reference):
0.   - left to the left
1.   - left
2.   - center
3.   - right
4.   - right to the right

###  Handposition - Top/Bottom
Handposition - top/bottom class consists of 37 symbols (0 to 36). Following list represents class number to symbol mapping:
0.  None
1.  
2.  
3.  
4.  
5.  
6.  
7.  
8.  
9.  
10.  
11.  
12.  
13.  
14.  
15.  
16.  
17.  
18.  
19.  
20.  
21.  
22.  
23.  
24.  
25.  
26.  
27.  
28.  
29.  
30.  
31.  
32.  
33.  
34.  
35.  
36.  

###  Handposition - Distance
Handposition - top/bottom class consists of 37 symbols (0 to 36). Following list represents class number to symbol mapping:
1.  
2.  
3.  
4.  None
5.  
6.  
7.  

## Read more
* [Introduction to HamNoSys](https://www.hearai.pl/post/4-hamnosys/)
* [Introduction to HamNoSys Part 2](https://www.hearai.pl/post/5-hamnosys2/)