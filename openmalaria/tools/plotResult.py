#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# This file is part of the openmalaria.tools package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/openmalaria.tools
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from optparse import OptionParser
import sys
import math
from numbers import Number

import numpy
import matplotlib.pyplot as plt
from matplotlib.colors import cnames

from openmalaria.tools.readOutput import Keys, ValDict


measureNames = {
    0: 'nHost',
    1: 'nInfect',
    2: 'nExpectd',
    3: 'nPatent',
    4: 'sumLogPyrogenThres',
    5: 'sumlogDens',
    6: 'totalInfs',
    7: 'nTransmit',
    8: 'totalPatentInf',
    9: 'contrib',
    10: 'sumPyrogenThresh',
    11: 'nTreatments1',
    12: 'nTreatments2',
    13: 'nTreatments3',
    14: 'nUncomp',
    15: 'nSevere',
    16: 'nSeq',
    17: 'nHospitalDeaths',
    18: 'nIndDeaths',
    19: 'nDirDeaths',
    20: 'nEPIVaccinations',
    21: 'allCauseIMR',
    22: 'nMassVaccinations',
    23: 'nHospitalRecovs',
    24: 'nHospitalSeqs',
    25: 'nIPTDoses',
    26: 'annAvgK',
    27: 'nNMFever',
    30: 'innoculationsPerAgeGroup',
    28: 'innoculationsPerDayOfYear',
    29: 'kappaPerDayOfYear',
    31: 'Vector_Nv0',
    32: 'Vector_Nv',
    33: 'Vector_Ov',
    34: 'Vector_Sv',
    35: 'Vector_EIR_Input',
    36: 'Vector_EIR_Simulated',
    39: 'Clinical_RDTs',
    40: 'Clinical_DrugUsage',
    41: 'Clinical_FirstDayDeaths',
    42: 'Clinical_HospitalFirstDayDeaths',
    43: 'nNewInfections',
    44: 'nMassITNs',
    45: 'nEPI_ITNs',
    46: 'nMassIRS',
    47: 'nMassVA',
    48: 'Clinical_Microscopy',
    49: 'Clinical_DrugUsageIV',
    50: 'nAddedToCohort',
    51: 'nRemovedFromCohort',
    52: 'nMDAs',
    53: 'nNmfDeaths',
    54: 'nAntibioticTreatments',
    55: 'nMassScreenings',
    56: 'nMassGVI',
    57: 'nCtsIRS',
    58: 'nCtsGVI',
    59: 'nCtsMDA',
    60: 'nCtsScreenings',
    61: 'nSubPopRemovalTooOld',
    62: 'nSubPopRemovalFirstEvent',
    63: 'nPQTreatments',
    64: 'nTreatDiagnostics',
    65: 'nMassRecruitOnly',
    66: 'nCtsRecruitOnly',
    67: 'nTreatDeployments',
    68: 'sumAge',
    69: 'nInfectByGenotype',
    70: 'nPatentByGenotype',
    71: 'logDensByGenotype',
    72: 'nHostDrugConcNonZero',
    73: 'sumLogDrugConcNonZero',
    74: 'expectedDirectDeaths',
    75: 'expectedHospitalDeaths',
    76: 'expectedIndirectDeaths',
    77: 'expectedSequelae',
    78: 'expectedNumSevere'
}

# List of measure groups. Each includes name, boolean (true if use log scale),
# and per-measure information. For each measure, list: id, name, colour
#TODO: add log/linear scale info. But is this useful??
# Note: color names are defined by matplotlib:
# /usr/lib64/python3.3/site-packages/matplotlib/colors.py
combinedMeasures = [
    ('hosts', [(0, 'all', 'black'), (72, 'hosts with non-zero drug conc', 'green')]),
    ('infected hosts', [(1, 'all', 'red'), (2, 'expected', 'green'), (3, 'patent', 'blue'), (43, 'new', 'purple'),
                        (69, 'all (by genotype)', 'orange'), (70, 'patent (by genotype)', 'black')]),
    ('sum log', [(4, 'pyrogenic threshold', 'purple'), (5, 'parasite density', 'green'),
                 (71, 'parasite density (by genotype)', 'orange')]),
    ('total infections', [(6, 'all', 'red'), (8, 'patent', 'blue')]),
    ('transmitting humans', [(7, 'sum(p(transmit))', 'green'), (26, 'annual sum(p(transmit)) / annual EIR', 'blue')]),
    ('sum pyrog thres', [(10, 'sum pyrogenic threshold', 'purple')]),
    ('uncomp cases', [(14, 'UC episodes', 'green'), (11, 'UC treatments 1', 'blue'), (12, 'UC treatments 2', 'purple'), (63, 'primaquine', 'darkblue')]),
    ('severe cases', [(13, 'hospital treatments', 'blue'), (15, 'severe episodes', 'green'), (78, 'expected severe', 'red')]),
    ('NMFs', [(27, 'NMF episodes', 'green'), (54, 'antibiotic treatments', 'blue')]),
    ('sequelae', [(16, 'all cases', 'green'), (24, 'hospital', 'orange'), (77, 'expected', 'red')]),
    ('direct deaths', [(17, 'in-hospital', 'orange'), (19, 'all direct deaths', 'red'), (74, 'expected direct deaths', 'black'),
                       (75, 'expected in-hospital', 'darkgreen'), (42, 'first day hospital', 'green'), (41, 'first day', 'brown')]),
    ('indirect deaths', [(18, 'indirect malaria deaths', 'pink'), (53, 'non-malaria fevers', 'blue'), (76, 'expected indirect malaria', 'purple')]),
    ('vaccination doses', [(20, 'EPI', 'green'), (22, 'mass', 'grey')]),
    ('drug doses (MDA/MSAT)', [(25, 'IPT', 'brown'), (52, 'MDA (timed)', 'purple'), (59, 'MDA (cts)', 'pink')]),
    ('infant mortality rate', [(21, 'IMR', 'red')]),
    ('hospital recoveries', [(23, 'hospital recoveries', 'orange')]),
    ('inoculations', [(30, 'all', 'red')]),
    ('feeding vectors', [(31, 'emergence - N_v0', 'green'), (32, 'all - N_v', 'blue'), (33, 'infected - O_v', 'purple'),
                         (34, 'infectious - S_v', 'red')]),
    ('EIR (innocs/pers/year)', [(35, 'requested', 'orange'), (36, 'simulated', 'red')]),
    ('diagnostics used', [(39, 'RDTs', 'purple'), (48, 'microscopy', 'brown'), (55, 'MSAT (timed)', 'orange'),
                          (60, 'MSAT (cts)', 'darkred'), (64, 'treatment', 'brown')]),
    ('drug usage (mg)', [(40, 'oral', 'blue'), (49, 'intrevenous', 'orange')]),
    ('bed nets', [(44, 'ITNs (timed)', 'darkgreen'), (45, 'ITNs (cts)', 'green')]),
    ('IRS', [(46, 'IRS (timed)', 'darkred'), (57, 'IRS (cts)', 'red')]),
    ('GVI', [(47, 'deterrents (timed)', 'brown'), (56, 'GVI (timed)', 'darkblue'), (58, 'GVI (cts)', 'blue')]),
    ('cohort delta', [(50, 'added', 'orange'), (51, 'removed', 'blue')]),
    ('sub-pop removals', [(61, 'too old', 'brown'), (62, 'first event', 'red')]),
    ('recruit only', [(65, 'timed', 'purple'), (66, 'cts', 'pink')]),
    ('intervention deployments', [(67, 'via CM', 'grey')]),
    ('host age', [(68, 'sum', 'darkred')]),
    ('user defined', [(90, '90', 'red'), (91, '91', 'brown'), (92, '92', 'green')]),
    ('sum log', [(73, 'drug concentration', 'green')]),
]
appendMeasureNumber = None


def measureNumber(m):
    if appendMeasureNumber:
        return " (" + str(m) + ")"
    else:
        return ""


def findMeasureGroup(m):
    for i in range(len(combinedMeasures)):
        for md in combinedMeasures[i][1]:
            if m == md[0]:
                return i
    raise KeyError("measure " + str(m) + " not in combinedMeasures")


def getMeasureLabel(mg, m):
    if mg is None:
        return measureNames[m] + measureNumber(m)
    else:
        for md in combinedMeasures[mg][1]:
            if m == md[0]:
                return md[1] + measureNumber(m)
        raise KeyError("measure " + str(m) + " not in combinedMeasures[" + str(mg) + "]")


def getMeasureColour(mg, m):
    if mg is None:
        return 'blue'
    else:
        for md in combinedMeasures[mg][1]:
            if m == md[0]:
                return md[2]
        raise KeyError("measure " + str(m) + " not in combinedMeasures[" + str(mg) + "]")


def ensureUnique(colour, used):
    if colour in used:
        colours = cnames.keys()
        i = 0
        while colours[i] != colour:
            i += 1
            if i >= len(colours):
                raise KeyError("colour " + colour + " not found!")
        # TODO: replace the following with a check of whether the colour is similar to any used colour
        while colours[i] in used:
            i += 1
            if i >= len(colours):
                i -= 1
                break
        colour = colours[i]
    used.add(colour)
    return colour


replaceFN = None


class MultiKey(object):
    __slots__ = ["mg", "m", "s", "g", "c", "gt", "f"]

    def __init__(self, measureGroup=None, measure=None, survey=None, group=None, cohort=None, genotype=None,
                 fileName=None):
        self.mg = measureGroup  # int index in combinedMeasures
        self.m = measure  # int
        self.s = survey  # int
        self.g = group  # int (age group or species)
        self.c = cohort  # int
        self.gt = genotype  # int
        self.f = fileName  # int

    def __and__(self, other):
        """Set each member from other if not set in self.
        Should complain if set in self and in other, but this is a bit unnecessary."""
        assert isinstance(other, MultiKey)
        first = MultiKey(self.mg, self.m, self.s, self.g, self.c, self.gt, self.f)
        if first.mg is None:
            first.mg = other.mg
        if first.m is None:
            first.m = other.m
        if first.s is None:
            first.s = other.s
        if first.g is None:
            first.g = other.g
        if first.c is None:
            first.c = other.c
        if first.gt is None:
            first.gt = other.gt
        if first.f is None:
            first.f = other.f
        return first

    @staticmethod
    def fromMeasureGroups(measureGroups):
        r = [MultiKey(measureGroup=measureGroup) for measureGroup in measureGroups]
        return r

    @staticmethod
    def fromMeasures(measures):
        r = [MultiKey(measure=measure) for measure in measures]
        return r

    @staticmethod
    def fromSurveys(surveys):
        return [MultiKey(survey=survey) for survey in surveys]

    @staticmethod
    def fromGroups(groups):
        return [MultiKey(group=group) for group in groups]

    @staticmethod
    def fromCohorts(cohorts):
        return [MultiKey(cohort=cohort) for cohort in cohorts]

    @staticmethod
    def fromGenotypes(genotypes):
        return [MultiKey(genotype=genotype) for genotype in genotypes]

    @staticmethod
    def fromFiles(files):
        return [MultiKey(fileName=fl) for fl in files]

    @staticmethod
    def expand(r, x):
        "r,x are expected to be lists of MultiKeys"
        "this creates a list of all combinations of a&b for a in r and b in x"
        lx = len(x)
        assert lx > 0, "expected len>0"
        r *= lx  # shallow copy: all references point to same object
        for i in range(len(r)):
            r[i] = r[i] & x[i % lx]

    def __str__(self):
        return self.label(MultiKey(), True)

    def label(self, base, valDict):
        r = ""
        if self.m != base.m:
            r = getMeasureLabel(self.mg, self.m)
        if self.s != base.s:
            if len(r):
                r += ","
            r += "survey " + str(self.s)
        if self.g != base.g:
            if len(r):
                r += ","
            r += "group " + str(self.g)
        if self.c != base.c:
            if len(r):
                r += ","
            r += "cohort " + str(self.c)
        if self.gt != base.gt:
            if len(r):
                r += ","
            r += "genotype " + str(self.gt)
        if self.f != base.f:
            if len(r):
                r += ","
            if replaceFN:
                r += "file " + str(self.f + 1)
            else:
                r += valDict.getFileName(self.f)
        return r


class Plotter(object):
    def __init__(self, keys):
        self.values = ValDict(keys)
        self.showLegends = None
        self.showTitle = None
        self.showXLabel = None
        self.showYLabel = None
        self.horizSubBars = None
        self.scale = None

    def read(self, fileName, filterExpr, debugFilter):
        self.values.read(fileName, filterExpr, debugFilter)
        if len(self.values.getMeasures()) == 0:
            raise Exception("No data to plot (after filtering)!")

    def plot(self, am, s, g, c, gt, f):
        x_axis = Keys.NONE
        x_label = ""
        if s == "x-axis":
            assert x_axis == Keys.NONE, "dual assignment to x-axis!"
            x_axis = Keys.SURVEY
            x_label = "survey"
        if g == "x-axis":
            assert x_axis == Keys.NONE, "dual assignment to x-axis!"
            x_axis = Keys.GROUP
            x_label = "group"
        if c == "x-axis":
            assert x_axis == Keys.NONE, "dual assignment to x-axis!"
            x_axis = Keys.COHORT
            x_label = "cohort"
        if gt == "x-axis":
            assert x_axis == Keys.NONE, "dual assignment to x-axis!"
            x_axis = Keys.GENOTYPE
            x_label = "genotype"
        if f == "x-axis":
            assert x_axis == Keys.NONE, "dual assignment to x-axis!"
            x_axis = Keys.FILE
            x_label = "file"
            x = self.values.getFileNames(replaceFN)
        assert x_axis != Keys.NONE, "nothing to plot on x-axis!"

        lines = set()
        if s == "line":
            lines.add(Keys.SURVEY)
        if g == "line":
            lines.add(Keys.GROUP)
        if c == "line":
            lines.add(Keys.COHORT)
        if gt == "line":
            lines.add(Keys.GENOTYPE)
        if f == "line":
            lines.add(Keys.FILE)

        plots = [MultiKey()]
        if am:
            measureGroups = dict()
            for m in self.values.getMeasures():
                mg = findMeasureGroup(m)
                if mg in measureGroups:
                    measureGroups[mg].append(m)
                else:
                    measureGroups[mg] = list([m])
            # note: here "measure" is used to represent "measure group"
            MultiKey.expand(plots, MultiKey.fromMeasureGroups(measureGroups.keys()))
        else:
            MultiKey.expand(plots, MultiKey.fromMeasures(self.values.getMeasures()))
        if s == "plot":
            # NOTE: probably not going to include measure 21 — this doesn't include multiple surveys
            MultiKey.expand(plots, MultiKey.fromSurveys(self.values.getSurveys(0)))
        if g == "plot":
            # like MultiKey.expand, but only using those groups applicable to each measure
            origplots = plots
            plots = list()
            for p in origplots:
                plots += [p & b for b in MultiKey.fromGroups(self.values.getGroups(p.m))]
        # TODO: cohorts and genotypes like groups?
        if f == "plot":
            # NOTE: we assume all files contain data over same measures, surveys and groups
            MultiKey.expand(plots, MultiKey.fromFiles(self.values.getFiles()))

        n = len(plots)
        d1 = int(math.ceil(math.sqrt(float(n))))
        d2 = int(math.ceil(float(n) / float(d1)))

        fig = plt.figure(1)
        plotNumber = 1
        for plot in plots:
            subplot = fig.add_subplot(d1, d2, plotNumber)
            plotNumber += 1

            m = plot.m
            if am:
                m = measureGroups[plot.mg][0]  # take first — not necessary correct but we need a measure

            if x_axis == Keys.GROUP:
                x = self.values.getGroups(m)
                x_label = self.values.getGroupLabel(m)
            elif x_axis == Keys.SURVEY:
                x = self.values.getSurveys(m)
            elif x_axis == Keys.COHORT:
                x = self.values.getCohorts(m)
            elif x_axis == Keys.GENOTYPE:
                x = self.values.getGenotypes(m)
            #else x was set previously

            pLines = [plot]

            #TODO: colour is not unique for any key other than measures from measure groups
            # i.e. we need to somehow manipulate colours to make them unique
            if Keys.SURVEY in lines:
                MultiKey.expand(pLines, MultiKey.fromSurveys(self.values.getSurveys(m)))
            if Keys.GROUP in lines:
                MultiKey.expand(pLines, MultiKey.fromGroups(self.values.getGroups(m)))
            if Keys.COHORT in lines:
                MultiKey.expand(pLines, MultiKey.fromCohorts(self.values.getCohorts(m)))
            if Keys.GENOTYPE in lines:
                MultiKey.expand(pLines, MultiKey.fromGenotypes(self.values.getGenotypes(m)))
            if Keys.FILE in lines:
                MultiKey.expand(pLines, MultiKey.fromFiles(self.values.getFiles()))

            # use to avoid reusing colours or white (and similar)
            lineColours = set()
            for colour in ['white', 'azure', 'floralwhite', 'ghostwhite', 'honeydew', 'ivory', 'snow', 'whitesmoke']:
                lineColours.add(colour)

            if self.showTitle:
                """ This is an aglomeration of all information constant in the
                plot. Unfortunately it's rather useless to show.
                # Only include y-axis info if not shown on y-axis:
                base=MultiKey(measure=plot.m) if self.showYLabel else MultiKey()
                subplot.set_title(plot.label(base,self.values))
                """
                if am:
                    measures = measureGroups[plot.mg]
                    title = "Measures " + str(measures[0])
                    for m in measures[1:]:
                        title += ", " + str(m)
                else:
                    title = "Measure " + str(plot.m)
                subplot.set_title(title)
            if self.showXLabel:
                subplot.set_xlabel(x_label)
            if self.showYLabel:
                if am:
                    y_label = combinedMeasures[plot.mg][0]
                else:
                    y_label = getMeasureLabel(plot.mg, plot.m)
                subplot.set_ylabel(y_label)
            if self.scale == "log":
                subplot.set_yscale('log')
            elif self.scale == "auto":
                pass  #TODO

            plotted = list()

            if len(x) > 1 and isinstance(x[0], Number):  # draw an xy line chart
                if am:
                    measures = measureGroups[plot.mg]
                    MultiKey.expand(pLines, MultiKey.fromMeasures(measures))

                for pLine in pLines:
                    xKeys = [pLine]
                    if x_axis == Keys.SURVEY:
                        MultiKey.expand(xKeys, MultiKey.fromSurveys(self.values.getSurveys(m)))
                    elif x_axis == Keys.GROUP:
                        MultiKey.expand(xKeys, MultiKey.fromGroups(self.values.getGroups(m)))
                    elif x_axis == Keys.COHORT:
                        MultiKey.expand(xKeys, MultiKey.fromCohorts(self.values.getCohorts(m)))
                    elif x_axis == Keys.GENOTYPE:
                        MultiKey.expand(xKeys, MultiKey.fromGenotypes(self.values.getGenotypes(m)))
                    elif x_axis == Keys.FILE:
                        MultiKey.expand(xKeys, MultiKey.fromFiles(self.values.getFiles()))
                    y = [self.values.get(k.m, k.s, k.g, k.c, k.gt, k.f) for k in xKeys]
                    colour = ensureUnique(getMeasureColour(pLine.mg, pLine.m), lineColours)
                    try:
                        plotted.append(subplot.plot(x, y, colour))
                    except ValueError, e:
                        print("Bad plot values (script error):")
                        print("x:", x)
                        print("y:", y)
                        print("colour:", colour)

                if self.showLegends and (am or len(plotted) > 1):
                    plots = [p[0] for p in plotted]
                    legends = [pLine.label(plot, self.values) for pLine in pLines]
                    subplot.legend(plots, legends, 'upper right')
            else:  # one x-coord or non-numeric x-coords: draw a bar chart
                plotted = list()
                firstLine = None
                firstStack = None

                xind = numpy.arange(len(x))
                propPlotUse = 0.95
                width = propPlotUse / len(pLines)
                xincr = 0.5 * (1.0 - propPlotUse)

                # each pLine has a vertical bar/stack for each x-position
                for pLine in pLines:
                    pLStack = [pLine]
                    if am:
                        measures = measureGroups[plot.mg]
                        MultiKey.expand(pLStack, MultiKey.fromMeasures(measures))

                    if firstLine is None:
                        firstLine = pLine
                        firstStack = pLStack

                    ytop = None
                    probBarUse = 0.8
                    subwidth = width * probBarUse / len(pLStack)
                    xsubincr = width * 0.5 * (1.0 - probBarUse)
                    lastPlotted = None
                    # each bar is a stack of one or more items
                    for pLSBlock in pLStack:
                        # finally, we have several x-positions
                        xKeys = [pLSBlock]
                        if x_axis == Keys.SURVEY:
                            MultiKey.expand(xKeys, MultiKey.fromSurveys(self.values.getSurveys(m)))
                        elif x_axis == Keys.GROUP:
                            MultiKey.expand(xKeys, MultiKey.fromGroups(self.values.getGroups(m)))
                        elif x_axis == Keys.COHORT:
                            MultiKey.expand(xKeys, MultiKey.fromCohorts(self.values.getCohorts(m)))
                        elif x_axis == Keys.GENOTYPE:
                            MultiKey.expand(xKeys, MultiKey.fromGenotypes(self.values.getGenotypes(m)))
                        elif x_axis == Keys.FILE:
                            MultiKey.expand(xKeys, MultiKey.fromFiles(self.values.getFiles()))

                        if ytop is None:
                            ytop = [0.0 for k in xKeys]
                        y = [self.values.get(k.m, k.s, k.g, k.c, k.gt, k.f) for k in xKeys]
                        colour = getMeasureColour(pLSBlock.mg, pLSBlock.m)
                        if not am:
                            colour = ensureUnique(colour, lineColours)
                        try:
                            if self.horizSubBars:
                                #multiple bars
                                lastPlotted = subplot.bar(xind + xincr + xsubincr, y, subwidth, color=colour)
                                for i in range(0, len(y)):
                                    ytop[i] = max(ytop[i], y[i])
                            else:
                                #stack
                                lastPlotted = subplot.bar(xind + xincr, y, width, color=colour, bottom=ytop)
                                for i in range(0, len(y)):
                                    ytop[i] += y[i]
                            xsubincr += subwidth
                            plotted.append(lastPlotted)
                        except ValueError, e:
                            print("Bad plot values (script error):")
                            print("x:", xind + xincr)
                            print("y:", y)
                            print("ytop:", ytop)

                    if am:
                        message = pLine.label(plot, self.values)
                        lims = subplot.get_ylim()
                        yincr = (lims[1] - lims[0]) * 0.02
                        for i in range(0, len(ytop)):
                            xl = xind[i] + xincr
                            xc = xl + width / 2.
                            yc = ytop[i] + yincr
                            if len(pLStack) > 1:
                                subplot.errorbar(xc, yc, xerr=width * probBarUse * 0.5, ecolor='black')
                                yc += yincr
                            subplot.text(
                                xc,
                                yc,
                                message,
                                ha='center', va='bottom')
                    xincr += width

                plots = [p[0] for p in plotted]
                #if len(x)>1:
                subplot.set_xticks(xind + 0.5)
                subplot.set_xticklabels(x)
                subplot.set_xlim((0.0, float(len(x))))

                if self.showLegends and (am or len(plotted) > 1):
                    legends = [block.label(firstLine, self.values) for block in firstStack]
                    subplot.legend(plots, legends, 'upper right')

        plt.show()


def main(args):
    parser = OptionParser(usage="Usage: %prog [options] FILES",
                          description="""Plots results from an OpenMalaria (surveys) output
file by time. Currently no support for simultaeneously handling
multiple files or plotting according to age group.

Valid targets for plotting keys are: none (key is aggregated), x-axis, plot, line.
If no key is set to the x-axis, the first unassigned of survey, group, cohort,
genotype, file will be assigned to the x-axis.""", version="%prog 0.1")

    parser.add_option("-e", "--filter", action="store", type="string", dest="filterExpr", default="m!=0",
                      help="Filter entries read according to this rule "
                           "(i.e. values are included when this returns true). "
                           "Parameters available: f, m, s, g, c, gt, c. "
                           "Examples: 'True', 'm!=0' (default), 'm in [11,12,13]', 's > 73 and m!=0'.")
    parser.add_option("--debug-filter", action="store_true", dest="debugFilter", default=False,
                      help="Each time FILTEREXPR is called, print input values and output. "
                           "Warning: will print a lot of data!")
    parser.add_option("-a", "--no-auto-measures", action="store_false", dest="am", default=True,
                      help="Don't automatically put similar measures on the same plot.")
    parser.add_option("-s", "--survey", action="store", type="choice", dest="s", default="none",
                      choices=["none", "x-axis", "plot", "line"], help="How to plot surveys")
    parser.add_option("-g", "--group", action="store", type="choice", dest="g", default="none",
                      choices=["none", "x-axis", "plot", "line"], help="How to plot (age) groups")
    parser.add_option("-c", "--cohort", action="store", type="choice", dest="c", default="none",
                      choices=["none", "x-axis", "plot", "line"], help="How to plot cohorts")
    parser.add_option("--genotype", action="store", type="choice", dest="gt", default="none",
                      choices=["none", "x-axis", "plot", "line"], help="How to plot genotypes")
    parser.add_option("-f", "--file", action="store", type="choice", dest="f", default="plot",
                      choices=["none", "x-axis", "plot", "line"], help="How to plot outputs from different files")
    parser.add_option("-n", "--file-names", action="store_true", dest="fullNames", default=False,
                      help="Use full file names instead of replacing with short versions")
    parser.add_option("-l", "--no-legends", action="store_false", dest="legends", default=True,
                      help="Turn off legends (sometimes they hide parts of the plots)")
    parser.add_option("-L", "--labels", action="store", type="choice", dest="labels", default="txy",
                      choices=["", "y", "x", "xy", "t", "ty", "tx", "txy"],
                      help="Show [t]itle, [x]-axis and/or [y]-axis labels: txy tx ty t xy x y or (none); default is xy")
    parser.add_option("-b", "--vertical-stack", action="store_false", dest="horizSubBars", default=True,
                      help="Where bar-plots need sub-divisions, use a vertical stack instead of horizontal sub-bars")
    parser.add_option("--scale", action="store", type="choice", dest="scale", default="auto",
                      choices=["auto", "linear", "log"],
                      help="Set y-axis scale to linear, log or auto (currently auto does nothing)")

    (options, others) = parser.parse_args(args=args[1:])
    if len(others) == 0:
        parser.print_usage()
        return 1

    if options.s != "x-axis" and options.g != "x-axis" and options.c != "x-axis" and options.gt != "x-axis" and options.f != "x-axis":
        if options.s == "none":
            options.s = "x-axis"
        elif options.g == "none":
            options.g = "x-axis"
        elif options.c == "none":
            options.c = "x-axis"
        elif options.gt == "none":
            options.gt = "x-axis"
        elif options.f == "none":
            options.f = "x-axis"
        else:
            print("Error: nothing assigned to x-axis!")
            return 1

    keys = set()
    keys.add(Keys.MEASURE)
    if options.s != "none":
        keys.add(Keys.SURVEY)
    if options.g != "none":
        keys.add(Keys.GROUP)
    if options.c != "none":
        keys.add(Keys.COHORT)
    if options.gt != "none":
        keys.add(Keys.GENOTYPE)
    if options.f != "none":
        keys.add(Keys.FILE)

    plotter = Plotter(keys)

    global appendMeasureNumber
    appendMeasureNumber = not ('t' in options.labels)
    global replaceFN
    replaceFN = not options.fullNames
    plotter.showLegends = options.legends
    plotter.showTitle = 't' in options.labels
    plotter.showXLabel = 'x' in options.labels
    plotter.showYLabel = 'y' in options.labels
    plotter.horizSubBars = options.horizSubBars
    plotter.scale = options.scale

    for output in others:
        plotter.read(output, options.filterExpr, options.debugFilter)

    plotter.plot(options.am, options.s, options.g, options.c, options.gt, options.f)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
