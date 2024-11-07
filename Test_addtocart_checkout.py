from tkinter.tix import Select
from driver import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import UnexpectedAlertPresentException

#TC1
def test_add_product_to_cart(driver):
    driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div/div/ul/li[2]/a").click() 
    time.sleep(2)

    driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div[2]/div/div/div[1]/div/div[2]/p/a").click()  
    time.sleep(2)

    driver.find_element(By.NAME, "form_add_to_cart").click()  

    driver.find_element(By.XPATH,"/html/body/div[3]/div/div/div[2]/ul/li[3]/a").click()
    time.sleep(2)


    assert "Amazfit GTS 3 Smart Watch for Android iPhone" in driver.page_source  
    
#TC2
def test_remove_product_from_cart(driver):
    # Add the product to the cart first
    test_add_product_to_cart(driver)
    
    # Find the cart table
    table = driver.find_element(By.CLASS_NAME, "table")

    # Go through all the rows in the cart table
    rows = table.find_elements(By.TAG_NAME, "tr")
    
    product_name = "Amazfit GTS 3 Smart Watch for Android iPhone"  # Define the product name
    
    # Loop through each row in the table
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")

    # Check if the row contains more than one column (to avoid header row)
    if len(columns) > 1:
        # Get the product name from the cart
        product_name_in_cart = columns[2].text

        # If the product name matches, click to remove it
        if product_name == product_name_in_cart:
                remove_button = driver.find_element(By.CLASS_NAME, "trash")  # Assuming remove button is in 4th column
                remove_button.click()
                time.sleep(2)

        # After removal, check that the product is no longer in the cart
        assert product_name not in driver.page_source


#TC3
def test_update_item_quantity_in_cart(driver):
    test_add_product_to_cart(driver)
     
    # Find the cart table
    table = driver.find_element(By.CLASS_NAME, "table")

    # Go through all the rows in the cart table
    rows = table.find_elements(By.TAG_NAME, "tr")
    
    product_name = "Amazfit GTS 3 Smart Watch for Android iPhone"  # Define the product name
    
    # Loop through the rows to find the item and change the quantity
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        
    if len(columns) > 1:
        # Check the product name
        product_name_in_cart = columns[2].text  # Assuming product name is in the 3rd column

        if product_name == product_name_in_cart:
            # Find the quantity field and update it
            quantity_input = driver.find_element(By.CLASS_NAME, "input-text")  # Assuming the quantity input is in the 5th column
            quantity_input.clear()
            quantity_input.send_keys("2")  # Set the new quantity, for example "2"
                
            # Click the "Update Cart" button
            driver.find_element(By.NAME, "form1").click()
            time.sleep(2)


        # After updating, verify the updated quantity and price
        updated_quantity = driver.find_element(By.CLASS_NAME, "input-text").get_attribute("value")
        updated_price = driver.find_element(By.CLASS_NAME, "text-right").text 

        assert updated_quantity == "2"  # Assert that the updated quantity is now 2
        assert "Total Price: $..." in updated_price  # Replace with the expected total price after update
    
#TC4
def test_bankDeposit_payment(driver):
    driver.find_element(By.LINK_TEXT, "Login").click()  
    time.sleep(2)
    driver.find_element(By.NAME, "cust_email").send_keys("testuser@example.com")
    driver.find_element(By.NAME, "cust_password").send_keys("Password123")
    driver.find_element(By.NAME, "form1").click()  
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[text()='Update Billing and Shipping Info']").click()
    time.sleep(2)

    if not is_billing_address_filled(driver):
        update_billing_address(driver)
        
    if not is_shipping_address_filled(driver):
        update_shipping_address(driver)

    test_add_product_to_cart(driver)

    driver.find_element(By.XPATH, "//a[@href='checkout.php']").click()
    time.sleep(2)

    # Open the dropdown for payment method
    driver.find_element(By.ID, "select2-advFieldsStatus-container").click()  # This clicks the dropdown

    # Select "Bank Deposit" from the dropdown
    bank_deposit_option = driver.find_element(By.XPATH, "//li[contains(text(), 'Bank Deposit')]")
    bank_deposit_option.click()
    time.sleep(2)

    driver.find_element(By.NAME, "transaction_info").send_keys("Please deliver it quickly and carefully!")
    time.sleep(2)

    driver.find_element(By.NAME, "form3").click()
    time.sleep(2)

    success_message = driver.find_element(By.CSS_SELECTOR, "h3").text

    print(f"Success message: {success_message}")  # Debugging line to check the output
    assert "Congratulation! Payment is successful." in success_message

#TC5
def test_checkout_as_paypal(driver):
    driver.find_element(By.LINK_TEXT, "Login").click()  
    time.sleep(2)
    driver.find_element(By.NAME, "cust_email").send_keys("testuser@example.com")
    driver.find_element(By.NAME, "cust_password").send_keys("Password123")
    driver.find_element(By.NAME, "form1").click()  
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[text()='Update Billing and Shipping Info']").click()
    time.sleep(2)

    if not is_billing_address_filled(driver):
        update_billing_address(driver)
        
    if not is_shipping_address_filled(driver):
        update_shipping_address(driver)

    test_add_product_to_cart(driver)

    driver.find_element(By.XPATH, "//a[@href='checkout.php']").click()
    time.sleep(2)

    # Open the dropdown for payment method
    driver.find_element(By.ID, "select2-advFieldsStatus-container").click()  # Click the dropdown to open options

    # Select "PayPal" from the dropdown
    paypal_option = driver.find_element(By.XPATH, "//li[contains(text(), 'PayPal')]")
    paypal_option.click()
    time.sleep(2)

    # Click "Pay now"
    driver.find_element(By.NAME, "form1").click()
    time.sleep(2)

    assert "https://www.paypal.com/webapps/shoppingcart/error?flowlogging_id=f7930417dd231&code=GENERIC_ERROR&mfid=1730703263286_f7930417dd231" in driver.current_url



def is_billing_address_filled(driver):
    required_fields = ["cust_b_name", "cust_b_cname", "cust_b_phone", "cust_b_address", "cust_b_city", "cust_b_state", "cust_b_zip"]
    for field_name in required_fields:
        field_value = driver.find_element(By.NAME, field_name).get_attribute("value")
        if not field_value:
            return False
    return True


# This is a function to check if all fields of Shipping Address are filled and updated
def is_shipping_address_filled(driver):
    required_fields = ["cust_s_name", "cust_s_cname", "cust_s_phone", "cust_s_address", "cust_s_city", "cust_s_state", "cust_s_zip"]
    for field_name in required_fields:
        field_value = driver.find_element(By.NAME, field_name).get_attribute("value")
        if not field_value:
            return False
    return True

# This is a function to fill all fields of Shipping Address to Checkout
def update_shipping_address(driver):
    driver.find_element(By.NAME, "cust_s_name").send_keys("Nguyen Hoang Tien")
    time.sleep(1.5)

    driver.find_element(By.NAME, "cust_s_cname").send_keys("SGU")
    time.sleep(1.5)

    driver.find_element(By.NAME, "cust_s_phone").send_keys("0383161867")
    time.sleep(1.5)

    select_element = driver.find_element(By.NAME, "cust_s_country")
    select_element.click()

    # Tìm các tùy chọn trong dropdown và chọn "Vietnam"
    country_option = driver.find_element(By.XPATH, "//option[@value='237']")
    country_option.click()
    time.sleep(1.5)

    driver.find_element(By.NAME, "cust_s_address").send_keys("112 Huynh Ba Chanh")
    time.sleep(1.5)

    driver.find_element(By.NAME, "cust_s_city").send_keys("Ho Chi Minh")
    time.sleep(1.5)
    
    driver.find_element(By.NAME, "cust_s_state").send_keys("Mien Nam")
    time.sleep(1.5)

    driver.find_element(By.NAME, "cust_s_zip").send_keys(112233)
    time.sleep(1.5)

# This is a function to fill all fields of Billing Address to Checkout
def update_billing_address(driver):
    driver.find_element(By.NAME, "cust_b_name").send_keys("Nguyen Hoang Tien")
    time.sleep(1.5)

    driver.find_element(By.NAME, "cust_b_cname").send_keys("SGU")
    time.sleep(1.5)

    driver.find_element(By.NAME, "cust_b_phone").send_keys("0383161867")
    time.sleep(1.5)

    select_element = driver.find_element(By.NAME, "cust_b_country")
    select_element.click()

    # Tìm các tùy chọn trong dropdown và chọn "Vietnam"
    country_option = driver.find_element(By.XPATH, "//option[@value='237']")
    country_option.click()
    time.sleep(1.5)

    driver.find_element(By.NAME, "cust_b_address").send_keys("An Duong Vuong")
    time.sleep(1.5)

    driver.find_element(By.NAME, "cust_b_city").send_keys("Ho Chi Minh")
    time.sleep(1.5)
    
    driver.find_element(By.NAME, "cust_b_state").send_keys("Mien Nam")
    time.sleep(1.5)

    driver.find_element(By.NAME, "cust_b_zip").send_keys(112233)
    time.sleep(1.5)


    