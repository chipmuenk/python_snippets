# -*- coding: utf-8 -*-
"""
 === DFT_MA_Filt.py ========================================================

Python Aufgabe zu "DFT eines Moving-Average-Filters"

Berechnung und Darstellung der DFT in Python (erste Version mit Fehlern)

(c) 2014-Feb-04 Christian Münker - Files zur Vorlesung "DSV auf FPGAs"
===========================================================================
"""
from __future__ import division, print_function, unicode_literals

from numpy import arange
from numpy.fft import fft

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, plot, stem, grid, xlabel, ylabel, subplot

h = [1,1,1,1]
n = arange(len(h))
figure(1);
subplot(211)
stem(n,h)
ylabel(r"$h[n] \; \rightarrow$")
xlabel(r"$n \; \rightarrow$")
subplot(212)
H = fft(h,4)
k = arange(len(H))
stem(k,abs(H))

xlabel(r"$k \; \rightarrow$")
ylabel(r"$|H[k]| \; \rightarrow$")
plt.tight_layout()
plt.show()
