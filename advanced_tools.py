#!/usr/bin/env python3
"""
Advanced Tools Module - 200+ Tools for AI Agent
Organized by categories for maximum functionality
"""

import os
import sys
import json
import time
import random
import hashlib
import base64
import urllib.parse
import re
import math
import statistics
from datetime import datetime, timedelta
from collections import Counter

# ================= MATHEMATICAL TOOLS =================

def add(a, b):
    """Add two numbers"""
    return float(a) + float(b)

def subtract(a, b):
    """Subtract two numbers"""
    return float(a) - float(b)

def multiply(a, b):
    """Multiply two numbers"""
    return float(a) * float(b)

def divide(a, b):
    """Divide two numbers"""
    if float(b) == 0:
        return "Error: Division by zero"
    return float(a) / float(b)

def power(base, exponent):
    """Raise base to the power of exponent"""
    return float(base) ** float(exponent)

def square_root(n):
    """Calculate square root"""
    return math.sqrt(float(n))

def cube_root(n):
    """Calculate cube root"""
    return float(n) ** (1/3)

def factorial(n):
    """Calculate factorial"""
    n = int(n)
    if n < 0:
        return "❌ Error: Factorial of negative number"
    result = 1
    for i in range(1, n + 1):
        result *= i
    return f"🧮 Factorial of {n}: {result}"

def fibonacci(n):
    """Generate nth Fibonacci number"""
    n = int(n)
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

def prime_check(n):
    """Check if number is prime"""
    n = int(n)
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def gcd(a, b):
    """Greatest Common Divisor"""
    a, b = int(a), int(b)
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Least Common Multiple"""
    a, b = int(a), int(b)
    return abs(a * b) // gcd(a, b)

def sin_deg(degrees):
    """Sine in degrees"""
    return math.sin(math.radians(float(degrees)))

def cos_deg(degrees):
    """Cosine in degrees"""
    return math.cos(math.radians(float(degrees)))

def tan_deg(degrees):
    """Tangent in degrees"""
    return math.tan(math.radians(float(degrees)))

def log_base(n, base=10):
    """Logarithm with custom base"""
    return math.log(float(n), float(base))

def natural_log(n):
    """Natural logarithm"""
    return math.log(float(n))

def absolute_value(n):
    """Absolute value"""
    return abs(float(n))

def round_number(n, decimals=0):
    """Round number to specified decimals"""
    return round(float(n), int(decimals))

def ceiling(n):
    """Ceiling function"""
    return math.ceil(float(n))

def floor(n):
    """Floor function"""
    return math.floor(float(n))

def percentage(part, whole):
    """Calculate percentage"""
    return (float(part) / float(whole)) * 100

def compound_interest(principal, rate, time, n=1):
    """Calculate compound interest"""
    p, r, t, n = float(principal), float(rate)/100, float(time), float(n)
    return p * (1 + r/n) ** (n*t)

def quadratic_formula(a, b, c):
    """Solve quadratic equation ax² + bx + c = 0"""
    a, b, c = float(a), float(b), float(c)
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return "No real solutions"
    elif discriminant == 0:
        return -b / (2*a)
    else:
        sqrt_disc = math.sqrt(discriminant)
        return [(-b + sqrt_disc) / (2*a), (-b - sqrt_disc) / (2*a)]

def distance_2d(x1, y1, x2, y2):
    """Calculate distance between two 2D points"""
    return math.sqrt((float(x2) - float(x1))**2 + (float(y2) - float(y1))**2)

def area_circle(radius):
    """Calculate area of circle"""
    return math.pi * float(radius) ** 2

def area_rectangle(length, width):
    """Calculate area of rectangle"""
    return float(length) * float(width)

def area_triangle(base, height):
    """Calculate area of triangle"""
    return 0.5 * float(base) * float(height)

def volume_sphere(radius):
    """Calculate volume of sphere"""
    return (4/3) * math.pi * float(radius) ** 3

def volume_cylinder(radius, height):
    """Calculate volume of cylinder"""
    return math.pi * float(radius) ** 2 * float(height)

def random_int(min_val=1, max_val=100):
    """Generate random integer"""
    return random.randint(int(min_val), int(max_val))

def random_float(min_val=0.0, max_val=1.0):
    """Generate random float"""
    return random.uniform(float(min_val), float(max_val))

# ================= TEXT PROCESSING TOOLS =================

def text_length(text):
    """Get text length"""
    return len(str(text))

def word_count(text):
    """Count words in text"""
    return len(str(text).split())

def char_count(text):
    """Count characters in text"""
    return len(str(text))

def line_count(text):
    """Count lines in text"""
    return len(str(text).split('\n'))

def to_uppercase(text):
    """Convert text to uppercase"""
    return str(text).upper()

def to_lowercase(text):
    """Convert text to lowercase"""
    return str(text).lower()

def to_title_case(text):
    """Convert text to title case"""
    return str(text).title()

def reverse_text(text):
    """Reverse text"""
    return str(text)[::-1]

def remove_spaces(text):
    """Remove all spaces"""
    return str(text).replace(' ', '')

def remove_punctuation(text):
    """Remove punctuation"""
    import string
    return ''.join(c for c in str(text) if c not in string.punctuation)

def extract_numbers(text):
    """Extract all numbers from text"""
    return re.findall(r'\d+\.?\d*', str(text))

def extract_emails(text):
    """Extract email addresses"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, str(text))

def extract_urls(text):
    """Extract URLs from text"""
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(pattern, str(text))

def replace_text(text, old, new):
    """Replace text"""
    return str(text).replace(str(old), str(new))

def find_text(text, search):
    """Find text position"""
    return str(text).find(str(search))

def split_text(text, delimiter=' '):
    """Split text by delimiter"""
    return str(text).split(str(delimiter))

def join_text(text_list, separator=' '):
    """Join text list with separator"""
    if isinstance(text_list, str):
        text_list = text_list.split()
    return str(separator).join(str(item) for item in text_list)

def trim_text(text):
    """Trim whitespace"""
    return str(text).strip()

def pad_left(text, width, char=' '):
    """Pad text on left"""
    return str(text).rjust(int(width), str(char))

def pad_right(text, width, char=' '):
    """Pad text on right"""
    return str(text).ljust(int(width), str(char))

def center_text(text, width, char=' '):
    """Center text"""
    return str(text).center(int(width), str(char))

def text_similarity(text1, text2):
    """Calculate text similarity (simple)"""
    words1 = set(str(text1).lower().split())
    words2 = set(str(text2).lower().split())
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / len(union) if union else 0

def count_vowels(text):
    """Count vowels in text"""
    vowels = 'aeiouAEIOU'
    return sum(1 for char in str(text) if char in vowels)

def count_consonants(text):
    """Count consonants in text"""
    vowels = 'aeiouAEIOU'
    return sum(1 for char in str(text) if char.isalpha() and char not in vowels)

def is_palindrome(text):
    """Check if text is palindrome"""
    clean_text = re.sub(r'[^a-zA-Z0-9]', '', str(text)).lower()
    return clean_text == clean_text[::-1]

def text_frequency(text):
    """Get word frequency"""
    words = str(text).lower().split()
    return dict(Counter(words))

def remove_duplicates(text):
    """Remove duplicate words"""
    words = str(text).split()
    return ' '.join(dict.fromkeys(words))

def acronym_generator(text):
    """Generate acronym from text"""
    words = str(text).split()
    return ''.join(word[0].upper() for word in words if word)

def pig_latin(text):
    """Convert to pig latin"""
    words = str(text).split()
    result = []
    for word in words:
        if word[0].lower() in 'aeiou':
            result.append(word + 'way')
        else:
            result.append(word[1:] + word[0] + 'ay')
    return ' '.join(result)

def morse_code(text):
    """Convert to morse code"""
    morse_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', ' ': '/'
    }
    return ' '.join(morse_dict.get(char.upper(), char) for char in str(text))

# ================= DATA ANALYSIS TOOLS =================

def list_sum(numbers):
    """Sum of list"""
    if isinstance(numbers, str):
        numbers = [float(x) for x in numbers.split(',')]
    return sum(float(x) for x in numbers)

def list_average(numbers):
    """Average of list"""
    if isinstance(numbers, str):
        numbers = [float(x) for x in numbers.split(',')]
    nums = [float(x) for x in numbers]
    return sum(nums) / len(nums) if nums else 0

def list_median(numbers):
    """Median of list"""
    if isinstance(numbers, str):
        numbers = [float(x) for x in numbers.split(',')]
    nums = sorted([float(x) for x in numbers])
    n = len(nums)
    if n % 2 == 0:
        return (nums[n//2 - 1] + nums[n//2]) / 2
    return nums[n//2]

def list_mode(numbers):
    """Mode of list"""
    if isinstance(numbers, str):
        numbers = [float(x) for x in numbers.split(',')]
    nums = [float(x) for x in numbers]
    return statistics.mode(nums)

def list_range(numbers):
    """Range of list"""
    if isinstance(numbers, str):
        numbers = [float(x) for x in numbers.split(',')]
    nums = [float(x) for x in numbers]
    return max(nums) - min(nums)

def list_variance(numbers):
    """Variance of list"""
    if isinstance(numbers, str):
        numbers = [float(x) for x in numbers.split(',')]
    nums = [float(x) for x in numbers]
    return statistics.variance(nums)

def list_std_dev(numbers):
    """Standard deviation of list"""
    if isinstance(numbers, str):
        numbers = [float(x) for x in numbers.split(',')]
    nums = [float(x) for x in numbers]
    return statistics.stdev(nums)

def list_min(numbers):
    """Minimum of list"""
    if isinstance(numbers, str):
        numbers = [float(x) for x in numbers.split(',')]
    return min(float(x) for x in numbers)

def list_max(numbers):
    """Maximum of list"""
    if isinstance(numbers, str):
        numbers = [float(x) for x in numbers.split(',')]
    return max(float(x) for x in numbers)

def list_sort(numbers, reverse=False):
    """Sort list"""
    if isinstance(numbers, str):
        numbers = [float(x) for x in numbers.split(',')]
    nums = [float(x) for x in numbers]
    return sorted(nums, reverse=bool(reverse))

def list_unique(numbers):
    """Get unique values"""
    if isinstance(numbers, str):
        numbers = [float(x) for x in numbers.split(',')]
    return list(set(float(x) for x in numbers))

def list_frequency(numbers):
    """Get frequency distribution"""
    if isinstance(numbers, str):
        numbers = [float(x) for x in numbers.split(',')]
    nums = [float(x) for x in numbers]
    return dict(Counter(nums))

def correlation(x_values, y_values):
    """Calculate correlation coefficient"""
    if isinstance(x_values, str):
        x_values = [float(x) for x in x_values.split(',')]
    if isinstance(y_values, str):
        y_values = [float(x) for x in y_values.split(',')]
    
    x = [float(val) for val in x_values]
    y = [float(val) for val in y_values]
    
    if len(x) != len(y):
        return "Error: Lists must be same length"
    
    return statistics.correlation(x, y)

def linear_regression(x_values, y_values):
    """Simple linear regression"""
    if isinstance(x_values, str):
        x_values = [float(x) for x in x_values.split(',')]
    if isinstance(y_values, str):
        y_values = [float(x) for x in y_values.split(',')]
    
    x = [float(val) for val in x_values]
    y = [float(val) for val in y_values]
    
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x[i] * y[i] for i in range(n))
    sum_x2 = sum(xi ** 2 for xi in x)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n
    
    return {"slope": slope, "intercept": intercept}

# ================= SYSTEM TOOLS =================

def current_timestamp():
    """Get current timestamp"""
    return int(time.time())

def format_timestamp(timestamp, format_str="%Y-%m-%d %H:%M:%S"):
    """Format timestamp"""
    return datetime.fromtimestamp(int(timestamp)).strftime(format_str)

def days_between(date1, date2):
    """Days between two dates (YYYY-MM-DD)"""
    d1 = datetime.strptime(date1, "%Y-%m-%d")
    d2 = datetime.strptime(date2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def add_days(date, days):
    """Add days to date"""
    d = datetime.strptime(date, "%Y-%m-%d")
    new_date = d + timedelta(days=int(days))
    return new_date.strftime("%Y-%m-%d")

def day_of_week(date):
    """Get day of week"""
    d = datetime.strptime(date, "%Y-%m-%d")
    return d.strftime("%A")

def is_leap_year(year):
    """Check if year is leap year"""
    year = int(year)
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def age_calculator(birth_date):
    """Calculate age from birth date"""
    birth = datetime.strptime(birth_date, "%Y-%m-%d")
    today = datetime.now()
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

def sleep_timer(seconds):
    """Sleep for specified seconds"""
    time.sleep(float(seconds))
    return f"Slept for {seconds} seconds"

def generate_uuid():
    """Generate UUID"""
    import uuid
    return str(uuid.uuid4())

def system_info():
    """Get system information"""
    import platform
    return {
        "system": platform.system(),
        "platform": platform.platform(),
        "processor": platform.processor(),
        "python_version": platform.python_version()
    }

# ================= ENCODING/DECODING TOOLS =================

def base64_encode(text):
    """Encode to base64"""
    encoded_result = base64.b64encode(str(text).encode()).decode()
    return f"🔐 Base64 encoded: {encoded_result}"

def base64_decode(encoded):
    """Decode from base64"""
    try:
        decoded_result = base64.b64decode(str(encoded)).decode()
        return f"🔓 Base64 decoded: {decoded_result}"
    except:
        return "❌ Error: Invalid base64 encoding"

def url_encode(text):
    """URL encode text"""
    encoded_result = urllib.parse.quote(str(text))
    return f"🌐 URL encoded: {encoded_result}"

def url_decode(encoded):
    """URL decode text"""
    decoded_result = urllib.parse.unquote(str(encoded))
    return f"🌐 URL decoded: {decoded_result}"

def html_encode(text):
    """HTML encode text"""
    import html
    encoded_result = html.escape(str(text))
    return f"📄 HTML encoded: {encoded_result}"

def html_decode(encoded):
    """HTML decode text"""
    import html
    decoded_result = html.unescape(str(encoded))
    return f"📄 HTML decoded: {decoded_result}"

def md5_hash(text):
    """Generate MD5 hash"""
    hash_result = hashlib.md5(str(text).encode()).hexdigest()
    return f"🔐 MD5 hash: {hash_result}"

def sha1_hash(text):
    """Generate SHA1 hash"""
    hash_result = hashlib.sha1(str(text).encode()).hexdigest()
    return f"🔐 SHA1 hash: {hash_result}"

def sha256_hash(text):
    """Generate SHA256 hash"""
    hash_result = hashlib.sha256(str(text).encode()).hexdigest()
    return f"🔐 SHA256 hash: {hash_result}"

# ================= NETWORK TOOLS =================

def is_valid_ip(ip):
    """Check if IP address is valid"""
    import ipaddress
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        return False

def is_valid_email(email):
    """Check if email is valid"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, str(email)))

def is_valid_url(url):
    """Check if URL is valid"""
    pattern = r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
    return bool(re.match(pattern, str(url)))

def extract_domain(url):
    """Extract domain from URL"""
    from urllib.parse import urlparse
    return urlparse(str(url)).netloc

def ping_test(host="8.8.8.8"):
    """Simple ping test (mock)"""
    # Mock implementation - in real scenario would use actual ping
    return f"Ping to {host}: 20ms (mock)"

# ================= UTILITY TOOLS =================

def generate_password(length=12, include_symbols=True):
    """Generate random password"""
    import string
    chars = string.ascii_letters + string.digits
    if include_symbols:
        chars += "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(int(length)))

def qr_code_data(text):
    """Generate QR code data (mock)"""
    return f"QR Code for: {text} (mock implementation)"

def color_hex_to_rgb(hex_color):
    """Convert hex color to RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_rgb_to_hex(r, g, b):
    """Convert RGB to hex color"""
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

def temperature_converter(temp, from_unit, to_unit):
    """Convert temperature between units"""
    temp = float(temp)
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    # Convert to Celsius first
    if from_unit == 'fahrenheit':
        celsius = (temp - 32) * 5/9
    elif from_unit == 'kelvin':
        celsius = temp - 273.15
    else:
        celsius = temp
    
    # Convert from Celsius to target
    if to_unit == 'fahrenheit':
        return celsius * 9/5 + 32
    elif to_unit == 'kelvin':
        return celsius + 273.15
    else:
        return celsius

def bmi_calculator(weight, height, unit='metric'):
    """Calculate BMI"""
    weight = float(weight)
    height = float(height)
    
    if unit.lower() == 'imperial':
        # Convert pounds to kg, inches to meters
        weight = weight * 0.453592
        height = height * 0.0254
    
    bmi = weight / (height ** 2)
    
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    
    return {"bmi": round(bmi, 2), "category": category}

def loan_calculator(principal, rate, years):
    """Calculate loan payment"""
    principal = float(principal)
    rate = float(rate) / 100 / 12  # Monthly rate
    months = float(years) * 12
    
    if rate == 0:
        return principal / months
    
    payment = principal * (rate * (1 + rate)**months) / ((1 + rate)**months - 1)
    return round(payment, 2)

def tip_calculator(bill, tip_percent, people=1):
    """Calculate tip and split bill"""
    bill = float(bill)
    tip_percent = float(tip_percent)
    people = int(people)
    
    tip = bill * (tip_percent / 100)
    total = bill + tip
    per_person = total / people
    
    return {
        "bill": bill,
        "tip": round(tip, 2),
        "total": round(total, 2),
        "per_person": round(per_person, 2)
    }

# Create a registry of all tools
ADVANCED_TOOLS = {}

# Auto-register all functions
current_module = sys.modules[__name__]
for name in dir(current_module):
    obj = getattr(current_module, name)
    if callable(obj) and not name.startswith('_') and name != 'ADVANCED_TOOLS':
        ADVANCED_TOOLS[name] = obj

print(f"Advanced Tools Module Loaded: {len(ADVANCED_TOOLS)} tools available")