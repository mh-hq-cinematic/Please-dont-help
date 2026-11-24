import subprocess, json
L = {
1:("F","Obstacle Four",[(1.338,4.28)]),
2:("MH","Its Just a Bag",[(6.921,8.342),(9.963,11.123),(12.304,14.665)]),
3:("F","Carrying It on Crutches",[(17.227,20.268)]),
4:("MH","Following Quickly",[(23.37,24.57),(25.631,25.951),(27.412,29.093)]),
5:("F","Who Decided",[(31.073,33.434)]),
6:("MH","Dont Remember Signing",[(36.135,38.296),(39.076,39.837)]),
7:("F","Whats in the Bag",[(42.618,44.398)]),
8:("MH","Im Fine Dont Bother Anyone",[(47.64,51.581),(52.862,53.102),(55.023,58.444)]),
9:("F","Let It Rest",[(60.737,63.118)]),
10:("MH","Sitting Down on the Bag",[(66.52,67.661),(68.802,70.182),(71.363,73.204)]),
11:("F","Write a Letter",[(74.985,76.806)]),
12:("MH","Love Letter to a Sandbag",[(79.908,86.992)]),
13:("MH","Letter to the Bag",[(95.177,96.538),(98.078,99.599),(101.139,103.12)]),
14:("MH","Lighter With Two",[(110.36,113.664),(113.865,114.605)]),
15:("F","I Knew",[(115.285,115.725)]),
16:("MH","Foxy Knew",[(118.406,119.507),(120.527,122.248)]),
17:("F","Mud Pit Opening",[(123.97,127.401)]),
}
out={}
for n,(who,title,segs) in L.items():
    spans=[]; s=segs[0][0]-0.2; e=segs[0][1]
    for a,b in segs[1:]:
        if a-e<=1.2: e=b
        else: spans.append((s,e+0.6)); s=a-0.6; e=b
    spans.append((s,e+0.35))
    parts="".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[p{i}];" for i,(a,b) in enumerate(spans))
    cat="".join(f"[p{i}]" for i in range(len(spans)))+f"concat=n={len(spans)}:v=0:a=1[c];"
    dur=sum(b-a for a,b in spans)
    flt=parts+cat+f"[c]highpass=f=80,afftdn=nf=-25,afade=t=in:d=0.05,afade=t=out:st={max(0,dur-0.12):.3f}:d=0.12,loudnorm=I=-16:TP=-1.5:LRA=11[o]"
    who_name="Muscle Hero" if who=="MH" else "Foxy"
    name=f"Ch4 Line {n} - {who_name} - {title}.m4a"
    subprocess.run(["ffmpeg","-y","-v","error","-i","rec.wav","-filter_complex",flt,"-map","[o]","-ar","48000","-c:a","aac","-b:a","160k",name],check=True)
    d=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",name]))
    out[n]={"who":who,"file":name,"dur":round(d,2)}
json.dump(out,open("lines.json","w"),indent=1)
for n,v in out.items(): print(n,v["who"],v["dur"])
