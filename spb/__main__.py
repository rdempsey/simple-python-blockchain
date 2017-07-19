"""
Python Simple Blockchain

Usage:
     __main__.py <log-name> <log-level> <num-blocks-to-create>
     __main__.py <log-name> <log-level> <num-blocks-to-create> --log-dir=<dirpath> --log-file-name=<filename>
     __main__.py (-h | --help)
     __main__.py (-v | --version)

Options:
    -h --help               Show this screen.
    -v --version            Show version.
    --log-dir=<ld>          Log directory.
    --log-file-name=<lfn>   Log file name.

"""

from docopt import docopt
from datetime import datetime
from lib.block import Block
from os import path, makedirs
import logging


def run_spb():
    args = docopt(__doc__, version='Simple Python Blockchain 0.1.0')

    _logger = _create_logger(args=args)

    blockchain = [_create_genesis_block()]

    num_blocks_to_add = int(args['<num-blocks-to-create>'])
    _add_blocks_to_blockchain(num_blocks_to_add=num_blocks_to_add, blockchain=blockchain, logger=_logger)


def _create_logger(args):
    log_name = args['<log-name>']
    log_level = args['<log-level>']

    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    logging.basicConfig(format=logging_format)
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)

    if args['--log-file-name']:
        log_dir = args['--log-dir']
        log_file_name = args['--log-file-name']

        _make_directory(log_dir)

        log_file_path = path.join(log_dir, log_file_name)
        fh = logging.FileHandler(filename=log_file_path)
        fh.setLevel(log_level)
        formatter = logging.Formatter(logging_format)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def _make_directory(directory_path):
    """
    Make a directory if it doesn't already exist
    :param directory_path: full path to the directory
    :return: directory_path
    """
    if not path.exists(directory_path):
        makedirs(directory_path)

    return directory_path


def _create_genesis_block():
    return Block(0, datetime.now(), "Genesis Block", "0")


def _create_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = datetime.now()
    this_data = "Hey! I'm block " + str(this_index)
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)


def _add_blocks_to_blockchain(num_blocks_to_add, blockchain, logger):
    for i in range(0, num_blocks_to_add):
        previous_block = blockchain[i]
        block_to_add = _create_block(previous_block)
        blockchain.append(block_to_add)
        logger.info("Block #{} has been added to the blockchain!".format(block_to_add.index))
        logger.info("Hash: {}\n".format(block_to_add.hash))


if __name__ == '__main__':
    run_spb()
