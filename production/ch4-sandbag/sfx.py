import numpy as np, wave
SR=48000; END=101; buf=np.zeros(int(SR*END))
rng=np.random.default_rng(7)
def add(t,x,g=1.0):
    i=int(t*SR); n=min(len(x),len(buf)-i); buf[i:i+n]+=x[:n]*g
def env(n,a=0.003,d=0.1):
    t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/d)
def tock(f=900,d=0.05):
    n=int(.15*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*f*t)*env(n,0.001,d)
def step():
    n=int(.12*SR); return np.convolve(rng.normal(0,1,n),np.ones(40)/40,'same')*env(n,0.002,0.03)*3
def squelch(d=0.6):
    n=int(d*SR); t=np.arange(n)/SR; f=320*np.exp(-t*4)+60
    s=np.sin(2*np.pi*np.cumsum(f)/SR)*0.6+np.convolve(rng.normal(0,1,n),np.ones(60)/60,'same')*2
    return s*env(n,0.01,d/3)
def pop():
    n=int(.12*SR); t=np.arange(n)/SR; f=500+3000*t/0.12
    return np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,0.002,0.04)
def pluck(f,d=0.35,bright=1.0):
    n=int(d*SR); t=np.arange(n)/SR
    s=sum(np.sin(2*np.pi*f*k*t)/k**(1.6/bright) for k in range(1,7))
    return s*env(n,0.003,d/3.5)
def sting():  # slap-bass style riff
    out=np.zeros(int(1.0*SR))
    for i,(f,dt) in enumerate([(82.4,0),(98,0.12),(110,0.24),(73.4,0.42)]):
        x=pluck(f,0.45,1.8); j=int(dt*SR); out[j:j+len(x)]+=x
    return out*0.7
def whoosh(d=0.9):
    n=int(d*SR); noise=rng.normal(0,1,n); out=np.zeros(n); y=0
    for i in range(n):
        a=0.02+0.25*np.sin(np.pi*i/n); y+=a*(noise[i]-y); out[i]=y
    return out*np.sin(np.pi*np.arange(n)/n)*2.2
def thump():
    n=int(.3*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*(90*np.exp(-t*8)+40)*t)*env(n,0.002,0.08)*1.2
def bubbles(t0,t1):
    t=t0
    while t<t1:
        n=int(.06*SR); tt=np.arange(n)/SR; f=rng.uniform(250,600)
        add(t,np.sin(2*np.pi*f*(1+tt*6)*tt)*env(n,0.002,0.02),0.12); t+=rng.uniform(0.25,0.7)
def fanfare(t0):
    notes=[(523.25,0,.18),(659.25,.18,.18),(783.99,.36,.18),(1046.5,.54,.8)]
    for f,dt,d in notes:
        n=int((d+.3)*SR); tt=np.arange(n)/SR
        s=sum(np.sin(2*np.pi*f*k*tt+0.3*k)/k for k in range(1,6))*np.minimum(1,tt/0.02)*np.exp(-tt/(d+0.15))
        add(t0+dt,s,0.18); add(t0+dt,np.sin(2*np.pi*f/2*tt)*np.exp(-tt/(d+0.1)),0.1)
# --- Chapter 4 events
t=3.4; k=0
while t<27.8:
    if k%2==0: add(t,tock(1000+rng.uniform(-60,60)),0.3)
    else: add(t,step(),0.22)
    t+=0.55 if t<14.5 else 0.42; k+=1
add(25.7,pop(),0.35); add(25.85,sting(),0.5)
for tt in (39.6,41.2,45.0): add(tt,pop(),0.28)
add(50.2,pop(),0.35)
add(59.2,thump(),0.45)
add(66.6,whoosh(0.8),0.25)
add(76.0,tock(1320,0.25),0.12); add(76.12,tock(1760,0.3),0.1)
for tt in np.arange(84.4,86.0,0.4): add(tt,tock(520,0.04),0.3)
add(86.0,thump(),0.35)
add(87.2,tock(600,0.07),0.55)
fanfare(96.4)
# --- quiet original music bed: plucked pattern, ducks under dialogue
bed=np.zeros_like(buf); prog=[(196,247,294),(165,196,247),(175,220,262),(147,185,220)]
beat=0.5; t=3.0; i=0
while t<95:
    ch=prog[(i//8)%4]; f=ch[[0,1,2,1][i%4]]
    x=pluck(f,0.5,1.0); j=int(t*SR); n=min(len(x),len(bed)-j); bed[j:j+n]+=x[:n]
    if i%4==0:
        x=pluck(ch[0]/2,0.9,0.7); n=min(len(x),len(bed)-j); bed[j:j+n]+=x[:n]*0.8
    t+=beat; i+=1
lines=[(3.2,3.5),(7.1,7.9),(15.4,3.6),(19.4,6.1),(28.6,2.91),(32.0,4.3),(36.7,2.33),(39.4,10.6),(54.4,2.93),(57.7,7.3),(65.4,2.37),(68.2,7.7),(76.3,7.9),(87.8,4.8),(92.8,0.99),(94.2,4.4)]
g=np.ones(len(buf))*0.06
for s,d in lines: g[int((s-0.3)*SR):int((s+d+0.3)*SR)]=0.025
g=np.convolve(g,np.ones(4800)/4800,'same')
fo=np.ones(len(buf)); a=int(95*SR); b=int(96.4*SR); fo[a:b]=np.linspace(1,0,b-a); fo[b:]=0
buf+=bed*g*fo
buf=buf/np.max(np.abs(buf))*0.8
with wave.open('sfx.wav','wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf*32767).astype(np.int16).tobytes())
print('ok')
