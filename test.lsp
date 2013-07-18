(begin
  (set! a 2)
  (+ a a)
  (cond (>= a 5)
        (print #t)
        (print #f)
    )
)
