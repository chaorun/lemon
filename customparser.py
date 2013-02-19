#! /usr/bin/env python

# Copyright (c) 2013 Victor Terron. All rights reserved.
# Institute of Astrophysics of Andalusia, IAA-CSIC
#
# This file is part of LEMON.
#
# LEMON is free software: you can redistribute it and/or modify
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

import optparse
import textwrap

class NewlinesFormatter(optparse.IndentedHelpFormatter):
    """ This quick-and-dirty trick prevents optparse from stripping newlines
    (using textwrap) when the description of the module is printed. This should
    be acceptable enough until the transition to argparse is made. """

    def _format_text(self, text):
        text_width = self.width - self.current_indent
        indent = ' ' * self.current_indent
        # Wrap one paragraph at a time, then concatenate them
        formatted_text = ""
        for paragraph in text.split('\n\n'):

            formatted_text += textwrap.fill(paragraph.strip(),
                                            text_width,
                                            initial_indent=indent,
                                            subsequent_indent=indent)
            formatted_text += '\n\n'

        return formatted_text.rstrip()


def get_parser(description):
    """ Return the OptionParser object used in the LEMON modules.

    This function instantiates an optparse.OptionParser object and returns it.
    Its 'description' argument (a paragraph of text giving a brief overview of
    the program) is set to the value of the argument of the same name, while
    the NewlinesFormatter class is used for printing help text ('formatter'
    argument).

    """

    kwargs = dict(description = description,
                  formatter = NewlinesFormatter())
    parser = optparse.OptionParser(**kwargs)
    return parser

