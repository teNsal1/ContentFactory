ContentFactory — Tools

Initial MVP

Component	Candidate	Purpose	Status
Pipeline	Python	Coordinate all stages	Planned
Voiceover	Local text-to-speech engine	Generate narration	Not tested
Visuals	Existing images or free assets	Provide video scenes	Not tested
Subtitles	Whisper or another free tool	Create captions	Not tested
Video assembly	FFmpeg	Produce vertical MP4	Not tested
Publishing	YouTube Data API	Upload Shorts	Later

Rules

* Verify current installation and usage requirements before choosing tools.
* Prefer free options that work on Windows.
* Do not require a paid API for the initial MVP.
* Test every component separately before connecting the pipeline.
* Keep manual review before publication.

First acceptance test

Given one topic, generate one vertical MP4 with narration, visuals, and subtitles without manually assembling the timeline.