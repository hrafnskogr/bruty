#!/usr/bin/python3
import sys
import argparse
import signal
from math import log
import encodings

# nu = "0123456789"
# lo = "abcdefghijklmnopqrstuvwxyz"
# up = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# sp = "!@#$%^&*()-_+=~`[]{}|\:;\"'<>,.?/\\ "

_piped = False
_args = None
_index = 0

def main():
	global _args
	global _piped
	global _index

	if not sys.stdin.isatty():
		_piped = True

	args_inquisitor()

	if _piped:
		with open(0, 'r', errors='ignore') as f:
			for line in f:
				entropy(line.replace("\n", ""))
				_index += 1
	else:
		print("")
		for w in _args.words:
			entropy(w)
			_index += 1

	sys.exit(0)

def entropy(word):
	global _args
	global _piped
	global _index

	wlen = len(word)

	charspace = 0

	if(_args.charspace > 0):
		charspace = _args.charspace
	else:
		charspace = compute_charspace(word)

	if(charspace is None):
		return
	
	guesses = charspace**wlen

	#o = []
	#for c in word:
	#	o.append(str(ord(c)))
		
	#print("{} {} {} {} {}".format(word, "|".join(o), guesses, charspace, wlen))
	
	entro = log(guesses,2)

	if( (entro >= _args.tmin) and (entro <= _args.tmax)):
		if not _piped:
			print("="*10)
		print("#{} | Word: \"\033[94m{}\033[0m\" | Len: {} | Charspace: {} | Guesses: {} | Entropy:\033[91m {:.2f} \033[0m".format(_index, word, wlen, str(charspace), str(guesses), entro))
		if not _piped:
			print("="*10)
			print("")

def compute_charspace(word):
	cspace = 0

	lo = False
	up = False
	nu = False
	sp = False

	for c in word:
		val = ord(c)
		if((val > 47) and (val < 58)):
			nu = True
		elif((val > 64) and (val < 91)):
			up = True
		elif((val > 96) and (val < 123)):
			lo = True
		elif( ((val > 31) and (val < 48)) or ((val > 57) and (val < 65)) or ((val > 90) and (val < 97)) or((val > 122) and (val < 127)) ):
			sp = True
		else:
			# non-printable character, we skip this word
			return None

	cspace += 10 if nu is True else 0
	cspace += 26 if lo is True else 0
	cspace += 26 if up is True else 0
	cspace += 33 if sp is True else 0

	return cspace	

def signal_handler(sig, frame):
	print("\033[0m")
	sys.exit(0)

def args_inquisitor():
	global _args
	global _piped

	parser = argparse.ArgumentParser(description="Compute entropy of words. Accepts inline or stdin")

	if not _piped:
		parser.add_argument('words', nargs="+", help="words to be used for the entropy calculation")
	parser.add_argument('-t', '--minThresh', help="Output results only if entropy is higher or equal to this value", type=int, default=0, dest="tmin")
	parser.add_argument('-T', '--maxThresh', help="Output results only if entropy is less or equal to this value", type=int, default=1000000, dest="tmax")
	parser.add_argument('-c', '--charspace', help="Override auto charspace calculation with this value", type=int, default=-1)	

	_args = parser.parse_args()

if( __name__ == "__main__"):
	signal.signal(signal.SIGINT, signal_handler)
	main()

