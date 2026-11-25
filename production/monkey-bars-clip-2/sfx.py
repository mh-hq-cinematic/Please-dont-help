import numpy as np, wave
SR=48000; END=80; buf=np.zeros(int(SR*END)); rng=np.random.default_rng(7)
def add(t,x,g=1.0):
    i=int(t*SR); n=min(len(x),len(buf)-i); buf[i:i+n]+=x[:n]*g
def env(n,a=0.003,d=0.1):
    t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/d)
def tock(f=900,d=0.05):
    n=int(.15*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*f*t)*env(n,0.001,d)
def step():
    n=int(.12*SR); return np.convolve(rng.normal(0,1,n),np.ones(40)/40,'same')*env(n,0.002,0.03)*3
def bell(f,d=1.2):
    n=int(d*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*f*t)+0.35*np.sin(2*np.pi*f*2.76*t)+0.15*np.sin(2*np.pi*f*5.4*t))*env(n,0.002,d/4)
def whoosh(d=0.6):
    n=int(d*SR); x=np.convolve(rng.normal(0,1,n),np.ones(30)/30,'same'); return x*np.sin(np.pi*np.arange(n)/n)*1.5
def clank(): 
    n=int(.25*SR); t=np.arange(n)/SR; return (np.sin(2*np.pi*1350*t)+0.6*np.sin(2*np.pi*2210*t))*env(n,0.001,0.05)
def thump():
    n=int(.3*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*(90*np.exp(-t*8)+40)*t)*env(n,0.002,0.08)*1.2
def pop():
    n=int(.12*SR); t=np.arange(n)/SR; f=500+3000*t/0.12; return np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,0.002,0.04)
def pluck(f,d=0.35,bright=1.0):
    n=int(d*SR); t=np.arange(n)/SR
    return sum(np.sin(2*np.pi*f*k*t)/k**(1.6/bright) for k in range(1,7))*env(n,0.003,d/3.5)
def sting():
    out=np.zeros(int(1.0*SR))
    for f,dt in [(82.4,0),(98,0.12),(110,0.24),(73.4,0.42)]:
        x=pluck(f,0.45,1.8); j=int(dt*SR); out[j:j+len(x)]+=x
    return out*0.7
def fizz(d):
    n=int(d*SR); x=np.convolve(rng.normal(0,1,n),[1,-1],'same'); return x*0.15*(0.6+0.4*np.sin(np.arange(n)/SR*9))
def fanfare(t0):
    for f,dt,d in [(523.25,0,.18),(659.25,.18,.18),(783.99,.36,.18),(1046.5,.54,.8)]:
        n=int((d+.3)*SR); tt=np.arange(n)/SR
        s=sum(np.sin(2*np.pi*f*k*tt+0.3*k)/k for k in range(1,6))*np.minimum(1,tt/0.02)*np.exp(-tt/(d+0.15))
        add(t0+dt,s,0.18)
# crutch walk 3.2-8.0
t=3.4;k=0
while t<8.0:
    add(t,tock(1000+rng.uniform(-60,60)) if k%2==0 else step(),0.35 if k%2==0 else 0.25); t+=0.45;k+=1
add(8.6,clank(),0.3); add(8.75,clank(),0.2)     # crutches against the post
add(18.4,whoosh(0.6),0.4); add(19.0,clank(),0.35)
HOPS=[19.0,21.6,32.8,34.4,43.2,55.6]
scale=[784,880,988,1175,1319,1568]
for i,t0 in enumerate(HOPS):
    if i: add(t0-0.6,whoosh(0.5),0.3); add(t0,clank(),0.3)
    add(t0+0.35,bell(scale[i]),0.22)            # a chime for each counted rung, climbing higher
add(34.75,sting(),0.5)                           # FOUR?!
add(18.1,pop(),0.3); add(42.2,pop(),0.3)         # mouse cards
add(48.0,fizz(7.0),0.25)                         # hands on fire
add(57.4,whoosh(0.5),0.35); add(57.95,thump(),0.6)
add(59.6,pop(),0.4); add(59.65,bell(2093,0.8),0.15)   # gold star
add(74.2,tock(2400,0.015),0.15)                  # porch light click
fanfare(76.6)
# music-box bed (original), ducks under dialogue
bed=np.zeros_like(buf); prog=[(262,330,392),(220,262,330),(175,220,262),(196,247,294)]
t=3.0;i=0
while t<75.2:
    ch=prog[(i//8)%4]; f=ch[[0,1,2,1][i%4]]*2
    x=bell(f,0.9)*0.5; j=int(t*SR); n=min(len(x),len(bed)-j); bed[j:j+n]+=x[:n]
    if i%4==0:
        x=pluck(ch[0]/2,0.9,0.7); n=min(len(x),len(bed)-j); bed[j:j+n]+=x[:n]*0.7
    t+=0.5;i+=1
lines=[(8.8,9.1),(23.8,8.4),(37.2,4.9),(45.8,9.3),(60.0,7.7),(71.2,2.6)]
g=np.ones(len(buf))*0.07
for s,d in lines: g[int((s-0.3)*SR):int((s+d+0.3)*SR)]=0.03
g=np.convolve(g,np.ones(4800)/4800,'same')
fo=np.ones(len(buf)); a=int(74.5*SR); b=int(75.5*SR); fo[a:b]=np.linspace(1,0,b-a); fo[b:]=0
buf+=bed*g*fo
buf=buf/np.max(np.abs(buf))*0.8
with wave.open('sfx.wav','wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf*32767).astype(np.int16).tobytes())
print('ok')
