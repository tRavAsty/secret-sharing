import timeit
import conferenceKey

with open('test_time') as f:
    #w, h = [int(x) for x in next(f).split()]  # read first line
    array = []
    for line in f:  # read rest of lines
        array.append([int(x) for x in line.split()])
for i in array:
    start = timeit.default_timer()
    A, shareholders = conferenceKey.share_generation(i[0],i[1],i[2],i[3])
    stop = timeit.default_timer()
    print "share_generation",
    print i[0],i[1],i[2],i[3],
    print stop-start,
    print "seconds"

    start = timeit.default_timer()
    shareholders[0].conference_key_construct(range(i[1]))
    stop = timeit.default_timer()
    print "conference_key_construct",
    print i[0], i[1], i[2], i[3],
    print stop - start,
    print "seconds"


    v = []
    for s in shareholders:
        v.append(s.secret_value())
    mod = shareholders[0].get_modulus()
    start = timeit.default_timer()
    conferenceKey.secret_reconstruct(range(i[1]),v,i[1],i[0],mod)
    stop = timeit.default_timer()
    print "secret_reconstruct",
    print i[0], i[1], i[2], i[3],
    print stop - start,
    print "seconds"