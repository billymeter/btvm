.hello: "hello, world\n"    ;; length is 13

load r0, 0                  ;; counter
load r1, &hello             ;; message
loop:
    output r1               ;; output character
    add r0, 1               ;; counter++
    add r1, 1               ;; increment hello pointer
    compare r0, 0xd         ;; check if counter == 13
    jumpnoteq loop          ;; loop if counter != 13
halt                        ;; stop the system