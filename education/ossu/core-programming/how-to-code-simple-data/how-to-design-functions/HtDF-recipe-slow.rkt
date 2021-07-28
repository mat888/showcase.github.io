;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname HtDF-recipe-slow) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
;; Number -> Number
;; produces 2 times the given number

; check if the first input is equal to the second
(check-expect (double 3) 6)
(check-expect (double 4.2) 8.4) ; Number type includes all types of numbers
(check-expect (double 4.2) (* 2 4.2)) ; Demonstrate why you expect the value

;(define (double n) 0) ;this is the stub

;(define (double n)
;  (... n))

(define (double n)
  (* n 2))
