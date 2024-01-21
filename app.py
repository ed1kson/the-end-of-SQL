import main 

#funcs and important variables
customer_id = None

def log_in():
    global customer_id
    customer_id = main.get_id_by_email(input('enter your email adress:'))[0][0]
    print('Done')
    if not customer_id:
        answer = True if input('There is no such a user yet. Do you wanna sign up?(yes/no)') == 'yes' else False
        if answer:
            sign_up()
            log_in()
            return True
        else:
            return False

def sign_up():
    first_name = input('enter your first name please:')
    last_name = input('enter your last name please:')
    email = input('enter your email adress please:')
    commit = True if input('Are you sure that you wanna commit changes?(yes/no):') == "yes" else False
    main.sign_up(first_name, last_name, email, commit)
    print('signing up completed!')

def place_an_order():
    global customer_id
    product_id = input('chose a product id from list:'+ str(main.get_products_list()))
    quantity = input('please enter the wished amount of this item please:')
    commit = True if input('Do you want to save changes in database?(yes/no):').lower() == 'yes' else False
    print(customer_id, product_id, quantity, commit)
    main.apply_purchase(customer_id, product_id, quantity, commit)

#the app cycle
run = True
while run:
    print('''
1. Log in
2. Check products
3. Sign up
4. Place an order
5. See full income information
6. See order count per customer
7. See how much money people spend in one order on avarage
0. Exit''')
    answer = int(input('enter your answer (1-5):'))
    if answer == 1:
        log_in()

    elif answer == 2:
        print(main.get_products_list())

    elif answer == 3:
        sign_up()

    elif answer == 4:
        if customer_id:
            place_an_order()
        else:
            print('you have to log in first')
            if log_in():
                place_an_order()

    elif answer == 5:
        print(f'weve earned {int(main.get_all_income())}USD')

    elif answer == 6:
        print("\n{:<5} {:<15} {:<25} {:<3}".format('pos', 'first name','email adress','count'))
        for number, row in enumerate(main.get_order_count_per_customer(), 1):
            first_name, email, count = row
            print("{:<5} {:<15} {:<25} {:<3}".format(number, first_name, email, count))

    elif answer == 7:
        print(f'The avarage money-waste per order is {main.get_avg_check()}USD')

    elif answer == 0:
        run = False
    else:
        print('Please enter a number from 1 to 5:')
