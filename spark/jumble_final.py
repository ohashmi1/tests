#!/usr/bin/python -u

from pyspark import SparkConf, SparkContext
import ast

class JumbleSolver():
      
    def __init__(self,dic_path, scrambled_file):
        self.dic_path = dic_path
        self.scrambled_file = scrambled_file
        
        self.table = {}
        self.sorted_table ={}
        self.jumble_words = list()
        self.solve_rdd = None

    def read_anagram_into_rdd(self):
        
        #create a spark contect and read the puzzles into a rdd
        conf=SparkConf().setMaster("local[4]").setAppName("Jumble Solver")
        sc=SparkContext(conf=conf)
        rdd=sc.textFile(self.scrambled_file)
        self.solve_rdd = rdd.map(lambda x: [ast.literal_eval(x)])
        self.parse_anagram_rdd()
        sc.stop()
        
        
    def parse_anagram_rdd(self):
        # extract a single record from the puzzles and solve them
        list_of_records = self.solve_rdd.collect()
        #print(problems[0])
        for records in list_of_records:
            for record in records:
                print("\n*******")
                print("New Record")
                self.solve_each_anagram(record)
                print("*******")

    def populate_jumble(self,x):
        d = ast.literal_eval(x)
        return d

            
    def solve_each_anagram(self,record):
        # final string info
        final_str = record['str']
        final_str_text = final_str['sentence']
        final_str_lengths = final_str['lengths'].split(' ')
        
        #jumbled words info:
        words = record['words']
        possible_words = []
        found_words = []
        
        #var for possible strings that can be made with indices of real words
        p_str = ""
        # get all the real words that can be made from scrambled letters
     
        for k, v in words.iteritems():
            a = "".join(sorted(k))
            w_len = v.split(' ')
            # find real words from the dictionary after sorting the scrambled word
            if self.table.get(len(a)):
                found_words = self.table[len(a)]
                for w in found_words.keys():
                    if(w == a):
                        real_word = (found_words[a])[0].split(':')[0].strip().replace('"', '').lower()
                        print('{} was unscrambled to real word {}'.format(k.upper(),real_word.upper()))
                        for i in w_len:
                            p_str += real_word[int(i)]

                        
        print("Resultant string after getting chars at indices {}".format(p_str.upper()))
        possible_words.append(p_str) 
        #get the final answer from chars that were combined from real words to create a new jumble
        self.find_final_anagram(possible_words, final_str_text, final_str_lengths)

    def _get_sorted_key_value(self,x):
        a = ''.join(sorted(x.split(':')[0].strip().replace('"', '').lower()))
        return a,x 
      
    def create_dic_with_sorted_words_as_keys(self):
        '''
        Creates a dictionary {len(word):{sortedword:[words]} into a RDD so we 
        can look up words by their lengths
        '''
        
        conf=SparkConf().setMaster("local[4]").setAppName("Jumble Solver")
        sc=SparkContext(conf=conf)
        rdd=sc.textFile(self.dic_path)
        x =  (rdd
        .map(lambda x: self._get_sorted_key_value(x) )
        .groupByKey()
        .mapValues(lambda x: list(x))
        .map(lambda x: (len(x[0]), x))
        .groupByKey()
        .mapValues(lambda x: dict(x))
        .collectAsMap())
        #set the table to the rdd
        self.table = x
       
        sc.stop()


    def Solve(self):
        '''
        It first creates a dictionary as {len(word):{sortedword:[words]} and it then 
        reads each jumble into the rdd and solves it
        '''
        
        self.create_dic_with_sorted_words_as_keys()
        self.read_anagram_into_rdd()
       
    def find_final_anagram(self,target,final_str_text,str_lens):
        '''
        Finds the final answer that can be formed from the target string.
        target = jumbled chars
        final_str_text = final string with found words appended to the original string
        str_len = list of length of words that needs to be found
        '''
        target = "".join(sorted("".join(target)))
        sum_list = sum(int(i) for i in str_lens)
        if len(target) < sum_list: print('No Solution found')
        str_list = []
       
        for i in str_lens:
            str_list.append(target[:int(i)])
            target = target[int(i):]
        answer = ''
        for s in str_list:
            if len(s) > 0:
                dic = self.table[len(s)]
                if dic.get(s): answer += " "+ ((dic[s])[0]).split(':')[0].strip() 
                    
        print(final_str_text + answer)
        
if __name__ == '__main__':
    '''
    Creates a Jumble Solver Object and solves the puzzles
    '''
    import sys
    print(sys.version)
    jumble = JumbleSolver('freq_dict.json','jumble.json')
    jumble.Solve()
    
