( define-keyset 'admin-keyset (read-keyset "admin-keyset"))

;; Define the module

(module helloWorld 'admin-keyset
  "A smart contract to greet the world"
  (defun hello (name:string)
"Do the hello world rigamaroll"
(format "Hello {}!" [name]))
)

;; and say hello!
(hello "world")
