import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime, timedelta

MIN_DATE = datetime(1992, 7, 1)
MAX_DATE = datetime.now()

def get_exchange_rates():
    """
    Получает курсы валют на текущую дату.
    """
    return get_exchange_rates_for_date(datetime.now().strftime('%d.%m.%Y'))

def get_exchange_rates_for_date(date_str):
    """
    Получает курсы валют на указанную дату.
    """
    try:
        date = datetime.strptime(date_str, '%d.%m.%Y')
    except ValueError:
        return None, None

    if date < MIN_DATE or date > MAX_DATE:
        return None, None

    base_url = 'https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To='

    while True:
        url = base_url + date_str
        response = requests.get(url)

        if response.status_code == 200:
            soup = BS(response.text, 'lxml')

            # Ищем таблицу с курсами валют
            rates_table = soup.find('table', class_='data')
            if rates_table:
                rates = []

                for row in rates_table.find_all('tr')[1:]:
                    columns = row.find_all('td')
                    numeric_code = columns[0].text.strip()
                    alphabetic_code = columns[1].text.strip()
                    units = columns[2].text.strip()
                    currency = columns[3].text.strip()
                    rate = columns[4].text.strip()

                    rate = float(rate.replace(',', '.'))

                    rates.append({
                        'Цифр. код': numeric_code,
                        'Букв. код': alphabetic_code,
                        'Единиц': units,
                        'Валюта': currency,
                        'Курс': rate
                    })

                return date_str, rates
            else:
                date -= timedelta(days=1)
                date_str = date.strftime('%d.%m.%Y')
        else:
            date -= timedelta(days=1)
            date_str = date.strftime('%d.%m.%Y')

    return None, None

def format_rates(date_text, rates):
    response = f"Курсы валют на {date_text}:\n\n"
    for rate_info in rates:
        response += f"Букв. код: {rate_info['Букв. код']}\n"
        response += f"Цифр. код: {rate_info['Цифр. код']}\n"
        response += f"Единиц: {rate_info['Единиц']}\n"
        response += f"Валюта: {rate_info['Валюта']}\n"
        response += f"Курс: {rate_info['Курс']} RUB\n\n"
    return response

def search_currency(currency_input, date_text, rates):
    found = False
    response = f"Информация по валюте '{currency_input}' на {date_text}:\n\n"
    for rate_info in rates:
        if currency_input.lower() in rate_info['Букв. код'].lower() or currency_input.lower() in rate_info[
            'Валюта'].lower():
            response += f"Букв. код: {rate_info['Букв. код']}\n"
            response += f"Цифр. код: {rate_info['Цифр. код']}\n"
            response += f"Единиц: {rate_info['Единиц']}\n"
            response += f"Валюта: {rate_info['Валюта']}\n"
            response += f"Курс: {rate_info['Курс']} RUB\n\n"
            found = True
    if not found:
        response = f"Валюта '{currency_input}' не найдена.\n\n"
    return response