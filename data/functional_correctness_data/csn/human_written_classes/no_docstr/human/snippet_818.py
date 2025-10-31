import itertools
from PyDC.PyDC.utils import MaxPosArraived, PatternNotFound, bits2codepoint, bitstream2codepoints, codepoints2bitstream, count_the_same, find_iter_window, iter_steps, list2str, pformat_codepoints, print_bitlist

class BitstreamHandlerBase:

    def __init__(self, cassette, cfg):
        self.cassette = cassette
        self.cfg = cfg

    def feed(self, bitstream):
        while True:
            print('_' * 79)
            try:
                self.sync_bitstream(bitstream)
            except SyncByteNotFoundError as err:
                log.error(err)
                log.info(f'Last wave pos: {bitstream.pformat_pos()}')
                break
            block_type, block_length, codepoints = self.get_block_info(bitstream)
            try:
                block_type_name = self.cfg.BLOCK_TYPE_DICT[block_type]
            except KeyError:
                print(f'ERROR: Block type {hex(block_type)} unknown in BLOCK_TYPE_DICT!')
                print('-' * 79)
                print('Debug bitlist:')
                print_bitlist(bitstream)
                print('-' * 79)
                break
            log.debug(f'block type: 0x{block_type:x} ({block_type_name})')
            self.cassette.buffer_block(block_type, block_length, codepoints)
            if block_type == self.cfg.EOF_BLOCK:
                log.info('EOF-Block found')
                break
            if block_length == 0:
                print('ERROR: block length == 0 ???')
                print('-' * 79)
                print('Debug bitlist:')
                print_bitlist(bitstream)
                print('-' * 79)
                break
            print('=' * 79)
        self.cassette.buffer2file()

    def get_block_info(self, codepoint_stream):
        block_type = next(codepoint_stream)
        log.info(f'raw block type: {hex(block_type)} ({repr(block_type)})')
        block_length = next(codepoint_stream)
        codepoints = tuple(itertools.islice(codepoint_stream, block_length))
        try:
            verbose_block_type = self.cfg.BLOCK_TYPE_DICT[block_type]
        except KeyError:
            log.error('Blocktype unknown!')
            print(pformat_codepoints(codepoints))
            sys.exit()
        real_block_len = len(codepoints)
        if real_block_len == block_length:
            log.info(f'Block length: {block_length}Bytes, ok.')
        else:
            log.error(f'Block should be {block_length}Bytes but are: {real_block_len}Bytes!')
        origin_checksum = next(codepoint_stream)
        calc_checksum = sum((codepoint for codepoint in codepoints))
        calc_checksum += block_type
        calc_checksum += block_length
        calc_checksum = calc_checksum & 255
        if calc_checksum == origin_checksum:
            log.info(f'Block checksum {hex(origin_checksum)} is ok.')
        else:
            log.error(f'Block checksum {hex(origin_checksum)} is not equal with calculated checksum: {hex(calc_checksum)}')
        return (block_type, block_length, codepoints)