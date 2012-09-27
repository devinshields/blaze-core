from parse import parse
from datashape import *

def test_simple_parse():
    x = parse('800, 600, RGBA')
    y = parse('Enum (1,2)')
    z = parse('300 , 400, Record(x=int64, y=int32)')

    assert type(x) is DataShape
    assert type(y) is DataShape
    assert type(z) is DataShape

    assert type(x[0]) is Integer
    assert type(y[0]) is Enum

    assert type(z[0]) is Integer
    assert type(z[1]) is Integer
    assert type(z[2]) is Record

    assert z[2]('x') is int64
    assert z[2]('y') is int32

def test_compound_record():
    p = parse('6, Record(x=int, y=float, z=str)')
    assert type(p[0]) is Integer
    assert type(p[1]) is Record

def test_free_variables():
    p = parse('N, M, 800, 600, RGBA')

    assert type(p[0]) is TypeVar
    assert type(p[1]) is TypeVar
    assert type(p[2]) is Integer
    assert type(p[3]) is Integer
    assert type(p[4]) is Record
    assert p[4]('R') is int16
    assert p[4]('G') is int16
    assert p[4]('B') is int16
    assert p[4]('A') is int8

def test_flat_datashape():
    p = parse('N, M, 800, 600, (int16, int16, int16, int8)')

    assert type(p[0]) is TypeVar
    assert type(p[1]) is TypeVar
    assert type(p[2]) is Integer
    assert type(p[3]) is Integer

    assert p[4:8] == (int16, int16, int16, int8)

def test_flatten1():
    x = parse('a, ( b, ( c, ( d ) ) )')
    y = parse('a, b, c, d')

    assert len(x.operands) == len(y.operands)

    assert x[0].symbol == 'a'
    assert x[1].symbol == 'b'
    assert x[2].symbol == 'c'
    assert x[3].symbol == 'd'

    assert y[0].symbol == 'a'
    assert y[1].symbol == 'b'
    assert y[2].symbol == 'c'
    assert y[3].symbol == 'd'

    assert x.operands == y.operands

def test_flatten2():
    x = parse('a, ( b, ( c, d ) )')
    y = parse('a, b, c, d')

    assert len(x.operands) == len(y.operands)

    assert x[0].symbol == 'a'
    assert x[1].symbol == 'b'
    assert x[2].symbol == 'c'
    assert x[3].symbol == 'd'

    assert y[0].symbol == 'a'
    assert y[1].symbol == 'b'
    assert y[2].symbol == 'c'
    assert y[3].symbol == 'd'

    assert x.operands == y.operands

def test_parse_equality():
    x = parse('800, 600, int64')
    y = parse('800, 600, int64')

    assert x == y

def test_parse_ctypes():
    x = parse('800, 600, double')
    y = parse('800, 600, PyObject')

def test_parse_vars():
    x = parse('Var(1,2)')

    assert x[0].lower == 1
    assert x[0].upper == 2