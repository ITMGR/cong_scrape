"""bills module will call up json files loaded. Optionally allow for search by regex.
"""
import os, re, json, sys, argparse

class Bills(object):
    """Bills class. go Bills! """
    def __init__(self, base_dir):
        self.getfilelist(base_dir)
        self.records = []

    def getfilelist(self, base_dir, **kwargs):
        """ gets the initial file list. recall here to generate new file list
        """
        ext_search = kwargs['ext'] if 'ext' in kwargs else 'json'
        self.files = [os.path.join(paths[0], j) for paths in os.walk(base_dir) \
                    for j in     paths[2] if j.endswith(ext_search)]


    def getrecords(self, fields, **kwargs):
        """ grab specified json keys from the first n files in bills.records """
        if 'n' in kwargs:
            files = self.files[0:kwargs['n']] if kwargs['n'] else self.files
        else:
            files = self.files
        for j in files:
            self.records.append({i:get_json(j)[i] for i in fields})


    def search_records(self, key, loc, regex_str):
        """search with this method"""
        records = self.records
        for record in records:
            search_loc = get_path(record, "%s"% loc)
            record["%s_text"%key] = re.findall(regex_str, search_loc)
            record["%s_len"%key] = len(record["%s_text"%key])


def get_path(dct, path):
    """ paths to nested json more sensibly """
    for list_index, dict_key in re.findall(r'(\d+)|(\w+)', path):
        dct = dct[dict_key or int(list_index)]
    return dct

def get_json(file_name):
    """gets a given json file from path and returns in obj format"""
    with open(file_name, 'rb') as thefile:
        return json.load(thefile)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Process files and\
                                    return search results.')
    PARSER.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    PARSER.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')
    ARGS = PARSER.parse_args()
    print ARGS.accumulate(ARGS.integers)
    if len(sys.argv) < 3:
        X = Bills(".")
        print "both path and regex pattern are needed"
        sys.exit(1)
    elif len(sys.argv) > 2:
        print "Correct Usage: python bill PATH"
        print len(sys.argv)
        print sys.argv
        sys.exit(1)
    X.getrecords(["summary"])
    X.search_records("match", "summary.text",\
                    r"(\w{0,10}end(?:\w+?\s){0,6}fund.+?\s)")
    print [i['match_len'] for i in X.records if i['match_len'] > 0]
