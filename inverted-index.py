import re

"""引入函式庫，用於文本匹配和處理"""

class InvertedIndex:
    """ A simple inverted index, as explained in the lecture """
    def __init__(self):
        """ Create an empty inverted index. """
        self.inverted_lists = {}

    def read_from_file(self, file_name):
        """ 從指定的文件中讀取內容並構建反向索引 """
        with open(file_name) as file:
          """用 with 打開文件，確保在退出時文件會被正確關閉，可以避免文件泄露和資源佔用 """
          for doc_id, line in enumerate(file, start=1):
            """掃描文件，使用 enumerate 函數得到id和文本內容，id從 1 開始"""
            self.inverted_lists[doc_id] = line.strip()
            """把要處理的文檔，刪除每行開頭和結尾的空格，讓格式比較好看"""

    def search(self, query):
        """ Search for documents containing all keywords in the query """
        query_regex = r'\b(?:' + '|'.join(re.escape(q) for q in query.split()) + r')\b'
        """在字串前面加上 r'，讓反斜線不會有功能性，使其當成普通字元處理。
        query.split()將輸入的 query 利用空格拆成單個單字。
        \b 表示單詞的邊界，為了確保匹配的是完整的單字，而不是附屬在其他單字裡的部分。
        使用re.escape()，如果q是特殊字元，就會在特殊字符前面加上反斜線，使其能被正確掃描。
        最後，使用 '|'.join()將每個處理後的單字用 | 符號連接起來，形成了一個正規表示式"""
        results = {}
        """ 用來存每行中出現query的次數和highlight後的結果"""
        for _doc_id, line in self.inverted_lists.items():
            """利用id和line(內容)的匹配，看self.inverted_lists中的每一行"""
            matches = re.findall(query_regex, line, flags=re.IGNORECASE)
            """用findall()找到每行 line 中與 query_regex 匹配的所有單詞，會一次性回傳有出現有query的部分陣列，
            並將結果存在矩陣matches裡。flags=re.IGNORECASE 在搜尋時忽略大小寫。"""
            total_count = len(matches)
            if total_count > 0:
                """ 如果query有出現，就跑以下程式碼"""
                highlighted_line = re.sub(query_regex, r'\033[1m\033[91m\g<0>\033[0m', line, flags=re.IGNORECASE)
                """用sub()把highlighted_line文檔中出現query的部分(match)替換成highlight版本，
              \033[1m設為粗體，\033[91m設為紅色"""
                results[highlighted_line] = total_count
                """將有highlight的行作為id，和query出現的總次數作為值，之後加results中"""

        """ 找到query出現次數前三高的行"""
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        """用reverse=True倒序排列"""
        return sorted_results[:3]
    """回傳排序結果的前三元素"""

"""要處理的txt名稱"""
file_name = "movies.txt"
ii = InvertedIndex()
ii.read_from_file(file_name)

while True:
    query = input("輸入要搜索的關鍵字（按 Enter 鍵搜索，按 q 鍵退出）：")
    if query.lower() == 'q':
        break
    search_result = ii.search(query)
    print("Top Three Results:")
    for line, count in search_result:
        print(f"(出現次數: {count}) {line}")
        print('\n')
