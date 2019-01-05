# -*- coding: utf-8 -*-
from logfmt.formatter import format_line
from unittest import TestCase
from collections import OrderedDict
import sys


class FormatterTestCase(TestCase):
    def test_empty_log_line(self):
        data = format_line({})
        self.assertEqual(data, "")

    def test_key_without_value(self):
        data = format_line( OrderedDict([("key1", None), ("key2", None)]) )
        self.assertEqual(data, "key1= key2=")

    def test_boolean_values(self):
        data = format_line(OrderedDict([("key1", True), ("key2", False)])) 
        self.assertEqual(data, "key1=true key2=false")

    def test_int_value(self):
        data = format_line( OrderedDict([("key1", -1), ("key2", 2342342)]) )
        self.assertEqual(data, "key1=-1 key2=2342342")

    # In python 2.7, truncated to 12 digits total.  3.x does 16 
    def test_float_value(self):
        data = format_line( OrderedDict([("key1", 342.23424), ("key2", -234234234.2342342)]) )
        
        if sys.version_info < (3, 0):
            self.assertEqual(data, "key1=342.23424 key2=-234234234.234")
        else:
            self.assertEqual(data, "key1=342.23424 key2=-234234234.2342342")

    # Essentially, pre format your floats to strings
    def test_custom_float_format(self):
        data = format_line( OrderedDict([
            ("key1", 342.23424),
            ("key2", "%.7f" % -234234234.2342342)
        ]))

        self.assertEqual(data, "key1=342.23424 key2=-234234234.2342342")

    def test_string_value(self):
        data = format_line( OrderedDict([
            ("key1", """some random !@#$%^"&**_+-={}\\|;':,./<>?)"""),
            ("key2", """here's a line with
more stuff on the next""")
        ]))

        self.assertEqual(data, '''key1="some random !@#$%^\\"&**_+-={}\\|;\':,./<>?)" key2="here\'s a line with\nmore stuff on the next"''')
    
    def test_string_value_quoting(self):
        """
        Other implementation do not quote strings when not necessary.

        Examples:
            - https://github.com/kr/logfmt
            - https://github.com/csquared/node-logfmt
            - https://github.com/cyberdelia/logfmt-ruby
            - https://github.com/Sirupsen/logrus
        """
        data = format_line(OrderedDict([
            ("measure.a", "1ms"),
            ("measure.b", 10),
            ("measure.c", "100MB"),
            ("measure.d", "1s"),
        ]))
        self.assertEqual(data, "measure.a=1ms measure.b=10 measure.c=100MB measure.d=1s")



