from bot import main

# 这个文件用于 PythonAnywhere 的 WSGI 配置
# 实际运行 bot 时不会用到这个文件
application = None

if __name__ == '__main__':
    main()
