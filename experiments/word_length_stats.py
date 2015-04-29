import json
import csv
import re
import json
import numpy as np
import matplotlib.pyplot as plt

#Configuration
INPUT_FILE_NAME = "hiv_tweets.csv"
INPUT_FILE_NAME2 = "top_tweets.txt"


def plot_word_dist(word_dict, title):
	#print_dict(word_dict)
	length_dict = build_length_dict(word_dict)
	plot_hist(title, length_dict)

def process_hiv_set():
	word_dict = dict()
	with open(INPUT_FILE_NAME, "rb") as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			text = row["text"]
			if text == None:
				continue
			words = re.split(r'(;|,|\.|\?|!|\s)\s*', text)
			words = filter(len, words)
			for word in words:
				word = extract_alphabet(word)
				if word == None:
					continue
				if word in word_dict:
					word_dict[word] += 1
				else:
					word_dict[word] = 1
	plot_word_dist(word_dict, "Word number over Different Length(HIV Dataset)")


def process_common_set():
	word_dict = dict()
	with open(INPUT_FILE_NAME2, "rb") as inputfile:
		lines = inputfile.read().split("\n")
		lines = filter(len, lines)
		for line in lines:
			tweet = json.loads(line)
			text = tweet["tweet"]["text"]
			#print text + "\n"
			words = re.split(r'(;|,|\.|\?|!|\s)\s*', text)
			words = filter(len, words)
			for word in words:
				word = extract_alphabet(word)
				if word == None:
					continue
				if word in word_dict:
					word_dict[word] += 1
				else:
					word_dict[word] = 1
	plot_word_dist(word_dict, "Word number over Different Length(Common Dataset)")


def extract_alphabet(word):
	if word[0] == '#':
		word = word[1:]
	if word.find("http") != -1:
		return None
	if word.isalpha() == False:
		return None
	return word


def print_dict(d):
	print "dict: \n"
	for k, v in d.iteritems():
		print str(k) + ": " + str(v) + "\n"


def build_length_dict(word_dict):
	d = dict()
	for word, count in word_dict.iteritems():
		word_len = len(word)
		if word_len in d:
			d[word_len] += 1
		else:
			d[word_len] = 1
	return d

def plot_hist(title, length_dict):
	x = []
	y = []
	for k, v in length_dict.iteritems():
		x.append(k)
		y.append(v)

	data = np.array(y)
	mask = data.nonzero()

	N = len(length_dict)
	ind = np.arange(N)*1.1	# the x locations for the groups
	width = 0.6		# the width of the bars

	#fig = plt.figure()
	fig = plt.figure(num=None, figsize=(12, 6), dpi=80, facecolor='w', edgecolor='k')
	ax2 = fig.add_subplot(111)

	ax2.spines['right'].set_visible(False)
	ax2.spines['top'].set_visible(False)
	ax2.spines['left'].set_visible(False)
	ax2.spines['bottom'].set_visible(False)

	ax2.set_title(title)
	ax2.set_xlabel("Word Length")
	ax2.set_ylabel("Word Number")
	ax2.set_xticks(ind+width)
	ax2.set_xticklabels(x)

	rects = plt.bar(ind[mask], data[mask], width, color = 'r')
	autolabel(ax2, rects)
	ax2.set_xlim([0,N])
	plt.show()

def autolabel(ax, rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')


if __name__ == "__main__":
	#process_hiv_set()
	process_common_set()