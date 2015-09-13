import sys

def return_one(p,a,e,i):
    s = '{\n"iIndex": '+str(i)+',\n"sQuestion": "'+p.strip()+'",\n"lEquations": [\n"'+e.strip()+'"\n],\n"lSolutions": [ \n'+a.strip()+'\n ]\n}'
    return s

def floatcheck(x):
    try:
        x = ''.join([y for y in x if y != ','])
        if "/" in x:
            x = x.replace(" ","+")
            return(float(eval(x)))
        return float(x)
    except:
        return False

def proc_frac(x):
    if "/" in x:
        spl = x.split(" ")
        newspl = []
        i=0
        while i < len(spl):
            if spl[i].isdigit() and "/" in spl[i+1]:
                newspl.append(str(float(spl[i])+float(eval(spl[i+1]))))
                i+=2
            else:
                newspl.append(spl[i])
                i+=1
        return " ".join(newspl)
    else: return x



def parse_inp(inp):
    q=[]
    a=[]
    e=[]
    with open(inp) as f:
        f = f.readlines()
        i=0
        while i<len(f):
            q.append(f[i])
            i+=1
            e.append(proc_frac(f[i]))
            i+=1
            a.append(f[i])
            i+=1
    return (q,a,e)



if __name__=='__main__':
    q,aas,ees = parse_inp(sys.argv[1])

    for j,p in enumerate(q):
        a = aas[j].strip()
        if "/" in a:
            a = str(float(floatcheck(a)))
        else:
            a = str(float(a))
        e = proc_frac(ees[j])
        p = proc_frac(p); #' '.join([str(proc_frac(x)) for x in p.split(" ")])
        print(p,e,a)
