from data.cdn.sof_cdn import *
import logging

if __name__ == '__main__':
    count = QuestionsCDN.count(pagesize=100, unit=2000000, fromdate=1483228800, todate=1514764800)
    print(f'uses count {count}')