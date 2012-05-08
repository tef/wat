#!/usr/bin/env python


print "\n".join(x.rstrip() for x in (lambda y:y["t"](y,5,1))({"t":lambda y,n,w:["  "*w for _ in xrange(1,w)]+["__"*w] if n == 0 else ["%s%s%s"%(" "*(len(t)//2),t," "*(len(t)//2)) for t in y["t"](y,n-1,w)]+["%s%s"%m for m in zip(y["l"](y,n-1,w),y["r"](y,n-1,w))],"l":lambda y,n,w:["%s/%s"%(" "*i," "*j) for (i,j) in zip(xrange(w-1,-1,-1),xrange(w,w*2))] if n==0 else ["%s%s%s"%(" "*(len(t)//2),t," "*(len(t)//2)) for t in y["r"](y,n-1,w)]+["%s%s"%m for m in zip(y["t"](y,n-1,w),y["l"](y,n-1,w))],"r":lambda y,n,w:["%s\\%s"%(" "*i," "*j) for (j,i) in zip(xrange(w-1,-1,-1),xrange(w,w*2))] if n==0 else ["%s%s%s"%(" "*(len(t)//2),t," "*(len(t)//2)) for t in y["l"](y,n-1,w)]+ ["%s%s"%m for m in zip(y["r"](y,n-1,w),y["t"](y,n-1,w))]})) 

    

