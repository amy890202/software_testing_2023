# Lab07_Fuzz Testing

We provide a small program that converts bmp from color to grayscale.
Use AFL to find the file that can trigger the vulnerability.
Use test.bmp as initial seed.


Please write a report named README.md/rst placed in lab07 dir in your github repo.
The report shall contain the following information:
* PoC: the file that can trigger the vulnerability
* The commands (steps) that you used in this lab
* Screenshot of AFL running (with triggered crash)
* Screenshot of crash detail (with ASAN error report)


### PoC: the file that can trigger the vulnerability





#### Poc   
* id:000000,sig:06,src:000000,op:flip1,pos:18

```
cd out/crashes/
```
![](https://i.imgur.com/FbvdICu.png)
在Lab07的out/crashes/ 目錄下，README.txt 文件會提供一些有關該目錄下生成的崩潰日誌的有用信息，例如每個崩潰的 ID、發生崩潰的次數、觸發崩潰的測試用例、崩潰時的信號等等。
id:000000,sig:06,src:000000,op:flip1,pos:18 是一個崩潰 ID 和一些關於它的元數據。具體來說，這裡的 id:000000 表示這是第一個崩潰，sig:06 表示崩潰時發生了 SIGABRT 信號，src:000000 表示這個崩潰是由哪個測試用例引發的，op:flip1 表示導致崩潰的操作是 flip1，pos:18 表示 flip1 操作作用的是測試用例中的第 18 個字節。
因此，這個 ID 所對應的測試用例就是觸發崩潰的 PoC，可以使用它來進一步分析漏洞的原因和影響。



### The commands (steps) that you used in this lab
有些套件要先安裝才不會報錯
```
sudo apt-get update
sudo apt-get install pkg-config
sudo apt-get install autoconf
sudo apt-get install automake
sudo apt-get install libtool
```
Build & fuzz with AFL


```
git clone https://github.com/chameleon10712/NYCU-Software-Testing-2023.git
cd Lab07
export CC=~/AFL/afl-gcc
export AFL_USE_ASAN=1
make
mkdir in
cp test.bmp in/
~/AFL/afl-fuzz -i in -o out -m none -- ./bmpgrayscale @@ a.bmp
./bmpgrayscale out/crashes/id:000000* a.bmp
```
如果要remove整個資料夾: rm -rf NYCU-Software-Testing-2023


$ cd Lab07
進入Lab07目錄。
$ export CC=~/AFL/afl-gcc
將環境變量CC設置為afl-gcc，這是一個帶有AFL支持的GCC版本。
$ export AFL_USE_ASAN=1
啟用地址Sanitizer（ASAN）來檢測內存錯誤。
$ make
使用Makefile中的指令來編譯程序。
$ mkdir in
創建一個名為in的目錄，用於存放測試輸入。
$ cp test.bmp in/
將一個名為test.bmp的位圖文件複製到in目錄中，作為測試輸入。
$ ~/AFL/afl-fuzz -i in -o out -m none -- ./bmpgrayscale @@ a.bmp
使用AFL來模糊測試程序。 -i指定輸入文件夾，-o指定輸出文件夾，-m none表示使用默認內存限制，--後面跟著的是要測試的程序和其參數。 
@@用於指定輸入文件的位置，a.bmp是實際的輸入文件名。
$ ./bmpgrayscale out/crashes/id:000000* a.bmp
用 out/crashes/id:000000* 作為輸入文件，運行 bmpgrayscale 程序，嘗試重現導致崩潰的輸入文件的問題。

./bmpgrayscale 是你要運行的程序名稱，out/crashes/id:000000* 是由 AFL 生成的觸發崩潰的文件，a.bmp 是你想要用於程序的輸入文件。
因此，命令 ./bmpgrayscale out/crashes/id:000000* a.bmp 的意思是使用 AFL 生成的觸發崩潰的輸入文件 out/crashes/id:000000*，來運行程序 ./bmpgrayscale 並使用輸入文件 a.bmp。這將允許你調試崩潰並修復程序中的任何問題。

(以下與lab無關，純筆記)
example:
```
$ git clone https://gitlab.gnome.org/GNOME/libxml2.git
$ cd libxml2
$ ./autogen.sh
$ export CC=~/AFL/afl-gcc
$ export CXX=~/AFL/afl-g++
$ export AFL_USE_ASAN=1
$ ./configure --enable-shared=no
$ make

$ mkdir -p  ~/fuzz/in
$ cp xmllint  ~/fuzz/libxml2
$ cp test/*.xml   ~/fuzz/in/

$ cd ~/fuzz
$ ~/AFL/afl-fuzz -i in/ -o out/ -m none -- ./libxml2 @@
```
Fuzzing:
```
$ afl-fuzz -i in/ -o out/ -b 10 -m none -- ./target [argv1] @@ [argv2]
```
-i dir : seed dir
-o dir : output dir
-b CPU_ID : bind the fuzzing process to the specified CPU core
-m megs: memory limit for child process
@@ : the location of the input (if NO -> stdin)



### Screenshot of AFL running (with triggered crash)

![](https://i.imgur.com/FMSieYo.png)

### Screenshot of crash detail (with ASAN error report)
![](https://i.imgur.com/AtOEUxT.png)


