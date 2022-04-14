def tap(func):
    def resFunc(data):
        func(data)
        return data
    return resFunc    

def trans(func):
    def resFunc(data):
        return func(data)
    return resFunc    

def pipe(*funcs):
    def execute(data):
        result = data
        for i in range(0, len(funcs)):
            result = funcs[i](result)
        return result
    return execute