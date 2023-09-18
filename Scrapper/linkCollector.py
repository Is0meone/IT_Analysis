from Scrapper import JustITScrapper
from Scrapper import NoFluffScrapper
from Scrapper import PracujPLScrapper

#TODO: make to read whole page
justIT_lB = JustITScrapper.extractLinks("https://justjoin.it")

NoFluff_lB = NoFluffScrapper.extractAllLinks(30)

PracujPL_lB = PracujPLScrapper.extractAllLinks(30)

print(justIT_lB)
print(NoFluff_lB)
print(PracujPL_lB)