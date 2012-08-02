#! /usr/bin/env python

# Copyright (c) 2012 Victor Terron. All rights reserved.
# Institute of Astrophysics of Andalusia, IAA-CSIC
#
# This file is part of LEMON.
#
# LEMON is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import datetime

# LEMON modules
import snr

def curve_plot(figure, curve, marker = 'o', color = ''):
    """ Plot the light curve as a subplot of the matplotlib Figure.

    The method removes from 'figure' all the existing axes and adds a new one,
    plotting the differential magnitudes as a function of time, and including
    the error bars which can be derived from the signal-to-noise ratios. The
    original matplotlib Figure instance is modified, so nothing is returned.

    Keyword arguments:
    marker - format string character, which is passed down to matplotlib, that
             controls the line style. The default value, 'o', defines circle
             markers, while '-.', for example, uses the dash-dot line style.
             Please refer to the matplotlib documentation for details.
    color - the string which determines the color of the markers. Abbreviations
            such as 'g', full names ('green') and hexadecimal strings
            ('#008000'), among others, can be given. With an empty string,
            the first element of the matplotlib cycle of colors is used.

    """

    # Remove existing subplots plots, if any
    figure.clear()
    for axes in figure.get_axes():
        figure.delaxes(axes)

    unix_times, magnitudes, snrs = zip(*curve)
    # Plot Python datetime instances, instead of Unix seconds
    datetimes = [datetime.datetime.utcfromtimestamp(x) for x in unix_times]

    # For each signal-to-noise ratio we want the equivalent error in mags;
    # that is, both the maximum and minimum values induced by the noise.
    negative_errors = []
    positive_errors = []
    for s in snrs:
        min_error, max_error = snr.snr_to_error(s)
        negative_errors.append(abs(min_error))
        positive_errors.append(max_error)

    ax1 = figure.add_subplot(111)
    ax1.errorbar(datetimes, magnitudes, fmt = color + marker,
                  yerr = (negative_errors, positive_errors))
    ax1.set_ylabel("Magnitude (diff)")
    ax1.grid(True)

    # Use 5% of the height of the plot as the upper and bottom margin of the
    # magnitudes, so that the curves do not touch the border. Also, reverse the
    # y-axis, as we want the light curve to go up when the star is brighter;
    # that is, as the differential magnitude becomes smaller.
    max_mag = max(magnitudes)
    min_mag = min(magnitudes)
    margin_mag = (max_mag - min_mag) * 0.05
    ax1.set_ylim(max_mag + margin_mag, min_mag - margin_mag)

    # We also want a similar margin on the x-axis; the dates of the
    # observations should not touch the border of the plot either.
    elapsed_seconds = (unix_times[-1] - unix_times[0])
    margin_seconds = elapsed_seconds * 0.05
    margin_delta = datetime.timedelta(seconds = margin_seconds)
    ax1.set_xlim(datetimes[0] - margin_delta, datetimes[-1] + margin_delta)
