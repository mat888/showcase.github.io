;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname if-and-test-coverage) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(require 2htdp/image)

;; Image -> Bool
;; Decide whether a given image is "tall" or not. True if height is greater than width

(check-expect (tall? (rectangle 2 3 "solid" "red")) true)
(check-expect (tall? (rectangle 2 1 "solid" "red")) false)
(check-expect (tall? (rectangle 2 2 "solid" "red")) false) ;edge case
  
;(define (tall? img) false)

(define (tall? img)
; (if (> (image-height img) (image-width img)) true false))
  (> (image-height img) (image-width img))) ;simpler, more direct conditional