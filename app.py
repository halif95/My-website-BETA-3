from flask import Flask, render_template, request
import urllib.parse

app = Flask(__name__)

# helper: формирует ссылку поиска на DNS
def dns_search(name):
    return "https://www.dns-shop.ru/search/?q=" + urllib.parse.quote_plus(name)

# регистрируем фильтр Jinja
app.jinja_env.filters['dns_search'] = dns_search

# Полная база данных комплектующих
components_data = {
    'gpu': {
        # Новейшие RTX 40 series
        'NVIDIA RTX 4090': {'brand': 'NVIDIA', 'model': 'RTX 4090', 'vram': 24, 'memory_type': 'GDDR6X', 'bus_width': 384, 'price': 200000, 'rating': 5, 'release_year': 2022},
        'NVIDIA RTX 4080 Super': {'brand': 'NVIDIA', 'model': 'RTX 4080 Super', 'vram': 16, 'memory_type': 'GDDR6X', 'bus_width': 256, 'price': 130000, 'rating': 5, 'release_year': 2024},
        'NVIDIA RTX 4080': {'brand': 'NVIDIA', 'model': 'RTX 4080', 'vram': 16, 'memory_type': 'GDDR6X', 'bus_width': 256, 'price': 120000, 'rating': 4, 'release_year': 2022},
        'NVIDIA RTX 4070 Ti Super': {'brand': 'NVIDIA', 'model': 'RTX 4070 Ti Super', 'vram': 16, 'memory_type': 'GDDR6X', 'bus_width': 256, 'price': 95000, 'rating': 4, 'release_year': 2024},
        'NVIDIA RTX 4070 Ti': {'brand': 'NVIDIA', 'model': 'RTX 4070 Ti', 'vram': 12, 'memory_type': 'GDDR6X', 'bus_width': 192, 'price': 90000, 'rating': 4, 'release_year': 2023},
        'NVIDIA RTX 4070 Super': {'brand': 'NVIDIA', 'model': 'RTX 4070 Super', 'vram': 12, 'memory_type': 'GDDR6X', 'bus_width': 192, 'price': 85000, 'rating': 4, 'release_year': 2024},
        'NVIDIA RTX 4070': {'brand': 'NVIDIA', 'model': 'RTX 4070', 'vram': 12, 'memory_type': 'GDDR6X', 'bus_width': 192, 'price': 80000, 'rating': 4, 'release_year': 2023},
        'NVIDIA RTX 4060 Ti': {'brand': 'NVIDIA', 'model': 'RTX 4060 Ti', 'vram': 8, 'memory_type': 'GDDR6', 'bus_width': 128, 'price': 50000, 'rating': 3, 'release_year': 2023},
        'NVIDIA RTX 4060': {'brand': 'NVIDIA', 'model': 'RTX 4060', 'vram': 8, 'memory_type': 'GDDR6', 'bus_width': 128, 'price': 40000, 'rating': 3, 'release_year': 2023},
        
        # RTX 30 series
        'NVIDIA RTX 3090 Ti': {'brand': 'NVIDIA', 'model': 'RTX 3090 Ti', 'vram': 24, 'memory_type': 'GDDR6X', 'bus_width': 384, 'price': 180000, 'rating': 5, 'release_year': 2022},
        'NVIDIA RTX 3090': {'brand': 'NVIDIA', 'model': 'RTX 3090', 'vram': 24, 'memory_type': 'GDDR6X', 'bus_width': 384, 'price': 160000, 'rating': 5, 'release_year': 2020},
        'NVIDIA RTX 3080 Ti': {'brand': 'NVIDIA', 'model': 'RTX 3080 Ti', 'vram': 12, 'memory_type': 'GDDR6X', 'bus_width': 384, 'price': 110000, 'rating': 4, 'release_year': 2021},
        'NVIDIA RTX 3080': {'brand': 'NVIDIA', 'model': 'RTX 3080', 'vram': 10, 'memory_type': 'GDDR6X', 'bus_width': 320, 'price': 90000, 'rating': 4, 'release_year': 2020},
        'NVIDIA RTX 3070 Ti': {'brand': 'NVIDIA', 'model': 'RTX 3070 Ti', 'vram': 8, 'memory_type': 'GDDR6X', 'bus_width': 256, 'price': 70000, 'rating': 4, 'release_year': 2021},
        'NVIDIA RTX 3070': {'brand': 'NVIDIA', 'model': 'RTX 3070', 'vram': 8, 'memory_type': 'GDDR6', 'bus_width': 256, 'price': 60000, 'rating': 4, 'release_year': 2020},
        'NVIDIA RTX 3060 Ti': {'brand': 'NVIDIA', 'model': 'RTX 3060 Ti', 'vram': 8, 'memory_type': 'GDDR6', 'bus_width': 256, 'price': 45000, 'rating': 4, 'release_year': 2020},
        'NVIDIA RTX 3060': {'brand': 'NVIDIA', 'model': 'RTX 3060', 'vram': 12, 'memory_type': 'GDDR6', 'bus_width': 192, 'price': 35000, 'rating': 3, 'release_year': 2021},
        
        # RTX 20 series
        'NVIDIA RTX 2080 Ti': {'brand': 'NVIDIA', 'model': 'RTX 2080 Ti', 'vram': 11, 'memory_type': 'GDDR6', 'bus_width': 352, 'price': 80000, 'rating': 4, 'release_year': 2018},
        'NVIDIA RTX 2080 Super': {'brand': 'NVIDIA', 'model': 'RTX 2080 Super', 'vram': 8, 'memory_type': 'GDDR6', 'bus_width': 256, 'price': 60000, 'rating': 4, 'release_year': 2019},
        'NVIDIA RTX 2080': {'brand': 'NVIDIA', 'model': 'RTX 2080', 'vram': 8, 'memory_type': 'GDDR6', 'bus_width': 256, 'price': 55000, 'rating': 3, 'release_year': 2018},
        'NVIDIA RTX 2070 Super': {'brand': 'NVIDIA', 'model': 'RTX 2070 Super', 'vram': 8, 'memory_type': 'GDDR6', 'bus_width': 256, 'price': 50000, 'rating': 3, 'release_year': 2019},
        'NVIDIA RTX 2070': {'brand': 'NVIDIA', 'model': 'RTX 2070', 'vram': 8, 'memory_type': 'GDDR6', 'bus_width': 256, 'price': 45000, 'rating': 3, 'release_year': 2018},
        'NVIDIA RTX 2060 Super': {'brand': 'NVIDIA', 'model': 'RTX 2060 Super', 'vram': 8, 'memory_type': 'GDDR6', 'bus_width': 256, 'price': 40000, 'rating': 3, 'release_year': 2019},
        'NVIDIA RTX 2060': {'brand': 'NVIDIA', 'model': 'RTX 2060', 'vram': 6, 'memory_type': 'GDDR6', 'bus_width': 192, 'price': 35000, 'rating': 3, 'release_year': 2019},
        
        # GTX 16 series
        'NVIDIA GTX 1660 Ti': {'brand': 'NVIDIA', 'model': 'GTX 1660 Ti', 'vram': 6, 'memory_type': 'GDDR6', 'bus_width': 192, 'price': 25000, 'rating': 3, 'release_year': 2019},
        'NVIDIA GTX 1660 Super': {'brand': 'NVIDIA', 'model': 'GTX 1660 Super', 'vram': 6, 'memory_type': 'GDDR6', 'bus_width': 192, 'price': 23000, 'rating': 3, 'release_year': 2019},
        'NVIDIA GTX 1660': {'brand': 'NVIDIA', 'model': 'GTX 1660', 'vram': 6, 'memory_type': 'GDDR5', 'bus_width': 192, 'price': 22000, 'rating': 3, 'release_year': 2019},
        'NVIDIA GTX 1650 Super': {'brand': 'NVIDIA', 'model': 'GTX 1650 Super', 'vram': 4, 'memory_type': 'GDDR6', 'bus_width': 128, 'price': 18000, 'rating': 2, 'release_year': 2019},
        'NVIDIA GTX 1650': {'brand': 'NVIDIA', 'model': 'GTX 1650', 'vram': 4, 'memory_type': 'GDDR5', 'bus_width': 128, 'price': 15000, 'rating': 2, 'release_year': 2019},
        
        # Старые GTX серии
        'NVIDIA GTX 1080 Ti': {'brand': 'NVIDIA', 'model': 'GTX 1080 Ti', 'vram': 11, 'memory_type': 'GDDR5X', 'bus_width': 352, 'price': 40000, 'rating': 4, 'release_year': 2017},
        'NVIDIA GTX 1080': {'brand': 'NVIDIA', 'model': 'GTX 1080', 'vram': 8, 'memory_type': 'GDDR5X', 'bus_width': 256, 'price': 30000, 'rating': 3, 'release_year': 2016},
        'NVIDIA GTX 1070 Ti': {'brand': 'NVIDIA', 'model': 'GTX 1070 Ti', 'vram': 8, 'memory_type': 'GDDR5', 'bus_width': 256, 'price': 28000, 'rating': 3, 'release_year': 2017},
        'NVIDIA GTX 1070': {'brand': 'NVIDIA', 'model': 'GTX 1070', 'vram': 8, 'memory_type': 'GDDR5', 'bus_width': 256, 'price': 25000, 'rating': 3, 'release_year': 2016},
        'NVIDIA GTX 1060': {'brand': 'NVIDIA', 'model': 'GTX 1060', 'vram': 6, 'memory_type': 'GDDR5', 'bus_width': 192, 'price': 20000, 'rating': 3, 'release_year': 2016},
        
        # AMD видеокарты
        'AMD RX 7900 XTX': {'brand': 'AMD', 'model': 'RX 7900 XTX', 'vram': 24, 'memory_type': 'GDDR6', 'bus_width': 384, 'price': 110000, 'rating': 4, 'release_year': 2022},
        'AMD RX 7900 XT': {'brand': 'AMD', 'model': 'RX 7900 XT', 'vram': 20, 'memory_type': 'GDDR6', 'bus_width': 320, 'price': 95000, 'rating': 4, 'release_year': 2022},
        'AMD RX 7800 XT': {'brand': 'AMD', 'model': 'RX 7800 XT', 'vram': 16, 'memory_type': 'GDDR6', 'bus_width': 256, 'price': 70000, 'rating': 4, 'release_year': 2023},
        'AMD RX 7700 XT': {'brand': 'AMD', 'model': 'RX 7700 XT', 'vram': 12, 'memory_type': 'GDDR6', 'bus_width': 192, 'price': 55000, 'rating': 3, 'release_year': 2023},
        'AMD RX 7600': {'brand': 'AMD', 'model': 'RX 7600', 'vram': 8, 'memory_type': 'GDDR6', 'bus_width': 128, 'price': 35000, 'rating': 3, 'release_year': 2023},
        'AMD RX 6950 XT': {'brand': 'AMD', 'model': 'RX 6950 XT', 'vram': 16, 'memory_type': 'GDDR6', 'bus_width': 256, 'price': 80000, 'rating': 4, 'release_year': 2022},
        'AMD RX 6800 XT': {'brand': 'AMD', 'model': 'RX 6800 XT', 'vram': 16, 'memory_type': 'GDDR6', 'bus_width': 256, 'price': 70000, 'rating': 4, 'release_year': 2020},
        'AMD RX 6700 XT': {'brand': 'AMD', 'model': 'RX 6700 XT', 'vram': 12, 'memory_type': 'GDDR6', 'bus_width': 192, 'price': 50000, 'rating': 4, 'release_year': 2021},
        'AMD RX 6600 XT': {'brand': 'AMD', 'model': 'RX 6600 XT', 'vram': 8, 'memory_type': 'GDDR6', 'bus_width': 128, 'price': 35000, 'rating': 3, 'release_year': 2021},
    },
    'cpu': {
        # Intel Core 14-го поколения (Raptor Lake Refresh)
        'Intel Core i9-14900KS': {'brand': 'Intel', 'model': 'Core i9-14900KS', 'cores': 24, 'threads': 32, 'frequency': 6.2, 'socket': 'LGA1700', 'price': 75000, 'rating': 5, 'release_year': 2024},
        'Intel Core i9-14900K': {'brand': 'Intel', 'model': 'Core i9-14900K', 'cores': 24, 'threads': 32, 'frequency': 6.0, 'socket': 'LGA1700', 'price': 65000, 'rating': 5, 'release_year': 2023},
        'Intel Core i7-14700K': {'brand': 'Intel', 'model': 'Core i7-14700K', 'cores': 20, 'threads': 28, 'frequency': 5.6, 'socket': 'LGA1700', 'price': 50000, 'rating': 5, 'release_year': 2023},
        'Intel Core i5-14600K': {'brand': 'Intel', 'model': 'Core i5-14600K', 'cores': 14, 'threads': 20, 'frequency': 5.3, 'socket': 'LGA1700', 'price': 35000, 'rating': 4, 'release_year': 2023},
        
        # Intel Core 13-го поколения (Raptor Lake)
        'Intel Core i9-13900KS': {'brand': 'Intel', 'model': 'Core i9-13900KS', 'cores': 24, 'threads': 32, 'frequency': 6.0, 'socket': 'LGA1700', 'price': 70000, 'rating': 5, 'release_year': 2023},
        'Intel Core i9-13900K': {'brand': 'Intel', 'model': 'Core i9-13900K', 'cores': 24, 'threads': 32, 'frequency': 5.8, 'socket': 'LGA1700', 'price': 60000, 'rating': 5, 'release_year': 2022},
        'Intel Core i7-13700K': {'brand': 'Intel', 'model': 'Core i7-13700K', 'cores': 16, 'threads': 24, 'frequency': 5.4, 'socket': 'LGA1700', 'price': 45000, 'rating': 4, 'release_year': 2022},
        'Intel Core i5-13600K': {'brand': 'Intel', 'model': 'Core i5-13600K', 'cores': 14, 'threads': 20, 'frequency': 5.1, 'socket': 'LGA1700', 'price': 32000, 'rating': 4, 'release_year': 2022},
        
        # Intel Core 12-го поколения (Alder Lake)
        'Intel Core i9-12900KS': {'brand': 'Intel', 'model': 'Core i9-12900KS', 'cores': 16, 'threads': 24, 'frequency': 5.5, 'socket': 'LGA1700', 'price': 55000, 'rating': 5, 'release_year': 2022},
        'Intel Core i9-12900K': {'brand': 'Intel', 'model': 'Core i9-12900K', 'cores': 16, 'threads': 24, 'frequency': 5.2, 'socket': 'LGA1700', 'price': 50000, 'rating': 4, 'release_year': 2021},
        'Intel Core i7-12700K': {'brand': 'Intel', 'model': 'Core i7-12700K', 'cores': 12, 'threads': 20, 'frequency': 5.0, 'socket': 'LGA1700', 'price': 38000, 'rating': 4, 'release_year': 2021},
        'Intel Core i5-12600K': {'brand': 'Intel', 'model': 'Core i5-12600K', 'cores': 10, 'threads': 16, 'frequency': 4.9, 'socket': 'LGA1700', 'price': 28000, 'rating': 4, 'release_year': 2021},
        
        # Intel Core 11-го поколения (Rocket Lake)
        'Intel Core i9-11900K': {'brand': 'Intel', 'model': 'Core i9-11900K', 'cores': 8, 'threads': 16, 'frequency': 5.3, 'socket': 'LGA1200', 'price': 40000, 'rating': 4, 'release_year': 2021},
        'Intel Core i7-11700K': {'brand': 'Intel', 'model': 'Core i7-11700K', 'cores': 8, 'threads': 16, 'frequency': 5.0, 'socket': 'LGA1200', 'price': 32000, 'rating': 4, 'release_year': 2021},
        'Intel Core i5-11600K': {'brand': 'Intel', 'model': 'Core i5-11600K', 'cores': 6, 'threads': 12, 'frequency': 4.9, 'socket': 'LGA1200', 'price': 25000, 'rating': 3, 'release_year': 2021},
        
        # Intel Core 10-го поколения (Comet Lake)
        'Intel Core i9-10900K': {'brand': 'Intel', 'model': 'Core i9-10900K', 'cores': 10, 'threads': 20, 'frequency': 5.3, 'socket': 'LGA1200', 'price': 38000, 'rating': 4, 'release_year': 2020},
        'Intel Core i7-10700K': {'brand': 'Intel', 'model': 'Core i7-10700K', 'cores': 8, 'threads': 16, 'frequency': 5.1, 'socket': 'LGA1200', 'price': 30000, 'rating': 4, 'release_year': 2020},
        'Intel Core i5-10600K': {'brand': 'Intel', 'model': 'Core i5-10600K', 'cores': 6, 'threads': 12, 'frequency': 4.8, 'socket': 'LGA1200', 'price': 22000, 'rating': 3, 'release_year': 2020},
        
        # Бюджетные процессоры Intel
        'Intel Core i3-10100': {'brand': 'Intel', 'model': 'Core i3-10100', 'cores': 4, 'threads': 8, 'frequency': 4.3, 'socket': 'LGA1200', 'price': 12000, 'rating': 3, 'release_year': 2020},
        'Intel Pentium Gold G6400': {'brand': 'Intel', 'model': 'Pentium Gold G6400', 'cores': 2, 'threads': 4, 'frequency': 4.0, 'socket': 'LGA1200', 'price': 7000, 'rating': 2, 'release_year': 2020},
        'Intel Celeron G5900': {'brand': 'Intel', 'model': 'Celeron G5900', 'cores': 2, 'threads': 2, 'frequency': 3.4, 'socket': 'LGA1200', 'price': 5000, 'rating': 2, 'release_year': 2020},
        
        # Старые поколения Intel
        'Intel Core i7-9700K': {'brand': 'Intel', 'model': 'Core i7-9700K', 'cores': 8, 'threads': 8, 'frequency': 4.9, 'socket': 'LGA1151', 'price': 25000, 'rating': 4, 'release_year': 2018},
        'Intel Core i5-9600K': {'brand': 'Intel', 'model': 'Core i5-9600K', 'cores': 6, 'threads': 6, 'frequency': 4.6, 'socket': 'LGA1151', 'price': 18000, 'rating': 3, 'release_year': 2018},
        'Intel Core i7-8700K': {'brand': 'Intel', 'model': 'Core i7-8700K', 'cores': 6, 'threads': 12, 'frequency': 4.7, 'socket': 'LGA1151', 'price': 22000, 'rating': 4, 'release_year': 2017},
        
        # Серверные процессоры Intel
        'Intel Xeon W-3375': {'brand': 'Intel', 'model': 'Xeon W-3375', 'cores': 38, 'threads': 76, 'frequency': 4.0, 'socket': 'LGA4189', 'price': 450000, 'rating': 5, 'release_year': 2021},
        'Intel Xeon Platinum 8380': {'brand': 'Intel', 'model': 'Xeon Platinum 8380', 'cores': 40, 'threads': 80, 'frequency': 3.4, 'socket': 'LGA4189', 'price': 500000, 'rating': 5, 'release_year': 2021},
        
        # AMD Ryzen 7000 series
        'AMD Ryzen 9 7950X3D': {'brand': 'AMD', 'model': 'Ryzen 9 7950X3D', 'cores': 16, 'threads': 32, 'frequency': 5.7, 'socket': 'AM5', 'price': 70000, 'rating': 5, 'release_year': 2023},
        'AMD Ryzen 9 7950X': {'brand': 'AMD', 'model': 'Ryzen 9 7950X', 'cores': 16, 'threads': 32, 'frequency': 5.7, 'socket': 'AM5', 'price': 65000, 'rating': 5, 'release_year': 2022},
        'AMD Ryzen 9 7900X': {'brand': 'AMD', 'model': 'Ryzen 9 7900X', 'cores': 12, 'threads': 24, 'frequency': 5.6, 'socket': 'AM5', 'price': 50000, 'rating': 4, 'release_year': 2022},
        'AMD Ryzen 7 7800X3D': {'brand': 'AMD', 'model': 'Ryzen 7 7800X3D', 'cores': 8, 'threads': 16, 'frequency': 5.0, 'socket': 'AM5', 'price': 40000, 'rating': 4, 'release_year': 2023},
        'AMD Ryzen 7 7700X': {'brand': 'AMD', 'model': 'Ryzen 7 7700X', 'cores': 8, 'threads': 16, 'frequency': 5.4, 'socket': 'AM5', 'price': 35000, 'rating': 4, 'release_year': 2022},
        'AMD Ryzen 5 7600X': {'brand': 'AMD', 'model': 'Ryzen 5 7600X', 'cores': 6, 'threads': 12, 'frequency': 5.3, 'socket': 'AM5', 'price': 28000, 'rating': 4, 'release_year': 2022},
        
        # AMD Ryzen 5000 series
        'AMD Ryzen 9 5950X': {'brand': 'AMD', 'model': 'Ryzen 9 5950X', 'cores': 16, 'threads': 32, 'frequency': 4.9, 'socket': 'AM4', 'price': 55000, 'rating': 5, 'release_year': 2020},
        'AMD Ryzen 9 5900X': {'brand': 'AMD', 'model': 'Ryzen 9 5900X', 'cores': 12, 'threads': 24, 'frequency': 4.8, 'socket': 'AM4', 'price': 45000, 'rating': 5, 'release_year': 2020},
        'AMD Ryzen 7 5800X3D': {'brand': 'AMD', 'model': 'Ryzen 7 5800X3D', 'cores': 8, 'threads': 16, 'frequency': 4.5, 'socket': 'AM4', 'price': 35000, 'rating': 5, 'release_year': 2022},
        'AMD Ryzen 7 5800X': {'brand': 'AMD', 'model': 'Ryzen 7 5800X', 'cores': 8, 'threads': 16, 'frequency': 4.7, 'socket': 'AM4', 'price': 30000, 'rating': 4, 'release_year': 2020},
        'AMD Ryzen 5 5600X': {'brand': 'AMD', 'model': 'Ryzen 5 5600X', 'cores': 6, 'threads': 12, 'frequency': 4.6, 'socket': 'AM4', 'price': 22000, 'rating': 4, 'release_year': 2020},
        
        # Старые поколения AMD Ryzen
        'AMD Ryzen 9 3950X': {'brand': 'AMD', 'model': 'Ryzen 9 3950X', 'cores': 16, 'threads': 32, 'frequency': 4.7, 'socket': 'AM4', 'price': 45000, 'rating': 5, 'release_year': 2019},
        'AMD Ryzen 7 3700X': {'brand': 'AMD', 'model': 'Ryzen 7 3700X', 'cores': 8, 'threads': 16, 'frequency': 4.4, 'socket': 'AM4', 'price': 25000, 'rating': 4, 'release_year': 2019},
        'AMD Ryzen 5 3600': {'brand': 'AMD', 'model': 'Ryzen 5 3600', 'cores': 6, 'threads': 12, 'frequency': 4.2, 'socket': 'AM4', 'price': 18000, 'rating': 4, 'release_year': 2019},
        
        # Процессоры AMD Threadripper
        'AMD Threadripper Pro 5995WX': {'brand': 'AMD', 'model': 'Threadripper Pro 5995WX', 'cores': 64, 'threads': 128, 'frequency': 4.5, 'socket': 'sWRX8', 'price': 550000, 'rating': 5, 'release_year': 2022},
        'AMD Threadripper 3990X': {'brand': 'AMD', 'model': 'Threadripper 3990X', 'cores': 64, 'threads': 128, 'frequency': 4.3, 'socket': 'sTRX4', 'price': 350000, 'rating': 5, 'release_year': 2020},
        'AMD Threadripper 3970X': {'brand': 'AMD', 'model': 'Threadripper 3970X', 'cores': 32, 'threads': 64, 'frequency': 4.5, 'socket': 'sTRX4', 'price': 200000, 'rating': 5, 'release_year': 2019},
        
        # Серверные процессоры AMD EPYC
        'AMD EPYC 9654': {'brand': 'AMD', 'model': 'EPYC 9654', 'cores': 96, 'threads': 192, 'frequency': 3.7, 'socket': 'SP5', 'price': 850000, 'rating': 5, 'release_year': 2022},
        'AMD EPYC 7773X': {'brand': 'AMD', 'model': 'EPYC 7773X', 'cores': 64, 'threads': 128, 'frequency': 3.5, 'socket': 'SP3', 'price': 600000, 'rating': 5, 'release_year': 2021},
    },
    'ram': {
        # Оперативная память DDR5
        'G.Skill Trident Z5 RGB 64GB': {'brand': 'G.Skill', 'model': 'Trident Z5 RGB', 'size': 64, 'type': 'DDR5', 'frequency': 6000, 'timing': 'CL30', 'price': 28000, 'rating': 5, 'release_year': 2023},
        'G.Skill Trident Z5 RGB 32GB': {'brand': 'G.Skill', 'model': 'Trident Z5 RGB', 'size': 32, 'type': 'DDR5', 'frequency': 6000, 'timing': 'CL36', 'price': 15000, 'rating': 5, 'release_year': 2022},
        'G.Skill Trident Z5 RGB 16GB': {'brand': 'G.Skill', 'model': 'Trident Z5 RGB', 'size': 16, 'type': 'DDR5', 'frequency': 6000, 'timing': 'CL36', 'price': 8000, 'rating': 4, 'release_year': 2022},
        
        'Kingston Fury Beast 64GB': {'brand': 'Kingston', 'model': 'Fury Beast', 'size': 64, 'type': 'DDR5', 'frequency': 5600, 'timing': 'CL40', 'price': 25000, 'rating': 5, 'release_year': 2023},
        'Kingston Fury Beast 32GB': {'brand': 'Kingston', 'model': 'Fury Beast', 'size': 32, 'type': 'DDR5', 'frequency': 5600, 'timing': 'CL40', 'price': 12000, 'rating': 4, 'release_year': 2022},
        'Kingston Fury Beast 16GB': {'brand': 'Kingston', 'model': 'Fury Beast', 'size': 16, 'type': 'DDR5', 'frequency': 5600, 'timing': 'CL40', 'price': 6000, 'rating': 4, 'release_year': 2022},
        
        'Teamgroup T-Force Delta 32GB': {'brand': 'Teamgroup', 'model': 'T-Force Delta', 'size': 32, 'type': 'DDR5', 'frequency': 6000, 'timing': 'CL38', 'price': 11000, 'rating': 4, 'release_year': 2022},
        'Teamgroup T-Force Delta 16GB': {'brand': 'Teamgroup', 'model': 'T-Force Delta', 'size': 16, 'type': 'DDR5', 'frequency': 6000, 'timing': 'CL38', 'price': 5500, 'rating': 4, 'release_year': 2022},
        
        'ADATA XPG Lancer 32GB': {'brand': 'ADATA', 'model': 'XPG Lancer', 'size': 32, 'type': 'DDR5', 'frequency': 5200, 'timing': 'CL38', 'price': 13000, 'rating': 4, 'release_year': 2022},
        'ADATA XPG Lancer 16GB': {'brand': 'ADATA', 'model': 'XPG Lancer', 'size': 16, 'type': 'DDR5', 'frequency': 5200, 'timing': 'CL38', 'price': 6500, 'rating': 4, 'release_year': 2022},
        
        # Оперативная память DDR4
        'G.Skill Trident Z Neo 32GB': {'brand': 'G.Skill', 'model': 'Trident Z Neo', 'size': 32, 'type': 'DDR4', 'frequency': 3600, 'timing': 'CL16', 'price': 10000, 'rating': 5, 'release_year': 2020},
        'G.Skill Trident Z RGB 16GB': {'brand': 'G.Skill', 'model': 'Trident Z RGB', 'size': 16, 'type': 'DDR4', 'frequency': 3600, 'timing': 'CL18', 'price': 6000, 'rating': 4, 'release_year': 2019},
        
        'Kingston Fury Renegade 32GB': {'brand': 'Kingston', 'model': 'Fury Renegade', 'size': 32, 'type': 'DDR4', 'frequency': 3600, 'timing': 'CL16', 'price': 9000, 'rating': 4, 'release_year': 2021},
        'Kingston HyperX Predator 16GB': {'brand': 'Kingston', 'model': 'HyperX Predator', 'size': 16, 'type': 'DDR4', 'frequency': 3200, 'timing': 'CL16', 'price': 5000, 'rating': 4, 'release_year': 2018},
        
        'Corsair Vengeance RGB Pro 32GB': {'brand': 'Corsair', 'model': 'Vengeance RGB Pro', 'size': 32, 'type': 'DDR4', 'frequency': 3600, 'timing': 'CL18', 'price': 11000, 'rating': 4, 'release_year': 2019},
        'Corsair Vengeance LPX 16GB': {'brand': 'Corsair', 'model': 'Vengeance LPX', 'size': 16, 'type': 'DDR4', 'frequency': 3200, 'timing': 'CL16', 'price': 5500, 'rating': 4, 'release_year': 2017},
    },
    'motherboard': {
        # Материнские платы для Intel
        'ASUS ROG Maximus Z790 Hero': {'brand': 'ASUS', 'model': 'ROG Maximus Z790 Hero', 'socket': 'LGA1700', 'chipset': 'Z790', 'memory_type': 'DDR5', 'price': 55000, 'rating': 5, 'release_year': 2022},
        'Gigabyte Z790 AORUS Master': {'brand': 'Gigabyte', 'model': 'Z790 AORUS Master', 'socket': 'LGA1700', 'chipset': 'Z790', 'memory_type': 'DDR5', 'price': 45000, 'rating': 5, 'release_year': 2022},
        'MSI MPG Z790 Carbon WiFi': {'brand': 'MSI', 'model': 'MPG Z790 Carbon WiFi', 'socket': 'LGA1700', 'chipset': 'Z790', 'memory_type': 'DDR5', 'price': 40000, 'rating': 4, 'release_year': 2022},
        'ASRock Z790 Taichi': {'brand': 'ASRock', 'model': 'Z790 Taichi', 'socket': 'LGA1700', 'chipset': 'Z790', 'memory_type': 'DDR5', 'price': 42000, 'rating': 4, 'release_year': 2022},
        
        'ASUS ROG Strix Z690-E Gaming': {'brand': 'ASUS', 'model': 'ROG Strix Z690-E Gaming', 'socket': 'LGA1700', 'chipset': 'Z690', 'memory_type': 'DDR5', 'price': 35000, 'rating': 4, 'release_year': 2021},
        'MSI MAG Z690 Tomahawk': {'brand': 'MSI', 'model': 'MAG Z690 Tomahawk', 'socket': 'LGA1700', 'chipset': 'Z690', 'memory_type': 'DDR4', 'price': 25000, 'rating': 4, 'release_year': 2021},
        
        'ASUS ROG Maximus XIII Hero': {'brand': 'ASUS', 'model': 'ROG Maximus XIII Hero', 'socket': 'LGA1200', 'chipset': 'Z590', 'memory_type': 'DDR4', 'price': 30000, 'rating': 4, 'release_year': 2021},
        'Gigabyte Z590 AORUS Ultra': {'brand': 'Gigabyte', 'model': 'Z590 AORUS Ultra', 'socket': 'LGA1200', 'chipset': 'Z590', 'memory_type': 'DDR4', 'price': 25000, 'rating': 4, 'release_year': 2021},
        
        # Материнские платы для AMD
        'ASUS ROG Strix X670E-E Gaming': {'brand': 'ASUS', 'model': 'ROG Strix X670E-E Gaming', 'socket': 'AM5', 'chipset': 'X670E', 'memory_type': 'DDR5', 'price': 48000, 'rating': 5, 'release_year': 2022},
        'Gigabyte X670E AORUS Master': {'brand': 'Gigabyte', 'model': 'X670E AORUS Master', 'socket': 'AM5', 'chipset': 'X670E', 'memory_type': 'DDR5', 'price': 46000, 'rating': 5, 'release_year': 2022},
        'MSI MEG X670E ACE': {'brand': 'MSI', 'model': 'MEG X670E ACE', 'socket': 'AM5', 'chipset': 'X670E', 'memory_type': 'DDR5', 'price': 52000, 'rating': 5, 'release_year': 2022},
        
        'ASUS ROG Crosshair X570 Dark Hero': {'brand': 'ASUS', 'model': 'ROG Crosshair X570 Dark Hero', 'socket': 'AM4', 'chipset': 'X570', 'memory_type': 'DDR4', 'price': 35000, 'rating': 5, 'release_year': 2020},
        'MSI MPG X570 Gaming Pro Carbon': {'brand': 'MSI', 'model': 'MPG X570 Gaming Pro Carbon', 'socket': 'AM4', 'chipset': 'X570', 'memory_type': 'DDR4', 'price': 25000, 'rating': 4, 'release_year': 2019},
        'Gigabyte B550 AORUS Pro AC': {'brand': 'Gigabyte', 'model': 'B550 AORUS Pro AC', 'socket': 'AM4', 'chipset': 'B550', 'memory_type': 'DDR4', 'price': 18000, 'rating': 4, 'release_year': 2020},
    },
    'ssd': {
        # SSD NVMe PCIe 4.0
        'Samsung 990 Pro 2TB': {'brand': 'Samsung', 'model': '990 Pro', 'capacity': 2000, 'type': 'NVMe PCIe 4.0', 'read_speed': 7450, 'write_speed': 6900, 'price': 15000, 'rating': 5, 'release_year': 2022},
        'Samsung 990 Pro 1TB': {'brand': 'Samsung', 'model': '990 Pro', 'capacity': 1000, 'type': 'NVMe PCIe 4.0', 'read_speed': 7450, 'write_speed': 6900, 'price': 9000, 'rating': 5, 'release_year': 2022},
        'WD Black SN850X 2TB': {'brand': 'WD', 'model': 'Black SN850X', 'capacity': 2000, 'type': 'NVMe PCIe 4.0', 'read_speed': 7300, 'write_speed': 6600, 'price': 13000, 'rating': 5, 'release_year': 2022},
        'WD Black SN850X 1TB': {'brand': 'WD', 'model': 'Black SN850X', 'capacity': 1000, 'type': 'NVMe PCIe 4.0', 'read_speed': 7300, 'write_speed': 6300, 'price': 8000, 'rating': 5, 'release_year': 2022},
        'Crucial P5 Plus 2TB': {'brand': 'Crucial', 'model': 'P5 Plus', 'capacity': 2000, 'type': 'NVMe PCIe 4.0', 'read_speed': 6600, 'write_speed': 5000, 'price': 11000, 'rating': 4, 'release_year': 2021},
        'Kingston KC3000 2TB': {'brand': 'Kingston', 'model': 'KC3000', 'capacity': 2000, 'type': 'NVMe PCIe 4.0', 'read_speed': 7000, 'write_speed': 7000, 'price': 14000, 'rating': 5, 'release_year': 2021},
        
        # SSD NVMe PCIe 3.0
        'Samsung 980 Pro 1TB': {'brand': 'Samsung', 'model': '980 Pro', 'capacity': 1000, 'type': 'NVMe PCIe 4.0', 'read_speed': 7000, 'write_speed': 5000, 'price': 9000, 'rating': 5, 'release_year': 2020},
        'Samsung 970 Evo Plus 1TB': {'brand': 'Samsung', 'model': '970 Evo Plus', 'capacity': 1000, 'type': 'NVMe PCIe 3.0', 'read_speed': 3500, 'write_speed': 3300, 'price': 7000, 'rating': 4, 'release_year': 2019},
        'WD Blue SN570 1TB': {'brand': 'WD', 'model': 'Blue SN570', 'capacity': 1000, 'type': 'NVMe PCIe 3.0', 'read_speed': 3500, 'write_speed': 3000, 'price': 6000, 'rating': 4, 'release_year': 2021},
        'Crucial P3 1TB': {'brand': 'Crucial', 'model': 'P3', 'capacity': 1000, 'type': 'NVMe PCIe 3.0', 'read_speed': 3500, 'write_speed': 3000, 'price': 5500, 'rating': 3, 'release_year': 2022},
        
        # SATA SSD
        'Samsung 870 Evo 1TB': {'brand': 'Samsung', 'model': '870 Evo', 'capacity': 1000, 'type': 'SATA III', 'read_speed': 560, 'write_speed': 530, 'price': 8000, 'rating': 4, 'release_year': 2021},
        'Crucial MX500 1TB': {'brand': 'Crucial', 'model': 'MX500', 'capacity': 1000, 'type': 'SATA III', 'read_speed': 560, 'write_speed': 510, 'price': 7000, 'rating': 4, 'release_year': 2018},
        'WD Blue 3D NAND 1TB': {'brand': 'WD', 'model': 'Blue 3D NAND', 'capacity': 1000, 'type': 'SATA III', 'read_speed': 560, 'write_speed': 530, 'price': 7500, 'rating': 4, 'release_year': 2017},
    }
}

# Добавить после существующих маршрутов
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/')
def index():
    return render_template('index.html', components=components_data)

@app.route('/compare', methods=['POST'])
def compare():
    selected_components = []
    
    # Получаем выбранные компоненты из формы
    for category in components_data:
        selected = request.form.getlist(category)
        for item in selected:
            if item in components_data[category]:
                component = components_data[category][item].copy()
                component['type'] = category.upper()
                component['name'] = item
                selected_components.append(component)
    
    # Проверяем, что выбрано от 2 до 5 компонентов
    if len(selected_components) < 2:
        error = "Пожалуйста, выберите как минимум 2 компонента для сравнения."
        return render_template('index.html', components=components_data, error=error)
    elif len(selected_components) > 5:
        error = "Пожалуйста, выберите не более 5 компонентов для сравнения."
        return render_template('index.html', components=components_data, error=error)
    
    return render_template('results.html', components=selected_components)

if __name__ == '__main__':
    app.run(debug=True)