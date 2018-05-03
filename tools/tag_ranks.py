from analysis.common import *

def get_top_tags(top=100, file_path=r'E:\SOF\file\tag-rank.json'):
    data = load_file(file_path=file_path)[0]
    tags = [(tag, data[tag]) for tag in data]
    tags.sort(key=lambda item: item[1], reverse=True)
    return [item[0] for item in tags[:top]]

if __name__ == '__main__':
    print(get_top_tags(100))