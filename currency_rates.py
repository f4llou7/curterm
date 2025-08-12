import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def get_exchange_rates(date_str=None):
    """
    Получает курсы валют от ЦБ РФ на указанную дату.
    """
    if date_str:
        url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={date_str}"
    else:
        url = "https://www.cbr.ru/scripts/XML_daily.asp"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        
        rates = {}
        for valute in root.findall('Valute'):
            char_code = valute.find('CharCode').text
            if char_code in ['USD', 'EUR']:
                value = float(valute.find('Value').text.replace(',', '.'))
                rates[char_code] = value
        return rates

    except requests.exceptions.RequestException as e:
        print(f"🚨 Ошибка сети: Не удалось получить данные. {e}")
    except ET.ParseError:
        print("🚨 Ошибка: Не удалось разобрать ответ от сервера.")
    except Exception as e:
        print(f"🚨 Произошла непредвиденная ошибка: {e}")
    return None

def compare_and_print_rates():
    """
    Сравнивает курсы валют за сегодня и вчера и выводит результат.
    """
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    
    today_str = today.strftime('%d/%m/%Y')
    yesterday_str = yesterday.strftime('%d/%m/%Y')

    today_rates = get_exchange_rates()
    yesterday_rates = get_exchange_rates(yesterday_str)

    print("🏦 **Курсы валют от ЦБ РФ** 🏦")
    print(f"На {today.strftime('%d.%m.%Y')}")
    print("-----------------------------")

    if today_rates:
        for currency in ['USD', 'EUR']:
            if currency in today_rates:
                today_rate = today_rates[currency]
                yesterday_rate = yesterday_rates.get(currency) if yesterday_rates else None
                
                icon = ""
                if yesterday_rate:
                    if today_rate > yesterday_rate:
                        icon = "↑"
                    elif today_rate < yesterday_rate:
                        icon = "↓"
                
                currency_symbol = "🇺🇸" if currency == 'USD' else "🇪🇺"
                print(f"{currency_symbol} {currency}: {today_rate:.2f} руб. {icon}")
            else:
                print(f"Курс {currency} не найден.")
    else:
        print("Не удалось получить сегодняшний курс.")
        
    print("-----------------------------")


if __name__ == "__main__":
    compare_and_print_rates()