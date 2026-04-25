import time

user_input = str(input('Enter the time in hour, mins or secs: '))

alphabets = ''.join(char for char in user_input if char.isalpha())
numbers = ''.join(char for char in user_input if char.isdigit())

if alphabets.lower() == 'hours' or alphabets == 'hour':
    my_time = int(numbers) * 3600
elif alphabets.lower() == 'mins' or alphabets == 'min':
    my_time = int(numbers) * 60
elif alphabets.lower() == 'secs' or alphabets == 'sec':
    my_time = int(numbers) * 1
else:
    print('Invalid input')


my_times = int(my_time)

for x in range(my_times, 0, -1):
    seconds = x % 60
    minutes = int(x/60)%60
    hours = int(x/3600)
    print(f'{hours:02}:{minutes:02}:{seconds:02}')
    time.sleep(1)
print("TIME'S UP!")