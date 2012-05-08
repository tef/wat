import threading


class ContExit(SystemExit):
    pass

class Continuation(object):
    """ created by call/cc, passed into a new thread, and used to indicate when to resume the calling thread (if at all) """

    def __init__(self):
        self.event = threading.Event()
        self.result = None
        self.args = None
        self.exc = None 

    def throw(self, e):
        if self.event.is_set():
            raise StandardError('Continuation not restartable, cannot throw exception')

        self.exc = e
        self.event.set()

        threading.current_thread.daemon = True
        raise ContExit()

        
    def __call__(self, r, *arg):
        """ restart the continuation, exit current thread"""
        if self.event.is_set():
            raise StandardError('Continuation not restartable, cannot resume')

        # don't return single element tuple (like return foo)
        if arg:
            r = [r]
            r.extend(arg)

        self.ret(r)
        threading.current_thread.daemon = True
        raise ContExit()

    def ret(self, r):
        """ set the return value of the call/cc, and tell it to resume """
        if not self.event.is_set():
            self.result = r
            self.event.set()

    def value(self):
        """ block until the continuation is invoked """
        self.event.wait()
        if not self.exc:
            return self.result
        else:
            exc = self.exc
            if not self.exc:
                exc = StandardError('no result')
            raise exc
        

def callcc(func,*args, **kwargs):
    cont = Continuation() 

    if args and isinstance(args[0],Continuation):
        # Calling a continuation with our current continuation - so don't need a thread
        callee =args[0]
        callee.ret(cont)
    else:
        # we are invoking a function, so we create a thread, and block
        def run():
            try:
                cont.ret(func(cont, *args, **kwargs))
            except StandardError as e:
                import traceback; traceback.print_exc()
                cont.throw(e)

                
        t = threading.Thread(target=run)
        t.start()
    # wait until the contination is invoked
    return cont.value()

def add_1(r, x):
    r(x+1)

def mul_8(r, x):
    r(x*8)

print callcc(add_1, 1)
print callcc(mul_8, 1)

def example(r, x):
    add_1(lambda v: mul_8(r,v), x)

print callcc(example, 1)


def inner(cont):
    print "inner, calling cont with current cont"""
    main_cont, i =callcc(cont)
    print "inner, got main_cont back, calling with",i
    main_cont(i)


def outer(main_cont, inside, i):
    print "outer, calling inner with current cont"""
    inner_cont = callcc(inside)
    print "calling inner_cont with main_cont, ",i
    inner_cont(main_cont,i)

print "main, calling: outer -> inner -> outer -> inner"
r = callcc(outer, inner, "butt") 
print "main, got ", r


