# Synergy Data Check

Checks for invalid pitch types, video duration, and likely missing videos. Scans each pitcher's videos, for each school.

## Install

Download check.py or git clone. \
`git clone https://github.com/matt-rog/synergy-data-check.git`

Install externel dep. for parsing mp4 data \
`pip install mutagen`

Expected file structure:

```
.
└── <school_name>/
   └── <player_name>/
       ├── video/
       └── Export.csv
```

## Usage

Run the following at the root of your Synergy data directory, as referenced above. \
`python path/to/check.py`
