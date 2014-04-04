import sys
import sdictviewer.formats.dct.sdict as sdict
import sdictviewer.dictutil

dictionary = sdict.SDictionary( 'webster_1913.dct' )
dictionary.load()

start_word = sys.argv[1]

found = False

for item in dictionary.get_word_list_iter( start_word ):
    try:
        if start_word == str( item ):
            instance, definition = item.read_articles()[0]
            print "%s: %s" % ( item, definition )
            found = True
            break
    except:
        continue

if not found:
    print "No definition for '%s'." % start_word

dictionary.close()
