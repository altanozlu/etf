from etf import encoding, tags, terms
import struct
import unittest
import zlib

__author__ = 'ahawker'

class TestEncoder(unittest.TestCase):

    def setUp(self):
        self.encoder = encoding.ETFEncoder()

    def test_incorrect_version(self):
        pass

    def test_correct_version(self):
        pass

    def test_small_integer_too_low(self):
        term = self.encoder.encode_integer(-1)
        tag = term[0]
        self.assertNotEqual(tag, tags.SMALL_INTEGER)
        self.assertEqual(tag, tags.INTEGER)

    def test_small_integer_lower_bound(self):
        term = self.encoder.encode_integer(0)
        tag = term[0]
        self.assertEqual(tag, tags.SMALL_INTEGER)

    def test_small_integer_valid(self):
        term = self.encoder.encode_integer(100)
        tag = term[0]
        self.assertEqual(tag, tags.SMALL_INTEGER)

    def test_small_integer_upper_bound(self):
        term = self.encoder.encode_integer(255)
        tag = term[0]
        self.assertEqual(tag, tags.SMALL_INTEGER)

    def test_small_integer_too_large(self):
        term = self.encoder.encode_integer(256)
        tag = term[0]
        self.assertNotEqual(tag, tags.SMALL_INTEGER)
        self.assertEqual(tag, tags.INTEGER)

    def test_integer_lower_bound(self):
        term = self.encoder.encode_integer(-2147483648)
        tag = term[0]
        self.assertEqual(tag, tags.INTEGER)

    def test_integer_valid(self):
        term = self.encoder.encode_integer(4096)
        tag = term[0]
        self.assertEqual(tag, tags.INTEGER)

    def test_integer_upper_bound(self):
        term = self.encoder.encode_integer(2147483647)
        tag = term[0]
        self.assertEqual(tag, tags.INTEGER)

    def test_atom_false(self):
        term = self.encoder.encode_atom(False)
        tag = term[0]
        self.assertEqual(tag, tags.ATOM)

    def test_atom_true(self):
        term = self.encoder.encode_atom(True)
        tag = term[0]
        self.assertEqual(tag, tags.ATOM)

    def test_atom_none(self):
        term = self.encoder.encode_atom(None)
        tag = term[0]
        self.assertEqual(tag, tags.ATOM)

    def test_atom_name_lower_bound(self):
        term = self.encoder.encode_atom(terms.Atom(''))
        tag = term[0]
        self.assertEqual(tag, tags.ATOM)

    def test_atom_name_upper_bound(self):
        term = self.encoder.encode_atom(terms.Atom(' ' * 255))
        tag = term[0]
        self.assertEqual(tag, tags.ATOM)

    def test_atom_valid_name(self):
        term = self.encoder.encode_atom(terms.Atom('AtomName'))
        tag = term[0]
        self.assertEqual(tag, tags.ATOM)

    def test_float_zero(self):
        term = self.encoder.encode_float(terms.Float(0))
        tag = term[0]
        self.assertEqual(tag, tags.FLOAT)

    def test_float_negative(self):
        term = self.encoder.encode_float(terms.Float(1))
        tag = term[0]
        self.assertEqual(tag, tags.FLOAT)

    def test_float_valid(self):
        term = self.encoder.encode_float(terms.Float(4098))
        tag = term[0]
        self.assertEqual(tag, tags.FLOAT)

    def test_new_float_zero(self):
        self.encoder.minor_version = 1
        term = self.encoder.encode_new_float(terms.NewFloat(0))
        tag = term[0]
        self.assertEqual(tag, tags.NEW_FLOAT)

    def test_new_float_negative(self):
        term = self.encoder.encode_new_float(terms.NewFloat(1))
        tag = term[0]
        self.assertEqual(tag, tags.NEW_FLOAT)

    def test_new_float_valid(self):
        term = self.encoder.encode_new_float(terms.NewFloat(4096))
        tag = term[0]
        self.assertEqual(tag, tags.NEW_FLOAT)

    def test_new_float_builtin_zero(self):
        self.encoder.minor_version = 1
        term = self.encoder.encode_new_float(float(0))
        tag = term[0]
        self.assertEqual(tag, tags.NEW_FLOAT)

    def test_new_float_builtin_negative(self):
        term = self.encoder.encode_new_float(float(1))
        tag = term[0]
        self.assertEqual(tag, tags.NEW_FLOAT)

    def test_new__float_builtin_valid(self):
        term = self.encoder.encode_new_float(float(4096))
        tag = term[0]
        self.assertEqual(tag, tags.NEW_FLOAT)

    def test_small_tuple_empty(self):
        term = self.encoder.encode_tuple(tuple())
        tag = term[0]
        self.assertEqual(tag, tags.SMALL_TUPLE)

    def test_small_tuple_one_item(self):
        term = self.encoder.encode_tuple((1,))
        tag = term[0]
        self.assertEqual(tag, tags.SMALL_TUPLE)

    def test_small_tuple_max_items(self):
        term = self.encoder.encode_tuple((0,) * 255)
        tag = term[0]
        self.assertEqual(tag, tags.SMALL_TUPLE)

    def test_large_tuple_min_items(self):
        term = self.encoder.encode_tuple((0,) * 256)
        tag = term[0]
        self.assertEqual(tag, tags.LARGE_TUPLE)

    def test_large_tuple_many_items(self):
        term = self.encoder.encode_tuple((0,) * 4096)
        tag = term[0]
        self.assertEqual(tag, tags.LARGE_TUPLE)

    def test_list_empty(self):
        term = self.encoder.encode_list([])
        tag = term[0]
        self.assertEqual(tag, tags.NIL)

    def test_list_one_item(self):
        term = self.encoder.encode_list([1])
        tag = term[0]
        self.assertEqual(tag, tags.LIST)

    def test_list_many_items(self):
        term = self.encoder.encode_list([1] * 4096)
        tag = term[0]
        self.assertEqual(tag, tags.LIST)

    def test_reference_valid(self):
        ref = terms.Reference(terms.Atom(True), 0, 0)
        term = self.encoder.encode_reference(ref)
        tag = term[0]
        self.assertEqual(tag, tags.REFERENCE)

    def test_new_reference_one_id(self):
        ref = terms.NewReference(terms.Atom(True), 0, 0)
        term = self.encoder.encode_new_reference(ref)
        tag = term[0]
        self.assertEqual(tag, tags.NEW_REFERENCE)

    def test_new_reference_many_ids(self):
        ref = terms.NewReference(terms.Atom(True), 0, *((0,) * 4096))
        term = self.encoder.encode_new_reference(ref)
        tag = term[0]
        self.assertEqual(tag, tags.NEW_REFERENCE)

    def test_port_valid(self):
        port = terms.Port(terms.Atom(True), 0, 0)
        term = self.encoder.encode_port(port)
        tag = term[0]
        self.assertEqual(tag, tags.PORT)

    def test_pid_valid(self):
        pid = terms.Pid(terms.Atom(True), 0, 0, 0)
        term = self.encoder.encode_pid(pid)
        tag = term[0]
        self.assertEqual(tag, tags.PID)

    def test_string_empty(self):
        term = self.encoder.encode_string(terms.String(''))
        tag = term[0]
        self.assertEqual(tag, tags.STRING)

    def test_string_valid(self):
        term = self.encoder.encode_string(terms.String('HelloWorld'))
        tag = term[0]
        self.assertEqual(tag, tags.STRING)

    def test_string_max_length(self):
        term = self.encoder.encode_string(terms.String(' ' * 65535))
        tag = term[0]
        self.assertEqual(tag, tags.STRING)

    def test_string_too_long(self):
        term = self.encoder.encode_string(terms.String(' ' * 65536))
        tag = term[0]
        self.assertEqual(tag, tags.LIST)

    def test_string_builtin_empty(self):
        term = self.encoder.encode_string(unicode(''))
        tag = term[0]
        self.assertEqual(tag, tags.STRING)

    def test_string_builtin_valid(self):
        term = self.encoder.encode_string(unicode('HelloWorld'))
        tag = term[0]
        self.assertEqual(tag, tags.STRING)

    def test_string_builtin_max_length(self):
        term = self.encoder.encode_string(unicode(' ' * 65535))
        tag = term[0]
        self.assertEqual(tag, tags.STRING)

    def test_string_builtin_too_long(self):
        term = self.encoder.encode_string(unicode(' ' * 65536))
        tag = term[0]
        self.assertEqual(tag, tags.LIST)

    def test_binary_empty(self):
        term = self.encoder.encode_binary(terms.Binary(''))
        tag = term[0]
        self.assertEqual(tag, tags.BINARY)

    def test_binary_valid(self):
        term = self.encoder.encode_binary(terms.Binary('HelloWorld'))
        tag = term[0]
        self.assertEqual(tag, tags.BINARY)

    def test_binary_builtin_empty(self):
        term = self.encoder.encode_binary(str(''))
        tag = term[0]
        self.assertEqual(tag, tags.BINARY)

    def test_binary_builtin_valid(self):
        term = self.encoder.encode_binary(str('HelloWorld'))
        tag = term[0]
        self.assertEqual(tag, tags.BINARY)


if __name__ == '__main__':
    unittest.main()