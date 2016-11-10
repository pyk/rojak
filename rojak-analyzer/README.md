# rojak-analyzer

## Setup
I recommend to setup the `virtualenv` first using `virualenvwrapepr`.
    
    workon rojak
    pip install -r requirments.txt

## Train Analyzer
To generate the model, download the data first [here](https://slack-files.com/T2JFL31BR-F2YTDSLCT-0eceb7b18e)

    python rojak_ovr_pair.py

## Run Analyzer

    python rojak.py run --model=rojak_ovr_pair_latest_pentagram_model.bin --only-media=kompas,detikcom --max-news=20

## Help

    python rojak.py --help

