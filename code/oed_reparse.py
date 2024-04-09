from pathlib import Path
import oed_extract

TEST_LEMMA = 'lancet_n'

parser = oed_extract.OEDLemmaParser(TEST_LEMMA, True)
parser.access()
parser.parse()
# print(parser.variants)
parser.save(Path(f'../data/oed_quotations_v1/'))