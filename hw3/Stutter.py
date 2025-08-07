'''
// Authors: Paul Ammann & Jeff Offutt
// Chapter 7; page ??
// Can be run from command line
// See Stutter.num for a numbered version.
// No JUnit tests at this time.

/** *****************************************************
// Stutter checks for repeat words in a text file.
// It prints a list of repeat words, by line number.
// Stutter will accept standard input or a list
// of file names.
 *  Jeff Offutt, June 1989 (in C), Java version March 2003 
********************************************************* */
'''
import sys

class Stutter:
	'''
	// Class variables used in multiple methods.
	'''
	lastdelimit = True
	curWord = ''
	prevWord = ''
	delimits = ['\t', ' ', ',', '.', '!', '-', '+', '=', ';', ':', '?',
		'&', '{', '}', '\\']

	'''
	//************************************************
	// Stut() reads all lines in the input stream, and
	// finds words. Words are defined as being surrounded
	// by delimiters as defined in the delimits[] array.
	// Every time an end of word is found, checkDupes()
	// is called to see if it is the same as the
	// previous word.
	//************************************************
	'''
	@staticmethod
	def stut(inFile):
		linecnt = 1
		while (inLine := inFile.readline()) != '': # For each line
			inLine = inLine.rstrip('\n')
			i = 0
			while i < len(inLine): # for each character
				c = inLine[i]
				if Stutter.isDelimit(c): # Found an end of a word.
					Stutter.checkDupes(linecnt)
				else:
					Stutter.lastdelimit = False
					Stutter.curWord += c
				i += 1
			Stutter.checkDupes(linecnt)
			linecnt += 1

	'''
	//************************************************
	// checkDupes() checks to see if the globally defined
	// curWord is the same as prevWord and prints a message
	// if they are the same.
	//************************************************
	'''
	@staticmethod
	def checkDupes(line):
		if Stutter.lastdelimit:
			return # already checked, keep skipping
		Stutter.lastdelimit = True
		if Stutter.curWord == Stutter.prevWord:
			print('Repeated word on line ', line, ': ', Stutter.prevWord, ' ', Stutter.curWord, sep='')
		else:
			Stutter.prevWord = Stutter.curWord
		Stutter.curWord = ''

	'''
	//************************************************
	// Checks to see if a character is a delimiter.
	//************************************************
	'''
	@staticmethod
	def isDelimit(C):
		i = 0
		while i < len(Stutter.delimits):
			if C == Stutter.delimits[i]:
				return True
			i += 1
		return False

'''
//************************************************
// main parses the arguments, decides if stdin
// or a file name, and calls Stut().
//************************************************
'''
def main():
	if len(sys.argv) == 1: # no file, use stdin
		inFile = sys.stdin
	else:
		fileName = sys.argv[1]
		if fileName == '': # no file name, use stdin
			inFile = sys.stdin
		else: # file name, open the file.
			myFile = open(fileName, 'r')
			inFile = myFile
	Stutter.stut(inFile)

if __name__ == '__main__':
	main()
