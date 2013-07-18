def lex(pgm):
    pgm = pgm.replace("(", " ( ").replace(")", " ) ")
    tokens = pgm.split()
    l = make_list(tokens)
    print l
    return l[0]

def is_a_number(t):
    try:
        num = int(t)
        return True
    except:
        return False

def make_list(tokens):
    l = []
    while tokens:
        t = tokens.pop(0)
        if is_a_number(t):
            #print "FOUND A NUMBER", t
            l.append(int(t))
        elif t == ")":
            #print "LPAREN, returning list"
            return l
        elif t == "(":
            #print "RPAREN, making sublist"
            sub_list = make_list(tokens)
            l.append(sub_list)
        else:
            #print "FOUND A NAME", t
            l.append(t)
    return l


def lisp(filename):
    f = open(filename)
    pgm = f.read()
    f.close()

    ast = lex(pgm)
    interpret(ast)

env = {}

def gte(*expr_list):
    return interpret(expr_list[0]) >= interpret(expr_list[1])

def add(*expr_list):
    vals = [interpret(expr) for expr in expr_list]
    return sum(vals)

def lisp_print(*expr_list):
    val = interpret(expr_list[0])
    print val
    return val

my_functions = {
    ">=": gte,
    "+": add,
    "print": lisp_print

        }

def interpret(expr):
    if is_a_number(expr):
        return expr
    elif expr == "#t":
        return True
    elif expr == "#f":
        return False
    elif isinstance(expr, str):
        return env[expr]
    else:
        token = expr[0]
        if token in my_functions.keys():
            fn = my_functions.get(token)
            fn(*expr[1:])
        if token == "begin":
            rest = expr[1:]
            for node in rest:
                result = interpret(node)
            return result
        elif token == "set!":
            val = interpret(expr[2])
            key = expr[1]
            env[key] = val
            return val
        elif token == "cond":
            cond_val = interpret(expr[1])
            if cond_val == True:
                return interpret(expr[2])
            else:
                return interpret(expr[3])

lisp("test.lsp")
