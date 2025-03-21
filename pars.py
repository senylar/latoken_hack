import requests

with open('links.csv', 'r') as file:
    links = file.read().splitlines()


from bs4 import BeautifulSoup

# URL страницы

# Запрос страницы

def pars_page(url):
    # Проверка успешности запроса
    response = requests.get(url)
    if response.status_code == 200:
        # Парсинг HTML-кода
        soup = BeautifulSoup(response.content, 'html.parser')

        # Находим родительский блок
        root = soup.find(id="document-root-route")

        if root:
            seen_texts = set()  # Для отслеживания уникального текста
            paragraphs = []

            for tag in root.find_all(["div", "h3"]):
                # Пропускаем блоки, в которых есть ссылки
                if tag.find("a", href=True):
                    continue

                paragraph_text = tag.get_text(strip=True, separator=" ")  # Берем текст блока

                if paragraph_text and paragraph_text not in seen_texts:  # Проверяем на дубликаты
                    seen_texts.add(paragraph_text)
                    paragraphs.append(paragraph_text)

            # Собираем текст, разделяя абзацы пустой строкой
            result_text = "\n\n".join(paragraphs[8:])

            with open(f'/Users/gggg/meetup/latoken_hack/kb/{url.split("/")[-1]}.txt', 'a+') as file:
                file.write(result_text)
            print('done for', url)
        else:
            print("Блок #document-root-route не найден.")


for url in links:
    pars_page(url)