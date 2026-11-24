import subprocess, json
# word groups (start,end) per line from Picsart transcript
L = {
1:("Mud Pit Easy",[(1.071,1.892),(3.392,3.813),(5.013,6.954),(7.975,9.895)]),
2:("Mud Is Winning",[(12.957,14.758),(15.838,17.459)]),
3:("Im Good Mud Plank",[(20.14,20.92),(21.961,22.981),(24.282,25.102),(26.263,27.303),(28.544,29.344)]),
4:("I Had It But Thanks",[(31.876,32.356),(33.217,33.857),(35.238,36.059),(36.899,37.92)]),
5:("One Hoof Tap",[(41.042,42.202),(43.263,45.284),(45.904,47.345)]),
6:("Do It The Muscle Hero Way",[(49.727,51.468)]),
}
out={}
for n,(title,segs) in L.items():
    # build kept spans: pad 0.2 before first, 0.35 after last; gaps >1.2 trimmed to 0.6 each side
    spans=[]; s=segs[0][0]-0.2; e=segs[0][1]
    for a,b in segs[1:]:
        if a-e<=1.2: e=b
        else: spans.append((s,e+0.6)); s=a-0.6; e=b
    spans.append((s,e+0.35))
    parts="".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[p{i}];" for i,(a,b) in enumerate(spans))
    cat="".join(f"[p{i}]" for i in range(len(spans)))+f"concat=n={len(spans)}:v=0:a=1[c];"
    dur=sum(b-a for a,b in spans)
    flt=parts+cat+f"[c]highpass=f=80,afftdn=nf=-25,afade=t=in:d=0.05,afade=t=out:st={dur-0.12:.3f}:d=0.12,loudnorm=I=-16:TP=-1.5:LRA=11[o]"
    name=f"Mud Pit Line {n} - {title}.m4a"
    subprocess.run(["ffmpeg","-y","-v","error","-i","rec.wav","-filter_complex",flt,"-map","[o]","-ar","48000","-c:a","aac","-b:a","160k",name],check=True)
    d=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",name]))
    out[n]={"file":name,"dur":round(d,2)}
json.dump(out,open("lines.json","w"),indent=1); print(json.dumps(out,indent=1))
