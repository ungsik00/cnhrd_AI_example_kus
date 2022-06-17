'''
def celsius_to_fahrenheit(celsius):
    return celsius * 1.8 + 32

if __name__ == "__main__":
    celsius_value = int(input('섭씨 온도를 입력.\n'))

    fahrenheit_value = celsius_to_fahrenheit(celsius_value)

    print('화씨 온도로', fahrenheit_value)
'''

from tensorflow.keras.model import Sequential
