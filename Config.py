import os
import yaml
"""
Config file to hold FAIR Data Point and CEDAR related info
"""

CONFIG_FILE = "config.yml"
FDP_URL = None
FDP_USERNAME = None
FDP_PASSWORD = None
FDP_PERSISTENT_URL = None
CEDAR_TEMPLATE_ID = None
CEDAR_TEMPLATE_URL = None
CEDAR_BEG_URL = None
CEDAR_API_KEY = None

if os.path.isfile(CONFIG_FILE) :
    yaml_file = open(CONFIG_FILE)
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)
    # FDP config
    FDP_URL = config['FDP']['URL']
    FDP_USERNAME = config['FDP']['USERNAME']
    FDP_PASSWORD = config['FDP']['PASSWORD']
    FDP_PERSISTENT_URL = config['FDP']['PERSISTENT_URL']
    # CEDAR config
    CEDAR_TEMPLATE_ID = config['CEDAR']['TEMPLATE_ID']
    CEDAR_TEMPLATE_URL = config['CEDAR']['TEMPLATE_URL']
    CEDAR_BEG_URL = config['CEDAR']['BEG_URL']
    CEDAR_API_KEY = config['CEDAR']['API_KEY']
else:
    raise SystemExit("Config file does exits. Provided input file " + CONFIG_FILE)