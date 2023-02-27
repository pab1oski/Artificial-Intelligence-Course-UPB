# Useful imports:
from operator import add
from LPTester import test_batch


# In[2]:


### Representation - construction
[CONSTANT, VARIABLE, FUNCTION, ATOM, FORMULA, NEG, OR, AND] = range(8)

# Returns a constant term with the specified value.
def make_const(value):
    # TODO
    return [CONSTANT, value]


# Returns a term that is a variable with the specified name.
def make_var(name):
    # TODO
    return [VARIABLE, name, None]


# Returns a term that is a call to the specified function, on the rest of the given arguments.
# E.g. to build the term add [1, 2, 3] we will call -->
# --> make_function_call(add, make_const(1), make_const(2), make_const(3))
# !! WARNING: python gives args as a tuple with the rest of the arguments, not as a list.
# The conversion can be realised using list(args)
def make_function_call(function, *args):
    # TODO
    return [FUNCTION, function, list(args)]


# Returns a formula consisting of an atom which is the utilisation of the given predicate
# on the rest of the additional arguments(*args).
# !! WARNING: python gives args as a tuple with the rest of the arguments, not as a list.
# The conversion can be realised using list(args)
def make_atom(predicate, *args):
    # TODO
    return [FORMULA, ATOM, predicate, list(args)]


# Returns a formula that is the negation of the given sentence.
# get_args(make_neg(s1)) will return [s1]
def make_neg(sentence):
    # TODO
    return [FORMULA, NEG, [sentence]]


# Returns a formula that is the conjunction of the given sentences (2 or more).
# e.g. the call of the function make_and(s1, s2, s3, s4) returns the conjunction structure of s1 ^ s2 ^ s3 ^ s4
# and get_args for this structure returns [s1, s2, s3, s4]
def make_and(sentence1, sentence2, *others):
    # TODO
    return [FORMULA, AND, [sentence1, sentence2] + list(others)]


# Returns a formula which is the disjunction of the given sentences.
# e.g. the call of the function make_or(s1, s2, s3, s4) returns the disjunction structure of s1 V s2 V s3 V s4
# and get_args for this structure returns [s1, s2, s3, s4]
def make_or(sentence1, sentence2, *others):
    # TODO
    return [FORMULA, OR, [sentence1, sentence2] + list(others)]


# Returns a copy of the given formula or function call,
# in which the arguments have been replaced with those in the new_args list.
# e.g. for formula p (x, y), replacing the arguments with list [1, 2] will result in formula p (1, 2).
# The new argument list must have the same length as the original number of arguments in the formula.
def replace_args(formula, new_args):
    # TODO
    if formula[0] == FUNCTION:
        return [FUNCTION, formula[1], list(new_args)]
    elif formula[0] == FORMULA:
        if formula[1] == ATOM:
            return [FORMULA, ATOM, formula[2], list(new_args)]
        else:
            return [formula[0], formula[1], list(new_args)]
    return formula


# In[3]:


### Representation - verification

# Returns true if f is a term.
def is_term(f):
    return is_constant(f) or is_variable(f) or is_function_call(f)


# Returns true if f is a constant term.
def is_constant(f):
    # TODO
    return f[0] == CONSTANT


# Returns true if f is a term that is a variable.
def is_variable(f):
    # TODO
    return f[0] == VARIABLE


# Returns true if f is a function call.
def is_function_call(f):
    # TODO
    return f[0] == FUNCTION


# Returns true if f is an atom (application of a predicate).
def is_atom(f):
    # TODO
    return f[0] == FORMULA and f[1] == ATOM


# Returns true if f is a valid sentence.
def is_sentence(f):
    # TODO
    return f[0] == FORMULA


# Returns true if the formula f is something that has arguments..
def has_args(f):
    return is_function_call(f) or is_sentence(f)


# For constants (to be checked), the value of the constant is returned; otherwise, None.
def get_value(f):
    # TODO
    if is_constant(f):
        return f[1]
    return None


# For variables (to be checked), return the name of the variable; otherwise, None.
def get_name(f):
    # TODO
    if is_variable(f):
        return f[1]
    return None


# for function calls, return the function;
# for atoms, the name of the predicate is returned;
# for compound sentences, return a string representing the logical connector (e.g. ~, A or V);
# otherwise, None
def get_head(f):
    # TODO
    if is_function_call(f):
        return f[1]
    elif f[0] == FORMULA:
        if is_atom(f):
            return f[2]
        else:
            return f[1]
    return None


# For sentences or function calls, the list of arguments is returned; otherwise, None.
# See also "Important:" above.
def get_args(f):
    # TODO
    if is_function_call(f):
        return f[2]
    elif is_atom(f):
        return f[3]
    elif is_sentence(f):
        return f[2]
    return None


test_batch(0, globals())


# In[4]:


# This function displays the formula f.
# If the return_result argument is True, the result is returnd and not displayed on the console.
def print_formula(f, return_result=False):
    ret = ""
    if is_term(f):
        if is_constant(f):
            ret += str(get_value(f))
        elif is_variable(f):
            ret += "?" + get_name(f)
        elif is_function_call(f):
            ret += (
                str(get_head(f))
                + "["
                + "".join([print_formula(arg, True) + "," for arg in get_args(f)])[:-1]
                + "]"
            )
        else:

            ret += "???"
    elif is_atom(f):
        ret += (
            str(get_head(f))
            + "("
            + "".join([print_formula(arg, True) + ", " for arg in get_args(f)])[:-2]
            + ")"
        )
    elif is_sentence(f):
        # negation, conjunction or disjunction
        args = get_args(f)
        if len(args) == 1:
            ret += str(get_head(f)) + print_formula(args[0], True)
        else:
            ret += (
                "("
                + str(get_head(f))
                + "".join([" " + print_formula(arg, True) for arg in get_args(f)])
                + ")"
            )
    else:
        ret += "???"
    if return_result:
        return ret
    print(ret)
    return


# Verify construction and display
# The output should be similar to: (A (V ~P(?x) Q(?x)) T(?y, <built-in function add>[1,2]))
formula1 = make_and(
    make_or(make_neg(make_atom("P", make_var("x"))), make_atom("Q", make_var("x"))),
    make_atom(
        "T", make_var("y"), make_function_call(add, make_const(1), make_const(2))
    ),
)
print_formula(formula1)


# ## Unification
#
# The unification of two logical formulas containing variables means finding a substitution so that its application on the two formulas results in two identical formulas.
#
# A substitution contains associations of variables to terms. When a substitution is applied, the variables that appear in the substitution are replaced, in the formula, by the associated terms, until no replacement can be made.
#
# We represent a substitution as a dictionary `{variable name: term representation}`

# In[5]:


# This function applies in formula f all elements of the given substitution and returns the resulting formula
def substitute(f, substitution):
    if substitution is None:
        return None
    if is_variable(f) and (get_name(f) in substitution):
        return substitute(substitution[get_name(f)], substitution)
    if has_args(f):
        return replace_args(f, [substitute(arg, substitution) for arg in get_args(f)])
    return f


def test_formula(x, copyy=False):
    fun = make_function_call(add, make_const(1), make_const(2))
    return make_and(
        make_or(make_neg(make_atom("P", make_const(x))), make_atom("Q", make_const(x))),
        make_atom("T", fun if copyy else make_var("y"), fun),
    )


# Test (the effects of substitutions in the formula must be seen)
test_batch(1, globals())


# ### Task 1
#
# Implement the `occur_check` and` unify` functions, according to Robinson's algorithm (see pdf).

# In[6]:


# Check if the variable v appears in the term t, considering the substitution of subst.
# Returns True if v appears in t (v can NOT be replaced with t), and False if v can be replaced with t.
def occur_check(v, t, subst):
    # TODO
    if v == t:
        return True
    if get_name(t) in subst:
        return occur_check(v, substitute(t, subst), subst)
    if is_function_call(t):
        for arg in t[2]:
            if occur_check(v, arg, subst):
                return True
    return False


# Test!
test_batch(2, globals())


# In[7]:


# Unifies the formulas f1 and f2, under an existing substitution subst.
# The result of the unification is a substitution (dictionary name-variable -> term),
# so that if the substitution of the two formulas is applied, the result is identical.
def unify(f1, f2, subst=None):
    if subst is None:
        subst = {}
    # TODO
    stack = []
    stack.append((f1, f2))
    while len(stack) > 0:
        (f1, f2) = stack.pop()

        while get_name(f1) in subst:
            f1 = substitute(f1, subst)
        while get_name(f2) in subst:
            f2 = substitute(f2, subst)

        if not f1 == f2:
            if is_variable(f1):
                if occur_check(f1, f2, subst):
                    return False
                else:
                    subst[get_name(f1)] = f2
            elif is_variable(f2):
                if occur_check(f2, f1, subst):
                    return False
                else:
                    subst[get_name(f2)] = f1

            elif has_args(f1) and has_args(f2):
                hs = get_args(f1)
                ht = get_args(f2)

                if get_head(f1) == get_head(f2) and len(hs) == len(ht):
                    n = len(hs)
                    for _ in range(n):
                        stack.append((hs[_], ht[_]))
                else:
                    return False
            else:
                return False
    return subst


# Test!
test_batch(3, globals())


# In[ ]:
