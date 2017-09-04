from polynomials import random_polynomial, mod_inverse, Polynomial, modular_lagrange_interpolation, share_Polynomial
from utilitybelt import secure_randint as randint
from conferenceKey import secret_reconstruct
import timeit
import sys


def sqaure_and_multiply(mod, base, index):
    m = bin(index)
    m = m[2:]
    if m[len(m) - 1] == '1':
        B = base
    else:
        B = 1
    A = base
    for i in range(len(m) - 2, -1, -1):
        A = A * A % mod
        if m[i] == '1':
            B = B * A % mod
    return B
#define number of users
print sys.argv
n = int(sys.argv[1])
rn = n/2
# 1024bit modulus
p1 = 11514844562790516655282382339997901326205477956091910904703943499562165719386197597458797308772109262770530717689695340334206066966408416627740404681562663L
q1 = 10423868126996985387214298003163473887816545231233184168499707786423333353741569421872579600137156466386073703548533187413949131260907402186949276882953347L
n1 = 120029221225396603943216312047289862327499010103056102571360609037851894896802135599029426055406735973259252625983764193927877972873712575004271317839369300415405820754446598418407393743146043397841334533819748796599919740150430457027942915144241523764241525063139352964442411349882905130519757202210486083061L
phi_1 = 120029221225396603943216312047289862327499010103056102571360609037851894896802135599029426055406735973259252625983764193927877972873712575004271317839369278476693130966944555921727050581770829375818147208724675592948633754651357329260923583767332614498512368458718114735914663194684677814700942512528921567052L

# 2048bit modulus
p2 = 146577968092877312553398069696998164521291778517747266285620770923741199895672989329883393034806862195786134935131447729635292436654606931321259940448635910284739497814443242901860431973473904516100420002377014760516087876319694046674932514757720182024711379435769206957579891080424488883021398865152668185847L
q2 = 161185860087032198171591177899415457502154280429768268816998037977934434736927998922989563504350082388505854576461166890757554351306828172915196408722596424537550936512619197351577432179777058245856717154742653464973379928171789861715315739636999452888860044631026786739283446194194236313836676520593401112159L
n2 = 23626295856859992265056730641465568551098718630084909446692697033225009031418301544480771860359655448664564181287192033292039242567946888484015603287220606316235151997738808126001142006753732243117524136214693962867755236545218137604793811858657384961745470253756673427655525701533591709750228473515744735089371318394149314335225824881013690795368106910575340795775903156498142994768069714898602269014705183848012394862675132316756664263850553979274626204746281189677294090916601447299267285290025687498569239951469483691647850557764983064367446907502177190801149385157844508468862171881233487337714983247906703413673L
phi_2 = 23626295856859992265056730641465568551098718630084909446692697033225009031418301544480771860359655448664564181287192033292039242567946888484015603287220606316235151997738808126001142006753732243117524136214693962867755236545218137604793811858657384961745470253756673427655525701533591709750228473515744735089063554565969404824500835633417277173344660851627825260673284347596467360135468726645729312475548239263720405351082517696363817475889118875038169855575048854855003656589539007045829421136774724736612102794349815466158382753273499155977198653107457555887577961091048514771998834606614762140856907862160634115668L

# degree of polynomial f11 is 10, and modulus is 1024 bits
f11 =  random_polynomial(10, randint(0, n1-1), n1)
P11 = Polynomial(f11, n1, n)
# degree of polynomial f12 is 10, and modulus is 2048 bits
f12 =  random_polynomial(10, randint(0, n2-1), n2)
P12 = Polynomial(f12, n2, n)

# degree of polynomial f11 is 20, and modulus is 1024 bits
f21 =  random_polynomial(20, randint(0, n1-1), n1)
P21 = Polynomial(f21, n1, n)

# degree of polynomial f12 is 20, and modulus is 2048 bits
f22 =  random_polynomial(20, randint(0, n2-1), n2)
P22 = Polynomial(f22, n2, n)

pub_inf = range(1,n+1)
f = open('results.txt','a')


#time for calculation of s_i(x)=f(i)^{1/(n-1)}f(x) with i = n/2, RSA modulus 1024 bits
start = timeit.default_timer()
inverseOfnminus1 = mod_inverse(n-1, phi_1)
stop = timeit.default_timer()
t_inverse_1 = stop-start
start = timeit.default_timer()
c11 = sqaure_and_multiply(n1,P11.value(pub_inf[n/2]), inverseOfnminus1)
s11_ = [(c11*i % n1)for i in f11]

stop = timeit.default_timer()
print "n=%d"%n,
print "time for calculation of s_i(x)=f(i)^{1/(n-1)}f(x) with i = n/2, RSA modulus 1024 bits degree k = 10 is "
print stop-start+t_inverse_1, " seconds"
f.write(str(stop-start+t_inverse_1))
f.write('\n')
s11=share_Polynomial(P11.get_mul_value(c11),n1,n, n/2)

#time for evaluation of s_i(x)=f(i)^{1/(n-1)}f(x) with x = n/2+1 and i = n/2
start = timeit.default_timer()
s11.value(n/2+1)
stop = timeit.default_timer()
print "n=%d"%n,
print "time for evaluation of s_i(x)=f(i)^{1/(n-1)}f(x) with i = n/2, x = n/2+1, RSA modulus 1024 bits degree k = 10 is "
print stop-start, " seconds"
f.write(str(stop-start))
f.write('\n')

#time for rn user reconstruct share secret using lagrange interpolation
S=[]
for i in range(rn+1):
    c = sqaure_and_multiply(n1,P11.value(pub_inf[i]), inverseOfnminus1)
    S.append(share_Polynomial(P11.get_mul_value(c), n1, n, i))
v = []
for s in S:
    v.append(s.secret_value())
r = range(rn+1)
start = timeit.default_timer()
secret_reconstruct(r, v, n, 10, n1)
stop = timeit.default_timer()
print "n=%d"%n,
print "time for k+1 user reconstruct share secret using lagrange interpolation RSA modulus 1024 bits degree k = 10 is "
print stop-start, " second"
f.write(str(stop-start))
f.write('\n')

#time for calculation of s_i(x)=f(i)^{1/(n-1)}f(x) with i = n/2, RSA modulus 2048 bits
start = timeit.default_timer()
inverseOfnminus1 = mod_inverse(n-1, phi_2)
stop = timeit.default_timer()
t_inverse_2 = stop-start

start = timeit.default_timer()
c12 = sqaure_and_multiply(n2,P12.value(pub_inf[n/2]), inverseOfnminus1)
s12_ = [(c12*i % n2)for i in f12]

stop = timeit.default_timer()
print "n=%d"%n,
print "time for calculation of s_i(x)=f(i)^{1/(n-1)}f(x) with i = n/2, RSA modulus 2048 bits degree k = 10 is "
print stop-start+t_inverse_2, " seconds"
f.write(str(stop-start+t_inverse_2))
f.write('\n')

s12=share_Polynomial(P12.get_mul_value(c12),n2,n, n/2)

#time for evaluation of s_i(x)=f(i)^{1/(n-1)}f(x) with x = n/2+1 and i = n/2
start = timeit.default_timer()
s12.value(n/2+1)
stop = timeit.default_timer()
print "n=%d"%n,
print "time for evaluation of s_i(x)=f(i)^{1/(n-1)}f(x) with i = n/2, x = n/2+1, RSA modulus 2048 bits degree k = 10 is "
print stop-start, " seconds"
f.write(str(stop-start))
f.write('\n')
#time for k+1 user reconstruct share secret using lagrange interpolation
S=[]
for i in range(rn+1):
    c = sqaure_and_multiply(n2,P12.value(pub_inf[i]), inverseOfnminus1)
    S.append(share_Polynomial(P12.get_mul_value(c), n2, n, i))
v = []
for s in S:
    v.append(s.secret_value())
r = range(rn+1)
start = timeit.default_timer()
secret_reconstruct(r, v, n, 10, n2)
stop = timeit.default_timer()
print "n=%d"%n,
print "time for k+1 user reconstruct share secret using lagrange interpolation RSA modulus 2048 bits degree k = 10 is "
print stop-start, " second"
f.write(str(stop-start))
f.write('\n')

#time for calculation of s_i(x)=f(i)^{1/(n-1)}f(x) with i = n/2, RSA modulus 1024 bits

inverseOfnminus1 = mod_inverse(n-1, phi_1)
start = timeit.default_timer()
c21 = sqaure_and_multiply(n1,P21.value(pub_inf[n/2]), inverseOfnminus1)
s21_ = [(c21*i % n1)for i in f21]

stop = timeit.default_timer()
print "n=%d"%n,
print "time for calculation of s_i(x)=f(i)^{1/(n-1)}f(x) with i = n/2, RSA modulus 1024 bits degree k = 20 is "
print stop-start+t_inverse_1, " seconds"
f.write(str(stop-start+t_inverse_1))
f.write('\n')

s21=share_Polynomial(P21.get_mul_value(c11),n1,n, n/2)

#time for evaluation of s_i(x)=f(i)^{1/(n-1)}f(x) with x = n/2+1 and i = n/2
start = timeit.default_timer()
s21.value(n/2+1)
stop = timeit.default_timer()
print "n=%d"%n,
print "time for evaluation of s_i(x)=f(i)^{1/(n-1)}f(x) with i = n/2, x = n/2+1, RSA modulus 1024 bits degree k = 20 is "
print stop-start, " seconds"
f.write(str(stop-start))
f.write('\n')
#time for k+1 user reconstruct share secret using lagrange interpolation
S=[]
for i in range(rn+1):
    c = sqaure_and_multiply(n1,P21.value(pub_inf[i]), inverseOfnminus1)
    S.append(share_Polynomial(P21.get_mul_value(c), n1, n, i))
v = []
for s in S:
    v.append(s.secret_value())
r = range(rn+1)
start = timeit.default_timer()
secret_reconstruct(r, v, n, 20, n1)
stop = timeit.default_timer()
print "n=%d"%n,
print "time for k+1 user reconstruct share secret using lagrange interpolation with RSA modulus 1024 bits degree k = 20 is "
print stop-start, " second"
f.write(str(stop-start))
f.write('\n')
#time for calculation of s_i(x)=f(i)^{1/(n-1)}f(x) with i = n/2, RSA modulus 2048 bits

inverseOfnminus1 = mod_inverse(n-1, phi_2)
start = timeit.default_timer()
c22 = sqaure_and_multiply(n2,P22.value(pub_inf[n/2]), inverseOfnminus1)
s22_ = [(c22*i % n2)for i in f22]

stop = timeit.default_timer()
print "n=%d"%n,
print "time for calculation of s_i(x)=f(i)^{1/(n-1)}f(x) with i = n/2, RSA modulus 2048 bits degree k = 20 is "
print stop-start+t_inverse_2, " seconds"
f.write(str(stop-start+t_inverse_2))
f.write('\n')
s22=share_Polynomial(P22.get_mul_value(c22),n2,n, n/2)

#time for evaluation of s_i(x)=f(i)^{1/(n-1)}f(x) with x = n/2+1 and i = n/2
start = timeit.default_timer()
s22.value(n/2+1)
stop = timeit.default_timer()
print "n=%d"%n,
print "time for evaluation of s_i(x)=f(i)^{1/(n-1)}f(x) with i = n/2, x = n/2+1, RSA modulus 2048 bits degree k = 20 is "
print stop-start, " seconds"
f.write(str(stop-start))
f.write('\n')
#time for k+1 user reconstruct share secret using lagrange interpolation
S=[]
for i in range(rn+1):
    c = sqaure_and_multiply(n2,P12.value(pub_inf[i]), inverseOfnminus1)
    S.append(share_Polynomial(P12.get_mul_value(c), n2, n, i))
v = []
for s in S:
    v.append(s.secret_value())
r = range(rn+1)
start = timeit.default_timer()
secret_reconstruct(r, v, n, 20, n2)
stop = timeit.default_timer()
print "n=%d"%n,
print "time for k+1 user reconstruct share secret using lagrange interpolation RSA modulus 2048 bits degree k = 20 is "
print stop-start, " second"
f.write(str(stop-start))
f.write('\n')