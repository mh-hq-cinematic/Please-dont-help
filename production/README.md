# Production files

Source files for the Paper Hero Club clips and images made for Please “Don’t” Help. Nothing in this folder is part of the live page.

## mud-pit-clip-1
"Every Obstacle Needs a Friend, Clip 1: The Mud Pit" (67 s, 1920x1080, 24 fps).

- `Mud Pit - Every Obstacle Needs a Friend Clip 1.mp4`: the finished video with Kyle's voice and original sound
- `Mud Pit Line 1–6 … .m4a`: Kyle's six recorded lines, cut and cleaned (highpass 80 Hz, light noise reduction, loudnorm -16)
- `lines.json`: clip lengths; line start times are in `scene.html` (LINES) and the mix command below
- `scene.html`: the animated 3D-cardstock scene; `render(t)` draws any moment
- `face.png`: Muscle Hero's face, cut from Kyle's race-day photo
- `sfx.py`: synthesizes all sound effects and the quiet music bed (`sfx.wav`)
- `cut.py`: cuts the lines from the recording using the Picsart transcript's word timings
- `render.js` / `snap.js`: render all frames to `video.mp4` / snapshot single moments

Voice line start times in the final mix: 6.0, 17.5, 24.0, 40.5, 54.0, 62.6 seconds.

## link-preview
`social-card.html` renders the 1200x630 share image (`/preview.png` at the site root, made at 2x).
