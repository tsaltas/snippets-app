import sys
import argparse
import logging
import csv

# Set the log output file, and the log level
logging.basicConfig(filename="output.log", level=logging.DEBUG)

def make_parser():
    """ Construct the command line parser """
    logging.info("Constructing parser")
    description = "Store and retrieve snippets of text"
    parser = argparse.ArgumentParser(description=description)

    subparsers = parser.add_subparsers(help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    put_parser.add_argument("filename", default="snippets.csv", nargs="?",
                            help="The snippet filename")
    put_parser.set_defaults(command="put")

    # Subparser for the get command
    logging.debug("Constructing get subparser")
    put_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("filename", default="snippets.csv", nargs="?",
                            help="The snippet filename")
    put_parser.set_defaults(command="get")
    
    # Subparser for the search command
    logging.debug("Constructing search subparser")
    put_parser = subparsers.add_parser("search", help="Search for a snippet containing a certain string")
    put_parser.add_argument("string", help="String contained in a snippet")
    put_parser.add_argument("filename", default="snippets.csv", nargs="?",
                            help="The snippet filename")
    put_parser.set_defaults(command="search")
    
    return parser

def put(name, snippet, filename):
    """ Store a snippet with an associated name in the CSV file """
    logging.info("Writing {}:{} to {}".format(name, snippet, filename))
    logging.debug("Opening file")
    with open(filename, "a") as f:
        writer = csv.writer(f)
        logging.debug("Writing snippet to file".format(name, snippet))
        writer.writerow([name, snippet])
    logging.debug("Write sucessful")
    return name, snippet
 
def get(name, filename):
    """ Retrieve a snippet with an associated name in the CSV file """
    logging.info("Retrieving snippet called {} from {}".format(name, filename))
    logging.debug("Opening file")
    with open(filename, "r") as f:
        reader = csv.reader(f)
        logging.debug("Reading snippet from file")
        # look for the snippet in the rows of the CSV file
        for row in reader:
            # if the snippet is found
            if row[0] == name:
                snippet = row[1]
                logging.debug("Located snippet")
                # return the name and the snippet
                return name, snippet
        # else, snippet must not exist, so raise an exception 
        raise Exception()

def search(string, filename):
    """ Search for a snippet containing the string in the CSV file """
    logging.info("Searching for snippet containing {} from {}".format(string, filename))
    logging.debug("Opening file")
    # initialize an empty list to contain any matching snippets we find
    snippet_list = []
    with open(filename, "r") as f:
        reader = csv.reader(f)
        logging.debug("Searching for string in file")
        # search for the string within the CSV file snippets
        for row in reader:
            # if the string is found within the snippet itself (not within snippet name)
            if row[1].find(string) >= 0:
                logging.debug("Located string within snippet")
                # put the name and the snippet into the snippet list as a tuple
                snippet_list.append((row[0], row[1]))
    # after looking through all the rows, return the snippet list
    return snippet_list    
  
def main():
    """ Main function """
    logging.info("Starting snippets")
    parser = make_parser()
    arguments = parser.parse_args(sys.argv[1:])

    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
       name, snippet = put(**arguments)
       print "Stored '{}' as '{}'".format(snippet, name)
      
    if command == "get":
        # if get function does not raise an exception, it has found the snippet
        try:
          name, snippet = get(**arguments)
          print "Retrieved '{}' as '{}'".format(snippet, name)
        # if the snippet does not yet exist, an exception will be raised, and we should explain the issue to the user
        except:
          print "Code snippet does not exist."
                                    
    if command == "search":
        snippet_list = search(**arguments)
        # if search command returns nothing, tell the user
        if len(snippet_list) == 0:
            print "No matching code snippets were found."
        else:
            for snippet_tuple in snippet_list:
                print snippet_tuple
          
if __name__ == "__main__":
    main()