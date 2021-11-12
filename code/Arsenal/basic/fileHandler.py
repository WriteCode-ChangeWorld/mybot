# -*- encoding: utf-8 -*-
'''
@File    :   fileio.py
@Time    :   2021/06/24 15:05:59
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
import json
import yaml
# from yaml import cyaml
from yaml.loader import Loader, SafeLoader


from log_record import logger


class LoadFile:
	# read yaml file
    @logger.catch
    def by_yaml(self, yaml_path, encoding='utf8', loader=SafeLoader):
        try:
            config_yaml = yaml.load(open(yaml_path, encoding=encoding), Loader=loader)
        except yaml.parser.ParserError as err:
            logger.warning(f"[yaml.load Error]: {err}")
            logger.warning(f"[yaml.path : {yaml_path}")
            return {}
        else:
            return config_yaml

	# read json file
    @logger.catch
    def by_json(self, json_path, encoding='utf8'):
        try:
            with open(json_path, encoding=encoding) as f:
                json_data = json.load(f)
        except json.decoder.JSONDecodeError as err:
            logger.warning(f"[json.load Error]: {err}")
            logger.warning(f"[json.path : {json_path}")
            return {}
        else:
            return json_data

class DumpFile:
	# dump yaml file
    @logger.catch
    def by_yaml(self, data, yaml_path, mode="w", encoding='utf8'):
        try:
            with open(yaml_path, mode=mode, encoding=encoding) as f:
                yaml.dump(data, f)
        except yaml.parser.ParserError as err:
            logger.warning(f"[yaml.dump Error]: {err}")
            logger.warning(f"[yaml.path : {yaml_path}")
            logger.warning(f"[yaml.data : {data}")
            return False
        else:
            return True

	# dump json file
    @logger.catch
    def by_json(self, data, json_path, mode="w", encoding='utf8'):
        try:
            with open(json_path, mode=mode, encoding=encoding) as f:
                json.dump(data, f, ensure_ascii=False)
        except json.decoder.JSONDecodeError as err:
            logger.warning(f"[json.dump Error]: {err}")
            logger.warning(f"[json.path : {json_path}")
            logger.warning(f"[json.data : {data}")
            return False
        else:
            return True

loadFile = LoadFile()
dumpFile = DumpFile()