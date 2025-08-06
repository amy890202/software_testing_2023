# Lab06: Program Security Detect

## Enviroment
```
gcc --version
```
```
gcc (Ubuntu 11.3.0-1ubuntu1~22.04) 11.3.0
```
## Command

### Asan
```
gcc -fsanitize=address -g -o test_A test.c
```
```
./test_A
```
### Valgrind
```
gcc -o test test.c
```
```
valgrind ./test
```
### I. 下面是常見的記憶體操作問題，請分別寫出有下列記憶體操作問題的簡單程式，並說明 Valgrind 和 ASan 能否找的出來
Heap out-of-bounds read/write
Stack out-of-bounds read/write
Global out-of-bounds read/write
Use-after-free
Use-after-return


### Heap out-of-bounds
```
#include <stdlib.h>

int main() {
  int *arr = (int*) malloc(sizeof(int)*5);
  arr[5] = 0; // Heap out-of-bounds write
  int x = arr[6]; // Heap out-of-bounds read
  free(arr);
  return 0;
}

```
#### Asan report
```
=================================================================
==820==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x603000000054 at pc 0x55905be9b242 bp 0x7ffff0242f80 sp 0x7ffff0242f70
WRITE of size 4 at 0x603000000054 thread T0
    #0 0x55905be9b241 in main (/home/amy890202/ST2023/test_A+0x1241)
    #1 0x7f5aa30f3d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f5aa30f3e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x55905be9b124 in _start (/home/amy890202/ST2023/test_A+0x1124)

0x603000000054 is located 0 bytes to the right of 20-byte region [0x603000000040,0x603000000054)
allocated by thread T0 here:
    #0 0x7f5aa33a6867 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x55905be9b1fe in main (/home/amy890202/ST2023/test_A+0x11fe)
    #2 0x7f5aa30f3d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/amy890202/ST2023/test_A+0x1241) in main
Shadow bytes around the buggy address:
  0x0c067fff7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c067fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c067fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c067fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c067fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c067fff8000: fa fa 00 00 00 fa fa fa 00 00[04]fa fa fa fa fa
  0x0c067fff8010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==820==ABORTING
```

#### valgrind report
```
==1049== Memcheck, a memory error detector
==1049== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1049== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1049== Command: ./test
==1049== 
==1049== Invalid write of size 4
==1049==    at 0x10918B: main (in /home/amy890202/ST2023/test)
==1049==  Address 0x4a8d054 is 0 bytes after a block of size 20 alloc'd
==1049==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==1049==    by 0x10917E: main (in /home/amy890202/ST2023/test)
==1049== 
==1049== Invalid read of size 4
==1049==    at 0x109195: main (in /home/amy890202/ST2023/test)
==1049==  Address 0x4a8d058 is 4 bytes after a block of size 20 alloc'd
==1049==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==1049==    by 0x10917E: main (in /home/amy890202/ST2023/test)
==1049== 
==1049== 
==1049== HEAP SUMMARY:
==1049==     in use at exit: 0 bytes in 0 blocks
==1049==   total heap usage: 1 allocs, 1 frees, 20 bytes allocated
==1049== 
==1049== All heap blocks were freed -- no leaks are possible
==1049== 
==1049== For lists of detected and suppressed errors, rerun with: -s
==1049== ERROR SUMMARY: 2 errors from 2 contexts (suppressed: 0 from 0)
```
ASan 能 , valgrind 能



### Stack out-of-bounds
```
#include <stdio.h>

int main() {
  int arr[5] = {1, 2, 3, 4, 5};;
  int x = arr[5]; // Stack out-of-bounds read
  //arr[6] = 0; // Stack out-of-bounds write 加這行本身gcc就會報錯 *** stack smashing detected ***: terminated
  //printf("%d\n", x);//加這行valgrind會報錯，ASAN也報Stack-buffer-overflow
  return 0;
}
```

#### Asan report
```
=================================================================
==1852==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fffdf88f024 at pc 0x55ef979fd3f9 bp 0x7fffdf88efd0 sp 0x7fffdf88efc0
READ of size 4 at 0x7fffdf88f024 thread T0
    #0 0x55ef979fd3f8 in main (/home/amy890202/ST2023/test_A+0x13f8)
    #1 0x7f082bb66d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f082bb66e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x55ef979fd124 in _start (/home/amy890202/ST2023/test_A+0x1124)

Address 0x7fffdf88f024 is located in stack of thread T0 at offset 52 in frame
    #0 0x55ef979fd1f8 in main (/home/amy890202/ST2023/test_A+0x11f8)

  This frame has 1 object(s):
    [32, 52) 'arr' (line 12) <== Memory access at offset 52 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow (/home/amy890202/ST2023/test_A+0x13f8) in main
Shadow bytes around the buggy address:
  0x10007bf09db0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007bf09dc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007bf09dd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007bf09de0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007bf09df0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 f1 f1
=>0x10007bf09e00: f1 f1 00 00[04]f3 f3 f3 f3 f3 00 00 00 00 00 00
  0x10007bf09e10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007bf09e20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007bf09e30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007bf09e40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007bf09e50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==1852==ABORTING
```

#### valgrind report
```
==1879== Memcheck, a memory error detector
==1879== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1879== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1879== Command: ./test
==1879== 
==1879== 
==1879== HEAP SUMMARY:
==1879==     in use at exit: 0 bytes in 0 blocks
==1879==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==1879== 
==1879== All heap blocks were freed -- no leaks are possible
==1879== 
==1879== For lists of detected and suppressed errors, rerun with: -s
==1879== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
ASan 能 , valgrind 不能

### Global out-of-bounds read/write
```
#include <stdio.h>

int arr[5] = {1, 2, 3, 4, 5};

int main() {
  int x = arr[5]; // Global out-of-bounds read
  arr[6] = 0; // Global out-of-bounds write
  printf("%d\n", x);
  return 0;
}

```

#### Asan report
```
=================================================================
==12217==ERROR: AddressSanitizer: global-buffer-overflow on address 0x558eb0bef034 at pc 0x558eb0bec24f bp 0x7ffc8a924bc0 sp 0x7ffc8a924bb0
READ of size 4 at 0x558eb0bef034 thread T0
    #0 0x558eb0bec24e in main /home/amy890202/ST2023/Global.c:6
    #1 0x7fbb15619d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7fbb15619e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x558eb0bec144 in _start (/home/amy890202/ST2023/test_A+0x1144)

0x558eb0bef034 is located 0 bytes to the right of global variable 'arr' defined in 'Global.c:3:5' (0x558eb0bef020) of size 20
SUMMARY: AddressSanitizer: global-buffer-overflow /home/amy890202/ST2023/Global.c:6 in main
Shadow bytes around the buggy address:
  0x0ab256175db0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab256175dc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab256175dd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab256175de0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab256175df0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0ab256175e00: 00 00 00 00 00 00[04]f9 f9 f9 f9 f9 00 00 00 00
  0x0ab256175e10: f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9
  0x0ab256175e20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab256175e30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab256175e40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ab256175e50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==12217==ABORTING
```

##### valgrind report
```
==12108== Memcheck, a memory error detector
==12108== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==12108== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==12108== Command: ./test
==12108== 
0
==12108== 
==12108== HEAP SUMMARY:
==12108==     in use at exit: 0 bytes in 0 blocks
==12108==   total heap usage: 1 allocs, 1 frees, 1,024 bytes allocated
==12108== 
==12108== All heap blocks were freed -- no leaks are possible
==12108== 
==12108== For lists of detected and suppressed errors, rerun with: -s
==12108== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
ASan 能 , valgrind 不能


### Use-after-free
```
#include <stdlib.h>

int main() {
  int *ptr = (int*) malloc(sizeof(int));
  free(ptr);
  *ptr = 5; // Use-after-free
  return 0;
}

//example code from TA
//char *x = (char*)malloc(10*sizeof(char*));
//free(x);
//return x[5];


```

#### Asan report
```
=================================================================
==12441==ERROR: AddressSanitizer: heap-use-after-free on address 0x602000000010 at pc 0x562a69f32226 bp 0x7ffc4de56e50 sp 0x7ffc4de56e40
WRITE of size 4 at 0x602000000010 thread T0
    #0 0x562a69f32225 in main /home/amy890202/ST2023/User.c:6
    #1 0x7f5d328ecd8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f5d328ece3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x562a69f32104 in _start (/home/amy890202/ST2023/test_A+0x1104)

0x602000000010 is located 0 bytes inside of 4-byte region [0x602000000010,0x602000000014)
freed by thread T0 here:
    #0 0x7f5d32b9f517 in __interceptor_free ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:127
    #1 0x562a69f321ee in main /home/amy890202/ST2023/User.c:5
    #2 0x7f5d328ecd8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58

previously allocated by thread T0 here:
    #0 0x7f5d32b9f867 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x562a69f321de in main /home/amy890202/ST2023/User.c:4
    #2 0x7f5d328ecd8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58

SUMMARY: AddressSanitizer: heap-use-after-free /home/amy890202/ST2023/User.c:6 in main
Shadow bytes around the buggy address:
  0x0c047fff7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c047fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c047fff8000: fa fa[fd]fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==12441==ABORTING
```

#### valgrind report
```
==12333== Memcheck, a memory error detector
==12333== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==12333== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==12333== Command: ./test
==12333== 
==12333== Invalid write of size 4
==12333==    at 0x109193: main (in /home/amy890202/ST2023/test)
==12333==  Address 0x4a8d040 is 0 bytes inside a block of size 4 free'd
==12333==    at 0x484B27F: free (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==12333==    by 0x10918E: main (in /home/amy890202/ST2023/test)
==12333==  Block was alloc'd at
==12333==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==12333==    by 0x10917E: main (in /home/amy890202/ST2023/test)
==12333== 
==12333== 
==12333== HEAP SUMMARY:
==12333==     in use at exit: 0 bytes in 0 blocks
==12333==   total heap usage: 1 allocs, 1 frees, 4 bytes allocated
==12333== 
==12333== All heap blocks were freed -- no leaks are possible
==12333== 
==12333== For lists of detected and suppressed errors, rerun with: -s
==12333== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```
ASan 能 , valgrind 能

### Use-after-return
```
#include <stdio.h>

char* x;
void f()
{
    char stack_buf[10];// stack_buf 是一個在 f() 返回後就被釋放的區域變數。
    x = &stack_buf[2];
}

int main()
{
    f();
    *x = 1;// Use-after-return
    return 0;
}
```
* ASAN 須加上參數ASAN_OPTION=detect_stack_use_after_return=1才偵測的到
```
gcc -fsanitize=address -g -o test_A user_after_return.c
ASAN_OPTIONS=detect_stack_use_after_return=1 ./test_A
```

#### Asan report
```
=================================================================
==13366==ERROR: AddressSanitizer: stack-use-after-return on address 0x7f9874778022 at pc 0x561bbbf43333 bp 0x7ffeb205ece0 sp 0x7ffeb205ecd0
WRITE of size 1 at 0x7f9874778022 thread T0
    #0 0x561bbbf43332 in main /home/amy890202/ST2023/user_after_return.c:14
    #1 0x7f9877f14d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f9877f14e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x561bbbf43144 in _start (/home/amy890202/ST2023/test_A+0x1144)

Address 0x7f9874778022 is located in stack of thread T0 at offset 34 in frame
    #0 0x561bbbf43218 in f /home/amy890202/ST2023/user_after_return.c:5

  This frame has 1 object(s):
    [32, 42) 'stack_buf' (line 6) <== Memory access at offset 34 is inside this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-use-after-return /home/amy890202/ST2023/user_after_return.c:14 in main
Shadow bytes around the buggy address:
  0x0ff38e8e6fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff38e8e6fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff38e8e6fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff38e8e6fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff38e8e6ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0ff38e8e7000: f5 f5 f5 f5[f5]f5 f5 f5 00 00 00 00 00 00 00 00
  0x0ff38e8e7010: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff38e8e7020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff38e8e7030: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff38e8e7040: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff38e8e7050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==13366==ABORTING
```

#### valgrind report
```
==13206== Memcheck, a memory error detector
==13206== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==13206== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==13206== Command: ./test
==13206== 
==13206== 
==13206== HEAP SUMMARY:
==13206==     in use at exit: 0 bytes in 0 blocks
==13206==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==13206== 
==13206== All heap blocks were freed -- no leaks are possible
==13206== 
==13206== For lists of detected and suppressed errors, rerun with: -s
==13206== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
ASan 能(須加上ASAN_OPTION=detect_stack_use_after_return=1參數) , valgrind 不能





|                      | **Valgrind** | **ASAN** |
| -------------------- | ------------ | -------- |
| Heap out-of-bounds   | O            | O        |
| Stack out-of-bounds  | X            | O        |
| Global out-of-bounds | X            | O        |
| Use-after-free       | O            | O        |
| Use-after-return     | X            | O        |



### II. 寫一個簡單程式 with ASan，Stack buffer overflow 剛好越過 redzone(並沒有對 redzone 做讀寫)，並說明 ASan 能否找的出來？
```
#include <stdio.h>

int main() {
    
    
    int a[8];
    int b[8];
    a[8+8] = 1;//剛好越過redzone，無法抓到錯誤
    a[8+18] =1;//a[8+8]以後，越過redzone無法抓到錯誤
    a[8+25] =1;//a[8+8]以後，越過redzone無法抓到錯誤
    //a[8+7] =1;//a[8+0]~a[8+7]在redzone內可以抓到錯誤

    return 0;
}

```

#### ASAN 
![](https://i.imgur.com/4Wnp6Oc.png)



a[8+0]~a[8+7] 在redzone內可以抓到錯誤
a[8+8]以後，越過redzone無法抓到錯誤
越過redzone之後，由於這些位置不在redzone中，程式無法檢測到這些溢出，因此ASAN抓不到錯誤
