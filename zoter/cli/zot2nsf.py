"""
CLI to generate NSF COAs from Zotero.
"""

import csv
import datetime
import glob
import json
import logging
import re
import unicodedata
from pathlib import Path

from zoter import Zoter

NEW_VER = datetime.datetime.today().strftime("%Y%m%d")

logger = logging.getLogger(__name__)

CACHE_FILE = "zotero.json"


def clean_name(name):
    """
    Replaces Unicode with standard ascii replacements and some text cleaning.
    """
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')
    name = name.strip()
    name = re.sub(r"\.", "", name)
    name = re.sub(r"'", "", name)
    name = re.sub(r"\s+", " ", name)
    return name


def load_old(fn):
    """
    Load institution information from old CSV file.

    :param fn: Filename
    :return: {name: institution}
    """
    data = {}
    with open(fn, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            data[clean_name(row[0])] = row[1]
    return data


def get_publications_data():
    """
    Get publication data, from Zotero API if needed, but load from cache file otherwise.

    :return: List of publications.
    """
    cfile = Path(CACHE_FILE)
    if cfile.exists():
        """
        If cache file is less than a day old, then load from cache.
        """
        mtime = datetime.datetime.fromtimestamp(cfile.stat().st_mtime)
        td = datetime.datetime.today() - mtime
        if td.days < 1:
            with open(CACHE_FILE, "rt") as f:
                items = json.load(f)
            return items

    print("Loading publications via Zotero API. This may take a few mins...")
    zoter = Zoter()
    items = zoter.get_my_publications()
    with open(CACHE_FILE, "wt") as f:
        """
        Since the API call is reasonably slow, load the data from cache.
        """
        json.dump(items, f)
    return items


def generate_collaborator_list(args):
    """
    Generate collaborator list.

    :param args:
    """
    start_year = args.year
    items = get_publications_data()
    logger.info("%d items loaded!" % len(items))
    authors = set()
    for d in items:
        data = d["data"]

        if data["itemType"] == "journalArticle":
            m = re.search(r"(\d\d\d\d)", data["date"])
            if m:
                year = int(m.group(1))
            else:
                year = datetime.datetime.today().year
            if year >= start_year:
                for a in data["creators"]:
                    last_name = clean_name(a["lastName"])
                    first_name = clean_name(a["firstName"])
                    authors.add((last_name, first_name))

    authors = sorted(authors)

    logger.info("Loading old collaborators from %s" % args.input_csv)
    names = load_old(args.input_csv)
    new_fname = 'collabs_%s.csv' % NEW_VER
    with open(new_fname, 'w', newline='') as f:
        writer = csv.writer(f)
        for a in authors:
            last_name = clean_name(a[0])
            first_name = clean_name(a[1])
            full_name = "%s, %s" % (last_name, first_name)
            writer.writerow((full_name, names.get(full_name, '')))

    print("%d collabators written to %s with start year = %d." %
          (len(authors), new_fname, start_year))


def main():
    """
    Main method.
    """
    import argparse

    desc = """
This script helps automate the generation and updating of collaborator lists from
zotero directly. Note that the first time this script is used, the csv
generated do not contain affiliations. These have to be entered by hand. 
Subsequently, supply old processed csv using -i and affiliations will be obtained
from the old list where possible. After you generate the csv, you can convert it to 
a string for pasting into the biosketch using make_str.
    """

    p = argparse.ArgumentParser(
        description=desc,
        epilog="Author: Shyue Ping Ong")

    p.add_argument("-y", "--year", dest="year",
                   type=int, default=datetime.datetime.now().year - 4,
                   help="Year from which to update. Defaults to current year - 4, "
                        "based on the usual NSF guideline of past 48 months.")

    p.add_argument("-i", "--input_csv", dest="input_csv",
                   type=str, default=list(glob.glob("collabs_*.csv"))[-1],
                   help="An input CSV file. This is used mainly for prior information on institutions.")

    logging.basicConfig(level=logging.INFO)
    args = p.parse_args()
    generate_collaborator_list(args)
