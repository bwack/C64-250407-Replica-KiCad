#!/usr/bin/env python

# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Name:     gen_model
# Purpose:  A script to create a 3d resistor model (WRL) with color correct rings according to value.
#           Note : this version works with KiCad v4 or v5
#
# Author:   Bob Cousins
# License:  Creative Commons CC0  Copyright Bob Cousins 2018
# Credits:  Input for the resistor models requires https://github.com/KammutierSpule/kicad3Dmodels
#           
# Usage:
#  1. Save the file "gen_model.py" somewhere
#
# To generate a file for a single resistor:
#
#    $ python -v <value>
# where value is a decimal, e.g.
#    $ python -v 4700
#
# To update a pcb file with resistor models:
#
#  1. Make sure the pcb file is closed in KiCad
#  2. $ gen_model.py -pcb <pcb file>
#  3. Open the pcb file in KiCad
#-------------------------------------------------------------------------------

import argparse
import shutil
import os
import sys
import re

#import pcbnew

def value_to_float(x):
    if type(x) == float or type(x) == int:
        return x
    if type(x) == str and (x.isdigit()) == True:
        return float(x)
    if 'K' in x:
        if len(x) > 1:
            return float(x.replace('K', '')) * 1000
        return 1000.0
    if 'M' in x:
        if len(x) > 1:
            return float(x.replace('M', '')) * 1000000
        return 1000000.0
    if 'B' in x:
        return float(x.replace('B', '')) * 1000000000
    return 0.0

class ModelGenerator:

    def __init__(self):
        self.source_folder = '3D-models'
        self.bands = 4

#        if 'KISYS3DMOD' in os.environ:
#            self.ki_packages3d_dir = os.environ['KISYS3DMOD']
#        else:
        self.ki_packages3d_dir = '3D-models'

        self.custom_folder = os.path.join (self.ki_packages3d_dir, "Resistors_THT_custom.3dshapes")
        if not os.path.exists (self.custom_folder):
            os.makedirs(self.custom_folder)

    def get_model_filename (self, value):
        return 'res_%dband_%g.wrl' % (self.bands, float(value))


    def generate_model (self, value):

	print (value)
        dest_name = os.path.join (self.custom_folder, self.get_model_filename (value))

        # copy the resistor model
        res_body_filename = 'RESAD780W55L630D240B.wrl'
        shutil.copy (os.path.join(self.source_folder, res_body_filename), dest_name)

        # copy the rings
        outf = open (dest_name, "a")

        transforms = []
        transforms.append ("translation -.90 0 .51 scale .55 1.22 1.22")
        transforms.append ("translation -.53 0 .51 scale .55 1.04 1.04")
        transforms.append ("translation -.18 0 .51 scale .55 1.03 1.03")
        if self.bands == 5:
            transforms.append ("translation .17 0 .51 scale .55 1.03 1.03")
        transforms.append ("translation 0.80 0 .51 scale .55 1.22 1.22") # tolerance

        mag = 0
        max = 100 if self.bands == 4 else 1000

        while value < max/10:
            mag -= 1
            value *= 10

        while value >= max:
            value /= 10
            mag += 1

        # 4/5 band code
        digits = []
        if self.bands == 5:
            digits.append ((value / 100) % 10)
        digits.append (int(value / 10) % 10)
        digits.append (int(value) % 10)

        if mag>=0:
            digits.append (mag)
        elif mag == -1:
            digits.append (10) # gold = x0.1
        elif mag == -2:
            digits.append (11) # silver = x0.01

        # 10 is gold, 11 is silver
        digits.append (10)

        for j in range (0,self.bands):
            digit  = digits [j]

            source_filename = os.path.join(self.source_folder, 'ring_%d.wrl' % digit)

            with open(source_filename) as file:
                ring_data = [line.rstrip() for line in file]

            seen_start = False
            for line in ring_data:
                if "geometry" in line and not seen_start:
                    outf.write ("Transform { %s children [ \n" % transforms[j])
                    seen_start = True
                else:
                    line = re.sub ("RES-RING-COLOR", "RES-RING-COLOR-P%d" % j, line)

                outf.write (line + '\n')

            outf.write (" ] }")

        #
        outf.close()

# this function does not work..
def pcbfunc(Filename = None):
    if Filename: 
        my_board = pcbnew.LoadBoard (Filename)
    else:
        my_board = pcbnew.GetBoard()

    # for v5 use GetLibItemName() instead of GetFootprintName()
    for module in my_board.GetModules():
        models = module.Models()
        print ("%s \"%s\"  " % ( module.GetReference(), 
                                    module.GetValue() ))
                                    #module.GetModels() ) )
        print models

def change_extension (filename, ext):
    path, filename = os.path.split (filename)
    basename = os.path.splitext (filename)[0]
    return os.path.join (path, basename + ext)

def get_next_line(file):
    line = file.readline()
    if line:
        line = line.rstrip()
    return line

def parse_pcb(Filename, model_gen):

    f = open(Filename, 'r')
    outfilename = change_extension (Filename, ".new")
    out = []

    line = f.readline()
    while line:
        line = line.rstrip()
        print ("|-- " + line)

        if "module" in line and "RESISTOR" in line:
            tokens = line.split()
            module = tokens[1]
            #print module

            out.append (line)
            line = get_next_line(f)
            print ("--- " + line)
            while line and line != "  )":
                if "model" in line:
                    tokens = line.split()
                    model = tokens[1]
                    print "   model=" + tokens[1]

                    if "Resistor_THT" in module :
                        # check if alrady exists?
                        # check pitch?
                        model_gen.generate_model (value)
                        if 'KISYS3DMOD' in os.environ:
                            line = "    (model ${KISYS3DMOD}/Resistors_THT_custom.3dshapes/%s" % model_gen.get_model_filename (value)
                        else:
                            line = "    (model %s/%s" % (model_gen.custom_folder, model_gen.get_model_filename (value) )

                        print module
                        print "  value = ", value
                        print "  model = ", model_gen.get_model_filename (value)

                        out.append (line)
                        out.append ("      (at (xyz %f 0 0))" % (0.3/2.0) )
                        out.append ("      (scale (xyz 1 1 1))")
                        out.append ("      (rotate (xyz 0 0 0))")
                        out.append ("    )")

                        # skip 4 lines
                        line = get_next_line(f)
                        #print ("---- " + line)
                        line = get_next_line(f)
                        #print ("---- " + line)
                        line = get_next_line(f)
                        #print ("---- " + line)
                        line = get_next_line(f)
                        #print ("---- " + line)
                        line = get_next_line(f)
                        #print ("---- " + line)

                        while line and line != "  )":
                            if "value" in line:
                                tokens = line.split()
                                value = value_to_float(tokens[2])
                                print line
                                print "   value=", tokens[2], value
                            line = get_next_line(f)

                out.append (line)
                line = get_next_line(f)
                #print ("---- " + line)

        out.append (line)
        line = f.readline()

    f.close()
    f = open(outfilename, "w")
    for line in out:
        f.write (line + '\n')
    f.close()

    shutil.copy (outfilename, Filename)

# main

try:
    args = sys.argv
except:
    args = None

if args:
    parser = argparse.ArgumentParser(description="Generate resistor model")
    parser.add_argument("-v", "--value", help="resistor value")
    parser.add_argument("--pcb", help="kicad_pcb file")
    args = parser.parse_args()

    if args.value:
        model_gen = ModelGenerator ()
        model_gen.bands = 4
        model_gen.generate_model (value_to_float(args.value))

    elif args.pcb:
        model_gen = ModelGenerator ()
        model_gen.bands = 4
        parse_pcb (args.pcb, model_gen)
else:
    parser.print_help()

    # pcbfunc()

