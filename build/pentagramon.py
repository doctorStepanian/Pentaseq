# -*- coding: cp1251 -*-
from __future__ import division

def pythagor(k,N_stup,mod, base_frq):
    '''алгоритм Пифагора для (золотого) коэффициента k, количества ступеней N_stup растянутого на mod мультиоктав'''
    intervals=[]  # шаг 1 синтез прогрессии
    for i in range(-1,N_stup-1):
        intervals.append(k**i)
    intervals.sort() # упорядочивание
    
    Z=[] # шаг 2 приведение в интервал октавы от 1 до 2
    for i in intervals:
        if i<1:
            z=i*2
            while z <1:
                z=z*2
            Z.append(z)
        elif i>2:
            z=i/2
            while z >2:
                z=z/2
                #print i,z
            Z.append(z)    
        else:
            Z.append(i)

    # mult=[]
    # a=(mod/2)**(1/N_stup)
    # for i in range(len(Z)): mult.append(Z[i]*(a**i)) 
    # шаг дополнительный растяжка на мультиоктау mod
    
    Z.sort() 
    
    mult = [i**mod for i in Z]  # старый (не верный) шаг дополнительный растяжка на мультиоктау mod
    # print mod, Z, '==', mult
    gamma = [base_frq*i for i in mult] # получение частот путем умножения коэффициентов на базовую частоту
    return gamma

def make_dict_old(list):
    '''делаем словарь из списка'''
    voc={}
    for i in range(len(list)):
        voc[str(i)]=list[i]
    return voc

def make_dict(lowers,uppers):
    '''делаем словарь из списка'''
    voc={}
    r1=range(len(uppers)); #print r1
    for i in r1: 
        voc[str(i)]=uppers[i]
    r2=[0-i for i in range(1,len(lowers))];# print r2
    k=0
    for i in r2:
        #print i,k
        voc[str(i)]=lowers[k] 
        k+=1
        #############################################
    return voc

def octaves(gamma, numoctaves, mod):
    '''увеличение количества октав в строе gamma на numoctaves
    вверх и вниз от базовой частоты
    '''
    def udvoenie_up(gamma,n_oct):#'óäâîåíèå ââåðõ'
        return [note*(2**n_oct) for note in gamma]
    def udvoenie_down(gamma,n_oct):#'óäâîåíèå âíèç'
        return [note/(2**n_oct) for note in gamma]
    
    uppers=[]
    lowers=[]
    for n_oct in range(numoctaves-1):
        uppers += udvoenie_up  (gamma,n_oct)
    #uppers.sort() # óïîðÿäî÷èâàíèå ìóëüòèîêòàâû ââåðõ
    for n_oct in range(1,numoctaves):
        a=udvoenie_down(gamma,n_oct)
        a.reverse()
        lowers+=a
        #print lowers
    #lowers.sort()
    
    #print lowers+uppers
    return lowers,uppers

#gamma=octaves(gamma5,2) # ñòîðîé, êîë-âî îêòàâ #print gamma5

def printer(tones):
    '''распечатать частоты для проверки '''
    k=[]
    for i in tones.keys():
        k.append(i)
    k.sort();#print k
    
    for i in k:
        #print i
        v=tones[i]
        l=[]
        a=[int(i) for i in v.keys()]
        a.sort()
        for i in a:
            print i,'::',v[str(i)]
        #print
           
def generate(stroi,multiocts,num_octaves,k,base_frq):     
    'генерация всех строев c коэффициентом k = golden_worf'
    tones={}
    for m in multiocts: # растяжка на мультиоктавы
        for stroy in stroi:
            gamma=pythagor(k,stroy,m, base_frq)
            lowers,uppers = octaves(gamma, num_octaves, m)
            tones[str(stroy)+'mod'+str(m)]=make_dict(lowers,uppers)
            #octaves(gamma,num_octaves,m)
    #print tones['3mod1']
    return tones


if __name__ == '__main__':
     ### задаются коээфициенты для алгоритма Пифагора --- генерация всех строев c коэффициентом k = golden_worf'
    kvinta = 3./2.
    golden_ratio=      (1+5**0.5)/2 # золотое сечение -- Сошинкий говорит что в этом случае все строи будут без третьих интервалов
    golden_worf = 0.5*((1+5**0.5)/2)**2 # золотой вурф  #golden_worf  =   ((1+5**0.5)/2)**2 # золотой вурф  - тоже самое для алгоритма
    #math.pi    
    #math.e
    #math.g // gravitational const
	
    k=golden_worf  # коэффициент задается здеь !!!!!!!!!!!!!!!!!!

    base_frq = 440 # базовая частота Ля 440/4
    #base_frq=260.7 # коассическая До
    #base_frq=293.7  # коассическая Ре для гитары
    #base_frq=528 # Олег Ткач просит эту частоту для звониицы и сочетания с сольфеджио частот
    #base_frq=432  # Ля метафизическая 
    #base_frq=256.8 # Äî ïðè Ëÿ = 440   # # шаг 3 получение частот но До плавает от строя к строю !
    num_octaves=2
    stroi=[1,2,3,5,8,13,21,34,55,89,144] # фиббоначиевые строи #stroi=[5]
    multiocts=range(10) # multiocts=[3/2] # мультиоктавы

    tones = generate(stroi,multiocts,num_octaves,k,base_frq)


    # пишем на диск ###
    import json
    with open('pentagramon.json', 'w') as outfile:
	    a= tones['13mod1'].values(); a.sort();print a #printer(tones)    
	    out=''
	    for i in a: out+=str(i)+'\n'
	    with open('13.txt', 'wa') as the_file: the_file.write(out)
	    a={'13mod1':a}
	    json.dump(a, outfile)

	    a= tones['8mod1'].values(); a.sort();print a #printer(tones)    
	    out=''
	    for i in a: out+=str(i)+'\n'
	    with open('8.txt', 'wa') as the_file: the_file.write(out)
	    a={'8mod1':a}
	    json.dump(a, outfile)

	    a= tones['5mod1'].values(); a.sort();print a #printer(tones)    
	    out=''
	    for i in a: out+=str(i)+'\n'
	    with open('5.txt', 'wa') as the_file: the_file.write(out)
	    a={'5mod1':a}
	    json.dump(a, outfile)

	    a= tones['3mod1'].values(); a.sort();print a #printer(tones)    
	    out=''
	    for i in a: out+=str(i)+'\n'
	    with open('3.txt', 'wa') as the_file: the_file.write(out)
	    a={'3mod1':a}
	    json.dump(a, outfile)

	    a= tones['2mod1'].values(); a.sort();print a #printer(tones)    
	    out=''
	    for i in a: out+=str(i)+'\n'
	    with open('2.txt', 'wa') as the_file: the_file.write(out)
	    a={'2mod1':a}
	    json.dump(a, outfile)

	    a= tones['1mod1'].values(); a.sort();print a #printer(tones)    
	    out=''
	    for i in a: out+=str(i)+'\n'
	    with open('1.txt', 'wa') as the_file: the_file.write(out)
	    a={'1mod1':a}
	    json.dump(a, outfile)


