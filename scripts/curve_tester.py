
if starting:
    start = 0.2
    end = .9
    step = .10 
    #easeOut = curves.create(start, end, 12, 40, 50, 91)
    easeIn = curves.create(start, end, 0.731, 0.544)
    
    
    for x in range(11):
        diagnostics.debug("{{ x:{0:0.00}, in: {1:0.000} }}",x*step, easeIn.getY(x*step))