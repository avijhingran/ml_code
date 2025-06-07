       IDENTIFICATION DIVISION.
       PROGRAM-ID. PAYROLL.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT EMPLOYEE-FILE ASSIGN TO 'EMPLOYEE.DAT'
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD  EMPLOYEE-FILE.
       01  EMPLOYEE-RECORD.
           05 EMP-ID       PIC X(5).
           05 EMP-NAME     PIC A(30).
           05 HOURS-WORKED PIC 99V99.
           05 HOURLY-RATE  PIC 99V99.

       WORKING-STORAGE SECTION.
       01 WS-END-FILE      PIC X VALUE 'N'.
           88 END-FILE     VALUE 'Y'.
           88 NOT-END-FILE VALUE 'N'.
       01 WS-TOTAL-PAY     PIC 9(5)V99 VALUE ZEROS.
       01 WS-CURRENT-PAY   PIC 9(5)V99.

       PROCEDURE DIVISION.
       BEGIN.
           OPEN INPUT EMPLOYEE-FILE
           PERFORM UNTIL END-FILE
               READ EMPLOYEE-FILE
                   AT END
                       SET END-FILE TO TRUE
                   NOT AT END
                       COMPUTE WS-CURRENT-PAY = HOURS-WORKED * HOURLY-RATE
                       ADD WS-CURRENT-PAY TO WS-TOTAL-PAY
                       DISPLAY 'Employee: ' EMP-NAME
                       DISPLAY 'Pay: $' WS-CURRENT-PAY
               END-READ
           END-PERFORM
           CLOSE EMPLOYEE-FILE
           DISPLAY 'Total Payroll: $' WS-TOTAL-PAY
           STOP RUN.
