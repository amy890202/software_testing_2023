# Homework 3: Test for Stutter
Use “Stutter.py” for questions a-d. (A compilable version is available in https://cs.gmu.edu/~offutt/softwaretest/java/Stutter.java. A line-numbered version is in
https://cs.gmu.edu/~offutt/softwaretest/java/Stutter.num. )
(a) Draw control flow graphs for all the methods in “Stutter.py”.
(b) List all the call sites.
(c\) List all coupling du-pairs for each call site.
(d) Create test data to satisfy All-Coupling Uses Coverage for “Stutter.py“. (Informally, to cover all coupling du-pairs in (c\).)
> …
> Then we make sure that every def reaches all possible uses
> All-uses coverage (AUC): For each set of du-paths to uses S = du (ni, nj, v), TR contains at least one path d in S.
> …
> From Ch07-1 “Data Flow Test Criteria”


#### (a) Draw control flow graphs for all the methods in “Stutter.py”
##### def main():
![reference link](https://i.imgur.com/6XdsaT4.png)

##### def stut(inFile):
![](https://hackmd.io/_uploads/rJwKUuwN2.png)

##### def checkDupes(line):
![](https://hackmd.io/_uploads/ry6yDdP43.png)


##### def isDelimit(C\):
![](https://hackmd.io/_uploads/SyIFDuwE2.png)



#### (b) List all the call sites.



| 行數      | call site                 |
| -------- | ------------------------- |
| 103      | stut(inFile)      |
| 46       | isDelimit(c\) |
| 47       | checkDupes(linecnt)|
| 52       |  checkDupes(linecnt)  | 



#### (c\) List all coupling du-pairs for each call site.
Pairs of locations(method name, variable name, statement)
##### def stut(inFile):

| last def      | first use                 |
| -------- | ------------------------- |
| (main(), inFile, 95)       | (stut(), inFile, 41)      |
| (main(), inFile, 99)        | (stut(), inFile, 41) |
| (main(), inFile, 102)        | (stut(), inFile, 41)|

##### def isDelimit(C\):

| last def      | first use                 |
| -------- | ------------------------- |
| (stut(), c, 45)        | (isDelimit(), C, 82)      |

##### def checkDupes(line):
| last def      | first use                 |
| -------- | ------------------------- |
| (stut(), linecnt, 40)       | (checkDupes(), line, 68)      |
| (stut(), linecnt, 53)       | (checkDupes(), line, 68) |


(d) Create test data to satisfy All-Coupling Uses Coverage for “Stutter.py“. (Informally, to cover all coupling du-pairs in (c\).)





| len(sys.argv) | sys.argv[1] | content in inFile             |    coupling du-pairs  |                                                                                |
| ------------- | ----------- | ----------------------------- | ------------------------------ | ----------------------------------------------------------------------------------------------- |
| 1             |             | "SoftwareTesting" //sys.stdin | 95  # no file, use stdin       | 41 # while (inLine := inFile.readline()) != '':                                                 |
| 2             | ''          | "SoftwareTesting" //sys.stdin | 99 # no file name, use stdin   | 41 # while (inLine := inFile.readline()) != '':                                                 |
| 2             | "test.txt"  | "Software Testing"            | 102 # file name, open the file | 41 # while (inLine := inFile.readline()) != '':                                                 |
| 2             | "test.txt"  | "Software;Testing"            | 45  # c = inLine[i]            | 82 # if C == Stutter.delimits[i]:                                                               |
| 2             | "test.txt"  | "Software,Testing,Testing"    | 40 # linecnt = 1               | 68 # print('Repeated word on line ', line, ': ', Stutter.prevWord, ' ', Stutter.curWord, sep='') |
| 2             | "test.txt"  | "Software\n  Testing,Testing" | 53 #換行 # linecnt += 1          | 68 # print('Repeated word on line ', line, ': ', Stutter.prevWord, ' ', Stutter.curWord, sep='') |
| 2             | "test.txt"  | "Software!Testing"            |                                | 82 # if C == Stutter.delimits[i]:                                                               |



