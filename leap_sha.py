# leap-seconds.list SHA-1 checksum calculator

import hashlib

# URLs where we find leap-seconds.list:
# wget "https://hpiers.obspm.fr/iers/bul/bulc/ntp/leap-seconds.list"
# wget "https://data.iana.org/time-zones/code/leap-seconds.list"

def sha1_calc():
    # given a leap-seconds.list file, parse it
    # and return both the old and a newly calculated SHA1
    s = hashlib.new('sha1')
    nlines=0
    old_hash=""
    with open("./leap-seconds.list", 'r', encoding='utf-8') as fid:
        for line in fid:
            nlines+=1
            if line.startswith('#$'): # last update time-stamp
                line = line.replace('\n','')
                line = line.replace('\t',' ')
                line = line.split() # separate #$ and number
                #print (line)
                #print ("update: ",line[1])
                s.update(line[1].encode('utf-8'))
            elif line.startswith('#@'): # expiration time-stamp
                line = line.replace('\n','')
                line=line.replace('\t',' ')
                line = line.split() # separate #$ and number
                #print ("expire: ",line[1])
                s.update(line[1].encode('utf-8'))
            elif line.startswith('#h'): # the SHA-1
                line=line.replace('\n','')
                line=line.replace('\t',' ')
                line=line.split()
                line.pop(0) # remove the "#h"
                old_hash = "".join(line)
                print ("Old hash: ", old_hash)
            elif line.startswith('#'): #comment
                pass
            else: # actual data
                print (line)
                line=line.split()
                s.update(line[0].encode('utf-8'))
                s.update(line[1].encode('utf-8'))
        #print ("read ",nlines," lines")
        return (old_hash, s.hexdigest() )

def sha1_check():
    (old_hash, new_hash) = sha1_calc()

    print ("New Hash: ", new_hash)
    print ("Old Hash: ", old_hash)
    success = old_hash==new_hash
    print ("Identical ? ", success)
    print ("")
    return success

sha1_check()
