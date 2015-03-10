#!/bin/bash
"""
    hashcollider
    Copyright (C) 2015  Davide Gessa

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import time
import imp
import sys

__AUTHOR__ = "Davide Gessa (gessadavide@gmail.com)"


def loadSynonyms (syn_f):
	f = open (syn_f, 'r')
	d = f.read ().split ('\n')
	f.close ()
	syndict = {}
	
	for line in d:
		if len (line) > 0 and line[0] == '#':
			continue

		line = line.split (';')
		syndict[line[0]] = line[1:]		

	return syndict


""" 
	Dato un testo, un db di sinonimi, ed una lista di id di sinonimi, 
	genera una nuova stringa | sia la stringa base con i sinonimi 
	specificati dalla lista eid.
	I replace vengono fatti solo alle stringhe tra %[ ]%
"""
def encodeString (base, syn, eid):
	ntext = base
	sp = base.split ('%[')[1:]
	i = 0

	for s in sp:
		v = s.split (']%')[0]

		if eid[i] == 0:
			nv = v
		else:
			nv = syn[v][eid[i]-1]

		ntext = ntext.replace ('%['+v+']%', nv)
		i += 1

	return ntext


"""
	0 0 0 0 0 0 0 0
	1 0 0 0 0 0 0 0
	2 0 0 0 00 0 0 0
	0 1 0 0 0 0 00 0 0

"""
def nextEID (base, syn, eid):
	sp = base.split ('%[')[1:]
	i = 0

	for s in sp:
		v = s.split (']%')[0]

		if eid[i] < (len (syn[v])):
			eid[i] += 1
			return eid

		elif eid[i] == (len (syn[v])):
			eid[i] = 0
			i += 1
	return None


def estimateNumber (base, syn):
	sp = base.split ('%[')[1:]
	n = 1

	for s in sp:
		v = s.split (']%')[0]

		n *= (len (syn[v]) + 1)
	return n



if __name__ == "__main__":
	if len (sys.argv) < 5:
		print 'usage: hashcollider.py baseFile synonymsFile hash hashFunc.py'
		sys.exit (0)

	print '* hashcollider.py by',__AUTHOR__,'is starting.'
	
	base_uri = sys.argv[1]
	syn_uri = sys.argv[2]
	hash_str = sys.argv[3]

	try:
		print '* Loading hash function hashf/'+sys.argv[4]+'.py ...',
		hfunc = imp.load_source('module.name', './hashf/'+sys.argv[4]+'.py')

		if hfunc.evaluteHash ('hashcollider') == hfunc.evaluteHash ('hashcollider'):
			print 'ok'
		else:
			print 'fail'
			sys.exit (0)
	except:
		print 'fail'
		print 'wrong hash function', sys.argv[4]
		sys.exit (0)


	base = open (base_uri, 'r').read ().replace ('\n', '').replace ('\0', '').replace ('\r', '')
	nsub = len (base.split ('%')) / 2
	s = loadSynonyms (syn_uri)
	e = [0] * nsub
	found = False
	i = 0
	tot = estimateNumber (base, s)
	t0 = time.time ()

	while not found and e != None:
		i += 1
		ntext = encodeString (base, s, e)
		h = hfunc.evaluteHash (ntext)

		#print ntext

		if i % 30000 == 0:
			t1 = time.time ()
			f = 30000.0/(t1-t0)
			t0 = t1
			p = 100*i/tot
			print e, '\t|\t', str(i)+' of '+str(tot)+' ('+str(p)+'%)', '\t|\t', str(int (f))+' t/s','(ETA: '+str(int ((tot - i) / f / 60)/60.0)+' hours)'


		if (h == hash_str):
			print e, h, i
			print ntext
			found = True

			f = open ('result.txt','w')
			f.write (ntext)
			f.close ()

			print '* Result written in result.txt'
		else:
			e = nextEID (base, s, e)


	print '* End in',i,'iteractions'
