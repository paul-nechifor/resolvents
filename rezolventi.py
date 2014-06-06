#!/usr/bin/env python2

import re #regular expressions
from string import join

class Prop: #definire clasa Prop
    def __init__(self, s): #constructor
        norm = True
        for i in xrange(len(s)):
            if s[0]=='!':
                norm = not norm
                s = s[1:] #adica s devine s fara primul caracter
            else: break #iesire fortata din bucla
        self.nume = s #ce litera are
        self.normal = norm #daca este negata sau nu
    def __eq__(self, other): #overload-eaza operatorul '=='
        return (self.nume == other.nume) and (self.normal == other.normal)
    def __neg__(self): #overload-eaza operatorul '-' (Python nu are '!')
        return Prop('!'+self.arata())
    def arata(self):
        if self.normal: return self.nume
        else: return '!'+self.nume
    __repr__ = arata #functia asta este chemata cand este afisat prin print
    
class Clauza: #defineste clasa Clauza
    def __init__(self, s): #constructor
        self.vect = [] #lista vida
        self.index = -1 #pentru iterator
        #pentru fiecare string separat de ',' din s fara primul si ultimul caracter... adauga
        for i in s[1:-1].split(','): self.vect.append(Prop(i.strip()))
    def arata(self):
        if self.vect == []: return "{}"
        r = '{'
        for i in self.vect: r += i.arata() + ", "
        return r[:-2]+'}' #r fara ultimele doua caractere (adica ", ") plus "}"
    def are(self, e): #daca cauza curenta are Prop e
        for i in self.vect:
            if i == e: return True
        return False
    def __iter__(self): #defineste un iterator pentru a fi utilizat cu for
        return Clauza(self.arata())
    def next(self): #intoarce urmatorul Prop din clauza (pentru iterator)
        if self.index == len(self.vect)-1: raise StopIteration
        self.index += 1
        return self.vect[self.index]
    def fara(self, e): #intoarce clauza curenta fara un element
        C = Clauza(self.arata())
        for i in xrange(len(C.vect)):
            if C.vect[i]==e:
                C.vect.pop(i)
                break
        return C
    def __add__(self, other): #overload-eaza operatorul '+'
        C = Clauza(self.arata())
        if C.arata()=='{}': C.vect = []
        for i in xrange(len(other.vect)):
            if not C.are(other.vect[i]): C.vect.append(other.vect[i])
        return C #intoarce multimea formata din reuniunea doua clauze
    def __eq__(self, other): #operatorul '=='
        if len(self.vect)!=len(other.vect): return False
        for i in xrange(len(self.vect)):
            if not (self.are(other.vect[i])): return False
        return True
    __repr__ = arata #ca si la Prop

class Res:
    def __init__(self, s):
        self.form = [] #multimea de clauze
        for i in re.findall('{[^{}]*}', s): #sirurile de caractere care nu contin '{' sau '}'
            self.form.append(Clauza(i))
    def arata(self):
        if self.form == []: return "{}"
        r = '{'
        for i in self.form: r += i.arata() + ", "
        return r[:-2]+'}'
    def rezolventii(self):
        r = Res('')
        for i in xrange(0, len(self.form)-1): #pentru fiecare, fara ultimul
            for j in xrange(i+1, len(self.form)): #cu fiecare dupa el...
                for e in self.form[i]: # pentru fiecare Prop din Clauza i
                    if self.form[j].are(-e): #daca cealalta clauza are negatul Prop-ului...
                        nc = self.form[i].fara(e) + self.form[j].fara(-e)
                        nou = True
                        for k in r.form:
                            if k==nc: nou = False
                        if nou and len(nc.vect)>0: r.form.append(nc) #... si este unic si >0 Prop-uri => adauga
        return r
    def are(self, c): 
        for i in self.form:
            if i == c: return True
        return False
    def __add__(self, other): #overload-eaza operatorul '+'
        R = Res(self.arata())
        R.addd = 0
        if R.arata()=='{}': R.form = []
        for i in xrange(len(other.form)):
            if not R.are(other.form[i]):
                R.addd += 1
                R.form.append(other.form[i])
        return R #intoarce multimea formata din reuniunea doua clauze    
    __repr__ = arata

class Form:
    def __init__(self, s):
        self.s = s
    def res0(self): #converteste formula in prima multime de rezolventi
        #intre list() se afla un generator care separa string-ul s dupa '&' si pentru fiecare i
        #gaseste string-urile care nu contin '()| ' si le uneste separate de ", " si inconjurat de "{" si "}"
        #si pentru fiecare element din generator, le uneste din nou cu vergula si acolade
        return '{'+join(list('{'+join(re.findall('[^()| ]+',i),", ")+'}' for i in self.s.split('&')), ', ')+'}'
    def res(self, n): #arata pana la un anumit numar
        toti = R = Res(self.res0())
        for i in xrange(n):
            toti = toti + R.rezolventii()
            print toti, "\n\n", R, "\n\n",toti.addd,"\n"
            R = R.rezolventii()
    def resn(self): #arata pana nu mai sunt clauze unice
        print "F =", self.s, "\n"
        toti = R = Res(self.res0())
        for i in xrange(50):        #maxim cat am sa incerc
            R = R.rezolventii()
            toti = toti + R
            print "Res",i+1,"= Res", i, "reunit cu",R, "\n"
            if toti.addd==0: break  #termina daca nu mai sunt altele noi
        print "Res * =",toti
        print "----------"*8 #80 de caractere
    def __repr__(self):
        return self.s

def main():
    for linie in open("formule.txt"): #pentru fiecare linie din formule.txt
        f = Form(linie[:-1]) #creaza o formula fara ultimul caracter ('\n') => de asta trebuie ultima linie libera
        f.resn() #cauta rezolventii

if __name__ == '__main__':
    main()
