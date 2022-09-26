import os.path

def work_file() -> list:
    '''
    Запускает файловый дескриптор как генератор
    :return: Результат работы программы
    '''
    quary = input('Введите запрос\n')
    with open(os.path.join('isa-func-source', 'data', "apache_logs.txt")) as f:
        work_utlis = utlis(f,quary)
    return work_utlis


def utlis(file, quary: str) -> list:
    '''
    Разбиавает запрос и проверят на соответствия командам и выполняет их при положительном результате
    '''
    quary: list = quary.split('|')
    # Эта строка для того, что бы можно было в запросе делать 2 условия.
    # Из тестов получается что filter всегда должен выполняться первым, иначе все ломается.
    # Не придумал варианта лучше как это исправить
    if 'filter' in quary[1]:
        quary.reverse()
    res: object = map(lambda item: ' '.join((item.replace('- - ', '').replace(' +0000', '').split(' '))[:6]), file)
    for quary_item in quary:
        quary_item: list = quary_item.split(' ')
        quary_item.remove('')
        request: str = quary_item[0]
        arg: str | int = quary_item[1]
        if request == 'filter':
            res: list = list(filter(lambda line: arg in line, res))
        if request == 'map':
            res: list = list(map(lambda line: line.split(' ')[int(arg)], res))
        if request == 'unique':
            res: list = list(set(res))
        if request == 'sort':
            reverse = arg == 'desc'
            res: list = list(sorted(res, reverse=reverse))
        if request == 'limit':
            res: list = list(res)[:int(arg)]
    return list(res)

if __name__ == '__main__':
    print(*work_file(), sep='\n')

