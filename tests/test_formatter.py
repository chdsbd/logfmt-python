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
        data = format_line(OrderedDict([
            ("key1", """some random !@#$%^"&**_+-={}\\|;':,./<>?)"""),
            ("key2", """here's a line with
more stuff on the next""")
        ]))

        self.assertEqual(data, '''key1="some random !@#$%^\\"&**_+-={}\\|;\':,./<>?)" key2="here\'s a line with\nmore stuff on the next"''')
    
    def test_kr_logfmt(self):
        """        
        Test using canonical example from https://github.com/kr/logfmt/blob/b84e30acd515aadc4b783ad4ff83aff3299bdfe0/example_test.go#L45
        """
        data = format_line(OrderedDict([
            ("measure.a", "1ms"),
            ("measure.b", 10),
            ("measure.c", "100MB"),
            ("measure.d", "1s"),
        ]))
        self.assertEqual(data, "measure.a=1ms measure.b=10 measure.c=100MB measure.d=1s")


class NodeLogfmtFormatterTestCase(TestCase):
    """
    Test cases modified from node-logfmt

    https://github.com/csquared/node-logfmt/blob/9cccf6273cdd862392ef7fea049d37a2b7c42e04/test/stringify_test.js


    MIT LICENSE

    Copyright (C) 2014 Chris Continanza

    Permission is hereby granted, free of charge, to any person obtaining
    a copy of this software and associated documentation files (the
    "Software"), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    """
    def test_string_spaces(self):
        """
        Quote strings with spaces
        """
        data = {'foo': "hello kitty"}
        self.assertEqual("foo=\"hello kitty\"", format_line(data))
    
    def test_string_equals(self):
        """
        Quote strings with equals
        """
        data = {'foo': "hello=kitty"}
        self.assertEqual("foo=\"hello=kitty\"", format_line(data))
    
    def test_string_spaces_quotes(self):
        """
        Escape quotes in strings with spaces
        """
        data = {'foo': 'hello my "friend"'}
        self.assertEqual('foo="hello my \\"friend\\""', format_line(data))
        data = {'foo': 'hello my "friend" whom I "love"'}
        self.assertEqual('foo="hello my \\"friend\\" whom I \\"love\\""', format_line(data))
    

    def test_string_blackslashes(self):
        """
        Escape backslashes in strings
        """
        data = {'foo': 'why would you use \\LaTeX?'}
        self.assertEqual('foo="why would you use \\\\LaTeX?"', format_line(data))
