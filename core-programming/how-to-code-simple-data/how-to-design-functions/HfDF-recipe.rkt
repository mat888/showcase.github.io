;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname HfDF-recipe) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
;; Number -> Number
;; produce 2 times the given number
(check-expect (double 3) 6)
(check-expect (double 4.2) 8.4)
(check-expect (double -1) -2)

;( define (double n) 0)   ; this is the stub

;( define (double n) ; this is the template
;  (... n))

( define (double n)
   (* 2 n))