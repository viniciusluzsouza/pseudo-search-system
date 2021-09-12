import json
from time import time

DB = './catalogo_produtos.json'
CACHE = {}
LIMIT = 20


def get_products_from_db(word, limit):
    found_products = []
    with open(DB, 'r') as db:
        count = 0
        for line in db:
            product = json.loads(line)
            product_name = product['name'].lower()
            if word in product_name:
                found_products.append((product['id'], product_name))
                count += 1
            
            if count == limit:
                break
    
    # Python uses Timsort algorithm, which is an algorithm
    # derived from merge and insertion sorting algorithm
    # https://wiki.python.org/moin/HowTo/Sorting
    return sorted(found_products, key=lambda i: i[0])


def find_product_by_word(word, limit):
    products = CACHE.get(word, None)

    # If search not in cache, get from DB and keep in memory (CACHE)
    if not products:
        products = get_products_from_db(word, limit)
        CACHE[word] = products
    
    return products


if __name__ == '__main__':
    while True:
        try:
            word = input("Digite aqui sua consulta: ").lower().strip()

            query_start_time = time()
            products = find_product_by_word(word, LIMIT)
            if products:
                i = 1
                for product in products:
                    print('#%d - "%s" - "%s"' % (i, product[0], product[1]))
                    i += 1
            else:
                print("Não foram encontrados produtos para a busca '%s'" % word)

            query_end_time = time()
            query_time = (query_end_time - query_start_time) * 1000     # ms
            print("Tempo de consulta: %.2f ms\n" % query_time)

        except KeyboardInterrupt:
            print()
            break
        except Exception as e:
            print("Falha ao procurar produtos:\n%s" % str(e))
