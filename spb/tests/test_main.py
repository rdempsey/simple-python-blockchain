import pytest
from mock import MagicMock, patch
from spb import __main__ as spb_main
import os
import sys


@pytest.fixture
def mock_base_args():
    args = {
        '<log-name>': 'mock_log',
        '<log-level>': 'INFO',
        '<num-blocks-to-create>': '20',
        '--log-file-name': None,
        '--log-dir': None
    }
    return args


@pytest.fixture()
def mock_all_args():
    args = {
        '<log-name>': 'mock_log',
        '<log-level>': 'INFO',
        '<num-blocks-to-create>': '20',
        '--log-file-name': 'mock_log.log',
        '--log-dir': '/fake/path/to/directory'
    }
    return args


class TestMain(object):
    def test_ensure_spb_can_be_run_with_base_args(self, mock_base_args):
        spb_main.run_spb(mock_base_args)

    @patch('spb.__main__.os.path')
    @patch('spb.__main__.os')
    def test_ensure_spb_can_be_run_with_all_args(self, mock_os, mock_path, mock_all_args):
        mock_path.join.return_value = os.path.join(mock_all_args['--log-dir'], mock_all_args['--log-file-name'])
        mock_file_handle = MagicMock(return_value=MagicMock())
        with patch('builtins.open', mock_file_handle):
            spb_main.run_spb(mock_all_args)

    def test_ensure_logger_is_created_from_base_args(self, mock_base_args):
        logger = spb_main._create_logger(args=mock_base_args)
        assert logger is not None

    @patch('spb.__main__.os.path')
    @patch('spb.__main__.os')
    def test_ensure_logger_is_created_using_all_args(self, mock_os, mock_path, mock_all_args):
        spb_main.args = mock_all_args
        mock_path.join.return_value = os.path.join(mock_all_args['--log-dir'], mock_all_args['--log-file-name'])

        mock_file_handle = MagicMock(return_value=MagicMock())
        with patch('builtins.open', mock_file_handle):
            logger = spb_main._create_logger(args=mock_all_args)
            assert logger is not None

    @patch('spb.__main__.os.path.exists')
    @patch('spb.__main__.os.makedirs')
    @patch('spb.__main__.os.path')
    @patch('spb.__main__.os')
    def test_ensure_logger_and_log_file_are_created(self, mock_os, mock_path, mock_make_dirs, mock_exists, mock_all_args):
        spb_main.args = mock_all_args
        mock_exists.return_value = False
        mock_path.join.return_value = os.path.join(mock_all_args['--log-dir'], mock_all_args['--log-file-name'])

        mock_file_handle = MagicMock(return_value=MagicMock())
        with patch('builtins.open', mock_file_handle):
            spb_main._create_logger(args=mock_all_args)
            mock_make_dirs.assert_called_with('/fake/path/to/directory')

    def test_ensure_genesis_block_is_added_to_blockchain(self):
        mock_blockchain = list()
        spb_main._add_genesis_block_to_blockchain(mock_blockchain)
        assert len(mock_blockchain) == 1

    def test_ensure_multiple_blocks_are_added_to_blockchain(self, mock_base_args):
        logger = spb_main._create_logger(args=mock_base_args)

        mock_blockchain = list()
        spb_main._add_genesis_block_to_blockchain(mock_blockchain)
        assert len(mock_blockchain) == 1

        spb_main._add_blocks_to_blockchain(num_blocks_to_add=20, blockchain=mock_blockchain, logger=logger)
        assert len(mock_blockchain) == 21
