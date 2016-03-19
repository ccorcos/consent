# US Government Consent

The data is scraped using [unitedstates/congress](https://github.com/unitedstates/congress).

![](/histogram.png)

# Running Code

## Beginners

If you don't really program or anything, there are some prerequisits you'll need to install. I'm assuming you're using a Mac, or at least you better be! :P

Open up your "Terminal" application. Its in your Utilities folder. Then pase the following command:

    xcode-select --install

This will install the "commandline tools" for your Mac. you'll have to go though some installation instructions. All this stuff comes from Apple. Its basically the tools used to build computers and programs.

Next we're going to install [homebrew](http://brew.sh), a package manager for Mac software and [pip](https://pypi.python.org/pypi/pip) a package manager for python libraries (python is a programming language).

    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    easy_install pip

Thats basically it, now move on to the develop instalation instructions. Note that everything will be run in Terminal. And command that starts with `sudo` will require your password to install.

## Developers

To download the dataset:

    # install some requirements
    brew install wget
    sudo pip install virtualenv
    sudo pip install virtualenvwrapper

    # install pythong dependencies in a virtual environment
    cd congress
    virtualenv congress
    . ./congress/bin/activate
    pip install -r requirements.txt

    # download voting data
    sh ./scripts/votes.sh

To run the example and generate the histogram plot and play around with the data:

    sudo pip install pyramda
    sudo pip install numpy
    sudo pip install matplotlib
    python -i consent.py

# Most Recent Data

Rebase against the latest version of the unitedstates/congress scraper:

    git remote add upstream git@github.com:unitedstates/congress.git
    git rebase remote upstream/master
