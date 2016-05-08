#!/usr/bin/env python

# Copyright 2016 NeuroData (http://neurodata.io)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# multiplot.py
# Created by Greg Kiar on 2016-03-29.
# Email: gkiar@jhu.edu

from collections import OrderedDict
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys



class feature_plot():

    def __init__(self, data, names, figtitle, fig_outfile=None, plot_mode='bar',
                 xlab = None, ylab = None, axis_scale = None, yscale = None, xscale = None,
                 ylims = None, xlims = None, scale_factor = None):
        """
        Plots multiple populations of histograms in the same figure.
        Expects:
            fnames: list of filenames, each of which is a pickle dictionary containing
                    pdfs and x values over which they were evaluated
            names: list of length equal to filenames, which is the coloquial name of the
                   dataset we want in the figure title
        """
        self.data = data
        self.names = names
        self.fig_outfile = fig_outfile
        self.figtitle = figtitle
        self.ylims = ylims
        self.xlims = xlims
        self.scale_factor = scale_factor
        self.ylab = ylab
        self.xlab = xlab
        self.axis_scale = axis_scale
        self.xscale = xscale
        self.yscale = yscale
        if plot_mode == 'bar' :
            self.bar_plot()
        elif plot_mode == 'scatter' :
            self.scatter_plot()
        elif plot_mode == 'series' :
            self.series_plot()
        else :
            self.hist_plot()

    def bar_plot(self):
        """
        Plots series of histograms in a single figure
        """
        
        """
        Setup plot shape, etc.
        """
        N = len(self.names)
        ds = list()
        count = 0
        while len(ds) == 0:
            ds = list(self.factors(N+count))
            count += 1
            print ds
        if len(ds) == 1:
            ds = list((ds[0], ds[0]))
        fig = plt.figure(figsize=(4*ds[-1], 4*ds[0]))
        bl = ds[-1]*(ds[0]-1)

        """
        Actually plot things
        """
        for idx, set in enumerate(self.data.keys()):
            ax = plt.subplot(ds[0], ds[-1], idx+1)
            plt.hold(True)
            plt.bar(range(len(self.data[set])),self.data[set].values(), alpha=0.7, color='#888888')
            plt.title(set, y = 1.04)
            if idx == bl:
                plt.ylabel('Count')
                plt.xlabel('Graph')
            plt.xlim((0, len(self.data[set].keys())))
            if self.ylims is not None:
                plt.ylim(self.ylims)

            plt.tight_layout()

        if self.fig_outfile is not None:
            plt.savefig(self.fig_outfile)
        plt.show()

    def scatter_plot(self):
        """
        Plots series of histograms in a single figure
        """
        
        """
        Setup plot shape, etc.
        """
        N = len(self.names)
        fig = plt.figure(figsize=(1.2*N, 1*N))
        
        """
        Actually plot things
        """
        ax = plt.subplot(1,1,1)
        plt.hold(True)
        for idx, set in enumerate(self.data.keys()):
            plt.scatter(self.rand_jitter( [idx]*len(self.data[set].values()) ),self.data[set].values(), alpha=0.1, color='#000000')

        plt.title(self.figtitle, y = 1.04)
        plt.ylabel('Count')
        ax.set_xticks(np.arange(len(self.names)))
        ax.set_xticklabels(self.names, rotation=40)
        plt.xlabel('Dataset')
        plt.xlim([-0.5, len(self.names)-0.5])
        if self.ylims is not None:
            plt.ylim(self.ylims)

        plt.tight_layout()

        if self.fig_outfile is not None:
            plt.savefig(self.fig_outfile)
        plt.show()


    def hist_plot(self):
        """
        Plots series of histograms in a single figure
        """

        """
        Set up plotting area
        """
        eps = 1e-9/2
        N = len(self.names)
        ds = list()
        count = 0
        while len(ds) == 0:
            ds = list(self.factors(N+count))
            count += 1
        
        if len(ds) == 1:
            ds = list((ds[0], ds[0]))
        fig = plt.figure(figsize=(4*ds[-1], 4*ds[0]))
        bl = ds[-1]*(ds[0]-1)
        
        """
        Actually plot things
        """
        for idx, set in enumerate(self.data.keys()):
            ax = plt.subplot(ds[0], ds[-1], idx+1)
            plt.hold(True)
            for subj in self.data[set]:
                dens = gaussian_kde(self.data[set][subj])
                x = np.linspace(0, 1.2*np.max(self.data[set][subj]), 1000)
                if self.scale_factor is not None:
                    plt.plot(x/int(self.scale_factor), dens.pdf(x)*int(self.scale_factor), color='#000000', alpha=0.07)
                elif self.xscale is not None:
                    plt.plot(x/int(self.xscale), dens.pdf(x), color='#000000', alpha=0.07)
                elif self.yscale is not None:
                    plt.plot(x, dens.pdf(x)*int(self.yscale), color='#000000', alpha=0.07)
                else:
                    plt.plot(x, dens.pdf(x), color='#000000', alpha=0.07)
            plt.title(set)
            if self.axis_scale == 'log':
                plt.xscale('log')

            if idx == bl:
                if self.ylab is not None:
                    plt.ylabel(self.ylab)
                if self.xlab is not None:
                    plt.xlabel(self.xlab)

                plt.tight_layout()

        if self.fig_outfile is not None:
            plt.savefig(self.fig_outfile)
        plt.show()
        
        
    def series_plot(self):
        """
        Plots series of histograms in a single figure
        """

        """
        Set up plotting area
        """
        eps = 1e-9/2
        N = len(self.names)
        ds = list()
        count = 0
        while len(ds) == 0:
            ds = list(self.factors(N+count))
            count += 1
        
        if len(ds) == 1:
            ds = list((ds[0], ds[0]))
        fig = plt.figure(figsize=(4*ds[-1], 4*ds[0]))
        bl = ds[-1]*(ds[0]-1)
        
        """
        Actually plot things
        """
        for idx, set in enumerate(self.data.keys()):
            ax = plt.subplot(ds[0], ds[-1], idx+1)
            plt.hold(True)
            for subj in self.data[set]:
                dens = self.data[set][subj]
                x = np.linspace(1, len(self.data[set][subj]), len(self.data[set][subj]))
                if self.scale_factor is not None:
                    plt.plot(x/int(self.scale_factor), dens*int(self.scale_factor), color='#000000', alpha=0.07)
                elif self.xscale is not None:
                    plt.plot(x/int(self.xscale), dens, color='#000000', alpha=0.07)
                elif self.yscale is not None:
                    plt.plot(x, dens*int(self.yscale), color='#000000', alpha=0.07)
                else:
                    plt.plot(x, dens, color='#000000', alpha=0.07)
            plt.title(set)
            if self.axis_scale == 'log':
                plt.xscale('log')

            if idx == bl:
                if self.ylab is not None:
                    plt.ylabel(self.ylab)
                if self.xlab is not None:
                    plt.xlabel(self.xlab)

                plt.tight_layout()

        if self.fig_outfile is not None:
            plt.savefig(self.fig_outfile)
        plt.show()
        
        
        
    
    def rand_jitter(self, arr):
        stdev = .03*(max(arr)-min(arr)+2)
        return arr + np.random.randn(len(arr)) * stdev
        
    def factors(self, N): 
        return set([item for subitem in 
                    [(i, N//i) for i in range(1, int(N**0.5) + 1) if N % i == 0 and i > 1]
                    for item in subitem])