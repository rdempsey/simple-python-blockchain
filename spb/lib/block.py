import hashlib


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self._hash_block()

    def _hash_block(self):
        sha = hashlib.sha256()
        encoded_data = self._encode_data_for_hash_update()
        sha.update(encoded_data)
        return sha.hexdigest()

    def _encode_data_for_hash_update(self):
        e_index = str(self.index).encode('utf-8')
        e_timestamp = str(self.timestamp).encode('utf-8')
        e_data = str(self.data).encode('utf-8')
        e_previous_hash = str(self.previous_hash).encode('utf-8')
        encoded_data_for_hashing = e_index + e_timestamp + e_data + e_previous_hash
        return encoded_data_for_hashing
