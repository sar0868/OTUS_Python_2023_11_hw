#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fnmatch
import gzip
import json
import logging
import os
import re
import statistics
import sys
import argparse
from pathlib import Path
from string import Template

from data import Data


# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config')

    return parser


def read_configure(path):
    config = {
        "REPORT_SIZE": 1000,
        "REPORT_DIR": "./reports",
        "LOG_DIR": "./log",
        "logfile": None,
        # "logfile": "log_analyzer.log",
    }

    with open(path) as f:
        for line in f:
            data = line.strip().split('=')
            if len(data) < 2:
                continue
            # except Exception:
            #     raise Exception("file don't parser")
            config[data[0]] = data[1]

    try:
        int(config['REPORT_SIZE'])
    except ValueError:
        raise ValueError("file don't parser\nREPORT_SIZE don't int")

    if not os.path.isdir(config['LOG_DIR']):
        raise TypeError(f"file don't parser\ndirectory {config['LOG_DIR']} don't exist")

    return config


def create_logger(path: str):
    logging.basicConfig(
        filename=path,
        format='[%(asctime)s] %(levelname).1s %(message)s',
        datefmt='%Y.%m.%d %H:%M:%S',
        level=logging.INFO,
    )
    return logging.getLogger()


def gen_find(filepath, top):
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepath):
            yield os.path.join(path, name)


def get_date_logfile(file: str) -> str:
    date_file: str = file.rsplit('-', maxsplit=1)[-1]
    if date_file.endswith('.gz'):
        return date_file.rsplit('.', maxsplit=1)[0]
    return date_file


def get_date_report_file(file: str) -> str:
    date_file: str = file.rsplit('-', maxsplit=1)[-1]
    return "".join(date_file.rsplit(".")[:-1])


def check_exist_report(filename: str, path) -> bool:
    date_log_file = get_date_logfile(filename)
    report_files = list(gen_find("*.html", path))
    if not report_files:
        return True
    date_report = '0'
    for i in report_files:
        date_cfile = get_date_report_file(i)
        if date_cfile > date_report:
            date_report = date_cfile
    logger.info("last date report file: %s" % date_report)
    return date_log_file > date_report


def get_filename_for_analysis(filenames):
    name = ""
    date_logfile = '0'
    for i in filenames:
        current_date_logfile = get_date_logfile(i)
        if current_date_logfile > date_logfile:
            name = i
            date_logfile = current_date_logfile

    return name


def get_open(name):
    return gzip.open(name) if name.endswith('.gz') else open(name)


def gen_grep(lines):
    prog = re.compile("GET")
    for line in lines:
        if type(line) == bytes:
            if prog.search(line.decode()):
                yield line.decode()
        else:
            if prog.search(line):
                yield line


def parse_line(lines):
    for line in lines:
        yield line.rsplit(None, 1)


def calculation_report(records, error_level):
    record = ((x[0].rsplit('"')[1], x[1]) for x in records)
    result: dict[str, Data] = dict()
    total_count = 0
    total_time_sum = 0
    cnt_error = 0
    for i in record:
        temp = i[0].rsplit()
        url = temp[1]
        try:
            time_request = float(i[1])
        except ValueError:
            cnt_error += 1
            continue
        total_count += 1
        total_time_sum += time_request
        if url in result:
            result[url].count += 1
            result[url].time_list.append(time_request)
        else:
            result[url] = Data(url=url, time_list=[time_request])
    if cnt_error * 100 / (total_count + cnt_error) > error_level:
        return
    for data in result.values():
        data.count_perc = data.count * 100 / total_count
        data.time_sum = sum(data.time_list)
        data.time_perc = data.time_sum * 100 / total_time_sum
        data.time_avg = statistics.mean(data.time_list)
        data.time_max = max(data.time_list)
        data.time_med = statistics.median(data.time_list)
    return result


def create_report(date_log: str, result, path):
    root_result = Path(path)
    if not root_result.exists():
        Path.mkdir(root_result)
    filename = root_result / f'report-{date_log}.html'
    data_report = [el[1].get_dict() for el in result]
    try:
        with open('report.html') as file, open(filename, 'w') as report:
            template = Template(file.read())
            report.write(template.safe_substitute(table_json=json.dumps(data_report)))
    except FileNotFoundError as e:
        logger.exception(e)
    except OSError:
        os.remove(filename)
        logger.error("file report don't create")
    else:
        logger.info("file report name='%s' create" % str(filename).rsplit('/')[-1])


def main(config: dir):
    # top = os.getcwd()
    top = config['LOG_DIR']
    filenames = list(gen_find('nginx-access-ui.log*', top=top))
    filename = get_filename_for_analysis(filenames)
    if filename:
        logger.info("find last file %s" % filename.split("/")[-1])
    else:
        logger.error("last log file don't find")
        return
    if not check_exist_report(filename, config['REPORT_DIR']):
        logger.info("report file exists")
        return
    logfiles = get_open(filename)

    pathlines = gen_grep(logfiles)
    records = parse_line(pathlines)
    result = calculation_report(records, float(config['ERROR_LEVEL']))
    if not result:
        logger.error("error level exceeded")
        return
    date_report_file = get_date_logfile(filename)
    date_file = '%s.%s.%s' % (date_report_file[:4], date_report_file[4:6], date_report_file[6:])
    create_report(date_file,
                  sorted(result.items(),
                         key=lambda el: el[1].time_sum, reverse=True)[:int(config['REPORT_SIZE'])],
                  path=config["REPORT_DIR"])


if __name__ == "__main__":
    parser = create_parser()
    namespace = parser.parse_args()
    if namespace.config:
        config = read_configure(namespace.config)
    else:
        raise Exception("couldn't find the configuration file")
    logger = create_logger(config["logfile"])
    logger.info("start script")

    try:
        main(config)
    except KeyboardInterrupt as e:
        logger.exception(e)
    logger.info("end script")
