# data comes from here: https://github.com/unitedstates/congress
# info about voting format here: https://github.com/unitedstates/congress/wiki/votes
# file format: congress/data/[congress]/votes/[session]/[chamber][number]/data.json

import os
import json
import pyramda as R
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import Counter

#######################################
## some utility functions
#######################################
def pipe(*fns):
    def _pipe(arg):
        return R.reduce(lambda x,f: f(x), arg, fns)
    return _pipe

def toInt(x):
    try:
        return int(x)
    except:
        return False

R.prop = R.getitem
R.T = lambda x: True
R.pipe = pipe
R.isInt = lambda x: isinstance(toInt(x), int)
R.toInt = toInt
R.propEq = R.curry(lambda k,v,d: d.get(k) == v)
R.flatten = lambda c: [a for b in c for a in b]
R.unique = lambda x: list(set(x))
R.any_of = R.curry(lambda l, x: x in l)
R.freq = lambda x: dict(Counter(x).items())
R.mean = lambda x: R.sum(x) / len(x)

#######################################
## helper functions for reading files
#######################################

# a function to find the data.json files we want
not_hidden = lambda x: not (x[0] == '.' or x == 'fdsys')
def find_data(filter_congress=R.T, filter_session=R.T, filter_chamber=R.T, filter_number=R.T):
    files = []
    all_cong = filter(not_hidden, os.listdir('./congress/data'))
    which_cong = filter(filter_congress, map(int, all_cong))
    for cong in which_cong:
        all_sess = filter(not_hidden, os.listdir('./congress/data/{cong}/votes/'.format(cong=cong)))
        which_sess = filter(filter_session, all_sess)
        for sess in which_sess:
            all_items = filter(not_hidden, os.listdir('./congress/data/{cong}/votes/{sess}/'.format(cong=cong, sess=sess)))
            which_items = filter(lambda x: filter_chamber(x[0]) and filter_number(x[0:]), all_items)
            for item in which_items:
                files.append('./congress/data/{cong}/votes/{sess}/{item}/data.json'.format(cong=cong, sess=sess, item=item))
    return files

# read a json file at some path
def read_file(path):
    with open(path, 'r')as f:
        return json.loads(f.read())


def hist_list(categories):
    hist_obj(Counter(categories))


#######################################
## helper functions making charts
#######################################
def hist_obj(categories):
    labels, values = zip(*categories.items())
    indexes = np.arange(len(labels))
    width = 1

    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, labels)
    plt.show()

def hist(numbers, title="", bins=10):
    bins = np.linspace(0.0, 1.0, bins)
    plt.hist(numbers, bins)
    plt.title(title)
    plt.show()

#######################################
## helper functions for filtering voting data
#######################################

yeses = lambda x: (x.get('Aye') or []) + (x.get('Yea') or [])
nos = lambda x: (x.get('No') or []) + (x.get('Nay') or [])
abstains = lambda x: x.get('Not Voting') or []
presents = lambda x: x.get('Present') or []

normalize_votes = lambda x: {
    'yes': yeses(x),
    'no': nos(x),
    'present': presents(x),
    'abstain': abstains(x)
}

passed = R.any_of([
    u'Agreed to',
    u'Passed',
    u'Amendment Agreed to',
])

failed = R.any_of([
    u'Amendment Rejected',
    u'Failed',
])

amendment_passed = R.pipe(
    R.prop('result'),
    passed
)

amendment_failed = R.pipe(
    R.prop('result'),
    failed
)

yes_ratio = R.pipe(
    R.prop('votes'),
    normalize_votes,
    R.map_dict(len),
    R.freq,
    lambda x: x['yes'] / float(x['yes'] + x['no'])
)

no_ratio = R.pipe(
    R.prop('votes'),
    normalize_votes,
    R.map_dict(len),
    R.freq,
    lambda x: x['no'] / float(x['yes'] + x['no'])
)

#######################################
## loading the voting data in memory
#######################################
# this takes up about 3.5Gb of RAM plus another 5.5Gb in some kernel task

print "loading data into memory..."
latest_congress = 114
last_n_congresses = 10
files = find_data(filter_congress=lambda x: x > latest_congress - last_n_congresses)
data = map(read_file, files)
print "...done"

#######################################
## analysis
#######################################

# print one vote
# print data[0]

# list the category types
# R.pipe(
#     R.map(R.prop('category')),
#     hist_list
# )(data)

# filter data for only the amendments
amendments = R.filter(R.propEq('category', 'amendment'), data)

# all the passing amendments and the ratio of yes votes
passing = R.pipe(
    R.filter(amendment_passed),
    R.map(yes_ratio)
)(amendments)

# all the failing amendments and the ratio of yes votes
failing = R.pipe(
    R.filter(amendment_failed),
    R.map(yes_ratio)
)(amendments)

# the percent of nonconsenting voters
dissatisfied_passing = R.map(lambda x: 1 - x, passing)
dissatisfied = R.mean(dissatisfied_passing + failing)

# plot a histogram
bins = 200
bins = np.linspace(0.0, 1.0, bins)

# passing ratio
plt.hist(passing, bins, color="green", label="passed")
plt.hist(failing, bins, color="red", label="failed")
plt.title("Passing Ratio for Ammendments in the House of Representatives\n %0.02f dissatisfaction" % (dissatisfied*100))
plt.show()