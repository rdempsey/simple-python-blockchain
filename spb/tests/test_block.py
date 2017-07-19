from datetime import datetime

from spb.lib.block import Block


class TestBlock(object):
    def test_ensure_a_block_can_be_created(self):
        index = 0
        timestamp = datetime.utcnow()
        data = 'this is some data'
        previous_hash = '770709ec27c964fed7b8c5df97912ae44e42c6c34c3f75a83c33f6d259f6bcbb'
        test_block = Block(index, timestamp, data, previous_hash)
        assert type(test_block) == Block
