import datetime
import json
import aiohttp
import asyncio
import tracemalloc

tracemalloc.start()

current_date = datetime.datetime.now().strftime('%m-%d')

# Асинхронный запрос для получения всех категорий
async def all_cat_str():
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en;q=0.9',
        'origin': 'https://5ka.ru',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "YaBrowser";v="24.10", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36',
        'x-app-version': '0.1.1.dev',
        'x-device-id': 'f0e53491-22d8-4a84-96ec-fb1f296f9acb',
        'x-platform': 'webapp',
    }

    params = {
        'mode': 'delivery',
        'include_subcategories': '1',
    }

    async with aiohttp.ClientSession() as session:
        async with session.get('https://5d.5ka.ru/api/catalog/v1/stores/326L/categories', params=params, headers=headers) as response:
            return await response.json()

# Асинхронная функция для извлечения id категорий
def cat_id(file):
    all_cat = []
    for cat in file:
        all_cat.append({"id": cat["id"], "name": cat["name"]})
    return json.dumps(all_cat, ensure_ascii=False, indent=4)

# Асинхронная функция для извлечения подкатегорий по id
def subcats(file, cat):
    subcat = []
    for item in file:
        if item['id'] == cat:
            for sub in item['subcategories']:
                subcat.append({"id": sub["id"], "name": sub["name"]})
    return json.dumps(subcat, ensure_ascii=False, indent=4)

# Асинхронная функция для получения товаров из подкатегории
async def items(subcat):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en;q=0.9',
        'origin': 'https://5ka.ru',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "YaBrowser";v="24.10", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36',
        'x-app-version': '0.1.1.dev',
        'x-device-id': 'f0e53491-22d8-4a84-96ec-fb1f296f9acb',
        'x-platform': 'webapp',
    }

    params = {
        'mode': 'delivery',
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://5d.5ka.ru/api/catalog/v1/stores/326L/categories/{subcat}/products",
            params=params,
            headers=headers
        ) as response:
            result = await response.json()

    items = []
    foto_url = []
    for item in result["products"]:
        if item['prices']['discount'] is not None:
            items.append(f"Наименование: {item['name']} Цена: {item['prices']['regular']} Цена по акции: {item['prices']['discount']}")
            foto_url.append(item["image_links"]["small"])
            print(f"Наименование: {item['name']} Цена: {item['prices']['regular']} Цена по акции: {item['prices']['discount']}")

    if items:
        print(foto_url)
        print(items)
        return items, foto_url
    else:
        return "Нету товара по акции в данной категории"

# Главная асинхронная функция для запуска
async def main():
    file = await all_cat_str()
    cat = cat_id(file)
    print(cat)

    # Пример получения подкатегорий
    subcat = input("Введите ID категории для получения подкатегорий: ")
    print(subcats(file, subcat))

    # Пример получения товаров из подкатегории
    subcat = input("Введите ID подкатегории для получения товаров: ")
    await items(subcat)

# Запуск программы
if __name__ == '__main__':
    asyncio.run(main())