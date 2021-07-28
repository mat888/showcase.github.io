;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname img-area) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(require 2htdp/image)

;; Image -> Natural
;; Take an images height and width and produce its area

(check-expect (img-area (rectangle 1 1 "solid" "red")) 1)
(check-expect (img-area (rectangle 1 0 "solid" "green")) 0)
;(check-expect (img-area (rectangle 1.2 1.2 "solid" "blue")) 1.44) ;reals not allowed for pixel values
(check-expect (img-area (rectangle 3 5 "solid" "yellow")) 15)

; (define (img-area img) 0) ;stub

;(define (img-area img)
;  (... img))

(define (img-area img)
  (* (image-width img) (image-height img)))