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

## ch4-sandbag
"Every Obstacle Needs a Friend, Chapter 4: A Love Letter to a Sandbag" (1:41). Kyle voices Muscle Hero; Kyle's therapist voices Foxy Fax (recorded together Nov 24, 2026).
Line files `Ch4 Line N - <Speaker> - <Title>.m4a`. Line 17 (Foxy: "Obstacle one. The mud pit. Let's see if he asks.") is a pickup for the Mud Pit clip and is not used in Chapter 4.
Voice start times: 3.2, 7.1, 15.4, 19.4, 28.6, 32.0, 36.7, 39.4, 54.4, 57.7, 65.4, 68.2, 76.3, 87.8, 92.8, 94.2 s.
