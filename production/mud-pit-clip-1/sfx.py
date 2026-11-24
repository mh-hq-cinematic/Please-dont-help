import numpy as np, wave
SR=48000; END=67; buf=np.zeros(int(SR*END))
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
# --- crutch walk 3.2–12.5: right crutch, left foot, left crutch, right foot (beat 0.45s)
t=3.4; k=0
while t<12.4:
    if k%2==0: add(t,tock(1000+rng.uniform(-60,60)),0.35)
    else: add(t,step(),0.25)
    t+=0.45; k+=1
add(15.4,step(),0.25); add(15.95,squelch(0.7),0.55); add(16.5,squelch(0.5),0.35)
bubbles(17.0,38.5)
for t in np.arange(22.6,24.4,0.4): add(t,tock(520,0.04),0.3)   # hooves arrive
add(33.9,pop(),0.35); add(34.05,sting(),0.55)
add(38.55,whoosh(1.0),0.4); add(38.7,squelch(0.5),0.4); add(40.0,thump(),0.5)
add(47.2,pop(),0.35)
add(51.02,tock(600,0.07),0.55)   # the hoof tap
for t in np.arange(51.6,54.4,0.4): add(t,tock(520,0.04),0.22)
add(53.0,tock(2400,0.015),0.12)  # porch light click
fanfare(62.3)
# --- quiet original music bed: plucked pattern, ducks under dialogue
bed=np.zeros_like(buf); prog=[(196,247,294),(165,196,247),(175,220,262),(147,185,220)]
beat=0.5; t=3.0; i=0
while t<61:
    ch=prog[(i//8)%4]; f=ch[[0,1,2,1][i%4]]
    x=pluck(f,0.5,1.0); j=int(t*SR); n=min(len(x),len(bed)-j); bed[j:j+n]+=x[:n]
    if i%4==0:
        x=pluck(ch[0]/2,0.9,0.7); n=min(len(x),len(bed)-j); bed[j:j+n]+=x[:n]*0.8
    t+=beat; i+=1
lines=[(6.0,9.1),(17.5,5.1),(24.0,9.7),(40.5,6.5),(54.0,6.9)]
g=np.ones(len(buf))*0.06
for s,d in lines: g[int((s-0.3)*SR):int((s+d+0.3)*SR)]=0.025
g=np.convolve(g,np.ones(4800)/4800,'same')
fo=np.ones(len(buf)); a=int(60*SR); b=int(61.2*SR); fo[a:b]=np.linspace(1,0,b-a); fo[b:]=0
buf+=bed*g*fo
buf=buf/np.max(np.abs(buf))*0.8
with wave.open('sfx.wav','wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf*32767).astype(np.int16).tobytes())
print('ok')
