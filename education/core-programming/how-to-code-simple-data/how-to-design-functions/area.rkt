;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname area) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
;; Consumes the legnth of one side of the square to get the area

;; Number -> Number
;; Given the legnth of one side of the square, produce the area of that square


(check-expect (area 3) 3)
(check-expect (area 1.2) 1.44)

;(define (area n) 0)

;(define (area s)
;  (... s))

(define (area s)
  (* s s))
