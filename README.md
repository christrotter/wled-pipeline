# wled-pipeline
Caveat!  Copilot-generated, coaching by me.  I'm not a python developer by trade.

I needed a way to easily generate presets and segments, doing it via the UI only was sadness.  There is not much provided to do this beyond 'uhhh look at the API docs' or 'uhhh use this rust library' - which is fine, it's open source and I'm not complaining!

But we can get a full config json...and that means copilot can mangle it for us.  And when you have a functional full structure, copilot is actually pretty good at this.  As it's not my job and life dream to be an expert in the json schema of WLED, let's have copilot handle those duties, shall we?

I needed some simple presets - they are just solid colours called via API from the `qmk-hid-host` c/o the pedals (qmk) switching layers.

# How to use
Update your presets in `main.py`, tell copilot to add more bits to them if you need it.

Run `bootstrap.sh` to get the basics set up.

Run `python src/main.py` from your commandline.

Copy the contents of `src/generated_configs/recreated_config.json` into `http://[WLED ip address]/edit` - choosing the `presets.json` file.  Overwrite whatever is there.  Save.

# todo
- I'm sure there is an API for jamming the whole preset config in - the whole process could be automated.
- And then you'd want to test it prior to jamming, but, see jobs/hopes/dreams comment above.

# Example preset
```python
self.presets = {
    "qmk-layer-1": {
        "color": [255, 252, 251],  # base layer
        "transition": 1,
        "main_sel": False,
        "qmk_sel": True,
    },
```
