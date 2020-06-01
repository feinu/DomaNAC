from time import sleep
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


class DomainsClient:
    """
    Web browser alternative to the domains.co.za API, which is only available
    to domain resellers.
    It's very fragile as it relies on the way their website is laid out.
    """

    def __init__(self, username, password):
        self.baseurl = "https://www.domains.co.za"
        self.username = username
        self.password = password

        opts = Options()
        # opts.set_headless()
        self.browser = Firefox(options=opts)
        self.browser.get(self.baseurl)

    def login(self):
        """
        Input state: loaded domains.co.za
        Output state: logged in
        """
        # Open the login dialog
        login_button = self.browser.find_element_by_id("loginOrRegister")
        login_button.click()
        # Find and fill the username and password fields
        popover = self.browser.find_element_by_class_name("popover-content")
        inputs = popover.find_elements_by_tag_name("input")
        inputs[1].send_keys(self.username)
        inputs[2].send_keys(self.password)
        inputs[2].submit()

    def manage_domains(self):
        """
        Input state: logged in
        Output state: On Domain List Overview screen
        """
        # Click Manage Account
        dropdown = self.browser.find_element_by_id("mainDashNav")
        dropdown.click()
        # Domains is the first subitem
        navitems = dropdown.find_elements_by_class_name("innerNavItem")
        navitems[0].click()

    def manage_dns(self):
        """
        Input state: On Domain List Overview screen
        Output state: On "You are now managing" screen
        """
        # Assuming we're only managing one domain
        domain_row = self.browser.find_elements_by_class_name("regRow")[0]
        manage_button = domain_row.find_elements_by_class_name("dropCaret")[0]
        manage_button.click()
        dns_button = self.browser.find_element_by_class_name("manageDnsBttn")
        dns_button.click()

    def set_dns_entries(self, entries):
        """
        Input state: On "You are now managing" screen
        :param entries: dict of host:IP pairs, excluding the trailing domain
        """
        for input_row in self.browser.find_elements_by_class_name("dnsRowTd"):
            input_cells = input_row.find_elements_by_tag_name("input")
            host_cell = input_cells[0].get_attribute("value")
            if host_cell in entries.keys():
                address_cell = input_cells[4]
                address_cell.clear()
                address_cell.send_keys(entries[host_cell])
                break
        buttons = self.browser.find_elements_by_class_name("bttn")
        save_button = [
            b for b in buttons if b.get_attribute("value") == "Save Changes"
        ][0]
        save_button.click()

    def set_dns_from_scratch(self, entries):
        sleep(2)
        self.login()
        sleep(2)
        self.manage_domains()
        sleep(2)
        self.manage_dns()
        sleep(2)
        self.set_dns_entries(entries)
