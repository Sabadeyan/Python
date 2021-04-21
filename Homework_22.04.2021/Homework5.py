def show_employee_basic_data (name,age):
    print("Name>",name,"; Age >",age)


def show_employee(employee,salary=9000):
    print("Employee >",employee,"Salery>",salary)




def show_whole_employee_info (name,age,salary=9000):
    show_employee_basic_data(name,age)
    show_employee(name,salary)

show_whole_employee_info("Vardan",28,500000)


