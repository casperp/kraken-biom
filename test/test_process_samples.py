#!/usr/bin/env python
# coding: utf-8
import os, os.path as osp
import tempfile
from textwrap import dedent as twdd
import unittest

import kraken_biom as kb
from test.test_parsing import prep_kraken_input


class kraken_biom_Test(unittest.TestCase):
    def setUp(self):
        self.krepA = twdd(u"""\
            100.00	6783846	6783846	U	0	unclassified
            0.00	130	18	-	1	root
            0.00	105	0	-	131567	  cellular organisms
            0.00	105	0	D	2	    Bacteria
            0.00	62	30	P	1239	      Firmicutes
            0.00	29	0	C	91061	        Bacilli
            0.00	29	0	O	186826	          Lactobacillales
            0.00	20	0	F	1300	            Streptococcaceae
            0.00	20	8	G	1301	              Streptococcus
            0.00	5	4	S	1304	                Streptococcus salivarius
            0.00	1	1	-	1048332	                  Streptococcus salivarius CCHSS3
            0.00	3	0	S	1303	                Streptococcus oralis
            0.00	3	3	-	927666	                  Streptococcus oralis Uo5
            0.00	2	2	S	1318	                Streptococcus parasanguinis
            0.00	1	0	S	1305	                Streptococcus sanguinis
            0.00	1	1	-	388919	                  Streptococcus sanguinis SK36
            0.00	1	1	S	1308	                Streptococcus thermophilus
            0.00	9	0	F	81852	            Enterococcaceae
            0.00	9	0	G	1350	              Enterococcus
            0.00	9	0	S	37734	                Enterococcus casseliflavus
            0.00	9	9	-	565655	                  Enterococcus casseliflavus EC20
            0.00	1	0	C	186801	        Clostridia
            0.00	1	1	O	186802	          Clostridiales
            0.00	40	0	P	1224	      Proteobacteria
            0.00	20	2	C	1236	        Gammaproteobacteria
            0.00	11	1	O	135622	          Alteromonadales
            0.00	10	0	F	72275	            Alteromonadaceae
            0.00	10	0	G	226	              Alteromonas
            0.00	10	0	S	28108	                Alteromonas macleodii
            0.00	10	10	-	1300257	                  Alteromonas macleodii str. 'Ionian Sea U8'
            0.00	7	0	O	91347	          Enterobacteriales
            0.00	7	6	F	543	            Enterobacteriaceae
            0.00	1	0	G	561	              Escherichia
            0.00	1	1	S	562	                Escherichia coli
            0.00	20	5	C	28216	        Betaproteobacteria
            0.00	15	0	O	80840	          Burkholderiales
            0.00	11	0	F	119060	            Burkholderiaceae
            0.00	11	0	G	48736	              Ralstonia
            0.00	11	10	S	329	                Ralstonia pickettii
            0.00	1	1	-	428406	                  Ralstonia pickettii 12D
            0.00	4	0	F	80864	            Comamonadaceae
            0.00	2	2	G	12916	              Acidovorax
            0.00	2	0	G	201096	              Alicycliphilus
            0.00	2	0	S	179636	                Alicycliphilus denitrificans
            0.00	2	2	-	596154	                  Alicycliphilus denitrificans K601
            0.00	3	0	P	201174	      Actinobacteria
            0.00	3	0	C	1760	        Actinobacteria
            0.00	2	0	-	84998	          Coriobacteridae
            0.00	2	0	O	84999	            Coriobacteriales
            0.00	2	0	-	255727	              Coriobacterineae
            0.00	2	0	F	84107	                Coriobacteriaceae
            0.00	2	0	G	1380	                  Atopobium
            0.00	2	0	S	1382	                    Atopobium parvulum
            0.00	2	2	-	521095	                      Atopobium parvulum DSM 20469
            0.00	1	0	-	85003	          Actinobacteridae
            0.00	1	0	O	2037	            Actinomycetales
            0.00	1	0	-	85009	              Propionibacterineae
            0.00	1	0	F	31957	                Propionibacteriaceae
            0.00	1	0	G	1743	                  Propionibacterium
            0.00	1	1	S	1747	                    Propionibacterium acnes
            0.00	20	0	D	2157	    Archaea
            0.00	20	7	P	28890	      Euryarchaeota
            0.00	8	0	C	183963	        Halobacteria
            0.00	8	0	O	1644060	          Natrialbales
            0.00	8	0	F	1644061	            Natrialbaceae
            0.00	8	0	G	29287	              Natronococcus
            0.00	8	0	S	29288	                Natronococcus occultus
            0.00	8	8	-	694430	                  Natronococcus occultus SP4
            0.00	4	0	C	224756	        Methanomicrobia
            0.00	4	0	O	94695	          Methanosarcinales
            0.00	4	0	F	2206	            Methanosarcinaceae
            0.00	3	0	G	101191	              Methanomethylovorans
            0.00	3	0	S	101192	                Methanomethylovorans hollandica
            0.00	3	3	-	867904	                  Methanomethylovorans hollandica DSM 15978
            0.00	1	0	G	2207	              Methanosarcina
            0.00	1	0	S	2214	                Methanosarcina acetivorans
            0.00	1	1	-	188937	                  Methanosarcina acetivorans C2A
            0.00	1	0	C	183939	        Methanococci
            0.00	1	0	O	2182	          Methanococcales
            0.00	1	0	F	2183	            Methanococcaceae
            0.00	1	0	G	2184	              Methanococcus
            0.00	1	0	S	2188	                Methanococcus voltae
            0.00	1	1	-	456320	                  Methanococcus voltae A3
            0.00	7	0	D	10239	  Viruses
            0.00	2	0	-	29258	    ssDNA viruses
            0.00	2	0	F	10841	      Microviridae
            0.00	2	0	G	10842	        Microvirus
            0.00	2	2	S	374840	          Enterobacteria phage phiX174 sensu lato
            0.00	2	0	-	35237	    dsDNA viruses, no RNA stage
            0.00	2	0	F	10482	      Polydnaviridae
            0.00	2	0	G	10483	        Ichnovirus
            0.00	2	2	S	265522	          Hyposoter fugitivus ichnovirus
            0.00	2	0	-	439488	    ssRNA viruses
            0.00	2	0	-	35278	      ssRNA positive-strand viruses, no DNA stage
            0.00	2	0	F	11018	        Togaviridae
            0.00	2	0	G	11019	          Alphavirus
            0.00	2	0	-	177872	            VEEV complex
            0.00	2	2	S	11036	              Venezuelan equine encephalitis virus
            0.00	1	0	-	35268	    Retro-transcribing viruses
            0.00	1	0	F	11632	      Retroviridae
            0.00	1	0	-	35276	        unclassified Retroviridae
            0.00	1	0	-	206037	          Human endogenous retroviruses
            0.00	1	0	S	45617	            Human endogenous retrovirus K
            0.00	1	1	-	166122	              Human endogenous retrovirus K113
            """).encode("utf-8")

        self.krepB = twdd(u"""\
            100.00	6783846	6783846	U	0	unclassified
            0.00	130	18	-	1	root
            0.00	105	0	-	131567	  cellular organisms
            0.00	105	0	D	2	    Bacteria
            0.00	62	30	P	1239	      Firmicutes
            0.00	29	0	C	91061	        Bacilli
            0.00	29	0	O	186826	          Lactobacillales
            0.00	20	0	F	1300	            Streptococcaceae
            0.00	20	8	G	1301	              Streptococcus
            0.00	5	4	S	1304	                Streptococcus salivarius
            0.00	1	1	-	1048332	                  Streptococcus salivarius CCHSS3
            0.00	3	0	S	1303	                Streptococcus oralis
            0.00	3	3	-	927666	                  Streptococcus oralis Uo5
            0.00	2	2	S	1318	                Streptococcus parasanguinis
            0.00	1	0	S	1305	                Streptococcus sanguinis
            0.00	1	1	-	388919	                  Streptococcus sanguinis SK36
            0.00	1	1	S	1308	                Streptococcus thermophilus
            0.00	9	0	F	81852	            Enterococcaceae
            0.00	9	0	G	1350	              Enterococcus
            0.00	9	0	S	37734	                Enterococcus casseliflavus
            0.00	9	9	-	565655	                  Enterococcus casseliflavus EC20
            0.00	1	0	C	186801	        Clostridia
            0.00	1	1	O	186802	          Clostridiales
            0.00	40	0	P	1224	      Proteobacteria
            0.00	20	2	C	1236	        Gammaproteobacteria
            0.00	11	1	O	135622	          Alteromonadales
            0.00	10	0	F	72275	            Alteromonadaceae
            0.00	10	0	G	226	              Alteromonas
            0.00	10	0	S	28108	                Alteromonas macleodii
            0.00	10	10	-	1300257	                  Alteromonas macleodii str. 'Ionian Sea U8'
            0.00	7	0	O	91347	          Enterobacteriales
            0.00	7	6	F	543	            Enterobacteriaceae
            0.00	1	0	G	561	              Escherichia
            0.00	1	1	S	562	                Escherichia coli
            0.00	20	5	C	28216	        Betaproteobacteria
            0.00	15	0	O	80840	          Burkholderiales
            0.00	11	0	F	119060	            Burkholderiaceae
            0.00	11	0	G	48736	              Ralstonia
            0.00	11	10	S	329	                Ralstonia pickettii
            0.00	1	1	-	428406	                  Ralstonia pickettii 12D
            0.00	4	0	F	80864	            Comamonadaceae
            0.00	2	2	G	12916	              Acidovorax
            0.00	2	0	G	201096	              Alicycliphilus
            0.00	2	0	S	179636	                Alicycliphilus denitrificans
            0.00	2	2	-	596154	                  Alicycliphilus denitrificans K601
            0.00	3	0	P	201174	      Actinobacteria
            0.00	3	0	C	1760	        Actinobacteria
            0.00	2	0	-	84998	          Coriobacteridae
            0.00	2	0	O	84999	            Coriobacteriales
            0.00	2	0	-	255727	              Coriobacterineae
            0.00	2	0	F	84107	                Coriobacteriaceae
            0.00	2	0	G	1380	                  Atopobium
            0.00	2	0	S	1382	                    Atopobium parvulum
            0.00	2	2	-	521095	                      Atopobium parvulum DSM 20469
            0.00	1	0	-	85003	          Actinobacteridae
            0.00	1	0	O	2037	            Actinomycetales
            0.00	1	0	-	85009	              Propionibacterineae
            0.00	1	0	F	31957	                Propionibacteriaceae
            0.00	1	0	G	1743	                  Propionibacterium
            0.00	1	1	S	1747	                    Propionibacterium acnes
            0.00	20	0	D	2157	    Archaea
            0.00	20	7	P	28890	      Euryarchaeota
            0.00	8	0	C	183963	        Halobacteria
            0.00	8	0	O	1644060	          Natrialbales
            0.00	8	0	F	1644061	            Natrialbaceae
            0.00	8	0	G	29287	              Natronococcus
            0.00	8	0	S	29288	                Natronococcus occultus
            0.00	8	8	-	694430	                  Natronococcus occultus SP4
            0.00	4	0	C	224756	        Methanomicrobia
            0.00	4	0	O	94695	          Methanosarcinales
            0.00	4	0	F	2206	            Methanosarcinaceae
            0.00	3	0	G	101191	              Methanomethylovorans
            0.00	3	0	S	101192	                Methanomethylovorans hollandica
            0.00	3	3	-	867904	                  Methanomethylovorans hollandica DSM 15978
            0.00	1	0	G	2207	              Methanosarcina
            0.00	1	0	S	2214	                Methanosarcina acetivorans
            0.00	1	1	-	188937	                  Methanosarcina acetivorans C2A
            0.00	1	0	C	183939	        Methanococci
            0.00	1	0	O	2182	          Methanococcales
            0.00	1	0	F	2183	            Methanococcaceae
            0.00	1	0	G	2184	              Methanococcus
            0.00	1	0	S	2188	                Methanococcus voltae
            0.00	1	1	-	456320	                  Methanococcus voltae A3
            0.00	7	0	D	10239	  Viruses
            0.00	2	0	-	29258	    ssDNA viruses
            0.00	2	0	F	10841	      Microviridae
            0.00	2	0	G	10842	        Microvirus
            0.00	2	2	S	374840	          Enterobacteria phage phiX174 sensu lato
            0.00	2	0	-	35237	    dsDNA viruses, no RNA stage
            0.00	2	0	F	10482	      Polydnaviridae
            0.00	2	0	G	10483	        Ichnovirus
            0.00	2	2	S	265522	          Hyposoter fugitivus ichnovirus
            0.00	2	0	-	439488	    ssRNA viruses
            0.00	2	0	-	35278	      ssRNA positive-strand viruses, no DNA stage
            0.00	2	0	F	11018	        Togaviridae
            0.00	2	0	G	11019	          Alphavirus
            0.00	2	0	-	177872	            VEEV complex
            0.00	2	2	S	11036	              Venezuelan equine encephalitis virus
            """).encode("utf-8")

        # create temp files containing the above kraken results
        tempf_krepA = tempfile.NamedTemporaryFile()
        tempf_krepA.write(self.krepA)

        tempf_krepB = tempfile.NamedTemporaryFile()
        tempf_krepB.write(self.krepB)

        self.fps = [tempf_krepA.name, tempf_krepB.name]
        self.fnames = [osp.split(fp)[1] for fp in self.fps]

        self.sample_counts, self.taxa = kb.process_samples(self.fps,
                                                           max_rank="O",
                                                           min_rank="S")

    def test_sample_ids(self):
        proc_snames = set(self.sample_counts)

        self.assertEqual(proc_snames.symmetric_difference(self.fnames),
                         set())

    def test_sample_counts(self):
        countsA = {'265522': 2, '1382': 2, '11036': 2, '37734': 9,
                   '1747': 1,
                   '374840': 2, '543': 6, '562': 1, '179636': 2,
                   '28108': 10,
                   '12916': 2, '1303': 3, '1308': 1, '135622': 1,
                   '1318': 2,
                   '2188': 1, '2214': 1, '29288': 8, '329': 11,
                   '1301': 8,
                   '101192': 3, '45617': 1, '1305': 1, '1304': 5,
                   '186802': 1, "0": 6783846}
        countsB = {'265522': 2, '1382': 2, '11036': 2, '37734': 9,
                   '1747': 1,
                   '374840': 2, '543': 6, '562': 1, '179636': 2,
                   '28108': 10,
                   '12916': 2, '1303': 3, '1308': 1, '135622': 1,
                   '1318': 2,
                   '2188': 1, '2214': 1, '29288': 8, '329': 11,
                   '1301': 8,
                   '101192': 3, '1305': 1, '1304': 5, '186802': 1,
                   "0": 6783846}

        proc_countsA = self.sample_counts[self.fnames[0]]
        proc_countsB = self.sample_counts[self.fnames[1]]
        print(proc_countsA)
        self.assertTrue(all([countsA[otu_id] == proc_countsA[otu_id]
                             for otu_id in countsA]))
        self.assertTrue(all([countsA[otu_id] == proc_countsA[otu_id]
                             for otu_id in proc_countsA]))

        self.assertTrue(all([countsB[otu_id] == proc_countsB[otu_id]
                             for otu_id in countsB]))
        self.assertTrue(all([countsB[otu_id] == proc_countsB[otu_id]
                             for otu_id in proc_countsB]))

    def test_taxa(self):
        manual = {"1304": ["k__Bacteria", "p__Firmicutes", "c__Bacilli",
                           "o__Lactobacillales", "f__Streptococcaceae",
                           "g__Streptococcus", "s__salivarius"],
                  "29288": ["k__Archaea", "p__Euryarchaeota",
                            "c__Halobacteria",
                            "o__Natrialbales", "f__Natrialbaceae",
                            "g__Natronococcus", "s__occultus"],
                  "45617": ["k__Viruses", "p__", "c__", "o__",
                            "f__Retroviridae",
                            "g__", "s__Human endogenous retrovirus K"],
                  "1301": ["k__Bacteria", "p__Firmicutes", "c__Bacilli",
                           "o__Lactobacillales", "f__Streptococcaceae",
                           "g__Streptococcus", "s__"],
                  "135622": ["k__Bacteria", "p__Proteobacteria",
                             "c__Gammaproteobacteria",
                             "o__Alteromonadales",
                             "f__", "g__", "s__"],
                  "543": ["k__Bacteria", "p__Proteobacteria",
                          "c__Gammaproteobacteria",
                          "o__Enterobacteriales",
                          "f__Enterobacteriaceae", "g__", "s__"],
                  "265522": ["k__Viruses", "p__", "c__", "o__",
                             "f__Polydnaviridae", "g__Ichnovirus",
                             "s__Hyposoter fugitivus ichnovirus"],
                  "374840": ["k__Viruses", "p__", "c__", "o__",
                             "f__Microviridae", "g__Microvirus",
                             "s__Enterobacteria phage phiX174 sensu lato"],
                  "0": ["k__Unclassified", "p__Unclassified",
                        "c__Unclassified", "o__Unclassified",
                        "f__Unclassified", "g__Unclassified",
                        "s__Unclassified"]
                  }

        self.assertTrue(all([manual[tax_id] == self.taxa[tax_id]
                             for tax_id in manual]))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
