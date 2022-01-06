import ahocorasick


class AcMachine:
    # Aho-Corasick自动机
    def __init__(self, words):
        self.words = words
        self.words_tree = self.build()

    def build(self):
        # 构建所有类型的检索机
        words_tree = ahocorasick.Automaton()
        for idx, val in enumerate(self.words):
            words_tree.add_word(val, (idx, val))
        words_tree.make_automaton()
        return words_tree

    def map_actree(self, sentence) -> list:
        """
        :param self:
        :param word:
        :return:
        """
        result = []
        # for w in self.words_tree.iter(sentence):
        #     if len(w) > 0:
        #         result.append(w[1][1])
        # return result
        for end_index, value in self.words_tree.iter(sentence):
            if len(value) > 0:
                original_value = value[1]
                start_index = end_index - len(original_value) + 1
                result.append({'word': original_value, "start_index": start_index, "end_index": end_index})
        return result

if __name__ == '__main__':
    test_dict = ['测试1','测试2','测试3','测试345','语句1']
    ac_machine = AcMachine(test_dict)
    test_sentence = '测试1测试345语句1xx'
    info = ac_machine.map_actree(test_sentence)
    print(info)