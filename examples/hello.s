.hello: "hello, world\n"    ;; length is 13

move r0, 0                  ;; counter
move r1, hello              ;; message
loop:
    output r1               ;; output character
    add r0, 1               ;; counter++
    compare r0, 0xd         ;; check if counter == 13
    ; compare r0, 13        ;; alternate form of line 8
    jumpnoteq loop          ;; loop if counter != 13
halt                        ;; stop the system