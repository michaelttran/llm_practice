## Summary
asdads

## Setup
- python3 -m virtualenv env
- source /env/bin/activate
- pip3 install -r requirements.txt
- python3 aapi.py

## TODO
- Maybe take what it transcribes and calculate its accuracy?
- Is there a bug on the front end? I only use $0.5/0.05 each run and after running three times, I hit my limit on the webpage
    - "Unable to retrieve your balance. Please try again or contact support if the problem persists."
- For movie torrents that don't come with SRTs, I can actually run them through the API to get subtitles
- Extract audio file from movies
- Refactor directory design to include different LLMs
- Cleanup file pathing
- When logging, how to save transcriptions + their data source without bloating logs -> transcription txt files as a hash


## Learnings
- Creating a source of truth for validation can be hard
    - Using music sounded good because most lyrics can be found online, so I don't have to manually write them out myself