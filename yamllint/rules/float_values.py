# -*- coding: utf-8 -*-
# Copyright (C) 2017 ScienJus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Use this rule to limit the permitted values for floats. YAML permits three classes
of float expressions:

`[-+]?(\.[0-9]+|[0-9]+(\.[0-9]*)?)([eE][-+]?[0-9]+)?`
`[-+]?(\.inf|\.Inf|\.INF)`
`\.nan|\.NaN|\.NAN`

.. rubric:: Options

* Use ``require-numeral-before-decimal'`` to require floats to start with a numeral (ex 0.0 instead of .0)
* Use ``forbid-scientific-notation`` to forbid scientific notiation
* Use ``forbid-nan`` to forbid NaN values
* Use ``forbid-inf`` to forbid infinite values

.. rubric:: Default values (when enabled)

.. code-block:: yaml

 rules:
   float-values:
        require-numeral-before-decimal: false
        forbid-scientific-notation: false
        forbid-nan: false
        forbid-inf: false

.. rubric:: Examples

#. With ``float-values: {require-numeral-before-decimal: true}``

   the following code snippets would **PASS**:
   ::

    anemometer:
        angle: 0.0

   the following code snippets would **FAIL**:
   ::

    anemometer:
        angle: .0

#. With ``float-values: {forbid-scientific-notation: true}``

   the following code snippets would **PASS**:
   ::

    anemometer:
        angle: 0.00001

   the following code snippets would **FAIL**:
   ::

    anemometer:
        angle: 10e-6

#. With ``float-values: {forbid-nan: true}``

   the following code snippets would **FAIL**:
   ::

    anemometer:
        angle: .NaN

 #. With ``float-values: {forbid-inf: true}``

   the following code snippets would **FAIL**:
   ::

    anemometer:
        angle: .inf
"""

import re

import yaml

from yamllint.linter import LintProblem


ID = 'float-values'
TYPE = 'token'
CONF = {
    'require-numeral-before-decimal': bool,
    'forbid-scientific-notation': bool,
    'forbid-nan': bool,
    'forbid-inf': bool,
}
DEFAULT = {
    'require-numeral-before-decimal': False,
    'forbid-scientific-notation': bool,
    'forbid-nan': False,
    'forbid-inf': False,
}

IS_NUMERAL_BEFORE_DECIMAL_PATTERN = re.compile(
    '[-+]?(\.[0-9]+)([eE][-+]?[0-9]+)?')
IS_SCIENTIFIC_NOTATION_PATTERN = re.compile(
    '[-+]?(\.[0-9]+|[0-9]+(\.[0-9]*)?)([eE][-+]?[0-9]+)')
IS_INF_PATTERN = re.compile('[-+]?(\.inf|\.Inf|\.INF)')
IS_NAN_PATTERN = re.compile('\.nan|\.NaN|\.NAN')


def check(conf, token, prev, next, nextnext, context):
    if prev and isinstance(prev, yaml.tokens.TagToken):
        return
    if not isinstance(token, yaml.tokens.ScalarToken):
        return
    if token.style:
        return
    val = token.value

    if conf['forbid-nan'] and IS_NAN_PATTERN.match(val):
        yield LintProblem(
            token.start_mark.line + 1, token.end_mark.column + 1,
            'forbidden nan value "%s"' %
            token.value
        )

    if conf['forbid-inf'] and IS_INF_PATTERN.match(val):
        yield LintProblem(
            token.start_mark.line + 1, token.end_mark.column + 1,
            'forbidden inf value "%s"' %
            token.value
        )

    if conf['forbid-scientific-notation'] and IS_SCIENTIFIC_NOTATION_PATTERN.match(val):
        yield LintProblem(
            token.start_mark.line + 1, token.end_mark.column + 1,
            'forbidden scientific notation value "%s"' %
            token.value
        )

    if conf['require-numeral-before-decimal'] and IS_NUMERAL_BEFORE_DECIMAL_PATTERN.match(val):
        yield LintProblem(
            token.start_mark.line + 1, token.end_mark.column + 1,
            'Decimals must have a 0 prefix (ex. 0.0). Forbidden decimal missing prefix "%s"' %
            token.value
        )