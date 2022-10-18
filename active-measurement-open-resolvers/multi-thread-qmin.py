#!/usr/bin/python3
import argparse
from multiprocessing import Pool
import time
import dns.resolver
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-r", required=True, help="file containing a list of resolver IP-addresses")
parser.add_argument("-w", required=False, type=int, default=10, help="number of workers in the pool")
parser.add_argument("-t", required=False, type=int, default=3, help="resolver timeout")
parser.add_argument("--geo", required=True, help="geographical location of machine")
parser.add_argument("-i", required=True, type=str, help="iteration")
args = vars(parser.parse_args())

num_threads = args['w']
resolver_timeout = args['t']
if not args['geo'] in ['nvirginia', 'tokyo', 'frankfurt']:
    exit('invalid geo')

def index_list(foo):
    return [(i, x) for i,x in enumerate(foo)]

def read_file(fname):
    with open(fname, "r") as fp:
        return fp.read().splitlines()

# https://stackoverflow.com/a/65788144
def resolve(index, resolver_ip):
    target_resolver = dns.resolver.Resolver(configure=False)
    target_resolver.timeout = target_resolver.lifetime = resolver_timeout
    target_resolver.nameservers = [resolver_ip]
    try:
        dname = f"a.{args['geo']}-{args['i'].zfill(2)}.qnamemintest.net"
        # https://stackoverflow.com/a/49509519
        answers = target_resolver.resolve(dname, "TXT")
        return f"{resolver_ip};NOERROR " + ", ".join([answer.to_text() for answer in answers])
    except dns.exception.Timeout:
        return f"{resolver_ip};TIMEOUT"
    except Exception as e:
        for r in ["NOTZONE","SERVFAIL","REFUSED","NOTIMP","NOTAUTH"]:
            if r in e.args[0]:
                return f"{resolver_ip};{r}"
        if "does not contain an answer" in e.args[0]:
                return f"{resolver_ip};NOERROR"
        if "name does not exist" in e.args[0]:
                return f"{resolver_ip};NXDOMAIN"
        return f"{resolver_ip};OTHER {e.args[0]}"

def main():
    resolvers = read_file(args['r'])
    print(f"Querying {len(resolvers)} resolvers using {num_threads} workers")
    p = Pool(num_threads)
    results = p.starmap(resolve, index_list(resolvers))
    print("resolver_ip;response")
    [print(line) for line in sorted(results)]

if __name__ == "__main__":
    main()
