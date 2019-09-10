java_path = input('输入java文件路径:\n')
#
with open(java_path, 'w+', encoding='utf-8') as f:
    methods = ''''''
    for i in range(3000):
        methods += '''
        	public void Test''' + str(i) + '''() {
    	}'''
    content = '''
        package com.yy.yy;

    public class LargeMethodCount {
    	''' + methods + '''
    }

        '''
    f.write(content)
