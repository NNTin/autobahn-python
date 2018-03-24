###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from __future__ import absolute_import

import os
from cffi import FFI


ffi = FFI()

ffi.cdef("""
    void* ueberschall_utf8vld_new ();

    void ueberschall_utf8vld_reset (void* utf8vld);

    int ueberschall_utf8vld_validate (void* utf8vld, const uint8_t* data, size_t length);

    void ueberschall_utf8vld_free (void* utf8vld);

    int ueberschall_utf8vld_set_impl(void* utf8vld, int impl);

    int ueberschall_utf8vld_get_impl(void* utf8vld);
""")

with open(os.path.join(os.path.dirname(__file__), '_validator.c')) as fd:
    c_source = fd.read()
    ffi.set_source(
        "_ueberschall_validator",
        c_source,
        libraries=[],
        extra_compile_args=['-std=c99', '-Wall', '-Wno-strict-prototypes', '-O3', '-march=native']
    )


class Utf8Validator:

    def __init__(self):
        self.ffi = ffi

        from _ueberschall_validator import lib
        self.lib = lib

        self._vld = self.ffi.gc(self.lib.ueberschall_utf8vld_new(), self.lib.ueberschall_utf8vld_free)
        print(self.lib.ueberschall_utf8vld_get_impl(self._vld))

    def reset(self):
        self.lib.ueberschall_utf8vld_reset(self._vld)

    def validate(self, ba):
        res = self.lib.ueberschall_utf8vld_validate(self._vld, ba, len(ba))
        return (res >= 0, res == 0, None, None)


if __name__ == "__main__":
    ffi.compile()
